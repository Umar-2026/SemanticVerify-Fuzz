#!/usr/bin/env python3

from pathlib import Path
import json
import subprocess

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

EXPECTED_PARENT = (
    "8fe5a8937d14d5ed645a14af0c634ff8fe8b90ad"
)

ROOT = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
)

AUTH = (
    ROOT
    + "schema_v2_req06_req14_accounting_satisfaction_"
    + "evidence_gap_and_acquisition_specification_study_v1_"
    + "corrective_successor_authorization_v1/"
)

A01 = AUTH + "01_bounded_corrective_study_successor_authorization.v1.json"
A02 = AUTH + "02_authorize_bounded_corrective_study_successor_once.v1.py"
A03 = AUTH + "03_bounded_corrective_scope_contract.v1.json"
A04 = AUTH + "04_bounded_corrective_successor_authorization_boundary.v1.md"

DEC = (
    "documentation/decisions/"
    "0212-authorize-bounded-corrective-study-successor-for-"
    "aser01-aser02-aser04-aser07.md"
)

EXPECTED_CHANGED = sorted([
    A01,
    A02,
    A03,
    A04,
    DEC,
])


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


head = subprocess.check_output(
    ["git", "-C", str(REPO), "rev-parse", "HEAD"],
    text=True
).strip()

parent = subprocess.check_output(
    ["git", "-C", str(REPO), "rev-parse", "HEAD^"],
    text=True
).strip()

if parent != EXPECTED_PARENT:
    stop("D0212_PARENT_INVALID", parent)

status = subprocess.check_output(
    [
        "git", "-C", str(REPO),
        "status", "--porcelain=v1",
        "--untracked-files=all"
    ],
    text=True
)

if status.strip():
    stop("REPOSITORY_NOT_CLEAN")

changed = subprocess.check_output(
    [
        "git", "-C", str(REPO),
        "diff-tree", "--no-commit-id",
        "--name-only", "-r", "HEAD"
    ],
    text=True
).splitlines()

if sorted(changed) != EXPECTED_CHANGED:
    stop("D0212_COMMIT_SCOPE_INVALID")

for rel in (A01, A03, A04, DEC):
    if not (REPO / rel).is_file():
        stop("D0212_ARTIFACT_MISSING", rel)

authorization = json.loads(
    (REPO / A01).read_text(encoding="utf-8")
)

contract = json.loads(
    (REPO / A03).read_text(encoding="utf-8")
)

if authorization["decision"] != "0212":
    stop("AUTHORIZATION_DECISION_INVALID")

if authorization["authorization_status"] != (
    "AUTHORIZED_TO_AUTHOR_BOUNDED_CORRECTIVE_STUDY_SUCCESSOR_ONLY"
):
    stop("AUTHORIZATION_STATUS_INVALID")

scope = authorization["corrective_scope"]

if scope["revision_required_items"] != [
    "ASER01",
    "ASER02",
    "ASER04",
    "ASER07",
]:
    stop("CORRECTIVE_ITEM_SCOPE_INVALID")

if scope["preserved_pass_items"] != [
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]:
    stop("PRESERVED_PASS_ITEMS_INVALID")

constraints = authorization["corrective_constraints"]

required_true = [
    "use_existing_committed_evidence_only_for_provenance_and_substantive_copying",
    "no_new_accounting_evidence_acquisition",
    "no_actual_governed_source_unit_domain_acquisition",
    "no_actual_governed_schema_carrier_domain_acquisition",
    "no_forward_witness_acquisition",
    "no_reverse_witness_acquisition",
    "no_concrete_source_unit_to_schema_carrier_mapping",
    "no_accounting_satisfaction_evaluation",
    "no_pair_reclassification",
    "original_d0203_artifacts_must_not_be_edited_in_place",
    "returned_human_review_must_not_be_edited_in_place",
    "corrective_successor_must_be_new_artifacts",
]

for key in required_true:
    if constraints.get(key) is not True:
        stop("CORRECTIVE_CONSTRAINT_INVALID", key)

non = authorization["explicit_nonauthorization"]

for key, value in non.items():
    if value is not False:
        stop("NONAUTHORIZATION_INVALID", key)

if contract["corrective_items"] != [
    "ASER01",
    "ASER02",
    "ASER04",
    "ASER07",
]:
    stop("CONTRACT_CORRECTIVE_ITEMS_INVALID")

if contract["review_lifecycle"]["successor_status_after_authoring"] != (
    "AUTHOR_CANDIDATE"
):
    stop("SUCCESSOR_STATUS_INVALID")

if contract["review_lifecycle"][
    "independent_human_rereview_required"
] is not True:
    stop("REREVIEW_REQUIREMENT_INVALID")

print(
    "DECISION0212_BOUNDED_CORRECTIVE_STUDY_SUCCESSOR_AUTHORIZATION_VERIFIER=PASS"
)

print("AUTHORIZATION_COMMIT=" + head)
print("AUTHORIZATION_PARENT=" + parent)

print("CORRECTIVE_ITEMS=ASER01,ASER02,ASER04,ASER07")
print("PRESERVED_PASS_ITEMS=ASER03,ASER05,ASER06,ASER08,ASER09")

print("CORRECTIVE_SUCCESSOR_AUTHORING_AUTHORIZED=YES")
print("CORRECTIVE_SUCCESSOR_AUTHORED_BY_THIS_VERIFIER=NO")
print("SUCCESSOR_STATUS_IF_AUTHORED=AUTHOR_CANDIDATE")

print("PORTABLE_D0203_PROVENANCE_AUTHORING_AUTHORIZED=YES")
print("EXISTING_FIXED_EVIDENCE_EXACT_COPY_PACKAGING_AUTHORIZED=YES")
print("DOMAIN_ENUMERATION_RULE_AUTHORING_AUTHORIZED=YES")
print("FORMAL_AEA_SCHEMA_AUTHORING_AUTHORIZED=YES")
print("CANONICALIZATION_RULE_AUTHORING_AUTHORIZED=YES")
print("FLAG_BEARING_SCHEMA_BINDING_AUTHORING_AUTHORIZED=YES")
print("FREEZE_AND_LINEAGE_CONTROL_AUTHORING_AUTHORIZED=YES")

print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("ACTUAL_DOMAIN_ACQUISITION_AUTHORIZED=NO")
print("FORWARD_WITNESS_ACQUISITION_AUTHORIZED=NO")
print("REVERSE_WITNESS_ACQUISITION_AUTHORIZED=NO")
print("CONCRETE_MAPPING_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")

print("STUDY_GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("INDEPENDENT_REREVIEW_REQUIRED=YES")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("AUTHORIZATION_EXECUTION_ATTEMPT_COUNT_FOR_THIS_RUN=1")
print("AUTHORIZATION_RERUN_AFTER_FIRST_ATTEMPT_AUTHORIZED=NO")
