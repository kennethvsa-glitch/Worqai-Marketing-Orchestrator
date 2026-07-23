import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent

sys.path.insert(0, str(ROOT / 'scripts'))
from make_film import validate_manifest


def _make_sounds_dir(base):
    d = base / 'Ideation' / 'Sound effects'
    d.mkdir(parents=True, exist_ok=True)
    return d


def _make_sounds_json(base, entries):
    p = base / 'sounds.json'
    p.write_text(json.dumps(entries), encoding='utf-8')
    return p


def test_all_required_present(tmp_path):
    scene = tmp_path / 'scene.html'
    scene.write_text('<html></html>', encoding='utf-8')

    sounds_dir = _make_sounds_dir(tmp_path)
    (sounds_dir / 'click-123.wav').write_bytes(b'')
    sounds_json = _make_sounds_json(tmp_path, [
        {"offset_ms": 0, "file": "click", "volume": 1.0}
    ])

    vo_audio = tmp_path / 'vo.mp3'
    vo_audio.write_bytes(b'')
    vo_script = tmp_path / 'vo_script.json'
    vo_script.write_text('[]', encoding='utf-8')

    music = tmp_path / 'music.mp3'
    music.write_bytes(b'')

    manifest = {
        "name": "test",
        "scene": "scene.html",
        "sounds": "sounds.json",
        "voiceover": {"audio": "vo.mp3", "script": "vo_script.json"},
        "music": {"file": "music.mp3"},
        "cutdowns": [{"name": "c1", "from_sec": 0, "to_sec": 5.0}],
        "captions": True,
    }

    result = validate_manifest(manifest, tmp_path)
    assert result["status"] == "ok"
    assert result["errors"] == []


def test_scene_missing(tmp_path):
    manifest = {
        "name": "test",
        "scene": "nonexistent.html",
    }
    result = validate_manifest(manifest, tmp_path)
    assert result["status"] == "error"
    assert any(e["asset"] == "scene" for e in result["errors"])


def test_sound_file_missing(tmp_path):
    scene = tmp_path / 'scene.html'
    scene.write_text('<html></html>', encoding='utf-8')

    sounds_dir = _make_sounds_dir(tmp_path)
    sounds_json = _make_sounds_json(tmp_path, [
        {"offset_ms": 0, "file": "missing_prefix", "volume": 1.0}
    ])

    manifest = {
        "name": "test",
        "scene": "scene.html",
        "sounds": "sounds.json",
    }
    result = validate_manifest(manifest, tmp_path)
    assert result["status"] == "error"
    assert any(
        e["asset"] == "sound_file" or "sound" in e["asset"].lower()
        for e in result["errors"]
    )


def test_voiceover_missing(tmp_path):
    scene = tmp_path / 'scene.html'
    scene.write_text('<html></html>', encoding='utf-8')

    manifest = {
        "name": "test",
        "scene": "scene.html",
        "voiceover": {"audio": "nonexistent.mp3", "script": "nonexistent.json"},
    }
    result = validate_manifest(manifest, tmp_path)
    assert result["status"] == "ok"
    assert result["errors"] == []
    assert len(result["warnings"]) > 0


def test_music_missing(tmp_path):
    scene = tmp_path / 'scene.html'
    scene.write_text('<html></html>', encoding='utf-8')

    manifest = {
        "name": "test",
        "scene": "scene.html",
        "music": {"file": "nonexistent.mp3"},
    }
    result = validate_manifest(manifest, tmp_path)
    assert result["status"] == "ok"
    assert result["errors"] == []
    assert len(result["warnings"]) > 0


def test_cli_ok(tmp_path):
    scene_rel = "templates/scenes/scene-launch-villain-v3.html"
    assert (ROOT / scene_rel).exists(), f"fixture scene not found: {scene_rel}"

    manifest = {"name": "test-film", "scene": scene_rel}
    manifest_path = tmp_path / "test.json"
    manifest_path.write_text(json.dumps(manifest), encoding='utf-8')

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "make_film.py"),
         "--film", str(manifest_path),
         "--validate-only"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"Expected 0, got {proc.returncode}: {proc.stdout} {proc.stderr}"
    data = json.loads(proc.stdout)
    assert "status" in data
    assert isinstance(data["errors"], list)
    assert isinstance(data["warnings"], list)
    assert data["status"] == "ok", f"Expected ok: {data}"


@pytest.mark.parametrize(
    ("filename", "contents"),
    [
        ("missing.json", None),
        ("malformed.json", "{not valid json"),
    ],
)
def test_cli_manifest_error_is_machine_readable(tmp_path, filename, contents):
    manifest_path = tmp_path / filename
    if contents is not None:
        manifest_path.write_text(contents, encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "make_film.py"),
            "--film",
            str(manifest_path),
            "--validate-only",
        ],
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["status"] == "error"
    assert data["errors"][0]["asset"] == "manifest"
    assert data["warnings"] == []
