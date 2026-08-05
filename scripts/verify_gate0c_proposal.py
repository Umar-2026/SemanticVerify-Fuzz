#!/usr/bin/env python3

import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = (
    ROOT
    / "provenance"
    / "proposal"
    / "SemanticVerify-Fuzz_Verification-First_Staged-Repair_Proposal.docx"
)
REPORT = (
    ROOT
    / "evidence"
    / "gates"
    / "gate0"
    / "proposal_provenance.json"
)

EXPECTED_SHA256 = (
    "3abc92ee7ac0100a6b9ac148a2ad2a4ca"
    "71d187677cb84abf1545de29afb4a21"
)
EXPECTED_SIZE = 245766

def require(condition, reason):
    if not condition:
        print("GATE0C_PROPOSAL_PROVENANCE=FAIL")
        print(f"REASON={reason}")
        raise SystemExit(1)

require(PROPOSAL.is_file(), "authoritative proposal missing")
require(PROPOSAL.stat().st_size == EXPECTED_SIZE, "size mismatch")

actual_sha256 = hashlib.sha256(PROPOSAL.read_bytes()).hexdigest()
require(actual_sha256 == EXPECTED_SHA256, "SHA-256 mismatch")

with zipfile.ZipFile(PROPOSAL, "r") as archive:
    require(archive.testzip() is None, "DOCX ZIP integrity failure")

    members = set(archive.namelist())

    require(
        "[Content_Types].xml" in members,
        "DOCX content-types part missing"
    )
    require(
        "word/document.xml" in members,
        "DOCX main document part missing"
    )

    document_xml = archive.read("word/document.xml")

xml_root = ElementTree.fromstring(document_xml)

text_fragments = [
    node.text
    for node in xml_root.iter()
    if node.tag.endswith("}t") and node.text
]

document_text = " ".join(
    " ".join(text_fragments).split()
)

required_literal_markers = [
    "RESEARCH PROPOSAL",
    "SemanticVerify-Fuzz",
    "Resource-Centered Path-Sensitive Verification and Constrained Repair",
    "API-Protocol Violations in LLM-Generated Fuzz Drivers",
    "2 low-cost API models",
    "10 scenarios",
    "800",
    "zlib",
    "libpcap",
    "DeepSeek V4 Flash-0731",
    "Gemini 3.1 Flash-Lite",
    "Fresh-Start Research Boundary",
    "Gate V",
    "verification freeze",
    "no-backflow"
]

marker_results = {}

for marker in required_literal_markers:
    present = marker in document_text
    marker_results[marker] = present
    require(present, f"missing proposal marker: {marker}")

rq_results = {
    f"RQ{index}": bool(
        re.search(rf"\bRQ{index}\b", document_text)
    )
    for index in range(1, 6)
}

contribution_results = {
    f"C{index}": bool(
        re.search(rf"\bC{index}\b", document_text)
    )
    for index in range(1, 5)
}

require(all(rq_results.values()), "RQ1-RQ5 incomplete")
require(
    all(contribution_results.values()),
    "C1-C4 incomplete"
)

library_results = {
    library: library in document_text
    for library in [
        "zlib",
        "libpcap",
        "curl",
        "cJSON",
        "libtiff",
        "libvpx",
        "c-ares",
        "lcms"
    ]
}

require(
    all(library_results.values()),
    "eight-library lock incomplete"
)

secret_patterns = {
    "aws_access_key": rb"AKIA[0-9A-Z]{16}",
    "generic_sk_key": rb"sk-[A-Za-z0-9_-]{20,}",
    "github_token": rb"gh[pousr]_[A-Za-z0-9]{20,}",
    "private_key": (
        rb"-----BEGIN (?:RSA |EC |OPENSSH )?"
        rb"PRIVATE KEY-----"
    )
}

secret_scan = {
    name: bool(re.search(pattern, document_xml))
    for name, pattern in secret_patterns.items()
}

require(
    not any(secret_scan.values()),
    "secret-like material detected in proposal XML"
)

require(REPORT.is_file(), "frozen proposal provenance report missing")

try:
    frozen_report = json.loads(
        REPORT.read_text(encoding="utf-8")
    )
except (OSError, json.JSONDecodeError) as error:
    require(
        False,
        f"frozen proposal provenance report unreadable: {error}"
    )

frozen_timestamp = frozen_report.get("verified_at_utc")

require(
    isinstance(frozen_timestamp, str)
    and bool(
        re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T"
            r"\d{2}:\d{2}:\d{2}\+00:00",
            frozen_timestamp
        )
    ),
    "frozen verified_at_utc is invalid"
)

report = {
    "schema_version": "1.0.0",
    "gate": "Gate 0C",
    "status": "PASS",
    "verified_at_utc": frozen_timestamp,
    "authority": "AUTHORITATIVE",
    "chat_attachment_filename": (
        "SemanticVerify-Fuzz_Verification-First_"
        "Staged-Repair_Proposal(1).docx"
    ),
    "canonical_repository_filename": PROPOSAL.name,
    "canonical_repository_path": (
        PROPOSAL.relative_to(ROOT).as_posix()
    ),
    "logical_repository_path": (
        "/openbayes/home/semanticverify-fuzz-research"
    ),
    "physical_repository_path": str(ROOT),
    "size_bytes": PROPOSAL.stat().st_size,
    "sha256": actual_sha256,
    "chat_attachment_hash_match": True,
    "docx_zip_integrity": "PASS",
    "main_document_part": "PASS",
    "required_markers": marker_results,
    "research_questions": rq_results,
    "contributions": contribution_results,
    "libraries": library_results,
    "extracted_xml_secret_scan": {
        key: "PASS" if not value else "FAIL"
        for key, value in secret_scan.items()
    },
    "stage_order": {
        "stage_a": "verification",
        "gate_v": "verification freeze",
        "stage_b": "constrained repair"
    },
    "repair_implementation_allowed": False
}

require(
    frozen_report == report,
    "frozen proposal provenance report content mismatch"
)

report_sha256 = hashlib.sha256(REPORT.read_bytes()).hexdigest()
lock_path = ROOT / "config" / "research_lock.json"

require(lock_path.is_file(), "research lock missing")

try:
    research_lock = json.loads(
        lock_path.read_text(encoding="utf-8")
    )
except (OSError, json.JSONDecodeError) as error:
    require(False, f"research lock unreadable: {error}")

pinned_report_sha256 = (
    research_lock
    .get("proposal_provenance", {})
    .get("report_sha256")
)

require(
    pinned_report_sha256 == report_sha256,
    "frozen proposal report SHA-256 differs from research lock"
)

print("GATE0C_PROPOSAL_PROVENANCE=PASS")
print("DOCX_ZIP_INTEGRITY=PASS")
print("CHAT_ATTACHMENT_HASH_MATCH=PASS")
print("RESEARCH_QUESTIONS=5")
print("CONTRIBUTIONS=4")
print("LIBRARIES=8")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print("FROZEN_REPORT_MUTATION=NO")
print(f"PROPOSAL_SHA256={actual_sha256}")
print(
    "REPORT_SHA256="
    + report_sha256
)
