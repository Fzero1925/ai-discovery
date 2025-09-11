#!/usr/bin/env python3
"""
AI Discovery - Auto Content Pipeline (Quality-Gated)

Goals:
- Pull multi-source trending keywords/topics
- Generate long-form articles (reviews/guides)
- Humanize content to reduce AI-detection footprint
- Run quality assessment and only publish if score >= 85
- Auto-iterate fixes and keep generating until 4 high-quality posts/day
- Record failures without lowering standards
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Local imports
from modules.quality.content_quality_assessor import ContentQualityAssessor
from modules.content_generator.advanced_anti_ai_detection import (
    AdvancedAntiAIDetection,
    HumanizationConfig,
)

# Reuse the daily generator building blocks
import sys
sys.path.append(str(Path("scripts").resolve()))
from generate_daily_ai_content import generate_ai_tool_review  # type: ignore


DATA_DIR = Path("data")
CONTENT_REVIEWS_DIR = Path("content/reviews")
CONTENT_ARTICLES_DIR = Path("content/articles")


def run_keywords_refresh() -> bool:
    """Run multi-source keyword analysis with fallback."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run([sys.executable, "scripts/multi_source_keywords.py"], capture_output=True, text=True, encoding="utf-8")
        if r.returncode == 0:
            return True
        # Fallback
        r2 = subprocess.run([sys.executable, "scripts/generate_keywords.py"], capture_output=True, text=True, encoding="utf-8")
        return r2.returncode == 0
    except Exception:
        return False


def load_keywords() -> List[Dict]:
    if Path("daily_keywords.json").exists():
        with open("daily_keywords.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def humanize_content(text: str) -> str:
    humanizer = AdvancedAntiAIDetection(HumanizationConfig())
    return humanizer.humanize_content(text, context={"section_type": "article"})


def build_frontmatter(meta: Dict, quality: Dict) -> str:
    # Ensure required fields
    fm = {
        "title": meta.get("title"),
        "description": meta.get("description", meta.get("title", "")),
        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "categories": meta.get("categories", []),
        "tags": meta.get("tags", []),
        "featured_image": meta.get("featured_image", ""),
        "image_alt": meta.get("image_alt", f"{meta.get('tags', ['AI tool'])[0]} interface"),
        "draft": False,
        # Quality annotations
        "quality_score": quality.get("score"),
        "quality_breakdown": quality.get("breakdown"),
        "humanization_overall": quality.get("metrics", {}).get("humanization_overall"),
        "word_count": quality.get("metrics", {}).get("word_count"),
    }
    # Build YAML (Hugo TOML/YAML ok; we keep YAML)
    def yaml_list(x: List[str]) -> str:
        return "[" + ", ".join(f'"{i}"' for i in x) + "]"

    return (
        "---\n"
        f"title: \"{fm['title']}\"\n"
        f"description: \"{fm['description']}\"\n"
        f"date: {fm['date']}\n"
        f"categories: {yaml_list(fm['categories'])}\n"
        f"tags: {yaml_list(fm['tags'])}\n"
        f"featured_image: \"{fm['featured_image']}\"\n"
        f"image_alt: \"{fm['image_alt']}\"\n"
        f"draft: {str(fm['draft']).lower()}\n"
        f"quality_score: {fm['quality_score']}\n"
        f"humanization_overall: {fm['humanization_overall']}\n"
        f"word_count: {fm['word_count']}\n"
        "---\n\n"
    )


def write_article_file(slug: str, frontmatter: str, body: str, section: str = "reviews") -> Path:
    if section == "articles":
        out_dir = CONTENT_ARTICLES_DIR
    else:
        out_dir = CONTENT_REVIEWS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{slug}-{datetime.utcnow().strftime('%Y-%m-%d')}.md"
    path = out_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(frontmatter)
        f.write(body)
    return path


def slugify(s: str) -> str:
    return (
        s.lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace("|", "-")
        .replace(":", "")
        .replace(",", "")
    )


def pick_targets(keywords: List[Dict]) -> List[Dict]:
    # Prioritize high commercial intent + trending
    targets = sorted(
        keywords,
        key=lambda x: (float(x.get("commercial_intent", 0)), float(x.get("trend_score", 0))),
        reverse=True,
    )
    return targets


def main():
    parser = argparse.ArgumentParser(description="Auto content pipeline with quality gating")
    parser.add_argument("--target", type=int, default=4, help="Target number of high-quality posts")
    parser.add_argument("--max-attempts", type=int, default=3, help="Max attempts per article before marking failure")
    args = parser.parse_args()

    print("🚀 Auto Content Pipeline starting...")
    refreshed = run_keywords_refresh()
    if not refreshed:
        print("⚠️ Keyword refresh failed. Continuing with existing daily_keywords.json if present.")

    keywords = load_keywords()
    if not keywords:
        print("🛑 No keywords available. Aborting.")
        return 1

    assessor = ContentQualityAssessor(min_score=85.0)
    generated: List[str] = []
    failures: List[Dict] = []

    for kw in pick_targets(keywords):
        if len(generated) >= args.target:
            break

        keyword = kw.get("keyword", "AI tool")
        category = kw.get("category", "content_creation")
        print(f"\n📝 Generating candidate for: {keyword} [{category}]")

        attempts = 0
        success = False
        while attempts < args.max_attempts and not success:
            attempts += 1
            try:
                article = generate_ai_tool_review(keyword, category, kw)
                # article must be dict with metadata + content
                meta = {
                    "title": article.get("title"),
                    "description": article.get("metadata", {}).get("description", ""),
                    "categories": article.get("metadata", {}).get("categories", [category]),
                    "tags": article.get("metadata", {}).get("tags", [keyword]),
                    "featured_image": article.get("metadata", {}).get("featured_image", ""),
                    "image_alt": f"{keyword.title()} interface and features",
                }

                body = article.get("content", "")
                # First pass humanization
                body = humanize_content(body)

                # Assess quality
                quality = assessor.assess(body, meta)

                if not quality.passed:
                    print(f"  ❌ Quality {quality.score}/100 (<85). Attempt {attempts}/{args.max_attempts}")
                    # Auto-improve and reassess next loop
                    improved_body, _ = assessor.improve(body, meta)
                    body = improved_body
                    continue

                # Passed gate
                frontmatter = build_frontmatter(meta, {
                    "score": quality.score,
                    "breakdown": quality.breakdown,
                    "metrics": quality.metrics,
                })

                # Ensure images in content have alt texts
                improved_body, _ = assessor.improve(body, meta)
                slug = slugify(f"{keyword}-review")
                out_path = write_article_file(slug, frontmatter, improved_body, section="reviews")
                generated.append(str(out_path))
                success = True
                print(f"  ✅ Published: {out_path} | Score: {quality.score}")

            except Exception as e:
                print(f"  ⚠️ Generation error: {e}")
                break

        if not success:
            failures.append({
                "keyword": keyword,
                "category": category,
                "attempts": attempts,
                "reason": "Quality gate not met",
            })

    # Persist outputs
    if generated:
        with open("generated_files.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(generated))

    if failures:
        fail_file = DATA_DIR / "quality_failures.json"
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        try:
            # Append to existing failures if present
            existing: List[Dict] = []
            if fail_file.exists():
                existing = json.loads(fail_file.read_text(encoding="utf-8"))
            existing.extend(failures)
            fail_file.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  📄 Logged failures to {fail_file}")
        except Exception:
            pass

    print(f"\n🎯 Generated {len(generated)} high-quality articles (target {args.target}).")
    if len(generated) < args.target:
        print("🛑 Not enough content passed the quality gate. Review generator or raise attempts.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

