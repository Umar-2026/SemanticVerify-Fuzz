#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

D0252_COMMIT = "1148f2264b368e97920a81cd465850a7aca85fc5"
D0252_TREE = "cd8644f2132edefb797a826936d358e8622f2085"
D0252_RECORD_SHA = "7557b89593f7462848f96836cef741e6a6c2cc90004aaf7054bc06d66ccb4bef"
D0252_VERIFIER_SHA = "04a2e2ab4761274c50c8fc1efce11a72cfdd42eaeb855e5ce2add63480f059d3"
D0252_MANIFEST_SHA = "12c87093d7daac420a79220efe471ddacbc992d60349600142f1a5ac339d02f1"

D0251_COMMIT = "7505af46bf8a7c16bbb8ba83b0a7bb81cb8e99b5"
D0251_TREE = "6b5729e8ae8281798363330c682da10bb38a84bc"
D0251_PRIMARY_SHA = "e6d027353df054ac6c31b700e15cc29a0e7b88b8a7324775d3212a7d5fb08fb5"
D0251_MANIFEST_SHA = "fd0dbb7befebe33f8969ca40d6a48d142ad8146bbb25b941f8a4560b1f1985bb"
D0251_VERIFIER_SHA = "594aea41f85bb578786abd65997db78950c385c415b51f9fb29bd8111a750061"

D0241_COMMIT = "bfc389580da261786556aa91d127ff5ac053ea2d"
D0241_TREE = "bc13dcabe70167d7f81bba4b9142a7ede0e71b4d"
D0241_RECORD_SHA = "6fd0b9de10cb0acd7c6ab81bdc25874d7cdf7b36aff5b1e24ce3c3e5b1e6202e"
D0241_SCOPE_SHA = "52bf5a39f89ee2e37478c662dbcb7732214108e73589b82f0fe6a1b5eccfdc49"
D0241_DECISION_SHA = "64ca946cc05f8b0295c7e9e6c73600f406a26885ce2d9abc12d1e2a08ea83e7c"

C3_UNIVERSE_SHA = "dbb16ce946761f76490f86ee7f72a8be3871a72f3ea3c3d25d28ffb67307d7b5"

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

D0251_PRIMARY_REL = (
    BASE
    / "d0251_c2_bounded_candidate_content_acquisition_execution_v1"
    / "01_c2_bounded_candidate_content_acquisition_execution.v1.json"
)

D0251_MANIFEST_REL = (
    BASE
    / "d0251_c2_bounded_candidate_content_acquisition_execution_v1"
    / "04_c2_bounded_candidate_content_acquisition_execution.v1.SHA256SUMS"
)

D0251_VERIFIER_REL = (
    BASE
    / "d0251_c2_bounded_candidate_content_acquisition_execution_v1"
    / "03_verify_c2_bounded_candidate_content_acquisition_execution.v1.py"
)

D0252_RECORD_REL = (
    BASE
    / "d0252_d0250_post_d0251_verifier_compatibility_corrective_successor_v1"
    / "01_d0250_post_d0251_verifier_compatibility_corrective_successor.v1.json"
)

D0252_VERIFIER_REL = (
    BASE
    / "d0252_d0250_post_d0251_verifier_compatibility_corrective_successor_v1"
    / "03_verify_d0250_post_d0251_verifier_compatibility_corrective_successor.v1.py"
)

D0252_MANIFEST_REL = (
    BASE
    / "d0252_d0250_post_d0251_verifier_compatibility_corrective_successor_v1"
    / "04_d0250_post_d0251_verifier_compatibility_corrective_successor.v1.SHA256SUMS"
)

D0241_RECORD_REL = (
    BASE
    / "d0241_carrier_admissibility_evidence_closure_design_v1"
    / "01_carrier_admissibility_evidence_closure_design.v1.json"
)

D0241_SCOPE_REL = (
    BASE
    / "d0241_carrier_admissibility_evidence_closure_design_v1"
    / "02_carrier_admissibility_evidence_closure_scope.v1.md"
)

D0241_DECISION_REL = Path(
    "documentation/decisions/"
    "0241-design-carrier-admissibility-evidence-closure-before-b2-"
    "without-execution-authorization.md"
)

PACKAGE = Path(__file__).resolve().parent
RECORD = PACKAGE / "01_c3_bounded_candidate_content_adjudication_authorization.v1.json"
SCOPE = PACKAGE / "02_c3_bounded_candidate_content_adjudication_authorization_scope.v1.md"
MANIFEST = PACKAGE / "04_c3_bounded_candidate_content_adjudication_authorization.v1.SHA256SUMS"

repo = Path(
    os.environ.get(
        "SVF_REPO_ROOT",
        "/openbayes/home/semanticverify-fuzz-research",
    )
).resolve()

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )

def no_dup(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise AssertionError("duplicate JSON key: " + key)
        out[key] = value
    return out

current_head = git("rev-parse", "HEAD").stdout.strip()

assert git(
    "merge-base",
    "--is-ancestor",
    D0252_COMMIT,
    current_head,
    check=False,
).returncode == 0

assert git(
    "rev-parse",
    f"{D0252_COMMIT}^{{tree}}",
).stdout.strip() == D0252_TREE

assert git(
    "rev-parse",
    f"{D0251_COMMIT}^{{tree}}",
).stdout.strip() == D0251_TREE

assert git(
    "rev-parse",
    f"{D0241_COMMIT}^{{tree}}",
).stdout.strip() == D0241_TREE

d0252_record = repo / D0252_RECORD_REL
d0252_verifier = repo / D0252_VERIFIER_REL
d0252_manifest = repo / D0252_MANIFEST_REL

d0251_primary = repo / D0251_PRIMARY_REL
d0251_manifest = repo / D0251_MANIFEST_REL
d0251_verifier = repo / D0251_VERIFIER_REL

d0241_record = repo / D0241_RECORD_REL
d0241_scope = repo / D0241_SCOPE_REL
d0241_decision = repo / D0241_DECISION_REL

assert sha256(d0252_record) == D0252_RECORD_SHA
assert sha256(d0252_verifier) == D0252_VERIFIER_SHA
assert sha256(d0252_manifest) == D0252_MANIFEST_SHA

assert sha256(d0251_primary) == D0251_PRIMARY_SHA
assert sha256(d0251_manifest) == D0251_MANIFEST_SHA
assert sha256(d0251_verifier) == D0251_VERIFIER_SHA

assert sha256(d0241_record) == D0241_RECORD_SHA
assert sha256(d0241_scope) == D0241_SCOPE_SHA
assert sha256(d0241_decision) == D0241_DECISION_SHA

d251 = json.loads(
    d0251_primary.read_text(encoding="utf-8")
)

rows = d251["candidate_content_snapshots"]

assert len(rows) == 10
assert [x["candidate_index"] for x in rows] == list(range(1, 11))

universe_raw = json.dumps(
    rows,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert hashlib.sha256(universe_raw).hexdigest() == C3_UNIVERSE_SHA

raw = RECORD.read_bytes()
assert not raw.endswith(b"\n")

r = json.loads(
    raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

canonical = json.dumps(
    r,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert raw == canonical

assert r["decision"] == "D0253"
assert r["status"] == "AUTHORIZED_NOT_EXECUTED"

assert r["authorization"] == {
    "authorized": True,
    "c3_authorized": True,
    "designated_execution_decision": "D0254",
    "executed": False,
    "independent_d0253_checkpoint_required_before_d0254_execution": True,
}

assert r[
    "adjudication_input_universe"
]["snapshot_record_count"] == 10

assert r[
    "adjudication_input_universe"
]["snapshot_record_universe_sha256"] == C3_UNIVERSE_SHA

assert r[
    "adjudication_input_universe"
]["snapshot_records"] == rows

assert r[
    "d0252_corrective_successor_binding"
]["commit"] == D0252_COMMIT

assert r[
    "d0251_frozen_input_binding"
]["commit"] == D0251_COMMIT

assert r[
    "d0241_c3_governance_binding"
]["commit"] == D0241_COMMIT

assert r[
    "d0241_c3_governance_binding"
]["role"] == "ADJUDICATION"

contract = r["d0254_execution_contract"]

assert contract["snapshot_count"] == 10
assert contract["snapshot_read_allowed"] is True
assert contract["original_source_blob_reopening"] is False
assert contract["original_source_blob_read_count"] == 0
assert contract["source_root_reenumeration"] is False
assert contract["repository_wide_search"] is False
assert contract["git_history_search"] is False
assert contract["external_network_access"] is False
assert contract["reference_follow_count"] == 0
assert contract["snapshot_python_execution_count"] == 0

assert r[
    "evidence_reference_policy"
]["references_must_point_only_to_current_candidate_snapshot"] is True

assert r[
    "evidence_reference_policy"
]["reference_following_allowed"] is False

for key, value in r["results_not_established"].items():
    assert value is False, key

assert r["nonauthorization"] == {
    "b2_authorized": False,
    "b2_executed": False,
    "c4_authorized": False,
    "c5_authorized": False,
    "c6_authorized": False,
    "d0254_execution_allowed_before_independent_d0253_checkpoint": False,
}

assert r["next_required_checkpoint"] == (
    "INDEPENDENT_READ_ONLY_VERIFY_D0253_BEFORE_ANY_D0254_SNAPSHOT_CONTENT_READ"
)

scope_text = SCOPE.read_text(encoding="utf-8")

for marker in (
    "D0253 itself does not execute C3",
    "does not read any D0251 snapshot content",
    "D0254 may read only the exact ten frozen D0251 snapshot outputs",
    "does not authorize C4, C5, C6, B2",
    "must not assert D0254 path absence",
):
    assert marker in scope_text, marker

manifest_lines = [
    line
    for line in MANIFEST.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

assert len(manifest_lines) == 3

expected_manifest_names = {
    RECORD.name,
    SCOPE.name,
    Path(__file__).name,
}

seen = set()

for line in manifest_lines:
    digest, name = line.split(None, 1)
    name = name.strip()
    assert name in expected_manifest_names
    assert name not in seen
    seen.add(name)
    assert sha256(PACKAGE / name) == digest

assert seen == expected_manifest_names

print("D0253_C3_ADJUDICATION_AUTHORIZATION_VERIFIER=PASS")
print("D0252_VERIFIED_FROZEN_INPUT_BINDING=PASS")
print("D0251_VERIFIED_FROZEN_METADATA_BINDING=PASS")
print("D0241_C3_GOVERNANCE_BINDING=PASS")
print("C3_FROZEN_SNAPSHOT_RECORD_COUNT=10")
print("C3_FROZEN_SNAPSHOT_RECORD_UNIVERSE_SHA256=" + C3_UNIVERSE_SHA)
print("C3_AUTHORIZED=YES")
print("C3_EXECUTED=NO")
print("D0254_DESIGNATED_EXECUTION=YES")
print("D0254_EXECUTION_ALLOWED_BEFORE_INDEPENDENT_D0253_CHECKPOINT=NO")
print("D0251_SNAPSHOT_CONTENT_READ_BY_VERIFIER=NO")
print("ORIGINAL_SOURCE_BLOB_REOPENED_BY_VERIFIER=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("SAFE_D0253_VERIFIER=PASS")
