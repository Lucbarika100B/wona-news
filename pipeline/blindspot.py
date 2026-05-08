"""Blindspot detection.

A story is flagged as a blindspot when its sources concentrate on a narrow
slice of the available source landscape. We measure this on two axes:

    1. Source category coverage: how many of the configured categories
       (international, panafrican, local) cover the story.
    2. Source-country diversity: how many distinct origin countries cover it.

A low score on either axis means the story is being missed by major slices
of the press.
"""
from __future__ import annotations

from typing import Iterable

from . import config
from .fetch_rss import RawArticle


def _all_categories(sources: Iterable[dict]) -> set[str]:
    return {s["category"] for s in sources}


def compute_blindspot(
    cluster_articles: list[RawArticle],
    all_sources: list[dict],
) -> tuple[bool, float, str | None]:
    """Return (is_blindspot, score, optional human note)."""
    if not cluster_articles:
        return False, 0.0, None

    available_categories = _all_categories(all_sources)
    covering_categories = {a.source_category for a in cluster_articles}

    coverage_ratio = len(covering_categories) / max(1, len(available_categories))
    source_count = len({a.source_id for a in cluster_articles})

    # A blindspot requires at least 2 sources (otherwise the story is
    # just niche, not "underreported"), AND those sources all cluster in
    # a narrow slice of the source-category landscape.
    is_blindspot = (
        source_count >= 2
        and coverage_ratio < config.BLINDSPOT_CATEGORY_FLOOR
    )

    # Score is inverse of coverage, only when this is actually a blindspot.
    score = round(1.0 - coverage_ratio, 3) if is_blindspot else 0.0

    note = None
    if is_blindspot:
        missing = sorted(available_categories - covering_categories)
        if missing:
            note = (
                f"Couvert principalement par les médias de catégorie "
                f"{', '.join(sorted(covering_categories))}. "
                f"Absent des fils {', '.join(missing)}."
            )

    return is_blindspot, score, note
