#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

D0255_COMMIT = "0f77d1553e4aa9840ed36c03ec0c2f925156cfab"
D0255_TREE = "e76587abf136fdeb6d3d7350850886654f726006"
D0255_RECORD_SHA = "df9eb2c1148b5829c10fc1527e4b21a1a373206320581a6097720c6c8a8b05bb"
D0255_MANIFEST_SHA = "da97553e63de7158bac30728599c60fc0cb889c8e2d5f86b0f69d7c96f953346"

D0254_COMMIT = "5cfbbe57ad4fa5c00174137dd19d003be737d29c"
D0254_TREE = "6e1abfc1bfdb1a405b7e6594c4b77a395387cb19"
D0254_PRIMARY_SHA = "8ee9bf4b84412d1bddf86da60aa2e947e5b7c44ac9d2dfe1d539af126023f3d0"
D0254_VERIFIER_SHA = "f2ef7c9dcd18fdc42157a11a4e25d674c54d38875215840af31722a51829c058"
D0254_MANIFEST_SHA = "320a752cc37e7285215ad9f0c0269440277f70105825634c647378334ab82e1c"

D0251_COMMIT = "7505af46bf8a7c16bbb8ba83b0a7bb81cb8e99b5"
D0251_TREE = "6b5729e8ae8281798363330c682da10bb38a84bc"
D0251_PRIMARY_SHA = "e6d027353df054ac6c31b700e15cc29a0e7b88b8a7324775d3212a7d5fb08fb5"

FULL_C3_UNIVERSE_SHA = "dbb16ce946761f76490f86ee7f72a8be3871a72f3ea3c3d25d28ffb67307d7b5"
SHARED_SEVEN_FIELD_PROJECTION_SHA = "fe0ba4023b8f9dd9bfbf00b4056717229de4f420d6311053f9864e21b729206e"
EVIDENCE_LOCATOR_UNIVERSE_SHA = "a0e326368d63c350c1d18f0f8e8988047f9731079c330d71dcd814f7e102df97"

PASS_MARKER_SET_SHA = "7141a9af923a4729767a6197c6be1e7d9aafb0d4d3a1d0cbdad9c7bcc6725712"

EXPECTED_RECORD_SHA = "8e6fe312f98fb489c2f05f7bb07a4e8444181bd6542b4e378f85e5b6ecd01113"
EXPECTED_SCOPE_SHA = "9198c68adb509357467bbaa18b372f4f109959309e0ea44ee5a821620ada2eb3"
EXPECTED_TRANSCRIPT_SHA = "c94fe232fcf4a1ad50dea9371b7b7c5826e00bf92279b2cafee19da765500ada"

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

D0251_PRIMARY = (
    BASE
    / "d0251_c2_bounded_candidate_content_acquisition_execution_v1"
    / "01_c2_bounded_candidate_content_acquisition_execution.v1.json"
)

D0254_PKG = BASE / "d0254_c3_bounded_candidate_content_adjudication_execution_v1"
D0254_PRIMARY = D0254_PKG / "01_c3_bounded_candidate_content_adjudication_execution.v1.json"
D0254_VERIFIER = D0254_PKG / "03_verify_c3_bounded_candidate_content_adjudication_execution.v1.py"
D0254_MANIFEST = D0254_PKG / "04_c3_bounded_candidate_content_adjudication_execution.v1.SHA256SUMS"

D0255_PKG = BASE / "d0255_d0254_full_freeze_snapshot_revalidation_authorization_v1"
D0255_RECORD = D0255_PKG / "01_d0254_full_freeze_snapshot_revalidation_authorization.v1.json"
D0255_MANIFEST = D0255_PKG / "04_d0254_full_freeze_snapshot_revalidation_authorization.v1.SHA256SUMS"

EXPECTED_COMMITTED_PATHS = sorted([
    "documentation/decisions/0256-execute-d0254-full-freeze-snapshot-revalidation.md",
    str(
        BASE
        / "d0256_d0254_full_freeze_snapshot_revalidation_execution_v1"
        / "01_d0254_full_freeze_snapshot_revalidation_execution.v1.json"
    ),
    str(
        BASE
        / "d0256_d0254_full_freeze_snapshot_revalidation_execution_v1"
        / "02_d0254_full_freeze_snapshot_revalidation_execution_scope.v1.md"
    ),
    str(
        BASE
        / "d0256_d0254_full_freeze_snapshot_revalidation_execution_v1"
        / "03_d0254_safe_verifier_execution_transcript.EXACT_TEXT.v1.txt"
    ),
    str(
        BASE
        / "d0256_d0254_full_freeze_snapshot_revalidation_execution_v1"
        / "04_verify_d0254_full_freeze_snapshot_revalidation_execution.v1.py"
    ),
    str(
        BASE
        / "d0256_d0254_full_freeze_snapshot_revalidation_execution_v1"
        / "05_d0254_full_freeze_snapshot_revalidation_execution.v1.SHA256SUMS"
    ),
])

REQUIRED_MARKERS = [
    "D0251_FROZEN_SNAPSHOT_UNIVERSE_BINDING=PASS",
    "D0253_AUTHORIZATION_BINDING=PASS",
    "D0254_EVIDENCE_REFERENCE_INTEGRITY=PASS",
    "D0254_EXECUTION_MAPPING_BINDING=PASS",
    "D0254_PRIMARY_JSON_CANONICALIZATION=PASS",
    "D0254_SAFE_BOUNDED_ADJUDICATION_VERIFIER=PASS",
    "D0254_SNAPSHOT_IDENTITY_RECOMPUTATION=PASS",
    "D0254_SUMMARY_COUNTS=PASS",
    "D0254_VERDICT_FORMULA_CONSISTENCY=PASS",
    "SAFE_D0254_VERIFIER=PASS",
]

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

    record_path = package / "01_d0254_full_freeze_snapshot_revalidation_execution.v1.json"
    scope_path = package / "02_d0254_full_freeze_snapshot_revalidation_execution_scope.v1.md"
    transcript_path = package / "03_d0254_safe_verifier_execution_transcript.EXACT_TEXT.v1.txt"
    manifest_path = package / "05_d0254_full_freeze_snapshot_revalidation_execution.v1.SHA256SUMS"

    assert sha256(record_path) == EXPECTED_RECORD_SHA
    assert sha256(scope_path) == EXPECTED_SCOPE_SHA
    assert sha256(transcript_path) == EXPECTED_TRANSCRIPT_SHA

    assert git(repo, "rev-parse", f"{D0255_COMMIT}^{{tree}}") == D0255_TREE
    assert git(repo, "rev-parse", f"{D0254_COMMIT}^{{tree}}") == D0254_TREE
    assert git(repo, "rev-parse", f"{D0251_COMMIT}^{{tree}}") == D0251_TREE

    head = git(repo, "rev-parse", "HEAD")

    for ancestor in (D0251_COMMIT, D0254_COMMIT, D0255_COMMIT):
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, head],
            cwd=repo,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    assert sha256(repo / D0251_PRIMARY) == D0251_PRIMARY_SHA
    assert sha256(repo / D0254_PRIMARY) == D0254_PRIMARY_SHA
    assert sha256(repo / D0254_VERIFIER) == D0254_VERIFIER_SHA
    assert sha256(repo / D0254_MANIFEST) == D0254_MANIFEST_SHA
    assert sha256(repo / D0255_RECORD) == D0255_RECORD_SHA
    assert sha256(repo / D0255_MANIFEST) == D0255_MANIFEST_SHA

    raw = record_path.read_bytes()

    def no_dup(pairs):
        out = {}
        for k, v in pairs:
            assert k not in out, k
            out[k] = v
        return out

    obj = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=no_dup,
    )

    assert raw == canonical(obj)
    assert not raw.endswith(b"\n")

    expected_top = {
        "revalidation_id",
        "authorization_binding",
        "d0254_binding",
        "d0251_snapshot_universe_binding",
        "evidence_locator_universe_binding",
        "execution_engine_binding",
        "execution_count",
        "return_code",
        "transcript_path",
        "transcript_sha256",
        "pass_markers_required",
        "pass_markers_observed",
        "revalidation_boundaries",
        "result",
        "next_required_checkpoint",
    }

    assert set(obj.keys()) == expected_top

    assert obj["revalidation_id"] == (
        "D0256-D0254-FULL-FREEZE-SNAPSHOT-REVALIDATION-V1"
    )

    assert obj["authorization_binding"]["d0255_commit"] == D0255_COMMIT
    assert obj["authorization_binding"]["d0255_tree"] == D0255_TREE
    assert obj["authorization_binding"]["d0255_record_sha256"] == D0255_RECORD_SHA
    assert obj["authorization_binding"]["d0255_manifest_sha256"] == D0255_MANIFEST_SHA

    assert obj["d0254_binding"]["commit"] == D0254_COMMIT
    assert obj["d0254_binding"]["tree"] == D0254_TREE
    assert obj["d0254_binding"]["primary_sha256"] == D0254_PRIMARY_SHA
    assert obj["d0254_binding"]["safe_verifier_sha256"] == D0254_VERIFIER_SHA
    assert obj["d0254_binding"]["manifest_sha256"] == D0254_MANIFEST_SHA

    universe = obj["d0251_snapshot_universe_binding"]

    assert universe["commit"] == D0251_COMMIT
    assert universe["tree"] == D0251_TREE
    assert universe["primary_sha256"] == D0251_PRIMARY_SHA
    assert universe["full_snapshot_record_count"] == 10
    assert universe["full_snapshot_record_universe_sha256"] == FULL_C3_UNIVERSE_SHA
    assert universe["shared_seven_field_projection_sha256"] == SHARED_SEVEN_FIELD_PROJECTION_SHA

    evidence = obj["evidence_locator_universe_binding"]

    assert evidence["count"] == 24
    assert evidence["line_range_count"] == 24
    assert evidence["json_pointer_count"] == 0
    assert evidence["byte_range_count"] == 0
    assert evidence["sha256"] == EVIDENCE_LOCATOR_UNIVERSE_SHA

    engine = obj["execution_engine_binding"]

    assert engine["engine"] == "COMMITTED_D0254_SAFE_VERIFIER"
    assert engine["engine_sha256"] == D0254_VERIFIER_SHA
    assert engine["required_pass_marker_count"] == 10
    assert engine["required_pass_marker_set_sha256"] == PASS_MARKER_SET_SHA
    assert engine["expected_snapshot_record_count"] == 10
    assert engine["expected_snapshot_read_count_under_successful_engine_contract"] == 10
    assert engine["invocation_guard_final_state"] == "INVOCATION_RETURNED"
    assert engine["invocation_guard_execution_count"] == 1

    assert obj["execution_count"] == 1
    assert obj["return_code"] == 0
    assert obj["transcript_sha256"] == EXPECTED_TRANSCRIPT_SHA

    assert obj["pass_markers_required"] == REQUIRED_MARKERS
    assert obj["pass_markers_observed"] == REQUIRED_MARKERS

    transcript = transcript_path.read_text(encoding="utf-8")

    for marker in REQUIRED_MARKERS:
        assert transcript.splitlines().count(marker) == 1

    observed = sorted(
        line
        for line in transcript.splitlines()
        if line.endswith("=PASS")
    )

    assert observed == sorted(REQUIRED_MARKERS)

    marker_sha = hashlib.sha256(
        json.dumps(
            sorted(REQUIRED_MARKERS),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    assert marker_sha == PASS_MARKER_SET_SHA

    bounds = obj["revalidation_boundaries"]

    assert bounds["snapshot_bytes_read_only_inside_d0254_safe_verifier"] is True
    assert bounds["direct_d0256_snapshot_reads_outside_d0254_verifier"] == 0
    assert bounds["original_source_blob_reopen"] is False
    assert bounds["original_candidate_worktree_content_read"] is False
    assert bounds["source_root_reenumeration"] is False
    assert bounds["repository_wide_source_search"] is False
    assert bounds["git_history_source_search"] is False
    assert bounds["network_access"] is False
    assert bounds["reference_following"] is False
    assert bounds["snapshot_python_execution_or_import"] is False
    assert bounds["c3_adjudication_reexecution"] is False
    assert bounds["semantic_status_rejudgment"] is False
    assert bounds["class06_verdict_rejudgment"] is False

    result = obj["result"]

    assert result["structural_and_evidence_integrity_revalidation_executed"] is True
    assert result["structural_and_evidence_integrity_revalidation_passed"] is True
    assert result["d0254_verified_frozen"] is False
    assert result["post_adjudication_branch_authorized"] is False

    d251 = json.loads(
        (repo / D0251_PRIMARY).read_text(encoding="utf-8")
    )
    d254 = json.loads(
        (repo / D0254_PRIMARY).read_text(encoding="utf-8")
    )

    rows = d251["candidate_content_snapshots"]
    adjs = d254["candidate_adjudications"]

    assert len(rows) == 10
    assert len(adjs) == 10

    assert (
        hashlib.sha256(canonical(rows)).hexdigest()
        == FULL_C3_UNIVERSE_SHA
    )

    fields = [
        "candidate_index",
        "root_id",
        "source_locator",
        "snapshot_path",
        "snapshot_sha256",
        "snapshot_byte_count",
        "snapshot_git_blob_oid",
    ]

    projection = [
        {k: row[k] for k in fields}
        for row in rows
    ]

    d254_projection = [
        {k: row[k] for k in fields}
        for row in adjs
    ]

    assert projection == d254_projection

    assert (
        hashlib.sha256(canonical(projection)).hexdigest()
        == SHARED_SEVEN_FIELD_PROJECTION_SHA
    )

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

    assert (
        hashlib.sha256(canonical(refs)).hexdigest()
        == EVIDENCE_LOCATOR_UNIVERSE_SHA
    )

    lines = manifest_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 4

    expected_manifest_files = {
        "01_d0254_full_freeze_snapshot_revalidation_execution.v1.json",
        "02_d0254_full_freeze_snapshot_revalidation_execution_scope.v1.md",
        "03_d0254_safe_verifier_execution_transcript.EXACT_TEXT.v1.txt",
        "04_verify_d0254_full_freeze_snapshot_revalidation_execution.v1.py",
    }

    seen = set()

    for line in lines:
        digest, rel = line.split("  ", 1)

        assert rel in expected_manifest_files
        assert rel not in seen

        seen.add(rel)

        assert sha256(package / rel) == digest

    assert seen == expected_manifest_files

    preinstall = (
        os.environ.get("D0256_PREINSTALL_MODE", "NO") == "YES"
    )

    if not preinstall:
        expected_commit = os.environ["D0256_EXPECTED_COMMIT"]

        assert git(repo, "rev-parse", f"{expected_commit}^") == D0255_COMMIT

        assert git(
            repo,
            "log",
            "-1",
            "--format=%s",
            expected_commit,
        ) == "decision: execute D0254 full-freeze snapshot revalidation"

        subprocess.run(
            ["git", "merge-base", "--is-ancestor", expected_commit, head],
            cwd=repo,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        changed = git(
            repo,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            expected_commit,
        ).splitlines()

        assert sorted(changed) == EXPECTED_COMMITTED_PATHS

    print("D0256_REVALIDATION_EXECUTION_VERIFIER=PASS")
    print("D0255_AUTHORIZATION_BINDING=PASS")
    print("D0254_ENGINE_BINDING=PASS")
    print("D0251_METADATA_UNIVERSE_BINDING=PASS")
    print("D0256_PRIMARY_JSON_CANONICALIZATION=PASS")
    print("D0256_EXECUTION_COUNT_EXACTLY_1=PASS")
    print("D0256_RETURN_CODE_0=PASS")
    print("D0256_TRANSCRIPT_IDENTITY=PASS")
    print("D0256_REQUIRED_PASS_MARKERS=PASS")
    print("D0256_FULL_SNAPSHOT_UNIVERSE_HASH_BINDING=PASS")
    print("D0256_SEVEN_FIELD_PROJECTION_HASH_BINDING=PASS")
    print("D0256_EVIDENCE_LOCATOR_UNIVERSE_HASH_BINDING=PASS")
    print("D0251_SNAPSHOT_CONTENT_READ_BY_D0256_SAFE_VERIFIER=NO")
    print("D0254_SAFE_VERIFIER_EXECUTED_BY_D0256_SAFE_VERIFIER=NO")
    print("D0254_VERIFIED_FROZEN=NO")
    print("POST_ADJUDICATION_BRANCH_AUTHORIZED=NO")
    print("SAFE_D0256_VERIFIER=PASS")

    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(
            "D0256_REVALIDATION_EXECUTION_VERIFIER=FAIL",
            file=sys.stderr,
        )
        print(
            f"{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise
