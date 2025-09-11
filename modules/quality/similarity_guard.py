#!/usr/bin/env python3
"""
Similarity Guard

Prevents publishing near-duplicate content by comparing candidate text
against existing site content (including drafts) using TF-IDF cosine similarity.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import frontmatter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class SimilarityReport:
    max_similarity: float
    most_similar_file: str | None
    similar_items: List[Tuple[str, float]]


class SimilarityGuard:
    def __init__(self, content_dir: str = "content"):
        self.content_dir = Path(content_dir)

    def _collect_texts(self) -> List[Tuple[str, str]]:
        items: List[Tuple[str, str]] = []
        if not self.content_dir.exists():
            return items
        for md in self.content_dir.rglob("*.md"):
            try:
                post = frontmatter.load(md)
                body = post.content or ""
                # Normalize whitespace
                norm = re.sub(r"\s+", " ", body).strip()
                items.append((str(md), norm))
            except Exception:
                continue
        return items

    def assess(self, candidate_text: str, top_k: int = 5) -> SimilarityReport:
        corpus = self._collect_texts()
        if not corpus:
            return SimilarityReport(0.0, None, [])

        texts = [t for _, t in corpus]
        files = [f for f, _ in corpus]

        vectorizer = TfidfVectorizer(stop_words="english", max_features=20000)
        tfidf = vectorizer.fit_transform(texts + [candidate_text])
        sim = cosine_similarity(tfidf[-1], tfidf[:-1]).flatten()

        ranked = sorted(zip(files, sim), key=lambda x: x[1], reverse=True)
        most_similar_file, max_sim = ranked[0]
        return SimilarityReport(
            max_similarity=float(max_sim),
            most_similar_file=most_similar_file,
            similar_items=[(f, float(s)) for f, s in ranked[:top_k]],
        )

