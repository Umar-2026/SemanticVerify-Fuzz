#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

D0250_COMMIT = "e6c319ce22a4de68bece34db60829a75597c06e7"
D0250_TREE = "4b67d4fdd0475be8ab3d89f4ccfe54b1e76f0317"
D0250_PARENT = "379ae0663fd9c6dbadd24eb677f16cf3ca12f4be"
D0250_RECORD_SHA = "27ae3c94601841184bd7149e82d674550c7c2fd7610462d244b049d4663e6d8d"
D0250_MANIFEST_SHA = "265cdec3a551e8214217caf790e2dd8c03037f20096e7da2b2c6dc84576ca803"
D0250_VERIFIER_SHA = "d3377970b595b37a775fdce4710c67717eefeab19a71ae56f7d82f6e282794db"
D0250_DEFECT_SPAN_SHA = "a1e4664783a37842675d4d6cc61b89bbba15ad26dcbece85b02fdc6fc59efb9a"

D0251_COMMIT = "7505af46bf8a7c16bbb8ba83b0a7bb81cb8e99b5"
D0251_TREE = "6b5729e8ae8281798363330c682da10bb38a84bc"
D0251_PARENT = D0250_COMMIT
D0251_PRIMARY_SHA = "e6d027353df054ac6c31b700e15cc29a0e7b88b8a7324775d3212a7d5fb08fb5"
D0251_MANIFEST_SHA = "fd0dbb7befebe33f8969ca40d6a48d142ad8146bbb25b941f8a4560b1f1985bb"
D0251_VERIFIER_SHA = "594aea41f85bb578786abd65997db78950c385c415b51f9fb29bd8111a750061"

CONTENT_UNIVERSE_SHA = "2d57d40ae4106b4b8179278172d462822078626166bef9272b0e91cbe1c00054"
MAPPING_SHA = "2246236e8651b382afdfe34a2ca0ee3ca8081709527634d3b919c7bb02fbe189"

D0250_RECORD = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0250_c2_bounded_candidate_content_acquisition_authorization_v1/"
    "01_c2_bounded_candidate_content_acquisition_authorization.v1.json"
)

D0250_MANIFEST = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0250_c2_bounded_candidate_content_acquisition_authorization_v1/"
    "04_c2_bounded_candidate_content_acquisition_authorization.v1.SHA256SUMS"
)

D0250_HISTORICAL_VERIFIER = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0250_c2_bounded_candidate_content_acquisition_authorization_v1/"
    "03_verify_c2_bounded_candidate_content_acquisition_authorization.v1.py"
)

D0251_PRIMARY = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0251_c2_bounded_candidate_content_acquisition_execution_v1/"
    "01_c2_bounded_candidate_content_acquisition_execution.v1.json"
)

D0251_MANIFEST = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0251_c2_bounded_candidate_content_acquisition_execution_v1/"
    "04_c2_bounded_candidate_content_acquisition_execution.v1.SHA256SUMS"
)

D0251_SAFE_VERIFIER = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0251_c2_bounded_candidate_content_acquisition_execution_v1/"
    "03_verify_c2_bounded_candidate_content_acquisition_execution.v1.py"
)

EXPECTED_NEXT = (
    "INDEPENDENT_READ_ONLY_VERIFY_D0252_BEFORE_RETRYING_D0251_INDEPENDENT_CHECKPOINT"
)

repo = Path(
    os.environ.get(
        "SVF_REPO_ROOT",
        "/openbayes/home/semanticverify-fuzz-research",
    )
)

pkg = Path(
    os.environ.get(
        "SVF_PACKAGE_DIR",
        Path(__file__).resolve().parent,
    )
)


def run_text(*args):
    return subprocess.check_output(
        args,
        cwd=repo,
        text=True,
    ).strip()


def run_bytes(*args):
    return subprocess.check_output(
        args,
        cwd=repo,
    )


def sha256_bytes(data):
    return hashlib.sha256(
        data
    ).hexdigest()


def no_dup(pairs):
    out = {}

    for key, value in pairs:
        if key in out:
            raise AssertionError(
                "duplicate JSON key: " + key
            )

        out[key] = value

    return out


current_head = run_text(
    "git",
    "rev-parse",
    "HEAD",
)

rc = subprocess.run(
    [
        "git",
        "merge-base",
        "--is-ancestor",
        D0251_COMMIT,
        current_head,
    ],
    cwd=repo,
).returncode

assert rc == 0

assert run_text(
    "git",
    "rev-parse",
    f"{D0250_COMMIT}^{{tree}}",
) == D0250_TREE

assert run_text(
    "git",
    "rev-parse",
    f"{D0250_COMMIT}^",
) == D0250_PARENT

assert run_text(
    "git",
    "rev-parse",
    f"{D0251_COMMIT}^{{tree}}",
) == D0251_TREE

assert run_text(
    "git",
    "rev-parse",
    f"{D0251_COMMIT}^",
) == D0250_COMMIT

assert run_text(
    "git",
    "log",
    "-1",
    "--pretty=%s",
    D0251_COMMIT,
) == (
    "decision: execute C2 bounded candidate content acquisition"
)

d250_raw = run_bytes(
    "git",
    "show",
    f"{D0250_COMMIT}:{D0250_RECORD}",
)

assert sha256_bytes(
    d250_raw
) == D0250_RECORD_SHA

d250_manifest_raw = run_bytes(
    "git",
    "show",
    f"{D0250_COMMIT}:{D0250_MANIFEST}",
)

assert sha256_bytes(
    d250_manifest_raw
) == D0250_MANIFEST_SHA

d250_verifier_raw = run_bytes(
    "git",
    "show",
    f"{D0250_COMMIT}:{D0250_HISTORICAL_VERIFIER}",
)

assert sha256_bytes(
    d250_verifier_raw
) == D0250_VERIFIER_SHA

d250_verifier_text = d250_verifier_raw.decode(
    "utf-8"
)

assert "D0251_PKG" in d250_verifier_text
assert "D0251_DECISION" in d250_verifier_text

assert re.search(
    r'for\s+path\s+in\s*\(\s*D0251_PKG\s*,\s*D0251_DECISION\s*,?\s*\)',
    d250_verifier_text,
    re.S,
)

assert 'f"HEAD:{path}"' in d250_verifier_text
assert "assert rc != 0" in d250_verifier_text

lines = d250_verifier_text.splitlines()

defect_span = "\n".join(
    lines[352:370]
).encode("utf-8")

assert sha256_bytes(
    defect_span
) == D0250_DEFECT_SPAN_SHA

d250 = json.loads(
    d250_raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

assert d250["decision"] == "D0250"

assert d250["authorization"] == {
    "authorized": True,
    "c2_authorized": True,
    "designated_execution_decision": "D0251",
    "executed": False,
}

universe = d250[
    "candidate_content_universe"
]

assert len(universe) == 10

universe_raw = json.dumps(
    universe,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert sha256_bytes(
    universe_raw
) == CONTENT_UNIVERSE_SHA

d251_raw = run_bytes(
    "git",
    "show",
    f"{D0251_COMMIT}:{D0251_PRIMARY}",
)

assert sha256_bytes(
    d251_raw
) == D0251_PRIMARY_SHA

d251_manifest_raw = run_bytes(
    "git",
    "show",
    f"{D0251_COMMIT}:{D0251_MANIFEST}",
)

assert sha256_bytes(
    d251_manifest_raw
) == D0251_MANIFEST_SHA

d251_verifier_raw = run_bytes(
    "git",
    "show",
    f"{D0251_COMMIT}:{D0251_SAFE_VERIFIER}",
)

assert sha256_bytes(
    d251_verifier_raw
) == D0251_VERIFIER_SHA

d251 = json.loads(
    d251_raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

assert d251[
    "acquisition_id"
] == (
    "D0251-C2-BOUNDED-CANDIDATE-CONTENT-ACQUISITION-V1"
)

assert d251[
    "authorization_binding"
] == {
    "commit": D0250_COMMIT,
    "decision": "D0250",
    "manifest_sha256": D0250_MANIFEST_SHA,
    "record_path": D0250_RECORD,
    "record_sha256": D0250_RECORD_SHA,
    "tree": D0250_TREE,
}

binding = d251[
    "d0249_candidate_content_universe_binding"
]

assert binding[
    "candidate_content_universe_sha256"
] == CONTENT_UNIVERSE_SHA

assert binding[
    "source_oid_to_snapshot_mapping_sha256"
] == MAPPING_SHA

assert d251[
    "acquisition_summary"
] == {
    "exact_snapshot_blob_identity_match_count": 10,
    "snapshot_count": 10,
    "source_blob_read_count": 10,
    "source_candidate_count": 10,
}

boundaries = d251[
    "execution_boundaries"
]

assert boundaries[
    "candidate_content_semantic_interpretation"
] is False

assert boundaries[
    "source_authority_adjudication"
] is False

assert boundaries[
    "crosswalk_semantic_adjudication"
] is False

assert boundaries[
    "candidate_admissibility_adjudication"
] is False

assert boundaries[
    "req06_req14_determination"
] is False

results = d251[
    "results_not_established"
]

assert results[
    "b2_readiness_established"
] is False

record_path = (
    pkg
    / "01_d0250_post_d0251_verifier_compatibility_corrective_successor.v1.json"
)

raw = record_path.read_bytes()

assert not raw.endswith(b"\n")

record = json.loads(
    raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

canonical = json.dumps(
    record,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert raw == canonical

assert record[
    "correction_id"
] == (
    "D0252-D0250-POST-D0251-VERIFIER-COMPATIBILITY-CORRECTIVE-SUCCESSOR-V1"
)

assert record[
    "correction_role"
] == (
    "D0250_POST_D0251_VERIFIER_COMPATIBILITY_CORRECTIVE_SUCCESSOR"
)

assert record[
    "correction_target"
] == (
    "D0250_VERIFIER_POST_DESIGNATED_EXECUTION_DESCENDANT_ABSENCE_ASSERTION_ONLY"
)

assert record[
    "d0250_binding"
] == {
    "commit": D0250_COMMIT,
    "historical_verifier_sha256": D0250_VERIFIER_SHA,
    "manifest_sha256": D0250_MANIFEST_SHA,
    "parent": D0250_PARENT,
    "record_sha256": D0250_RECORD_SHA,
    "tree": D0250_TREE,
}

defect = record[
    "d0250_historical_verifier_defect"
]

assert defect[
    "defect_class"
] == (
    "POST_DESIGNATED_EXECUTION_DESCENDANT_ABSENCE_ASSERTION"
)

assert defect[
    "defect_span_sha256"
] == D0250_DEFECT_SPAN_SHA

assert defect[
    "historical_verifier_valid_at_original_d0250_checkpoint"
] is True

assert defect[
    "post_d0251_descendant_rerunnable"
] is False

assert defect[
    "rerun_in_current_d0251_descendant_history_authorized"
] is False

assert record[
    "d0251_designated_execution_binding"
] == {
    "acquisition_summary": {
        "exact_snapshot_blob_identity_match_count": 10,
        "snapshot_count": 10,
        "source_blob_read_count": 10,
        "source_candidate_count": 10,
    },
    "commit": D0251_COMMIT,
    "content_universe_sha256": CONTENT_UNIVERSE_SHA,
    "manifest_sha256": D0251_MANIFEST_SHA,
    "mapping_sha256": MAPPING_SHA,
    "parent": D0251_PARENT,
    "primary_output_sha256": D0251_PRIMARY_SHA,
    "safe_verifier_sha256": D0251_VERIFIER_SHA,
    "tree": D0251_TREE,
}

preserved = record[
    "preserved_semantics"
]

assert preserved[
    "d0250_authorization_semantics_changed"
] is False

assert preserved[
    "d0250_prior_independent_verified_frozen_status_preserved"
] is True

assert preserved[
    "d0251_execution_semantics_changed"
] is False

assert preserved[
    "d0251_acquired_snapshots_changed"
] is False

contract = record[
    "safe_successor_verifier_contract"
]

assert contract[
    "execute_d0250_historical_verifier"
] is False

assert contract[
    "open_original_source_blobs"
] is False

assert contract[
    "read_d0251_snapshot_bytes"
] is False

assert contract[
    "postcommit_rerunnable"
] is True

for key, value in record[
    "results_not_established"
].items():
    assert value is False, key

assert record[
    "next_required_checkpoint"
] == EXPECTED_NEXT

print("D0252_SAFE_SUCCESSOR_VERIFIER=PASS")
print("D0250_AUTHORIZATION_DIRECT_BINDING=PASS")
print("D0250_HISTORICAL_VERIFIER_STATIC_DEFECT_BINDING=PASS")
print("D0250_HISTORICAL_VERIFIER_EXECUTED=NO")
print("D0251_DESIGNATED_EXECUTION_BINDING=PASS")
print("D0251_CONTENT_UNIVERSE_BINDING=PASS")
print("D0251_EXECUTION_MAPPING_BINDING=PASS")
print("D0251_ACQUISITION_SUMMARY_10_10_10_10=PASS")
print("D0251_SNAPSHOT_BYTES_READ_BY_D0252_VERIFIER=NO")
print("ORIGINAL_SOURCE_BLOB_REOPENED_BY_D0252_VERIFIER=NO")
print("D0250_PRIOR_INDEPENDENT_VERIFIED_FROZEN_STATUS_PRESERVED=YES")
print("D0251_VERIFIED_FROZEN=NO")
print("C2_AUTHORIZED=YES")
print("C2_EXECUTED=YES")
print("C3_AUTHORIZED=NO")
print("C3_EXECUTED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("SAFE_D0252_VERIFIER=PASS")
