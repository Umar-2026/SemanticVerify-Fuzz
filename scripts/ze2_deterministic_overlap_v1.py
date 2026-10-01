#!/usr/bin/env python3
"""Frozen-candidate ZE2 engine. Do not invoke one-shot modes before gates."""

import argparse
import ast
import builtins
import hashlib
import io
import json
import os
import re
import secrets
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GOV = ROOT / "evaluation/governance_reconciliation"
D36 = GOV / "d0336_ze2_deterministic_candidate_source_representation_overlap_design.json"
D37 = GOV / "d0337_single_ze2_deterministic_overlap_execution_authorization.json"
D43 = GOV / "d0343_prospective_ze2_ze0_operational_correction_design.json"
D44 = GOV / "d0344_successor_ze2_operational_correction_authorization_amendment.json"
D45 = GOV / "d0345_post_amendment_ze2_readiness_reconciliation_authorization.json"
D0326 = GOV / "d0326_ze0_execution_result.json"
D46 = GOV / "d0346_ze2_operational_implementation_freeze.json"

D0343_COMMIT = "28160c3cb9fa0184b7b260f210fffa8202c6ee28"
D0344_COMMIT = "bf851ffea0b73978d55ef2b7da0896ed2b5731b7"
D0345_COMMIT = "06ab9ff6f9563c7f854a538bcb7124279bab2347"

ZE2_AUTH = "SVF-D0344-ZE2-SUCCESSOR-AUTHORIZATION-AMENDMENT-V1"
ZE2_RUN = "SVF-ZE2-DETERMINISTIC-REPRESENTATION-OVERLAP-RUN-001"
READINESS_AUTH = "SVF-D0345-ZE2-POST-AMENDMENT-READINESS-AUTH-V1"
D0326_SHA = "0cf4f0233664d8abe69e55f41fbcaa28815257ac479d14a5ff13a980e237009e"
D0326_BLOB = "ef86fa58ddc5c1b7173730afe28f4e93bb736ea5"

ZE0 = ROOT / (
    "evidence/representation_alignment/ZE0/"
    "candidate_representation_manifest_v1/"
    "candidate_representation_manifest.json"
)
ZE1 = ROOT / (
    "evidence/representation_alignment/ZE1/"
    "source_representation_inventory_v1/"
    "source_representation_inventory.json"
)
ZE0_STATE = ZE0.parent / "_execution_state.json"
ZE1_STATE = ZE1.parent / "_execution_state.json"
ZE2_ROOT = ROOT / (
    "evidence/representation_alignment/ZE2/"
    "deterministic_candidate_source_overlap_v1"
)

FORMS = [
    "ZE0-F0-RAW-PATH-EXACT",
    "ZE0-F1-DOT-SEGMENT-SEQUENCE-EXACT",
    "ZE0-F2-LEAF-SEGMENT-EXACT",
    "ZE0-F3-PARENT-LEAF-SEQUENCE-EXACT",
    "ZE0-F4-LEAF-LEXICAL-TOKENS",
    "ZE0-F5-PARENT-LEAF-LEXICAL-TOKEN-SEQUENCES",
    "ZE0-F6-ALL-SEGMENT-LEXICAL-TOKEN-SEQUENCES",
]

READY_CHECKS = [
    "D0344_EFFECTIVE_SUCCESSOR_AUTHORIZATION_BINDING_EXACT",
    "D0343_PROSPECTIVE_OPERATIONAL_CORRECTION_BINDING_EXACT",
    "D0340_CANDIDATE_INDEX_BINDING_EXACT",
    "D0336_ZE2_OUTPUT_CONTRACT_BINDING_EXACT",
    "ZE0_GIT_PATH_AND_BLOB_IDENTITY_EXACT",
    "ZE1_GIT_PATH_AND_LFS_POINTER_IDENTITY_EXACT",
    "GIT_LFS_RUNTIME_AND_REPOSITORY_HOOK_BINDING_EXACT",
    "ZE2_RESERVED_OUTPUT_ROOT_ABSENT",
    "D0343_ZE0_ATTESTATION_IMPLEMENTATION_CONFORMANCE_PASS",
    "D0343_F0_THROUGH_F6_REGENERATION_IMPLEMENTATION_CONFORMANCE_PASS",
    "D0337_CANDIDATE_VALUE_SERIALIZER_SYNTHETIC_CONFORMANCE_PASS",
    "D0337_EXACT_MATCHER_SYNTHETIC_CONFORMANCE_PASS",
    "D0344_SUCCESSOR_CONSUMED_SEQUENCE_CONFORMANCE_PASS",
    "D0344_ZE2_EXECUTION_STATE_AUTHORIZATION_ID_BINDING_CONFORMANCE_PASS",
    "NO_SCIENTIFIC_PAYLOAD_READ_DURING_READINESS",
]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def read_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def sha_file(path):
    sha = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            data = handle.read(1024 * 1024)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


def git(*args):
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True
    ).strip()


def load_contracts():
    return {
        "d36": read_json(D36),
        "d37": read_json(D37),
        "d43": read_json(D43),
        "d44": read_json(D44),
        "d45": read_json(D45),
        "d46": read_json(D46),
    }


def ascii_upper(c):
    return "A" <= c <= "Z"


def ascii_lower(c):
    return "a" <= c <= "z"


def ascii_digit(c):
    return "0" <= c <= "9"


def lexicalize(segment):
    require(isinstance(segment, str), "SEGMENT_NOT_STRING")
    tokens = []
    current = []

    def flush():
        if current:
            token = "".join(current)
            tokens.append(
                "".join(
                    chr(ord(c) + 32) if ascii_upper(c) else c
                    for c in token
                )
            )
            current.clear()

    for i, c in enumerate(segment):
        if c in "_-":
            flush()
            continue

        if i and current:
            prev = segment[i - 1]
            following = segment[i + 1] if i + 1 < len(segment) else ""
            boundary = (
                (ascii_lower(prev) or ascii_digit(prev))
                and ascii_upper(c)
            ) or (
                ascii_upper(prev)
                and ascii_upper(c)
                and ascii_lower(following)
            )
            if boundary:
                flush()

        current.append(c)

    flush()
    return tokens


def derive_forms(path):
    require(isinstance(path, str), "PROPERTY_PATH_NOT_STRING")
    segments = path.split(".")
    leaf = segments[-1]
    parent_leaf = segments[-2:] if len(segments) >= 2 else segments[:]
    return [
        path,
        segments,
        leaf,
        parent_leaf,
        lexicalize(leaf),
        [lexicalize(s) for s in parent_leaf],
        [lexicalize(s) for s in segments],
    ]


def u64(number):
    require(type(number) is int and 0 <= number < 2**64, "U64_RANGE")
    return number.to_bytes(8, "big")


def encode_string(value):
    require(isinstance(value, str), "NOT_STRING")
    data = value.encode("utf-8")
    return b"S" + u64(len(data)) + data


def encode_value(value, shape):
    if shape == "STRING":
        return encode_string(value)

    if shape == "SEQUENCE_OF_STRINGS":
        require(isinstance(value, list), "NOT_SEQUENCE")
        return (
            b"L" + u64(len(value))
            + b"".join(encode_string(item) for item in value)
        )

    if shape == "SEQUENCE_OF_SEQUENCE_OF_STRINGS":
        require(isinstance(value, list), "NOT_NESTED_SEQUENCE")
        return (
            b"N" + u64(len(value))
            + b"".join(
                encode_value(item, "SEQUENCE_OF_STRINGS")
                for item in value
            )
        )

    raise RuntimeError("UNKNOWN_SHAPE")


def exact_equal(left, right, shape):
    if shape == "STRING":
        return isinstance(left, str) and isinstance(right, str) and left == right

    if shape == "SEQUENCE_OF_STRINGS":
        return (
            isinstance(left, list)
            and isinstance(right, list)
            and all(isinstance(x, str) for x in left + right)
            and len(left) == len(right)
            and all(a == b for a, b in zip(left, right))
        )

    if shape == "SEQUENCE_OF_SEQUENCE_OF_STRINGS":
        return (
            isinstance(left, list)
            and isinstance(right, list)
            and len(left) == len(right)
            and all(
                exact_equal(a, b, "SEQUENCE_OF_STRINGS")
                for a, b in zip(left, right)
            )
        )

    raise RuntimeError("UNKNOWN_SHAPE")


def canonical_digest(value):
    encoder = json.JSONEncoder(
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    sha = hashlib.sha256()
    for part in encoder.iterencode(value):
        sha.update(part.encode("utf-8"))
    return sha.hexdigest()


def pretty_bytes(value):
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        ) + "\n"
    ).encode("utf-8")


def verify_freeze_identity(contracts):
    freeze = contracts["d46"]
    implementations = freeze["implementation_file_set"]
    require(len(implementations) == 1, "IMPLEMENTATION_FILE_SET_NOT_EXACT")
    item = implementations[0]
    require(
        item["repository_path"] == "scripts/ze2_deterministic_overlap_v1.py",
        "WRONG_IMPLEMENTATION_PATH",
    )
    require(
        sha_file(ROOT / item["repository_path"]) == item["sha256"],
        "IMPLEMENTATION_SHA_MISMATCH",
    )
    require(
        git("hash-object", "--no-filters", item["repository_path"])
        == item["git_blob_oid"],
        "IMPLEMENTATION_BLOB_MISMATCH",
    )



SUCCESSOR_OPERATIONS = [
    "READ_ZE0_MANIFEST_FULL_SCIENTIFIC_PAYLOAD",
    "VERIFY_ZE0_FULL_FILE_SHA256",
    "VERIFY_ZE0_CANDIDATE_IDENTITY_BY_FROZEN_ARTIFACT_ATTESTATION_V1",
    "DERIVE_F0_THROUGH_F6_FROM_EXACT_STORED_schema_v2_property_path_USING_D0323_GRAMMAR",
    "READ_ZE1_INVENTORY_FULL_SCIENTIFIC_PAYLOAD",
    "VERIFY_ZE1_FULL_FILE_SHA256",
    "VERIFY_ZE1_CANONICAL_JSON_SHA256",
    "BEGIN_D0336_EXACT_CANDIDATE_SOURCE_COMPARISON",
]


def verify_d0326_provenance(expected):
    """Read frozen governance metadata only, never ZE0 scientific content."""
    require(sha_file(D0326) == D0326_SHA, "D0326_GOVERNANCE_SHA")
    require(
        git("rev-parse", "HEAD:" + str(D0326.relative_to(ROOT)))
        == D0326_BLOB,
        "D0326_GIT_BLOB",
    )
    evidence = read_json(D0326)
    result = evidence["ZE0_execution_result"]
    identity = evidence["ZE0_output_identity"]
    accounting = evidence["candidate_representation_accounting"]

    require(result["result"] == "SUCCESS", "D0326_RESULT")
    require(result["attempt_completed"] is True, "D0326_COMPLETION")
    require(result["authorization_consumed"] is True, "D0326_CONSUMPTION")
    require(
        identity["manifest_sha256"] == expected["ZE0_manifest_sha256"],
        "D0326_MANIFEST_BINDING",
    )
    require(
        identity["execution_state_sha256"]
        == expected["ZE0_execution_state_sha256"],
        "D0326_EXECUTION_STATE_BINDING",
    )
    require(
        accounting["candidate_manifest_canonical_json_sha256"]
        == expected["ZE0_candidate_canonical_sha256"],
        "D0326_CANDIDATE_IDENTITY_BINDING",
    )
    require(
        accounting["candidate_namespace"] == "SCHEMA_V2_PROPERTY_PATH"
        and accounting["record_count"] == 171
        and accounting["candidate_count"] == 171
        and accounting["representation_forms_per_candidate"] == 7
        and accounting["total_representation_values"] == 1197,
        "D0326_ACCOUNTING",
    )
    return expected["ZE0_manifest_sha256"]


class ConsumedSequenceGate:
    """Reject out-of-order, repeated, or skipped D0344 operations."""

    def __init__(self):
        self.index = 0

    def advance(self, operation):
        require(self.index < len(SUCCESSOR_OPERATIONS), "EXTRA_ZE2_STEP")
        require(
            operation == SUCCESSOR_OPERATIONS[self.index],
            "OUT_OF_ORDER_ZE2_STEP",
        )
        self.index += 1

    def finish(self):
        require(
            self.index == len(SUCCESSOR_OPERATIONS),
            "INCOMPLETE_ZE2_SEQUENCE",
        )


def implemented_successor_operations():
    """Inspect the actual frozen function's literal stage transitions."""
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    target = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "run_ze2"
    )
    calls = []
    for node in ast.walk(target):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "gate"
            and node.func.attr == "advance"
        ):
            require(len(node.args) == 1, "ZE2_STAGE_ARGUMENTS")
            require(
                isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str),
                "ZE2_STAGE_NOT_LITERAL",
            )
            calls.append((node.lineno, node.col_offset, node.args[0].value))
    calls.sort()
    return [item[2] for item in calls]


def exact_remote_main(expected_commit):
    """Read-only exact GitHub main identity; interactive PAT if requested."""
    remote = git("remote", "get-url", "origin")
    require(
        remote == "https://github.com/Umar-2026/SemanticVerify-Fuzz.git",
        "ORIGIN_URL_MISMATCH",
    )
    output = subprocess.check_output(
        [
            "git", "-c", "http.version=HTTP/1.1",
            "ls-remote", "--heads", "origin", "refs/heads/main",
        ],
        cwd=ROOT,
        text=True,
    )
    require(
        output.splitlines()
        == [expected_commit + "\trefs/heads/main"],
        "EXACT_REMOTE_MAIN_READBACK_MISMATCH",
    )


def preflight_identity():
    """No ZE2 output-root existence test or scientific payload access."""
    head = git("rev-parse", "HEAD")
    require(git("branch", "--show-current") == "main", "BRANCH_NOT_MAIN")
    require(
        git("rev-parse", "HEAD^") == D0345_COMMIT,
        "FREEZE_PARENT_NOT_D0345",
    )
    require(not git("status", "--porcelain"), "PREFLIGHT_WORKTREE_DIRTY")
    require(
        git("rev-parse", "HEAD:scripts/ze2_deterministic_overlap_v1.py")
        == git(
            "hash-object", "--no-filters",
            "scripts/ze2_deterministic_overlap_v1.py",
        ),
        "IMPLEMENTATION_NOT_FROZEN_IN_HEAD",
    )
    documents = load_contracts()
    verify_freeze_identity(documents)

    metadata = documents["d45"]["frozen_readiness_metadata_identities"]
    runtime = metadata["runtime_and_repository"]

    require(
        subprocess.check_output(
            ["which", "git-lfs"], text=True
        ).strip() == runtime["git_lfs_path"],
        "PREFLIGHT_GIT_LFS_PATH",
    )
    require(
        subprocess.check_output(
            ["dpkg-query", "-W", "-f=${Version}", "git-lfs"],
            text=True,
        ).strip() == runtime["git_lfs_dpkg_version"],
        "PREFLIGHT_GIT_LFS_VERSION",
    )
    for name, digest in (
        (".git/config", "local_git_config_sha256"),
        (".git/hooks/post-commit", "post_commit_hook_sha256"),
        (".git/hooks/pre-push", "pre_push_hook_sha256"),
    ):
        require(
            sha_file(ROOT / name) == runtime[digest],
            "PREFLIGHT_RUNTIME_IDENTITY:" + name,
        )

    return head


def external_receipt_path(value):
    require(value, "EXTERNAL_RECEIPT_PATH_REQUIRED")
    p = Path(value).resolve()
    require(p.parent.is_dir(), "RECEIPT_PARENT_NOT_DIRECTORY")
    require(
        p != ROOT and ROOT not in p.parents,
        "RECEIPT_MUST_BE_OUTSIDE_REPOSITORY",
    )
    return p


def run_preflight(args):
    """Separate non-consuming transaction, never a readiness retry."""
    require(args.preflight_receipt_path, "PREFLIGHT_RECEIPT_REQUIRED")
    dest = external_receipt_path(args.preflight_receipt_path)
    require(not dest.exists(), "PREFLIGHT_RECEIPT_ALREADY_EXISTS")

    head = preflight_identity()
    exact_remote_main(head)

    record = {
        "evidence_type": "D0345_SEPARATE_NONCONSUMING_TRANSPORT_PREFLIGHT",
        "result": "PASS",
        "freeze_commit": head,
        "parent_D0345_commit": D0345_COMMIT,
        "remote_main": head,
        "implementation_sha256": sha_file(Path(__file__)),
        "transaction_nonce": secrets.token_hex(24),
        "readiness_attempt_started": False,
        "ZE2_execution_started": False,
    }
    body = pretty_bytes(record)

    # Separate preflight evidence outside the Git repository.
    fd = os.open(
        str(dest),
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o600,
    )
    with os.fdopen(fd, "wb") as stream:
        stream.write(body)
        stream.flush()
        os.fsync(stream.fileno())

    print("D0345_TRANSPORT_PREFLIGHT=PASS", flush=True)
    print("PREFLIGHT_RECEIPT_PATH=" + str(dest), flush=True)
    print("READINESS_AUTHORIZATION_CONSUMED=NO", flush=True)
    print("ZE2_AUTHORIZATION_LINEAGE_CONSUMED=NO", flush=True)


def verify_preflight_receipt(path_value):
    path = external_receipt_path(path_value)
    require(not path.is_symlink(), "PREFLIGHT_RECEIPT_SYMLINK")
    info = path.stat()
    require(stat.S_ISREG(info.st_mode), "PREFLIGHT_RECEIPT_NOT_FILE")
    require(info.st_uid == os.getuid(), "PREFLIGHT_RECEIPT_OWNER")
    require(info.st_mode & 0o077 == 0, "PREFLIGHT_RECEIPT_PERMISSIONS")

    record = read_json(path)
    head = git("rev-parse", "HEAD")
    require(
        record["evidence_type"]
        == "D0345_SEPARATE_NONCONSUMING_TRANSPORT_PREFLIGHT",
        "PREFLIGHT_EVIDENCE_TYPE",
    )
    require(record["result"] == "PASS", "PREFLIGHT_NOT_PASS")
    require(
        record["freeze_commit"] == head
        and record["remote_main"] == head
        and record["parent_D0345_commit"] == D0345_COMMIT,
        "PREFLIGHT_COMMIT_BINDING",
    )
    require(
        isinstance(record.get("transaction_nonce"), str)
        and len(record["transaction_nonce"]) == 48,
        "PREFLIGHT_NONCE",
    )
    require(
        record["implementation_sha256"] == sha_file(Path(__file__)),
        "PREFLIGHT_IMPLEMENTATION_BINDING",
    )
    require(
        record["readiness_attempt_started"] is False
        and record["ZE2_execution_started"] is False,
        "PREFLIGHT_TRANSACTION_FIREWALL",
    )
    require(
        git("rev-parse", "HEAD^") == D0345_COMMIT,
        "FREEZE_PARENT_BINDING",
    )

    # The local receipt is not accepted as independent remote proof.
    # Re-establish current exact origin/main identity before the
    # one-shot readiness authorization may be consumed.
    exact_remote_main(head)
    return path


class ReadinessReadGuard:
    """Default-deny local file reads throughout the readiness call path."""

    def __init__(self, receipt):
        allowed = [
            D36, D37, D43, D44, D45, D46,
            D0326,
            Path(__file__),
            receipt,
            ROOT / ".git/config",
            ROOT / ".git/hooks/post-commit",
            ROOT / ".git/hooks/pre-push",
        ]
        self.allowed = {p.resolve() for p in allowed}
        self.denied_count = 0
        self.checked_file_opens = 0

    def install(self):
        guard = self
        guard.checked_subprocesses = 0
        guard.subprocess_denied_count = 0

        ze0_git_path = str(ZE0.relative_to(ROOT))
        ze1_git_path = str(ZE1.relative_to(ROOT))

        allowed_git_commands = {
            (
                "git", "merge-base", D0344_COMMIT, "HEAD",
            ),
            (
                "git", "rev-parse", "HEAD:" + ze0_git_path,
            ),
            (
                "git", "rev-parse", "HEAD:" + ze1_git_path,
            ),
            (
                "git", "show", "HEAD:" + ze1_git_path,
            ),
            (
                "git", "hash-object", "--no-filters",
                "scripts/ze2_deterministic_overlap_v1.py",
            ),
        }

        allowed_runtime_commands = {
            ("which", "git-lfs"),
            ("dpkg-query", "-W", "-f=${Version}", "git-lfs"),
        }

        def audit(event, args):
            if event == "open":
                file = args[0]

                guard.checked_file_opens += 1

                if not isinstance(
                    file, (str, bytes, os.PathLike)
                ):
                    guard.denied_count += 1
                    raise RuntimeError(
                        "READINESS_NONPATH_FILE_OPEN_DENIED"
                    )

                resolved = Path(file).resolve()

                if resolved not in guard.allowed:
                    guard.denied_count += 1
                    raise RuntimeError(
                        "READINESS_FILE_FIREWALL_DENIED:"
                        + str(resolved)
                    )

            elif event == "subprocess.Popen":
                argv = args[1]

                if not isinstance(argv, (tuple, list)):
                    guard.subprocess_denied_count += 1
                    raise RuntimeError(
                        "READINESS_NONARGV_SUBPROCESS_DENIED"
                    )

                command = tuple(
                    os.fsdecode(part) for part in argv
                )

                guard.checked_subprocesses += 1

                if (
                    command not in allowed_git_commands
                    and command not in allowed_runtime_commands
                ):
                    guard.subprocess_denied_count += 1
                    raise RuntimeError(
                        "READINESS_SUBPROCESS_DENIED:"
                        + repr(command)
                    )

        # Audit hooks are process-lifetime controls and cannot
        # be silently removed. Readiness is a terminal process.
        sys.addaudithook(audit)


def verify_d0336_output_contract(d36):
    output = d36["reserved_future_output_contract"]
    matrix = d36["overlap_contract"]["compatibility_matrix"]
    require(len(matrix) == 7, "COMPATIBILITY_COUNT")
    require([x["id"] for x in matrix] == FORMS, "COMPATIBILITY_ORDER")

    shapes = [
        "STRING", "SEQUENCE_OF_STRINGS", "STRING",
        "SEQUENCE_OF_STRINGS", "SEQUENCE_OF_STRINGS",
        "SEQUENCE_OF_SEQUENCE_OF_STRINGS",
        "SEQUENCE_OF_SEQUENCE_OF_STRINGS",
    ]
    scopes = [
        "FULL_SOURCE_ATOM",
        "FULL_SOURCE_ATOM_SEGMENT_SEQUENCE",
        "EACH_SOURCE_DOT_SEGMENT",
        "EACH_CONTIGUOUS_TWO_SEGMENT_WINDOW",
        "EACH_SOURCE_DOT_SEGMENT",
        "EACH_CONTIGUOUS_TWO_SEGMENT_WINDOW",
        "FULL_SOURCE_ATOM_SEGMENT_TOKEN_SEQUENCE",
    ]
    relations = [
        "EXACT_STRING_EQUALITY",
        "EXACT_SEQUENCE_EQUALITY",
        "EXACT_STRING_EQUALITY",
        "EXACT_SEQUENCE_EQUALITY",
        "EXACT_SEQUENCE_EQUALITY",
        "EXACT_NESTED_SEQUENCE_EQUALITY",
        "EXACT_NESTED_SEQUENCE_EQUALITY",
    ]

    surfaces = [
        "ZE1-SF0-RAW-ATOM",
        "ZE1-SF1-DOT-SEGMENT-SEQUENCE",
        "ZE1-SF1-DOT-SEGMENT",
        "ZE1-SF1-DOT-SEGMENT-SEQUENCE",
        "ZE1-SF2-LEXICAL-TOKENS",
        "ZE1-SF2-LEXICAL-TOKEN-SEQUENCES",
        "ZE1-SF2-LEXICAL-TOKEN-SEQUENCES",
    ]

    for row, shape, scope, relation, surface in zip(
        matrix, shapes, scopes, relations, surfaces
    ):
        require(
            set(row) == {
                "id", "relation", "shape",
                "source_scope", "source_surface",
            },
            "COMPATIBILITY_EXACT_FIELDS",
        )
        require(row["shape"] == shape, "COMPATIBILITY_SHAPE")
        require(row["source_scope"] == scope, "COMPATIBILITY_SCOPE")
        require(
            row["relation"] == relation,
            "COMPATIBILITY_EXACT_RELATION",
        )
        require(
            row["source_surface"] == surface,
            "COMPATIBILITY_EXACT_SOURCE_SURFACE",
        )

    expected_locators = [
        {
            "dot_segment_start_ordinal": None,
            "dot_segment_end_ordinal": None,
            "meaning": "FULL_ATOM_LOCATED_BY_SOURCE_ATOM_LOCATOR",
        },
        {
            "dot_segment_start_ordinal": "FIRST_SEGMENT_ORDINAL",
            "dot_segment_end_ordinal": "LAST_SEGMENT_ORDINAL",
            "meaning": "FULL_ATOM_DOT_SEGMENT_SEQUENCE",
        },
        {
            "dot_segment_start_ordinal": "MATCHED_SEGMENT_ORDINAL",
            "dot_segment_end_ordinal": "SAME_AS_START",
            "meaning": "SINGLE_DOT_SEGMENT",
        },
        {
            "dot_segment_start_ordinal": "WINDOW_FIRST_SEGMENT_ORDINAL",
            "dot_segment_end_ordinal": "START_PLUS_ONE",
            "meaning": "ADJACENT_TWO_SEGMENT_WINDOW",
        },
        {
            "dot_segment_start_ordinal": "MATCHED_SEGMENT_ORDINAL",
            "dot_segment_end_ordinal": "SAME_AS_START",
            "meaning": "SINGLE_SEGMENT_LEXICAL_TOKEN_SEQUENCE",
        },
        {
            "dot_segment_start_ordinal": "WINDOW_FIRST_SEGMENT_ORDINAL",
            "dot_segment_end_ordinal": "START_PLUS_ONE",
            "meaning": "ADJACENT_TWO_SEGMENT_LEXICAL_TOKEN_SEQUENCES",
        },
        {
            "dot_segment_start_ordinal": "FIRST_SEGMENT_ORDINAL",
            "dot_segment_end_ordinal": "LAST_SEGMENT_ORDINAL",
            "meaning": "FULL_ATOM_SEGMENT_LEXICAL_TOKEN_SEQUENCE",
        },
    ]

    frozen_locators = output[
        "source_locator_semantics_by_representation_id"
    ]

    for form_id, expected in zip(FORMS, expected_locators):
        require(
            frozen_locators[form_id] == expected,
            "FROZEN_SOURCE_LOCATOR_SEMANTICS:" + form_id,
        )

    require(
        output["candidate_form_record_order"]["representation_order"]
        == FORMS,
        "FORM_OUTPUT_ORDER",
    )
    require(
        output["expected_candidate_form_record_count"] == 1197,
        "FORM_OUTPUT_COUNT",
    )
    require(
        output["source_occurrence_match_order"]["keys"]
        == [
            "source_ordinal", "atom_ordinal",
            "dot_segment_start_ordinal", "dot_segment_end_ordinal",
        ],
        "MATCH_SORT_ORDER",
    )
    require(
        output["source_occurrence_match_order"][
            "null_sort_key_value_for_ordering_only"
        ] == 0,
        "NULL_MATCH_SORT",
    )
    require(
        set(output["source_occurrence_match_fields"])
        == set(output["source_occurrence_match_schema"]["required_fields"]),
        "SOURCE_MATCH_SCHEMA",
    )
    require(
        set(output["match_record_fields"])
        == set(output["candidate_form_record_schema"]["required_fields"]),
        "CANDIDATE_FORM_SCHEMA",
    )
    require(
        set(output["manifest_top_level_schema"])
        == {
            "artifact_type", "candidate_form_record_order",
            "candidate_form_records",
            "candidate_representation_value_hash_contract_id",
            "contract_id", "execution_id",
            "frozen_input_identity",
            "scientific_interpretation_boundary",
            "serialization_contract_id",
        },
        "MANIFEST_TOP_LEVEL_SCHEMA",
    )
    require(
        output["serialization_contract"]["encoding"] == "UTF-8"
        and output["serialization_contract"]["sort_keys"] is True
        and output["serialization_contract"]["ensure_ascii"] is False
        and output["serialization_contract"]["indent"] == 2
        and output["serialization_contract"]["final_newline"] is True
        and output["serialization_contract"]["allow_nan"] is False,
        "OUTPUT_SERIALIZATION",
    )
    require(
        len(output["source_locator_semantics_by_representation_id"]) == 7
        and set(output["source_locator_semantics_by_representation_id"])
        == set(FORMS),
        "SOURCE_LOCATOR_SCHEMA",
    )
    require(
        set(output["execution_state_schema"]["required_top_level_fields"])
        == {
            "authorization_id", "candidate_form_record_count",
            "candidate_record_count", "contract_id", "execution_id",
            "input_identity_verification", "nonzero_match_record_count",
            "output_hashes", "per_representation_match_summary",
            "scientific_interpretation_boundary",
            "serialization_contract_id", "status",
            "total_source_occurrence_match_count",
            "zero_match_record_count",
        },
        "EXECUTION_STATE_TOP_LEVEL_SCHEMA",
    )
    return True


def validate_ze2_result_objects(d36, manifest, state):
    output = d36["reserved_future_output_contract"]
    require(
        set(manifest) == set(output["manifest_top_level_schema"]),
        "MANIFEST_EXACT_FIELDS",
    )
    require(
        set(state)
        == set(output["execution_state_schema"]["required_top_level_fields"]),
        "EXECUTION_STATE_EXACT_FIELDS",
    )
    records = manifest["candidate_form_records"]
    require(len(records) == 1197, "OUTPUT_RECORD_COUNT")
    require(
        state["candidate_record_count"] == 171
        and state["candidate_form_record_count"] == 1197,
        "OUTPUT_ACCOUNTING",
    )
    fields = set(output["candidate_form_record_schema"]["required_fields"])
    matchfields = set(output["source_occurrence_match_fields"])
    locatorfields = {
        "source_member_id", "atom_ordinal",
        "start_character_offset_zero_based",
        "end_character_offset_exclusive",
        "start_line_one_based", "start_column_one_based",
    }
    shapes = {
        row["id"]: row["shape"]
        for row in d36["overlap_contract"]["compatibility_matrix"]
    }
    surfaces = {
        row["id"]: row["source_surface"]
        for row in d36["overlap_contract"]["compatibility_matrix"]
    }
    all_count = 0
    for i, record in enumerate(records):
        require(set(record) == fields, "CANDIDATE_RECORD_FIELDS")
        require(
            record["candidate_index"] == i // 7 + 1
            and record["representation_id"] == FORMS[i % 7],
            "CANDIDATE_RECORD_ORDER",
        )
        require(
            record["candidate_representation_value_sha256"]
            == hashlib.sha256(
                encode_value(
                    record["candidate_representation_value"],
                    shapes[record["representation_id"]],
                )
            ).hexdigest(),
            "CANDIDATE_VALUE_DIGEST",
        )
        matches = record["source_occurrence_matches"]
        require(
            record["match_count"] == len(matches),
            "MATCH_COUNT_INVARIANT",
        )
        previous = None
        for match in matches:
            require(set(match) == matchfields, "MATCH_FIELDS")
            require(
                set(match["source_atom_locator"]) == locatorfields,
                "SOURCE_ATOM_LOCATOR_FIELDS",
            )
            require(
                match["source_surface"]
                == surfaces[record["representation_id"]],
                "MATCH_SOURCE_SURFACE",
            )
            key = (
                match["source_ordinal"],
                match["atom_ordinal"],
                match["dot_segment_start_ordinal"] or 0,
                match["dot_segment_end_ordinal"] or 0,
            )
            require(previous is None or previous <= key, "MATCH_ORDER")
            previous = key
        all_count += len(matches)

    require(
        all_count == state["total_source_occurrence_match_count"],
        "TOTAL_MATCH_COUNT",
    )
    require(
        state["zero_match_record_count"]
        + state["nonzero_match_record_count"] == 1197,
        "ZERO_NONZERO_COUNT",
    )
    require(
        len(state["per_representation_match_summary"]) == 7,
        "REPRESENTATION_SUMMARY_COUNT",
    )
    require(
        state["authorization_id"] == ZE2_AUTH,
        "ZE2_AUTHORIZATION_ID_OUTPUT",
    )
    require(
        all(v is False for v in manifest["scientific_interpretation_boundary"].values())
        and all(v is False for v in state["scientific_interpretation_boundary"].values()),
        "SCIENTIFIC_BOUNDARY_OUTPUT",
    )


def verify_effective_readiness_result(args):
    require(
        args.effective_readiness_result_commit,
        "READINESS_RESULT_COMMIT_REQUIRED",
    )
    require(
        args.readiness_result_artifact,
        "READINESS_RESULT_ARTIFACT_REQUIRED",
    )
    head = git("rev-parse", "HEAD")
    require(
        head == args.effective_readiness_result_commit,
        "READINESS_RESULT_LOCAL_HEAD_MISMATCH",
    )
    require(not git("status", "--porcelain"), "ZE2_WORKTREE_DIRTY")
    require(
        git("branch", "--show-current") == "main",
        "ZE2_NOT_MAIN",
    )
    rel = Path(args.readiness_result_artifact)
    require(
        not rel.is_absolute()
        and ".." not in rel.parts
        and rel.parts[:2] == (
            "evaluation", "governance_reconciliation",
        ),
        "READINESS_RESULT_ARTIFACT_PATH",
    )
    require(
        rel.is_file() and not rel.is_symlink(),
        "READINESS_RESULT_ARTIFACT_MISSING",
    )
    committed = git("show", "HEAD:" + rel.as_posix())
    require(
        committed == rel.read_text(encoding="utf-8").strip(),
        "READINESS_RESULT_COMMITTED_BYTES_MISMATCH",
    )
    result = json.loads(committed)
    require(result["readiness_result"] == "PASS", "READINESS_NOT_PASS")
    require(
        result["readiness_authorization_id"] == READINESS_AUTH,
        "READINESS_RESULT_AUTHORIZATION",
    )
    require(
        result["readiness_authorization_consumed"] is True
        and result["remaining_readiness_attempt_capacity"] == 0,
        "READINESS_RESULT_CONSUMPTION",
    )
    require(
        result["required_check_count"] == 15
        and result["passed_check_count"] == 15
        and result["failed_check_count"] == 0,
        "READINESS_RESULT_CHECK_ACCOUNTING",
    )
    require(
        result.get("passed_check_ids") == READY_CHECKS
        and result["passed_check_ids"]
        == load_contracts()["d45"][
            "closed_required_check_set"
        ]["checks"],
        "READINESS_RESULT_FULL_CHECK_IDENTITY",
    )
    freeze_commit = result["implementation_freeze_commit"]
    require(
        git("rev-parse", freeze_commit + "^") == D0345_COMMIT,
        "READINESS_RESULT_FREEZE_PARENT",
    )
    require(
        git("merge-base", freeze_commit, head) == freeze_commit,
        "READINESS_RESULT_FREEZE_ANCESTRY",
    )

    exact_remote_main(head)
    return result



def attest_ze0(manifest, expected, provenance_binding_established):
    require(
        provenance_binding_established == expected["ZE0_manifest_sha256"],
        "D0326_ATTESTATION_BINDING_MISSING",
    )
    require(type(manifest) is dict, "ZE0_MANIFEST_NOT_OBJECT")

    fixed = {
        "artifact_type": "SVF_ZE0_CANDIDATE_REPRESENTATION_MANIFEST_V1",
        "contract_id": "SVF-ZE0-CANDIDATE-REPRESENTATION-MANIFEST-CONTRACT-V1",
        "candidate_namespace": "SCHEMA_V2_PROPERTY_PATH",
        "candidate_manifest_canonical_json_sha256":
            expected["ZE0_candidate_canonical_sha256"],
        "record_count": 171,
    }
    for key, value in fixed.items():
        require(manifest.get(key) == value, "ZE0_ATTESTATION_" + key)

    records = manifest.get("records")
    require(isinstance(records, list) and len(records) == 171, "ZE0_RECORD_COUNT")
    seen = set()

    for ordinal, record in enumerate(records, 1):
        require(type(record) is dict, "ZE0_RECORD_NOT_OBJECT")
        require(type(record.get("candidate_ordinal")) is int, "ZE0_ORDINAL_TYPE")
        require(record["candidate_ordinal"] == ordinal, "ZE0_ORDINAL_ORDER")

        name = record.get("schema_v2_property_path")
        require(isinstance(name, str), "ZE0_PROPERTY_PATH_TYPE")
        require(name not in seen, "ZE0_DUPLICATE_PROPERTY_PATH")
        seen.add(name)

        require(
            record.get("representation_grammar_id") == "SVF-ZE0-DET-REP-GRAMMAR-V1",
            "ZE0_GRAMMAR_ID",
        )
        require("representations" in record, "ZE0_REPRESENTATIONS_MISSING")

    return records


def source_values(atom, form_ids):
    raw = atom["raw_atom"]
    dots = atom["dot_segments"]
    segments = [x["raw_segment"] for x in dots]
    tokens = [
        [t["token"] for t in d["lexical_tokens"]]
        for d in dots
    ]
    count = len(dots)

    require(count >= 1, "EMPTY_SOURCE_DOT_SEQUENCE")
    yield form_ids[0], raw, None, None
    yield form_ids[1], segments, 1, count

    for i, (segment, tok) in enumerate(zip(segments, tokens), 1):
        require(dots[i - 1]["dot_segment_ordinal"] == i, "DOT_ORDINAL_MISMATCH")
        yield form_ids[2], segment, i, i
        yield form_ids[4], tok, i, i

    for i in range(count - 1):
        yield form_ids[3], segments[i:i + 2], i + 1, i + 2
        yield form_ids[5], tokens[i:i + 2], i + 1, i + 2

    yield form_ids[6], tokens, 1, count


def match_candidates(records, ze1, matrix):
    by_key = {}
    shapes = {row["id"]: row["shape"] for row in matrix}
    surfaces = {row["id"]: row["source_surface"] for row in matrix}

    for index, record in enumerate(records):
        representation_id = record["representation_id"]
        key = (
            representation_id,
            encode_value(record["candidate_representation_value"],
                         shapes[representation_id]),
        )
        by_key.setdefault(key, []).append(index)

    expected_sources = ["C1-S01", "C1-S02", "C1-S03", "C1-S04"]
    source_records = ze1["source_records"]

    require(len(source_records) == 4, "SOURCE_RECORD_COUNT_NOT_FOUR")

    for ordinal, source in enumerate(source_records, 1):
        require(source["source_ordinal"] == ordinal, "SOURCE_ORDER")
        require(
            source["source_member_id"] == expected_sources[ordinal - 1],
            "SOURCE_MEMBER_ORDER",
        )

        for atom_ordinal, atom in enumerate(source["atom_occurrences"], 1):
            require(atom["atom_ordinal"] == atom_ordinal, "ATOM_ORDER")
            locator = atom["source_atom_locator"]

            for form_id, value, start, end in source_values(atom, FORMS):
                key = (form_id, encode_value(value, shapes[form_id]))

                for candidate_i in by_key.get(key, ()):
                    record = records[candidate_i]
                    if not exact_equal(
                        record["candidate_representation_value"],
                        value,
                        shapes[form_id],
                    ):
                        continue

                    record["source_occurrence_matches"].append({
                        "source_member_id": source["source_member_id"],
                        "source_ordinal": ordinal,
                        "atom_ordinal": atom_ordinal,
                        "source_atom_locator": locator,
                        "source_surface": surfaces[form_id],
                        "dot_segment_start_ordinal": start,
                        "dot_segment_end_ordinal": end,
                    })

    for record in records:
        matches = record["source_occurrence_matches"]
        matches.sort(key=lambda x: (
            x["source_ordinal"],
            x["atom_ordinal"],
            x["dot_segment_start_ordinal"]
                if x["dot_segment_start_ordinal"] is not None else 0,
            x["dot_segment_end_ordinal"]
                if x["dot_segment_end_ordinal"] is not None else 0,
        ))
        record["match_count"] = len(matches)


def candidate_form_records(ze0_records, matrix):
    records = []
    for item in ze0_records:
        candidate_index = item["candidate_ordinal"]
        values = derive_forms(item["schema_v2_property_path"])

        for row, value in zip(matrix, values):
            records.append({
                "candidate_index": candidate_index,
                "representation_id": row["id"],
                "candidate_representation_value": value,
                "candidate_representation_value_sha256":
                    hashlib.sha256(encode_value(value, row["shape"])).hexdigest(),
                "match_count": 0,
                "source_occurrence_matches": [],
            })

    require(len(records) == 1197, "CANDIDATE_FORM_COUNT")
    return records


def check_synthetic_serializer(d37):
    contract = d37["postpublication_nonconsuming_preexecution_reconciliation"][
        "synthetic_conformance_contract"
    ]
    vectors = contract["candidate_value_serializer_vectors"]
    require(len(vectors) == 11, "SERIALIZER_VECTOR_COUNT")
    for vector in vectors:
        actual = encode_value(vector["value"], vector["value_type"])
        require(actual.hex() == vector["expected_serialized_hex"],
                "SERIALIZER_BYTES_" + vector["vector_id"])
        require(hashlib.sha256(actual).hexdigest() == vector["expected_sha256"],
                "SERIALIZER_SHA_" + vector["vector_id"])


def check_synthetic_matcher(d37):
    contract = d37["postpublication_nonconsuming_preexecution_reconciliation"][
        "synthetic_conformance_contract"
    ]
    vectors = contract["exact_matcher_vectors"]
    require(len(vectors) == 12, "MATCHER_VECTOR_COUNT")
    for vector in vectors:
        require(
            exact_equal(vector["left"], vector["right"], vector["shape"])
            is vector["expected_match"],
            "MATCHER_" + vector["vector_id"],
        )


def run_readiness(args):
    receipt = verify_preflight_receipt(args.preflight_receipt_path)
    guard = ReadinessReadGuard(receipt)
    guard.install()

    docs = load_contracts()
    verify_freeze_identity(docs)
    d36, d37, d43, d44, d45 = (
        docs["d36"], docs["d37"], docs["d43"], docs["d44"], docs["d45"]
    )
    ids = d45["frozen_readiness_metadata_identities"]
    matrix = d36["overlap_contract"]["compatibility_matrix"]
    required = d45["closed_required_check_set"]["checks"]
    require(required == READY_CHECKS, "FROZEN_READINESS_CHECK_ORDER")

    # This is the irreversible boundary. No synthetic/check execution
    # precedes this point.
    print("D0345_READINESS_ATTEMPT_STARTED=YES", flush=True)
    print("D0345_READINESS_AUTHORIZATION_CONSUMED=YES", flush=True)
    print("D0345_REMAINING_READINESS_ATTEMPT_CAPACITY=0", flush=True)

    def check(number):
        if number == 1:
            require(
                git("merge-base", D0344_COMMIT, "HEAD") == D0344_COMMIT,
                "D0344_NOT_ANCESTOR",
            )
            require(d44["authorization_lineage"]["successor_authorization_id"]
                    == ZE2_AUTH, "D0344_AUTH_BINDING")

        elif number == 2:
            require(
                d43["gap_A_prospective_correction"]["candidate_record_count"] == 171
                and d43["gap_A_prospective_correction"]["representation_order"] == FORMS,
                "D0343_BINDING",
            )

        elif number == 3:
            require(
                d44["D0340_binding"]["candidate_index_binding"]
                == "candidate_index := candidate_ordinal",
                "D0340_BINDING",
            )

        elif number == 4:
            require(
                len(matrix) == 7
                and [x["id"] for x in matrix] == FORMS
                and d36["reserved_future_output_contract"][
                    "expected_candidate_form_record_count"
                ] == 1197,
                "D0336_CONTRACT_BINDING",
            )
            require(
                verify_d0336_output_contract(d36),
                "D0336_FULL_OUTPUT_CONTRACT",
            )

        elif number == 5:
            z = ids["ZE0"]
            path = z["manifest_path"]
            require(
                git("rev-parse", "HEAD:" + path)
                == z["manifest_git_blob_oid"],
                "ZE0_GIT_BLOB",
            )

        elif number == 6:
            z = ids["ZE1"]
            path = z["inventory_path"]
            require(
                git("rev-parse", "HEAD:" + path)
                == z["inventory_pointer_git_blob_oid"],
                "ZE1_GIT_POINTER_BLOB",
            )
            pointer = git("show", "HEAD:" + path)
            require(
                "oid sha256:" + z["inventory_lfs_oid_sha256"] in pointer
                and "size " + str(z["inventory_lfs_size"]) in pointer,
                "ZE1_LFS_POINTER",
            )

        elif number == 7:
            r = ids["runtime_and_repository"]
            require(
                subprocess.check_output(["which", "git-lfs"], text=True).strip()
                == r["git_lfs_path"], "GIT_LFS_PATH",
            )
            version = subprocess.check_output(
                ["dpkg-query", "-W", "-f=${Version}", "git-lfs"],
                text=True,
            ).strip()
            require(version == r["git_lfs_dpkg_version"], "GIT_LFS_VERSION")
            for path, expected in (
                (ROOT / ".git/config", r["local_git_config_sha256"]),
                (ROOT / ".git/hooks/post-commit", r["post_commit_hook_sha256"]),
                (ROOT / ".git/hooks/pre-push", r["pre_push_hook_sha256"]),
            ):
                require(sha_file(path) == expected, "RUNTIME_HASH:" + str(path))

        elif number == 8:
            require(not ZE2_ROOT.exists(), "ZE2_OUTPUT_ROOT_EXISTS")

        elif number == 9:
            expected = d36["reserved_future_output_contract"][
                "manifest_frozen_input_identity_schema"
            ]["exact_values"]
            fake = {
                "artifact_type": "SVF_ZE0_CANDIDATE_REPRESENTATION_MANIFEST_V1",
                "contract_id":
                    "SVF-ZE0-CANDIDATE-REPRESENTATION-MANIFEST-CONTRACT-V1",
                "candidate_namespace": "SCHEMA_V2_PROPERTY_PATH",
                "candidate_manifest_canonical_json_sha256":
                    expected["ZE0_candidate_canonical_sha256"],
                "record_count": 171,
                "records": [
                    {
                        "candidate_ordinal": i,
                        "schema_v2_property_path": "synthetic_" + str(i),
                        "representation_grammar_id":
                            "SVF-ZE0-DET-REP-GRAMMAR-V1",
                        "representations": None,
                    }
                    for i in range(1, 172)
                ],
            }
            require(
                len(attest_ze0(
                    fake,
                    expected,
                    expected["ZE0_manifest_sha256"],
                )) == 171,
                "ATTESTATION_SYNTHETIC",
            )

        elif number == 10:
            values = derive_forms("HTTPServer.start_2")
            require(
                values == [
                    "HTTPServer.start_2",
                    ["HTTPServer", "start_2"],
                    "start_2",
                    ["HTTPServer", "start_2"],
                    ["start", "2"],
                    [["http", "server"], ["start", "2"]],
                    [["http", "server"], ["start", "2"]],
                ],
                "F0_F6_SYNTHETIC_REGENERATION",
            )
            require(derive_forms("a.")[-1] == [["a"], []],
                    "EMPTY_FINAL_SEGMENT")

        elif number == 11:
            check_synthetic_serializer(d37)

        elif number == 12:
            check_synthetic_matcher(d37)

        elif number == 13:
            operations = [
                row["operation"]
                for row in d44["successor_consumed_execution_sequence"]
            ]
            require(operations == [
                "READ_ZE0_MANIFEST_FULL_SCIENTIFIC_PAYLOAD",
                "VERIFY_ZE0_FULL_FILE_SHA256",
                "VERIFY_ZE0_CANDIDATE_IDENTITY_BY_FROZEN_ARTIFACT_ATTESTATION_V1",
                "DERIVE_F0_THROUGH_F6_FROM_EXACT_STORED_schema_v2_property_path_USING_D0323_GRAMMAR",
                "READ_ZE1_INVENTORY_FULL_SCIENTIFIC_PAYLOAD",
                "VERIFY_ZE1_FULL_FILE_SHA256",
                "VERIFY_ZE1_CANONICAL_JSON_SHA256",
                "BEGIN_D0336_EXACT_CANDIDATE_SOURCE_COMPARISON",
            ], "SUCCESSOR_SEQUENCE")
            require(
                implemented_successor_operations() == SUCCESSOR_OPERATIONS,
                "IMPLEMENTED_SUCCESSOR_OPERATION_ORDER",
            )

        elif number == 14:
            require(
                d44["ZE2_execution_state_authorization_id_binding"]["required_value"]
                == ZE2_AUTH,
                "ZE2_STATE_AUTHORIZATION_ID",
            )

        elif number == 15:
            # The readiness path has no ZE0/ZE1 scientific payload reads.
            require(
                guard.denied_count == 0
                and guard.checked_file_opens > 0
                and guard.subprocess_denied_count == 0
                and guard.checked_subprocesses > 0,
                "READINESS_SCIENTIFIC_FIREWALL",
            )

        else:
            raise RuntimeError("UNKNOWN_READINESS_CHECK")

    for number, label in enumerate(required, 1):
        try:
            check(number)
        except Exception:
            print("READINESS_CHECK_FAILED=" + label, flush=True)
            print("D0345_READINESS_RESULT=FAIL_CONSUMED_NO_RETRY", flush=True)
            raise
        print("PASS | " + label, flush=True)

    print("D0345_READINESS_RESULT=PASS_CONSUMED", flush=True)
    print("ZE2_EXECUTION_GO=NO_PENDING_SEPARATE_RESULT_CHECKPOINT", flush=True)


def run_ze2(args):
    require(args.ack_one_shot_consumption, "EXPLICIT_ONE_SHOT_ACK_REQUIRED")
    readiness_result = verify_effective_readiness_result(args)
    docs = load_contracts()
    verify_freeze_identity(docs)
    d36 = docs["d36"]
    d43 = docs["d43"]
    d44 = docs["d44"]

    require(
        d44["ZE2_execution_state_authorization_id_binding"]["required_value"]
        == ZE2_AUTH,
        "SUCCESSOR_ZE2_AUTHORIZATION_BINDING",
    )
    require(
        d43["gap_A_prospective_correction"]["representation_order"] == FORMS,
        "REPRESENTATION_ORDER",
    )

    output = d36["reserved_future_output_contract"]
    frozen = output["manifest_frozen_input_identity_schema"]["exact_values"]
    matrix = d36["overlap_contract"]["compatibility_matrix"]
    require([row["id"] for row in matrix] == FORMS, "COMPATIBILITY_ORDER")

    require(sha_file(ZE0_STATE) == frozen["ZE0_execution_state_sha256"],
            "ZE0_STATE_IDENTITY")
    require(sha_file(ZE1_STATE) == frozen["ZE1_execution_state_sha256"],
            "ZE1_STATE_IDENTITY")

    gate = ConsumedSequenceGate()
    gate.advance("READ_ZE0_MANIFEST_FULL_SCIENTIFIC_PAYLOAD")

    # Conservative, irreversible accounting is emitted BEFORE first read.
    # A process interruption cannot make a partially started read appear
    # safe to retry. The actual D0344 trigger remains first payload read.
    print("ZE2_FIRST_SCIENTIFIC_READ_IMMINENT=YES", flush=True)
    print("ZE2_AUTHORIZATION_LINEAGE_CONSUMED=YES", flush=True)
    print("ZE2_REMAINING_ATTEMPT_CAPACITY=0", flush=True)

    with open(ZE0, "rb") as handle:
        ze0_bytes = handle.read()

    gate.advance("VERIFY_ZE0_FULL_FILE_SHA256")
    require(
        hashlib.sha256(ze0_bytes).hexdigest()
        == frozen["ZE0_manifest_sha256"],
        "ZE0_FULL_FILE_SHA",
    )

    # D0344 step 3: prospective frozen-artifact attestation.
    gate.advance(
        "VERIFY_ZE0_CANDIDATE_IDENTITY_BY_FROZEN_ARTIFACT_ATTESTATION_V1"
    )
    ze0 = json.loads(ze0_bytes.decode("utf-8"))

    attestation_contract = d43["gap_B_prospective_correction"]
    require(
        attestation_contract["verification_semantics"]
        == "PROSPECTIVE_FROZEN_ARTIFACT_ATTESTATION",
        "ATTESTATION_GOVERNANCE",
    )
    require(
        attestation_contract["required_attestation_checks"][-1]["field"]
        == "D0326_provenance_attestation",
        "D0326_PROVENANCE_CONTRACT",
    )
    provenance = verify_d0326_provenance(frozen)
    ze0_records = attest_ze0(ze0, frozen, provenance)

    gate.advance(
        "DERIVE_F0_THROUGH_F6_FROM_EXACT_STORED_schema_v2_property_path_USING_D0323_GRAMMAR"
    )
    records = candidate_form_records(ze0_records, matrix)

    # D0344 ordered operations 5 and 6.
    gate.advance("READ_ZE1_INVENTORY_FULL_SCIENTIFIC_PAYLOAD")
    print("ZE2_CONSUMING_ZE1_SCIENTIFIC_READ_START=YES", flush=True)
    ze1_sha = sha_file(ZE1)

    gate.advance("VERIFY_ZE1_FULL_FILE_SHA256")
    require(
        ze1_sha == frozen["ZE1_inventory_file_sha256"],
        "ZE1_FULL_FILE_SHA",
    )

    gate.advance("VERIFY_ZE1_CANONICAL_JSON_SHA256")
    ze1 = read_json(ZE1)
    require(
        canonical_digest(ze1)
        == frozen["ZE1_inventory_canonical_json_sha256"],
        "ZE1_CANONICAL_JSON_SHA",
    )

    gate.advance("BEGIN_D0336_EXACT_CANDIDATE_SOURCE_COMPARISON")
    match_candidates(records, ze1, matrix)
    gate.finish()

    require(not ZE2_ROOT.exists(), "ZE2_ROOT_ALREADY_EXISTS")

    zero = sum(r["match_count"] == 0 for r in records)
    nonzero = len(records) - zero
    total = sum(r["match_count"] for r in records)

    summary = []
    for form_id in FORMS:
        subset = [r for r in records if r["representation_id"] == form_id]
        summary.append({
            "representation_id": form_id,
            "candidate_form_record_count": len(subset),
            "zero_match_record_count":
                sum(r["match_count"] == 0 for r in subset),
            "nonzero_match_record_count":
                sum(r["match_count"] != 0 for r in subset),
            "total_source_occurrence_match_count":
                sum(r["match_count"] for r in subset),
        })

    boundaries = {
        key: False
        for key in output[
            "manifest_scientific_interpretation_boundary_schema"
        ]["required_fields"]
    }

    manifest = {
        **output["manifest_fixed_identity_values"],
        "candidate_form_record_order": output["candidate_form_record_order"],
        "candidate_form_records": records,
        "frozen_input_identity": frozen,
        "scientific_interpretation_boundary": boundaries,
    }

    manifest_bytes = pretty_bytes(manifest)
    manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
    canonical_sha = canonical_digest(manifest)

    state = {
        **output["execution_state_schema"]["fixed_values"],
        "authorization_id": ZE2_AUTH,
        "input_identity_verification": {
            key: "PASS"
            for key in output["execution_state_schema"][
                "input_identity_verification"
            ]["required_fields"]
        },
        "candidate_form_record_count": 1197,
        "candidate_record_count": 171,
        "nonzero_match_record_count": nonzero,
        "zero_match_record_count": zero,
        "total_source_occurrence_match_count": total,
        "per_representation_match_summary": summary,
        "scientific_interpretation_boundary": boundaries,
        "output_hashes": {
            "overlap_manifest_file_sha256": manifest_sha,
            "overlap_manifest_canonical_json_sha256": canonical_sha,
            "execution_state_full_file_sha256_recorded_externally":
                "NEXT_RESULT_CHECKPOINT",
        },
    }

    validate_ze2_result_objects(d36, manifest, state)

    # Output creation occurs only after the authorized consumed sequence.
    ZE2_ROOT.mkdir(parents=True, exist_ok=False)
    (ZE2_ROOT / "candidate_source_representation_overlap.json").write_bytes(
        manifest_bytes
    )
    (ZE2_ROOT / "_execution_state.json").write_bytes(pretty_bytes(state))

    print("ZE2_EXECUTION_STATUS=COMPLETED", flush=True)
    print("ZE2_CANDIDATE_FORM_RECORD_COUNT=1197", flush=True)
    print("ZE2_TOTAL_SOURCE_OCCURRENCE_MATCH_COUNT=" + str(total), flush=True)
    print("NEXT=SEPARATE_ZE2_RESULT_CHECKPOINT", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description="Governed ZE2 implementation. One-shot modes are blocked "
                    "until separately published prerequisites are effective."
    )
    parser.add_argument(
        "--mode", required=True, choices=("preflight", "readiness", "ze2")
    )
    parser.add_argument("--preflight-receipt-path")
    parser.add_argument("--effective-readiness-result-commit")
    parser.add_argument("--readiness-result-artifact")
    parser.add_argument("--ack-one-shot-consumption", action="store_true")
    args = parser.parse_args()

    if args.mode == "preflight":
        run_preflight(args)
    elif args.mode == "readiness":
        run_readiness(args)
    elif args.mode == "ze2":
        run_ze2(args)


if __name__ == "__main__":
    main()
