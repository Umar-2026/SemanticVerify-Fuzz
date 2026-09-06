#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

D0246_COMMIT = "512df3091b4aeb76ad0979f1c559a3e59cab756e"
D0246_TREE = "bab06bee08e85ea33260a32cf2f4328f37430b52"
D0246_RECORD_SHA = "d0c31c01f0beb10a42cee7f40e6a09a9301ba3ca7aef9935810a78591a9c96f3"
D0246_MANIFEST_SHA = "53879217777296e83258683e3a2b57edfa63526431da511e3654a4f78ed3d9a7"

D0244_ROOT_SET_SHA = "4fceb4501bc84b3d43d9b2b7591cc84fc4bebcaaa23218c68ac7bbd6fe8bb3bf"

D0246_RECORD = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0246_replacement_bounded_crosswalk_locator_discovery_execution_authorization_v1/01_replacement_bounded_crosswalk_locator_discovery_execution_authorization.v1.json"

D0246_MANIFEST = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0246_replacement_bounded_crosswalk_locator_discovery_execution_authorization_v1/04_replacement_bounded_crosswalk_locator_discovery_execution_authorization.v1.SHA256SUMS"

EXPECTED_TOP_LEVEL_KEYS = {
    "authorization_binding",
    "bound_root_trees",
    "discovery_id",
    "enumerated_immediate_children",
    "enumeration_summary",
    "execution_boundaries",
    "lexical_candidate_locators",
    "next_required_checkpoint",
    "results_not_established",
}

EXPECTED_CHILD_KEYS = {
    "git_mode",
    "git_object_id",
    "git_object_type",
    "lexical_candidate",
    "matched_filename_tokens",
    "relative_name",
    "root_id",
}

EXPECTED_CANDIDATE_KEYS = {
    "full_locator",
    "git_mode",
    "git_object_id",
    "git_object_type",
    "matched_filename_tokens",
    "relative_name",
    "root_id",
}

EXPECTED_BOUNDARIES = {
    "concrete_mapping": False,
    "cross_source_join": False,
    "discovered_file_byte_hash_recomputation": False,
    "external_network_access": False,
    "file_content_read": False,
    "follow_candidate": False,
    "follow_symlink": False,
    "git_history_search": False,
    "new_evidence_acquisition": False,
    "referenced_target_open": False,
    "repository_wide_search": False,
    "semantic_interpretation": False,
    "subdirectory_recursion": False,
}

EXPECTED_RESULTS = {
    "authoritative_crosswalk_source_instance_bound": False,
    "b2_readiness_established": False,
    "c2_authorization_ready": False,
    "candidate_admissibility_resolved": False,
    "crosswalk_semantics_established": False,
    "evidence_adequacy_established": False,
    "req06_req14_satisfaction_established": False,
    "source_authority_established": False,
    "zero_unresolved_closure_established": False,
}

VALID_MODES = {
    "040000",
    "100644",
    "100755",
    "120000",
    "160000",
}

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

primary_path = pkg / "01_bounded_crosswalk_locator_discovery_execution.v1.json"
scope_path = pkg / "02_bounded_crosswalk_locator_discovery_execution_scope.v1.md"


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


def no_dup(pairs):
    out = {}

    for k, v in pairs:
        if k in out:
            raise AssertionError(
                "duplicate JSON key: " + k
            )

        out[k] = v

    return out


def canonical_string(s):
    assert isinstance(s, str)

    out = ['"']

    for ch in s:
        cp = ord(ch)

        assert not (
            0xD800 <= cp <= 0xDFFF
        )

        if ch == '"':
            out.append('\\"')
        elif ch == '\\':
            out.append('\\\\')
        elif cp <= 0x1F:
            out.append("\\u%04x" % cp)
        else:
            out.append(ch)

    out.append('"')

    return "".join(out).encode("utf-8")


def canonical_json(value):
    if value is None:
        return b"null"

    if value is True:
        return b"true"

    if value is False:
        return b"false"

    if isinstance(value, int) and not isinstance(value, bool):
        return str(value).encode("ascii")

    if isinstance(value, str):
        return canonical_string(value)

    if isinstance(value, list):
        return (
            b"["
            + b",".join(
                canonical_json(x)
                for x in value
            )
            + b"]"
        )

    if isinstance(value, dict):
        assert all(
            isinstance(k, str)
            for k in value
        )

        items = sorted(
            value.items(),
            key=lambda kv: kv[0].encode("utf-8"),
        )

        return (
            b"{"
            + b",".join(
                canonical_string(k)
                + b":"
                + canonical_json(v)
                for k, v in items
            )
            + b"}"
        )

    raise AssertionError(
        "unsupported JSON value type"
    )


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def git_tree_entry_mode(mode):
    assert mode in VALID_MODES

    normalized = mode.lstrip("0")

    assert normalized

    return normalized.encode("ascii")


def reconstruct_tree_oid(children):
    raw = bytearray()

    for child in children:
        mode = child["git_mode"]
        obj_type = child["git_object_type"]
        oid = child["git_object_id"]
        name = child["relative_name"]

        assert mode in VALID_MODES

        if mode == "040000":
            assert obj_type == "tree"
        elif mode == "160000":
            assert obj_type == "commit"
        else:
            assert obj_type == "blob"

        assert re.fullmatch(
            r"[0-9a-f]{40}",
            oid,
        )

        name_bytes = name.encode(
            "utf-8",
            errors="strict",
        )

        assert name_bytes.decode(
            "utf-8",
            errors="strict",
        ) == name

        assert b"\x00" not in name_bytes
        assert b"/" not in name_bytes

        raw.extend(
            git_tree_entry_mode(mode)
        )
        raw.extend(b" ")
        raw.extend(name_bytes)
        raw.extend(b"\x00")
        raw.extend(bytes.fromhex(oid))

    header = (
        b"tree "
        + str(len(raw)).encode("ascii")
        + b"\x00"
    )

    return hashlib.sha1(
        header + bytes(raw)
    ).hexdigest()


# ------------------------------------------------------------
# A. D0246 immutable authorization binding.
# ------------------------------------------------------------

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
        D0246_COMMIT,
        current_head,
    ],
    cwd=repo,
).returncode

assert rc == 0

assert run_text(
    "git",
    "rev-parse",
    f"{D0246_COMMIT}^{{tree}}",
) == D0246_TREE

d0246_record_bytes = run_bytes(
    "git",
    "show",
    f"{D0246_COMMIT}:{D0246_RECORD}",
)

assert sha256_bytes(
    d0246_record_bytes
) == D0246_RECORD_SHA

d0246_manifest_bytes = run_bytes(
    "git",
    "show",
    f"{D0246_COMMIT}:{D0246_MANIFEST}",
)

assert sha256_bytes(
    d0246_manifest_bytes
) == D0246_MANIFEST_SHA

d0246 = json.loads(
    d0246_record_bytes.decode("utf-8"),
    object_pairs_hook=no_dup,
)

auth = d0246["authorization"]

assert d0246["decision"] == "D0246"
assert auth["authorized"] is True
assert auth["executed"] is False
assert auth["designated_execution_decision"] == "D0247"

roots = auth["roots"]
tokens = auth["filename_filter"]["tokens"]

assert len(roots) == 3
assert len(tokens) == 10
assert auth["recursion_depth"] == 1
assert auth["filename_filter"]["match_mode"] == "CASE_INSENSITIVE_SUBSTRING_OR"

root_bytes = json.dumps(
    roots,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert sha256_bytes(
    root_bytes
) == D0244_ROOT_SET_SHA

# ------------------------------------------------------------
# B. Canonical D0247 primary output.
# ------------------------------------------------------------

raw = primary_path.read_bytes()

assert not raw.endswith(b"\n")

record = json.loads(
    raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

assert set(record.keys()) == EXPECTED_TOP_LEVEL_KEYS

assert raw == canonical_json(record)

assert record["discovery_id"] == (
    "D0247-BOUNDED-CROSSWALK-LOCATOR-DISCOVERY-V1"
)

binding = record["authorization_binding"]

assert binding == {
    "commit": D0246_COMMIT,
    "decision": "D0246",
    "manifest_sha256": D0246_MANIFEST_SHA,
    "record_path": D0246_RECORD,
    "record_sha256": D0246_RECORD_SHA,
    "root_record_set_sha256": D0244_ROOT_SET_SHA,
    "tree": D0246_TREE,
}

assert record["bound_root_trees"] == roots

# ------------------------------------------------------------
# C. Validate child metadata and exact root block order.
# ------------------------------------------------------------

children = record["enumerated_immediate_children"]

summary = record["enumeration_summary"]

assert summary["root_count"] == 3

per_root = summary["per_root"]

assert len(per_root) == 3

offset = 0
recomputed_candidates = []

for root_index, root in enumerate(
    roots
):
    root_id = root["root_id"]

    root_summary = per_root[root_index]

    assert root_summary["root_id"] == root_id

    n = root_summary[
        "enumerated_child_count"
    ]

    assert isinstance(n, int)
    assert n >= 0

    block = children[
        offset:offset + n
    ]

    assert len(block) == n

    candidate_count = 0

    for child in block:
        assert set(
            child.keys()
        ) == EXPECTED_CHILD_KEYS

        assert child["root_id"] == root_id

        name = child["relative_name"]

        assert isinstance(name, str)
        assert "/" not in name
        assert "\x00" not in name

        mode = child["git_mode"]

        assert mode in VALID_MODES

        obj_type = child[
            "git_object_type"
        ]

        assert obj_type in {
            "blob",
            "tree",
            "commit",
        }

        oid = child[
            "git_object_id"
        ]

        assert re.fullmatch(
            r"[0-9a-f]{40}",
            oid,
        )

        folded = name.casefold()

        matched = [
            token
            for token in tokens
            if token.casefold() in folded
        ]

        assert child[
            "matched_filename_tokens"
        ] == matched

        lexical = bool(matched)

        assert child[
            "lexical_candidate"
        ] is lexical

        if lexical:
            candidate_count += 1

            recomputed_candidates.append(
                {
                    "full_locator": (
                        root["directory"]
                        + "/"
                        + name
                    ),
                    "git_mode": mode,
                    "git_object_id": oid,
                    "git_object_type": obj_type,
                    "matched_filename_tokens": matched,
                    "relative_name": name,
                    "root_id": root_id,
                }
            )

    reconstructed = reconstruct_tree_oid(
        block
    )

    assert reconstructed == root[
        "git_tree_object"
    ]

    assert root_summary[
        "lexical_candidate_count"
    ] == candidate_count

    assert root_summary[
        "lexical_noncandidate_count"
    ] == n - candidate_count

    offset += n


assert offset == len(children)

# ------------------------------------------------------------
# D. Candidate array is exact filtered subsequence.
# ------------------------------------------------------------

candidates = record[
    "lexical_candidate_locators"
]

for candidate in candidates:
    assert set(
        candidate.keys()
    ) == EXPECTED_CANDIDATE_KEYS

assert candidates == recomputed_candidates

child_count = len(children)
candidate_count = len(candidates)
noncandidate_count = (
    child_count
    - candidate_count
)

assert summary[
    "enumerated_child_count"
] == child_count

assert summary[
    "lexical_candidate_count"
] == candidate_count

assert summary[
    "lexical_noncandidate_count"
] == noncandidate_count

assert (
    summary["enumerated_child_count"]
    ==
    summary["lexical_candidate_count"]
    +
    summary["lexical_noncandidate_count"]
)

# ------------------------------------------------------------
# E. Exact execution/result boundaries.
# ------------------------------------------------------------

assert record[
    "execution_boundaries"
] == EXPECTED_BOUNDARIES

assert record[
    "results_not_established"
] == EXPECTED_RESULTS

if candidate_count > 0:
    expected_next = (
        "SEPARATE_READ_ONLY_LOCATOR_CANDIDATE_QUALIFICATION_AND_IDENTITY_BINDING"
    )
else:
    expected_next = (
        "STOP_NO_AUTOMATIC_SCOPE_EXPANSION_REQUIRES_SEPARATE_GOVERNANCE"
    )

assert record[
    "next_required_checkpoint"
] == expected_next

# ------------------------------------------------------------
# F. Human-readable scope boundary.
# ------------------------------------------------------------

scope = scope_path.read_text(
    encoding="utf-8"
)

markers = [
    "EXECUTED — METADATA-ONLY LOCATOR DISCOVERY",
    "D0247_ROOT_ENUMERATION_COUNT=3",
    "D0247_FILE_CONTENT_READ=NO",
    "D0247_DISCOVERED_FILE_BYTE_HASH_RECOMPUTATION=NO",
    "D0247_SUBDIRECTORY_RECURSION=NO",
    "D0247_FOLLOW_CANDIDATE=NO",
    "D0247_REPOSITORY_WIDE_SEARCH=NO",
    "D0247_GIT_HISTORY_SEARCH=NO",
    "D0247_EXTERNAL_NETWORK_ACCESS=NO",
    "D0247_SEMANTIC_INTERPRETATION=NO",
    "D0247_CROSS_SOURCE_JOIN=NO",
    "D0247_CONCRETE_MAPPING=NO",
    "C2_AUTHORIZED=NO",
    "C3_AUTHORIZED=NO",
    "B2_AUTHORIZED=NO",
    expected_next,
]

for marker in markers:
    assert marker in scope, marker

print("D0247_NON_REENUMERATING_SAFE_VERIFIER=PASS")
print("D0246_AUTHORIZATION_BINDING=PASS")
print("D0247_PRIMARY_JSON_CANONICALIZATION=PASS")
print("D0247_COMPLETE_ROOT_RECORD_BINDING=PASS")
print("D0247_TREE_COMPLETENESS_BY_METADATA_RECONSTRUCTION=PASS")
print("D0247_BOUND_ROOT_REENUMERATION_BY_VERIFIER=NO")
print("D0247_ENUMERATED_CHILD_COUNT=" + str(child_count))
print("D0247_LEXICAL_CANDIDATE_COUNT=" + str(candidate_count))
print("D0247_LEXICAL_NONCANDIDATE_COUNT=" + str(noncandidate_count))
print("D0247_FILENAME_FILTER_RECOMPUTATION=PASS")
print("D0247_CANDIDATE_ARRAY_RECOMPUTATION=PASS")
print("D0247_SUMMARY_RECOMPUTATION=PASS")
print("D0247_FILE_CONTENT_READ=NO")
print("D0247_SEMANTIC_INTERPRETATION=NO")
print("C2_AUTHORIZED=NO")
print("C2_EXECUTED=NO")
print("C3_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("D0247_SAFE_VERIFIER=PASS")
