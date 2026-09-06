#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

repo = Path(
    os.environ.get(
        "SVF_REPO_ROOT",
        "/openbayes/home/semanticverify-fuzz-research",
    )
)

pkg = Path(__file__).resolve().parent
record_path = pkg / "01_carrier_admissibility_evidence_closure_design.v1.json"

D0240_COMMIT = "023419fc8a69bfc8595750146a4918ce0f6c4b69"
D0240_TREE = "f686cd20b4fe057a604ae6ae62fcad4126f82580"
D0240_MANIFEST_SHA = "f29b9954396222cb17717dd19ced7211794dfc1242ed6bd5042845adf0c7bcb5"

def die(msg):
    print("D0241_CARRIER_ADMISSIBILITY_EVIDENCE_CLOSURE_DESIGN_VERIFIER=FAIL")
    print("FAIL_REASON=" + msg)
    sys.exit(1)

try:
    raw = record_path.read_bytes()

    dup = []

    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                dup.append(k)
            d[k] = v
        return d

    r = json.loads(raw.decode("utf-8"), object_pairs_hook=hook)

    if dup:
        die("DUPLICATE_JSON_OBJECT_KEYS")

    canonical = json.dumps(
        r,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    if raw != canonical:
        die("RECORD_NOT_GENERIC_CANONICAL_JSON")

    if raw.endswith(b"\n"):
        die("RECORD_HAS_FINAL_LF")

    if r["artifact_id"] != "SVF-D0241-CARRIER-ADMISSIBILITY-EVIDENCE-CLOSURE-DESIGN-V1":
        die("ARTIFACT_ID")

    if r["decision"] != "D0241":
        die("DECISION")

    if r["status"] != "DESIGN_ONLY_NO_EVIDENCE_EXECUTION_NO_B2_AUTHORIZATION":
        die("STATUS")

    p = r["predecessor"]

    if p["commit"] != D0240_COMMIT:
        die("D0240_COMMIT_BINDING")

    if p["tree"] != D0240_TREE:
        die("D0240_TREE_BINDING")

    if p["manifest_sha256"] != D0240_MANIFEST_SHA:
        die("D0240_MANIFEST_BINDING")

    if p["verified_frozen"] is not True:
        die("D0240_VERIFIED_FROZEN_BINDING")

    actual_tree = subprocess.check_output(
        ["git", "rev-parse", f"{D0240_COMMIT}^{{tree}}"],
        cwd=repo,
        text=True,
    ).strip()

    if actual_tree != D0240_TREE:
        die("D0240_TREE_RECOMPUTATION")

    s = r["current_governed_state"]

    expected = {
        "authoritative_candidate_reference_count": 171,
        "historical_supported_binding_pair_count": 211,
        "historical_unresolved_binding_pair_count": 1642,
        "historical_not_supported_binding_pair_count": 0,
        "req06_req14_pair_count": 218,
        "req06_req14_pairs_currently_unresolved": 218,
        "requirement_bound_carrier_admissibility_unresolved_requirement_count": 17,
    }

    for k, v in expected.items():
        if s[k] != v:
            die("CURRENT_STATE_" + k)

    if s["requirement_bound_carrier_admissibility_global_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
        die("RBCA_GLOBAL_OUTCOME")

    if s["requirement_bound_carrier_admissibility_resolved"] is not False:
        die("RBCA_RESOLVED")

    if s["zero_unresolved_carrier_admissibility_closure_established"] is not False:
        die("ZERO_UNRESOLVED_CLOSURE")

    sem = r["semantic_separation"]

    if any(v is not False for v in sem.values()):
        die("SEMANTIC_SEPARATION")

    reuse = r["existing_governed_evidence_reuse_design"]

    if reuse["reuse_is_authorized_by_d0241"] is not False:
        die("REUSE_AUTHORIZATION")

    if len(reuse["eligible_categories_for_future_explicit_binding"]) != 6:
        die("REUSE_CATEGORY_COUNT")

    add = r["additional_evidence_design"]

    if add["acquisition_authorized_by_d0241"] is not False:
        die("ADDITIONAL_EVIDENCE_AUTHORIZATION")

    if add["future_authorization_required"] is not True:
        die("FUTURE_AUTHORIZATION_REQUIRED")

    closure = r["future_closure_output_design"]

    if closure["created_by_d0241"] is not False:
        die("CLOSURE_CREATED")

    if closure["candidate_universe_size"] != 171:
        die("CANDIDATE_UNIVERSE_SIZE")

    if closure["intermediate_states_are_AEA02_dispositions"] is not False:
        die("INTERMEDIATE_AEA02_DISPOSITION")

    if closure["intermediate_states_create_C_domain_membership"] is not False:
        die("INTERMEDIATE_C_MEMBERSHIP")

    if closure["closure_acceptance_evaluated_by_d0241"] is not False:
        die("CLOSURE_ACCEPTANCE_EVALUATED")

    if closure["closure_established_by_d0241"] is not False:
        die("CLOSURE_ESTABLISHED")

    ladder = r["future_authorization_ladder"]

    if [x["phase"] for x in ladder] != ["C1", "C2", "C3", "C4", "C5", "C6"]:
        die("LADDER_PHASES")

    if any(x["authorized_by_d0241"] is not False for x in ladder):
        die("LADDER_AUTHORIZATION")

    if any(v is not False for v in r["explicit_nonauthorization"].values()):
        die("EXPLICIT_NONAUTHORIZATION")

    if any(v is not False for v in r["substantive_results_established"].values()):
        die("SUBSTANTIVE_RESULTS")

    if r["next_governance_requirement"] != \
        "SEPARATELY_AUTHORIZE_C1_EXACT_EXISTING_EVIDENCE_INVENTORY_AND_BINDING_BEFORE_ANY_EVIDENCE_ACQUISITION_OR_B2_AUTHORIZATION":
        die("NEXT_GOVERNANCE_REQUIREMENT")

except Exception as exc:
    die(type(exc).__name__ + ":" + str(exc))

print("D0241_CARRIER_ADMISSIBILITY_EVIDENCE_CLOSURE_DESIGN_VERIFIER=PASS")
print("D0240_PREDECESSOR_BINDING=PASS")
print("CURRENT_CARRIER_CANDIDATE_COUNT=171")
print("CURRENT_SUPPORTED_BINDING_PAIR_COUNT=211")
print("CURRENT_UNRESOLVED_BINDING_PAIR_COUNT=1642")
print("CURRENT_NOT_SUPPORTED_BINDING_PAIR_COUNT=0")
print("CURRENT_REQ06_REQ14_UNRESOLVED_PAIR_COUNT=218")
print("CURRENT_RBCA_UNRESOLVED_REQUIREMENT_COUNT=17")
print("ZERO_UNRESOLVED_CARRIER_ADMISSIBILITY_CLOSURE_ESTABLISHED=NO")
print("EXISTING_EVIDENCE_REUSE_AUTHORIZED=NO")
print("ADDITIONAL_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("CANDIDATE_ADMISSIBILITY_EVALUATION_AUTHORIZED=NO")
print("CANDIDATE_DISPOSITION_CREATION_AUTHORIZED=NO")
print("AEA02_CONSTRUCTION_AUTHORIZED=NO")
print("C_DOMAIN_CONSTRUCTION_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("SAFE_D0241_VERIFIER=PASS")
