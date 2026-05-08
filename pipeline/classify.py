"""Orientation classification.

Three-layer priority:
    1. Manual tags from data/manual_tags.json (highest, wins everything).
    2. Zero-shot classification via mDeBERTa multilingual NLI model.
    3. Keyword scoring fallback when transformers is not installed.

The model is loaded lazily and cached as a module global.
"""
from __future__ import annotations

import logging
import re
from typing import Iterable

from .fetch_rss import RawArticle

log = logging.getLogger(__name__)

# Zero-shot model. Multilingual, base-size, ~280MB.
# https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7
_ZERO_SHOT_MODEL = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"

# Hypothesis-style natural-language labels. The zero-shot model checks
# whether the article entails each hypothesis. Phrasing matters a lot for
# zero-shot quality. These are tuned for African media discourse.
ORIENTATION_LABELS = {
    "panafricaniste": "perspective panafricaine d'unite continentale et de souverainete africaine collective",
    "post_colonial_critique": "critique post-coloniale denoncant le neocolonialisme et les heritages coloniaux",
    "nationaliste": "perspective nationaliste centree sur la souverainete nationale d'un pays africain",
    "pre_colonial_referentiel": "valorisation des traditions precoloniales et des systemes africains ancestraux",
    "diaspora": "perspective de la diaspora africaine et de ses liens avec le continent",
}

_HYPOTHESIS_TEMPLATE = "Cet article reflete une {}."

# Cached pipeline reference
_pipeline = None
_pipeline_loaded = False


# ----------------------------------------------------------------------------
# Zero-shot path
# ----------------------------------------------------------------------------
def _get_pipeline():
    """Lazy-load the zero-shot pipeline. Returns None if transformers absent."""
    global _pipeline, _pipeline_loaded
    if _pipeline_loaded:
        return _pipeline
    _pipeline_loaded = True
    try:
        from transformers import pipeline
    except ImportError:
        log.warning("transformers not installed, falling back to keyword classifier")
        return None
    try:
        log.info("Loading zero-shot model %s (first time only)...", _ZERO_SHOT_MODEL)
        _pipeline = pipeline(
            "zero-shot-classification",
            model=_ZERO_SHOT_MODEL,
            device=-1,
        )
        log.info("Zero-shot model loaded.")
        return _pipeline
    except Exception as exc:
        log.warning("Zero-shot model load failed (%s), falling back to keywords", exc)
        return None


def _zero_shot_score(text: str) -> dict[str, float] | None:
    pipe = _get_pipeline()
    if pipe is None:
        return None
    try:
        result = pipe(
            text,
            candidate_labels=list(ORIENTATION_LABELS.values()),
            hypothesis_template=_HYPOTHESIS_TEMPLATE,
            multi_label=False,
        )
    except Exception as exc:
        log.warning("Zero-shot inference failed (%s)", exc)
        return None

    label_to_id = {desc: oid for oid, desc in ORIENTATION_LABELS.items()}
    scores: dict[str, float] = {}
    for label, score in zip(result["labels"], result["scores"]):
        oid = label_to_id.get(label)
        if oid:
            scores[oid] = round(float(score), 3)

    # Filter out very weak signals so the orientation bar stays legible.
    # Anything < 5% gets dropped; remainder renormalized.
    filtered = {k: v for k, v in scores.items() if v >= 0.05}
    if not filtered:
        return scores
    total = sum(filtered.values()) or 1.0
    return {k: round(v / total, 3) for k, v in filtered.items()}


# ----------------------------------------------------------------------------
# Keyword fallback (kept for environments without transformers)
#
# Rule for adding words: keyword must be HIGHLY specific to the orientation.
# Common political vocabulary (president, government, army, tradition,
# heritage, migrant) is excluded because it appears in nearly every news
# article and produces false positives. When in doubt, leave it out.
# ----------------------------------------------------------------------------
KEYWORDS: dict[str, list[str]] = {
    "panafricaniste": [
        "afcfta", "zlecaf",
        "union africaine", "african union",
        "panafricain", "panafricaine", "panafrican", "pan-african",
        "panafricanisme", "pan-africanism",
        "intra-african", "intra-africain",
        "ecowas", "cedeao",
        "unite africaine", "african unity",
        "souverainete africaine", "african sovereignty",
    ],
    "post_colonial_critique": [
        "colonial", "coloniale", "coloniaux",
        "neocolonial", "neocoloniale", "neo-colonial",
        "reparations",
        "francafrique", "franc cfa", "cfa franc",
        "imperialisme", "imperialism", "imperialiste",
        "extractivisme", "extractivism", "extractiviste",
        "restitution", "restitutions",
        "decolonisation", "decolonization", "decoloniser",
        "spolie", "spoliation", "spolies",
    ],
    "nationaliste": [
        "souverainete nationale", "national sovereignty",
        "interet national", "national interest",
        "souverainiste", "souverainisme",
        "junte", "junta",
        "patriotique",
    ],
    "pre_colonial_referentiel": [
        "ancestral", "ancestrale", "ancestraux",
        "indigene", "indigenous",
        "precolonial", "pre-colonial", "precoloniale",
        "coutumier", "customary",
        "chefferie", "chieftaincy",
        "royaume traditionnel", "traditional kingdom",
    ],
    "diaspora": [
        "diaspora", "diasporique",
        "afro-descendant", "afrodescendant",
        "caraibe", "caribbean", "antillais",
        "afro-americain", "african american",
        "afro-bresilien", "afro-brazilian",
        "afro-europeen",
        "quilombo", "quilombola",
        "remittance", "remittances",
    ],
}


def _keyword_score(text: str) -> dict[str, float]:
    text_lower = text.lower()
    raw: dict[str, float] = {}
    for orientation, keywords in KEYWORDS.items():
        hits = sum(1 for kw in keywords if re.search(rf"\b{re.escape(kw)}\b", text_lower))
        raw[orientation] = float(hits)
    total = sum(raw.values())
    if total == 0:
        # No keyword signal. Return empty rather than the misleading
        # 20/20/20 fake distribution that ruined the previous run.
        return {}
    return {k: round(v / total, 3) for k, v in raw.items() if v > 0}


# ----------------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------------
def classify_article(article: RawArticle, force_keyword: bool = False) -> dict[str, float]:
    """Score one article across the 5 orientations."""
    text = f"{article.title}. {article.raw_text[:1500]}".strip()
    if not text:
        return {}

    if not force_keyword:
        scores = _zero_shot_score(text)
        if scores:
            return scores

    return _keyword_score(text)


def classify_cluster(
    articles: Iterable[RawArticle],
    manual: dict[str, float] | None = None,
    force_keyword: bool = False,
) -> dict[str, float]:
    """Classify a cluster. Manual override wins. Otherwise, classify the
    lead article only (longest body, most representative) instead of every
    article. This cuts inference cost for multi-source stories without
    hurting quality, since articles in a cluster cover the same topic.
    """
    if manual:
        total = sum(manual.values()) or 1.0
        return {k: round(v / total, 3) for k, v in manual.items() if v > 0}

    article_list = list(articles)
    if not article_list:
        return {}

    lead = max(article_list, key=lambda a: len(a.raw_text or ""))
    return classify_article(lead, force_keyword=force_keyword)
