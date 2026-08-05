#!/usr/bin/env python3

import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = (
    ROOT
    / "evidence"
    / "gates"
    / "gate0"
    / "gate0ab_checkpoint.json"
)

files = []

for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue

    relative = path.relative_to(ROOT)

    if ".git" in relative.parts:
        continue

    if "__pycache__" in relative.parts:
        continue

    if path == TARGET:
        continue

    files.append({
        "path": relative.as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()
    })

manifest = {
    "schema_version": "1.0.0",
    "checkpoint": "Gate 0A-0B",
    "status": "PASS",
    "gate_0_overall": "IN_PROGRESS",
    "created_at_utc": (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    ),
    "repository": {
        "logical_path": (
            "/openbayes/home/semanticverify-fuzz-research"
        ),
        "physical_path": str(ROOT)
    },
    "completed": [
        "Gate 0A repository bootstrap",
        "Gate 0B environment qualification"
    ],
    "pending": [
        "Gate 0C authoritative proposal provenance",
        "Gate 0D model/API qualification",
        "Final Gate 0 registration and freeze"
    ],
    "stage": "Stage A - verification",
    "repair_implementation_allowed": False,
    "files": files
}

TARGET.parent.mkdir(parents=True, exist_ok=True)
TARGET.write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8"
)

print("GATE0AB_CHECKPOINT_MANIFEST=CREATED")
print(f"FILES_RECORDED={len(files)}")
print(f"MANIFEST={TARGET}")
print(
    "MANIFEST_SHA256="
    + hashlib.sha256(TARGET.read_bytes()).hexdigest()
)
