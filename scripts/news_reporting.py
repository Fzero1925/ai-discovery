#!/usr/bin/env python3
"""
Daily News Report to Telegram

Summarize last 24h scheduling and publishing stats and send a concise
Chinese report to Telegram.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from scripts.notify_ai_discovery import send_telegram_message  # type: ignore
except Exception:
    send_telegram_message = None


def safe_load(path: Path):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def main():
    schedule = safe_load(Path("data/schedule_report.json"))
    publish = safe_load(Path("data/publish_report.json"))
    queue = []
    try:
        if Path("data/publish_queue.json").exists():
            queue = json.loads(Path("data/publish_queue.json").read_text(encoding="utf-8"))
    except Exception:
        pass

    added = int(schedule.get("added", 0)) if isinstance(schedule, dict) else 0
    total_queue = int(schedule.get("total_queue", 0)) if isinstance(schedule, dict) else len(queue)
    published = int(publish.get("published", 0)) if isinstance(publish, dict) else 0
    remaining = int(publish.get("remaining", len(queue))) if isinstance(publish, dict) else len(queue)

    msg = (
        "🗞️ 每日新闻自动化报告\n\n"
        f"📥 近24h入队: {added} 篇\n"
        f"🚀 近24h发布: {published} 篇\n"
        f"📦 当前队列: {remaining} 篇\n"
        f"🧩 系统状态: 自动化运行中"
    )

    if send_telegram_message and os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        send_telegram_message(msg)
        print("Daily report sent")
    else:
        print(msg)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

