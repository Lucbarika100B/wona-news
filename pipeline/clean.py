"""Download full article bodies, normalize text, drop low-quality entries."""
from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta, timezone
from typing import Iterable

import requests
from bs4 import BeautifulSoup

from . import config
from .fetch_rss import RawArticle

log = logging.getLogger(__name__)

_WS = re.compile(r"\s+")
_BLOCK_TAGS = ("script", "style", "noscript", "iframe", "form", "aside", "nav", "footer", "header")


def _strip_html(html: str) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(_BLOCK_TAGS):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return _WS.sub(" ", text).strip()


def _fetch_page(url: str) -> str | None:
    try:
        response = requests.get(
            url,
            headers={"User-Agent": config.USER_AGENT},
            timeout=config.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        log.warning("Page fetch failed for %s: %s", url, exc)
        return None


def _extract_body_and_image(html: str) -> tuple[str, str | None]:
    """Return (body_text, og_image_url) from a full HTML page."""
    soup = BeautifulSoup(html, "html.parser")

    # Image first (cheap, before body decomposition mutates the soup)
    image_url = None
    og = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "twitter:image"})
    if og and og.get("content"):
        image_url = og["content"]

    # Body
    for tag in soup.find_all(_BLOCK_TAGS):
        tag.decompose()
    article_node = soup.find("article") or soup.find("main") or soup.body
    body = ""
    if article_node is not None:
        body = _WS.sub(" ", article_node.get_text(separator=" ")).strip()

    return body, image_url


# ----------------------------------------------------------------------------
# Quality filters
# ----------------------------------------------------------------------------
def _is_too_old(article: RawArticle, cutoff: datetime) -> bool:
    try:
        pub = datetime.fromisoformat(article.published_at.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return False  # Keep ambiguous dates rather than drop
    return pub < cutoff


def _is_excluded(article: RawArticle) -> bool:
    url_lower = article.url.lower()
    for pattern in config.EXCLUDE_URL_PATTERNS:
        if pattern in url_lower:
            return True
    title_lower = article.title.lower()
    for keyword in config.EXCLUDE_TITLE_KEYWORDS:
        if keyword in title_lower:
            return True
    return False


# ----------------------------------------------------------------------------
# Public entrypoint
# ----------------------------------------------------------------------------
def clean_articles(articles: Iterable[RawArticle], fetch_bodies: bool = True) -> list[RawArticle]:
    """Apply quality filters, fetch bodies, populate raw_text and image_url."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=config.MAX_ARTICLE_AGE_DAYS)
    out: list[RawArticle] = []
    dropped_old = dropped_excluded = dropped_short = 0

    for art in articles:
        if _is_too_old(art, cutoff):
            dropped_old += 1
            continue
        if _is_excluded(art):
            dropped_excluded += 1
            continue

        body = _strip_html(art.summary_html)

        if fetch_bodies:
            html = _fetch_page(art.url)
            if html:
                full, og_image = _extract_body_and_image(html)
                if len(full) > len(body):
                    body = full
                if not art.image_url and og_image:
                    art.image_url = og_image

        if len(body) < config.MIN_ARTICLE_CHARS:
            dropped_short += 1
            continue

        art.raw_text = body
        out.append(art)

    log.info(
        "Cleaned %d articles. Dropped: %d too old, %d excluded, %d too short.",
        len(out), dropped_old, dropped_excluded, dropped_short,
    )
    return out
