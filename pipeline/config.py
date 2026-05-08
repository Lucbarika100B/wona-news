"""Central configuration for the Wona.news pipeline."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

SOURCES_FILE = DATA_DIR / "sources.json"
ORIENTATIONS_FILE = DATA_DIR / "orientations.json"
ARTICLES_FILE = DATA_DIR / "articles.json"
RAW_DIR = DATA_DIR / "raw"
TAGS_FILE = DATA_DIR / "manual_tags.json"

# Ingestion
REQUEST_TIMEOUT = 15
USER_AGENT = "WonaNewsBot/0.1 (+https://wona.news)"
MAX_ENTRIES_PER_SOURCE = 25
MIN_ARTICLE_CHARS = 100

# Recency: drop articles older than this many days
MAX_ARTICLE_AGE_DAYS = 7

# Quality filter: drop entries whose URL or title matches these patterns.
# Lowercased substring match.
EXCLUDE_URL_PATTERNS = [
    "/promoted/",
    "/sponsored/",
    "/advertorial/",
    "/sport/",
    "/sports/",
]

EXCLUDE_TITLE_KEYWORDS = [
    "casino",
    "betting",
    "gambling",
    "sportsbook",
    "cryptocurrency",
    "press release",
]

# Clustering
CLUSTER_SIMILARITY_THRESHOLD = 0.25

# Summarization
SUMMARY_SENTENCES = 5

# Blindspot heuristic
BLINDSPOT_CATEGORY_FLOOR = 0.5

# Output
OUTPUT_VERSION = "1.0"
