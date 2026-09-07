#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

D0254_COMMIT = "5cfbbe57ad4fa5c00174137dd19d003be737d29c"
D0254_TREE = "6e1abfc1bfdb1a405b7e6594c4b77a395387cb19"
D0254_PRIMARY_SHA = "8ee9bf4b84412d1bddf86da60aa2e947e5b7c44ac9d2dfe1d539af126023f3d0"
D0254_SCOPE_SHA = "83d15ed0781884f100e083b605fec7957dc92e9c81b8f92ff551072ea7c08b50"
D0254_VERIFIER_SHA = "f2ef7c9dcd18fdc42157a11a4e25d674c54d38875215840af31722a51829c058"
D0254_MANIFEST_SHA = "320a752cc37e7285215ad9f0c0269440277f70105825634c647378334ab82e1c"
D0254_DECISION_SHA = "17951397d4bbcd6673660a457e322769aae3140fc949d8100f2c2fc8ae529d5b"

D0253_COMMIT = "7057c8a655229f2265ea120a1d6945d5afe092fc"
D0253_TREE = "68c1146eacd370238b249352b93efd20502f0e5f"
D0253_RECORD_SHA = "70cf66d89d3c1903be69586396764db68c378fc584447d0d2370556625e61199"

D0251_COMMIT = "7505af46bf8a7c16bbb8ba83b0a7bb81cb8e99b5"
D0251_TREE = "6b5729e8ae8281798363330c682da10bb38a84bc"
D0251_PRIMARY_SHA = "e6d027353df054ac6c31b700e15cc29a0e7b88b8a7324775d3212a7d5fb08fb5"

FULL_C3_UNIVERSE_SHA = "dbb16ce946761f76490f86ee7f72a8be3871a72f3ea3c3d25d28ffb67307d7b5"
SHARED_SEVEN_FIELD_PROJECTION_SHA = "fe0ba4023b8f9dd9bfbf00b4056717229de4f420d6311053f9864e21b729206e"
EVIDENCE_LOCATOR_UNIVERSE_SHA = "a0e326368d63c350c1d18f0f8e8988047f9731079c330d71dcd814f7e102df97"

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

D0251_PRIMARY = (
    BASE
    / "d0251_c2_bounded_candidate_content_acquisition_execution_v1"
    / "01_c2_bounded_candidate_content_acquisition_execution.v1.json"
)

D0253_RECORD = (
    BASE
    / "d0253_c3_bounded_candidate_content_adjudication_authorization_v1"
    / "01_c3_bounded_candidate_content_adjudication_authorization.v1.json"
)

D0254_PKG = BASE / "d0254_c3_bounded_candidate_content_adjudication_execution_v1"
D0254_PRIMARY = D0254_PKG / "01_c3_bounded_candidate_content_adjudication_execution.v1.json"
D0254_SCOPE = D0254_PKG / "02_c3_bounded_candidate_content_adjudication_execution_scope.v1.md"
D0254_VERIFIER = D0254_PKG / "03_verify_c3_bounded_candidate_content_adjudication_execution.v1.py"
D0254_MANIFEST = D0254_PKG / "04_c3_bounded_candidate_content_adjudication_execution.v1.SHA256SUMS"
D0254_DECISION = Path(
    "documentation/decisions/"
    "0254-execute-c3-bounded-candidate-content-adjudication-from-frozen-d0251-snapshots.md"
)

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical(obj) -> bytes:
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

def git(repo: Path, *args: str) -> str:
    cp = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return cp.stdout.strip()

def main() -> int:
    repo = Path(os.environ["SVF_REPO_ROOT"]).resolve()
    package = Path(__file__).resolve().parent

    head = git(repo, "rev-parse", "HEAD")

    assert git(repo, "rev-parse", f"{D0254_COMMIT}^{{tree}}") == D0254_TREE
    assert git(repo, "rev-parse", f"{D0253_COMMIT}^{{tree}}") == D0253_TREE
    assert git(repo, "rev-parse", f"{D0251_COMMIT}^{{tree}}") == D0251_TREE

    for ancestor in (D0254_COMMIT, D0253_COMMIT, D0251_COMMIT):
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, head],
            cwd=repo,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    assert sha256(repo / D0251_PRIMARY) == D0251_PRIMARY_SHA
    assert sha256(repo / D0253_RECORD) == D0253_RECORD_SHA

    assert sha256(repo / D0254_PRIMARY) == D0254_PRIMARY_SHA
    assert sha256(repo / D0254_SCOPE) == D0254_SCOPE_SHA
    assert sha256(repo / D0254_VERIFIER) == D0254_VERIFIER_SHA
    assert sha256(repo / D0254_MANIFEST) == D0254_MANIFEST_SHA
    assert sha256(repo / D0254_DECISION) == D0254_DECISION_SHA

    d251 = json.loads(
        (repo / D0251_PRIMARY).read_text(encoding="utf-8")
    )
    d253 = json.loads(
        (repo / D0253_RECORD).read_text(encoding="utf-8")
    )
    d254 = json.loads(
        (repo / D0254_PRIMARY).read_text(encoding="utf-8")
    )

    source_rows = d251["candidate_content_snapshots"]
    auth_rows = d253["adjudication_input_universe"]["snapshot_records"]
    adjs = d254["candidate_adjudications"]

    assert len(source_rows) == 10
    assert len(auth_rows) == 10
    assert len(adjs) == 10
    assert source_rows == auth_rows

    assert hashlib.sha256(canonical(source_rows)).hexdigest() == FULL_C3_UNIVERSE_SHA

    fields = [
        "candidate_index",
        "root_id",
        "source_locator",
        "snapshot_path",
        "snapshot_sha256",
        "snapshot_byte_count",
        "snapshot_git_blob_oid",
    ]

    source_projection = [
        {k: row[k] for k in fields}
        for row in source_rows
    ]
    d254_projection = [
        {k: row[k] for k in fields}
        for row in adjs
    ]

    assert source_projection == d254_projection

    projection_sha = hashlib.sha256(
        canonical(source_projection)
    ).hexdigest()

    assert projection_sha == SHARED_SEVEN_FIELD_PROJECTION_SHA
    assert projection_sha != FULL_C3_UNIVERSE_SHA

    refs = []
    for row in adjs:
        for ordinal, ref in enumerate(
            row["evidence_references"],
            start=1,
        ):
            refs.append({
                "candidate_index": row["candidate_index"],
                "evidence_ordinal": ordinal,
                "evidence_purpose": ref["evidence_purpose"],
                "locator_kind": ref["locator_kind"],
                "locator_value": ref["locator_value"],
                "snapshot_path": row["snapshot_path"],
            })

    assert len(refs) == 24
    assert all(x["locator_kind"] == "LINE_RANGE" for x in refs)
    assert (
        hashlib.sha256(canonical(refs)).hexdigest()
        == EVIDENCE_LOCATOR_UNIVERSE_SHA
    )

    record_path = (
        package
        / "01_d0254_full_freeze_snapshot_revalidation_authorization.v1.json"
    )
    raw = record_path.read_bytes()

    def no_dup(pairs):
        out = {}
        for k, v in pairs:
            assert k not in out, k
            out[k] = v
        return out

    record = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=no_dup,
    )

    assert raw == canonical(record)
    assert not raw.endswith(b"\n")

    assert record["authorization_id"] == (
        "D0255-D0254-FULL-FREEZE-SNAPSHOT-REVALIDATION-AUTHORIZATION-V1"
    )
    assert record["authorization_role"] == (
        "D0254_FULL_FREEZE_SNAPSHOT_REVALIDATION_AUTHORIZATION_ONLY"
    )

    binding = record["authorization_binding"]
    assert binding["parent_d0254_commit"] == D0254_COMMIT
    assert binding["parent_d0254_tree"] == D0254_TREE
    assert binding["d0254_primary_sha256"] == D0254_PRIMARY_SHA
    assert binding["d0254_safe_verifier_sha256"] == D0254_VERIFIER_SHA
    assert binding["d0253_authorization_commit"] == D0253_COMMIT
    assert binding["d0253_authorization_record_sha256"] == D0253_RECORD_SHA
    assert binding["d0251_frozen_snapshot_source_commit"] == D0251_COMMIT
    assert binding["d0251_primary_sha256"] == D0251_PRIMARY_SHA

    ai = record["authorized_input"]

    assert ai["full_snapshot_record_count"] == 10
    assert ai["full_snapshot_record_universe_sha256"] == FULL_C3_UNIVERSE_SHA
    assert ai["shared_binding_field_count"] == 7
    assert ai["shared_seven_field_projection_sha256"] == SHARED_SEVEN_FIELD_PROJECTION_SHA
    assert ai["d0254_shared_fields_must_equal_d0251_full_record_projection"] is True
    assert ai["evidence_locator_count"] == 24
    assert ai["evidence_locator_universe_sha256"] == EVIDENCE_LOCATOR_UNIVERSE_SHA

    ae = record["authorized_execution"]

    assert ae["designated_execution_decision"] == "D0256"
    assert ae["execution_engine"] == "COMMITTED_D0254_SAFE_VERIFIER"
    assert ae["execution_engine_sha256"] == D0254_VERIFIER_SHA
    assert ae["execution_count"] == 1
    assert ae["expected_snapshot_read_count"] == 10
    assert ae["snapshot_bytes_may_be_read_only_inside_execution_engine"] is True
    assert ae["direct_additional_snapshot_reads_outside_execution_engine"] is False

    gate = record["execution_gate"]

    assert gate["d0256_execution_allowed_before_independent_d0255_checkpoint"] is False
    assert gate["d0256_must_use_exactly_one_d0254_safe_verifier_execution"] is True
    assert gate["d0256_must_capture_execution_transcript"] is True
    assert gate["d0256_must_not_rerun_after_invocation_begins"] is True

    correction = record["correction_provenance"]

    assert correction["prior_uncommitted_authoring_failure_class"] == (
        "METADATA_HASH_DOMAIN_MISMATCH"
    )
    assert correction["prior_uncommitted_authoring_repository_effect"] == "NONE"

    assert all(record["prohibited_operations"].values())
    assert all(
        value is False
        for value in record["downstream_nonauthorization"].values()
    )

    result = record["results"]

    assert result["d0254_verified_frozen"] is False
    assert result["revalidation_authorized"] is True
    assert result["revalidation_executed"] is False
    assert result["post_adjudication_branch_authorized"] is False

    manifest = (
        package
        / "04_d0254_full_freeze_snapshot_revalidation_authorization.v1.SHA256SUMS"
    )

    lines = manifest.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3

    expected_files = {
        "01_d0254_full_freeze_snapshot_revalidation_authorization.v1.json",
        "02_d0254_full_freeze_snapshot_revalidation_authorization_scope.v1.md",
        "03_verify_d0254_full_freeze_snapshot_revalidation_authorization.v1.py",
    }

    seen = set()

    for line in lines:
        digest, rel = line.split("  ", 1)
        assert rel in expected_files
        assert rel not in seen
        seen.add(rel)
        assert sha256(package / rel) == digest

    assert seen == expected_files

    print("D0255_CORRECTED_REVALIDATION_AUTHORIZATION_VERIFIER=PASS")
    print("D0254_PACKAGE_IDENTITY_BINDING=PASS")
    print("D0251_D0253_FULL_UNIVERSE_BINDING=PASS")
    print("D0255_FULL_SNAPSHOT_RECORD_COUNT=10")
    print("D0255_FULL_SNAPSHOT_RECORD_UNIVERSE_SHA256=" + FULL_C3_UNIVERSE_SHA)
    print("D0255_SHARED_SEVEN_FIELD_PROJECTION_SHA256=" + SHARED_SEVEN_FIELD_PROJECTION_SHA)
    print("D0255_D0254_SEVEN_FIELD_BINDING=PASS")
    print("D0255_HASH_DOMAINS_DISTINCT=YES")
    print("D0255_EVIDENCE_LOCATOR_COUNT=24")
    print("D0255_EVIDENCE_LOCATOR_UNIVERSE_SHA256=" + EVIDENCE_LOCATOR_UNIVERSE_SHA)
    print("D0256_REVALIDATION_AUTHORIZED=YES")
    print("D0256_REVALIDATION_EXECUTED=NO")
    print("D0256_EXECUTION_ALLOWED_BEFORE_INDEPENDENT_D0255_CHECKPOINT=NO")
    print("D0254_SAFE_VERIFIER_EXECUTED_BY_D0255_VERIFIER=NO")
    print("D0251_SNAPSHOT_CONTENT_READ_BY_D0255_VERIFIER=NO")
    print("C4_AUTHORIZED=NO")
    print("C5_AUTHORIZED=NO")
    print("C6_AUTHORIZED=NO")
    print("B2_AUTHORIZED=NO")
    print("SAFE_CORRECTED_D0255_VERIFIER=PASS")

    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(
            "D0255_CORRECTED_REVALIDATION_AUTHORIZATION_VERIFIER=FAIL",
            file=sys.stderr,
        )
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        raise
