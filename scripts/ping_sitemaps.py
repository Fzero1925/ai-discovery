#!/usr/bin/env python3
"""
Ping search engines with updated sitemaps.
"""

from __future__ import annotations

import os
import sys
import urllib.parse
import urllib.request

BASE = os.getenv("SITE_BASE_URL", "https://ai-discovery-nu.vercel.app")


def ping(url: str) -> None:
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            print(f"Pinged: {url} -> {resp.status}")
    except Exception as e:
        print(f"Ping failed: {url} -> {e}")


def main():
    sitemaps = [
        f"{BASE}/sitemap.xml",
        f"{BASE}/sitemap-news.xml",
    ]
    for sm in sitemaps:
        url = "https://www.google.com/ping?sitemap=" + urllib.parse.quote(sm, safe="")
        ping(url)
    return 0


if __name__ == "__main__":
    sys.exit(main())

