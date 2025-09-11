#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

try:
    from scripts.notify_ai_discovery import send_telegram_message  # type: ignore
except Exception:
    send_telegram_message = None

STATE_FILE = Path("data/publish_state.json")


def load_state():
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def main():
    state = load_state()
    if not state:
        print("No publish state found")
        return 0
    # keys are 'YYYY-MM-DD HH'
    now = datetime.utcnow()
    start = now - timedelta(days=7)
    total = 0
    daily = {}
    for key, cnt in state.items():
        try:
            dt = datetime.strptime(key, "%Y-%m-%d %H")
        except Exception:
            continue
        if dt >= start:
            day_key = dt.strftime("%Y-%m-%d")
            total += int(cnt)
            daily[day_key] = int(daily.get(day_key, 0)) + int(cnt)

    # build message
    lines = ["📅 近7日发布统计:"]
    for day in sorted(daily.keys()):
        lines.append(f"- {day}: {daily[day]} 篇")
    msg = (
        "📊 每周新闻发布报告\n\n" + "\n".join(lines) + f"\n\n✅ 合计: {total} 篇"
    )

    if send_telegram_message and os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        send_telegram_message(msg)
        print("Weekly report sent")
    else:
        print(msg)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

