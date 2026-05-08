#!/usr/bin/env bash
# Copies data/*.json into frontend/data so the frontend can fetch them
# as relative paths when frontend/ is served as the static root.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/data"
DST="$ROOT/frontend/data"

mkdir -p "$DST"
cp "$SRC/articles.json" "$DST/articles.json"
cp "$SRC/orientations.json" "$DST/orientations.json"
cp "$SRC/sources.json" "$DST/sources.json"

echo "Synced data into frontend/data:"
ls -1 "$DST"
