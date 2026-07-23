import json
from pathlib import Path

import pytest

from worqai_marketing_intel.brand_memory import BrandMemory
from worqai_marketing_intel.models import AssetType, MarketingTask
from worqai_marketing_intel.validation import (
    BLOCK,
    JUDGE_RUBRIC,
    blocking_failures,
    build_judge_packet,
    evaluate_hard_gates,
)

FIXTURES = json.loads(
    (Path(__file__).parent / "fixtures" / "validation_cases.json").read_text(encoding="utf-8")
)


def _task(case: dict) -> MarketingTask:
    return MarketingTask(
        request=case["name"],
        asset_type=AssetType(case["asset_type"]),
        topic=case.get("topic", "resume tailoring"),
        language=case.get("language", "en"),
        source_text=case.get("source_text", ""),
    )


@pytest.mark.parametrize("case", FIXTURES, ids=[c["name"] for c in FIXTURES])
def test_golden_validation_cases(case):
    brand = BrandMemory()
    gates = evaluate_hard_gates(case["draft"], _task(case), brand)
    failed_ids = {gate.id for gate in blocking_failures(gates)}

    assert bool(failed_ids) == case["expect_blocked"], (case["name"], failed_ids)
    if case.get("expect_gate"):
        assert case["expect_gate"] in failed_ids, (case["name"], failed_ids)


def test_banned_phrase_blocks():
    brand = BrandMemory()
    banned = brand.banned_phrases()
    assert banned, "brand anti-slop list should not be empty"
    draft = f"This campaign will {banned[0]} for job seekers with a clear next step to try today."
    task = MarketingTask(request="x", asset_type=AssetType.CAMPAIGN, topic="resume")

    failed = {gate.id for gate in blocking_failures(evaluate_hard_gates(draft, task, brand))}
    assert "banned_phrases" in failed


def test_format_completeness_is_advisory_not_blocking():
    brand = BrandMemory()
    # A terse but clean reply with no reel structure keywords: format gate should
    # warn, never block.
    draft = "Sí, podés probarlo gratis y sin tarjeta. Subí tu CV y revisá la vacante."
    task = MarketingTask(
        request="reply", asset_type=AssetType.IG_REEL, topic="reply", language="es-LatAm"
    )

    gates = evaluate_hard_gates(draft, task, brand)
    format_gate = next(gate for gate in gates if gate.id == "format_completeness")
    assert format_gate.severity != BLOCK
    assert not blocking_failures(gates)


def test_judge_packet_structure():
    brand = BrandMemory()
    task = MarketingTask(request="x", asset_type=AssetType.CAROUSEL, topic="ATS myths")
    gates = evaluate_hard_gates("A short draft about ATS myths.", task, brand)
    packet = build_judge_packet("A short draft about ATS myths.", task, brand, gates)

    assert set(packet["rubric"]) == set(JUDGE_RUBRIC)
    assert packet["draft"]
    assert packet["brand_excerpts"]["voice"]
    assert packet["task"]["asset_type"] == "carousel"
    assert len(packet["hard_gates"]) == len(gates)


def test_no_numeric_taste_score_in_packet():
    # The judge packet must not smuggle a fabricated numeric taste score; scoring
    # is the operator's separate pass.
    brand = BrandMemory()
    task = MarketingTask(request="x", asset_type=AssetType.CAMPAIGN, topic="resume")
    packet = build_judge_packet("draft text", task, brand, ())
    assert "score" not in packet
