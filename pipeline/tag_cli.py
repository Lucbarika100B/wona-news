"""Interactive CLI to manually tag stories with orientation scores.

Usage:
    python -m pipeline.tag_cli list
    python -m pipeline.tag_cli tag <story_id>
    python -m pipeline.tag_cli show <story_id>

Manual tags persist to data/manual_tags.json and override heuristic
classification on the next pipeline run. The CLI is deliberately small:
no curses UI, no fancy terminal libraries, just stdin and prints.
"""
from __future__ import annotations

import sys

from . import store


def _orientation_ids() -> list[str]:
    return [o["id"] for o in store.load_orientations() if not o.get("secondary")]


def cmd_list() -> int:
    data = store.load_articles()
    tags = store.load_manual_tags()
    if not data["stories"]:
        print("No stories found. Run the pipeline first.")
        return 1
    print(f"{'ID':<28} {'TAGGED':<8} TITLE")
    print("-" * 80)
    for story in data["stories"]:
        flag = "yes" if story["id"] in tags else "no"
        title = story["title"][:50]
        print(f"{story['id']:<28} {flag:<8} {title}")
    return 0


def cmd_show(story_id: str) -> int:
    data = store.load_articles()
    story = next((s for s in data["stories"] if s["id"] == story_id), None)
    if not story:
        print(f"Story not found: {story_id}")
        return 1
    print(f"\n{story['title']}")
    print("=" * len(story['title']))
    print(f"\nSummary: {story['summary']}\n")
    print("Current orientations:")
    for k, v in sorted(story["orientations"].items(), key=lambda kv: -kv[1]):
        bar = "#" * int(v * 30)
        print(f"  {k:<28} {bar} {v:.2f}")
    print(f"\nSources ({len(story['sources'])}):")
    for src in story["sources"]:
        print(f"  - {src['name']} ({src['country_origin']}, {src['language']})")
    return 0


def cmd_tag(story_id: str) -> int:
    data = store.load_articles()
    story = next((s for s in data["stories"] if s["id"] == story_id), None)
    if not story:
        print(f"Story not found: {story_id}")
        return 1

    print(f"\nTagging: {story['title']}\n")
    print(f"Summary: {story['summary'][:300]}...\n")
    print("Enter a number 0-100 for each orientation. Empty = skip (zero).")

    scores: dict[str, float] = {}
    for orientation in _orientation_ids():
        while True:
            raw = input(f"  {orientation}: ").strip()
            if raw == "":
                break
            try:
                value = float(raw)
                if 0 <= value <= 100:
                    scores[orientation] = value / 100.0
                    break
                print("    Out of range. 0 to 100.")
            except ValueError:
                print("    Not a number.")

    if not scores:
        print("No tags entered, nothing saved.")
        return 0

    total = sum(scores.values()) or 1.0
    normalized = {k: round(v / total, 3) for k, v in scores.items()}

    tags = store.load_manual_tags()
    tags[story_id] = normalized
    store.save_manual_tags(tags)
    print(f"\nSaved manual tags for {story_id}:")
    for k, v in normalized.items():
        print(f"  {k}: {v}")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    cmd = argv[0]
    if cmd == "list":
        return cmd_list()
    if cmd == "show" and len(argv) >= 2:
        return cmd_show(argv[1])
    if cmd == "tag" and len(argv) >= 2:
        return cmd_tag(argv[1])
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
