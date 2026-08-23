#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = (
    HERE
    / "01_review_package_validator_recovery_authorization.v1.json"
)

PKG = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_semantic_role_relation_formalization_v1_review_package_v1"
)

P14 = PKG / \
    "14_pre_review_package_authorization_verifier_consumed.v1"

P15 = PKG / \
    "15_semantic_role_relation_formalization_v1_reviewer_packet.BLANK.v1.md"

P16 = PKG / \
    "16_verify_semantic_role_relation_formalization_v1_review_package.v1.py"

P17 = PKG / \
    "17_semantic_role_relation_formalization_v1_review_package_manifest.v1.json"

P18 = PKG / \
    "18_semantic_role_relation_formalization_v1_review_package.v1.SHA256SUMS"

EXPECTED = {
    P14:
        "2ea22aedeca53f2e372ef938e468b60be8bf13a41dac995ec76eec95063566ee",

    P15:
        "84aa233232268866aaf9a5b8db673ed1c42e0519c7231162dece7f53a7c4ad3b",

    P16:
        "0148c69a7b76190fcb52e05b6c4fcffbddd7316b1dabfcb2a493c6042b3b5bf4",

    P17:
        "ae8e4af6affc156e7774b61d9a360a9b630034b6d25f2fe37d620cf6c73e2ba5",

    P18:
        "a4de27038a599505768f78dfb48041d3701fa5d15fc2111850734d5f5259df99",
}

def fail(msg):
    print(
        "FAIL|" + msg
    )
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if a[
    "status"
] != "AUTHORIZED_EVIDENCE_ONLY_VALIDATOR_RECOVERY":
    fail("STATUS")

if a[
    "authorization_type"
] != "PRE_VALIDATOR_RECOVERY_ONLY":
    fail("AUTHORIZATION_TYPE")

basis = a[
    "recovery_basis"
]

if basis[
    "decision_0091_pre_review_package_verifier_permanently_retired"
] is not True:
    fail("DECISION_0091_RETIREMENT")

if basis[
    "decision_0091_pre_review_package_verifier_rerun_allowed"
] is not False:
    fail("DECISION_0091_RERUN")

for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail(
            "PRE_RECOVERY_SHA|" + path.name
        )

scope = a[
    "authorized_recovery_scope"
]

for key in (
    "modify_16_safe_package_verifier",
    "regenerate_18_checksum_manifest",
    "preserve_01_through_15_byte_exact",
    "preserve_17_byte_exact",
    "preserve_blank_reviewer_packet_byte_exact",
    "preserve_decision_0091_consumption_marker_byte_exact",
    "safe_validator_must_pass_after_recovery",
    "package_checksum_validation_must_pass_after_recovery",
    "new_package_checkpoint_required",
):
    if scope[key] is not True:
        fail(
            "RECOVERY_SCOPE|" + key
        )

for key, value in a[
    "retired_verifier_constraints"
].items():
    if value is not False:
        fail(
            "RETIRED_VERIFIER|" + key
        )

for key, value in a[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "NONAUTH|" + key
        )

packet = P15.read_text(
    encoding="utf-8"
)

safe = re.findall(
    r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):[ \t]*(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(safe) != 8:
    fail("SAFE_ITEM_MATCH_COUNT")

if any(
    value.strip()
    for value in safe
):
    fail("PACKET_NOT_BLANK")

buggy = re.findall(
    r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):\s*(.*)$",
    packet,
    flags=re.MULTILINE,
)

if buggy != [
    "Reviewer notes:"
] * 8:
    fail(
        "BUG_SIGNATURE_NOT_REPRODUCED"
    )

print("PARTIAL_REVIEW_PACKAGE_PRESERVED=YES")
print("SRR01_TO_SRR08_ACTUALLY_BLANK=YES")
print("REGEX_NEWLINE_CONSUMPTION_BUG_CONFIRMED=YES")
print("DECISION_0091_PRE_REVIEW_PACKAGE_VERIFIER_PERMANENTLY_RETIRED=YES")
print("DECISION_0091_PRE_REVIEW_PACKAGE_VERIFIER_RERUN_ALLOWED=NO")

print("P16_VALIDATOR_EVIDENCE_ONLY_CORRECTION_AUTHORIZED=YES")
print("P18_CHECKSUM_REGENERATION_AUTHORIZED=YES")
print("P01_TO_P15_MODIFICATION_AUTHORIZED=NO")
print("P17_MODIFICATION_AUTHORIZED=NO")
print("BLANK_REVIEWER_PACKET_MODIFICATION_AUTHORIZED=NO")
print("HUMAN_REVIEW_DECISION_CREATION_AUTHORIZED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0092_VALIDATOR_RECOVERY_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_VALIDATOR_RECOVERY_ONLY")
