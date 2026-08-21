#!/usr/bin/env python3

import copy
import hashlib
import json
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(
        p.read_bytes()
    ).hexdigest()

here = Path(__file__).resolve().parent
repo = here

while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

authp = here / \
    "01_schema_v2_activation_artifact_finalization_authorization.v1.json"

dispatch_source = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_activation_governance_package_v1/"
    "09_version_dispatch_policy.REVIEW_CANDIDATE.json"
)

successor_source = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_activation_governance_package_v1/"
    "05_proposed_decision_0019_successor.REVIEW_CANDIDATE.md"
)

hash_form = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_hash_contract_finalization_package_v1/"
    "02_active_form_v2_hash_contract.REVIEW_CANDIDATE.json"
)

active_hash = (
    repo /
    "config/protocol_content_hash_canonicalization.v2.json"
)

active_dispatch = (
    repo /
    "config/protocol_specification_schema_version_dispatch.v1.json"
)

curl_json = (
    repo /
    "config/protocol_specifications/curl.json"
)

package = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_activation_artifact_finalization_package_v1"
)

if sha(dispatch_source) != \
   "5a91a9938af7029edff6b91b8b624b2f0712680d49fad3abd1be29e649944bce":
    fail("DISPATCH_SOURCE_SHA")

if sha(successor_source) != \
   "8665163eb5d4f7a8718ba3ed2d3973ba928fea85789c23696599a2d6ea02bbb3":
    fail("SUCCESSOR_SOURCE_SHA")

if successor_source.stat().st_size != 2158:
    fail("SUCCESSOR_SOURCE_SIZE")

if sha(hash_form) != \
   "37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9":
    fail("HASH_FORM_SHA")

auth = json.loads(
    authp.read_text(encoding="utf-8")
)

if auth["status"] != \
   "AUTHORIZED_TO_AUTHOR_SCHEMA_V2_ACTIVATION_ARTIFACT_FINALIZATION_PACKAGE_ONLY":
    fail("AUTH_STATUS")

d = auth["proposed_active_version_dispatch_form"]

src = json.loads(
    dispatch_source.read_text(encoding="utf-8")
)

dst = copy.deepcopy(src)
dst["status"] = d["target_status"]

pretty = (
    json.dumps(
        dst,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False
    )
    + "\n"
).encode("utf-8")

canonical = json.dumps(
    dst,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False
).encode("utf-8")

if hashlib.sha256(pretty).hexdigest() != \
   "67a96c3eda8de95fa6c55342d5d33ea725e16cea8af21fcb4f3b8945b9d4eeee":
    fail("DISPATCH_TARGET_SHA")

if len(pretty) != 1334:
    fail("DISPATCH_TARGET_SIZE")

if hashlib.sha256(canonical).hexdigest() != \
   "2333c2521db84ddb347b23a956acebdc6ad713c61cc890b76d7b04d0b8d2fc7f":
    fail("DISPATCH_CANONICAL_SHA")

if d["exact_delta_count"] != 1:
    fail("DISPATCH_DELTA_COUNT")

if dst["dispatch"]["2.0.0"][
    "eligible_only_after_separate_reviewed_activation"
] is not True:
    fail("DISPATCH_ACTIVATION_CONDITION")

s = auth[
    "proposed_active_decision_0019_successor_form"
]

text = successor_source.read_text(
    encoding="utf-8"
).replace("\r\n", "\n").replace("\r", "\n")

for item in s["transformations"]:
    old = item["from"]
    new = item["to"]

    if text.count(old) != 1:
        fail(
            "SUCCESSOR_SOURCE_COUNT|"
            + item["id"]
            + "|"
            + str(text.count(old))
        )

    text = text.replace(
        old,
        new,
        1
    )

raw = text.encode("utf-8")

if hashlib.sha256(raw).hexdigest() != \
   "a96f9d8b6811a9f9170a18de9ff8be6f80a3704b9e6a13c59fbb88e423bec3bb":
    fail("SUCCESSOR_TARGET_SHA")

if len(raw) != 2203:
    fail("SUCCESSOR_TARGET_SIZE")

if s["exact_transformation_count"] != 3:
    fail("SUCCESSOR_TRANSFORMATION_COUNT")

if "REVIEW CANDIDATE —" in text:
    fail("SUCCESSOR_CANDIDATE_TITLE_REMAINS")

if "Status: REVIEW CANDIDATE — NOT ACTIVE" in text:
    fail("SUCCESSOR_CANDIDATE_STATUS_REMAINS")

if (
    "This text becomes operative only if a later explicit reviewed activation\n"
    "decision adopts it. Until then it is a review candidate only."
) in text:
    fail("SUCCESSOR_OLD_ACTIVATION_BLOCK_REMAINS")

if set(auth["mandatory_review_requirements"]) != {
    f"AF{i:02d}"
    for i in range(1, 11)
}:
    fail("AF_SET")

if auth["authorized_package"][
    "authoring_authorized"
] is not True:
    fail("PACKAGE_AUTHORIZATION")

if auth["authorized_package"][
    "human_review_required"
] is not True:
    fail("HUMAN_REVIEW_REQUIREMENT")

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

if active_hash.exists():
    fail("ACTIVE_HASH_EXISTS")

if active_dispatch.exists():
    fail("ACTIVE_DISPATCH_EXISTS")

if curl_json.exists():
    fail("CURL_JSON_EXISTS")

if package.exists():
    fail("PACKAGE_ALREADY_EXISTS")

if auth["next_boundary"] != \
   "AUTHOR_SCHEMA_V2_ACTIVATION_ARTIFACT_FINALIZATION_PACKAGE_V1":
    fail("NEXT_BOUNDARY")

print("REVIEWED_VERSION_DISPATCH_SOURCE=PASS")
print("AUTHORIZED_ACTIVE_DISPATCH_EXACT_DELTA_COUNT=1")
print("ACTIVE_DISPATCH_FUTURE_PATH=config/protocol_specification_schema_version_dispatch.v1.json")
print("REVIEWED_DECISION_0019_SUCCESSOR_SOURCE=PASS")
print("AUTHORIZED_SUCCESSOR_TRANSFORMATION_COUNT=3")
print("SUCCESSOR_MULTILINE_ACTIVATION_BLOCK_BINDING=PASS")
print("APPROVED_V2_HASH_FORM_REQUIRES_FURTHER_TRANSFORMATION=NO")
print("AF01_TO_AF10_REVIEW_REQUIREMENTS=BOUND")
print("ACTIVATION_ARTIFACT_FINALIZATION_PACKAGE_AUTHORING_AUTHORIZED=YES")
print("INDEPENDENT_ACTIVATION_ARTIFACT_HUMAN_REVIEW_REQUIRED=YES")
print("ACTIVE_V2_HASH_CONTRACT_CREATED=NO")
print("ACTIVE_VERSION_DISPATCH_POLICY_CREATED=NO")
print("SCHEMA_V2_ACTIVATED=NO")
print("ACTIVATION_ARTIFACT_FINALIZATION_AUTHORIZATION_VERIFICATION=PASS")
