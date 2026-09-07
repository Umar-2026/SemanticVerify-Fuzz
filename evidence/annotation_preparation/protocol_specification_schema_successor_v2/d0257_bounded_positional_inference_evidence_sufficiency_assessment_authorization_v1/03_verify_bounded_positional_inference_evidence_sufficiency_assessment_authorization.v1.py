#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

D0256_COMMIT = "042a3fdc13936ee1e879bcd077ebe2d8ac2fbc75"
D0256_TREE = "b161bc485f544ed460be15719302b04cee1a126d"
D0256_RECORD_SHA = "8e6fe312f98fb489c2f05f7bb07a4e8444181bd6542b4e378f85e5b6ecd01113"
D0256_MANIFEST_SHA = "a1bb3d472c696443314ec870fbd225b37c378bbcee40df040af2b2496bbd1a9b"

D0254_COMMIT = "5cfbbe57ad4fa5c00174137dd19d003be737d29c"
D0254_TREE = "6e1abfc1bfdb1a405b7e6594c4b77a395387cb19"
D0254_PRIMARY_SHA = "8ee9bf4b84412d1bddf86da60aa2e947e5b7c44ac9d2dfe1d539af126023f3d0"
D0254_MANIFEST_SHA = "320a752cc37e7285215ad9f0c0269440277f70105825634c647378334ab82e1c"

D0251_COMMIT = "7505af46bf8a7c16bbb8ba83b0a7bb81cb8e99b5"

NINE_BINDING_SHA = "51afc6fda72397cebde135eb8762a1269ffd7acdbe32d5941abbf4db220d23b3"
NINE_STATUS_PROFILE_SHA = "3342ab3e560f3a47290bb83ad93e34f9e834623470e229fad84bcd86a92989eb"
NINE_EVIDENCE_METADATA_SHA = "a5c534b13dca61719e8dca903ae6fe3214b719d52926b8cfd4620e6a7be9e4ae"

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

D0254_PRIMARY_REL = (
    BASE
    / "d0254_c3_bounded_candidate_content_adjudication_execution_v1"
    / "01_c3_bounded_candidate_content_adjudication_execution.v1.json"
)

D0254_MANIFEST_REL = (
    BASE
    / "d0254_c3_bounded_candidate_content_adjudication_execution_v1"
    / "04_c3_bounded_candidate_content_adjudication_execution.v1.SHA256SUMS"
)

D0256_RECORD_REL = (
    BASE
    / "d0256_d0254_full_freeze_snapshot_revalidation_execution_v1"
    / "01_d0254_full_freeze_snapshot_revalidation_execution.v1.json"
)

D0256_MANIFEST_REL = (
    BASE
    / "d0256_d0254_full_freeze_snapshot_revalidation_execution_v1"
    / "05_d0254_full_freeze_snapshot_revalidation_execution.v1.SHA256SUMS"
)

EXPECTED_INDICES = [1,2,3,5,6,7,8,9,10]

def fail(msg):
    print("D0257_SAFE_VERIFIER=FAIL")
    print("D0257_SAFE_VERIFIER_REASON=" + str(msg))
    sys.exit(1)

def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def load_json_no_dup(path):
    def no_dup(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                raise AssertionError("duplicate JSON key: " + k)
            out[k] = v
        return out
    return json.loads(
        Path(path).read_text(encoding="utf-8"),
        object_pairs_hook=no_dup,
    )

def canon_sha(obj):
    raw = json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

try:
    repo = Path(
        os.environ.get("SVF_REPO_ROOT", "")
    ).resolve()

    if not repo.is_dir():
        fail("repository root unavailable")

    pkg = Path(__file__).resolve().parent

    record_path = pkg / (
        "01_bounded_positional_inference_evidence_"
        "sufficiency_assessment_authorization.v1.json"
    )
    scope_path = pkg / (
        "02_bounded_positional_inference_evidence_"
        "sufficiency_assessment_authorization_scope.v1.md"
    )
    verifier_path = Path(__file__).resolve()
    manifest_path = pkg / (
        "04_bounded_positional_inference_evidence_"
        "sufficiency_assessment_authorization.v1.SHA256SUMS"
    )

    for p in [
        record_path,
        scope_path,
        verifier_path,
        manifest_path,
    ]:
        assert p.is_file()

    # --------------------------------------------------------------
    # Repository ancestry / immutable checkpoint identities
    # --------------------------------------------------------------

    current_head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()

    d0256_tree = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", D0256_COMMIT + "^{tree}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()

    d0254_tree = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", D0254_COMMIT + "^{tree}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()

    assert d0256_tree == D0256_TREE
    assert d0254_tree == D0254_TREE

    subprocess.run(
        [
            "git", "-C", str(repo),
            "merge-base", "--is-ancestor",
            D0256_COMMIT, current_head,
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    subprocess.run(
        [
            "git", "-C", str(repo),
            "merge-base", "--is-ancestor",
            D0251_COMMIT, D0254_COMMIT,
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    d254_primary_path = repo / D0254_PRIMARY_REL
    d254_manifest_path = repo / D0254_MANIFEST_REL
    d256_record_path = repo / D0256_RECORD_REL
    d256_manifest_path = repo / D0256_MANIFEST_REL

    assert sha_file(d254_primary_path) == D0254_PRIMARY_SHA
    assert sha_file(d254_manifest_path) == D0254_MANIFEST_SHA
    assert sha_file(d256_record_path) == D0256_RECORD_SHA
    assert sha_file(d256_manifest_path) == D0256_MANIFEST_SHA

    # --------------------------------------------------------------
    # Verify D0257 record canonicalization
    # --------------------------------------------------------------

    raw_record = record_path.read_bytes()
    record = load_json_no_dup(record_path)

    canonical = json.dumps(
        record,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    assert raw_record == canonical
    assert not raw_record.endswith(b"\n")

    assert record["authorization_id"] == (
        "D0257-BOUNDED-POSITIONAL-INFERENCE-EVIDENCE-"
        "SUFFICIENCY-ASSESSMENT-AUTHORIZATION-V1"
    )

    assert record["authorization_role"] == (
        "BOUNDED_POSITIONAL_INFERENCE_EVIDENCE_SUFFICIENCY_"
        "ASSESSMENT_AUTHORIZATION_ONLY"
    )

    parent = record["authorization_parent_binding"]

    assert parent["d0256_commit"] == D0256_COMMIT
    assert parent["d0256_tree"] == D0256_TREE
    assert parent["d0256_record_sha256"] == D0256_RECORD_SHA
    assert parent["d0256_manifest_sha256"] == D0256_MANIFEST_SHA

    assert parent["d0254_commit"] == D0254_COMMIT
    assert parent["d0254_tree"] == D0254_TREE
    assert parent["d0254_primary_sha256"] == D0254_PRIMARY_SHA
    assert parent["d0254_manifest_sha256"] == D0254_MANIFEST_SHA

    assert parent["d0251_commit"] == D0251_COMMIT

    # --------------------------------------------------------------
    # Independently recompute nine-candidate metadata domains
    # --------------------------------------------------------------

    d254 = load_json_no_dup(d254_primary_path)

    selected = [
        x for x in d254["candidate_adjudications"]
        if x["candidate_index"] in EXPECTED_INDICES
    ]

    assert [x["candidate_index"] for x in selected] == EXPECTED_INDICES
    assert len(selected) == 9

    shared = [
        "candidate_index",
        "root_id",
        "source_locator",
        "snapshot_path",
        "snapshot_sha256",
        "snapshot_byte_count",
        "snapshot_git_blob_oid",
    ]

    bindings = [
        {k: row[k] for k in shared}
        for row in selected
    ]

    required_fields = [
        "requirement_identity_status",
        "semantic_unit_identity_status",
        "explicit_crosswalk_relation_status",
        "version_or_checksum_binding_status",
        "authority_basis_status",
    ]

    profile = []
    evidence_rows = []

    for row in selected:
        assert row["class06_qualification_verdict"] == (
            "INDETERMINATE_UNDER_BOUNDED_EVIDENCE"
        )
        assert row["positional_inference_status"] == "INDETERMINATE"

        negatives = []

        for field in required_fields:
            assert row[field] in {
                "ESTABLISHED",
                "NOT_ESTABLISHED",
            }
            if row[field] == "NOT_ESTABLISHED":
                negatives.append(field)

        assert negatives

        profile.append({
            "candidate_index": row["candidate_index"],
            "positional_inference_status":
                row["positional_inference_status"],
            "required_not_established_fields": negatives,
        })

        refs = []

        for ref in row["evidence_references"]:
            refs.append({
                "evidence_purpose": ref["evidence_purpose"],
                "locator_kind": ref["locator_kind"],
                "locator_value": ref["locator_value"],
            })

        evidence_rows.append({
            "candidate_index": row["candidate_index"],
            "evidence_references": refs,
        })

    assert canon_sha(bindings) == NINE_BINDING_SHA
    assert canon_sha(profile) == NINE_STATUS_PROFILE_SHA
    assert canon_sha(evidence_rows) == NINE_EVIDENCE_METADATA_SHA

    evidence_count = sum(
        len(x["evidence_references"])
        for x in evidence_rows
    )

    assert evidence_count == 19

    input_binding = record["input_universe_binding"]

    assert input_binding["candidate_count"] == 9
    assert input_binding["candidate_indices"] == EXPECTED_INDICES
    assert input_binding[
        "nine_candidate_binding_universe_sha256"
    ] == NINE_BINDING_SHA
    assert input_binding[
        "frozen_status_profile_sha256"
    ] == NINE_STATUS_PROFILE_SHA
    assert input_binding[
        "evidence_reference_metadata_sha256"
    ] == NINE_EVIDENCE_METADATA_SHA
    assert input_binding[
        "evidence_reference_metadata_count"
    ] == 19

    # --------------------------------------------------------------
    # Authorization semantics
    # --------------------------------------------------------------

    scope = record["authorization_scope"]

    assert scope["assessment_authorized"] is True
    assert scope["assessment_executed"] is False
    assert scope["authorized_candidate_count"] == 9
    assert scope["authorized_candidate_indices"] == EXPECTED_INDICES

    assert scope[
        "authorized_snapshot_primary_read_count_per_candidate"
    ] == "AT_MOST_1"

    assert scope[
        "authorizes_d0258_to_read_exact_bound_frozen_snapshots"
    ] is True

    assert scope["authorizes_assignment_of_new_positional_status"] is False
    assert scope["authorizes_class06_verdict_reclassification"] is False
    assert scope[
        "authorizes_rejudgment_of_frozen_required_criteria"
    ] is False

    assert scope["authorizes_original_source_blob_reopen"] is False
    assert scope["authorizes_original_candidate_worktree_read"] is False
    assert scope["authorizes_reference_following"] is False
    assert scope["authorizes_repository_search"] is False
    assert scope["authorizes_git_history_search"] is False
    assert scope["authorizes_network_access"] is False
    assert scope[
        "authorizes_snapshot_python_execution_or_import"
    ] is False

    assert scope["authorizes_c4"] is False
    assert scope["authorizes_c5"] is False
    assert scope["authorizes_c6"] is False
    assert scope["authorizes_b2"] is False

    assert scope["designated_execution_decision"] == "D0258"
    assert scope[
        "d0258_execution_allowed_before_independent_d0257_checkpoint"
    ] is False

    boundary = record["results_nonestablishment_boundary"]

    assert boundary[
        "authoritative_class06_source_instance_operationally_bound"
    ] is False
    assert boundary["c2_source_instance_allowlist_bound"] is False
    assert boundary["d0254_frozen_verdicts_changed"] is False
    assert boundary["d0258_assessment_executed"] is False
    assert boundary["post_adjudication_branch_authorized"] is False
    assert boundary["req06_req14_determination_performed"] is False
    assert boundary["zero_unresolved_closure_established"] is False

    # --------------------------------------------------------------
    # Manifest
    # --------------------------------------------------------------

    lines = [
        x.strip()
        for x in manifest_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if x.strip()
    ]

    assert len(lines) == 3

    expected_names = {
        record_path.name,
        scope_path.name,
        verifier_path.name,
    }

    observed_names = set()

    for line in lines:
        digest, name = line.split(None, 1)
        name = name.strip()
        observed_names.add(name)
        target = pkg / name
        assert target.is_file()
        assert sha_file(target) == digest

    assert observed_names == expected_names

    print("D0257_EVIDENCE_SUFFICIENCY_AUTHORIZATION_VERIFIER=PASS")
    print("D0256_FROZEN_INPUT_BINDING=PASS")
    print("D0254_FROZEN_RESULT_BINDING=PASS")
    print("D0257_NINE_CANDIDATE_INPUT_BINDING=PASS")
    print("D0257_EVIDENCE_REFERENCE_METADATA_BINDING=PASS")
    print("D0257_AUTHORIZATION_SEMANTICS=PASS")
    print("D0258_ASSESSMENT_AUTHORIZED=YES")
    print("D0258_ASSESSMENT_EXECUTED=NO")
    print(
        "D0258_EXECUTION_ALLOWED_BEFORE_INDEPENDENT_D0257_CHECKPOINT=NO"
    )
    print("D0251_SNAPSHOT_CONTENT_READ_BY_D0257_VERIFIER=NO")
    print("D0254_SAFE_VERIFIER_EXECUTED_BY_D0257_VERIFIER=NO")
    print("D0256_SAFE_VERIFIER_EXECUTED_BY_D0257_VERIFIER=NO")
    print("C4_AUTHORIZED=NO")
    print("C5_AUTHORIZED=NO")
    print("C6_AUTHORIZED=NO")
    print("B2_AUTHORIZED=NO")
    print("SAFE_D0257_VERIFIER=PASS")

except Exception as exc:
    fail(repr(exc))
