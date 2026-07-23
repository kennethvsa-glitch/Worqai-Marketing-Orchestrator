from pathlib import Path
from importlib.util import module_from_spec,spec_from_file_location
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=spec_from_file_location(name,path); module=module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(module); return module
def test_packet_requires_taste_roles_and_contracts():
    checker=load("check_packet",ROOT/".claude/skills/produce-motion-video/scripts/check_packet.py")
    errors=checker.validate({"brief":"x","dag":[{"id":"creative-spec","role":"creative-director","depends_on":[]}],"approval_gates":[]})
    assert any("taste-director" in item for item in errors); assert any("taste_policy" in item for item in errors)
def test_motion_contract_requires_temporal_language():
    gate=load("taste_gate",ROOT/".claude/skills/produce-motion-video/scripts/taste_gate.py")
    assert "missing field: motion_vocabulary" in gate.validate_contract({"tone":["direct"]})

def test_gate_hash_changes_with_artifact(tmp_path):
    approval=load("approve_gate",ROOT/".claude/skills/produce-motion-video/scripts/approve_gate.py")
    artifact=tmp_path/"concept.json"; artifact.write_text("{}",encoding="utf-8")
    first=approval.digest([artifact]); artifact.write_text('{"changed":true}',encoding="utf-8")
    assert approval.digest([artifact])!=first
