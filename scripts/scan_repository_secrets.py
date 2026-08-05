#!/usr/bin/env python3

import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = (
    ROOT
    / "evidence"
    / "gates"
    / "gate0"
    / "secret_scan.json"
)

PATTERNS = [
    (
        "aws_access_key",
        re.compile(
            rb"(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![A-Z0-9])"
        ),
    ),
    (
        "google_api_key",
        re.compile(
            rb"(?<![A-Za-z0-9_-])AIza[0-9A-Za-z_-]{30,}"
        ),
    ),
    (
        "generic_sk_key",
        re.compile(
            rb"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}"
        ),
    ),
    (
        "github_token",
        re.compile(
            rb"(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{20,}"
        ),
    ),
    (
        "slack_token",
        re.compile(
            rb"(?<![A-Za-z0-9_-])xox[baprs]-[A-Za-z0-9-]{20,}"
        ),
    ),
    (
        "huggingface_token",
        re.compile(
            rb"(?<![A-Za-z0-9_])hf_[A-Za-z0-9]{20,}"
        ),
    ),
    (
        "private_key_header",
        re.compile(
            rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
        ),
    ),
]

listed = subprocess.run(
    [
        "git",
        "-C",
        str(ROOT),
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
        "-z",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=False,
)

if listed.returncode != 0:
    print("STRICT_SECRET_SCAN=FAIL")
    print(listed.stderr.decode("utf-8", errors="replace"))
    raise SystemExit(1)

relative_paths = sorted(
    Path(item.decode("utf-8"))
    for item in listed.stdout.split(b"\0")
    if item
)

scanned = []
binary_skipped = []
findings = []

for relative in relative_paths:
    path = ROOT / relative

    if path == REPORT_PATH or not path.is_file():
        continue

    data = path.read_bytes()

    if b"\0" in data[:8192]:
        binary_skipped.append(relative.as_posix())
        continue

    file_digest = hashlib.sha256(data).hexdigest()

    scanned.append({
        "path": relative.as_posix(),
        "size_bytes": len(data),
        "sha256": file_digest,
    })

    for pattern_name, pattern in PATTERNS:
        matches = list(pattern.finditer(data))

        if matches:
            findings.append({
                "path": relative.as_posix(),
                "pattern": pattern_name,
                "match_count": len(matches),
            })

tree_material = "".join(
    f"{record['sha256']}  {record['path']}\n"
    for record in scanned
).encode("utf-8")

report = {
    "schema_version": "1.0.0",
    "gate": "Gate 0A-0B corrective audit",
    "scanned_at_utc": (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    ),
    "scanner": "Dependency-free fail-closed repository scanner",
    "scope": (
        "Git tracked files and untracked non-ignored files; "
        "the generated report itself is excluded"
    ),
    "status": "FAIL" if findings else "PASS",
    "candidate_files": len(relative_paths),
    "text_files_scanned": len(scanned),
    "binary_files_skipped": binary_skipped,
    "pattern_names": [
        pattern_name for pattern_name, _ in PATTERNS
    ],
    "findings": findings,
    "scanned_tree_sha256": hashlib.sha256(
        tree_material
    ).hexdigest(),
    "scanned_files": scanned,
}

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
REPORT_PATH.write_text(
    json.dumps(report, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

if findings:
    print("STRICT_SECRET_SCAN=FAIL")
    print(f"FINDING_GROUPS={len(findings)}")
    print(f"REPORT={REPORT_PATH}")
    raise SystemExit(1)

print("STRICT_SECRET_SCAN=PASS")
print(f"TEXT_FILES_SCANNED={len(scanned)}")
print(f"BINARY_FILES_SKIPPED={len(binary_skipped)}")
print(
    "SCANNED_TREE_SHA256="
    + report["scanned_tree_sha256"]
)
print(
    "REPORT_SHA256="
    + hashlib.sha256(REPORT_PATH.read_bytes()).hexdigest()
)
