"""End-to-end pipeline orchestrator.

Run with:
    python -m pipeline.run                   # full run, zero-shot + bodies
    python -m pipeline.run --no-bodies       # skip body fetch (faster, lower quality)
    python -m pipeline.run --keyword-only    # skip zero-shot model (faster, lower quality)
    python -m pipeline.run --limit 5         # limit number of sources
    python -m pipeline.run --verbose         # debug logging

Output: data/articles.json
"""
from __future__ import annotations

import argparse
import logging
import sys

from . import blindspot, classify, cluster, clean, fetch_rss, store, summarize
from .fetch_rss import RawArticle


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=logging.DEBUG if verbose else logging.INFO,
        stream=sys.stderr,
    )


def _build_story(
    cluster_articles: list[RawArticle],
    sources: list[dict],
    manual_tags: dict[str, dict],
    force_keyword: bool,
) -> dict:
    lead = max(cluster_articles, key=lambda a: len(a.raw_text or ""))
    story_id = f"story_{lead.id}"

    raw_manual = manual_tags.get(story_id)
    if isinstance(raw_manual, dict) and "orientations" in raw_manual:
        manual = raw_manual["orientations"]
    else:
        manual = raw_manual if isinstance(raw_manual, dict) else None

    orientations = classify.classify_cluster(
        cluster_articles,
        manual=manual,
        force_keyword=force_keyword,
    )
    summary = summarize.summarize(lead.raw_text, language=lead.source_language)
    is_blindspot, blindspot_score, note = blindspot.compute_blindspot(cluster_articles, sources)

    # Achievement: any contributing source carries category="achievement"
    is_achievement = any(a.source_category == "achievement" for a in cluster_articles)

    return {
        "id": story_id,
        "title": lead.title,
        "summary": summary,
        "themes": [],
        "region": "unspecified",
        "published_at": min(a.published_at for a in cluster_articles),
        "orientations": orientations,
        "blindspot": is_blindspot,
        "blindspot_score": blindspot_score,
        "blindspot_note": note,
        "achievement": is_achievement,
        "image_url": next((a.image_url for a in cluster_articles if a.image_url), None),
        "sources": [
            {
                "name": a.source_name,
                "url": a.url,
                "language": a.source_language,
                "country_origin": a.source_country,
                "category": a.source_category,
                "logo_initials": a.source_logo_initials,
            }
            for a in cluster_articles
        ],
    }


def run(
    fetch_bodies: bool = True,
    source_limit: int | None = None,
    force_keyword: bool = False,
) -> dict:
    sources = store.load_sources()
    if source_limit:
        sources = sources[:source_limit]

    raw = fetch_rss.fetch_all(sources)
    cleaned = clean.clean_articles(raw, fetch_bodies=fetch_bodies)
    clusters = cluster.cluster(cleaned)
    manual_tags = store.load_manual_tags()

    stories = [_build_story(c, sources, manual_tags, force_keyword) for c in clusters]
    stories.sort(key=lambda s: s["published_at"], reverse=True)

    stats = {
        "total_stories": len(stories),
        "total_sources": len({a.source_id for a in cleaned}),
        "blindspot_count": sum(1 for s in stories if s["blindspot"]),
        "achievement_count": sum(1 for s in stories if s.get("achievement")),
    }
    store.write_articles(stories, stats)
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Wona.news ingestion pipeline.")
    parser.add_argument("--no-bodies", action="store_true", help="Skip full article body fetch")
    parser.add_argument("--keyword-only", action="store_true", help="Skip zero-shot model, use keyword fallback only")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of sources")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    _setup_logging(args.verbose)
    stats = run(
        fetch_bodies=not args.no_bodies,
        source_limit=args.limit,
        force_keyword=args.keyword_only,
    )
    print(
        f"Done. {stats['total_stories']} stories from "
        f"{stats['total_sources']} sources, "
        f"{stats['blindspot_count']} blindspots."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())