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

authp = here / "01_schema_v2_successor_authoring_authorization.v1.json"

v1p = repo / "config/schemas/protocol_specification.schema.json"
v2p = repo / "config/schemas/protocol_specification.v2.schema.json"

v4p = (
    repo /
    "config/annotation/"
    "curl_canonical_representation_mapping_contract.v4.json"
)

reviewp = (
    repo /
    "evidence/annotation_preparation/"
    "curl_canonical_representation_mapping_contract_v4/"
    "completed_human_review_v1/"
    "02_completed_v4_human_review_record.v1.json"
)

pathmap = (
    repo /
    "config/annotation/"
    "canonical_protocol_specification_paths.v1.json"
)

hashcontract = (
    repo /
    "config/protocol_content_hash_canonicalization.v1.json"
)

curlp = repo / "config/protocol_specifications/curl.json"

if sha(v1p) != \
   "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34":
    fail("V1_SCHEMA_SHA")

if sha(v4p) != \
   "9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070":
    fail("V4_SHA")

if sha(reviewp) != \
   "292a4a569139d4b09dc341579ab25bfdba0db60e44d7b42da36cf2ab0740e53d":
    fail("V4_REVIEW_RECORD_SHA")

if sha(pathmap) != \
   "4c6471d51627997f58b6c6bca833d364edc4c51e5aa7b80d0c34be8d63d19aaa":
    fail("PATH_MAP_SHA")

if sha(hashcontract) != \
   "5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f":
    fail("HASH_CONTRACT_SHA")

a = json.loads(authp.read_text(encoding="utf-8"))
r = json.loads(reviewp.read_text(encoding="utf-8"))

if a["status"] != \
   "AUTHORIZED_FOR_SCHEMA_V2_SUCCESSOR_AUTHORING_ONLY":
    fail("STATUS")

if a["authorized_schema_v2_candidate"]["path"] != \
   "config/schemas/protocol_specification.v2.schema.json":
    fail("V2_PATH")

if a["authorized_schema_v2_candidate"][
    "protocol_specification_schema_version"
] != "2.0.0":
    fail("V2_VERSION")

if a["authorized_schema_v2_candidate"]["authoring_authorized"] is not True:
    fail("V2_AUTHORING")

if a["authorized_schema_v2_candidate"]["activation_authorized"] is not False:
    fail("V2_ACTIVATION")

if a["frozen_v1_schema_binding"]["immutable"] is not True:
    fail("V1_IMMUTABILITY")

if a["frozen_v1_schema_binding"][
    "in_place_modification_authorized"
] is not False:
    fail("V1_MODIFICATION")

if r["technical_interpretation"]["exact_v4_approved"] is not True:
    fail("V4_APPROVAL")

if r["technical_interpretation"][
    "canonical_schema_successor_technically_required"
] is not True:
    fail("SCHEMA_SUCCESSOR_NEED")

required_caps = a["design_scope"][
    "required_first_class_structural_capabilities"
]

for key, value in required_caps.items():
    if key == "machine_verdict_vocabulary":
        if value != [
            "VALID",
            "VIOLATION-MUST",
            "VIOLATION-MAY",
            "UNKNOWN"
        ]:
            fail("VERDICT_VOCABULARY")
    elif value is not True:
        fail("REQUIRED_CAPABILITY|" + key)

coverage = a["design_scope"]["required_curl_v4_coverage"]

for key, value in coverage.items():
    if value is not True:
        fail("COVERAGE|" + key)

if a["decision_0019_boundary"][
    "decision_0019_superseded_by_this_authorization"
] is not False:
    fail("DECISION_0019_SUPERSESSION")

if a["decision_0019_boundary"][
    "future_activation_requires_separate_decision_0019_successor_or_amendment"
] is not True:
    fail("DECISION_0019_FUTURE_ACTION")

if a["hash_contract_boundary"][
    "current_contract_modification_authorized"
] is not False:
    fail("HASH_CONTRACT_MODIFICATION")

for key, value in a["explicit_non_authorizations"].items():
    if value is not False:
        fail("NON_AUTHORIZATION|" + key)

for key, value in a["evidence_quarantine"].items():
    if value is not False:
        fail("QUARANTINE|" + key)

if a["next_boundary"] != \
   "AUTHOR_PROTOCOL_SPECIFICATION_SCHEMA_V2_SUCCESSOR_CANDIDATE":
    fail("NEXT_BOUNDARY")

if v2p.exists():
    fail("SCHEMA_V2_ALREADY_AUTHORED")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("APPROVED_V4_SCHEMA_INSUFFICIENCY_BINDING=PASS")
print("FROZEN_SCHEMA_V1_IMMUTABLE=YES")
print("SCHEMA_V2_RESERVED_PATH=config/schemas/protocol_specification.v2.schema.json")
print("SCHEMA_V2_RESERVED_PROTOCOL_VERSION=2.0.0")
print("SCHEMA_V2_SUCCESSOR_AUTHORING_AUTHORIZED=YES")
print("SCHEMA_V2_ACTIVATION_AUTHORIZED=NO")
print("DECISION_0019_SUPERSEDED=NO")
print("HASH_CONTRACT_MODIFICATION_AUTHORIZED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_MATERIALIZATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("PROTOCOL_SPECIFICATION_SCHEMA_V2_AUTHORING_AUTHORIZATION=PASS")
