"""Deterministic UTM link builder.

Every published asset carries its WMI asset ID inside ``utm_content`` so that
performance data pulled back later (Metricool, Search Console, product analytics)
can be matched to the asset that produced it. Optional variant labels are
appended after a ``--`` separator so the asset ID stays parseable.
"""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

_VARIANT_SEPARATOR = "--"


def build_utm_url(
    base_url: str,
    *,
    asset_id: str,
    source: str,
    medium: str,
    campaign: str,
    variant: str | None = None,
    term: str | None = None,
) -> str:
    """Return ``base_url`` with UTM parameters attached.

    ``utm_content`` is set to the asset ID (plus ``--variant`` when given), so the
    originating asset is always recoverable from a click's UTM data.
    """

    if not asset_id.strip():
        raise ValueError("asset_id is required")
    parsed = urlparse(base_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"base_url must be an absolute URL (got {base_url!r})")

    content = asset_id if not variant else f"{asset_id}{_VARIANT_SEPARATOR}{variant}"
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.update(
        {
            "utm_source": source,
            "utm_medium": medium,
            "utm_campaign": campaign,
            "utm_content": content,
        }
    )
    if term:
        query["utm_term"] = term
    return urlunparse(parsed._replace(query=urlencode(query)))


def asset_id_from_utm_content(utm_content: str) -> str:
    """Recover the asset ID from a ``utm_content`` value produced above."""

    return utm_content.split(_VARIANT_SEPARATOR, 1)[0]
