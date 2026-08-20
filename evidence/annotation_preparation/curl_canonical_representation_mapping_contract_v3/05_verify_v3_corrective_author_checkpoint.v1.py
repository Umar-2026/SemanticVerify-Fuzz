#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def csha(x):
    return hashlib.sha256(
        json.dumps(
            x,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

here = Path(__file__).resolve().parent
repo = here
while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

v2p = repo / "config/annotation/curl_canonical_representation_mapping_contract.v2.json"
v3p = repo / "config/annotation/curl_canonical_representation_mapping_contract.v3.json"
v4p = repo / "config/annotation/curl_technical_protocol_working_draft.v4.json"
authp = here / "01_v3_successor_authorization.v1.json"
checkpointp = here / "04_v3_corrective_author_checkpoint.v1.json"
curlp = repo / "config/protocol_specifications/curl.json"

if sha(v2p) != "f2badbc07895e8baff078a0ce617ceb6ff02d39c7634a9e38b3b8a46a18d811c":
    fail("V2_SHA")

if sha(v4p) != "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8":
    fail("V4_SHA")

if sha(authp) != "66e4dd845f2919c161b00972a993a2a0f5e6a1dbf4a2726ee5c7ff2985f85d60":
    fail("AUTH_SHA")

v2 = json.loads(v2p.read_text(encoding="utf-8"))
v3 = json.loads(v3p.read_text(encoding="utf-8"))
v4 = json.loads(v4p.read_text(encoding="utf-8"))
cp = json.loads(checkpointp.read_text(encoding="utf-8"))

if v3["contract_version"] != "V3":
    fail("VERSION")

if v3["contract_kind"] != \
        "FORMAL_FROZEN_SCHEMA_INSUFFICIENCY_PROOF_CORRECTED_SUCCESSOR":
    fail("KIND")

if v3["status"] != "AUTHOR_CHECKPOINT_INDEPENDENT_REVIEW_REQUIRED":
    fail("STATUS")

expected_outcome = (
    "FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_"
    "SCHEMA_SUCCESSOR_REQUIRED"
)

if v3["author_outcome"] != expected_outcome:
    fail("OUTCOME")

# V2 proof sections that must remain semantically identical.
for key in (
    "approved_v4_semantic_container_hashes",
    "frozen_inventory",
    "frozen_schema_structural_facts",
    "structural_obstruction_witnesses",
):
    if v3[key] != v2[key]:
        fail("V2_PROOF_SECTION_CHANGED|" + key)

for key in (
    "admissibility_constraints",
    "candidate_carrier_classes_considered",
    "proof_conclusion",
):
    if v3["formal_insufficiency_argument"][key] != \
            v2["formal_insufficiency_argument"][key]:
        fail("V2_FORMAL_PROOF_SECTION_CHANGED|" + key)

rp = v4["representation_policy"]
binding = v3["approved_v4_representation_policy_binding"]

if binding["exact_value"] != rp:
    fail("REPRESENTATION_POLICY_EXACT_VALUE")

if binding["field_count"] != len(rp):
    fail("REPRESENTATION_POLICY_FIELD_COUNT")

if binding["canonical_semantic_sha256"] != csha(rp):
    fail("REPRESENTATION_POLICY_HASH")

account = {
    x["field"]: x
    for x in binding["field_accounting"]
}

if set(account) != set(rp):
    fail("REPRESENTATION_POLICY_ACCOUNTING_KEYS")

for key, value in rp.items():
    row = account[key]

    if row["exact_value"] != value:
        fail("REPRESENTATION_POLICY_VALUE|" + key)

    if row["preservation_required"] is not True:
        fail("REPRESENTATION_POLICY_PRESERVATION|" + key)

    if row["accounting_status"] != "EXPLICITLY_BOUND":
        fail("REPRESENTATION_POLICY_ACCOUNTING|" + key)

loss = v3["formal_insufficiency_argument"][
    "required_losslessness_contract"
]

required_true = (
    "all_10_v4_semantic_containers_preserved",
    "all_64_rule_records_accounted_for",
    "all_3_exit_obligations_accounted_for",
    "four_verdict_contract_preserved",
    "unknown_first_class_preserved",
    "membership_sensitive_semantics_preserved",
    "path_sensitive_semantics_preserved",
    "set_valued_state_reasoning_preserved",
    "forward_accounting_required",
    "reverse_accounting_required",
    "ownership_sensitive_semantics_preserved",
    "return_sensitive_semantics_preserved",
    "resource_centered_semantics_preserved",
    "normative_strength_uncertainty_policy_preserved",
    "synthetic_protocol_events_invented_false_policy_preserved",
    "complete_exact_v4_representation_policy_preserved",
    "complete_exact_v4_representation_policy_machine_checkably_bound",
)

for key in required_true:
    if loss.get(key) is not True:
        fail("LOSSLESSNESS_BOUNDARY|" + key)

corr = v3["corrective_successor_from_v2_review"]

if corr["review_outcome"] != "REVISION_REQUIRED":
    fail("PREDECESSOR_REVIEW_OUTCOME")

if corr["revision_required_items"] != ["V2-RR01", "V2-RR08"]:
    fail("PREDECESSOR_REVIEW_ITEMS")

if corr["rr08_corrections"][
    "ownership_sensitive_semantics_added_to_formal_losslessness_contract"
] is not True:
    fail("RR08_OWNERSHIP")

if corr["rr08_corrections"][
    "return_sensitive_semantics_added_to_formal_losslessness_contract"
] is not True:
    fail("RR08_RETURN")

if corr["rr08_corrections"][
    "complete_exact_v4_representation_policy_bound"
] is not True:
    fail("RR08_POLICY_BINDING")

if corr["rr01_resolution_for_future_review_package"][
    "portable_git_object_evidence_required"
] is not True:
    fail("RR01_GIT_EVIDENCE")

if corr["rr01_resolution_for_future_review_package"][
    "v2_human_decision_retroactively_changed"
] is not False:
    fail("RR01_DECISION_MUTATION")

for key in (
    "positive_mapping_algorithm_defined",
    "positive_mapping_algorithm_approved",
    "lossless_v4_to_frozen_schema_mapping_proven",
    "canonical_materialization_safe",
    "curl_json_creation_authorized",
    "curl_json_created",
    "canonical_schema_successor_authorized",
):
    if v3[key] is not False:
        fail("PROHIBITED_POSITIVE_STATUS|" + key)

if v3["canonical_schema_successor_required"] is not True:
    fail("SCHEMA_SUCCESSOR_REQUIRED")

if cp["exact_v3_contract"]["sha256"] != sha(v3p):
    fail("CHECKPOINT_V3_SHA")

if cp["exact_v3_contract"]["size_bytes"] != v3p.stat().st_size:
    fail("CHECKPOINT_V3_SIZE")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("EXACT_V3_CONTRACT_SHA256=" + sha(v3p))
print("EXACT_V3_CONTRACT_SIZE=" + str(v3p.stat().st_size))
print("V3_CONTRACT_KIND=FORMAL_FROZEN_SCHEMA_INSUFFICIENCY_PROOF_CORRECTED_SUCCESSOR")
print("V2_VALID_PROOF_SECTIONS_PRESERVED=YES")
print("V4_REPRESENTATION_POLICY_FIELD_COUNT=" + str(len(rp)))
print("V4_REPRESENTATION_POLICY_CANONICAL_SHA256=" + csha(rp))
print("COMPLETE_V4_REPRESENTATION_POLICY_BOUND=YES")
print("COMPLETE_V4_REPRESENTATION_POLICY_MACHINE_CHECKED=YES")
print("OWNERSHIP_SENSITIVE_PRESERVATION_EXPLICIT=YES")
print("RETURN_SENSITIVE_PRESERVATION_EXPLICIT=YES")
print("MEMBERSHIP_SENSITIVE_PRESERVATION_RETAINED=YES")
print("PATH_SENSITIVE_PRESERVATION_RETAINED=YES")
print("SET_VALUED_REASONING_PRESERVATION_RETAINED=YES")
print("FIRST_CLASS_UNKNOWN_PRESERVATION_RETAINED=YES")
print("FOUR_VERDICT_CONTRACT_PRESERVATION_RETAINED=YES")
print("FORWARD_REVERSE_ACCOUNTING_RETAINED=YES")
print("RR08_CORRECTION=PASS")
print("PORTABLE_GIT_OBJECT_EVIDENCE_FOR_V3_REVIEW_REQUIRED=YES")
print("V2_RR01_HUMAN_DECISION_CHANGED=NO")
print("V3_AUTHOR_OUTCOME=" + expected_outcome)
print("V3_AUTHOR_OUTCOME_INDEPENDENTLY_APPROVED=NO")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("V3_CORRECTIVE_AUTHOR_CHECKPOINT_VERIFICATION=PASS")
