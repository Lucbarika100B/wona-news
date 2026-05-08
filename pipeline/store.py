"""Read and write canonical JSON files."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import config


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_sources() -> list[dict]:
    return _read_json(config.SOURCES_FILE)["sources"]


def load_orientations() -> list[dict]:
    return _read_json(config.ORIENTATIONS_FILE)["orientations"]


def load_manual_tags() -> dict[str, dict]:
    if not config.TAGS_FILE.exists():
        return {}
    return _read_json(config.TAGS_FILE)


def save_manual_tags(tags: dict[str, dict]) -> None:
    _write_json(config.TAGS_FILE, tags)


def write_articles(stories: list[dict], stats: dict) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": config.OUTPUT_VERSION,
        "stats": stats,
        "stories": stories,
    }
    _write_json(config.ARTICLES_FILE, payload)


def load_articles() -> dict:
    if not config.ARTICLES_FILE.exists():
        return {"stories": [], "stats": {}, "generated_at": None}
    return _read_json(config.ARTICLES_FILE)
