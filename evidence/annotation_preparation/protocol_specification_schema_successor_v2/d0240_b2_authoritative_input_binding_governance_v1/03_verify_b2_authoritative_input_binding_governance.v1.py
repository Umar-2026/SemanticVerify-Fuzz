#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

EXPECTED_D0239 = "fb2be97c8adf295f53a6bb67eb0c6a8dc721098e"
EXPECTED_D0239_TREE = "7718d7a5317e93e96e3fe2631b179c44663790f0"
EXPECTED_D0239_MANIFEST = "dcaa186c7ba0178601c8227cd23c905284531cfb6757fe0db47263ba6da7ddce"

EXPECTED_MATRIX_SHA = "44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12"
EXPECTED_MATRIX_BLOB = "b50e1bb81f7eb8842c7bdc9bd5cb9df5a56ed861"
EXPECTED_MATRIX_SOURCE_COMMIT = "70437180754f8248a5cc06d0af3e59c2c343520c"

EXPECTED_RBCA_SHA = "2c9ca9125aa89dd77f7f74950f7285657fcaee7dbd17ce0dca01012ad716263c"
EXPECTED_RBCA_ADOPTION_SHA = "d133548d4c3b7eef2436faabece406b3bfb815bab12c0a5c119c84258e84169a"

EXPECTED_DOMAIN_SPEC_SHA = "1ff98f8aee27f382996810041f01176015409714e6d39fe8b8122227954613b8"
EXPECTED_INVARIANTS_SHA = "91284c99ad85ca939e3f250fe7f04faf44dd7f3cab5760852356305eecb0f580"

def die(msg):
    print("D0240_BINDING_GOVERNANCE_VERIFIER=FAIL")
    print("FAILURE=" + msg)
    sys.exit(1)

def sha256(path):
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
        repo / "documentation/decisions/0240-govern-b2-authoritative-input-bindings-without-b2-authorization.md",
    )
)

record_path = pkg / "01_b2_authoritative_input_binding_governance.v1.json"
scope_path = pkg / "02_b2_authoritative_input_binding_scope.v1.md"
manifest_path = pkg / "04_b2_authoritative_input_binding_governance.v1.SHA256SUMS"

for p in [record_path, scope_path, manifest_path, decision]:
    if not p.is_file():
        die("missing:" + str(p))

try:
    record = json.loads(record_path.read_text(encoding="utf-8"))
except Exception as exc:
    die("record-json:" + repr(exc))

canonical = json.dumps(
    record,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

if record_path.read_bytes() != canonical:
    die("record-not-canonical-json")

if record["artifact_id"] != "SVF-D0240-B2-AUTHORITATIVE-INPUT-BINDING-GOVERNANCE-V1":
    die("artifact-id")

if record["status"] != "BINDING_ONLY_GOVERNANCE_NO_B2_AUTHORIZATION":
    die("status")

pred = record["predecessor"]

if pred["commit"] != EXPECTED_D0239:
    die("d0239-commit-binding")

if pred["tree"] != EXPECTED_D0239_TREE:
    die("d0239-tree-binding")

if pred["manifest_sha256"] != EXPECTED_D0239_MANIFEST:
    die("d0239-manifest-binding")

source = record["authoritative_dual_role_source"]

if source["sha256"] != EXPECTED_MATRIX_SHA:
    die("matrix-sha-binding")

if source["git_blob"] != EXPECTED_MATRIX_BLOB:
    die("matrix-blob-binding")

if source["source_commit"] != EXPECTED_MATRIX_SOURCE_COMMIT:
    die("matrix-source-commit-binding")

u = source["projections"]["AEA01"]
c = source["projections"]["AEA02"]

if u != {
    "role": "SOURCE_UNIT_ENUMERATION",
    "identifier_field": "semantic_unit_id",
    "historical_reference_count": 109,
    "membership_semantics_redefined_by_d0240": False,
}:
    die("aea01-projection")

if c != {
    "role": "CARRIER_CANDIDATE_ENUMERATION",
    "identifier_field": "schema_v2_property_path",
    "historical_reference_count": 171,
    "membership_semantics_redefined_by_d0240": False,
    "candidate_disposition_semantics_redefined_by_d0240": False,
}:
    die("aea02-projection")

original = repo / source["source_path"]
b1 = repo / record["b1_acquired_source_copy_binding"]["path"]

if sha256(original) != EXPECTED_MATRIX_SHA:
    die("original-matrix-sha")

if sha256(b1) != EXPECTED_MATRIX_SHA:
    die("b1-matrix-sha")

if original.read_bytes() != b1.read_bytes():
    die("b1-copy-not-byte-identical")

def git_blob(commit, path):
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", f"{commit}:{path}"],
        text=True,
    ).strip()

if git_blob("HEAD", source["source_path"]) != EXPECTED_MATRIX_BLOB:
    die("current-original-blob")

if git_blob("HEAD", record["b1_acquired_source_copy_binding"]["path"]) != EXPECTED_MATRIX_BLOB:
    die("current-b1-blob")

if git_blob(EXPECTED_MATRIX_SOURCE_COMMIT, source["source_path"]) != EXPECTED_MATRIX_BLOB:
    die("historical-source-blob")

basis = record["governance_basis"]

domain_spec = repo / basis["d0222_future_accounting_domain_construction_specification"]["path"]
invariants = repo / basis["d0227_cross_artifact_machine_invariants"]["path"]
d0233 = repo / basis["d0233_authorization_design"]["path"]

if sha256(domain_spec) != EXPECTED_DOMAIN_SPEC_SHA:
    die("domain-spec-sha")

if sha256(invariants) != EXPECTED_INVARIANTS_SHA:
    die("invariants-sha")

if sha256(d0233) != basis["d0233_authorization_design"]["sha256"]:
    die("d0233-sha")

domain = json.loads(domain_spec.read_text(encoding="utf-8"))
inv = json.loads(invariants.read_text(encoding="utf-8"))
design = json.loads(d0233.read_text(encoding="utf-8"))

du = domain["AEA01_governed_source_unit_domain"]["authoritative_enumeration_source"]
dcroot = domain["AEA02_governed_schema_carrier_domain"]
dc = dcroot["authoritative_candidate_enumeration_source"]

if du["source_path"] != source["source_path"]:
    die("domain-spec-aea01-source")

if du["sha256"] != EXPECTED_MATRIX_SHA or du["git_blob"] != EXPECTED_MATRIX_BLOB:
    die("domain-spec-aea01-identity")

if du["historical_unique_semantic_unit_count"] != 109:
    die("domain-spec-aea01-count")

if dc["source_path"] != source["source_path"]:
    die("domain-spec-aea02-source")

if dc["sha256"] != EXPECTED_MATRIX_SHA or dc["git_blob"] != EXPECTED_MATRIX_BLOB:
    die("domain-spec-aea02-identity")

if dc["candidate_identifier_field"] != "schema_v2_property_path":
    die("domain-spec-aea02-field")

if dc["historical_unique_candidate_count"] != 171:
    die("domain-spec-aea02-count")

evidence = record["governing_admissibility_evidence"]

rbca = repo / evidence["carrier_admissibility_assessment"]["path"]
rbca_adoption = repo / evidence["carrier_admissibility_governance_adoption"]["path"]

if sha256(rbca) != EXPECTED_RBCA_SHA:
    die("rbca-sha")

if sha256(rbca_adoption) != EXPECTED_RBCA_ADOPTION_SHA:
    die("rbca-adoption-sha")

if evidence["carrier_admissibility_assessment"]["authoritative_candidate_enumeration_source"] is not False:
    die("rbca-promoted")

if evidence["carrier_admissibility_governance_adoption"]["authoritative_candidate_enumeration_source"] is not False:
    die("rbca-adoption-promoted")

checks = {}

def walk(v):
    if isinstance(v, dict):
        if isinstance(v.get("id"), str) and isinstance(v.get("expression"), str):
            checks[v["id"]] = v["expression"]
        for child in v.values():
            walk(child)
    elif isinstance(v, list):
        for child in v:
            walk(child)

walk(inv)

expected_ids = (
    [f"U{i:02d}" for i in range(1, 11)]
    + [f"C{i:02d}" for i in range(1, 7)]
)

if basis["d0227_cross_artifact_machine_invariants"]["bound_pre_freeze_check_ids"] != expected_ids:
    die("bound-check-id-list")

if not set(expected_ids).issubset(checks):
    die("missing-governed-check-id")

if design["design_principles"]["concrete_mapping_requires_explicit_authorization"] is not True:
    die("mapping-boundary")

if design["design_principles"]["domain_freeze_requires_explicit_authorization"] is not True:
    die("freeze-boundary")

if any(record["explicit_nonauthorization"].values()):
    die("unexpected-operational-authorization")

if any(record["substantive_results_established"].values()):
    die("unexpected-substantive-result")

if record["binding_effect"]["create_new_U_membership_semantics"] is not False:
    die("new-u-semantics")

if record["binding_effect"]["create_new_C_membership_semantics"] is not False:
    die("new-c-semantics")

if record["binding_effect"]["create_new_candidate_disposition_semantics"] is not False:
    die("new-disposition-semantics")

scope = scope_path.read_text(encoding="utf-8")
decision_text = decision.read_text(encoding="utf-8")

for marker in [
    "BINDING_ONLY_GOVERNANCE_NO_B2_AUTHORIZATION",
    "B2 authorization remains a separate future governance checkpoint.",
]:
    if marker not in scope:
        die("scope-marker:" + marker)

for marker in [
    "B2_READINESS_ESTABLISHED=NO",
    "B2_AUTHORIZED=NO",
    "B2_EXECUTION_AUTHORIZED=NO",
    "DOMAIN_FREEZE_AUTHORIZED=NO",
    "CONCRETE_MAPPING_AUTHORIZED=NO",
]:
    if marker not in decision_text:
        die("decision-marker:" + marker)

manifest_lines = [
    line
    for line in manifest_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

if len(manifest_lines) != 3:
    die("manifest-entry-count")

expected_names = {
    "01_b2_authoritative_input_binding_governance.v1.json",
    "02_b2_authoritative_input_binding_scope.v1.md",
    "03_verify_b2_authoritative_input_binding_governance.v1.py",
}

seen = set()

for line in manifest_lines:
    parts = line.split("  ", 1)

    if len(parts) != 2:
        die("manifest-format")

    expected_hash, name = parts
    target = pkg / name

    if name not in expected_names:
        die("manifest-unexpected-entry:" + name)

    if sha256(target) != expected_hash:
        die("manifest-hash:" + name)

    seen.add(name)

if seen != expected_names:
    die("manifest-coverage")

print("D0240_BINDING_GOVERNANCE_VERIFIER=PASS")
print("D0239_PREDECESSOR_BINDING=PASS")
print("AUTHORITATIVE_MATRIX_IDENTITY=PASS")
print("AEA01_PROJECTION_BINDING=PASS")
print("AEA02_CANDIDATE_PROJECTION_BINDING=PASS")
print("B1_BYTE_IDENTICAL_COPY_BINDING=PASS")
print("RBCA_EVIDENCE_ONLY_ROLE=PASS")
print("RBCA_ADOPTION_PROVENANCE_ONLY_ROLE=PASS")
print("D0227_U01_U10_C01_C06_BINDING=PASS")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("DOMAIN_FREEZE_AUTHORIZED=NO")
print("CONCRETE_MAPPING_AUTHORIZED=NO")
print("SAFE_D0240_VERIFIER=PASS")
