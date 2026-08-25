#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

MANIFEST = HERE / "01_bounded_governance_adoption_manifest.v1.json"
ACCOUNTING = HERE / "02_adopted_reviewed_result_accounting.v1.json"
A02_OUT = HERE / "03_decision0145_a02_final_output.EXACT_COPY.v1.txt"
A02_CONS = HERE / "04_decision0145_a02_consumption_record.v1.json"
DEC0145 = HERE / "05_decision0145.EXACT_COPY.md"
DEC0144 = HERE / "06_decision0144.EXACT_COPY.md"
SUMS = HERE / "08_bounded_governance_adoption_v1.SHA256SUMS"

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

RECORD_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_completed_human_review_record_v1"
)

RECORD = REPO / RECORD_REL

RECORD_SAFE = (
    RECORD
    / "08_verify_completed_RBCA01_RBCA08_human_review_record.v1.py"
)

EXPECTED_RECORD_TREE = (
    "1b42cb3de3eb699c9e8a80387787250c6355d23b"
)

EXPECTED_REVIEW_SHA = (
    "9ded6b54b04c438a9a0f5ac3b7557d5ab19283c812fa5f2f6b529c92ef2e7eb1"
)

EXPECTED_DEC0145_SHA = (
    "901b6c1156164bb3b9801074ebe99252b518a8828d15b13e77f5435a55e50d56"
)

EXPECTED_DEC0144_SHA = (
    "02a16fc23b7e67bafb0973abc9f11ea7bbd914992b8d0207feb842a539c1ad95"
)

EXPECTED_OVERALL = (
    "APPROVE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

manifest = json.loads(
    MANIFEST.read_text(encoding="utf-8")
)

if (
    manifest["adoption_status"]
    != "ADOPTED_AS_BOUNDED_GOVERNANCE_EVIDENCE"
):
    fail("ADOPTION_STATUS")

review = manifest["human_review_binding"]

if review["completed_review_packet_sha256"] != EXPECTED_REVIEW_SHA:
    fail("REVIEW_SHA")

if review["human_review_completed"] is not True:
    fail("HUMAN_REVIEW_COMPLETED")

if review["human_review_recorded_in_repository"] is not True:
    fail("HUMAN_REVIEW_RECORDED")

if review["review_item_count"] != 8:
    fail("REVIEW_ITEM_COUNT")

if review["pass_count"] != 8:
    fail("PASS_COUNT")

if review["revision_required_count"] != 0:
    fail("REVISION_COUNT")

if review["fail_count"] != 0:
    fail("FAIL_COUNT")

if review["overall_review_decision"] != EXPECTED_OVERALL:
    fail("OVERALL_REVIEW_DECISION")

if review["reviewer_decision_synthesized"] is not False:
    fail("REVIEWER_DECISION_SYNTHESIZED")

if review["reviewer_identity_synthesized"] is not False:
    fail("REVIEWER_IDENTITY_SYNTHESIZED")

if review["reviewer_notes_rewritten"] is not False:
    fail("REVIEWER_NOTES_REWRITTEN")

bounded = manifest["adopted_bounded_result"]

if bounded["governance_result"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("GOVERNANCE_RESULT")

if bounded["requirement_count"] != 17:
    fail("REQUIREMENT_COUNT")

if bounded["semantic_unit_count"] != 109:
    fail("SEMANTIC_UNIT_COUNT")

if bounded["schema_v2_property_path_count"] != 171:
    fail("SCHEMA_PATH_COUNT")

if bounded["historical_carrier_pair_count"] != 18639:
    fail("PAIR_COUNT")

if (
    bounded["requirement_to_semantic_unit_crosswalk_identified"]
    is not False
):
    fail("CROSSWALK_STATE")

if bounded["admissible_exact_count"] != 0:
    fail("ADMISSIBLE_EXACT")

if bounded["admissible_composite_count"] != 0:
    fail("ADMISSIBLE_COMPOSITE")

if bounded["no_admissible_carrier_proven_count"] != 0:
    fail("NO_ADMISSIBLE_CARRIER_PROVEN")

if bounded["unresolved_count"] != 17:
    fail("UNRESOLVED_COUNT")

gov = manifest["governance_state"]

if gov["human_review_completed"] is not True:
    fail("GOV_REVIEW_COMPLETED")

if gov["human_review_recorded_in_repository"] is not True:
    fail("GOV_REVIEW_RECORDED")

if gov["study_governance_adopted"] is not True:
    fail("GOVERNANCE_NOT_ADOPTED")

if gov["study_governance_adoption_scope"] != \
    "BOUNDED_REVIEWED_RESULT_ONLY":
    fail("GOVERNANCE_SCOPE")

if gov["adopted_governance_result"] != \
    "FURTHER_EVIDENCE_REQUIRED":
    fail("ADOPTED_RESULT")

if (
    gov[
        "governance_adoption_does_not_resolve_carrier_admissibility"
    ]
    is not True
):
    fail("CARRIER_BOUNDARY")

if (
    gov[
        "governance_adoption_does_not_establish_mapping"
    ]
    is not True
):
    fail("MAPPING_BOUNDARY")

for key, value in manifest["technical_nonclaims"].items():
    if value is not False:
        fail("UNEXPECTED_TECHNICAL_CLAIM|" + key)

for key, value in manifest["explicit_non_authorizations"].items():
    if value is not False:
        fail("UNEXPECTED_OPERATIONAL_AUTHORIZATION|" + key)

cons = json.loads(
    A02_CONS.read_text(encoding="utf-8")
)

if cons["final_run_result"] != "PASS":
    fail("A02_RESULT")

if cons["verifier_state_after_run"] != "PERMANENTLY_RETIRED":
    fail("A02_STATE")

if cons["rerun_authorized"] is not False:
    fail("A02_RERUN")

if cons["must_never_be_rerun"] is not True:
    fail("A02_RETIREMENT")

if cons["previous_retired_a02_verifiers_executed"] is not False:
    fail("PREVIOUS_RETIRED_A02")

if sha(A02_OUT) != cons["final_output_sha256"]:
    fail("A02_OUTPUT_SHA")

if (
    "BOUNDED_GOVERNANCE_ADOPTION_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(encoding="utf-8")
):
    fail("A02_PASS_MARKER")

if sha(DEC0145) != EXPECTED_DEC0145_SHA:
    fail("DECISION0145_SHA")

if sha(DEC0144) != EXPECTED_DEC0144_SHA:
    fail("DECISION0144_SHA")

accounting = json.loads(
    ACCOUNTING.read_text(encoding="utf-8")
)

if accounting["review_accounting"]["pass_count"] != 8:
    fail("ACCOUNTING_PASS_COUNT")

if (
    accounting["review_accounting"]["overall_review_decision"]
    != EXPECTED_OVERALL
):
    fail("ACCOUNTING_OVERALL")

adopted = accounting["adopted_result_accounting"]

if adopted["governance_result"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("ACCOUNTING_RESULT")

if adopted["unresolved_count"] != 17:
    fail("ACCOUNTING_UNRESOLVED")

if accounting["governance_adoption"]["adopted"] is not True:
    fail("ACCOUNTING_ADOPTION")

if accounting["governance_adoption"]["scope"] != \
    "BOUNDED_REVIEWED_RESULT_ONLY":
    fail("ACCOUNTING_SCOPE")

if accounting["operational_permissions_granted"] != []:
    fail("OPERATIONAL_PERMISSION_LIST")

p = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        "HEAD:" + RECORD_REL,
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail("RECORD_TREE_QUERY")

if p.stdout.strip() != EXPECTED_RECORD_TREE:
    fail("RECORD_TREE_CHANGED")

p = subprocess.run(
    ["python3", str(RECORD_SAFE)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "COMPLETED_REVIEW_RECORD_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

for marker in (
    "COMPLETED_RBCA01_RBCA08_HUMAN_REVIEW_RECORD_V1=PASS",
    "HUMAN_REVIEW_COMPLETED=YES",
    "HUMAN_REVIEW_RECORDED_IN_REPOSITORY=YES",
    "RBCA01_RBCA08_PASS_COUNT=8",
    "REVIEWED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED",
    "UNRESOLVED_COUNT=17",
    "CARRIER_ADMISSIBILITY_RESOLVED=NO",
    "POSITIVE_MAPPING_PROVEN=NO",
    "NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO",
    "WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO",
    "DECISION_0143_A02_STATE=PERMANENTLY_RETIRED",
    "RETIRED_A02_VERIFIERS_EXECUTED=NO",
):
    if marker not in p.stdout:
        fail("UPSTREAM_SAFE_MARKER|" + marker)

if SUMS.is_file():
    for line in SUMS.read_text(
        encoding="utf-8"
    ).splitlines():

        if not line.strip():
            continue

        digest, rel = line.split(None, 1)
        rel = rel.strip().lstrip("*")

        if sha(HERE / rel) != digest:
            fail("CHECKSUM|" + rel)

print("REQUIREMENT_BOUND_CARRIER_STUDY_V1_BOUNDED_GOVERNANCE_ADOPTION=PASS")
print("ADOPTION_STATUS=ADOPTED_AS_BOUNDED_GOVERNANCE_EVIDENCE")
print("HUMAN_REVIEW_COMPLETED=YES")
print("HUMAN_REVIEW_RECORDED_IN_REPOSITORY=YES")
print("STUDY_GOVERNANCE_ADOPTED=YES")
print("GOVERNANCE_ADOPTION_SCOPE=BOUNDED_REVIEWED_RESULT_ONLY")
print("ADOPTED_GOVERNANCE_RESULT=FURTHER_EVIDENCE_REQUIRED")
print("REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_IDENTIFIED=NO")
print("ADMISSIBLE_EXACT_COUNT=0")
print("ADMISSIBLE_COMPOSITE_COUNT=0")
print("NO_ADMISSIBLE_CARRIER_PROVEN_COUNT=0")
print("UNRESOLVED_COUNT=17")
print("CARRIER_ADMISSIBILITY_RESOLVED=NO")
print("POSITIVE_MAPPING_PROVEN=NO")
print("NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO")
print("SCHEMA_V2_LOSSLESSNESS_PROVEN=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("DECISION_0145_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0145_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
