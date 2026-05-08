"""Group articles covering the same story via TF-IDF + cosine similarity.

Algorithm: simple agglomerative single-link clustering on title+lead text.
Threshold is configurable. This is good enough for daily volumes under a few
hundred entries. Replace with HDBSCAN or sentence-transformers when scale
demands it.
"""
from __future__ import annotations

import logging
from typing import Iterable

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from . import config
from .fetch_rss import RawArticle

log = logging.getLogger(__name__)


def _signature(article: RawArticle) -> str:
    lead = article.raw_text[:600] if article.raw_text else ""
    return f"{article.title} {lead}"


def cluster(articles: list[RawArticle]) -> list[list[RawArticle]]:
    if not articles:
        return []
    if len(articles) == 1:
        return [articles]

    docs = [_signature(a) for a in articles]
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        stop_words=None,
        max_features=20000,
    )
    matrix = vectorizer.fit_transform(docs)
    similarity = cosine_similarity(matrix)

    threshold = config.CLUSTER_SIMILARITY_THRESHOLD
    n = len(articles)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj

    for i in range(n):
        for j in range(i + 1, n):
            if similarity[i, j] >= threshold:
                union(i, j)

    groups: dict[int, list[RawArticle]] = {}
    for idx, art in enumerate(articles):
        groups.setdefault(find(idx), []).append(art)

    clusters = list(groups.values())
    log.info("Clustered %d articles into %d stories", n, len(clusters))
    return clusters
