#!/usr/bin/env python3
"""
News Hourly Scheduler

Hourly job:
- Refresh multi-source trending keywords
- Select 5–8 top topics
- Generate articles as drafts (quality >=85) with staggered publish times
- Queue them in data/publish_queue.json for the publisher to release every ~12–18 minutes
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from datetime import datetime, timedelta
import pytz
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.append(str(Path("scripts").resolve()))

from auto_content_pipeline import (
    run_keywords_refresh,
    load_keywords,
    humanize_content,
    build_frontmatter,
    write_article_file,
    slugify,
)
from modules.quality.content_quality_assessor import ContentQualityAssessor
from modules.quality.similarity_guard import SimilarityGuard
from generate_daily_ai_content import generate_ai_tool_review  # type: ignore
try:
    # Inline notification (optional)
    from scripts.notify_ai_discovery import send_telegram_message  # type: ignore
except Exception:
    send_telegram_message = None


QUEUE_FILE = Path("data/publish_queue.json")
CONFIG_FILE = Path("data/scheduler_config.json")


def load_config() -> Dict:
    default = {
        "timezone": "Asia/Shanghai",
        "active_hours": {"start": "08:00", "end": "23:00"},
        "day": {"max_per_hour": 6, "min_interval_minutes": 12, "max_interval_minutes": 18},
        "night": {"policy": "throttle", "max_per_hour": 2, "min_interval_minutes": 20, "max_interval_minutes": 30},
    }
    try:
        if CONFIG_FILE.exists():
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default


def choose_targets(keywords: List[Dict], count_min: int, count_max: int) -> List[Dict]:
    n = random.randint(count_min, count_max)
    ranked = sorted(
        keywords,
        key=lambda x: (
            float(x.get("commercial_intent", 0)),
            float(x.get("trend_score", 0)),
            float(x.get("controversy_score", 0)),
        ),
        reverse=True,
    )
    return ranked[: n * 2]  # pick a buffer; similarity/quality may filter


def is_in_active_hours(dt: datetime, cfg: Dict) -> bool:
    tz = pytz.timezone(cfg.get("timezone", "Asia/Shanghai"))
    local = dt.astimezone(tz)
    start = cfg.get("active_hours", {}).get("start", "08:00")
    end = cfg.get("active_hours", {}).get("end", "23:00")
    s_h, s_m = map(int, start.split(":"))
    e_h, e_m = map(int, end.split(":"))
    local_minutes = local.hour * 60 + local.minute
    start_minutes = s_h * 60 + s_m
    end_minutes = e_h * 60 + e_m
    return start_minutes <= local_minutes <= end_minutes


def next_active_start(dt: datetime, cfg: Dict) -> datetime:
    tz = pytz.timezone(cfg.get("timezone", "Asia/Shanghai"))
    local = dt.astimezone(tz)
    start = cfg.get("active_hours", {}).get("start", "08:00")
    s_h, s_m = map(int, start.split(":"))
    start_today = local.replace(hour=s_h, minute=s_m, second=0, microsecond=0)
    if local <= start_today:
        target_local = start_today
    else:
        target_local = start_today + timedelta(days=1)
    return target_local.astimezone(pytz.utc)


def _get_category_intervals(cfg: Dict, category: str, in_day: bool) -> Tuple[int, int]:
    cat_cfg = (cfg.get("categories", {}) or {}).get(category or "", {})
    key = "day" if in_day else "night"
    if key in cat_cfg:
        v = cat_cfg[key]
        return int(v.get("min_interval_minutes", 12 if in_day else 20)), int(v.get("max_interval_minutes", 18 if in_day else 30))
    base = cfg.get(key, {})
    return int(base.get("min_interval_minutes", 12 if in_day else 20)), int(base.get("max_interval_minutes", 18 if in_day else 30))


def schedule_times(now: datetime, k: int, cfg: Dict) -> List[datetime]:
    times: List[datetime] = []

    def get_interval(dt: datetime) -> tuple[int, int]:
        if is_in_active_hours(dt, cfg):
            d = cfg.get("day", {})
            return int(d.get("min_interval_minutes", 12)), int(d.get("max_interval_minutes", 18))
        n = cfg.get("night", {})
        return int(n.get("min_interval_minutes", 20)), int(n.get("max_interval_minutes", 30))

    min_int, max_int = get_interval(now)
    cursor = now + timedelta(minutes=random.randint(min_int, max_int))
    for _ in range(k):
        if not is_in_active_hours(cursor, cfg):
            policy = cfg.get("night", {}).get("policy", cfg.get("night_policy", "pause"))
            if policy == "pause":
                cursor = next_active_start(cursor, cfg) + timedelta(minutes=random.randint(0, 10))
        times.append(cursor)
        min_int, max_int = get_interval(cursor)
        cursor += timedelta(minutes=random.randint(min_int, max_int))
    return times


def schedule_times_for_items(now: datetime, items: List[Dict], cfg: Dict) -> List[datetime]:
    """Assign per-item publish times honoring category overrides."""
    times: List[datetime] = []
    cursor = now
    for it in items:
        category = (it.get("category") or "").lower()
        in_day = is_in_active_hours(cursor, cfg)
        min_int, max_int = _get_category_intervals(cfg, category, in_day)
        # move cursor forward by category-specific interval
        cursor = cursor + timedelta(minutes=random.randint(min_int, max_int))
        if not is_in_active_hours(cursor, cfg):
            policy = cfg.get("night", {}).get("policy", cfg.get("night_policy", "pause"))
            if policy == "pause":
                cursor = next_active_start(cursor, cfg) + timedelta(minutes=random.randint(0, 10))
        times.append(cursor)
    return times


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
    parser = argparse.ArgumentParser(description="Hourly news scheduler")
    parser.add_argument("--min", type=int, default=5, help="Minimum items to schedule")
    parser.add_argument("--max", type=int, default=8, help="Maximum items to schedule")
    parser.add_argument("--similarity-threshold", type=float, default=0.82, help="Max allowed cosine similarity")
    args = parser.parse_args()

    print("🕐 Running hourly trending refresh...")
    if not run_keywords_refresh():
        print("⚠️ Trending refresh failed; attempting with existing keywords file")

    keywords = load_keywords()
    if not keywords:
        print("🛑 No keywords available; exiting")
        return 1

    assessor = ContentQualityAssessor(min_score=85.0)
    guard = SimilarityGuard(content_dir="content")
    cfg = load_config()

    candidates = choose_targets(keywords, args.min, args.max)
    queued: List[Dict] = load_queue()
    published_paths = {item.get("path") for item in queued}

    scheduled_items: List[Dict] = []
    accepted = 0
    skipped_sim = 0
    skipped_quality = 0

    for kw in candidates:
        if accepted >= args.max:
            break
        name = kw.get("keyword", "AI tool")
        category = kw.get("category", "content_creation")
        print(f"📝 Candidate: {name}")
        try:
            article = generate_ai_tool_review(name, category, kw)
            meta = {
                "title": article.get("title"),
                "description": article.get("metadata", {}).get("description", ""),
                "categories": ["news"],  # IT 新闻类
                "tags": article.get("metadata", {}).get("tags", [name]),
                "featured_image": article.get("metadata", {}).get("featured_image", ""),
                "image_alt": f"{name.title()} news analysis",
                "draft": True,
            }
            body = humanize_content(article.get("content", ""))

            # Similarity guard
            rep = guard.assess(body)
            if rep.max_similarity >= args.similarity_threshold:
                print(f"  ⛔ Similarity too high ({rep.max_similarity:.2f}) with {rep.most_similar_file}")
                skipped_sim += 1
                continue

            # Quality gate
            q = assessor.assess(body, meta)
            if not q.passed:
                improved, _ = assessor.improve(body, meta)
                q2 = assessor.assess(improved, meta)
                if not q2.passed:
                    print(f"  ❌ Quality failed ({q2.score:.1f})")
                    skipped_quality += 1
                    continue
                body = improved
                q = q2

            fm = build_frontmatter(meta, {"score": q.score, "breakdown": q.breakdown, "metrics": q.metrics})
            slug = slugify(f"{name}-news")
            out_path = write_article_file(slug, fm, body, section="articles")

            # Add to queue with publish_at
            scheduled_items.append({
                "path": str(out_path),
                "keyword": name,
                "category": category,
                "queued_at": datetime.utcnow().isoformat() + "Z",
                # publish_at set in a second pass with staggering
            })
            accepted += 1
            print(f"  ✅ Draft queued: {out_path} (score {q.score})")
        except Exception as e:
            print(f"  ⚠️ Generation error: {e}")
            continue

    if not scheduled_items:
        print(f"ℹ️ No items scheduled. Similarity skips: {skipped_sim}, quality skips: {skipped_quality}")
        # Optional Telegram notification for zero additions
        if send_telegram_message and os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
            try:
                msg = (
                    "🕐 每小时新闻入队\n\n"
                    f"⚠️ 本次新增草稿: 0 篇\n"
                    f"🧪 相似度过滤: {skipped_sim} | 质量未达标: {skipped_quality}"
                )
                send_telegram_message(msg)
            except Exception:
                pass
        return 0

    # Assign publish_at times with staggering
    times = schedule_times_for_items(datetime.utcnow(), scheduled_items, cfg)
    for item, t in zip(scheduled_items, times):
        item["publish_at"] = t.isoformat() + "Z"

    # Merge with existing queue (avoid duplicates)
    queued_paths = {q.get("path") for q in queued}
    queued.extend([it for it in scheduled_items if it["path"] not in queued_paths])
    save_queue(queued)

    added = len(scheduled_items)
    total = len(queued)
    print(f"📦 Scheduled {added} drafts with staggered publishing (queue total: {total})")

    # Save schedule report for CI or local use
    report = {
        "added": added,
        "total_queue": total,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "items": scheduled_items,
    }
    Path("data").mkdir(parents=True, exist_ok=True)
    Path("data/schedule_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # Optional Telegram notification
    if send_telegram_message and os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID") and added > 0:
        msg = (
            f"🕐 每小时新闻入队\n\n"
            f"✅ 本次新增草稿: {added} 篇\n"
            f"📦 当前队列: {total} 篇\n"
            f"⏱️ 将在未来1小时内分批自动发布"
        )
        try:
            send_telegram_message(msg)
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
