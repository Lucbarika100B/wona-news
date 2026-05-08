"""Fetch RSS feeds and normalize entries into raw articles."""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Iterable

import feedparser
from dateutil import parser as date_parser

from . import config

log = logging.getLogger(__name__)


@dataclass
class RawArticle:
    id: str
    source_id: str
    source_name: str
    source_language: str
    source_country: str
    source_category: str
    source_logo_initials: str
    title: str
    url: str
    summary_html: str
    published_at: str
    image_url: str | None = None
    fetched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    raw_text: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _hash_url(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def _parse_date(value: str | None) -> str:
    if not value:
        return datetime.now(timezone.utc).isoformat()
    try:
        return date_parser.parse(value).astimezone(timezone.utc).isoformat()
    except (ValueError, TypeError):
        return datetime.now(timezone.utc).isoformat()


def _entry_image(entry) -> str | None:
    media = entry.get("media_content") or entry.get("media_thumbnail") or []
    for item in media:
        if "url" in item:
            return item["url"]
    for link in entry.get("links", []):
        if link.get("type", "").startswith("image/"):
            return link.get("href")
    if "image" in entry:
        return entry.image.get("href")
    return None


def _matches_filter(entry, keywords: list[str]) -> bool:
    if not keywords:
        return True
    text = " ".join([
        entry.get("title", ""),
        entry.get("summary", ""),
        " ".join(tag.get("term", "") for tag in entry.get("tags", []) or []),
    ]).lower()
    return any(kw.lower() in text for kw in keywords)


def fetch_source(source: dict) -> list[RawArticle]:
    """Fetch and normalize entries for a single source."""
    log.info("Fetching %s", source["name"])
    feed = feedparser.parse(
        source["rss_url"],
        agent=config.USER_AGENT,
        request_headers={"Accept": "application/rss+xml,application/xml,text/xml"},
    )
    if feed.bozo and not feed.entries:
        log.warning("Feed parse failed for %s: %s", source["name"], feed.bozo_exception)
        return []

    articles: list[RawArticle] = []
    keywords = source.get("filter_keywords") or []
    for entry in feed.entries[: config.MAX_ENTRIES_PER_SOURCE]:
        if not _matches_filter(entry, keywords):
            continue
        url = entry.get("link") or ""
        title = (entry.get("title") or "").strip()
        if not url or not title:
            continue
        published = _parse_date(entry.get("published") or entry.get("updated"))
        articles.append(
            RawArticle(
                id=_hash_url(url),
                source_id=source["id"],
                source_name=source["name"],
                source_language=source["language"],
                source_country=source["country_origin"],
                source_category=source["category"],
                source_logo_initials=source["logo_initials"],
                title=title,
                url=url,
                summary_html=entry.get("summary", ""),
                published_at=published,
                image_url=_entry_image(entry),
            )
        )
    log.info("  -> %d entries kept", len(articles))
    return articles


def fetch_all(sources: Iterable[dict]) -> list[RawArticle]:
    seen_urls: set[str] = set()
    out: list[RawArticle] = []
    for source in sources:
        try:
            for art in fetch_source(source):
                if art.url in seen_urls:
                    continue
                seen_urls.add(art.url)
                out.append(art)
        except Exception as exc:
            log.exception("Source %s failed: %s", source.get("name"), exc)
    return out
