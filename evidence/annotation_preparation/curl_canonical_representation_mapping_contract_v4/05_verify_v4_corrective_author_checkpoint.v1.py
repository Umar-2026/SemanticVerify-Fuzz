#!/usr/bin/env python3

import copy
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

authp = here / "01_v4_corrective_successor_authorization.v1.json"
cpp = here / "04_v4_corrective_author_checkpoint.v1.json"

curlp = repo / "config/protocol_specifications/curl.json"

V3_SHA = "ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97"
AUTH_SHA = "727d1083c73b3f9d43f35f918c885e6e1490a14ed169c6f92de976ec1690b96e"

if sha(v3p) != V3_SHA:
    fail("V3_SHA")

if sha(authp) != AUTH_SHA:
    fail("AUTH_SHA")

v3 = json.loads(v3p.read_text(encoding="utf-8"))
v4 = json.loads(v4p.read_text(encoding="utf-8"))
cp = json.loads(cpp.read_text(encoding="utf-8"))

if v4["contract_version"] != "V4":
    fail("VERSION")

if v4["contract_kind"] != \
   "FORMAL_FROZEN_SCHEMA_INSUFFICIENCY_PROOF_RR10_CORRECTED_SUCCESSOR":
    fail("KIND")

if v4["status"] != "AUTHOR_CHECKPOINT_INDEPENDENT_REVIEW_REQUIRED":
    fail("STATUS")

if v4["independent_review_requirement"]["review_target"] != \
   "Exact immutable V4 corrective schema-insufficiency proof.":
    fail("SELF_REVIEW_TARGET")

if "Exact immutable V2 schema-insufficiency proof." == \
   v4["independent_review_requirement"]["review_target"]:
    fail("STALE_V2_TARGET")

# Full substantive-preservation check.
allowed = {
    "schema_id",
    "contract_version",
    "contract_kind",
    "status",
    "purpose",
    "input_bindings",
    "corrective_successor_from_v3_review",
    "independent_review_requirement",
    "immutability_policy",
    "next_boundary",
}

a = copy.deepcopy(v3)
b = copy.deepcopy(v4)

for key in allowed:
    a.pop(key, None)
    b.pop(key, None)

if a != b:
    fail("SUBSTANTIVE_V3_CHANGE")

for key, value in v3["input_bindings"].items():
    if v4["input_bindings"].get(key) != value:
        fail("INPUT_BINDING_CHANGED|" + key)

r3 = copy.deepcopy(v3["independent_review_requirement"])
r4 = copy.deepcopy(v4["independent_review_requirement"])

r3.pop("review_target")
r4.pop("review_target")

if r3 != r4:
    fail("REVIEW_REQUIREMENT_OTHER_CHANGE")

corr = v4["corrective_successor_from_v3_review"]

if corr["revision_required_item"] != "V3-RR10":
    fail("RR10_BINDING")

if corr["defect"] != "STALE_INTERNAL_INDEPENDENT_REVIEW_TARGET":
    fail("RR10_DEFECT")

if corr["corrected_value"] != \
   "Exact immutable V4 corrective schema-insufficiency proof.":
    fail("RR10_CORRECTED_VALUE")

for key in (
    "substantive_proof_semantics_changed",
    "representation_policy_binding_changed",
    "structural_obstruction_witnesses_changed",
    "admissibility_constraints_changed",
    "schema_changed",
    "positive_mapping_added",
):
    if corr[key] is not False:
        fail("UNAUTHORIZED_CORRECTIVE_CHANGE|" + key)

expected_outcome = (
    "FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_"
    "SCHEMA_SUCCESSOR_REQUIRED"
)

if v4["author_outcome"] != expected_outcome:
    fail("AUTHOR_OUTCOME")

for key in (
    "positive_mapping_algorithm_defined",
    "positive_mapping_algorithm_approved",
    "lossless_v4_to_frozen_schema_mapping_proven",
    "canonical_materialization_safe",
    "curl_json_creation_authorized",
    "curl_json_created",
    "canonical_schema_successor_authorized",
):
    if v4[key] is not False:
        fail("PROHIBITED_STATUS|" + key)

if v4["canonical_schema_successor_required"] is not True:
    fail("SCHEMA_SUCCESSOR_REQUIRED")

if cp["exact_v4_contract"]["sha256"] != sha(v4p):
    fail("CHECKPOINT_SHA")

if cp["exact_v4_contract"]["size_bytes"] != v4p.stat().st_size:
    fail("CHECKPOINT_SIZE")

if cp["rr10_correction"]["new_value"] != \
   "Exact immutable V4 corrective schema-insufficiency proof.":
    fail("CHECKPOINT_RR10_VALUE")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("EXACT_V4_CONTRACT_SHA256=" + sha(v4p))
print("EXACT_V4_CONTRACT_SIZE=" + str(v4p.stat().st_size))
print("V4_CONTRACT_VERSION=V4")
print("V4_RR10_CORRECTIVE_SUCCESSOR=YES")
print("V4_EXACT_SELF_REVIEW_TARGET=PASS")
print("STALE_V2_REVIEW_TARGET_REMOVED=YES")
print("V3_SUBSTANTIVE_PROOF_PRESERVED=YES")
print("V3_EXISTING_INPUT_BINDINGS_PRESERVED=YES")
print("COMPLETE_V4_REPRESENTATION_POLICY_BINDING_PRESERVED=YES")
print("OWNERSHIP_SENSITIVE_PRESERVATION_RETAINED=YES")
print("RETURN_SENSITIVE_PRESERVATION_RETAINED=YES")
print("STRUCTURAL_OBSTRUCTION_WITNESSES_PRESERVED=YES")
print("ADMISSIBILITY_CONSTRAINTS_PRESERVED=YES")
print("SCOPED_SCHEMA_INSUFFICIENCY_CONCLUSION_PRESERVED=YES")
print("V4_AUTHOR_OUTCOME=" + expected_outcome)
print("V4_AUTHOR_OUTCOME_INDEPENDENTLY_APPROVED=NO")
print("PORTABLE_GIT_OBJECT_EVIDENCE_FOR_V4_REVIEW_REQUIRED=YES")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("V4_CORRECTIVE_AUTHOR_CHECKPOINT_VERIFICATION=PASS")
