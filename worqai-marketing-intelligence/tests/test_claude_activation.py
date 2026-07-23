from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_claude_primary_activation_files_exist():
    assert (ROOT / "CLAUDE.md").is_file()
    assert (ROOT / ".claude/skills/worqai-marketing-intelligence/SKILL.md").is_file()
    assert (ROOT / ".claude/skills/worqai-marketing-intelligence/scripts/wmi_bridge.py").is_file()
    assert (ROOT / "scripts/wmi_bridge.py").is_file()


def test_claude_bridge_does_not_depend_on_codex_integration_path():
    bridge = (
        ROOT / ".claude/skills/worqai-marketing-intelligence/scripts/wmi_bridge.py"
    ).read_text(encoding="utf-8")

    assert "integrations" not in bridge
    assert 'ROOT / "scripts" / "wmi_bridge.py"' in bridge


def test_primary_docs_identify_claude_as_creative_operator():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    constitution = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")

    assert "Claude   = novel creative judgment and writing" in readme
    assert "Codex    = novel creative judgment and writing" not in readme
    assert "ordinary prompts" in constitution
