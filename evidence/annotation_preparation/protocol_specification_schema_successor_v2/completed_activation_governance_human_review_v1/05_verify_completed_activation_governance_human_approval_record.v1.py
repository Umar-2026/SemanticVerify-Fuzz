#!/usr/bin/env python3

import hashlib
import json
import re
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

review = (
    here /
    "01_completed_activation_governance_human_review.APPROVED.v1.md"
)

handoff = (
    here /
    "02_activation_governance_handoff_manifest.v1.json"
)

proof = (
    here /
    "03_postcommit_package_noninterference_proof"
)

recordp = (
    here /
    "04_completed_activation_governance_human_approval_record.v1.json"
)

package = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_activation_governance_package_v1"
)

v2 = (
    repo /
    "config/schemas/protocol_specification.v2.schema.json"
)

v1hash = (
    repo /
    "config/protocol_content_hash_canonicalization.v1.json"
)

decision19 = (
    repo /
    "documentation/decisions/"
    "0019-canonical-library-protocol-specification-path-convention.md"
)

zlibp = (
    repo /
    "config/protocol_specifications/zlib.json"
)

pcapp = (
    repo /
    "config/protocol_specifications/libpcap.json"
)

active_v2_hash = (
    repo /
    "config/protocol_content_hash_canonicalization.v2.json"
)

curlp = (
    repo /
    "config/protocol_specifications/curl.json"
)

if sha(review) != \
   "2b5421a0466bdec575e87f035fb303c8ed1b610bc242c14a977870b4b87d2109":
    fail("REVIEW_SHA")

if review.stat().st_size != 7345:
    fail("REVIEW_SIZE")

if sha(handoff) != \
   "cf598ff24ebc32a23b3fdefe1c3e068cd85663572a9e5e917389b1b15bd98147":
    fail("HANDOFF_SHA")

if sha(
    proof /
    "00_postcommit_noninterference_manifest.v1.json"
) != \
   "36724321570e9ab03f524d7aa905bb3322d6a20c5522ffc30047fbd04c72b029":
    fail("POSTPROOF_MANIFEST_SHA")

if sha(
    proof /
    "97_postcommit_activation_governance_package_noninterference.v1.SHA256SUMS"
) != \
   "d28336184b566c630dfe44bc9906daf4f985a2f72f1a6c0726c19f31d868567e":
    fail("POSTPROOF_SUMS_SHA")

subprocess.check_call(
    [
        "python3",
        str(
            proof /
            "99_verify_postcommit_activation_governance_package_noninterference.v1.py"
        )
    ],
    stdout=subprocess.DEVNULL
)

if sha(
    package /
    "20_schema_v2_activation_governance_package_manifest.v1.json"
) != \
   "5338a5347ce73dbf6420e4c7eb5c1c87c0fbcee41598888d84c531034eedd71c":
    fail("PACKAGE_MANIFEST_SHA")

if sha(
    package /
    "21_schema_v2_activation_governance_package.v1.SHA256SUMS"
) != \
   "ef528e002fed0db3cb1faa99642898f3053cd3e4d326763d2cc8e26d028b82a7":
    fail("PACKAGE_SUMS_SHA")

if sha(
    package /
    "07_proposed_v2_hash_contract.REVIEW_CANDIDATE.json"
) != \
   "8fa63b0faea168e7dcc7701d94704d408dbd8d22e5d17d6c83cc3ab90095aab0":
    fail("V2_HASH_CANDIDATE_SHA")

if sha(
    package /
    "09_version_dispatch_policy.REVIEW_CANDIDATE.json"
) != \
   "5a91a9938af7029edff6b91b8b624b2f0712680d49fad3abd1be29e649944bce":
    fail("DISPATCH_SHA")

if sha(
    package /
    "05_proposed_decision_0019_successor.REVIEW_CANDIDATE.md"
) != \
   "8665163eb5d4f7a8718ba3ed2d3973ba928fea85789c23696599a2d6ea02bbb3":
    fail("SUCCESSOR_SHA")

if sha(v2) != \
   "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956":
    fail("V2_SCHEMA_SHA")

if sha(v1hash) != \
   "5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f":
    fail("V1_HASH_SHA")

if sha(decision19) != \
   "50e273ecb6af838bc83d2499a2ed3a71607bc7c0cf8d74bd2622b56c2fefafa9":
    fail("DEC0019_SHA")

if sha(zlibp) != \
   "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1":
    fail("ZLIB_SHA")

if sha(pcapp) != \
   "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73":
    fail("LIBPCAP_SHA")

text = (
    review.read_text(encoding="utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

for i in range(1, 10):
    rid = f"AG{i:02d}"

    h = re.search(
        r"^##\s+" + re.escape(rid) + r"\b[^\n]*$",
        text,
        re.M
    )

    if not h:
        fail("AG_HEADING|" + rid)

    tail = text[h.end():]

    nxt = re.search(
        r"^##\s+",
        tail,
        re.M
    )

    section = tail[:nxt.start()] if nxt else tail

    vals = re.findall(
        r"^Decision:[ \t]*(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
        section,
        re.M
    )

    if vals != ["PASS"]:
        fail("AG_DECISION|" + rid)

overall = re.findall(
    r"^Overall decision:[ \t]*"
    r"(APPROVE_SCHEMA_V2_ACTIVATION_GOVERNANCE_PACKAGE|"
    r"REVISION_REQUIRED|FAIL)"
    r"[ \t]*$",
    text,
    re.M
)

if overall != [
    "APPROVE_SCHEMA_V2_ACTIVATION_GOVERNANCE_PACKAGE"
]:
    fail("OVERALL_DECISION")

if "9 PASS / 0 REVISION_REQUIRED / 0 FAIL" not in text:
    fail("FINAL_COUNTS")

record = json.loads(
    recordp.read_text(
        encoding="utf-8"
    )
)

if record["status"] != \
   "ACTIVATION_GOVERNANCE_PACKAGE_HUMAN_APPROVED_NOT_ACTIVATED":
    fail("RECORD_STATUS")

pkg = record["activation_governance_package"]

if pkg["human_approved"] is not True:
    fail("PACKAGE_APPROVAL")

if pkg["immutable"] is not True:
    fail("PACKAGE_IMMUTABILITY")

review_record = record["completed_human_review"]

if review_record["sha256"] != \
   "2b5421a0466bdec575e87f035fb303c8ed1b610bc242c14a977870b4b87d2109":
    fail("RECORD_REVIEW_SHA")

if review_record["overall_decision"] != \
   "APPROVE_SCHEMA_V2_ACTIVATION_GOVERNANCE_PACKAGE":
    fail("RECORD_OVERALL")

if review_record["final_counts"] != {
    "PASS": 9,
    "REVISION_REQUIRED": 0,
    "FAIL": 0
}:
    fail("RECORD_COUNTS")

items = record["review_item_state"]

if set(items) != {
    f"AG{i:02d}"
    for i in range(1, 10)
}:
    fail("AG_SET")

if any(
    value != "PASS"
    for value in items.values()
):
    fail("AG_NONPASS")

candidates = record["review_candidates"]

if candidates[
    "proposed_v2_hash_contract"
]["installed_at_active_path"] is not False:
    fail("ACTIVE_HASH_INSTALLED")

if candidates[
    "version_dispatch_policy"
]["active"] is not False:
    fail("DISPATCH_ACTIVE")

if candidates[
    "decision_0019_successor"
]["adopted"] is not False:
    fail("SUCCESSOR_ADOPTED")

g = record["governance_interpretation"]

if g[
    "activation_governance_package_human_approved"
] is not True:
    fail("GOV_APPROVAL")

if g[
    "all_AG01_through_AG09_pass"
] is not True:
    fail("GOV_AG_PASS")

false_fields = (
    "schema_v2_activation_authorized_by_this_record",
    "schema_v2_activated",
    "active_v2_hash_contract_created",
    "decision_0019_modified_in_place",
    "decision_0019_superseded",
    "decision_0019_successor_adopted",
    "positive_v4_to_v2_mapping_defined",
    "positive_v4_to_v2_mapping_authorized",
    "curl_json_created",
    "analyzer_implementation_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
)

for key in false_fields:
    if g[key] is not False:
        fail("NONAUTH|" + key)

if record["next_boundary"] != \
   "PREFLIGHT_SCHEMA_V2_ACTIVATION_DECISION":
    fail("NEXT_BOUNDARY")

if active_v2_hash.exists():
    fail("ACTIVE_V2_HASH_EXISTS")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("EXACT_ACTIVATION_GOVERNANCE_HUMAN_APPROVAL=PASS")
print("FINAL_ACTIVATION_GOVERNANCE_REVIEW_COUNTS=9_PASS_0_REVISION_REQUIRED_0_FAIL")
print("ACTIVATION_GOVERNANCE_PACKAGE_HUMAN_APPROVED=YES")
print("SCHEMA_V2_ACTIVATED=NO")
print("ACTIVE_V2_HASH_CONTRACT_CREATED=NO")
print("DECISION_0019_SUCCESSOR_ADOPTED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("COMPLETED_ACTIVATION_GOVERNANCE_HUMAN_APPROVAL_RECORD_VERIFICATION=PASS")
