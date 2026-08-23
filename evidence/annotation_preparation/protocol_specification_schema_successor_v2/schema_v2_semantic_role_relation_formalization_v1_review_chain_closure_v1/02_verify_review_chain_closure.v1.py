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

COMPLETED_REL = (
    BASE_REL
    + "/schema_v2_semantic_role_relation_formalization_v1_"
      "corrective_successor_package_v2_completed_focused_human_review_v1"
)

COMPLETED = REPO / COMPLETED_REL

R01 = (
    COMPLETED
    / "01_completed_focused_human_review.EXACT_COPY.v1.md"
)

R02 = (
    COMPLETED
    / "02_completed_focused_human_review_record.v1.json"
)

R03 = (
    COMPLETED
    / "03_verify_repository_completed_focused_human_review.v1.py"
)

R04 = (
    COMPLETED
    / "04_completed_focused_human_review.v1.SHA256SUMS"
)

ASSESSMENT = (
    HERE
    / "01_review_chain_closure_assessment.v1.json"
)

SUMS = (
    HERE
    / "03_review_chain_closure.v1.SHA256SUMS"
)

EXPECTED_SHA = {
    R01:
        "30973cde36434c4737be4359ba316f579af6a58ca5c0cd9ff1155cab03e902ce",

    R02:
        "08e458c46cdbfd66d500a2dac33110a16569dbb6db999252364d9ecf8d44a8b4",

    R03:
        "70dfc8dee94436f25057de242cb67db9cf1661bb958128a3780d7fd24e1951ba",

    R04:
        "38f21406b1d3c9f6f1abd3fa2994f9e2471016501e8d5f4a73b8380e42af3947",
}

EXPECTED_SIZE = {
    R01: 4546,
    R02: 2536,
    R03: 9930,
    R04: 356,
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED_SHA.items():
    actual = sha(path)

    if actual != expected:
        fail(
            "SOURCE_SHA|"
            + str(path)
            + "|ACTUAL="
            + actual
        )

    if path.stat().st_size != EXPECTED_SIZE[path]:
        fail(
            "SOURCE_SIZE|"
            + str(path)
        )

# ------------------------------------------------------------
# Bind Decision-0100 completed-review directory Git tree.
# ------------------------------------------------------------

proc = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        "HEAD:" + COMPLETED_REL,
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if proc.returncode != 0:
    fail(
        "COMPLETED_REVIEW_TREE_LOOKUP"
    )

if proc.stdout.strip() != \
        "0cf6eafe8c317ff7f3f1f11649664f058aefb2ec":
    fail(
        "COMPLETED_REVIEW_TREE_CHANGED"
    )

# ------------------------------------------------------------
# Run only safe Decision-0100 verifier.
# ------------------------------------------------------------

proc = subprocess.run(
    [
        "python3",
        str(R03),
    ],
    cwd=str(COMPLETED),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)

if proc.returncode != 0:
    fail(
        "DECISION0100_SAFE_VERIFIER_RC|"
        + str(proc.returncode)
    )

if (
    b"REPOSITORY_COMPLETED_FOCUSED_HUMAN_REVIEW=PASS"
    not in proc.stdout
):
    fail(
        "DECISION0100_SAFE_VERIFIER_PASS_MARKER"
    )

# ------------------------------------------------------------
# Validate historical source record.
# ------------------------------------------------------------

source = json.loads(
    R02.read_text(
        encoding="utf-8"
    )
)

if source[
    "review_chain_state"
][
    "original_overall_human_review"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_REVIEW_HISTORY"
    )

if source[
    "review_chain_state"
][
    "original_review_remains_immutable"
] is not True:
    fail(
        "ORIGINAL_REVIEW_IMMUTABILITY"
    )

if set(
    source[
        "review_chain_state"
    ][
        "carried_forward_pass_items"
    ]
) != {
    "SRR01",
    "SRR03",
    "SRR06",
    "SRR07",
}:
    fail(
        "CARRIED_FORWARD_PASS_SET"
    )

if source[
    "focused_item_decisions"
] != {
    "SRR02-C": "PASS",
    "SRR04-C": "PASS",
    "SRR05-C": "PASS",
    "SRR08-C": "PASS",
}:
    fail(
        "CORRECTIVE_PASS_SET"
    )

if source[
    "overall_focused_decision"
] != "APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2":
    fail(
        "FOCUSED_OVERALL"
    )

# ------------------------------------------------------------
# Validate Decision-0101 closure assessment.
# ------------------------------------------------------------

assessment = json.loads(
    ASSESSMENT.read_text(
        encoding="utf-8"
    )
)

if assessment["decision"] != "PASS_CLOSED":
    fail(
        "CLOSURE_DECISION"
    )

if assessment[
    "governance_action"
] != (
    "ADOPT_CORRECTIVE_FOCUSED_HUMAN_APPROVAL_AND_"
    "CLOSE_FORMALIZATION_V1_REVIEW_CHAIN"
):
    fail(
        "GOVERNANCE_ACTION"
    )

historical = assessment[
    "historical_original_review"
]

if historical[
    "overall_decision"
] != "REVISION_REQUIRED":
    fail(
        "HISTORICAL_ORIGINAL_DECISION"
    )

if historical[
    "historical_decision_remains_immutable"
] is not True:
    fail(
        "HISTORICAL_IMMUTABILITY"
    )

if set(
    historical[
        "carried_forward_pass_items"
    ]
) != {
    "SRR01",
    "SRR03",
    "SRR06",
    "SRR07",
}:
    fail(
        "HISTORICAL_CARRIED_PASS_SET"
    )

resolution = assessment[
    "corrective_resolution"
]

expected_mapping = {
    "SRR02": "SRR02-C",
    "SRR04": "SRR04-C",
    "SRR05": "SRR05-C",
    "SRR08": "SRR08-C",
}

for original, corrective in expected_mapping.items():
    row = resolution.get(original)

    if not row:
        fail(
            "MISSING_CORRECTIVE_MAPPING|" + original
        )

    if row["corrective_item"] != corrective:
        fail(
            "CORRECTIVE_MAPPING|" + original
        )

    if row["corrective_decision"] != "PASS":
        fail(
            "CORRECTIVE_DECISION|" + original
        )

    if row["effective_resolution"] != \
            "CLOSED_BY_CORRECTIVE_PASS":
        fail(
            "CORRECTIVE_RESOLUTION|" + original
        )

focused = assessment[
    "focused_review"
]

if focused[
    "overall_decision"
] != "APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2":
    fail(
        "ASSESSMENT_FOCUSED_OVERALL"
    )

if focused[
    "independent_human_review_completed"
] is not True:
    fail(
        "HUMAN_REVIEW_COMPLETION"
    )

if focused[
    "corrective_successor_package_v2_human_approved"
] is not True:
    fail(
        "HUMAN_APPROVAL"
    )

effective = assessment[
    "effective_review_state"
]

if effective[
    "all_original_review_criteria_satisfied"
] is not True:
    fail(
        "ALL_REVIEW_CRITERIA"
    )

if effective[
    "corrective_successor_package_v2_governance_adopted"
] is not True:
    fail(
        "PACKAGE_GOVERNANCE_ADOPTION"
    )

if effective[
    "formalization_v1_review_chain"
] != "PASS_CLOSED":
    fail(
        "REVIEW_CHAIN_STATE"
    )

if effective[
    "formalization_v1_governance_approval"
] is not True:
    fail(
        "FORMALIZATION_GOVERNANCE_APPROVAL"
    )

if effective[
    "formalization_v1_governance_status"
] != "APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME":
    fail(
        "FORMALIZATION_GOVERNANCE_STATUS"
    )

technical = assessment[
    "technical_outcome"
]

if technical[
    "formalization_v1_author_outcome"
] != "PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED":
    fail(
        "TECHNICAL_OUTCOME_CHANGED"
    )

if technical[
    "outcome_preserved"
] is not True:
    fail(
        "TECHNICAL_OUTCOME_NOT_PRESERVED"
    )

for key in (
    "positive_existing_v2_mapping_proven",
    "negative_existing_v2_mapping_impossibility_proven",
    "admissible_composition_exhaustiveness_established",
):
    if technical[key] is not False:
        fail(
            "UNSUPPORTED_TECHNICAL_CLAIM|" + key
        )

non_auth = assessment[
    "bounded_non_authorizations"
]

for key, value in non_auth.items():
    if value is not False:
        fail(
            "UNEXPECTED_AUTHORIZATION|" + key
        )

# ------------------------------------------------------------
# Check closure checksum manifest if present.
# ------------------------------------------------------------

if SUMS.is_file():
    lines = [
        x
        for x in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if x.strip()
    ]

    if len(lines) != 2:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for raw in lines:
        digest, rel = raw.split(
            None,
            1,
        )

        rel = rel.strip()

        if rel.startswith("*"):
            rel = rel[1:]

        if rel.startswith("./"):
            rel = rel[2:]

        target = HERE / rel

        if sha(target) != digest:
            fail(
                "CHECKSUM|" + rel
            )

print("DECISION_0100_COMPLETED_REVIEW_BINDING=PASS")
print("ORIGINAL_OVERALL_HUMAN_REVIEW=REVISION_REQUIRED")
print("ORIGINAL_REVIEW_REMAINS_IMMUTABLE=YES")

print("SRR01=PASS_CARRIED_FORWARD")
print("SRR03=PASS_CARRIED_FORWARD")
print("SRR06=PASS_CARRIED_FORWARD")
print("SRR07=PASS_CARRIED_FORWARD")

print("SRR02=PASS_CLOSED_BY_SRR02_C")
print("SRR04=PASS_CLOSED_BY_SRR04_C")
print("SRR05=PASS_CLOSED_BY_SRR05_C")
print("SRR08=PASS_CLOSED_BY_SRR08_C")

print("ALL_REVIEW_CRITERIA_EFFECTIVELY_SATISFIED=YES")
print("CORRECTIVE_SUCCESSOR_PACKAGE_V2_GOVERNANCE_ADOPTED=YES")
print("FORMALIZATION_V1_REVIEW_CHAIN=PASS_CLOSED")
print("FORMALIZATION_V1_GOVERNANCE_APPROVAL=YES")
print("FORMALIZATION_V1_GOVERNANCE_STATUS=APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME")

print("FORMALIZATION_V1_TECHNICAL_OUTCOME=PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED")

print("POSITIVE_EXISTING_V2_MAPPING_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO")

print("EXHAUSTIVE_COMPOSITION_STUDY_AUTHORIZED=NO")
print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("SEMANTIC_ROLE_FORMALIZATION_V1_REVIEW_CHAIN_CLOSURE=PASS")
