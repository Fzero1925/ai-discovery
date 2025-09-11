#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from typing import Dict, List


def render_short_news(title: str, summary: Dict, sources: List[Dict]) -> str:
    # summary keys: whats_new, why_matters, context
    lines = [
        f"## {title}",
        "",
        f"【What's new】{summary.get('whats_new','')}",
        f"【Why it matters】{summary.get('why_matters','')}",
        f"【Context】{summary.get('context','')}",
        "",
        "**来源**:",
    ]
    for s in sources[:3]:
        lines.append(f"- [{s.get('name','source')}]({s.get('url','#')})")
    return "\n".join(lines)


def build_frontmatter(title: str, tags: List[str], sources: List[Dict], nqs: float) -> str:
    date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    fm = [
        "---",
        f"title: \"{title}\"",
        f"date: {date}",
        "categories: [\"news\"]",
        f"tags: [{', '.join('"'+t+'"' for t in tags)}]",
        f"draft: true",
        f"nqs_score: {nqs}",
        "sources:",
    ]
    for s in sources[:3]:
        fm.append(f"  - name: \"{s.get('name','source')}\"")
        fm.append(f"    url: \"{s.get('url','#')}\"")
    fm.append("---\n")
    return "\n".join(fm)

