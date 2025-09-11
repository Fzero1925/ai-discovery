#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict


@dataclass
class NVSScore:
    score: float
    breakdown: Dict[str, float]


class NVSScoring:
    def __init__(self, config_path: str = "config/news_weights.json"):
        self.cfg = json.loads(Path(config_path).read_text(encoding="utf-8")) if Path(config_path).exists() else {
            "weights": {
                "SourceAuthority": 0.25,
                "Novelty": 0.20,
                "Impact": 0.15,
                "Recency": 0.15,
                "SearchDemand": 0.10,
                "SocialVelocity": 0.10,
                "AdValue": 0.05,
            }
        }

    def _recency(self, published_at: str) -> float:
        try:
            dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            hours = max(0.0, (datetime.now(timezone.utc) - dt).total_seconds() / 3600.0)
            return max(0.0, 100.0 * math.exp(-hours / 12.0))  # 12小时衰减
        except Exception:
            return 50.0

    def score_topic(self, topic: Dict) -> NVSScore:
        # 将现有 TrendingTopic 字段映射到 NVS 维度
        w = self.cfg.get("weights", {})
        source = topic.get("source", "")
        authority = 100.0 if ("reuters" in source or "ap" in source or "news_api" in source) else 70.0
        novelty = 100.0 if topic.get("is_new", True) else 50.0
        impact = min(100.0, topic.get("score", 50) + topic.get("controversy_score", 0) * 0.3)
        recency = self._recency(topic.get("timestamp", datetime.now(timezone.utc).isoformat()))
        search = min(100.0, 20 + topic.get("score", 50) * 0.8)
        social = min(100.0, 50 + topic.get("controversy_score", 0) * 0.5)
        advalue = 60.0  # 预设为中高

        breakdown = {
            "SourceAuthority": authority,
            "Novelty": novelty,
            "Impact": impact,
            "Recency": recency,
            "SearchDemand": search,
            "SocialVelocity": social,
            "AdValue": advalue,
        }

        total = sum(breakdown[k] * w.get(k, 0) for k in breakdown)
        return NVSScore(score=total, breakdown=breakdown)

