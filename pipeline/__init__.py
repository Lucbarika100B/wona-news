"""Wona.news ingestion pipeline.

Modules in execution order:
    config      - Paths and constants
    fetch_rss   - Pull entries from configured RSS feeds
    clean       - Strip and normalize article text
    summarize   - Produce a short readable summary
    classify    - Heuristic orientation pre-tagging
    cluster     - Group articles covering the same story
    blindspot   - Compute blindspot scores per cluster
    store       - Read/write canonical JSON
    run         - Orchestrator
"""

__version__ = "0.1.0"
