#!/usr/bin/env python3
"""Bind Motion production approvals to exact artifact bytes."""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def digest(paths:list[Path])->str:
    value=hashlib.sha256()
    for path in paths:
        resolved=path.resolve()
        if not resolved.is_file(): raise ValueError(f"artifact does not exist: {resolved}")
        value.update(resolved.name.encode()); value.update(b"\0"); value.update(resolved.read_bytes())
    return value.hexdigest()
def main()->int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("packet",type=Path); parser.add_argument("gate"); parser.add_argument("artifacts",nargs="+",type=Path); parser.add_argument("--by",default="human"); parser.add_argument("--verify",action="store_true")
    args=parser.parse_args(); packet=json.loads(args.packet.read_text(encoding="utf-8"))
    if args.gate not in packet.get("approval_gates",[]): raise SystemExit(f"unknown approval gate: {args.gate}")
    current=digest(args.artifacts); approval_path=args.packet.parent/"approvals.json"
    approvals=json.loads(approval_path.read_text(encoding="utf-8")) if approval_path.is_file() else {}
    if args.verify:
        valid=approvals.get(args.gate,{}).get("hash")==current
        print(json.dumps({"gate":args.gate,"valid":valid,"hash":current},indent=2)); return 0 if valid else 1
    approvals[args.gate]={"hash":current,"artifacts":[str(path.resolve()) for path in args.artifacts],"approved_by":args.by,"approved_at":datetime.now(timezone.utc).isoformat()}
    approval_path.write_text(json.dumps(approvals,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(approvals[args.gate],indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
