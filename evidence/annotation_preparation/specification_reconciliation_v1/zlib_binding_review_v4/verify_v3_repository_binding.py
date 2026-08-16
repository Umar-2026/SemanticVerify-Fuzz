#!/usr/bin/env python3

from pathlib import Path
import argparse
import hashlib
import json
import sys


def die(msg):
    print("VERIFY|FAIL|" + msg)
    raise SystemExit(1)


def check(name, ok, detail=""):
    print(
        "VERIFY|"
        + name
        + "|"
        + ("PASS" if ok else "FAIL")
        + ("|" + detail if detail else "")
    )
    if not ok:
        raise SystemExit(1)


def git_oid(obj_type, raw, fmt):
    header = (
        obj_type.encode("ascii")
        + b" "
        + str(len(raw)).encode("ascii")
        + b"\0"
    )
    data = header + raw

    if fmt == "sha1":
        return hashlib.sha1(data).hexdigest()

    if fmt == "sha256":
        return hashlib.sha256(data).hexdigest()

    die("unsupported Git object format: " + fmt)


def parse_tree(raw, oid_bytes):
    entries = []
    i = 0

    while i < len(raw):
        sp = raw.find(b" ", i)

        if sp < 0:
            die("malformed tree: missing mode separator")

        mode = raw[i:sp].decode("ascii")

        nul = raw.find(b"\0", sp + 1)

        if nul < 0:
            die("malformed tree: missing name terminator")

        name = raw[
            sp + 1:nul
        ].decode(
            "utf-8",
            errors="surrogateescape",
        )

        oid_raw = raw[
            nul + 1:
            nul + 1 + oid_bytes
        ]

        if len(oid_raw) != oid_bytes:
            die("malformed tree: incomplete oid")

        entries.append(
            {
                "mode": mode,
                "name": name,
                "oid": oid_raw.hex(),
            }
        )

        i = nul + 1 + oid_bytes

    if i != len(raw):
        die("malformed tree: trailing bytes")

    return entries


parser = argparse.ArgumentParser(
    description=(
        "Offline verifier for the SemanticVerify-Fuzz "
        "zlib V3 repository-binding proof."
    )
)

parser.add_argument(
    "--proof",
    default=None,
)

parser.add_argument(
    "--target",
    default=None,
)

args = parser.parse_args()

base = Path(__file__).resolve().parent

proof_path = (
    Path(args.proof)
    if args.proof
    else base / "04_v3_repository_binding_proof.v1.json"
)

target_path = (
    Path(args.target)
    if args.target
    else base / (
        "03_zlib_source_only_successor_"
        "working_fsm_draft.v3.json"
    )
)

check(
    "PROOF_PRESENT",
    proof_path.is_file(),
    str(proof_path),
)

check(
    "TARGET_PRESENT",
    target_path.is_file(),
    str(target_path),
)

proof = json.loads(
    proof_path.read_text(
        encoding="utf-8"
    )
)

binding = proof["repository_binding"]
target = proof["technical_review_target"]

fmt = binding["git_object_format"]

check(
    "OBJECT_FORMAT_SUPPORTED",
    fmt in {"sha1", "sha256"},
    fmt,
)

oid_bytes = 20 if fmt == "sha1" else 32

records = proof["raw_git_objects"]

check(
    "RAW_OBJECT_COUNT_7",
    len(records) == 7,
)

objects = {}

for rec in records:
    path = base / rec["package_path"]

    check(
        "OBJECT_PRESENT|" + rec["git_oid"],
        path.is_file(),
        str(path),
    )

    raw = path.read_bytes()

    check(
        "OBJECT_BYTE_COUNT|"
        + rec["git_oid"],
        len(raw)
        == rec["raw_byte_count"],
    )

    check(
        "OBJECT_RAW_SHA256|"
        + rec["git_oid"],
        hashlib.sha256(
            raw
        ).hexdigest()
        == rec["raw_sha256"],
    )

    check(
        "OBJECT_GIT_OID|"
        + rec["git_oid"],
        git_oid(
            rec["object_type"],
            raw,
            fmt,
        )
        == rec["git_oid"],
    )

    objects[
        rec["git_oid"]
    ] = {
        "type":
            rec["object_type"],

        "raw":
            raw,
    }

commit_oid = binding[
    "v3_author_commit"
]

check(
    "AUTHOR_COMMIT_INCLUDED",
    commit_oid in objects,
)

check(
    "AUTHOR_OBJECT_TYPE_COMMIT",
    objects[
        commit_oid
    ][
        "type"
    ] == "commit",
)

commit_text = objects[
    commit_oid
][
    "raw"
].decode(
    "utf-8",
    errors="replace",
)

tree_lines = [
    x
    for x in commit_text.splitlines()
    if x.startswith("tree ")
]

check(
    "COMMIT_ONE_ROOT_TREE",
    len(tree_lines) == 1,
)

root_oid = tree_lines[0].split(
    " ",
    1,
)[1]

check(
    "COMMIT_ROOT_TREE_EXACT",
    root_oid
    == binding[
        "v3_author_root_tree"
    ],
)

steps = binding[
    "merkle_path"
]

segments = target[
    "repository_path"
].split("/")

check(
    "MERKLE_STEP_COUNT_MATCHES_PATH",
    len(steps) == len(segments),
)

current_oid = root_oid

for depth, (
    step,
    segment,
) in enumerate(
    zip(
        steps,
        segments,
    )
):
    check(
        "STEP_TREE_OID|"
        + str(depth),
        step["tree_oid"]
        == current_oid,
    )

    check(
        "TREE_INCLUDED|"
        + current_oid,
        current_oid in objects,
    )

    check(
        "TREE_OBJECT_TYPE|"
        + current_oid,
        objects[
            current_oid
        ][
            "type"
        ] == "tree",
    )

    entries = parse_tree(
        objects[
            current_oid
        ][
            "raw"
        ],
        oid_bytes,
    )

    matches = [
        e
        for e in entries
        if e["name"] == segment
    ]

    check(
        "PATH_SEGMENT_UNIQUE|"
        + segment,
        len(matches) == 1,
    )

    entry = matches[0]

    check(
        "STEP_TARGET_NAME|"
        + segment,
        step[
            "target_name"
        ] == segment,
    )

    check(
        "STEP_TARGET_MODE|"
        + segment,
        step[
            "target_mode"
        ] == entry[
            "mode"
        ],
    )

    check(
        "STEP_TARGET_OID|"
        + segment,
        step[
            "target_oid"
        ] == entry[
            "oid"
        ],
    )

    current_oid = entry[
        "oid"
    ]

blob_oid = binding[
    "v3_blob_oid"
]

check(
    "MERKLE_CHAIN_ENDS_AT_DECLARED_BLOB",
    current_oid == blob_oid,
)

check(
    "BLOB_INCLUDED",
    blob_oid in objects,
)

check(
    "FINAL_OBJECT_TYPE_BLOB",
    objects[
        blob_oid
    ][
        "type"
    ] == "blob",
)

blob = objects[
    blob_oid
][
    "raw"
]

blob_sha256 = hashlib.sha256(
    blob
).hexdigest()

check(
    "BLOB_SHA256_MATCHES_PROOF",
    blob_sha256
    == binding[
        "v3_blob_content_sha256"
    ],
)

check(
    "BLOB_SHA256_MATCHES_REVIEW_TARGET",
    blob_sha256
    == target[
        "expected_content_sha256"
    ],
)

target_bytes = target_path.read_bytes()

check(
    "PACKAGE_LOCAL_TARGET_BYTE_IDENTICAL_TO_REPOSITORY_BLOB",
    target_bytes == blob,
)

check(
    "PACKAGE_LOCAL_TARGET_SHA256_EXACT",
    hashlib.sha256(
        target_bytes
    ).hexdigest()
    == target[
        "expected_content_sha256"
    ],
)

print(
    "V3_AUTHOR_COMMIT="
    + commit_oid
)

print(
    "V3_REPOSITORY_PATH="
    + target[
        "repository_path"
    ]
)

print(
    "V3_REPOSITORY_BLOB_OID="
    + blob_oid
)

print(
    "V3_CONTENT_SHA256="
    + blob_sha256
)

print(
    "REPOSITORY_COMMIT_TO_PATH_TO_BLOB_BINDING=VERIFIED"
)

print(
    "PACKAGE_LOCAL_V3_EQUALS_REPOSITORY_V3_BLOB=YES"
)

print(
    "BINDING_PROOF_VERIFICATION=PASS"
)
