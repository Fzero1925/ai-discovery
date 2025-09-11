#!/usr/bin/env python3
"""
Queued Publisher

Runs every ~10–15 minutes:
- Reads data/publish_queue.json
- Publishes due items: set draft=false, refresh date, remove publish_at
- Leaves not-yet-due items untouched
"""

from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict

import frontmatter
import os
import pytz
try:
    from scripts.notify_ai_discovery import send_telegram_message  # type: ignore
except Exception:
    send_telegram_message = None

QUEUE_FILE = Path("data/publish_queue.json")
CONFIG_FILE = Path("data/scheduler_config.json")
STATE_FILE = Path("data/publish_state.json")


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


def load_config() -> Dict:
    default = {
        "timezone": "Asia/Shanghai",
        "active_hours": {"start": "08:00", "end": "23:00"},
        "max_per_hour": 6,
    }
    try:
        if CONFIG_FILE.exists():
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default


def is_active_now(cfg: Dict) -> bool:
    tz = pytz.timezone(cfg.get("timezone", "Asia/Shanghai"))
    now = datetime.now(tz)
    start = cfg.get("active_hours", {}).get("start", "08:00")
    end = cfg.get("active_hours", {}).get("end", "23:00")
    s_h, s_m = map(int, start.split(":"))
    e_h, e_m = map(int, end.split(":"))
    local_minutes = now.hour * 60 + now.minute
    return (s_h * 60 + s_m) <= local_minutes <= (e_h * 60 + e_m)


def max_per_hour_now(cfg: Dict) -> int:
    if is_active_now(cfg):
        return int(cfg.get("day", {}).get("max_per_hour", cfg.get("max_per_hour", 6)))
    night = cfg.get("night", {})
    return int(night.get("max_per_hour", cfg.get("max_per_hour", 2)))


def get_published_count_this_hour(cfg: Dict) -> int:
    try:
        state = {}
        if STATE_FILE.exists():
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        tz = pytz.timezone(cfg.get("timezone", "Asia/Shanghai"))
        now = datetime.now(tz)
        key = now.strftime("%Y-%m-%d %H")
        return int(state.get(key, 0))
    except Exception:
        return 0


def inc_published_count_this_hour(cfg: Dict, n: int = 1) -> None:
    try:
        state = {}
        if STATE_FILE.exists():
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        tz = pytz.timezone(cfg.get("timezone", "Asia/Shanghai"))
        now = datetime.now(tz)
        key = now.strftime("%Y-%m-%d %H")
        state[key] = int(state.get(key, 0)) + n
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def is_due(iso_ts: str) -> bool:
    try:
        # Accept both Z and offset
        ts = iso_ts.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts)
        now = datetime.now(timezone.utc)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt <= now
    except Exception:
        return False


def publish_item(path_str: str) -> bool:
    path = Path(path_str)
    if not path.exists():
        print(f"⚠️ File not found: {path}")
        return False
    try:
        post = frontmatter.load(path)
        post["draft"] = False
        post["date"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        if "publish_at" in post:
            del post["publish_at"]
        with path.open("wb") as f:
            frontmatter.dump(post, f)
        return True
    except Exception as e:
        print(f"⚠️ Publish error for {path}: {e}")
        return False


def main():
    cfg = load_config()
    queue = load_queue()
    if not queue:
        print("ℹ️ Queue empty")
        return 0

    remaining: List[Dict] = []
    published = 0

    # Respect active hours and max_per_hour
    # Allow night throttle if configured; otherwise skip outside active hours
    if not is_active_now(cfg):
        policy = cfg.get("night", {}).get("policy", cfg.get("night_policy", "pause"))
        if policy != "throttle":
            print("⏸️ Outside active hours. Skipping publishing this run.")
            return 0
    max_per_hour = max_per_hour_now(cfg)
    already = get_published_count_this_hour(cfg)
    budget = max(0, max_per_hour - already)
    if budget <= 0:
        print("🛑 Hourly publish cap reached. Will resume next run.")
        return 0
    for item in queue:
        publish_at = item.get("publish_at")
        if publish_at and is_due(publish_at) and published < budget:
            if publish_item(item.get("path", "")):
                published += 1
        else:
            remaining.append(item)

    save_queue(remaining)

    # Save publish report
    report = {
        "published": published,
        "remaining": len(remaining),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    Path("data").mkdir(parents=True, exist_ok=True)
    Path("data/publish_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Published {published} item(s); {len(remaining)} remaining in queue")
    if published > 0:
        inc_published_count_this_hour(cfg, published)

    # Optional Telegram notification
    if send_telegram_message and os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID") and published > 0:
        msg = (
            f"📰 队列发布完成\n\n"
            f"🚀 本次发布: {published} 篇\n"
            f"📦 队列剩余: {len(remaining)} 篇"
        )
        try:
            send_telegram_message(msg)
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
