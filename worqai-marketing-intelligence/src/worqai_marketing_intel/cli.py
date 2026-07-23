"""Command-line interface for WorqAI Marketing Intelligence."""

from __future__ import annotations

import argparse
import json

from .codec import to_plain
from .memory_store import MemoryStore
from .orchestrator import MarketingOrchestrator
from .prompt_runtime import run_prompt


def main() -> None:
    parser = argparse.ArgumentParser(prog="wmi", description="WorqAI Marketing Intelligence")
    parser.add_argument(
        "command",
        choices=[
            "brief",
            "run",
            "audit-script",
            "route",
            "score",
            "history",
            "export",
            "inspect-workspaces",
            "plan",
            "plans",
            "approve",
            "produce",
            "execute",
            "remember-example",
            "examples",
            "record-performance",
            "research",
            "research-url",
        ],
    )
    parser.add_argument("text", nargs="?")
    parser.add_argument("--json", action="store_true", help="Print structured JSON")
    parser.add_argument("--save", action="store_true", help="Save brief to SQLite memory")
    parser.add_argument("--write", action="store_true", help="Write brief to production Markdown")
    parser.add_argument("--execute", action="store_true", help="Actually write an approved plan")
    parser.add_argument("--create-branch", action="store_true", help="Create/switch to recommended branch during execute")
    parser.add_argument("--verify", action="store_true", help="Run verification commands during execute")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow execution in a dirty Git workspace")
    parser.add_argument("--live", action="store_true", help="Use live web research when supported")
    parser.add_argument("--limit", type=int, default=10, help="History row limit")
    args = parser.parse_args()

    orchestrator = MarketingOrchestrator()
    if args.command == "run":
        _require_text(args.text, "run")
        result = run_prompt(
            args.text,
            orchestrator=orchestrator,
            save=args.save,
            live_research=args.live,
            limit=args.limit,
        )
        data = to_plain(result)
        print(json.dumps(data, indent=2) if args.json else _render_prompt_runtime(data))
        return
    if args.command == "brief":
        _require_text(args.text, "brief")
        result = orchestrator.brief(args.text)
        record_id = MemoryStore().save_brief(result) if args.save else None
        artifact_path = orchestrator.write_brief(result, record_id=record_id) if args.write else None
    elif args.command == "audit-script":
        _require_text(args.text, "audit-script")
        request, script = _parse_audit_script(args.text)
        data = orchestrator.audit_script(request, script)
        print(json.dumps(data, indent=2) if args.json else _render_script_audit(data))
        return
    elif args.command == "route":
        _require_text(args.text, "route")
        result = orchestrator.route(args.text)
        record_id = None
        artifact_path = None
    elif args.command == "score":
        _require_text(args.text, "score")
        result = orchestrator.score(args.text)
        record_id = None
        artifact_path = None
    elif args.command == "history":
        records = MemoryStore().list_briefs(limit=args.limit)
        data = [to_plain(record) for record in records]
        print(json.dumps(data, indent=2) if args.json else _render_history(data))
        return
    elif args.command == "inspect-workspaces":
        result = orchestrator.inspect_workspaces()
        data = to_plain(result)
        print(json.dumps(data, indent=2) if args.json else _render_workspace_inspections(data))
        return
    elif args.command == "plan":
        _require_text(args.text, "plan")
        brief, plan = orchestrator.action_plan(args.text)
        data = to_plain(plan)
        if args.save:
            data["plan_id"] = MemoryStore().save_action_plan(plan, brief)
        print(json.dumps(data, indent=2) if args.json else _render_action_plan(data))
        return
    elif args.command == "plans":
        records = MemoryStore().list_action_plans(limit=args.limit)
        data = [to_plain(record) for record in records]
        print(json.dumps(data, indent=2) if args.json else _render_plan_records(data))
        return
    elif args.command == "approve":
        _require_text(args.text, "approve")
        MemoryStore().approve_action_plan(args.text)
        print(f"Approved action plan {args.text}")
        return
    elif args.command == "produce":
        _require_text(args.text, "produce")
        store = MemoryStore()
        status, plan_payload, brief_payload = store.get_action_plan_bundle(args.text)
        if status != "approved" and args.execute:
            raise SystemExit("Plan must be approved before --execute can write.")
        result = orchestrator.produce_from_payload(
            plan_id=args.text,
            plan_payload=plan_payload,
            brief_payload=brief_payload,
            dry_run=not args.execute,
        )
        data = to_plain(result)
        print(json.dumps(data, indent=2) if args.json else _render_production_result(data))
        return
    elif args.command == "execute":
        _require_text(args.text, "execute")
        store = MemoryStore()
        status, plan_payload, brief_payload = store.get_action_plan_bundle(args.text)
        if status != "approved" and args.execute:
            raise SystemExit("Plan must be approved before --execute can write.")
        result = orchestrator.execute_from_payload(
            plan_id=args.text,
            plan_payload=plan_payload,
            brief_payload=brief_payload,
            dry_run=not args.execute,
            create_branch=args.create_branch,
            verify=args.verify,
            allow_dirty=args.allow_dirty,
        )
        if result.wrote:
            store.update_action_plan_status(args.text, "produced")
        data = to_plain(result)
        print(json.dumps(data, indent=2) if args.json else _render_production_result(data))
        return
    elif args.command == "remember-example":
        _require_text(args.text, "remember-example")
        example = _parse_example(args.text)
        record_id = MemoryStore().save_benchmark_example(**example)
        print(f"Saved benchmark example {record_id}")
        return
    elif args.command == "examples":
        records = MemoryStore().list_benchmark_examples(limit=args.limit)
        data = [to_plain(record) for record in records]
        print(json.dumps(data, indent=2) if args.json else _render_examples(data))
        return
    elif args.command == "record-performance":
        _require_text(args.text, "record-performance")
        fields = _parse_performance(args.text)
        record_ids = MemoryStore().save_performance_text(**fields)
        if record_ids:
            print(f"Recorded {len(record_ids)} metric event(s): {', '.join(record_ids)}")
        else:
            print("No recognizable metrics found in that note.")
        return
    elif args.command == "research":
        _require_text(args.text, "research")
        brief = orchestrator.brief(args.text)
        examples = MemoryStore().list_benchmark_examples(
            asset_type=brief.task.asset_type.value,
            limit=args.limit,
        )
        data = {
            "asset_type": brief.task.asset_type.value,
            "benchmark_patterns": to_plain(brief.benchmark_patterns),
            "saved_examples": [to_plain(example) for example in examples],
        }
        if args.live:
            live_report = orchestrator.live_research(args.text, limit=args.limit)
            data["live_report"] = to_plain(live_report)
            if args.save:
                store = MemoryStore()
                saved_ids = []
                for pattern in live_report.extracted_patterns:
                    saved_ids.append(
                        store.save_benchmark_example(
                            asset_type=pattern.asset_type,
                            title=pattern.title,
                            source=pattern.source,
                            pattern=pattern.pattern,
                            notes=pattern.notes,
                        )
                    )
                data["saved_live_example_ids"] = saved_ids
        print(json.dumps(data, indent=2) if args.json else _render_research(data))
        return
    elif args.command == "research-url":
        _require_text(args.text, "research-url")
        request, url = _parse_research_url(args.text)
        brief = orchestrator.brief(request)
        report = orchestrator.research_url(request, url)
        data = {
            "asset_type": brief.task.asset_type.value,
            "benchmark_patterns": to_plain(brief.benchmark_patterns),
            "saved_examples": [],
            "live_report": to_plain(report),
        }
        if args.save:
            store = MemoryStore()
            saved_ids = []
            for pattern in report.extracted_patterns:
                saved_ids.append(
                    store.save_benchmark_example(
                        asset_type=pattern.asset_type,
                        title=pattern.title,
                        source=pattern.source,
                        pattern=pattern.pattern,
                        notes=pattern.notes,
                    )
                )
            data["saved_live_example_ids"] = saved_ids
        print(json.dumps(data, indent=2) if args.json else _render_research(data))
        return
    else:
        _require_text(args.text, "export")
        payload = MemoryStore().get_brief_payload(args.text)
        artifact_path = _write_payload(payload, record_id=args.text)
        print(str(artifact_path))
        return

    data = to_plain(result)
    if record_id:
        data["memory_id"] = record_id
    if artifact_path:
        data["artifact_path"] = str(artifact_path)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(_render_markdown(args.command, data))


def _render_markdown(command: str, data: dict[str, object]) -> str:
    if command == "route":
        return (
            f"# Workspace Route\n\n"
            f"- Workspace: {data['workspace_id']}\n"
            f"- Path: {data['path']}\n"
            f"- Confidence: {data['confidence']}\n"
            f"- Reason: {data['reason']}\n"
        )

    if command == "score":
        strengths = "\n".join(f"- {item}" for item in data["strengths"])
        risks = "\n".join(f"- {item}" for item in data["risks"])
        return f"# Quality Score\n\n{data['score']}/{data['max_score']}\n\n## Strengths\n{strengths}\n\n## Risks\n{risks}\n"

    task = data["task"]
    workspace = data["workspace"]
    quality = data["quality"]
    patterns = "\n".join(
        f"- {item['name']}: {item['pattern']}" for item in data["benchmark_patterns"]
    )
    agents = ", ".join(data["active_agents"])
    concept = json.dumps(data["concept"], indent=2)
    return (
        f"# WorqAI Marketing Brief\n\n"
        f"- Asset: {task['asset_type']}\n"
        f"- Audience: {task['audience']}\n"
        f"- Agents: {agents}\n"
        f"- Workspace: {workspace['workspace_id']} ({workspace['confidence']})\n\n"
        f"## Strategic Angle\n{data['strategic_angle']}\n\n"
        f"## Benchmark Patterns\n{patterns}\n\n"
        f"## Concept\n```json\n{concept}\n```\n\n"
        f"## Quality\n{quality['score']}/{quality['max_score']}\n"
        f"{_render_saved_lines(data)}"
    )


def _render_prompt_runtime(data: dict[str, object]) -> str:
    mode = str(data["mode"])
    payload = data["payload"]
    notes = _list_or_dash(data["notes"])
    if mode == "script_audit":
        body = _render_script_audit(payload)
    elif mode == "message_reply":
        body = _render_message_reply(payload)
    elif mode == "social_reframe":
        body = _render_social_reframe(payload)
    elif mode == "seo_plan":
        body = _render_json_payload("SEO Plan", payload)
    elif mode == "campaign_package":
        body = _render_json_payload("Campaign Package", payload)
    elif mode == "deep_research":
        body = _render_json_payload("Deep Research Plan", payload)
    elif mode == "feedback_loop":
        body = _render_json_payload("Feedback Loop", payload)
    elif mode == "motion_handoff":
        body = _render_json_payload("Motion Handoff", payload)
    elif mode == "universal_intake":
        body = _render_universal_intake(payload)
    elif mode == "research":
        body = _render_research(payload)
    elif mode == "action_plan":
        body = _render_action_plan(payload)
    else:
        body = _render_markdown("brief", payload)
    return f"# WMI Prompt Runtime\n\n- Mode: `{mode}`\n\n{body}\n\n## Dispatch Notes\n{notes}\n"


def _render_message_reply(data: dict[str, object]) -> str:
    rules = _list_or_dash(data["tone_rules"])
    return (
        "# Message Reply\n\n"
        f"- Intent: `{data['intent']}`\n\n"
        f"## Recommended Reply\n{data['recommended_reply']}\n\n"
        f"## Short Reply\n{data['short_reply']}\n\n"
        f"## Friendly Reply\n{data['friendly_reply']}\n\n"
        f"## Follow-Up Question\n{data['follow_up_question']}\n\n"
        f"## Tone Rules\n{rules}\n"
    )


def _render_universal_intake(data: dict[str, object]) -> str:
    options = "\n".join(
        f"- `{item['mode']}`: {item['use_for']} Example: {item['example']}"
        for item in data["routing_options"]
    )
    examples = _list_or_dash(data["better_prompt_examples"])
    return (
        "# Universal Intake\n\n"
        f"- Intent: `{data['interpreted_intent']}`\n"
        f"- Best mode: `{data['best_mode']}`\n"
        f"- Confidence: {data['confidence']}\n\n"
        f"## What I Would Do\n{data['what_i_would_do']}\n\n"
        f"## Immediate Output\n{data['immediate_output']}\n\n"
        f"## Better Prompt Examples\n{examples}\n\n"
        f"## Available Routes\n{options}\n"
    )


def _render_json_payload(title: str, data: dict[str, object]) -> str:
    payload = json.dumps(data, indent=2, ensure_ascii=False)
    return f"# {title}\n\n```json\n{payload}\n```"


def _render_social_reframe(data: dict[str, object]) -> str:
    hooks = _list_or_dash(data["hook_options"])
    keep = _list_or_dash(data["what_to_keep"])
    change = _list_or_dash(data["what_to_change"])
    trust = _list_or_dash(data["trust_notes"])
    return (
        "# Social Reframe\n\n"
        f"- Format: `{data['format']}`\n"
        f"- Audience: `{data['audience']}`\n\n"
        f"## Diagnosis\n{data['diagnosis']}\n\n"
        f"## Hook Options\n{hooks}\n\n"
        f"## Keep\n{keep}\n\n"
        f"## Change\n{change}\n\n"
        f"## Recommended Post\n{data['recommended_post']}\n\n"
        f"## Short Version\n{data['short_version']}\n\n"
        f"## Comment Reply\n{data['comment_reply']}\n\n"
        f"## Trust Notes\n{trust}\n"
    )


def _render_saved_lines(data: dict[str, object]) -> str:
    lines: list[str] = []
    if "memory_id" in data:
        lines.append(f"\n- Saved memory ID: `{data['memory_id']}`")
    if "artifact_path" in data:
        lines.append(f"\n- Artifact: `{data['artifact_path']}`")
    return "".join(lines)


def _render_history(records: list[dict[str, object]]) -> str:
    if not records:
        return "No saved briefs yet."
    return "\n".join(
        f"{item['id']}  {item['asset_type']}  {item['workspace_id']}  "
        f"{item['quality_score']}/10  {item['request']}"
        for item in records
    )


def _render_script_audit(data: dict[str, object]) -> str:
    issues = "\n".join(
        f"- [{item['severity']}] {item['problem']} Fix: {item['fix']}"
        for item in data["issues"]
    ) or "- No major issues found."
    keep = _list_or_dash(data["what_to_keep"])
    cut = _list_or_dash(data["what_to_cut_or_compress"])
    visuals = _list_or_dash(data["visual_beats"])
    return (
        "# Script Audit\n\n"
        f"- Language: `{data['language']}`\n"
        f"- Words: {data['word_count']}\n"
        f"- Estimated duration: {data['estimated_duration']}\n"
        f"- Score: {data['score']['value']}/{data['score']['max']} ({data['score']['label']})\n\n"
        f"## Diagnosis\n{data['diagnosis']}\n\n"
        f"## Hook\n- Current: {data['hook_audit']['current_hook']}\n"
        f"- Recommended: {data['hook_audit']['recommended_hook']}\n"
        f"- Why: {data['hook_audit']['reason']}\n\n"
        f"## Issues\n{issues}\n\n"
        f"## Keep\n{keep}\n\n"
        f"## Cut Or Compress\n{cut}\n\n"
        f"## Rewritten Script\n{data['rewritten_script']}\n\n"
        f"## Visual Beats\n{visuals}\n\n"
        f"## Best Line\n{data['best_line']}\n\n"
        f"## CTA\n{data['cta']}\n"
    )


def _render_workspace_inspections(inspections: list[dict[str, object]]) -> str:
    if not inspections:
        return "No workspaces configured."
    blocks: list[str] = ["# Workspace Inspection"]
    for item in inspections:
        commands = _list_or_dash(item["available_commands"])
        destinations = _list_or_dash(item["asset_destinations"])
        important = _list_or_dash(item["important_files"])
        notes = _list_or_dash(item["notes"])
        dirty = "unknown" if item["dirty"] is None else str(item["dirty"]).lower()
        blocks.append(
            f"## {item['workspace_id']}\n\n"
            f"- Path: `{item['path']}`\n"
            f"- Exists: {str(item['exists']).lower()}\n"
            f"- Project type: `{item['project_type']}`\n"
            f"- Git repo: {str(item['is_git_repo']).lower()}\n"
            f"- Branch: `{item['current_branch'] or '-'}`\n"
            f"- Dirty: {dirty}\n"
            f"- Access error: `{item['access_error'] or '-'}`\n\n"
            f"Commands:\n{commands}\n\n"
            f"Asset destinations:\n{destinations}\n\n"
            f"Important files:\n{important}\n\n"
            f"Notes:\n{notes}\n"
        )
    return "\n".join(blocks)


def _render_action_plan(data: dict[str, object]) -> str:
    verification = _list_or_dash(data["verification_commands"])
    safety = _list_or_dash(data["safety_notes"])
    plan_id = f"- Plan ID: `{data['plan_id']}`\n" if "plan_id" in data else ""
    return (
        "# Workspace Action Plan\n\n"
        f"{plan_id}"
        f"- Workspace: `{data['workspace_id']}`\n"
        f"- Workspace path: `{data['workspace_path']}`\n"
        f"- Asset type: `{data['asset_type']}`\n"
        f"- Current branch: `{data['current_branch'] or '-'}`\n"
        f"- Dirty: {data['dirty']}\n"
        f"- Recommended branch: `{data['recommended_branch']}`\n"
        f"- Asset path: `{data['asset_relative_path']}`\n"
        f"- Write mode: `{data['write_mode']}`\n"
        f"- Can write: {str(data['can_write']).lower()}\n"
        f"- Human approval required: {str(data['human_approval_required']).lower()}\n\n"
        f"Verification:\n{verification}\n\n"
        f"Safety notes:\n{safety}\n"
    )


def _render_plan_records(records: list[dict[str, object]]) -> str:
    if not records:
        return "No saved action plans yet."
    return "\n".join(
        f"{item['id']}  {item['status']}  {item['asset_type']}  "
        f"{item['workspace_id']}  {item['request']}"
        for item in records
    )


def _render_production_result(data: dict[str, object]) -> str:
    notes = _list_or_dash(data["notes"])
    verification = _list_or_dash(data["verification_commands"])
    return (
        "# Production Result\n\n"
        f"- Plan ID: `{data['plan_id']}`\n"
        f"- Workspace: `{data['workspace_id']}`\n"
        f"- Destination: `{data['destination_path']}`\n"
        f"- Dry run: {str(data['dry_run']).lower()}\n"
        f"- Wrote file: {str(data['wrote']).lower()}\n\n"
        f"Verification:\n{verification}\n\n"
        f"Notes:\n{notes}\n"
    )


def _render_examples(records: list[dict[str, object]]) -> str:
    if not records:
        return "No benchmark examples saved yet."
    return "\n".join(
        f"{item['id']}  {item['asset_type']}  {item['title']}  {item['source']}"
        for item in records
    )


def _render_research(data: dict[str, object]) -> str:
    patterns = "\n".join(
        f"- {item['name']}: {item['pattern']}" for item in data["benchmark_patterns"]
    )
    examples = (
        "\n".join(
            f"- {item['title']} ({item['source']}): {item['pattern']}"
            for item in data["saved_examples"]
        )
        if data["saved_examples"]
        else "- No saved examples for this asset type yet."
    )
    live = ""
    if "live_report" in data:
        report = data["live_report"]
        references = (
            "\n".join(
                f"- {item['title']} ({item['url']})\n  {item['snippet']}"
                for item in report["references"]
            )
            if report["references"]
            else "- No live references returned."
        )
        extracted = (
            "\n".join(
                f"- {item['title']}: {item['pattern']} ({item['confidence']})"
                for item in report["extracted_patterns"]
            )
            if report["extracted_patterns"]
            else "- No live patterns extracted."
        )
        warnings = _list_or_dash(report["warnings"])
        saved = _list_or_dash(data.get("saved_live_example_ids", []))
        live = (
            f"\n## Live Research\n\n"
            f"- Query: `{report['query']}`\n\n"
            f"### References\n{references}\n\n"
            f"### Extracted Patterns\n{extracted}\n\n"
            f"### Warnings\n{warnings}\n\n"
            f"### Saved Live Example IDs\n{saved}\n"
        )
    return (
        "# Benchmark Research\n\n"
        f"- Asset type: `{data['asset_type']}`\n\n"
        f"## Pattern Library\n{patterns}\n\n"
        f"## Saved Examples\n{examples}\n"
        f"{live}"
    )


def _list_or_dash(values: object) -> str:
    if not values:
        return "- -"
    return "\n".join(f"- `{item}`" for item in values)


def _require_text(text: str | None, command: str) -> None:
    if not text:
        raise SystemExit(f"`{command}` requires text")


def _parse_example(text: str) -> dict[str, str]:
    parts = [part.strip() for part in text.split("|")]
    if len(parts) < 4:
        raise SystemExit(
            "remember-example format: asset_type | title | source | pattern | optional notes"
        )
    return {
        "asset_type": parts[0],
        "title": parts[1],
        "source": parts[2],
        "pattern": parts[3],
        "notes": parts[4] if len(parts) > 4 else "",
    }


def _parse_performance(text: str) -> dict[str, str]:
    parts = [part.strip() for part in text.split("|", maxsplit=3)]
    if len(parts) < 4 or not all(parts[:4]):
        raise SystemExit(
            "record-performance format: asset_id | asset_type | channel | performance note"
        )
    return {"asset_id": parts[0], "asset_type": parts[1], "channel": parts[2], "text": parts[3]}


def _parse_research_url(text: str) -> tuple[str, str]:
    parts = [part.strip() for part in text.split("|", maxsplit=1)]
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise SystemExit("research-url format: request | https://example.com/reference")
    return parts[0], parts[1]


def _parse_audit_script(text: str) -> tuple[str, str]:
    parts = [part.strip() for part in text.split("|", maxsplit=1)]
    if len(parts) == 2 and parts[0] and parts[1]:
        return parts[0], parts[1]
    return "Audit and improve a Spanish IG reel script for WorqAI about ATS resume tailoring", text


def _write_payload(payload: dict[str, object], *, record_id: str):
    from .artifact_writer import ArtifactWriter, render_brief

    writer = ArtifactWriter()
    task = payload["task"]
    path = writer.output_dir / f"{task['asset_type']}-{record_id}.md"
    path.write_text(render_brief(payload, record_id=record_id), encoding="utf-8")
    return path


if __name__ == "__main__":
    main()
