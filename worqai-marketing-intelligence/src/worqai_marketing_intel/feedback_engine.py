"""Feedback loop design for marketing performance learning."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedMetric:
    """A canonical metric extracted from natural-language performance notes."""

    name: str
    value: float
    original: str


_METRIC_ALIASES: dict[str, tuple[str, ...]] = {
    "average_position": ("average position", "avg position", "posición promedio", "posicion promedio"),
    "profile_clicks": ("profile clicks", "clics al perfil", "clicks al perfil"),
    "pilot_interest": ("pilot interest", "interés piloto", "interes piloto"),
    "cv_uploads": ("cv uploads", "cv upload", "subidas de cv", "cvs subidos"),
    "signups": ("signups", "signup", "registrations", "registros"),
    "impressions": ("impressions", "impresiones"),
    "comments": ("comments", "comentarios"),
    "saves": ("saves", "guardados"),
    "shares": ("shares", "compartidos"),
    "clicks": ("clicks", "clics"),
    "views": ("views", "vistas", "reproducciones"),
    "replies": ("replies", "reply", "respuestas", "respuesta"),
    "meetings": ("meetings", "meeting", "reuniones", "reunión", "reunion"),
    "downloads": ("downloads", "download", "descargas", "descarga"),
    "conversions": ("conversions", "conversiones"),
    "bounce_rate": ("bounce rate", "tasa de rebote"),
    "unsubscribe_rate": ("unsubscribe rate", "tasa de baja"),
    "conversion_rate": ("conversion rate", "tasa de conversión", "tasa de conversion"),
    "ctr": ("ctr", "click-through rate", "click through rate"),
}

_NUMBER = r"[+-]?\d+(?:[.,]\d+)?\s*(?:million|mil|k|m)?\s*%?"


def canonical_metric_name(name: str) -> str:
    """Return a stable metric key while accepting common English/Spanish labels."""

    normalized = re.sub(r"[_\s-]+", " ", name.strip().lower())
    for canonical, aliases in _METRIC_ALIASES.items():
        if normalized == canonical.replace("_", " ") or normalized in aliases:
            return canonical
    return normalized.replace(" ", "_")


def parse_metric_value(value: str) -> float:
    """Parse percentages, decimal commas, and compact k/m/mil values."""

    cleaned = value.strip().lower().replace(" ", "")
    cleaned = cleaned.removesuffix("%")
    multiplier = 1.0
    for suffix, factor in (("million", 1_000_000.0), ("mil", 1_000.0), ("k", 1_000.0), ("m", 1_000_000.0)):
        if cleaned.endswith(suffix):
            cleaned = cleaned[: -len(suffix)]
            multiplier = factor
            break
    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        whole, fraction = cleaned.rsplit(",", maxsplit=1)
        cleaned = f"{whole}.{fraction}" if len(fraction) != 3 else f"{whole}{fraction}"
    return float(cleaned) * multiplier


def parse_metrics(text: str) -> tuple[ParsedMetric, ...]:
    """Extract metric/value pairs regardless of whether the label comes first."""

    found: list[tuple[int, ParsedMetric]] = []
    occupied: list[tuple[int, int]] = []
    for canonical, aliases in _METRIC_ALIASES.items():
        alias_pattern = "|".join(re.escape(alias) for alias in sorted(aliases, key=len, reverse=True))
        patterns = (
            rf"\b(?:{alias_pattern})\b\s*(?:was|were|is|at|de|:|=)?\s*({_NUMBER})",
            rf"({_NUMBER})\s*(?:of|de)?\s*\b(?:{alias_pattern})\b",
        )
        for pattern in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                span = match.span()
                if any(span[0] < end and start < span[1] for start, end in occupied):
                    continue
                raw_value = match.group(1)
                try:
                    value = parse_metric_value(raw_value)
                except ValueError:
                    continue
                found.append((span[0], ParsedMetric(canonical, value, match.group(0))))
                occupied.append(span)
    found.sort(key=lambda item: (item[0], item[1].name))
    return tuple(item for _, item in found)


def metric_direction(name: str) -> str:
    """Describe whether a larger or smaller value represents better performance."""

    canonical = canonical_metric_name(name)
    if canonical in {"average_position", "bounce_rate", "unsubscribe_rate"}:
        return "lower"
    return "higher"


def metric_weight(name: str) -> float:
    """Weight outcome metrics above reach metrics during pattern ranking."""

    canonical = canonical_metric_name(name)
    if canonical in {"signups", "conversions", "meetings", "pilot_interest", "downloads", "cv_uploads"}:
        return 3.0
    if canonical in {"replies", "shares", "saves", "ctr", "conversion_rate"}:
        return 2.0
    if canonical in {"clicks", "profile_clicks", "average_position"}:
        return 1.5
    if canonical in {"impressions", "views"}:
        return 0.5
    return 1.0


def build_feedback_loop(request: str) -> dict[str, object]:
    return {
        "format": "performance feedback loop",
        "purpose": "Turn real marketing outcomes into future routing, hooks, and quality decisions.",
        "events_to_track": [
            "post_published",
            "reel_published",
            "carousel_published",
            "seo_page_published",
            "pitch_sent",
            "reply_received",
            "signup",
            "cv_analyzed",
            "cv_adapted",
        ],
        "metrics_by_channel": {
            "social": ["impressions", "comments", "saves", "shares", "profile_clicks", "signups"],
            "seo": ["query", "impressions", "clicks", "ctr", "average_position", "indexed"],
            "outreach": ["sent", "opened_if_available", "reply", "meeting", "pilot_interest"],
            "product": ["signup", "cv_upload", "job_description_paste", "adapted_cv_download"],
        },
        "memory_schema": [
            "asset_id",
            "asset_type",
            "channel",
            "hook",
            "audience",
            "cta",
            "published_at",
            "metric_name",
            "metric_value",
            "notes",
        ],
        "storage_status": "SQLite performance_events table is supported by MemoryStore.",
        "learning_runtime": {
            "natural_language_ingestion": "MemoryStore.save_performance_text uses parse_metrics.",
            "ranking": "MemoryStore.rank_benchmark_examples aggregates by asset type and channel.",
            "generation_selection": "ResearchEngine.patterns_for promotes measured winners first.",
        },
        "weekly_review": [
            "Find posts with high saves/comments and store their hook pattern.",
            "Find SEO pages with impressions but low CTR and rewrite title/meta.",
            "Find pitches with replies and extract the objection/interest language.",
            "Retire claims or formats that create confusion.",
        ],
        "source_request": request,
    }
