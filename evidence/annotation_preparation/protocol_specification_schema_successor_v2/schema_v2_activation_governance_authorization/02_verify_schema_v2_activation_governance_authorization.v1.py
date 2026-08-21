#!/usr/bin/env python3

import hashlib
import json
import subprocess
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
    "01_schema_v2_activation_governance_authorization.v1.json"
)

approval = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "completed_final_human_rereview_v3/"
    "04_completed_schema_v2_final_human_approval_record.v3.json"
)

v1 = repo / "config/schemas/protocol_specification.schema.json"
v2 = repo / "config/schemas/protocol_specification.v2.schema.json"

v1hash = repo / "config/protocol_content_hash_canonicalization.v1.json"

decision19 = (
    repo /
    "documentation/decisions/"
    "0019-canonical-library-protocol-specification-path-convention.md"
)

zlibp = repo / "config/protocol_specifications/zlib.json"
pcapp = repo / "config/protocol_specifications/libpcap.json"
curlp = repo / "config/protocol_specifications/curl.json"

v2hash = repo / "config/protocol_content_hash_canonicalization.v2.json"

package = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_activation_governance_package_v1"
)

if sha(approval) != \
   "6a7c8c836071fe42522330f7b9ff75ec3cba3a855853756c3588c7a04844e1f8":
    fail("APPROVAL_RECORD_SHA")

if sha(v1) != \
   "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34":
    fail("V1_SCHEMA_SHA")

if sha(v2) != \
   "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956":
    fail("V2_SCHEMA_SHA")

if v2.stat().st_size != 43030:
    fail("V2_SCHEMA_SIZE")

if sha(v1hash) != \
   "5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f":
    fail("V1_HASH_SHA")

if sha(zlibp) != \
   "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1":
    fail("ZLIB_SHA")

if sha(pcapp) != \
   "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73":
    fail("LIBPCAP_SHA")

auth = json.loads(
    authp.read_text(
        encoding="utf-8"
    )
)

if auth["status"] != \
   "AUTHORIZED_TO_AUTHOR_SCHEMA_V2_ACTIVATION_GOVERNANCE_PACKAGE_ONLY":
    fail("STATUS")

if auth["basis"]["schema_v2_candidate_human_approved"] is not True:
    fail("HUMAN_APPROVAL")

if auth["basis"]["schema_v2_candidate_activated"] is not False:
    fail("PREMATURE_ACTIVATION")

candidate = auth["approved_schema_v2_candidate"]

if candidate["may_modify"] is not False:
    fail("CANDIDATE_MUTABILITY")

if candidate["sha256"] != \
   "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956":
    fail("CANDIDATE_SHA")

existing = auth["existing_governance"]

if existing["decision_0019_currently_amended_for_v2"] is not False:
    fail("DEC0019_ALREADY_AMENDED")

if existing["decision_0019_currently_superseded"] is not False:
    fail("DEC0019_ALREADY_SUPERSEDED")

if sha(decision19) != existing["decision_0019_sha256"]:
    fail("DECISION_0019_SHA")

v1hc = auth["frozen_v1_hash_contract"]

if v1hc["may_modify"] is not False:
    fail("V1_HASH_MUTABILITY")

if v1hc["may_silently_reuse_for_schema_v2"] is not False:
    fail("V1_HASH_REUSE")

successor = auth["authorized_governance_package"]

if successor["authoring_authorized"] is not True:
    fail("PACKAGE_AUTHORING")

if successor["activation_authorized"] is not False:
    fail("ACTIVATION_AUTHORIZATION")

if successor["human_review_required"] is not True:
    fail("HUMAN_REVIEW")

if successor["schema_v2_candidate_modification_authorized"] is not False:
    fail("SCHEMA_MODIFICATION")

reqs = auth["activation_governance_requirements"]

if set(reqs.keys()) != {
    f"AG{i:02d}"
    for i in range(1, 10)
}:
    fail("AG_SET")

for rid, obj in reqs.items():
    if obj["mandatory"] is not True:
        fail("AG_NOT_MANDATORY|" + rid)

hashv2 = auth["proposed_v2_hash_contract"]

if hashv2["eventual_reserved_path"] != \
   "config/protocol_content_hash_canonicalization.v2.json":
    fail("V2_HASH_RESERVED_PATH")

if hashv2["may_be_created_by_this_authorization_step"] is not False:
    fail("V2_HASH_CREATED_BY_AUTH")

if hashv2["may_be_activated_by_this_authorization"] is not False:
    fail("V2_HASH_ACTIVATED_BY_AUTH")

if hashv2["governance_package_may_contain_review_candidate_copy"] is not True:
    fail("V2_HASH_REVIEW_CANDIDATE")

d19 = auth["decision_0019_change_policy"]

if d19["may_modify_decision_0019_in_place"] is not False:
    fail("DEC0019_INPLACE")

if d19["must_use_new_successor_or_explicit_amendment_decision"] is not True:
    fail("DEC0019_SUCCESSOR_REQUIRED")

if d19["existing_decision_0019_must_remain_historical_immutable_record"] is not True:
    fail("DEC0019_HISTORY")

review = auth["review_requirement"]

if review["independent_human_review_required"] is not True:
    fail("REVIEW_REQUIRED")

if review["review_must_cover_all_AG01_through_AG09"] is not True:
    fail("REVIEW_SCOPE")

if review["reviewer_must_not_be_synthetically_filled"] is not True:
    fail("SYNTHETIC_REVIEW")

if review["schema_v2_must_remain_inactive_until_reviewed_activation_decision"] is not True:
    fail("INACTIVE_UNTIL_REVIEW")

for key, value in auth["explicit_non_authorizations"].items():
    if value is not False:
        fail("NONAUTH|" + key)

if auth["next_boundary"] != \
   "AUTHOR_SCHEMA_V2_ACTIVATION_GOVERNANCE_PACKAGE_V1":
    fail("NEXT_BOUNDARY")

if package.exists():
    fail("ACTIVATION_GOVERNANCE_PACKAGE_ALREADY_EXISTS")

if v2hash.exists():
    fail("ACTIVE_V2_HASH_CONTRACT_ALREADY_EXISTS")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

zblob = subprocess.check_output(
    [
        "git",
        "-C",
        str(repo),
        "rev-parse",
        "HEAD:config/protocol_specifications/zlib.json"
    ],
    text=True
).strip()

pblob = subprocess.check_output(
    [
        "git",
        "-C",
        str(repo),
        "rev-parse",
        "HEAD:config/protocol_specifications/libpcap.json"
    ],
    text=True
).strip()

if zblob != \
   "5e4d5744f9da0b1a2723d4ec834f9ad03b7e64ea":
    fail("ZLIB_BLOB")

if pblob != \
   "ce4ea9b2d97c1ca570b004dc1c4869eb067f8c5d":
    fail("LIBPCAP_BLOB")

print("FINAL_SCHEMA_V2_HUMAN_APPROVAL_BINDING=PASS")
print("SCHEMA_V2_CANDIDATE_HUMAN_APPROVED=YES")
print("SCHEMA_V2_CANDIDATE_IMMUTABLE=YES")
print("DECISION_0019_EXISTING_RULE_BOUND=YES")
print("DECISION_0019_IN_PLACE_MODIFICATION_AUTHORIZED=NO")
print("V1_HASH_CONTRACT_FROZEN=YES")
print("V1_HASH_CONTRACT_SILENT_V2_REUSE_ALLOWED=NO")
print("FROZEN_ZLIB_V1_ARTIFACT_UNMIGRATED=YES")
print("FROZEN_LIBPCAP_V1_ARTIFACT_UNMIGRATED=YES")
print("ACTIVATION_GOVERNANCE_REQUIREMENTS_AG01_TO_AG09=BOUND")
print("SCHEMA_V2_ACTIVATION_GOVERNANCE_PACKAGE_AUTHORING_AUTHORIZED=YES")
print("INDEPENDENT_ACTIVATION_GOVERNANCE_REVIEW_REQUIRED=YES")
print("SCHEMA_V2_ACTIVATED=NO")
print("V2_HASH_CONTRACT_DEFINED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("SCHEMA_V2_ACTIVATION_GOVERNANCE_AUTHORIZATION_VERIFICATION=PASS")
