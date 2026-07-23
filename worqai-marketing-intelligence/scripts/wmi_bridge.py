"""Bridge an AI workspace to the repository-local WMI Python runtime."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from worqai_marketing_intel.codec import to_plain  # noqa: E402
from worqai_marketing_intel.feedback_engine import canonical_metric_name, parse_metrics  # noqa: E402
from worqai_marketing_intel.memory_store import MemoryStore  # noqa: E402
from worqai_marketing_intel.models import AssetType  # noqa: E402
from worqai_marketing_intel.orchestrator import MarketingOrchestrator  # noqa: E402
from worqai_marketing_intel.prompt_runtime import run_prompt  # noqa: E402
from worqai_marketing_intel.router import classify  # noqa: E402
from worqai_marketing_intel.utm import build_utm_url  # noqa: E402
from worqai_marketing_intel.validation import (  # noqa: E402
    blocking_failures,
    build_judge_packet,
    evaluate_hard_gates,
    gate_to_dict,
)


def compile_context(request: str, *, live: bool, limit: int) -> dict[str, Any]:
    orchestrator = MarketingOrchestrator()
    packet = orchestrator.prepare(request)
    runtime = run_prompt(
        request,
        orchestrator=orchestrator,
        live_research=live,
        limit=limit,
    )
    data = {
        "request": request,
        "task": to_plain(packet.task),
        "brand_context": packet.brand_context,
        "benchmark_patterns": to_plain(packet.benchmark_patterns),
        "agent_insights": to_plain(packet.agent_insights),
        "requirements": list(packet.requirements),
        "claims_to_qualify": list(packet.claims_to_qualify),
        "source_facts": list(packet.source_facts),
        "runtime": to_plain(runtime),
        "creative_contract": (
            "Use this output as grounding and constraints. The creative operator must "
            "create the novel final work."
        ),
    }
    if live:
        data["live_research"] = to_plain(orchestrator.live_research(request, limit=limit))
    return data


def validate_draft(request: str, draft: str) -> dict[str, Any]:
    if not draft.strip():
        raise SystemExit("Draft is empty.")

    orchestrator = MarketingOrchestrator()
    task = classify(request)

    gates = evaluate_hard_gates(draft, task, orchestrator.brand)
    blocking = blocking_failures(gates)
    judge_packet = build_judge_packet(draft, task, orchestrator.brand, gates)

    # Advisory only: a rough heuristic smoke signal, never a gate. Real quality
    # judgment happens when the operator scores the draft against judge_packet.
    advisory = orchestrator.taste.score_asset(draft, asset_type=task.asset_type, task=task)

    script_audit = None
    if task.asset_type == AssetType.IG_REEL:
        script_audit = orchestrator.audit_script(request, draft)

    repair_targets = [gate.detail for gate in blocking]
    if script_audit:
        repair_targets.extend(
            f"{issue['problem']} Fix: {issue['fix']}"
            for issue in script_audit.get("issues", [])
        )

    return {
        "request": request,
        "asset_type": task.asset_type.value,
        "blocked": bool(blocking),
        "blocking_gates": [gate_to_dict(gate) for gate in blocking],
        "judge_packet": judge_packet,
        "script_audit": script_audit,
        "repair_targets": repair_targets,
        "advisory_quality": to_plain(advisory),
        "repair_contract": (
            "First clear every blocked hard gate. Then score the draft against "
            "judge_packet.rubric as a separate critical pass, quoting exact sentences for each "
            "deduction, and repair the weakest axis before revalidating. advisory_quality is a "
            "rough heuristic smoke signal only, not a gate — do not pad a concise draft to raise it."
        ),
    }


def record_performance(
    *,
    asset_id: str,
    asset_type: str,
    channel: str,
    metrics_json: str | None,
    text: str | None,
    notes: str,
) -> dict[str, Any]:
    """Persist performance metrics for a published asset.

    Accepts either a structured ``--metrics-json`` object (``{"saves": 42}``) or a
    natural-language ``--text`` update. Metric names are canonicalized so English
    and Spanish labels land in the same bucket for ranking.
    """

    store = MemoryStore()
    recorded: list[dict[str, Any]] = []

    if metrics_json:
        data = json.loads(metrics_json)
        if not isinstance(data, dict):
            raise SystemExit("--metrics-json must be a JSON object of metric_name: value.")
        for raw_name, raw_value in data.items():
            metric = canonical_metric_name(str(raw_name))
            value = float(raw_value)
            record_id = store.save_performance_event(
                asset_id=asset_id,
                asset_type=asset_type,
                channel=channel,
                metric_name=metric,
                metric_value=value,
                notes=notes,
            )
            recorded.append({"id": record_id, "metric": metric, "value": value})
    elif text:
        parsed = parse_metrics(text)
        record_ids = store.save_performance_text(
            asset_id=asset_id,
            asset_type=asset_type,
            channel=channel,
            text=text,
            notes=notes,
        )
        recorded = [
            {"id": record_id, "metric": metric.name, "value": metric.value}
            for record_id, metric in zip(record_ids, parsed)
        ]
    else:
        raise SystemExit("Provide --metrics-json or --text.")

    return {
        "asset_id": asset_id,
        "asset_type": asset_type,
        "channel": channel,
        "count": len(recorded),
        "recorded": recorded,
        "note": (
            "Link this asset_id to a saved benchmark example of the same ID for the metric to "
            "influence future pattern ranking."
        ),
    }


def build_utm(
    *,
    asset_id: str,
    url: str,
    source: str,
    medium: str,
    campaign: str,
    variant: str | None,
    term: str | None,
) -> dict[str, Any]:
    tagged = build_utm_url(
        url,
        asset_id=asset_id,
        source=source,
        medium=medium,
        campaign=campaign,
        variant=variant,
        term=term,
    )
    return {"asset_id": asset_id, "tagged_url": tagged}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    compile_parser = commands.add_parser("compile", help="Compile WMI context for a request.")
    compile_parser.add_argument("--request", required=True)
    compile_parser.add_argument("--live", action="store_true")
    compile_parser.add_argument("--limit", type=int, default=5)

    validate_parser = commands.add_parser("validate", help="Validate a created draft.")
    validate_parser.add_argument("--request", required=True)
    validate_parser.add_argument("--draft-file", type=Path, required=True)

    perf_parser = commands.add_parser(
        "record-performance", help="Record performance metrics for a published asset."
    )
    perf_parser.add_argument("--asset-id", required=True)
    perf_parser.add_argument("--asset-type", required=True)
    perf_parser.add_argument("--channel", required=True)
    perf_parser.add_argument("--metrics-json", help='JSON object, e.g. {"saves": 42, "signups": 8}')
    perf_parser.add_argument("--text", help="Natural-language performance note.")
    perf_parser.add_argument("--notes", default="")

    utm_parser = commands.add_parser(
        "utm", help="Build a tracked link that carries the asset ID in utm_content."
    )
    utm_parser.add_argument("--asset-id", required=True)
    utm_parser.add_argument("--url", required=True)
    utm_parser.add_argument("--source", required=True)
    utm_parser.add_argument("--medium", required=True)
    utm_parser.add_argument("--campaign", required=True)
    utm_parser.add_argument("--variant")
    utm_parser.add_argument("--term")
    return parser


def main() -> None:
    args = _parser().parse_args()
    if args.command == "compile":
        result = compile_context(args.request, live=args.live, limit=args.limit)
    elif args.command == "validate":
        draft = args.draft_file.read_text(encoding="utf-8")
        result = validate_draft(args.request, draft)
    elif args.command == "record-performance":
        result = record_performance(
            asset_id=args.asset_id,
            asset_type=args.asset_type,
            channel=args.channel,
            metrics_json=args.metrics_json,
            text=args.text,
            notes=args.notes,
        )
    else:
        result = build_utm(
            asset_id=args.asset_id,
            url=args.url,
            source=args.source,
            medium=args.medium,
            campaign=args.campaign,
            variant=args.variant,
            term=args.term,
        )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
