#!/usr/bin/env python3
"""
Generate Google News sitemap for recent articles.

Scans content/ for items with category "news" modified in last 48 hours and writes
static/sitemap-news.xml with proper namespaces.
"""

from __future__ import annotations

import os
import sys
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict

import frontmatter

CONTENT_DIR = Path("content")
OUTPUT = Path("static/sitemap-news.xml")
BASE_URL = os.getenv("SITE_BASE_URL", "https://ai-discovery-nu.vercel.app")


def collect_recent_articles(hours: int = 48) -> List[Dict]:
    items: List[Dict] = []
    if not CONTENT_DIR.exists():
        return items
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    for md in CONTENT_DIR.rglob("*.md"):
        try:
            post = frontmatter.load(md)
            # Only include news-category posts
            cats = post.get("categories") or []
            if isinstance(cats, str):
                cats = [cats]
            cats = [str(c).lower() for c in cats]
            if "news" not in cats:
                continue
            # Determine date
            dt_str = post.get("date") or post.get("last_updated")
            if dt_str:
                try:
                    dt = datetime.fromisoformat(str(dt_str).replace("Z", "+00:00"))
                except Exception:
                    dt = datetime.now(timezone.utc)
            else:
                dt = datetime.fromtimestamp(md.stat().st_mtime, tz=timezone.utc)
            if dt < cutoff:
                continue
            # Only published
            if bool(post.get("draft", False)):
                continue
            title = post.get("title") or md.stem
            loc = f"{BASE_URL}/{md.relative_to('content').with_suffix('').as_posix()}"
            items.append({
                "loc": loc,
                "title": title,
                "date": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            })
        except Exception:
            continue
    return items


def render_news_sitemap(items: List[Dict]) -> str:
    header = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n"
        "        xmlns:news=\"http://www.google.com/schemas/sitemap-news/0.9\">\n"
    )
    body_parts = []
    for it in items:
        body_parts.append(
            f"  <url>\n"
            f"    <loc>{it['loc']}</loc>\n"
            f"    <news:news>\n"
            f"      <news:publication>\n"
            f"        <news:name>AI Discovery</news:name>\n"
            f"        <news:language>en</news:language>\n"
            f"      </news:publication>\n"
            f"      <news:publication_date>{it['date']}</news:publication_date>\n"
            f"      <news:title>{it['title']}</news:title>\n"
            f"      <news:genres>Blog</news:genres>\n"
            f"    </news:news>\n"
            f"  </url>\n"
        )
    footer = "</urlset>\n"
    return header + "".join(body_parts) + footer


def main():
    items = collect_recent_articles(48)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    xml = render_news_sitemap(items)
    OUTPUT.write_text(xml, encoding="utf-8")
    print(f"🗺️ News sitemap generated with {len(items)} entries at {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
