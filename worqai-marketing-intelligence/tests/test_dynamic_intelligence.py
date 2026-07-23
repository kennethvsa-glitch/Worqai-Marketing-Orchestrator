import json

from worqai_marketing_intel import MarketingOrchestrator
from worqai_marketing_intel.context_compiler import enrich_task
from worqai_marketing_intel.router import classify


def test_carousel_generation_changes_with_topic_and_audience():
    engine = MarketingOrchestrator()
    graduate = engine.brief(
        "Crea un carrusel de 7 slides sobre errores del CV para graduados en Costa Rica"
    )
    executive = engine.brief(
        "Create a 9 slide carousel about executive resume evidence for Mexico"
    )

    assert graduate.concept != executive.concept
    assert graduate.task.language == "es-LatAm"
    assert graduate.task.market == "Costa Rica"
    assert len(graduate.concept["slides"]) == 7
    assert "executive" in json.dumps(executive.concept).lower()


def test_reel_requested_count_is_respected():
    brief = MarketingOrchestrator().brief(
        "Give me 2 IG reel ideas about executive resumes for Mexico"
    )

    assert brief.task.asset_type.value == "ig_reel"
    assert len(brief.concept["concepts"]) == 2


def test_script_rewrite_preserves_subject_and_changes_with_source():
    engine = MarketingOrchestrator()
    linkedin = engine.audit_script(
        "Audita este guion para LinkedIn",
        "Mi perfil de LinkedIn no recibe visitas. Quiero enseñar tres cambios concretos en el titular.",
    )
    interview = engine.audit_script(
        "Audita este guion sobre entrevistas",
        "Me pongo nervioso en entrevistas. Quiero explicar una técnica simple para responder con calma.",
    )

    assert linkedin["rewritten_script"] != interview["rewritten_script"]
    assert "LinkedIn" in linkedin["rewritten_script"]
    assert "nerv" in interview["rewritten_script"].lower()


def test_preparation_packet_contains_real_intelligence_inputs():
    packet = MarketingOrchestrator().prepare(
        "Create a carousel about ATS myths for LatAm graduates"
    )

    assert packet.brand_context["voice"]
    assert "semantic specificity" in packet.brand_context["anti_generic_creative"].lower()
    assert packet.benchmark_patterns
    assert packet.agent_insights
    assert packet.requirements
    assert any(insight.recommendation for insight in packet.agent_insights)


def test_context_compiler_does_not_treat_cv_as_spanish_by_itself():
    task = enrich_task(classify("Make an SEO plan for CV analysis in Colombia"))

    assert task.language == "en"
    assert task.market == "Colombia"


def test_quality_judge_penalizes_topic_drift():
    engine = MarketingOrchestrator()
    task = enrich_task(classify("Create a carousel about executive resume evidence"))
    score = engine.taste.score_asset(
        "This generic campaign has a CTA and enough words to look complete, but it discusses coffee shops, menus, neighborhoods, and morning routines instead of the requested professional application subject.",
        asset_type=task.asset_type,
        task=task,
    )

    assert "The output does not visibly use the requested topic." in score.risks


def test_brief_does_not_score_claim_guardrails_as_generated_copy():
    brief = MarketingOrchestrator().brief(
        "Crea un carrusel para graduados de Costa Rica que buscan su primer empleo"
    )

    assert not any("all ats" in risk.lower() for risk in brief.quality.risks)
