#!/usr/bin/env python3
"""Validate Motion art direction and bounded taste findings."""
from __future__ import annotations
import argparse, json
from pathlib import Path
CONTRACT={"audience","objective","tone","concept","typography","color_roles","composition","restraint","motion_vocabulary","pacing","continuity","prohibited_patterns"}
DIMENSIONS={"composition","hierarchy","typography","restraint","originality","brand_fit","storytelling","motion"}
def validate_contract(value:dict)->list[str]:
    errors=[f"missing field: {key}" for key in sorted(CONTRACT-value.keys())]
    for key in ("tone","composition","restraint","motion_vocabulary","pacing","continuity"):
        if not isinstance(value.get(key),list) or not value.get(key): errors.append(f"{key} must be a non-empty list")
    return errors
def validate_findings(values:list[dict])->list[str]:
    errors=[]; required={"id","artifact","timestamp","dimension","severity","evidence","direction","confidence","judgment"}
    for index,value in enumerate(values):
        for key in sorted(required-value.keys()): errors.append(f"finding[{index}] missing field: {key}")
        if value.get("dimension") not in DIMENSIONS: errors.append(f"finding[{index}] invalid dimension")
        if value.get("severity") not in {"minor","major","blocking"}: errors.append(f"finding[{index}] invalid severity")
        confidence=value.get("confidence")
        if not isinstance(confidence,(int,float)) or not 0<=confidence<=1: errors.append(f"finding[{index}] confidence must be between 0 and 1")
    return errors
def main()->int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("kind",choices=("contract","findings")); parser.add_argument("path",type=Path)
    args=parser.parse_args(); value=json.loads(args.path.read_text(encoding="utf-8")); errors=validate_contract(value) if args.kind=="contract" else validate_findings(value)
    print(json.dumps({"valid":not errors,"errors":errors},indent=2)); return 1 if errors else 0
if __name__=="__main__": raise SystemExit(main())
