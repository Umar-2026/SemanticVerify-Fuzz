#!/usr/bin/env python3

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

DRAFT = (
    REPO /
    "config/annotation/"
    "curl_technical_protocol_working_draft.v1.json"
)

V3 = (
    REPO /
    "config/annotation/"
    "curl_v3_authoring_scope.v3.json"
)

D26 = (
    REPO /
    "documentation/decisions/"
    "0026-curl-v3-post-freeze-technical-working-draft-authorization.md"
)

D27 = (
    REPO /
    "documentation/decisions/"
    "0027-curl-technical-protocol-working-draft-v1-author-checkpoint.md"
)

MAP = HERE / "01_source_evidence_map.v1.json"
NOTES = HERE / "02_author_review_notes.v1.md"

V3_SHA = "ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb"
D26_SHA = "6d4d9e19074834cfbbacb5125f9a11e7f13651693e70333120ad6c13525f36c1"

EXPECTED_APIS = {
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


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


if sha(V3) != V3_SHA:
    fail("FROZEN_V3_SHA")

if sha(D26) != D26_SHA:
    fail("DECISION_0026_SHA")

d = json.loads(DRAFT.read_text(encoding="utf-8"))

if d.get("status") != "WORKING_DRAFT_NOT_CANONICAL":
    fail("DRAFT_STATUS")

apis = d.get("api_surface", [])

if len(apis) != 12:
    fail("API_COUNT")

if set(apis) != EXPECTED_APIS:
    fail("API_SURFACE")

if len(apis) != len(set(apis)):
    fail("DUPLICATE_API")

g = d.get("governance", {})

required_true = {
    "technical_working_draft_authorized",
    "independent_technical_review_required",
}

for key in required_true:
    if g.get(key) is not True:
        fail("GOVERNANCE_TRUE|" + key)

required_false = {
    "canonical_specification_authorized",
    "generated_driver_inspection_authorized",
    "gold_annotation_authorized",
    "analyzer_implementation_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
}

for key in required_false:
    if g.get(key) is not False:
        fail("GOVERNANCE_FALSE|" + key)

verdicts = d.get("verdict_semantics", {})

if set(verdicts) != {
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN",
}:
    fail("VERDICT_SET")

if d.get(
    "representation_policy", {}
).get("unknown_must_never_be_converted_to_valid") is not True:
    fail("UNKNOWN_DISCIPLINE")

resources = d.get("resources", {})

for required in (
    "GLOBAL_RUNTIME_REFERENCE_STATE",
    "EXPLICIT_GLOBAL_CLEANUP_OBLIGATION",
    "EASY_HANDLE",
    "MULTI_HANDLE",
    "EASY_MULTI_MEMBERSHIP",
):
    if required not in resources:
        fail("RESOURCE_MODEL_MISSING|" + required)

multi_states = set(
    resources["MULTI_HANDLE"].get("states", [])
)

if "MULTI_OWNED_POST_ERROR_UNCERTAIN" not in multi_states:
    fail("POST_ERROR_MULTI_STATE")

rules = []

for section in (
    "global_runtime_rules",
    "easy_handle_rules",
    "multi_handle_rules",
    "cross_resource_rules",
):
    rules.extend(d.get(section, []))

rule_ids = [x.get("rule_id") for x in rules]

if len(rule_ids) != len(set(rule_ids)):
    fail("DUPLICATE_RULE_ID")

required_rules = {
    "G01", "G02", "G03", "G04", "G05", "G06",
    "G07", "G08", "G09", "G10",
    "E01", "E02", "E03", "E04", "E05", "E06",
    "E07", "E08", "E09", "E10", "E11", "E12", "E13",
    "M01", "M02", "M03", "M04", "M05", "M06",
    "M07", "M08", "M09", "M10", "M11", "M12",
    "M13", "M14", "M15",
    "X01", "X02", "X03", "X04",
}

if set(rule_ids) != required_rules:
    fail("RULE_SET")

review_items = d.get("open_independent_review_items", [])

review_ids = {x.get("id") for x in review_items}

if review_ids != {
    "NR01", "NR02", "NR03", "NR04", "NR05", "NR06"
}:
    fail("REVIEW_ITEM_SET")

# Critical non-strengthening assertions.
rule_by_id = {x["rule_id"]: x for x in rules}

if rule_by_id["G10"].get("verdict") != "UNKNOWN":
    fail("NR01_SILENTLY_STRENGTHENED")

if rule_by_id["M13"].get("verdict") != "UNKNOWN":
    fail("NR02_SILENTLY_STRENGTHENED")

if rule_by_id["M08"].get("verdict") != "UNKNOWN":
    fail("NR03_SILENTLY_STRENGTHENED")

if rule_by_id["E07"].get("verdict") != "VIOLATION-MUST":
    fail("ATTACHED_EASY_PERFORM_RULE")

if rule_by_id["E11"].get("verdict") != "VIOLATION-MUST":
    fail("ATTACHED_EASY_CLEANUP_RULE")

if rule_by_id["M07"].get("effect") != \
        "multi becomes MULTI_OWNED_POST_ERROR_UNCERTAIN":
    fail("MULTI_ERROR_TRANSITION")

m = json.loads(MAP.read_text(encoding="utf-8"))

if m.get("prohibited_evidence_used") is not False:
    fail("PROHIBITED_EVIDENCE")

if m.get("working_draft", {}).get("sha256") != sha(DRAFT):
    fail("EVIDENCE_MAP_DRAFT_BINDING")

if "not the canonical `curl.json`" not in \
        NOTES.read_text(encoding="utf-8"):
    fail("AUTHOR_NOTE_CANONICAL_BOUNDARY")

d27_text = D27.read_text(encoding="utf-8")

if sha(DRAFT) not in d27_text:
    fail("DECISION_0027_DRAFT_BINDING")

print("EXACT_12_FUNCTION_SURFACE=PASS")
print("RESOURCE_MODEL_SET=PASS")
print("RETURN_CONDITIONED_TRANSITIONS=PASS")
print("GLOBAL_RUNTIME_VS_CLEANUP_OBLIGATION_SEPARATION=PASS")
print("EASY_MULTI_MEMBERSHIP_MODEL=PASS")
print("MULTI_POST_ERROR_UNCERTAINTY=PASS")
print("UNKNOWN_VERDICT_DISCIPLINE=PASS")
print("UNRESOLVED_NORMATIVE_ITEMS_NOT_SILENTLY_STRENGTHENED=PASS")
print("SOURCE_EVIDENCE_MAP_BINDING=PASS")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_TECHNICAL_WORKING_DRAFT_V1_VERIFICATION=PASS")
