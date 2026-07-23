from worqai_marketing_intel import MarketingOrchestrator, run_prompt
from worqai_marketing_intel.action_planner import ActionPlanner
from worqai_marketing_intel.codec import to_plain
from worqai_marketing_intel.memory_store import MemoryStore
from worqai_marketing_intel.models import AssetType, WorkspaceActionPlan, WorkspaceInspection
from worqai_marketing_intel.models import SearchReference
from worqai_marketing_intel.research_adapters.live_research import LiveResearchRunner
from worqai_marketing_intel.router import classify
from worqai_marketing_intel.verification_runner import VerificationRunner
from worqai_marketing_intel.workspace_inspector import WorkspaceInspector
from worqai_marketing_intel.workspace_writer import WorkspaceWriter
import json


def test_carousel_request_routes_to_marketing_workspace():
    brief = MarketingOrchestrator().brief("Create a carousel for WorqAI resume tailoring")

    assert brief.task.asset_type == AssetType.CAROUSEL
    assert brief.workspace.workspace_id == "worqai-marketing"
    assert "carousel-architect" in brief.active_agents
    assert brief.quality.score >= 7


def test_motion_request_routes_to_motion_studio():
    brief = MarketingOrchestrator().brief("Make a motion video idea for AI resume tailoring")

    assert brief.task.asset_type == AssetType.MOTION_VIDEO
    assert brief.workspace.workspace_id == "motion-studio"
    assert "motion-creative-director" in brief.active_agents


def test_ig_reel_request_uses_reel_engine():
    brief = MarketingOrchestrator().brief("Give me IG reel script ideas for WorqAI resume tailoring")

    assert brief.task.asset_type == AssetType.IG_REEL
    assert brief.workspace.workspace_id == "worqai-reel-factory"
    assert brief.concept["format"].startswith("3 short-form video concepts")
    assert "market-research-scout" in brief.active_agents


def test_script_audit_engine_scores_pasted_reel_script():
    script = (
        "Estamos en una era en la que buscar trabajo es un trabajo de tiempo completo. "
        "Antes usted competia contra solo la gente de su zona. Ahora compite contra 500 personas. "
        "Si su cv no coincide con la descripcion, un humano nunca llega a verlo. "
        "WorqAI adapta su CV sin inventar nada. Link en la bio."
    )

    audit = MarketingOrchestrator().audit_script(
        "Audit Spanish IG reel script for WorqAI",
        script,
    )

    assert audit["format"] == "Spanish reel script audit"
    assert audit["score"]["value"] <= 8
    assert audit["hook_audit"]["recommended_hook"].startswith("Su CV")
    assert "inventar" in audit["rewritten_script"].lower()


def test_prompt_runtime_dispatches_script_audit():
    result = run_prompt(
        "Audit this reel script for WorqAI: Estamos en una era en la que buscar trabajo "
        "es un trabajo de tiempo completo. Si su CV no coincide, un humano nunca llega a verlo."
    )

    assert result.mode == "script_audit"
    assert result.payload["format"] == "Spanish reel script audit"
    assert not result.payload["hook_audit"]["current_hook"].startswith("Audit")


def test_prompt_runtime_dispatches_research():
    result = run_prompt("Research successful examples for a WorqAI carousel about ATS resumes")

    assert result.mode == "research"
    assert result.payload["asset_type"] == "carousel"
    assert result.payload["benchmark_patterns"]


def test_prompt_runtime_keeps_known_asset_brief_path():
    result = run_prompt("WMI, give me IG reel ideas for WorqAI")

    assert result.mode == "brief"
    assert result.payload["task"]["asset_type"] == "ig_reel"


def test_prompt_runtime_executes_vague_prompts_through_universal_intake():
    result = run_prompt("this feels weak what should we do")

    assert result.mode == "brief"
    assert result.payload["intake_decision"]["interpreted_intent"] == "taste_or_quality_check"
    assert result.payload["intake_decision"]["execution_policy"] == "execute_once_with_recursion_guard"


def test_prompt_runtime_dispatches_fast_message_reply():
    result = run_prompt("Reply to this message: Es gratis o tengo que poner tarjeta?")

    assert result.mode == "message_reply"
    assert result.payload["intent"] == "pricing_or_free_access"
    assert "gratis" in result.payload["recommended_reply"].lower()


def test_prompt_runtime_dispatches_seo_plan():
    result = run_prompt("Make an SEO plan so WorqAI can rank for cv con ia")

    assert result.mode == "seo_plan"
    assert result.payload["priority_pages"][0]["slug"] == "/cv-con-ia"


def test_prompt_runtime_dispatches_campaign_package():
    result = run_prompt("Create a full campaign package for WorqAI LatAm job seekers")

    assert result.mode == "campaign_package"
    assert "reels" in result.payload["assets"]
    assert "seo" in result.payload["assets"]


def test_prompt_runtime_dispatches_feedback_loop():
    result = run_prompt("Build a feedback loop so WMI can learn from impressions, CTR, and replies")

    assert result.mode == "feedback_loop"
    assert "metrics_by_channel" in result.payload


def test_prompt_runtime_dispatches_motion_handoff():
    result = run_prompt("Create a Motion Studio handoff with render manifest for the ATS video")

    assert result.mode == "motion_handoff"
    assert result.payload["target_workspace"] == "motion-studio"


def test_prompt_runtime_dispatches_deep_research():
    result = run_prompt("Run deep research and competitor analysis for CV con IA pages")

    assert result.mode == "deep_research"
    assert result.payload["source_sets"]


def test_prompt_runtime_dispatches_social_reframe_before_script_audit():
    result = run_prompt(
        "Rewrite this LinkedIn group post for job seekers: Si está buscando brete esto le puede servir. "
        "Con un compa hicimos una página para adaptar el CV a cada puesto."
    )

    assert result.mode == "social_reframe"
    assert "recommended_post" in result.payload


def test_university_pitch_request_uses_pitch_engine():
    brief = MarketingOrchestrator().brief("Pitch WorqAI to universities and workforce institutions")

    assert brief.task.asset_type == AssetType.PARTNERSHIP_PITCH
    assert brief.workspace.workspace_id == "worqai-marketing"
    assert brief.audience == "career centers, universities, institutions, and workforce programs"
    assert "partnership-pitch-strategist" in brief.active_agents
    assert brief.concept["segment"] == "university career and employability team"
    assert brief.concept["pilot"]


def test_brief_can_build_seo_concept():
    brief = MarketingOrchestrator().brief("SEO page for cv con ia")

    assert brief.task.asset_type == AssetType.SEO_PAGE
    assert brief.workspace.workspace_id == "cv-tailored"
    assert "priority_pages" in brief.concept


def test_brief_can_build_campaign_package():
    brief = MarketingOrchestrator().brief("Create a campaign package for WorqAI")

    assert brief.task.asset_type == AssetType.CAMPAIGN_PACKAGE
    assert brief.workspace.workspace_id == "worqai-marketing"
    assert "assets" in brief.concept


def test_score_penalizes_banned_language():
    score = MarketingOrchestrator().score("Leverage AI to unlock your potential with a game-changing platform.")

    assert score.score < 8
    assert "leverage ai" in score.banned_phrases


def test_memory_store_saves_brief(tmp_path):
    brief = MarketingOrchestrator().brief("Create a carousel for WorqAI resume tailoring")
    store = MemoryStore(tmp_path / "memory.db")

    record_id = store.save_brief(brief)
    records = store.list_briefs()
    payload = store.get_brief_payload(record_id)

    assert records[0].id == record_id
    assert payload["task"]["asset_type"] == "carousel"


def test_workspace_inspector_detects_node_workspace(tmp_path):
    workspace = tmp_path / "worqai-marketing"
    workspace.mkdir()
    (workspace / "package.json").write_text(
        json.dumps({"scripts": {"build": "vite build", "dev": "vite"}}),
        encoding="utf-8",
    )
    (workspace / "campaigns").mkdir()
    registry = tmp_path / "workspaces.json"
    registry.write_text(
        json.dumps(
            {
                "workspaces": [
                    {
                        "id": "worqai-marketing",
                        "path": str(workspace),
                        "purpose": "Campaign assets",
                        "asset_types": ["carousel"],
                        "signals": ["carousel"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    inspection = WorkspaceInspector(registry).inspect_all()[0]

    assert inspection.exists is True
    assert inspection.project_type == "node"
    assert "npm run build" in inspection.available_commands
    assert "campaigns" in inspection.asset_destinations


def test_workspace_inspector_emits_executable_python_verification(tmp_path):
    workspace = tmp_path / "python-project"
    workspace.mkdir()
    (workspace / "src").mkdir()
    (workspace / "pyproject.toml").write_text("[project]\nname = \"demo\"\n", encoding="utf-8")
    registry = tmp_path / "workspaces.json"
    registry.write_text(
        json.dumps(
            {
                "workspaces": [
                    {
                        "id": "demo",
                        "path": str(workspace),
                        "purpose": "Python project",
                        "asset_types": ["campaign"],
                        "signals": ["demo"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    inspection = WorkspaceInspector(registry).inspect_all()[0]

    assert "python -m compileall -q src" in inspection.available_commands
    assert "python project detected" not in inspection.available_commands


def test_action_plan_can_be_saved_and_approved(tmp_path):
    orchestrator = MarketingOrchestrator()
    brief = orchestrator.brief("Create a carousel for WorqAI resume tailoring")
    plan = ActionPlanner().plan(
        brief,
        (
            WorkspaceInspection(
                workspace_id="worqai-marketing",
                path=str(tmp_path),
                exists=True,
                project_type="markdown",
                is_git_repo=True,
                current_branch="main",
                dirty=False,
                available_commands=("manual_review_generated_markdown",),
                asset_destinations=("production",),
            ),
        ),
    )
    store = MemoryStore(tmp_path / "memory.db")

    plan_id = store.save_action_plan(plan, brief)
    store.approve_action_plan(plan_id)
    status, plan_payload, brief_payload = store.get_action_plan_bundle(plan_id)

    assert status == "approved"
    assert plan_payload["workspace_id"] == "worqai-marketing"
    assert brief_payload["task"]["asset_type"] == "carousel"


def test_benchmark_examples_are_stored(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")

    record_id = store.save_benchmark_example(
        asset_type="carousel",
        title="Before after resume teardown",
        source="manual",
        pattern="Show weak bullet, explain why it fails, rewrite with role-specific proof.",
    )
    examples = store.list_benchmark_examples(asset_type="carousel")

    assert examples[0].id == record_id
    assert examples[0].asset_type == "carousel"


def test_performance_events_are_stored(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")

    record_id = store.save_performance_event(
        asset_id="post-001",
        asset_type="linkedin_post",
        channel="social",
        metric_name="comments",
        metric_value=7,
        notes="Founder post about CV con IA.",
    )
    events = store.list_performance_events(channel="social")

    assert events[0].id == record_id
    assert events[0].metric_name == "comments"
    assert events[0].metric_value == 7


def test_workspace_writer_dry_run_stays_read_only(tmp_path):
    plan = WorkspaceActionPlan(
        workspace_id="worqai-marketing",
        workspace_path=str(tmp_path),
        asset_type="carousel",
        source_request="Create carousel",
        current_branch="main",
        dirty=False,
        recommended_branch="codex/wmi-carousel-test",
        asset_relative_path="production/test/carousel-test.md",
        write_mode="create_new_markdown_artifact",
        can_write=True,
        human_approval_required=True,
        verification_commands=("manual_review_generated_markdown",),
        safety_notes=("Test plan",),
    )
    payload = MarketingOrchestrator().brief_dict("Create a carousel for WorqAI resume tailoring")

    result = WorkspaceWriter().write_payload(
        plan_id="plan123",
        plan=plan,
        brief_payload=payload,
        dry_run=True,
    )

    assert result.wrote is False
    assert not (tmp_path / "production" / "test" / "carousel-test.md").exists()


def test_execution_engine_dry_run_stays_read_only(tmp_path):
    plan = WorkspaceActionPlan(
        workspace_id="worqai-marketing",
        workspace_path=str(tmp_path),
        asset_type="carousel",
        source_request="Create carousel",
        current_branch="main",
        dirty=False,
        recommended_branch="codex/wmi-carousel-test",
        asset_relative_path="production/test/carousel-test.md",
        write_mode="create_new_markdown_artifact",
        can_write=True,
        human_approval_required=True,
        verification_commands=("manual_review_generated_markdown",),
        safety_notes=("Test plan",),
    )
    payload = MarketingOrchestrator().brief_dict("Create a carousel for WorqAI resume tailoring")

    result = MarketingOrchestrator().execute_from_payload(
        plan_id="plan123",
        plan_payload=to_plain(plan),
        brief_payload=payload,
        dry_run=True,
        create_branch=True,
        verify=True,
    )

    assert result.wrote is False
    assert not (tmp_path / "production" / "test" / "carousel-test.md").exists()
    assert "Dry run only; no file was written." in result.notes
    assert "Dry run: would run verification commands." in result.notes


def test_verification_runner_skips_unsupported_commands(tmp_path):
    result = VerificationRunner().run(tmp_path, ("python project detected",))[0]

    assert result.returncode == 1
    assert "skipped for safety" in result.stderr


def test_live_research_runner_extracts_patterns_from_fake_search():
    class FakeSearch:
        def search(self, query, *, limit=5):
            return (
                SearchReference(
                    title="LinkedIn carousel teardown: why resumes fail",
                    url="https://example.com/resume-carousel",
                    snippet="A teardown showing the mistake, the missing proof, and the rewritten bullet.",
                    source="fake",
                ),
            )

    task = classify("Create a carousel for WorqAI resume tailoring")
    report = LiveResearchRunner(FakeSearch()).run(task)

    assert report.asset_type == "carousel"
    assert "LinkedIn carousel examples" in report.query
    assert len(report.references) == 1
    assert report.extracted_patterns[0].asset_type == "carousel"
    assert "teardown" in report.extracted_patterns[0].pattern.lower()
