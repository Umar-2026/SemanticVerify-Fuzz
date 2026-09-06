#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

D0241_COMMIT = "bfc389580da261786556aa91d127ff5ac053ea2d"
D0241_TREE = "bc13dcabe70167d7f81bba4b9142a7ede0e71b4d"
D0241_MANIFEST_SHA = "6bb1501c6394f977fd573127e8bd5fb770d3a0e32f7645506920d21d305ffe10"

EXPECTED = {
    "C1-S01": (
        "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
        "schema_v2_requirement_to_semantic_unit_completed_human_positive_binding_evidence_record_v1/"
        "02_completed_human_positive_binding_evidence_packet.EXACT_COPY.v1.md",
        "effd2848702219741e3814d2dc283284c92ab07f49980cd799fde351ecb8b685",
        "7f0ea290e6f49c06fd7102d7b0eef5bd306697a5",
    ),
    "C1-S02": (
        "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
        "schema_v2_requirement_to_semantic_unit_bounded_technical_adjudication_completed_human_record_v1/"
        "01_returned_human_technical_adjudication.EXACT_COPY.v1.md",
        "ad35ddfefea1d79db79e36f24ef823407f977a682efcdf23a98a1cbc5ffd7eda",
        "cc14c8f9424caae4a85660c83a74491651d29c1b",
    ),
    "C1-S03": (
        "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
        "schema_v2_requirement_to_semantic_unit_bounded_supported_binding_promotion_successor_v1/"
        "01_bounded_supported_binding_successor_matrix.v1.json",
        "c74240135454c6746b0829306d60c5a818c67d06a4148116de0f21891669a940",
        "336573866fc84ab4b4379ee4f331fb448252acfb",
    ),
    "C1-S04": (
        "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
        "schema_v2_req06_req14_accounting_semantic_role_resolution_study_v1_governance_adoption_record_v1/"
        "01_bounded_role_governance_adoption_manifest.v1.json",
        "5c7b3c8dd77cd427ffd74a21f6e818daa99e4d02461635d76192ac0c2c08767e",
        "ab93158e0b44e3d4143d578040f73e34ba4eba8f",
    ),
    "C1-G01": (
        "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
        "schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser01_aser02_aser04_aser07/"
        "04_future_accounting_domain_construction_specification.v2.json",
        "1ff98f8aee27f382996810041f01176015409714e6d39fe8b8122227954613b8",
        "d4f496a4d4eb5b6c2b6c4f82e0684d7f3ffa9aba",
    ),
    "C1-G02": (
        "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
        "schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser04_aser07_remaining_findings_revision_v5/"
        "02_accounting_evidence_canonicalization_and_detached_hash_rules.v5.json",
        "8169d6e1f47b0e1bb468a48cde4edffac8792b29f660a27a46a37662edd980a8",
        "3d69ef7c70909bbb64bdb7a635389cbe210f69f0",
    ),
    "C1-G03": (
        "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
        "schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser04_aser07_remaining_findings_revision_v5/"
        "04_future_domain_freeze_lineage_and_ordering_control.v5.json",
        "ce8569431e4515712a9c0928c5b48d21591fbf56a22d7fd17b48eabf6a0e374f",
        "4a4f518eda5700a9a5fe3c132f0d0a2e2593d50c",
    ),
    "C1-G04": (
        "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
        "schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser04_aser07_remaining_findings_revision_v5/"
        "06_cross_artifact_machine_invariants.v3.json",
        "91284c99ad85ca939e3f250fe7f04faf44dd7f3cab5760852356305eecb0f580",
        "a07332028845f97f457dd9d0f99886c43a6e352f",
    ),
    "C1-G05": (
        "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
        "d0240_b2_authoritative_input_binding_governance_v1/"
        "01_b2_authoritative_input_binding_governance.v1.json",
        "41bc880c8a028301242a03440b899ed4d1aa6638a7be98813308a5a578533da8",
        "88ca3d1b06048de1025e5aafe10cc8c48faff14f",
    ),
}

def die(msg):
    print("D0242_C1_AUTHORIZATION_VERIFIER=FAIL")
    print("FAIL_REASON=" + msg)
    sys.exit(1)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

repo = Path(
    os.environ.get(
        "SVF_REPO_ROOT",
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
        ).strip(),
    )
)

pkg = Path(
    os.environ.get(
        "SVF_PACKAGE_DIR",
        Path(__file__).resolve().parent,
    )
)

decision = Path(
    os.environ.get(
        "SVF_DECISION_PATH",
        repo / "documentation/decisions/"
        "0242-authorize-c1-exact-existing-evidence-inventory-binding-without-execution.md",
    )
)

record_path = pkg / "01_c1_exact_existing_evidence_inventory_binding_authorization.v1.json"
scope_path = pkg / "02_c1_authorization_scope.v1.md"
manifest_path = pkg / "04_c1_exact_existing_evidence_inventory_binding_authorization.v1.SHA256SUMS"

for p in [record_path, scope_path, manifest_path, decision]:
    if not p.is_file():
        die("missing:" + str(p))

raw = record_path.read_bytes()

duplicates = []

def hook(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            duplicates.append(k)
        out[k] = v
    return out

try:
    r = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=hook,
    )
except Exception as exc:
    die("record-json:" + repr(exc))

if duplicates:
    die("duplicate-json-keys")

canonical = json.dumps(
    r,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

if raw != canonical:
    die("record-not-canonical-json")

if raw.endswith(b"\n"):
    die("record-final-lf")

if r["artifact_id"] != \
    "SVF-D0242-C1-EXACT-EXISTING-EVIDENCE-INVENTORY-BINDING-AUTHORIZATION-V1":
    die("artifact-id")

if r["status"] != "C1_AUTHORIZED_NOT_EXECUTED":
    die("status")

pred = r["predecessor"]

if pred["commit"] != D0241_COMMIT:
    die("d0241-commit")

if pred["tree"] != D0241_TREE:
    die("d0241-tree")

if pred["manifest_sha256"] != D0241_MANIFEST_SHA:
    die("d0241-manifest")

if pred["verified_frozen"] is not True:
    die("d0241-frozen")

actual_tree = subprocess.check_output(
    ["git", "-C", str(repo), "rev-parse", f"{D0241_COMMIT}^{{tree}}"],
    text=True,
).strip()

if actual_tree != D0241_TREE:
    die("d0241-tree-recompute")

auth = r["authorization"]

if auth["phase"] != "C1":
    die("phase")

if auth["authorized"] is not True:
    die("c1-not-authorized")

if auth["executed"] is not False:
    die("c1-executed")

if auth["designated_future_execution"] != "D0243":
    die("future-execution")

iset = r["exact_input_set"]

if iset["total_member_count"] != 9:
    die("input-count")

if iset["substantive_member_count"] != 4:
    die("substantive-count")

if iset["governance_support_member_count"] != 5:
    die("support-count")

if iset["complete_for_authorized_C1_scope"] is not True:
    die("input-complete")

if iset["source_expansion_allowed"] is not False:
    die("source-expansion")

members = iset["members"]

if len(members) != 9:
    die("member-array-count")

seen_ids = set()
seen_paths = set()

for m in members:
    mid = m["member_id"]

    if mid not in EXPECTED:
        die("unexpected-member:" + mid)

    if mid in seen_ids:
        die("duplicate-member-id:" + mid)

    p, expected_sha, expected_blob = EXPECTED[mid]

    if m["path"] != p:
        die("path:" + mid)

    if m["sha256"] != expected_sha:
        die("declared-sha:" + mid)

    if m["git_blob"] != expected_blob:
        die("declared-blob:" + mid)

    fp = repo / p

    if sha(fp) != expected_sha:
        die("actual-sha:" + mid)

    blob = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD:" + p],
        text=True,
    ).strip()

    if blob != expected_blob:
        die("actual-blob:" + mid)

    seen_ids.add(mid)
    seen_paths.add(p)

if seen_ids != set(EXPECTED):
    die("member-id-coverage")

if len(seen_paths) != 9:
    die("member-path-uniqueness")

ops = r["authorized_operations"]

if not all(value is True for value in ops.values()):
    die("authorized-operation-set")

sem = r["semantic_limits"]

if any(value is not False for value in sem.values()):
    die("semantic-limit")

nonauth = r["explicit_nonauthorization"]

if any(value is not False for value in nonauth.values()):
    die("nonauthorization")

results = r["results_not_established_by_authorization"]

if any(value is not False for value in results.values()):
    die("results-state")

if len(r["explicit_exclusions"]) != 12:
    die("exclusion-count")

if r["next_required_checkpoint"] != \
    "INDEPENDENT_READ_ONLY_VERIFY_D0242_BEFORE_ANY_D0243_C1_EXECUTION":
    die("next-checkpoint")

scope = scope_path.read_text(encoding="utf-8")
decision_text = decision.read_text(encoding="utf-8")

for marker in [
    "C1_AUTHORIZED_NOT_EXECUTED",
    "`SUPPORTED_BINDING` does not imply `INCLUDED`.",
    "`UNRESOLVED_BINDING` does not imply `EXCLUDED`.",
    "`C2_AUTHORIZED=NO`",
    "`B2_READINESS_ESTABLISHED=NO`",
    "`B2_EXECUTION_AUTHORIZED=NO`",
]:
    if marker not in scope:
        die("scope-marker:" + marker)

for marker in [
    "`C1_AUTHORIZED=YES`",
    "`C1_EXECUTED=NO`",
    "`C2_AUTHORIZED=NO`",
    "`B2_AUTHORIZED=NO`",
    "`B2_EXECUTED=NO`",
]:
    if marker not in decision_text:
        die("decision-marker:" + marker)

manifest_lines = [
    x
    for x in manifest_path.read_text(encoding="utf-8").splitlines()
    if x.strip()
]

if len(manifest_lines) != 3:
    die("manifest-count")

expected_manifest_names = {
    "01_c1_exact_existing_evidence_inventory_binding_authorization.v1.json",
    "02_c1_authorization_scope.v1.md",
    "03_verify_c1_exact_existing_evidence_inventory_binding_authorization.v1.py",
}

seen = set()

for line in manifest_lines:
    parts = line.split("  ", 1)

    if len(parts) != 2:
        die("manifest-format")

    expected_hash, name = parts

    if name not in expected_manifest_names:
        die("manifest-name:" + name)

    if sha(pkg / name) != expected_hash:
        die("manifest-hash:" + name)

    seen.add(name)

if seen != expected_manifest_names:
    die("manifest-coverage")

print("D0242_C1_AUTHORIZATION_VERIFIER=PASS")
print("D0241_PREDECESSOR_BINDING=PASS")
print("C1_EXACT_INPUT_MEMBER_COUNT=9")
print("C1_SUBSTANTIVE_MEMBER_COUNT=4")
print("C1_GOVERNANCE_SUPPORT_MEMBER_COUNT=5")
print("C1_EXACT_INPUT_IDENTITIES=PASS")
print("C1_SOURCE_EXPANSION_ALLOWED=NO")
print("C1_AUTHORIZED=YES")
print("C1_EXECUTED=NO")
print("C2_AUTHORIZED=NO")
print("C3_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("SAFE_D0242_VERIFIER=PASS")
