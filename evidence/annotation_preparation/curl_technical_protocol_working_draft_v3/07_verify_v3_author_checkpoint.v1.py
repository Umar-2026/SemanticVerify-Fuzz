#!/usr/bin/env python3

import hashlib
import json
import sys
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


here = Path(__file__).resolve().parent

repo = here
while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

if not (repo / ".git").exists():
    fail("REPOSITORY_ROOT_NOT_FOUND")


V2_SHA = (
    "63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31"
)

v2 = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v2.json"
)

v3 = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v3.json"
)

resolution = here / "04_v3_successor_author_resolution.v1.json"
trace = here / "05_v3_successor_rule_source_traceability.v1.json"
checkpoint = here / "06_v3_author_checkpoint.v1.json"

decision = (
    repo
    / "documentation/decisions/"
      "0033-curl-technical-working-draft-v3-author-checkpoint.md"
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if sha(v2) != V2_SHA:
    fail("V2_IMMUTABILITY")


cp = json.loads(
    checkpoint.read_text(encoding="utf-8")
)

v3_sha = cp["final_checkpoint_identity"]["sha256"]
v3_size = cp["final_checkpoint_identity"]["size_bytes"]

if sha(v3) != v3_sha:
    fail("V3_SHA")

if v3.stat().st_size != v3_size:
    fail("V3_SIZE")

if sha(resolution) != \
        cp["bound_author_artifacts"]["author_resolution"]["sha256"]:
    fail("AUTHOR_RESOLUTION_SHA")

if sha(trace) != \
        cp["bound_author_artifacts"]["rule_source_traceability"]["sha256"]:
    fail("TRACEABILITY_SHA")


d3 = json.loads(v3.read_text(encoding="utf-8"))

if d3["schema_id"] != \
        "curl.technical-protocol-working-draft.v3":
    fail("V3_SCHEMA")

if d3["status"] != \
        "SOURCE_ONLY_TECHNICAL_WORKING_DRAFT_V3_AUTHOR_CHECKPOINT":
    fail("V3_STATUS")

if d3["next_required_boundary"] != \
        "BUILD_INDEPENDENT_CURL_TECHNICAL_WORKING_DRAFT_V3_REVIEW_PACKAGE":
    fail("V3_NEXT_BOUNDARY")


if cp["implemented_corrections"] != [
    "V3-C01",
    "V3-C02",
    "V3-C03",
    "V3-C04",
    "V3-C05",
    "V3-C06",
    "V3-C07",
    "V3-C08",
]:
    fail("CORRECTION_SET")

if cp["preserved_v2_pass_review_items"] != [
    "V2-RR01",
    "V2-RR02",
    "V2-RR03",
    "V2-RR04",
    "V2-RR07",
    "V2-RR08",
    "V2-RR11",
]:
    fail("PRESERVED_PASS_SET")


trace_data = json.loads(
    trace.read_text(encoding="utf-8")
)

if trace_data["successor_binding"]["sha256"] != v3_sha:
    fail("TRACE_V3_BINDING")

if trace_data["evidence_class"] != "PREAPPROVED_SOURCE_ONLY":
    fail("TRACE_EVIDENCE_CLASS")

for k, v in trace_data["explicit_quarantine"].items():
    if v is not False:
        fail("PROHIBITED_EVIDENCE|" + k)


resolution_data = json.loads(
    resolution.read_text(encoding="utf-8")
)

if resolution_data["successor"]["sha256"] != v3_sha:
    fail("RESOLUTION_V3_BINDING")

if resolution_data["successor"]["status"] != \
        "SOURCE_ONLY_TECHNICAL_WORKING_DRAFT_V3_AUTHOR_CHECKPOINT":
    fail("RESOLUTION_STATUS")

if len(resolution_data["implemented_corrections"]) != 8:
    fail("RESOLUTION_CORRECTION_COUNT")


for k, v in cp["non_authorizations"].items():
    if v is not False:
        fail("NON_AUTHORIZATION_CHANGED|" + k)


if cp["next_boundary"] != \
        "BUILD_INDEPENDENT_CURL_TECHNICAL_WORKING_DRAFT_V3_REVIEW_PACKAGE":
    fail("CHECKPOINT_NEXT_BOUNDARY")


if not decision.is_file():
    fail("DECISION_0033_MISSING")

decision_text = decision.read_text(encoding="utf-8")

for marker in (
    v3_sha,
    V2_SHA,
    "SOURCE_ONLY_TECHNICAL_WORKING_DRAFT_V3_AUTHOR_CHECKPOINT",
    "PREAPPROVED_SOURCE_ONLY",
    "BUILD_INDEPENDENT_CURL_TECHNICAL_WORKING_DRAFT_V3_REVIEW_PACKAGE",
):
    if marker not in decision_text:
        fail("DECISION_BINDING|" + marker)


print("V2_IMMUTABILITY_SHA256=PASS")
print("FINAL_V3_CHECKPOINT_SHA256=PASS")
print("FINAL_V3_CHECKPOINT_SIZE=PASS")
print("V3_SCHEMA_ID=PASS")
print("V3_STATUS=AUTHOR_CHECKPOINT")
print("V3_C01_TO_V3_C08=PASS")
print("PRESERVED_V2_PASS_REVIEW_ITEMS=7_OF_7_PASS")
print("V3_SUCCESSOR_BOUND_TRACEABILITY=PASS")
print("PREAPPROVED_SOURCE_ONLY=PASS")
print("PROHIBITED_EVIDENCE_USED=NO")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_TECHNICAL_WORKING_DRAFT_V3_AUTHOR_CHECKPOINT_VERIFICATION=PASS")
