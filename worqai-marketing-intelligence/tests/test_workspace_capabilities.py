from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from worqai_marketing_intel import MarketingOrchestrator
from worqai_marketing_intel.action_planner import ActionPlanner
from worqai_marketing_intel.models import WorkspaceInspection
from worqai_marketing_intel.router import classify
from worqai_marketing_intel.verification_runner import VerificationRunner
from worqai_marketing_intel.workspace_manager import WorkspaceManager
from worqai_marketing_intel.workspace_writer import WorkspaceWriter, plan_from_payload


def test_capability_routing_matches_real_workspace_roles():
    manager = WorkspaceManager()

    assert manager.recommend(classify("Implement an SEO page for cv con ia")).workspace_id == "cv-tailored"
    assert manager.recommend(classify("Create a launch campaign archive")).workspace_id == "worqai-launch"
    assert manager.recommend(classify("Create an ATS carousel")).workspace_id == "worqai-marketing"
    assert manager.recommend(classify("Create an Instagram carousel")).workspace_id == "worqai-marketing"
    assert manager.recommend(classify("Create an Instagram reel from real footage")).workspace_id == "worqai-reel-factory"
    assert manager.recommend(classify("Produce a motion video")).workspace_id == "motion-studio"


@pytest.mark.parametrize(
    ("request_text", "workspace_id", "capability_id", "adapter", "source_format", "output_format"),
    [
        (
            "Implement an SEO page for cv con ia",
            "cv-tailored",
            "nextjs-website-seo-implementation",
            "nextjs_implementation",
            "implementation_brief_json",
            "nextjs_typescript_implementation",
        ),
        (
            "Create an ATS carousel",
            "worqai-marketing",
            "carousel-build-export",
            "carousel_build_export",
            "carousel_spec_json",
            "carousel_html_and_zip",
        ),
        (
            "Create an Instagram reel from real footage",
            "worqai-reel-factory",
            "reel-factory-real-footage-production",
            "reel_factory_handoff",
            "reel_factory_brief_json",
            "human_reviewed_captioned_reel_candidate_mp4",
        ),
        (
            "Produce a motion video for WorqAI",
            "motion-studio",
            "produce-motion-video",
            "produce_motion_video",
            "motion_creative_brief_markdown",
            "motion_video_mp4",
        ),
    ],
)
def test_action_plan_identifies_capability_source_verification_and_output(
    request_text: str,
    workspace_id: str,
    capability_id: str,
    adapter: str,
    source_format: str,
    output_format: str,
):
    brief = MarketingOrchestrator().brief(request_text)
    inspection = WorkspaceInspection(
        workspace_id=workspace_id,
        path=brief.workspace.path,
        exists=True,
        project_type="nextjs" if workspace_id == "cv-tailored" else "workspace",
        is_git_repo=True,
        current_branch="main",
        dirty=False,
    )

    plan = ActionPlanner().plan(brief, (inspection,))

    assert plan.workspace_id == workspace_id
    assert plan.capability_id == capability_id
    assert plan.adapter == adapter
    assert plan.source_format == source_format
    assert plan.output_format == output_format
    assert plan.write_mode == "stage_capability_source"
    assert plan.human_approval_required is True
    assert plan.verification_commands
    assert any("Intended source artifact:" in note for note in plan.safety_notes)
    assert any("Final output:" in note for note in plan.safety_notes)


def test_carousel_writer_stages_renderer_compatible_spec_in_temp_workspace(tmp_path: Path):
    brief = MarketingOrchestrator().brief("Create an ATS carousel")
    inspection = WorkspaceInspection(
        workspace_id="worqai-marketing",
        path=brief.workspace.path,
        exists=True,
        project_type="workspace",
        is_git_repo=True,
        dirty=False,
    )
    planned = ActionPlanner().plan(brief, (inspection,))
    plan = replace(planned, workspace_path=str(tmp_path), can_write=True)

    result = WorkspaceWriter().write_payload(
        plan_id="capability-test",
        plan=plan,
        brief_payload=MarketingOrchestrator().brief_dict("Create an ATS carousel"),
        dry_run=False,
    )

    payload = json.loads(Path(result.destination_path).read_text(encoding="utf-8"))
    assert result.wrote is True
    assert set(payload) >= {"meta", "slides"}
    assert payload["meta"]["source_plan_id"] == "capability-test"
    assert payload["slides"][0]["layout"] == "slide-hook-lockup"


def test_reel_factory_writer_stages_a_human_gated_real_footage_brief(tmp_path: Path):
    brief = MarketingOrchestrator().brief("Create an Instagram reel from real footage")
    inspection = WorkspaceInspection(
        workspace_id="worqai-reel-factory",
        path=brief.workspace.path,
        exists=True,
        project_type="node",
        is_git_repo=True,
        current_branch="main",
        dirty=False,
    )
    planned = ActionPlanner().plan(brief, (inspection,))
    plan = replace(planned, workspace_path=str(tmp_path), can_write=True)

    result = WorkspaceWriter().write_payload(
        plan_id="reel-route-test",
        plan=plan,
        brief_payload=MarketingOrchestrator().brief_dict(
            "Create an Instagram reel from real footage"
        ),
        dry_run=False,
    )

    payload = json.loads(Path(result.destination_path).read_text(encoding="utf-8"))
    contract = payload["production_contract"]
    assert result.wrote is True
    assert payload["schema"] == "worqai.reel-factory-production-brief/v1"
    assert payload["status"] == "requires_human_clip_caption_and_storyboard_review"
    assert contract["real_footage_only"] is True
    assert contract["synthetic_people_allowed"] is False
    assert contract["automatic_posting_allowed"] is False
    assert contract["reviewed_caption_corrections_required"] is True
    assert contract["hash_bound_human_approval_required"] is True
    assert payload["factory_handoff"]["rejected_legacy_source"] == "out/variants/"


def test_reel_factory_and_motion_studio_remain_distinct_routes():
    manager = WorkspaceManager()

    reel = manager.recommend(classify("Edit a captioned Instagram reel from real footage"))
    motion = manager.recommend(classify("Create an animated motion video with rendered scenes"))

    assert reel.workspace_id == "worqai-reel-factory"
    assert motion.workspace_id == "motion-studio"


def test_writer_rejects_destination_traversal_before_writing(tmp_path: Path):
    brief = MarketingOrchestrator().brief("Create an ATS carousel")
    inspection = WorkspaceInspection(
        workspace_id="worqai-marketing",
        path=brief.workspace.path,
        exists=True,
        project_type="workspace",
        is_git_repo=True,
        dirty=False,
    )
    planned = ActionPlanner().plan(brief, (inspection,))
    plan = replace(
        planned,
        workspace_path=str(tmp_path),
        asset_relative_path="../escape.json",
        can_write=True,
    )

    with pytest.raises(ValueError, match="outside the target workspace"):
        WorkspaceWriter().write_payload(
            plan_id="escape-test",
            plan=plan,
            brief_payload=MarketingOrchestrator().brief_dict("Create an ATS carousel"),
            dry_run=False,
        )
    assert not (tmp_path.parent / "escape.json").exists()


def test_verification_runner_rejects_traversal_and_production_commands(tmp_path: Path):
    commands = (
        "py scripts/render_carousel.py ../outside.json --validate-only",
        "py scripts/build_carousel.py production/spec.json",
    )

    results = VerificationRunner().run(tmp_path, commands)

    assert all(result.returncode == 1 for result in results)
    assert all("skipped for safety" in result.stderr for result in results)


def test_plan_payload_round_trip_preserves_capability_fields():
    brief = MarketingOrchestrator().brief("Produce a motion video")
    inspection = WorkspaceInspection(
        workspace_id="motion-studio",
        path=brief.workspace.path,
        exists=True,
        project_type="motion-studio",
        is_git_repo=True,
    )
    plan = ActionPlanner().plan(brief, (inspection,))
    payload = dict(plan.__dict__)

    restored = plan_from_payload(payload)

    assert restored.capability_id == "produce-motion-video"
    assert restored.adapter == "produce_motion_video"
    assert restored.source_format == "motion_creative_brief_markdown"
    assert restored.output_format == "motion_video_mp4"
