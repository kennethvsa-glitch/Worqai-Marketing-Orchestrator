from scripts.taste_gate import inspect_html, validate_contract, validate_findings


def test_contract_requires_operational_fields() -> None:
    assert "missing field: concept" in validate_contract({"tone": ["direct"]})


def test_finding_is_bounded() -> None:
    errors = validate_findings([{"dimension": "vibes", "severity": "huge", "confidence": 2}])
    assert any("invalid dimension" in item for item in errors)
    assert any("confidence" in item for item in errors)


def test_html_inspection_flags_generic_defaults(tmp_path) -> None:
    page = tmp_path / "slide.html"
    page.write_text("<style>h1{font-family:Inter} .x{background:linear-gradient(90deg,purple,#fff)}</style>", encoding="utf-8")
    findings = inspect_html(page)
    assert {item["dimension"] for item in findings} >= {"brand_fit", "originality"}
