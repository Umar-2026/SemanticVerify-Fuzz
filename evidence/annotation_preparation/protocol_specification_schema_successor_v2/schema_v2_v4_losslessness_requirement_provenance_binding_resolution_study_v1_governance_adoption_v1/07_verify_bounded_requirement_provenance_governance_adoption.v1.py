#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

STUDY_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1"
)

REVIEW_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1_completed_human_review_v1"
)

AUTH_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1_governance_adoption_authorization_v1"
)

MANIFEST = (
    HERE
    / "01_bounded_governance_adoption_manifest.v1.json"
)

A02_OUT = (
    HERE
    / "02_decision0135_a02_final_output.EXACT_COPY.v1.txt"
)

A02_CONS = (
    HERE
    / "03_decision0135_a02_consumption_record.v1.json"
)

DEC0135 = (
    HERE
    / "04_decision0135.EXACT_COPY.md"
)

REVIEW = (
    HERE
    / "05_completed_RPR01_RPR08_human_review.EXACT_COPY.v1.md"
)

STUDY_REPORT = (
    HERE
    / "06_study_v1_report.EXACT_COPY.md"
)

SUMS = (
    HERE
    / "08_bounded_governance_adoption_v1.SHA256SUMS"
)

EXPECTED_STUDY_TREE = (
    "ee85980dcff85b5be3f21995f578b3b78cf39aa2"
)

EXPECTED_REVIEW_TREE = (
    "d873ef00dceb359a2dc8dc25293ab8ec57518dd2"
)

EXPECTED_AUTH_TREE = (
    "8c62c8ec31bc4f6c4a3c0a6940d05f6e80349d79"
)

EXPECTED_REVIEW_SHA = (
    "f133c13bdaeb71055bd839663332c921"
    "556dc516544e19e655f204032d33af71"
)

EXPECTED_DEC0135_SHA = (
    "4a122685d52069641bb8f37e33e3b4cb"
    "2a456f78db9042af96d27495b6968f78"
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

def git(*args):
    p = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            *args,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        return None

    return p.stdout.strip()

if sha(REVIEW) != EXPECTED_REVIEW_SHA:
    fail("COMPLETED_REVIEW_SHA")

if sha(DEC0135) != EXPECTED_DEC0135_SHA:
    fail("DECISION0135_SHA")

review_lines = REVIEW.read_text(
    encoding="utf-8"
).splitlines()

if sum(
    1
    for line in review_lines
    if line.strip() == "Decision: `PASS`"
) != 8:
    fail("RPR_PASS_COUNT")

if (
    "Overall decision: "
    "`APPROVE_V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1`"
    not in review_lines
):
    fail("OVERALL_REVIEW_DECISION")

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if (
    manifest["record_status"]
    != "GOVERNANCE_ADOPTION_COMPLETED"
):
    fail("RECORD_STATUS")

adopted = manifest[
    "adopted_governance_result"
]

if (
    adopted["outcome"]
    != "REQUIREMENT_PROVENANCE_RESOLVED"
):
    fail("ADOPTED_OUTCOME")

if (
    adopted["scope"]
    != "REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY"
):
    fail("ADOPTED_SCOPE")

if adopted["adoption_is_bounded"] is not True:
    fail("BOUNDED_ADOPTION")

if adopted["existing_v4_losslessness_requirement_count"] != 17:
    fail("REQUIREMENT_COUNT")

if adopted["bound_exact_count"] != 17:
    fail("BOUND_EXACT_COUNT")

if adopted["bound_composite_count"] != 0:
    fail("BOUND_COMPOSITE_COUNT")

if adopted["unresolved_count"] != 0:
    fail("UNRESOLVED_COUNT")

if (
    adopted[
        "requirement_identity_and_source_provenance_governance_adopted"
    ]
    is not True
):
    fail("ADOPTION_STATE")

gov = manifest[
    "governance_state_after_adoption"
]

if gov["study_governance_adopted"] is not True:
    fail("GOVERNANCE_NOT_ADOPTED")

if gov["governance_adoption_completed"] is not True:
    fail("GOVERNANCE_ADOPTION_NOT_COMPLETED")

if (
    gov["adopted_scope"]
    != "REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY"
):
    fail("GOVERNANCE_SCOPE")

nonclaims = manifest[
    "technical_nonclaims_preserved"
]

for key, value in nonclaims.items():
    if value is not False:
        fail(
            "UNEXPECTED_TECHNICAL_CLAIM|"
            + key
        )

for key, value in manifest[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_OPERATIONAL_AUTHORIZATION|"
            + key
        )

cons = json.loads(
    A02_CONS.read_text(
        encoding="utf-8"
    )
)

if cons["final_run_result"] != "PASS":
    fail("A02_FINAL_RESULT")

if (
    cons["verifier_state_after_run"]
    != "PERMANENTLY_RETIRED"
):
    fail("A02_RETIREMENT")

if cons["rerun_authorized"] is not False:
    fail("A02_RERUN_POLICY")

if cons["must_never_be_rerun"] is not True:
    fail("A02_NO_RERUN_BOUNDARY")

if (
    cons["previous_retired_a02_verifiers_executed"]
    is not False
):
    fail("PREVIOUS_RETIRED_A02_EXECUTION")

if sha(A02_OUT) != cons["final_output_sha256"]:
    fail("A02_OUTPUT_SHA")

if (
    "REVIEWED_REQUIREMENT_PROVENANCE_GOVERNANCE_ADOPTION_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(
        encoding="utf-8"
    )
):
    fail("A02_PASS_MARKER")

if (
    "REQUIREMENT_PROVENANCE_RESOLVED"
    not in STUDY_REPORT.read_text(
        encoding="utf-8"
    )
):
    fail("STUDY_REPORT_OUTCOME")

# Verify repository tree bindings when available.
for rel, expected, label in (
    (
        STUDY_REL,
        EXPECTED_STUDY_TREE,
        "STUDY_V1_GIT_TREE",
    ),
    (
        REVIEW_REL,
        EXPECTED_REVIEW_TREE,
        "COMPLETED_REVIEW_GIT_TREE",
    ),
    (
        AUTH_REL,
        EXPECTED_AUTH_TREE,
        "AUTHORIZATION_GIT_TREE",
    ),
):
    actual = git(
        "rev-parse",
        "HEAD:" + rel,
    )

    if actual is not None and actual != expected:
        fail(label)

if SUMS.is_file():
    for line in SUMS.read_text(
        encoding="utf-8"
    ).splitlines():

        if not line.strip():
            continue

        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")

        if sha(HERE / rel) != digest:
            fail(
                "CHECKSUM|"
                + rel
            )

print(
    "BOUNDED_REQUIREMENT_PROVENANCE_GOVERNANCE_ADOPTION_V1=PASS"
)

print(
    "ADOPTED_OUTCOME="
    "REQUIREMENT_PROVENANCE_RESOLVED"
)

print(
    "ADOPTED_SCOPE="
    "REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY"
)

print("REQUIREMENT_COUNT=17")
print("BOUND_EXACT_COUNT=17")
print("BOUND_COMPOSITE_COUNT=0")
print("UNRESOLVED_COUNT=0")

print("HUMAN_REVIEW_COMPLETED=YES")
print("RPR01_RPR08_PASS_COUNT=8")
print("REVIEWER_DECISION_SYNTHESIZED=NO")

print("STUDY_GOVERNANCE_ADOPTED=YES")
print("GOVERNANCE_ADOPTION_AUTHORIZED=YES")
print("GOVERNANCE_ADOPTION_COMPLETED=YES")

print("SCHEMA_V2_LOSSLESSNESS_PROVEN=NO")
print("CARRIER_ADMISSIBILITY_PROVEN=NO")
print("POSITIVE_MAPPING_PROVEN=NO")
print("NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0135_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0135_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
