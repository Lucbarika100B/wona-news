"""Wona.news API server.

Endpoints:
    GET /api/health
    GET /api/articles
    GET /api/articles/{story_id}
    GET /api/orientations
    GET /api/sources
    GET /api/blindspots

Run locally:
    uvicorn api.main:app --reload --port 8000
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow importing the pipeline package when running uvicorn from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pipeline import store

app = FastAPI(
    title="Wona.news API",
    version="0.1.0",
    description="African media intelligence platform.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/articles")
def list_articles(
    orientation: str | None = None,
    blindspot: bool | None = None,
    region: str | None = None,
    limit: int = 50,
):
    data = store.load_articles()
    stories = data.get("stories", [])

    if orientation:
        stories = [s for s in stories if orientation in s.get("orientations", {})]
    if blindspot is not None:
        stories = [s for s in stories if bool(s.get("blindspot")) is blindspot]
    if region:
        stories = [s for s in stories if s.get("region") == region]

    return {
        "generated_at": data.get("generated_at"),
        "stats": data.get("stats", {}),
        "stories": stories[:limit],
    }


@app.get("/api/articles/{story_id}")
def get_article(story_id: str):
    data = store.load_articles()
    story = next((s for s in data.get("stories", []) if s["id"] == story_id), None)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@app.get("/api/orientations")
def list_orientations():
    return {"orientations": store.load_orientations()}


@app.get("/api/sources")
def list_sources():
    return {"sources": store.load_sources()}


@app.get("/api/blindspots")
def list_blindspots(limit: int = 20):
    data = store.load_articles()
    blindspots = [s for s in data.get("stories", []) if s.get("blindspot")]
    blindspots.sort(key=lambda s: s.get("blindspot_score", 0), reverse=True)
    return {"stories": blindspots[:limit]}
