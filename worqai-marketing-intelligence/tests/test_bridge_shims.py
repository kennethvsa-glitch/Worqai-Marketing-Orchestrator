from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SHIMS = [
    ROOT / ".claude" / "skills" / "worqai-marketing-intelligence" / "scripts" / "wmi_bridge.py",
    ROOT
    / "integrations"
    / "worqai-marketing-intelligence"
    / "skills"
    / "worqai-marketing-intelligence"
    / "scripts"
    / "wmi_bridge.py",
]


def test_root_bridge_holds_the_logic():
    root = ROOT / "scripts" / "wmi_bridge.py"
    text = root.read_text(encoding="utf-8")
    assert "def main()" in text
    assert "def validate_draft(" in text


def test_harness_bridges_stay_thin_shims():
    """The .claude and integrations bridges must delegate to the root bridge.

    If real logic is copy-pasted into either, it will drift. Keeping them as
    ``runpy`` shims of ``scripts/wmi_bridge.py`` is what keeps one source of truth.
    """

    for shim in SHIMS:
        text = shim.read_text(encoding="utf-8")
        assert "runpy.run_path" in text, f"{shim} should delegate, not copy logic"
        assert "wmi_bridge.py" in text
        assert len(text.splitlines()) < 20, f"{shim} looks like it grew real logic"
