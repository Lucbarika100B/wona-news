"""Extractive summarization. LexRank from sumy with a hand-rolled fallback."""
from __future__ import annotations

import logging
import re

from . import config

log = logging.getLogger(__name__)

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-ZÉÈÀÂÊÎÔÛÇ])")


def _fallback_summary(text: str, n: int) -> str:
    """First-N-sentences approach used when sumy is unavailable or fails."""
    sentences = [s.strip() for s in _SENT_SPLIT.split(text) if len(s.strip()) > 30]
    return " ".join(sentences[:n])


def summarize(text: str, language: str = "english", n: int | None = None) -> str:
    n = n or config.SUMMARY_SENTENCES
    if not text or len(text) < 200:
        return text.strip()

    try:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lex_rank import LexRankSummarizer
    except ImportError:
        log.warning("sumy not installed, using fallback summary")
        return _fallback_summary(text, n)

    sumy_lang = "french" if language.startswith("fr") else "english"
    try:
        parser = PlaintextParser.from_string(text, Tokenizer(sumy_lang))
        summarizer = LexRankSummarizer()
        sentences = summarizer(parser.document, n)
        result = " ".join(str(s) for s in sentences).strip()
        return result or _fallback_summary(text, n)
    except Exception as exc:
        log.warning("LexRank failed (%s), using fallback", exc)
        return _fallback_summary(text, n)
