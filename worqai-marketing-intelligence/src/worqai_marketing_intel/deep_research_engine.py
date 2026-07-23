"""Executable, evidence-linked deep research reports."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any
from urllib.parse import quote_plus

from .models import SearchReference


def build_deep_research_plan(
    request: str,
    *,
    sources: Iterable[SearchReference | Mapping[str, Any]] = (),
) -> dict[str, object]:
    """Build a runnable report whose findings always point to source records.

    The historical function name is retained for callers. With no supplied
    sources, the report is explicitly pending and contains executable search,
    fetch, extraction, and synthesis jobs rather than prewritten conclusions.
    """

    source_register = _source_register(sources)
    findings = _source_backed_findings(source_register)
    source_sets = _source_sets()
    pending_sources = not source_register
    return {
        "format": "deep research report",
        "status": "research_pending" if pending_sources else "evidence_collected",
        "research_goal": (
            "Find successful examples, preserve source evidence, and extract "
            "repeatable patterns without copying surface-level wording."
        ),
        "source_request": request,
        "source_sets": source_sets,
        "source_register": source_register,
        "findings": findings,
        "execution_queue": _execution_queue(source_sets, has_sources=bool(source_register)),
        "pattern_matrix": [
            {
                "hypothesis": "Pain-led examples make the cost of generic applications concrete.",
                "status": "unvalidated",
                "required_evidence": "Two independent sources plus one performance event.",
            },
            {
                "hypothesis": "Before/after resume evidence explains role alignment faster than feature copy.",
                "status": "unvalidated",
                "required_evidence": "A source excerpt and a measurable social or conversion outcome.",
            },
            {
                "hypothesis": "Trust language should state that WorqAI does not invent experience.",
                "status": "unvalidated",
                "required_evidence": "Repeated buyer objection language across source types.",
            },
        ],
        "decisions": _decisions(findings),
        "gaps": _gaps(source_register),
        "output_after_research": [
            "Three evidence-linked reusable hook patterns.",
            "One source-backed SEO outline per validated intent.",
            "Five social angles, each linked to source IDs.",
            "Claims to avoid, with the evidence or risk behind each one.",
            "A proof backlog with owner, source, metric, and next action.",
        ],
        "completion_criteria": [
            "At least six readable sources across two source sets.",
            "Every finding has one or more source_ids and a verbatim evidence excerpt.",
            "Every recommended pattern has a channel, asset type, and measurable validation event.",
            "Contradictory evidence is recorded instead of silently discarded.",
        ],
    }


def build_deep_research_report(
    request: str,
    *,
    sources: Iterable[SearchReference | Mapping[str, Any]] = (),
) -> dict[str, object]:
    """Named report entry point for new callers."""

    return build_deep_research_plan(request, sources=sources)


def _source_sets() -> list[dict[str, object]]:
    definitions = (
        (
            "serp_competitors",
            "SERP competitors",
            ("cv con ia", "analizador cv ats", "ai resume builder"),
            ("title promise", "page structure", "CTA", "FAQ topics", "proof shown"),
        ),
        (
            "buyer_language",
            "Buyer and social language",
            ("ATS resume rejection forum", "career coach ATS resume examples", "CV tailoring objections"),
            ("language of pain", "objections", "questions", "before/after examples"),
        ),
        (
            "offer_patterns",
            "Ad and landing-page patterns",
            ("resume builder landing page", "free ATS checker", "career AI pricing CTA"),
            ("offer framing", "free plan wording", "trust markers", "risk disclaimers"),
        ),
    )
    return [
        {
            "id": source_id,
            "name": name,
            "queries": list(queries),
            "search_urls": [f"https://duckduckgo.com/html/?q={quote_plus(query)}" for query in queries],
            "extract": list(extract),
        }
        for source_id, name, queries, extract in definitions
    ]


def _source_register(
    sources: Iterable[SearchReference | Mapping[str, Any]],
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for index, source in enumerate(sources, start=1):
        if isinstance(source, SearchReference):
            title, url, text, provider = source.title, source.url, source.snippet, source.source
        else:
            title = str(source.get("title", "Untitled source"))
            url = str(source.get("url", source.get("source", "")))
            text = str(source.get("text", source.get("snippet", "")))
            provider = str(source.get("provider", source.get("source_type", "provided")))
        records.append(
            {
                "id": f"S{index}",
                "title": title,
                "url": url,
                "provider": provider,
                "readable": bool(text.strip()),
                "evidence_excerpt": " ".join(text.split())[:500],
            }
        )
    return records


def _source_backed_findings(source_register: list[dict[str, object]]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for source in source_register:
        excerpt = str(source["evidence_excerpt"])
        if not excerpt:
            continue
        lowered = f"{source['title']} {excerpt}".lower()
        if any(term in lowered for term in ("before", "after", "case study")):
            observation = "The source uses a before/after or case-study proof structure."
        elif any(term in lowered for term in ("mistake", "fails", "failure", "teardown")):
            observation = "The source frames the lesson as a mistake or failure teardown."
        elif any(term in lowered for term in ("template", "checklist", "framework")):
            observation = "The source packages its guidance as a practical framework."
        else:
            observation = "The source contains readable category evidence for manual coding."
        findings.append(
            {
                "id": f"F{len(findings) + 1}",
                "observation": observation,
                "source_ids": [source["id"]],
                "evidence_excerpt": excerpt,
                "confidence": 0.7 if observation.endswith("structure.") else 0.45,
                "recommended_validation": "Record a performance event before promoting this to a winning pattern.",
            }
        )
    return findings


def _execution_queue(
    source_sets: list[dict[str, object]],
    *,
    has_sources: bool,
) -> list[dict[str, object]]:
    jobs: list[dict[str, object]] = []
    for source_set in source_sets:
        jobs.append(
            {
                "id": f"search_{source_set['id']}",
                "action": "search",
                "adapter": "DuckDuckGoSearchAdapter.search",
                "inputs": {"queries": source_set["queries"], "limit_per_query": 5},
                "output": "SearchReference records",
                "status": "pending",
            }
        )
    jobs.extend(
        (
            {
                "id": "fetch_pages",
                "action": "fetch",
                "adapter": "fetch_reference",
                "inputs": {"source": "search results", "max_chars": 12000},
                "output": "Readable page text or a per-URL warning",
                "status": "complete" if has_sources else "blocked_on_search",
            },
            {
                "id": "extract_evidence",
                "action": "extract",
                "adapter": "extract_patterns",
                "inputs": {"source": "fetched page text", "require_source_id": True},
                "output": "Evidence-linked findings and candidate patterns",
                "status": "complete" if has_sources else "blocked_on_fetch",
            },
            {
                "id": "validate_patterns",
                "action": "measure",
                "adapter": "MemoryStore.save_performance_event",
                "inputs": {"link_field": "asset_id", "segment_by": ["asset_type", "channel"]},
                "output": "Ranked generation-facing patterns",
                "status": "pending",
            },
        )
    )
    return jobs


def _decisions(findings: list[dict[str, object]]) -> list[dict[str, object]]:
    if not findings:
        return [
            {
                "decision": "Do not promote a pattern yet.",
                "reason": "No readable source evidence was supplied.",
                "source_ids": [],
                "status": "pending",
            }
        ]
    return [
        {
            "decision": "Keep extracted structures as test candidates, not proven winners.",
            "reason": "Source evidence exists, but performance validation is still required.",
            "source_ids": [source_id for finding in findings for source_id in finding["source_ids"]],
            "status": "candidate",
        }
    ]


def _gaps(source_register: list[dict[str, object]]) -> list[str]:
    gaps: list[str] = []
    readable = sum(bool(source["readable"]) for source in source_register)
    if readable < 6:
        gaps.append(f"Need {6 - readable} more readable source(s) to meet the evidence threshold.")
    if not source_register:
        gaps.append("Run the execution queue; no sources have been collected yet.")
    if source_register and not all(source["url"] for source in source_register):
        gaps.append("One or more supplied sources lacks a traceable URL.")
    gaps.append("Performance validation remains pending until events are linked to saved benchmark IDs.")
    return gaps
