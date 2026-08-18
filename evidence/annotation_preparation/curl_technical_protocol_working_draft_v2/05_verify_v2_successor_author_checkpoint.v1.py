#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


here = Path(__file__).resolve().parent

repo = here
while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

if not (repo / ".git").exists():
    fail("REPOSITORY_ROOT_NOT_FOUND")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


V1_SHA = "80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6"
V2_SHA = "63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31"
REVIEW_SHA = "e253340d540a06cd24af501c569154869ac0324d677995b7266349ba097973cc"

v1 = repo / "config/annotation/curl_technical_protocol_working_draft.v1.json"
v2 = repo / "config/annotation/curl_technical_protocol_working_draft.v2.json"

review = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v1/"
      "completed_human_review_v1/"
      "01_completed_human_technical_review.v1.md"
)

resolution = here / "04_v2_successor_author_resolution.v1.json"

decision = (
    repo
    / "documentation/decisions/"
      "0030-curl-technical-working-draft-v2-successor-author-checkpoint.md"
)

if sha(v1) != V1_SHA:
    fail("V1_SHA256")

if sha(v2) != V2_SHA:
    fail("V2_SHA256")

if sha(review) != REVIEW_SHA:
    fail("HUMAN_REVIEW_SHA256")

data = json.loads(v2.read_text(encoding="utf-8"))

expected_api = {
    "curl_global_init",
    "curl_global_cleanup",
    "curl_easy_init",
    "curl_easy_setopt",
    "curl_easy_perform",
    "curl_easy_reset",
    "curl_easy_cleanup",
    "curl_multi_init",
    "curl_multi_add_handle",
    "curl_multi_perform",
    "curl_multi_remove_handle",
    "curl_multi_cleanup",
}

if len(data["api_surface"]) != 12:
    fail("API_SURFACE_COUNT")

if set(data["api_surface"]) != expected_api:
    fail("API_SURFACE_SET")


def rule(rules, rid):
    vals = [
        r for r in rules
        if isinstance(r, dict)
        and r.get("rule_id") == rid
    ]
    if len(vals) != 1:
        fail("RULE_ID_COUNT|" + rid + "|" + str(len(vals)))
    return vals[0]


# TS-RR09
g10 = rule(data["global_runtime_rules"], "G10")
if (
    g10.get("defect") != "D5"
    or g10.get("verdict") != "VIOLATION-MUST"
    or g10.get("enforcement") != "MUST"
):
    fail("TS_RR09_G10")

# TS-RR11
m08 = rule(data["multi_handle_rules"], "M08")
if (
    m08.get("defect") != "D6"
    or m08.get("verdict") != "VIOLATION-MUST"
):
    fail("TS_RR11_M08")

# TS-RR13
m11 = rule(data["multi_handle_rules"], "M11")
if (
    m11.get("defect") != "D7"
    or m11.get("verdict") != "VIOLATION-MUST"
):
    fail("TS_RR13_M11")

if "actual original multi" not in m11.get("effect", ""):
    fail("TS_RR13_MEMBERSHIP_PRESERVATION")

# TS-RR14
x02 = rule(data["cross_resource_rules"], "X02")
if (
    x02.get("defect") != "D8"
    or x02.get("verdict") != "VIOLATION-MUST"
):
    fail("TS_RR14_X02")

# TS-RR05/06/10
m12 = rule(data["multi_handle_rules"], "M12")
m13 = rule(data["multi_handle_rules"], "M13")
m24 = rule(data["multi_handle_rules"], "M24")

if "CURLM_OK" not in m12.get("condition", ""):
    fail("TS_RR05_M12_RETURN_CONDITION")

if "CURLM_OK" not in m13.get("condition", ""):
    fail("TS_RR10_M13_RETURN_CONDITION")

if m13.get("enforcement") != "NON_ENFORCEABLE_RECOMMENDATION":
    fail("TS_RR10_RECOMMENDATION")

if m13.get("verdict") != "VALID":
    fail("TS_RR10_BASE_VERDICT")

if "non-CURLM_OK" not in m24.get("condition", ""):
    fail("TS_RR05_FAILED_CLEANUP_RULE")

if "outstanding" not in m24.get("effect", ""):
    fail("TS_RR05_FAILED_CLEANUP_OBLIGATION")

# TS-RR11 recovery
m25 = rule(data["multi_handle_rules"], "M25")
if "successfully removed" not in m25.get("condition", ""):
    fail("TS_RR11_RECOVERY_REMOVE_ALL")

if "successfully re-added" not in m25.get("condition", ""):
    fail("TS_RR11_RECOVERY_READD")

# TS-RR08 D1/D2/D4
for rid, defect in (
    ("E14", "D1"),
    ("E15", "D1"),
    ("E16", "D1"),
    ("E17", "D2"),
    ("E18", "D2"),
    ("E19", "D2"),
    ("E21", "D4"),
    ("M16", "D1"),
    ("M17", "D1"),
    ("M18", "D1"),
    ("M19", "D2"),
    ("M20", "D2"),
    ("M21", "D2"),
    ("M23", "D4"),
):
    collection = (
        data["easy_handle_rules"]
        if rid.startswith("E")
        else data["multi_handle_rules"]
    )
    r = rule(collection, rid)
    if r.get("defect") != defect:
        fail("TS_RR08_DEFECT|" + rid)

    if r.get("verdict") != "VIOLATION-MUST":
        fail("TS_RR08_VERDICT|" + rid)

# NULL cleanup exceptions
e20 = rule(data["easy_handle_rules"], "E20")
if e20.get("verdict") != "VALID":
    fail("TS_RR08_EASY_CLEANUP_NULL")

m22 = rule(data["multi_handle_rules"], "M22")
if m22.get("return") != "CURLM_BAD_HANDLE":
    fail("TS_RR08_MULTI_CLEANUP_NULL_RETURN")

if "no cleanup obligation is discharged" not in m22.get("effect", ""):
    fail("TS_RR08_MULTI_CLEANUP_NULL_EFFECT")

# TS-RR12: old blanket field forbidden.
def walk(obj, path="$"):
    if isinstance(obj, dict):
        for k, value in obj.items():
            np = path + "." + k

            if k == "verdict_if_future_reasoning_depends_on_exact_runtime_state":
                fail("TS_RR12_OLD_BLANKET_FIELD|" + np)

            if k in {"verdict", "missing_cleanup_verdict"}:
                if value not in {
                    "VALID",
                    "VIOLATION-MUST",
                    "VIOLATION-MAY",
                    "UNKNOWN",
                }:
                    fail(
                        "TS_RR07_NONSTANDARD_VERDICT|"
                        + np + "|" + repr(value)
                    )

            walk(value, np)

    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            walk(value, f"{path}[{i}]")

walk(data)

join = data["verdict_semantics"].get("feasible_state_join_policy", {})

if join.get("mixed_VALID_and_enforceable_violation") != "VIOLATION-MAY":
    fail("TS_RR12_JOIN_POLICY")

if data.get("open_independent_review_items") != []:
    fail("OLD_OPEN_REVIEW_ITEMS_REMAIN")

resolved = data.get("resolved_independent_review_items", [])

if len(resolved) != 6:
    fail("RESOLVED_NR_COUNT|" + str(len(resolved)))

if {
    x.get("review_item")
    for x in resolved
} != {
    "NR01",
    "NR02",
    "NR03",
    "NR04",
    "NR05",
    "NR06",
}:
    fail("RESOLVED_NR_SET")

policy = data["return_condition_policy"].get("curl_multi_cleanup")

if not isinstance(policy, dict):
    fail("MULTI_CLEANUP_RETURN_POLICY_MISSING")

if policy.get("success_condition") != "return == CURLM_OK":
    fail("MULTI_CLEANUP_SUCCESS_POLICY")

if policy.get("failure_condition") != "return != CURLM_OK":
    fail("MULTI_CLEANUP_FAILURE_POLICY")

resolution_record = json.loads(
    resolution.read_text(encoding="utf-8")
)

if resolution_record["successor"]["sha256"] != V2_SHA:
    fail("RESOLUTION_RECORD_V2_SHA")

blocked = resolution_record["authorization_state"]

for key in (
    "canonical_curl_specification_authorized",
    "generated_driver_inspection_authorized",
    "selected_sample_membership_inspection_authorized",
    "gold_annotation_authorized",
    "analyzer_implementation_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
):
    if blocked[key] is not False:
        fail("BLOCKED_BOUNDARY_CHANGED|" + key)

if not decision.is_file():
    fail("DECISION_0030_MISSING")

dtext = decision.read_text(encoding="utf-8")

for required in (
    V1_SHA,
    V2_SHA,
    REVIEW_SHA,
    "BUILD_CURL_TECHNICAL_WORKING_DRAFT_V2_INDEPENDENT_REVIEW_PACKAGE",
):
    if required not in dtext:
        fail("DECISION_0030_BINDING|" + required)

print("V1_IMMUTABILITY_SHA256=PASS")
print("V2_SUCCESSOR_SHA256=PASS")
print("EXACT_TWELVE_FUNCTION_API_SURFACE=PASS")
print("TS_RR05_RETURN_CONDITIONED_CLEANUP=PASS")
print("TS_RR06_POST_ERROR_CLEANUP=PASS")
print("TS_RR07_FOUR_VERDICT_CONTRACT=PASS")
print("TS_RR08_D1_D2_D4_AND_NULL_CASES=PASS")
print("TS_RR09_EXPLICIT_GLOBAL_EXIT_D5=PASS")
print("TS_RR10_NON_ENFORCEABLE_CLEANUP_RECOMMENDATION=PASS")
print("TS_RR11_POST_ERROR_D6_AND_RECOVERY=PASS")
print("TS_RR12_SET_VALUED_STATE_JOIN=PASS")
print("TS_RR13_WRONG_MULTI_D7=PASS")
print("TS_RR14_PREMATURE_GLOBAL_CLEANUP_D8=PASS")
print("NR01_TO_NR06_RESOLVED_IN_SUCCESSOR=PASS")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_TECHNICAL_WORKING_DRAFT_V2_AUTHOR_CHECKPOINT_VERIFICATION=PASS")
