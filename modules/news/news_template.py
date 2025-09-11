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
        name = s.get('name', 'source')
        url = s.get('url', '#')
        lines.append(f"- [{name}]({url})")
    return "\n".join(lines)


def build_frontmatter(title: str, tags: List[str], sources: List[Dict], nqs: float) -> str:
    date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    # build tags yaml list safely
    safe_tags = [t.replace('"', '\\"') for t in tags]
    tags_str = "[" + ", ".join('"%s"' % t for t in safe_tags) + "]"

    fm = [
        "---",
        f"title: \"{title}\"",
        f"date: {date}",
        "categories: [\"news\"]",
        f"tags: {tags_str}",
        f"draft: true",
        f"nqs_score: {nqs}",
        "sources:",
    ]
    for s in sources[:3]:
        name = s.get('name', 'source').replace('"', '\\"')
        url = s.get('url', '#').replace('"', '\\"')
        fm.append(f"  - name: \"{name}\"")
        fm.append(f"    url: \"{url}\"")
    fm.append("---\n")
    return "\n".join(fm)

