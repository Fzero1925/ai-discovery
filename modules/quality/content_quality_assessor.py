#!/usr/bin/env python3
"""
Content Quality Assessor

Quantifies content quality for SEO + AdSense readiness and human-likeness.
Returns a 0–100 score with detailed metrics and issues. Gate set at >=85.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Reuse advanced humanization scoring
try:
    from modules.content_generator.advanced_anti_ai_detection import (
        AdvancedAntiAIDetection,
        HumanizationConfig,
    )
except Exception:
    # Fallback import path when invoked from different cwd
    from content_generator.advanced_anti_ai_detection import (  # type: ignore
        AdvancedAntiAIDetection,
        HumanizationConfig,
    )


@dataclass
class QualityResult:
    score: float
    passed: bool
    breakdown: Dict[str, float]
    issues: List[str]
    suggestions: List[str]
    metrics: Dict[str, float]


class ContentQualityAssessor:
    """Assess Markdown article quality with weighted scoring."""

    def __init__(self, min_score: float = 85.0):
        self.min_score = min_score
        self.humanizer = AdvancedAntiAIDetection(HumanizationConfig())

    # ---- Public API -------------------------------------------------------
    def assess(self, markdown: str, frontmatter: Optional[Dict] = None) -> QualityResult:
        fm = frontmatter or {}
        body = self._strip_frontmatter(markdown)

        word_count = self._word_count(body)
        h2_count, h3_count = self._heading_counts(body)
        image_info = self._image_stats(body)
        internal_links = self._internal_link_count(body)
        human_scores = self._humanization_scores(body)

        # Readability: prefer avg sentence length 12–22 words
        avg_sentence_len = self._avg_sentence_length(body)
        readability_score = self._readability_score(avg_sentence_len)

        # Metadata completeness
        meta_required = ["title", "description", "categories", "tags", "featured_image"]
        meta_ok = sum(1 for k in meta_required if k in fm and fm.get(k))
        meta_score = (meta_ok / len(meta_required)) * 10.0  # 0–10

        # Components (weights sum to 100). News 与 Review 两套权重
        is_news = False
        cats = fm.get("categories") or []
        if isinstance(cats, list):
            is_news = any(str(c).lower() == "news" for c in cats)
        elif isinstance(cats, str):
            is_news = cats.lower() == "news"

        if is_news:
            # 针对短新闻优化：长度期望 ~180–300 词，结构简单但要求可读+人性化+元数据
            word_score = max(0.0, min(1.0, word_count / 180.0)) * 20.0
            structure_score = min(h2_count, 1) / 1.0 * 8.0  # 标题段落存在即可
            image_score = min(image_info["count"], 1) * 4.0  # 图片可选
            link_score = min(internal_links, 2) / 2.0 * 8.0
            humanization_score = max(0.0, min(1.0, human_scores.get("overall_score", 0.0))) * 25.0
            readability_component = min(15.0, self._readability_score(avg_sentence_len) + 5.0)
            meta_component = min(20.0, meta_score + 10.0)
        else:
            word_score = max(0.0, min(1.0, word_count / 2500.0)) * 25.0
            structure_score = self._structure_score(h2_count, h3_count)  # 0–15
            image_score = self._image_score(image_info)  # 0–10
            link_score = min(internal_links, 4) / 4.0 * 5.0  # 0–5
            humanization_score = max(0.0, min(1.0, human_scores.get("overall_score", 0.0))) * 20.0
            readability_component = readability_score  # 0–15
            meta_component = meta_score  # 0–10

        breakdown = {
            "word_count": round(word_score, 2),
            "structure": round(structure_score, 2),
            "images": round(image_score, 2),
            "internal_links": round(link_score, 2),
            "humanization": round(humanization_score, 2),
            "metadata": round(meta_component, 2),
            "readability": round(readability_component, 2),
        }

        score = sum(breakdown.values())
        passed = score >= self.min_score

        issues, suggestions = self._collect_issues(
            word_count=word_count,
            h2=h2_count,
            h3=h3_count,
            image_info=image_info,
            internal_links=internal_links,
            humanization=human_scores.get("overall_score", 0.0),
            meta_ok=meta_ok,
            avg_sentence_len=avg_sentence_len,
        )

        metrics = {
            "word_count": float(word_count),
            "h2_count": float(h2_count),
            "h3_count": float(h3_count),
            "images": float(image_info["count"]),
            "images_with_alt": float(image_info["with_alt"]),
            "internal_links": float(internal_links),
            "avg_sentence_len": float(avg_sentence_len),
            "humanization_overall": float(human_scores.get("overall_score", 0.0)),
        }

        return QualityResult(
            score=round(score, 2),
            passed=passed,
            breakdown=breakdown,
            issues=issues,
            suggestions=suggestions,
            metrics=metrics,
        )

    def improve(self, markdown: str, frontmatter: Optional[Dict] = None) -> Tuple[str, Dict]:
        """Apply pragmatic automatic improvements: add missing alts, add related links,
        humanize writing, and ensure FAQ presence. Returns (markdown, updated_frontmatter)."""
        fm = dict(frontmatter or {})
        body = self._strip_frontmatter(markdown)

        # Ensure image alt text
        default_alt = fm.get("image_alt") or fm.get("title") or "AI tool illustration"
        body = self._ensure_image_alts(body, default_alt)

        # Ensure a Related Resources section with internal links
        if "## Related Resources" not in body:
            related = (
                "\n\n## Related Resources\n\n"
                "- [AI Tools](/categories/)\n"
                "- [Content Creation](/categories/content-creation/)\n"
                "- [Image Generation](/categories/image-generation/)\n"
            )
            body += related

        # Humanize content for anti-AI detection
        humanized = self.humanizer.humanize_content(body, context={"section_type": "article"})

        # Reassemble with frontmatter if it existed
        if markdown.strip().startswith("---"):
            fm_text, _ = self._split_frontmatter(markdown)
            return f"{fm_text}\n{humanized}", fm
        else:
            return humanized, fm

    # ---- Internal helpers -------------------------------------------------
    def _strip_frontmatter(self, markdown: str) -> str:
        if markdown.strip().startswith("---"):
            _, body = self._split_frontmatter(markdown)
            return body
        return markdown

    def _split_frontmatter(self, markdown: str) -> Tuple[str, str]:
        parts = markdown.split("---", 2)
        if len(parts) >= 3:
            return f"---{parts[1]}---\n", parts[2]
        return "", markdown

    def _word_count(self, text: str) -> int:
        return len(re.findall(r"\b\w+\b", text))

    def _heading_counts(self, text: str) -> Tuple[int, int]:
        h2 = len(re.findall(r"^##\s+", text, flags=re.MULTILINE))
        h3 = len(re.findall(r"^###\s+", text, flags=re.MULTILINE))
        return h2, h3

    def _image_stats(self, text: str) -> Dict[str, int]:
        images = re.findall(r"!\[(.*?)\]\(([^\)]+)\)", text)
        with_alt = sum(1 for alt, _ in images if alt.strip())
        return {"count": len(images), "with_alt": with_alt}

    def _internal_link_count(self, text: str) -> int:
        return len(re.findall(r"\[[^\]]+\]\((/(?!/)[^)]+)\)", text))

    def _humanization_scores(self, text: str) -> Dict[str, float]:
        try:
            return self.humanizer.calculate_humanization_score(text)
        except Exception:
            return {"overall_score": 0.5}

    def _avg_sentence_length(self, text: str) -> float:
        # Basic segmentation on . ! ? and Chinese punctuation
        sentences = re.split(r"[\.!?。！？]+\s*", text)
        sentences = [s for s in sentences if s.strip()]
        if not sentences:
            return 0.0
        words = [len(re.findall(r"\b\w+\b", s)) for s in sentences]
        if not words:
            return 0.0
        return sum(words) / len(words)

    def _readability_score(self, avg_len: float) -> float:
        # 15 points if 12–22 words per sentence, taper outside
        if avg_len <= 0:
            return 6.0
        if 12 <= avg_len <= 22:
            return 15.0
        # Linearly reduce score at distance from ideal center 17
        dist = abs(avg_len - 17.0)
        return max(0.0, 15.0 - dist)

    def _structure_score(self, h2: int, h3: int) -> float:
        score = 0.0
        # Expect at least 6 H2 sections and some H3 subsections for long-form
        score += min(h2, 8) / 8.0 * 10.0  # up to 10
        score += min(h3, 6) / 6.0 * 5.0   # up to 5
        return score

    def _image_score(self, image_info: Dict[str, int]) -> float:
        count = image_info["count"]
        with_alt = image_info["with_alt"]
        if count == 0:
            return 0.0
        # Require at least 3 images for reviews
        base = min(count, 4) / 4.0 * 8.0  # up to 8 points
        alt_bonus = 2.0 if with_alt >= min(3, count) else 0.0
        return base + alt_bonus

    def _ensure_image_alts(self, text: str, default_alt: str) -> str:
        """Ensure that all markdown images have alt text; fill with default if empty."""
        # ![alt](url) or ![](url)
        def repl(m):
            alt = m.group(1)
            url = m.group(2)
            if alt.strip():
                return f"![{alt}]({url})"
            return f"![{default_alt}]({url})"

        return re.sub(r"!\[(.*?)\]\(([^\)]+)\)", repl, text)

    def _collect_issues(
        self,
        *,
        word_count: int,
        h2: int,
        h3: int,
        image_info: Dict[str, int],
        internal_links: int,
        humanization: float,
        meta_ok: int,
        avg_sentence_len: float,
    ) -> Tuple[List[str], List[str]]:
        issues: List[str] = []
        suggestions: List[str] = []

        if word_count < 2500:
            issues.append(f"Word count too low: {word_count} < 2500")
            suggestions.append("Expand sections with real examples, FAQs, and comparisons")
        if h2 < 6:
            issues.append(f"Insufficient H2 sections: {h2} < 6")
            suggestions.append("Add more H2 sections for features, pricing, alternatives, FAQ, ROI")
        if image_info["count"] < 3:
            issues.append("Too few images (<3) for a review")
            suggestions.append("Insert hero, comparison, and pricing images with descriptive alt text")
        if image_info["with_alt"] < image_info["count"]:
            issues.append("Missing alt text on some images")
            suggestions.append("Provide meaningful alt and title attributes for all images")
        if internal_links < 2:
            issues.append("Too few internal links (<2)")
            suggestions.append("Link to related categories and relevant reviews")
        if humanization < 0.6:
            issues.append(f"Humanization score low: {humanization:.2f} < 0.60")
            suggestions.append("Increase personal voice, vary sentence length, add natural connectors")
        if meta_ok < 5:
            issues.append("Frontmatter metadata incomplete")
            suggestions.append("Ensure title, description, categories, tags, featured_image are set")
        if not (12 <= avg_sentence_len <= 22):
            issues.append(f"Average sentence length suboptimal: {avg_sentence_len:.1f}")
            suggestions.append("Break up long sentences and merge very short ones for natural flow")

        return issues, suggestions
