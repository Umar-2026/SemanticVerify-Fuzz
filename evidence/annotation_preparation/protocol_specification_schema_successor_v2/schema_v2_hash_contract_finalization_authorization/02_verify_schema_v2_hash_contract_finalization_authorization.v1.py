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

authp = (
    here /
    "01_schema_v2_hash_contract_finalization_authorization.v1.json"
)

source = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_activation_governance_package_v1/"
    "07_proposed_v2_hash_contract.REVIEW_CANDIDATE.json"
)

approval = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "completed_activation_governance_human_review_v1/"
    "04_completed_activation_governance_human_approval_record.v1.json"
)

active = (
    repo /
    "config/protocol_content_hash_canonicalization.v2.json"
)

curlp = (
    repo /
    "config/protocol_specifications/curl.json"
)

package = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_hash_contract_finalization_package_v1"
)

if sha(source) != \
   "8fa63b0faea168e7dcc7701d94704d408dbd8d22e5d17d6c83cc3ab90095aab0":
    fail("SOURCE_SHA")

if source.stat().st_size != 3126:
    fail("SOURCE_SIZE")

if sha(approval) != \
   "a118cfd294f5a00fd0f8e124e464c791eaf97229c643b44b981882294191ef18":
    fail("APPROVAL_SHA")

auth = json.loads(
    authp.read_text(encoding="utf-8")
)

if auth["status"] != \
   "AUTHORIZED_TO_AUTHOR_ACTIVE_FORM_HASH_CONTRACT_FINALIZATION_PACKAGE_ONLY":
    fail("AUTH_STATUS")

if auth["basis"][
    "activation_governance_package_human_approved"
] is not True:
    fail("ACTIVATION_GOVERNANCE_APPROVAL")

if auth["basis"]["schema_v2_activated"] is not False:
    fail("PREMATURE_SCHEMA_ACTIVATION")

form = auth["authorized_active_form"]

if form["review_candidate_only"] is not True:
    fail("ACTIVE_FORM_REVIEW_STATE")

if form["target_status"] != \
   "FROZEN_BEFORE_FIRST_SCHEMA_V2_CANONICAL_SPECIFICATION":
    fail("TARGET_STATUS")

if form["top_level_keys_may_be_added"] is not False:
    fail("TOPLEVEL_ADD")

if form["top_level_keys_may_be_removed"] is not False:
    fail("TOPLEVEL_REMOVE")

if form["other_values_may_change"] is not False:
    fail("OTHER_VALUES")

src = json.loads(
    source.read_text(encoding="utf-8")
)

dst = copy.deepcopy(src)

dst["status"] = form["target_status"]

dst["draft_boundary"][
    "review_candidate_is_not_active_contract"
] = False

dst["draft_boundary"][
    "active_path_must_not_be_created_until_later_reviewed_activation_decision"
] = False

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
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
    allow_nan=False
).encode("utf-8")

if hashlib.sha256(pretty).hexdigest() != \
   form["expected_review_candidate_file_sha256"]:
    fail("TARGET_FILE_SHA")

if len(pretty) != \
   form["expected_review_candidate_file_size_bytes"]:
    fail("TARGET_FILE_SIZE")

if hashlib.sha256(canonical).hexdigest() != \
   form["expected_canonical_json_sha256"]:
    fail("TARGET_CANONICAL_SHA")

changes = []

def walk(a, b, path="$"):
    if type(a) is not type(b):
        changes.append((path, a, b))
        return

    if isinstance(a, dict):
        if set(a) != set(b):
            changes.append(
                (path + ".__keys__", sorted(a), sorted(b))
            )
            return

        for k in sorted(a):
            walk(a[k], b[k], path + "." + k)

    elif isinstance(a, list):
        if len(a) != len(b):
            changes.append(
                (path + ".__len__", len(a), len(b))
            )
            return

        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, path + f"[{i}]")

    elif a != b:
        changes.append((path, a, b))

walk(src, dst)

if len(changes) != 3:
    fail("DELTA_COUNT")

expected_paths = {
    "$.status",
    "$.draft_boundary.review_candidate_is_not_active_contract",
    "$.draft_boundary.active_path_must_not_be_created_until_later_reviewed_activation_decision",
}

if {x[0] for x in changes} != expected_paths:
    fail("DELTA_PATHS")

pkg = auth["authorized_finalization_package"]

if pkg["authoring_authorized"] is not True:
    fail("PACKAGE_AUTH")

if pkg["human_review_required"] is not True:
    fail("HUMAN_REVIEW")

if set(auth["review_requirements"]) != {
    f"HF{i:02d}"
    for i in range(1, 9)
}:
    fail("HF_SET")

for key, value in auth["explicit_non_authorizations"].items():
    if value is not False:
        fail("NONAUTH|" + key)

if auth["next_boundary"] != \
   "AUTHOR_ACTIVE_SCHEMA_V2_HASH_CONTRACT_FINALIZATION_PACKAGE_V1":
    fail("NEXT_BOUNDARY")

if active.exists():
    fail("ACTIVE_HASH_EXISTS")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

if package.exists():
    fail("FINALIZATION_PACKAGE_ALREADY_EXISTS")

print("SOURCE_REVIEWED_V2_HASH_CONTRACT=PASS")
print("AUTHORIZED_ACTIVE_FORM_EXACT_DELTA_COUNT=3")
print("AUTHORIZED_ACTIVE_FORM_TARGET_STATUS=FROZEN_BEFORE_FIRST_SCHEMA_V2_CANONICAL_SPECIFICATION")
print("ALL_OTHER_REVIEWED_HASH_CONTRACT_VALUES_PRESERVED=YES")
print("HF01_TO_HF08_REVIEW_REQUIREMENTS=BOUND")
print("ACTIVE_FORM_FINALIZATION_PACKAGE_AUTHORING_AUTHORIZED=YES")
print("INDEPENDENT_ACTIVE_FORM_HUMAN_REVIEW_REQUIRED=YES")
print("ACTIVE_V2_HASH_CONTRACT_CREATED=NO")
print("SCHEMA_V2_ACTIVATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("SCHEMA_V2_HASH_FINALIZATION_AUTHORIZATION_VERIFICATION=PASS")
