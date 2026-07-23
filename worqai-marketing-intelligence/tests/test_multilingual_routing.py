import pytest

import worqai_marketing_intel.prompt_runtime as prompt_runtime
from worqai_marketing_intel import MarketingOrchestrator, run_prompt
from worqai_marketing_intel.memory_store import MemoryStore
from worqai_marketing_intel.models import AssetType
from worqai_marketing_intel.router import classify


@pytest.mark.parametrize(
    ("prompt", "expected"),
    (
        ("Crea un carrusel para una universidad", AssetType.CAROUSEL),
        ("Redacta un correo para candidatos", AssetType.EMAIL),
        ("Haz una propuesta para Universidad Latina", AssetType.PARTNERSHIP_PITCH),
        ("Escribe un guion para WorqAI", AssetType.IG_REEL),
        ("Crea un video para WorqAI", AssetType.MOTION_VIDEO),
        ("Haz un plan SEO para CV con IA", AssetType.SEO_PAGE),
    ),
)
def test_spanish_asset_phrases_route_to_primary_asset(prompt, expected):
    task = classify(prompt)

    assert task.asset_type == expected
    assert task.language == "es-LatAm"


def test_phrase_boundaries_do_not_match_ad_inside_universidad():
    task = classify("Contenido para una universidad")

    assert task.asset_type == AssetType.PARTNERSHIP_PITCH
    assert "ad" not in task.signals


def test_standalone_ad_token_still_routes_to_ad():
    assert classify("Make an ad for WorqAI").asset_type == AssetType.AD


def test_creation_asset_precedes_supporting_research_intent():
    task = classify("Create a carousel and research examples first")
    result = run_prompt("Create a carousel and research examples first")

    assert task.asset_type == AssetType.CAROUSEL
    assert task.research_requested is True
    assert result.mode == "brief"
    assert result.payload["task"]["asset_type"] == "carousel"
    assert result.payload["task"]["research_requested"] is True
    assert result.payload["research_enrichment"]["asset_type"] == "carousel"
    assert result.payload["research_enrichment"]["benchmark_patterns"]


def test_spanish_creation_asset_precedes_supporting_research_intent():
    result = run_prompt("Crea un carrusel e investiga ejemplos primero")

    assert result.mode == "brief"
    assert result.payload["task"]["asset_type"] == "carousel"
    assert result.payload["task"]["language"] == "es-LatAm"
    assert result.payload["task"]["research_requested"] is True


def test_research_only_request_keeps_research_mode_and_target_asset():
    result = run_prompt("Research successful examples for a WorqAI carousel about ATS resumes")

    assert result.mode == "research"
    assert result.payload["asset_type"] == "carousel"
    assert result.payload["benchmark_patterns"]


def test_resume_builder_topic_does_not_steal_campaign_route():
    result = run_prompt("Create a campaign about our AI resume builder")

    assert result.mode == "brief"
    assert result.payload["task"]["asset_type"] == "campaign"


def test_explicit_seo_campaign_uses_seo_route():
    result = run_prompt("Create an SEO campaign for our AI resume builder")

    assert result.mode == "seo_plan"


def test_universal_intake_executes_one_guarded_route_without_menu():
    class CountingOrchestrator(MarketingOrchestrator):
        def __init__(self):
            super().__init__()
            self.brief_calls = 0

        def brief(self, request):
            self.brief_calls += 1
            return super().brief(request)

    orchestrator = CountingOrchestrator()
    result = run_prompt("this feels weak what should we do", orchestrator=orchestrator)

    assert result.mode == "brief"
    assert orchestrator.brief_calls == 1
    assert result.payload["intake_decision"]["best_mode"] == "brief"
    assert result.payload["intake_decision"]["execution_policy"] == "execute_once_with_recursion_guard"
    assert "routing_options" not in result.payload["intake_decision"]


def test_fast_message_reply_is_preserved():
    result = run_prompt("Reply to this message: Es gratis o tengo que poner tarjeta?")

    assert result.mode == "message_reply"
    assert "full orchestrator" in result.notes[0]


def test_performance_update_returns_structured_preview_and_missing_fields():
    result = run_prompt("this carousel got 1,250 impressions, 42 saves and 8 signups")

    assert result.mode == "performance_update"
    assert result.payload["status"] == "preview"
    assert result.payload["asset_type"] == "carousel"
    assert result.payload["channel"] == "social"
    assert result.payload["missing_fields"] == ["asset_id"]
    assert [(item["name"], item["value"]) for item in result.payload["metrics"]] == [
        ("impressions", 1250.0),
        ("saves", 42.0),
        ("signups", 8.0),
    ]
    assert result.payload["saved"] is False


def test_performance_update_saves_once_context_is_complete(tmp_path, monkeypatch):
    store = MemoryStore(tmp_path / "performance.db")
    monkeypatch.setattr(prompt_runtime, "MemoryStore", lambda: store)

    result = prompt_runtime.run_prompt(
        "Asset ID: carousel-042. This carousel on LinkedIn got 1,250 impressions, 42 saves and 8 signups",
        save=True,
    )
    events = store.list_performance_events(asset_type="carousel", channel="social")

    assert result.mode == "performance_update"
    assert result.payload["status"] == "saved"
    assert result.payload["missing_fields"] == []
    assert len(result.payload["saved_event_ids"]) == 3
    assert [(event.metric_name, event.metric_value) for event in events] == [
        ("impressions", 1250.0),
        ("saves", 42.0),
        ("signups", 8.0),
    ]


def test_terse_performance_update_infers_prefixed_asset_id(tmp_path, monkeypatch):
    store = MemoryStore(tmp_path / "performance.db")
    monkeypatch.setattr(prompt_runtime, "MemoryStore", lambda: store)

    result = prompt_runtime.run_prompt(
        "carousel-043 on Instagram: 700 impressions and 5 signups",
        save=True,
    )

    assert result.mode == "performance_update"
    assert result.payload["asset_id"] == "carousel-043"
    assert result.payload["status"] == "saved"


def test_performance_update_does_not_save_when_context_is_incomplete(tmp_path, monkeypatch):
    store = MemoryStore(tmp_path / "performance.db")
    monkeypatch.setattr(prompt_runtime, "MemoryStore", lambda: store)

    result = prompt_runtime.run_prompt(
        "This carousel got 900 impressions and 6 signups",
        save=True,
    )

    assert result.payload["status"] == "not_saved_missing_fields"
    assert result.payload["missing_fields"] == ["asset_id"]
    assert store.list_performance_events() == []
