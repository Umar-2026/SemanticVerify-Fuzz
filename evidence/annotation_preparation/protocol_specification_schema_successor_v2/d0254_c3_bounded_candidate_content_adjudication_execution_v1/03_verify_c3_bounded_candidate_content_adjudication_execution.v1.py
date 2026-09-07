#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

D0253_COMMIT = "7057c8a655229f2265ea120a1d6945d5afe092fc"
D0253_TREE = "68c1146eacd370238b249352b93efd20502f0e5f"
D0253_RECORD_SHA = "70cf66d89d3c1903be69586396764db68c378fc584447d0d2370556625e61199"
D0253_MANIFEST_SHA = "e8e8ae1da1bf2b1358c2aceb5ae7da65d0b17779d7435c8faeec99f955920357"

D0251_COMMIT = "7505af46bf8a7c16bbb8ba83b0a7bb81cb8e99b5"
D0251_TREE = "6b5729e8ae8281798363330c682da10bb38a84bc"
D0251_PRIMARY_SHA = "e6d027353df054ac6c31b700e15cc29a0e7b88b8a7324775d3212a7d5fb08fb5"
D0251_MANIFEST_SHA = "fd0dbb7befebe33f8969ca40d6a48d142ad8146bbb25b941f8a4560b1f1985bb"

C3_UNIVERSE_SHA = "dbb16ce946761f76490f86ee7f72a8be3871a72f3ea3c3d25d28ffb67307d7b5"
MAPPING_SHA = "04e0c3cfe4ffc59d3508e89c964edff61ef1645a3acd95ed6caf3b59a3977a79"
LOGIC_SHA = "e12fa090ce097613d06a4b396270fe60c82358b7f7f98893d35511a42639e14c"

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

D0253_RECORD = (
    BASE
    / "d0253_c3_bounded_candidate_content_adjudication_authorization_v1"
    / "01_c3_bounded_candidate_content_adjudication_authorization.v1.json"
)

D0253_MANIFEST = (
    BASE
    / "d0253_c3_bounded_candidate_content_adjudication_authorization_v1"
    / "04_c3_bounded_candidate_content_adjudication_authorization.v1.SHA256SUMS"
)

D0251_PKG = (
    BASE
    / "d0251_c2_bounded_candidate_content_acquisition_execution_v1"
)

D0251_PRIMARY = (
    D0251_PKG
    / "01_c2_bounded_candidate_content_acquisition_execution.v1.json"
)

D0251_MANIFEST = (
    D0251_PKG
    / "04_c2_bounded_candidate_content_acquisition_execution.v1.SHA256SUMS"
)

repo = Path(
    os.environ.get(
        "SVF_REPO_ROOT",
        "/openbayes/home/semanticverify-fuzz-research",
    )
)

package_root_env = os.environ.get("SVF_D0254_PACKAGE_ROOT")

if package_root_env:
    package_root = Path(package_root_env)
else:
    package_root = (
        repo
        / BASE
        / "d0254_c3_bounded_candidate_content_adjudication_execution_v1"
    )

primary_path = (
    package_root
    / "01_c3_bounded_candidate_content_adjudication_execution.v1.json"
)

manifest_path = (
    package_root
    / "04_c3_bounded_candidate_content_adjudication_execution.v1.SHA256SUMS"
)

def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def no_dup(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise AssertionError("duplicate JSON key: " + key)
        out[key] = value
    return out

def raw_blob_oid(data):
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()

def canonical_json(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

def resolve_json_pointer(doc, pointer):
    if pointer == "":
        return doc

    assert pointer.startswith("/")

    cur = doc

    for raw_token in pointer.split("/")[1:]:
        token = raw_token.replace("~1", "/").replace("~0", "~")

        if isinstance(cur, list):
            assert token.isdigit()
            cur = cur[int(token)]
        else:
            assert isinstance(cur, dict)
            assert token in cur
            cur = cur[token]

    return cur

assert subprocess.run(
    ["git", "merge-base", "--is-ancestor", D0253_COMMIT, "HEAD"],
    cwd=repo,
).returncode == 0

assert subprocess.run(
    ["git", "rev-parse", f"{D0253_COMMIT}^{{tree}}"],
    cwd=repo,
    text=True,
    stdout=subprocess.PIPE,
    check=True,
).stdout.strip() == D0253_TREE

assert subprocess.run(
    ["git", "rev-parse", f"{D0251_COMMIT}^{{tree}}"],
    cwd=repo,
    text=True,
    stdout=subprocess.PIPE,
    check=True,
).stdout.strip() == D0251_TREE

assert sha256_file(repo / D0253_RECORD) == D0253_RECORD_SHA
assert sha256_file(repo / D0253_MANIFEST) == D0253_MANIFEST_SHA
assert sha256_file(repo / D0251_PRIMARY) == D0251_PRIMARY_SHA
assert sha256_file(repo / D0251_MANIFEST) == D0251_MANIFEST_SHA

d253 = json.loads(
    (repo / D0253_RECORD).read_text(encoding="utf-8")
)

d251 = json.loads(
    (repo / D0251_PRIMARY).read_text(encoding="utf-8")
)

rows = d253["adjudication_input_universe"]["snapshot_records"]

assert rows == d251["candidate_content_snapshots"]
assert len(rows) == 10
assert [x["candidate_index"] for x in rows] == list(range(1, 11))

assert hashlib.sha256(
    canonical_json(rows)
).hexdigest() == C3_UNIVERSE_SHA

mapping = []

for row in rows:
    source = row["source_locator"]

    if source.endswith(".json"):
        fmt = "JSON"
    elif source.endswith(".md"):
        fmt = "MARKDOWN_TEXT"
    elif source.endswith(".py"):
        fmt = "PYTHON_TEXT_NOT_EXECUTABLE"
    elif source.endswith(".SHA256SUMS"):
        fmt = "SHA256SUMS_TEXT_REFERENCES_NOT_FOLLOWED"
    else:
        fmt = "GENERIC_UTF8_TEXT"

    rel = (D0251_PKG / row["snapshot_path"]).as_posix()

    mapping.append(
        {
            "candidate_index": row["candidate_index"],
            "format_kind": fmt,
            "full_snapshot_path": rel,
            "root_id": row["root_id"],
            "snapshot_byte_count": row["snapshot_byte_count"],
            "snapshot_git_blob_oid": row["snapshot_git_blob_oid"],
            "snapshot_sha256": row["snapshot_sha256"],
            "source_locator": row["source_locator"],
        }
    )

assert hashlib.sha256(
    canonical_json(mapping)
).hexdigest() == MAPPING_SHA

raw = primary_path.read_bytes()

assert not raw.endswith(b"\n")

primary = json.loads(
    raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

assert raw == canonical_json(primary)

assert primary["adjudication_id"] == (
    "D0254-C3-BOUNDED-CANDIDATE-CONTENT-ADJUDICATION-V1"
)

assert primary["authorization_binding"]["decision"] == "D0253"
assert primary["authorization_binding"]["commit"] == D0253_COMMIT
assert primary["authorization_binding"]["tree"] == D0253_TREE
assert primary["authorization_binding"]["record_sha256"] == D0253_RECORD_SHA
assert primary["authorization_binding"]["manifest_sha256"] == D0253_MANIFEST_SHA

binding = primary["d0251_frozen_snapshot_universe_binding"]

assert binding["commit"] == D0251_COMMIT
assert binding["tree"] == D0251_TREE
assert binding["primary_output_sha256"] == D0251_PRIMARY_SHA
assert binding["manifest_sha256"] == D0251_MANIFEST_SHA
assert binding["snapshot_record_count"] == 10
assert binding["snapshot_record_universe_sha256"] == C3_UNIVERSE_SHA
assert binding["execution_mapping_sha256"] == MAPPING_SHA

assert primary["adjudication_rubric"]["logic_sha256"] == LOGIC_SHA

adjs = primary["candidate_adjudications"]

assert len(adjs) == 10
assert [x["candidate_index"] for x in adjs] == list(range(1, 11))

criterion_statuses = {
    "ESTABLISHED",
    "NOT_ESTABLISHED",
    "INDETERMINATE",
}

positional_statuses = {
    "NOT_REQUIRED",
    "REQUIRED",
    "INDETERMINATE",
}

verdicts = {
    "QUALIFIES_UNDER_BOUNDED_EVIDENCE",
    "DOES_NOT_QUALIFY_UNDER_BOUNDED_EVIDENCE",
    "INDETERMINATE_UNDER_BOUNDED_EVIDENCE",
}

qualifying = []
nonqualifying = []
indeterminate = []

for row, adj in zip(rows, adjs):
    assert adj["candidate_index"] == row["candidate_index"]
    assert adj["root_id"] == row["root_id"]
    assert adj["source_locator"] == row["source_locator"]
    assert adj["snapshot_path"] == row["snapshot_path"]
    assert adj["snapshot_sha256"] == row["snapshot_sha256"]
    assert adj["snapshot_byte_count"] == row["snapshot_byte_count"]
    assert adj["snapshot_git_blob_oid"] == row["snapshot_git_blob_oid"]

    rel = D0251_PKG / row["snapshot_path"]
    snapshot_path = repo / rel

    data = snapshot_path.read_bytes()

    assert len(data) == row["snapshot_byte_count"]
    assert hashlib.sha256(data).hexdigest() == row["snapshot_sha256"]
    assert raw_blob_oid(data) == row["snapshot_git_blob_oid"]

    committed_oid = subprocess.run(
        ["git", "rev-parse", f"HEAD:{rel.as_posix()}"],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.strip()

    assert committed_oid == row["snapshot_git_blob_oid"]

    decode_status = adj["content_decode_status"]
    assert decode_status in {"DECODED", "DECODE_FAILED"}

    req = adj["requirement_identity_status"]
    sem = adj["semantic_unit_identity_status"]
    cross = adj["explicit_crosswalk_relation_status"]
    pos = adj["positional_inference_status"]
    ver = adj["version_or_checksum_binding_status"]
    auth = adj["authority_basis_status"]
    verdict = adj["class06_qualification_verdict"]

    assert req in criterion_statuses
    assert sem in criterion_statuses
    assert cross in criterion_statuses
    assert ver in criterion_statuses
    assert auth in criterion_statuses
    assert pos in positional_statuses
    assert verdict in verdicts

    required = [req, sem, cross, ver, auth]

    qualifies = (
        all(x == "ESTABLISHED" for x in required)
        and pos == "NOT_REQUIRED"
    )

    no_indeterminate = (
        all(x != "INDETERMINATE" for x in required)
        and pos != "INDETERMINATE"
    )

    if qualifies:
        expected_verdict = "QUALIFIES_UNDER_BOUNDED_EVIDENCE"
    elif no_indeterminate:
        expected_verdict = "DOES_NOT_QUALIFY_UNDER_BOUNDED_EVIDENCE"
    else:
        expected_verdict = "INDETERMINATE_UNDER_BOUNDED_EVIDENCE"

    if decode_status == "DECODE_FAILED":
        expected_verdict = "INDETERMINATE_UNDER_BOUNDED_EVIDENCE"

    assert verdict == expected_verdict

    text = None
    lines = None
    json_doc = None

    try:
        text = data.decode("utf-8", errors="strict")
        lines = text.split("\n")
    except UnicodeDecodeError:
        pass

    if (
        text is not None
        and row["source_locator"].endswith(".json")
    ):
        try:
            json_doc = json.loads(
                text,
                object_pairs_hook=no_dup,
            )
        except Exception:
            json_doc = None

    for ev in adj["evidence_references"]:
        assert set(ev.keys()) == {
            "evidence_purpose",
            "locator_kind",
            "locator_value",
        }

        kind = ev["locator_kind"]
        value = ev["locator_value"]

        if kind == "LINE_RANGE":
            assert lines is not None

            m = re.fullmatch(
                r"L([1-9][0-9]*)-L([1-9][0-9]*)",
                value,
            )
            assert m

            start = int(m.group(1))
            end = int(m.group(2))

            assert 1 <= start <= end <= len(lines)

        elif kind == "BYTE_RANGE":
            m = re.fullmatch(
                r"([0-9]+):([0-9]+)",
                value,
            )
            assert m

            start = int(m.group(1))
            end = int(m.group(2))

            assert 0 <= start < end <= len(data)

        elif kind == "JSON_POINTER":
            assert json_doc is not None
            resolve_json_pointer(json_doc, value)

        else:
            raise AssertionError("unsupported locator kind")

    if verdict == "QUALIFIES_UNDER_BOUNDED_EVIDENCE":
        qualifying.append(adj["candidate_index"])
    elif verdict == "DOES_NOT_QUALIFY_UNDER_BOUNDED_EVIDENCE":
        nonqualifying.append(adj["candidate_index"])
    else:
        indeterminate.append(adj["candidate_index"])

summary = primary["adjudication_summary"]

assert summary == {
    "candidate_count": 10,
    "qualifies_under_bounded_evidence_count": len(qualifying),
    "does_not_qualify_under_bounded_evidence_count": len(nonqualifying),
    "indeterminate_under_bounded_evidence_count": len(indeterminate),
}

assert len(qualifying) + len(nonqualifying) + len(indeterminate) == 10

results = primary["results"]

assert results["qualifying_candidate_indices"] == qualifying
assert results["does_not_qualify_candidate_indices"] == nonqualifying
assert results["indeterminate_candidate_indices"] == indeterminate
assert results["no_qualifying_candidate_in_exact_10_snapshot_universe"] == (
    len(qualifying) == 0
)

assert results["repository_wide_negative_proof"] is False
assert results["external_source_negative_proof"] is False
assert results[
    "authoritative_class06_source_instance_bound_for_operational_use"
] is False
assert results["c2_source_instance_allowlist_bound"] is False
assert results["req06_req14_determination_performed"] is False
assert results["zero_unresolved_closure_established"] is False
assert results["b2_readiness_established"] is False

boundaries = primary["execution_boundaries"]

assert boundaries["frozen_d0251_snapshot_content_read"] is True
assert boundaries["snapshot_read_count"] == 10
assert boundaries["original_source_blob_reopened"] is False
assert boundaries["original_candidate_worktree_content_read"] is False
assert boundaries["source_root_reenumeration"] is False
assert boundaries["repository_wide_search"] is False
assert boundaries["git_history_search"] is False
assert boundaries["external_network_access"] is False
assert boundaries["reference_following"] is False
assert boundaries["snapshot_python_execution"] is False
assert boundaries["cross_candidate_content_join"] is False
assert boundaries["req06_req14_determination"] is False
assert boundaries["c4_execution"] is False
assert boundaries["b2_execution"] is False

assert primary["next_required_checkpoint"] == (
    "INDEPENDENT_READ_ONLY_VERIFY_D0254_C3_ADJUDICATION"
)

print("D0254_SAFE_BOUNDED_ADJUDICATION_VERIFIER=PASS")
print("D0253_AUTHORIZATION_BINDING=PASS")
print("D0251_FROZEN_SNAPSHOT_UNIVERSE_BINDING=PASS")
print("D0254_EXECUTION_MAPPING_BINDING=PASS")
print("D0254_PRIMARY_JSON_CANONICALIZATION=PASS")
print("D0254_SNAPSHOT_IDENTITY_RECOMPUTATION=PASS")
print("D0254_EVIDENCE_REFERENCE_INTEGRITY=PASS")
print("D0254_VERDICT_FORMULA_CONSISTENCY=PASS")
print("D0254_SUMMARY_COUNTS=PASS")
print(f"D0254_CANDIDATE_COUNT={len(adjs)}")
print(f"D0254_QUALIFIES_COUNT={len(qualifying)}")
print(f"D0254_DOES_NOT_QUALIFY_COUNT={len(nonqualifying)}")
print(f"D0254_INDETERMINATE_COUNT={len(indeterminate)}")
print("ORIGINAL_SOURCE_BLOB_REOPENED_BY_D0254_VERIFIER=NO")
print("SNAPSHOT_PYTHON_EXECUTED_BY_D0254_VERIFIER=NO")
print("REFERENCE_FOLLOWED_BY_D0254_VERIFIER=NO")
print("C3_AUTHORIZED=YES")
print("C3_EXECUTED=YES")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("SAFE_D0254_VERIFIER=PASS")
