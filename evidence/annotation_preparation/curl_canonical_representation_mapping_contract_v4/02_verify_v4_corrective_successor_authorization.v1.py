#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

here = Path(__file__).resolve().parent
repo = here

while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

authp = here / "01_v4_corrective_successor_authorization.v1.json"

v3p = (
    repo /
    "config/annotation/"
    "curl_canonical_representation_mapping_contract.v3.json"
)

v4p = (
    repo /
    "config/annotation/"
    "curl_canonical_representation_mapping_contract.v4.json"
)

curlp = repo / "config/protocol_specifications/curl.json"

if sha(v3p) != \
   "ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97":
    fail("V3_SHA")

a = json.loads(authp.read_text(encoding="utf-8"))

if a["status"] != "AUTHORIZED_FOR_V4_RR10_CORRECTIVE_AUTHORING_ONLY":
    fail("STATUS")

r = a["completed_v3_human_review"]

if r["overall_decision"] != "REVISION_REQUIRED":
    fail("V3_REVIEW_OUTCOME")

if r["revision_required_items"] != ["V3-RR10"]:
    fail("V3_REVIEW_ITEMS")

if r["decision_counts"] != {
    "PASS": 9,
    "REVISION_REQUIRED": 1,
    "FAIL": 0
}:
    fail("V3_REVIEW_COUNTS")

if r["schema_insufficiency_conclusion_rejected"] is not False:
    fail("TECHNICAL_CONCLUSION")

c = a["required_rr10_correction"]

if c["predecessor_stale_value"] != \
   "Exact immutable V2 schema-insufficiency proof.":
    fail("STALE_VALUE")

if c["required_successor_value"] != \
   "Exact immutable V4 corrective schema-insufficiency proof.":
    fail("SUCCESSOR_VALUE")

if c["required_location"] != \
   "$.independent_review_requirement.review_target":
    fail("CORRECTION_LOCATION")

if c["require_unambiguous_self_target"] is not True:
    fail("SELF_TARGET")

for key, value in a["required_preservation"].items():
    if value is not True:
        fail("PRESERVATION|" + key)

for key, value in a["semantic_non_authorizations"].items():
    if value is not False:
        fail("SEMANTIC_NONAUTH|" + key)

for key, value in a["downstream_non_authorizations"].items():
    if value is not False:
        fail("DOWNSTREAM_NONAUTH|" + key)

future = a["future_v4_independent_review_requirement"]

for key in (
    "required",
    "must_verify_v3_rr10_correction",
    "must_verify_exact_v4_self_review_target",
    "must_verify_v3_semantic_preservation",
    "portable_git_object_evidence_required",
    "approval_must_not_be_synthetic",
    "approval_does_not_authorize_schema_successor",
):
    if future[key] is not True:
        fail("FUTURE_REVIEW|" + key)

if a["next_boundary"] != \
   "AUTHOR_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V4_CORRECTIVE_SUCCESSOR":
    fail("NEXT_BOUNDARY")

if v4p.exists():
    fail("V4_MAPPING_CONTRACT_ALREADY_AUTHORED")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("V3_HUMAN_REVIEW_REVISION_REQUIRED_BINDING=PASS")
print("V3_RR01_TO_V3_RR09_PASS_BINDING=PASS")
print("V3_RR10_REVISION_REQUIRED_BINDING=PASS")
print("V3_SCHEMA_INSUFFICIENCY_CONCLUSION_REJECTED=NO")
print("V4_CORRECTIVE_AUTHORING_AUTHORIZED=YES")
print("V4_REQUIRED_REVIEW_TARGET=Exact immutable V4 corrective schema-insufficiency proof.")
print("V3_SUBSTANTIVE_PROOF_PRESERVATION_REQUIRED=YES")
print("PORTABLE_GIT_OBJECT_EVIDENCE_FOR_V4_REVIEW_REQUIRED=YES")
print("EXACT_V3_REMAINS_IMMUTABLE=YES")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CURL_JSON_MATERIALIZATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_MAPPING_CONTRACT_V4_CORRECTIVE_SUCCESSOR_AUTHORIZATION=PASS")
