#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(
        p.read_bytes()
    ).hexdigest()

here = Path(__file__).resolve().parent

review = (
    here /
    "01_completed_activation_artifact_finalization_human_review.v1.md"
)

recordp = (
    here /
    "02_completed_activation_artifact_finalization_human_review_record.v1.json"
)

if sha(review) != \
   "72f5eb515529ee509140d606066c38b743cea76ad34a1272f982ef99b028e2d1":
    fail("REVIEW_SHA")

if review.stat().st_size != 6548:
    fail("REVIEW_SIZE")

record = json.loads(
    recordp.read_text(
        encoding="utf-8"
    )
)

if record["status"] != \
   "ACTIVATION_ARTIFACT_FINALIZATION_HUMAN_REVIEW_REVISION_REQUIRED_RECORDED":
    fail("RECORD_STATUS")

if record["record_only"] is not True:
    fail("NOT_RECORD_ONLY")

human = record["human_review"]

if human["sha256"] != sha(review):
    fail("RECORD_REVIEW_SHA_BINDING")

if human["size_bytes"] != review.stat().st_size:
    fail("RECORD_REVIEW_SIZE_BINDING")

expected = {
    "AF01": "PASS",
    "AF02": "PASS",
    "AF03": "PASS",
    "AF04": "REVISION_REQUIRED",
    "AF05": "PASS",
    "AF06": "PASS",
    "AF07": "REVISION_REQUIRED",
    "AF08": "REVISION_REQUIRED",
    "AF09": "REVISION_REQUIRED",
    "AF10": "PASS",
}

for key, value in expected.items():
    if human[key] != value:
        fail("RECORD_AF|" + key)

if human["pass_count"] != 6:
    fail("PASS_COUNT")

if human["revision_required_count"] != 4:
    fail("RR_COUNT")

if human["fail_count"] != 0:
    fail("FAIL_COUNT")

if human["overall_decision"] != "REVISION_REQUIRED":
    fail("OVERALL")

if human["open_items"] != [
    "AF04",
    "AF07",
    "AF08",
    "AF09"
]:
    fail("OPEN_ITEMS")

if human["reviewer_role"] != "Spec-Technical-Reviewer-1":
    fail("REVIEWER_ROLE")

if human["reviewer_name"] != "Abdul Raheem Shahzad":
    fail("REVIEWER_NAME")

if human["reviewer_confirmation"] != "ARS":
    fail("REVIEWER_CONFIRMATION")

if human["reviewer_date"] != "2026-08-21":
    fail("REVIEWER_DATE")

text = review.read_text(
    encoding="utf-8"
).replace("\r\n", "\n").replace("\r", "\n")

for key, expected_value in expected.items():
    h = re.search(
        r"^##\s+" + key + r"\b.*$",
        text,
        re.M
    )

    if not h:
        fail("REVIEW_AF_HEADING|" + key)

    tail = text[h.end():]
    nxt = re.search(r"^##\s+", tail, re.M)
    section = tail[:nxt.start()] if nxt else tail

    vals = re.findall(
        r"^Decision:[ \t]*(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
        section,
        re.M
    )

    if vals != [expected_value]:
        fail("REVIEW_AF_VALUE|" + key)

if "Overall decision: REVISION_REQUIRED" not in text:
    fail("REVIEW_OVERALL")

if "AF04, AF07, AF08, and AF09 remain open" not in text:
    fail("REVIEW_OPEN_SET")

if "Reissue the handoff with raw commit/root/tree/blob objects" not in text:
    fail("REVIEW_REMEDY")

remedy = record["reviewer_required_remedy"]

for key in (
    "evidence_only",
    "raw_git_commit_objects_required",
    "raw_git_root_tree_objects_required",
    "raw_git_nested_tree_objects_required",
    "raw_git_blob_objects_required",
    "recompute_git_object_ids_required",
    "prove_checkpoint_parent_relationship_required",
    "prove_commit_to_tree_to_path_to_blob_bindings_required",
    "prove_active_dispatch_path_absence_required",
    "prove_active_v2_hash_path_absence_required",
    "prove_curl_json_absence_required",
    "prove_core_artifact_immutability_required",
    "prove_package_only_change_scope_required",
):
    if remedy[key] is not True:
        fail("REMEDY|" + key)

if remedy["focused_rereview_items"] != [
    "AF04",
    "AF07",
    "AF08",
    "AF09"
]:
    fail("FOCUSED_REREVIEW_ITEMS")

effects = record["governance_effects"]

for key, value in effects.items():
    if value is not False:
        fail("PROHIBITED_EFFECT|" + key)

if record["next_boundary"] != \
   "AUTHOR_EVIDENCE_ONLY_CORRECTIVE_SUCCESSOR_GOVERNANCE_AUTHORIZATION_FOR_AF04_AF07_AF08_AF09":
    fail("NEXT_BOUNDARY")

print("COMPLETED_AF01_AF10_HUMAN_REVIEW_RECORD=PASS")
print("AF_PASS_COUNT=6")
print("AF_REVISION_REQUIRED_COUNT=4")
print("AF_FAIL_COUNT=0")
print("OPEN_AF_ITEMS=AF04,AF07,AF08,AF09")
print("OVERALL_HUMAN_REVIEW_DECISION=REVISION_REQUIRED")
print("REVIEWER_REQUIRED_RAW_GIT_OBJECT_EVIDENCE=YES")
print("RECORD_ONLY_NO_ACTIVATION=YES")
print("SAFE_COMPLETED_REVIEW_RECORD_VERIFIER=PASS")
