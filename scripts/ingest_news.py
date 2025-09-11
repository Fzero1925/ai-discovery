#!/usr/bin/env python3
"""
Ingest news from multi-source detector and queue short news items.
Maps TrendingTopic to NVS, renders short-news template, evaluates NQS (>=85),
and schedules publish_at via existing queue (data/publish_queue.json).
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

from modules.trending_detector.multi_source_detector import MultiSourceTrendDetector
from modules.news.nvs_scoring import NVSScoring
from modules.quality.content_quality_assessor import ContentQualityAssessor
from modules.news.news_template import render_short_news, build_frontmatter


QUEUE_FILE = Path("data/publish_queue.json")


def load_queue() -> List[Dict]:
    if QUEUE_FILE.exists():
        try:
            return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_queue(items: List[Dict]) -> None:
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    detector = MultiSourceTrendDetector()
    topics = detector.get_all_trending_topics(limit=30)
    if not topics:
        print("No topics")
        return 0

    nvs = NVSScoring()
    assessor = ContentQualityAssessor(min_score=85.0)

    queued = load_queue()
    queued_paths = {item.get("path") for item in queued}

    added = 0
    for t in topics:
        s = nvs.score_topic(t.__dict__ if hasattr(t, "__dict__") else t)
        if s.score < 60:
            continue
        title = t.keyword
        # Build summary heuristically
        summary = {
            "whats_new": f"{title} 出现在 {t.source}，热度评分 {t.score}/100。",
            "why_matters": "该事件对行业/用户有潜在影响，值得关注。",
            "context": "基于多源信号自动聚合，具体细节请查看来源链接。",
        }
        sources = [{"name": t.source, "url": t.url or ""}]
        body = render_short_news(title, summary, sources)
        fm = build_frontmatter(title, ["news", title], sources, 0)
        md = fm + body

        # Quality gate (for news体裁，长度短也应合格)
        q = assessor.assess(md, {"title": title, "categories": ["news"], "tags": [title]})
        if not q.passed:
            improved, _ = assessor.improve(md, {"title": title})
            q2 = assessor.assess(improved, {"title": title, "categories": ["news"], "tags": [title]})
            if not q2.passed:
                continue
            md = improved

        # Write file under content/articles for now
        slug = title.lower().replace(" ", "-")
        out_path = Path("content/articles") / f"{slug}-short-{datetime.utcnow().strftime('%Y-%m-%d')}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md, encoding="utf-8")

        # Queue for publishing (spread in next hour)
        publish_at = (datetime.utcnow() + timedelta(minutes=15 * (added + 1))).isoformat() + "Z"
        item = {
            "path": str(out_path),
            "keyword": title,
            "category": "news",
            "queued_at": datetime.utcnow().isoformat() + "Z",
            "publish_at": publish_at,
        }
        if item["path"] not in queued_paths:
            queued.append(item)
            added += 1

        if added >= 5:
            break

    save_queue(queued)
    print(f"Ingested and queued {added} news items")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

