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

authp = here / "01_v3_successor_authorization.v1.json"
v2p = repo / "config/annotation/curl_canonical_representation_mapping_contract.v2.json"
v4p = repo / "config/annotation/curl_technical_protocol_working_draft.v4.json"
schemap = repo / "config/schemas/protocol_specification.schema.json"
v3p = repo / "config/annotation/curl_canonical_representation_mapping_contract.v3.json"
curlp = repo / "config/protocol_specifications/curl.json"

if sha(v2p) != "f2badbc07895e8baff078a0ce617ceb6ff02d39c7634a9e38b3b8a46a18d811c":
    fail("V2_SHA")

if sha(v4p) != "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8":
    fail("V4_SHA")

if sha(schemap) != "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34":
    fail("SCHEMA_SHA")

a = json.loads(authp.read_text(encoding="utf-8"))

if a["status"] != "AUTHORIZED_FOR_V3_CORRECTIVE_AUTHORING_ONLY":
    fail("STATUS")

if a["completed_v2_human_review"]["overall_decision"] != "REVISION_REQUIRED":
    fail("V2_REVIEW_OUTCOME")

if a["completed_v2_human_review"]["revision_required_items"] != [
    "V2-RR01", "V2-RR08"
]:
    fail("REVIEW_ITEMS")

s = a["rr08_required_corrective_scope"]

for key in (
    "explicit_ownership_sensitive_semantics_preserved",
    "explicit_return_sensitive_semantics_preserved",
    "complete_exact_v4_representation_policy_must_be_bound",
    "complete_exact_v4_representation_policy_must_be_machine_checkably_accounted",
):
    if s[key] is not True:
        fail("RR08_SCOPE|" + key)

r = a["rr01_future_review_package_requirement"]

if r["portable_git_object_evidence_required"] is not True:
    fail("RR01_GIT_EVIDENCE")

if r["v2_human_rr01_decision_retroactively_changed"] is not False:
    fail("RR01_DECISION_MUTATION")

for key, value in a["semantic_non_authorizations"].items():
    if value is not False:
        fail("SEMANTIC_NONAUTH|" + key)

for key, value in a["downstream_non_authorizations"].items():
    if value is not False:
        fail("DOWNSTREAM_NONAUTH|" + key)

if a["independent_review_requirement"]["required"] is not True:
    fail("INDEPENDENT_REVIEW")

if a["independent_review_requirement"]["portable_git_evidence_required_in_review_handoff"] is not True:
    fail("GIT_EVIDENCE_REVIEW_HANDOFF")

if a["next_boundary"] != "AUTHOR_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V3":
    fail("NEXT_BOUNDARY")

if v3p.exists():
    fail("V3_ALREADY_AUTHORED")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("V2_REVISION_REQUIRED_BINDING=PASS")
print("V2_RR01_AND_RR08_BOUND=PASS")
print("V3_CORRECTIVE_AUTHORING_AUTHORIZED=YES")
print("OWNERSHIP_SENSITIVE_PRESERVATION_REQUIRED=YES")
print("RETURN_SENSITIVE_PRESERVATION_REQUIRED=YES")
print("COMPLETE_V4_REPRESENTATION_POLICY_BINDING_REQUIRED=YES")
print("PORTABLE_GIT_OBJECT_EVIDENCE_FOR_V3_REVIEW_REQUIRED=YES")
print("V2_RR01_HUMAN_DECISION_CHANGED=NO")
print("EXACT_V2_REMAINS_IMMUTABLE=YES")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CURL_JSON_MATERIALIZATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_MAPPING_CONTRACT_V3_SUCCESSOR_AUTHORIZATION=PASS")
