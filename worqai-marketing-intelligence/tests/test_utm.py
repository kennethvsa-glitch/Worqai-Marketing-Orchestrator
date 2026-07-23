import pytest

from worqai_marketing_intel.utm import asset_id_from_utm_content, build_utm_url


def test_asset_id_lands_in_utm_content():
    url = build_utm_url(
        "https://www.worqai.io/es/analizador-cv-ats",
        asset_id="abc123",
        source="linkedin",
        medium="social",
        campaign="ats-launch",
    )
    assert url.startswith("https://www.worqai.io/es/analizador-cv-ats?")
    assert "utm_content=abc123" in url
    assert "utm_source=linkedin" in url
    assert "utm_medium=social" in url
    assert "utm_campaign=ats-launch" in url


def test_variant_appends_but_asset_id_stays_recoverable():
    url = build_utm_url(
        "https://x.io/p",
        asset_id="abc123",
        source="ig",
        medium="social",
        campaign="c",
        variant="hookB",
    )
    assert "utm_content=abc123--hookB" in url
    assert asset_id_from_utm_content("abc123--hookB") == "abc123"
    assert asset_id_from_utm_content("abc123") == "abc123"


def test_preserves_existing_query_and_adds_term():
    url = build_utm_url(
        "https://x.io/p?ref=deck",
        asset_id="a1",
        source="s",
        medium="m",
        campaign="c",
        term="ats",
    )
    assert "ref=deck" in url
    assert "utm_term=ats" in url


def test_requires_absolute_url():
    with pytest.raises(ValueError):
        build_utm_url("/es/pricing", asset_id="a1", source="s", medium="m", campaign="c")


def test_requires_asset_id():
    with pytest.raises(ValueError):
        build_utm_url("https://x.io", asset_id="   ", source="s", medium="m", campaign="c")
