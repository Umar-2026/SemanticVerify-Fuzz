#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

CONTRACT = HERE / "07_portable_git_object_proof_contract.v1.json"
OBJECT_MANIFEST = HERE / "08_raw_git_object_manifest.v1.json"
AUTH = HERE / "02_decision_0063_authorization.EXACT_COPY.json"
REVIEW_RECORD = HERE / "04_completed_human_review_record.EXACT_COPY.json"
REVIEW = HERE / "05_completed_human_review.EXACT_COPY.md"
ORIGINAL_MANIFEST = HERE / "06_original_activation_artifact_package_manifest.EXACT_COPY.json"
FOCUSED_REVIEW = HERE / "11_AF04_AF07_AF08_AF09_focused_rereview_packet.REVIEW_DRAFT.v1.md"

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def git_oid(obj_type, raw):
    header = (
        obj_type
        + " "
        + str(len(raw))
        + "\0"
    ).encode("ascii")

    return hashlib.sha1(
        header + raw
    ).hexdigest()

def parse_tree(raw):
    i = 0
    entries = {}

    while i < len(raw):
        sp = raw.find(b" ", i)

        if sp < 0:
            fail("MALFORMED_TREE_MODE")

        mode = raw[i:sp].decode("ascii")

        nul = raw.find(b"\0", sp + 1)

        if nul < 0:
            fail("MALFORMED_TREE_NAME")

        name = raw[
            sp + 1:nul
        ].decode(
            "utf-8",
            errors="surrogateescape"
        )

        oid_bytes = raw[
            nul + 1:nul + 21
        ]

        if len(oid_bytes) != 20:
            fail("MALFORMED_TREE_OID")

        if name in entries:
            fail("DUPLICATE_TREE_ENTRY|" + name)

        entries[name] = {
            "mode":
                mode,

            "oid":
                oid_bytes.hex()
        }

        i = nul + 21

    return entries

def is_tree_mode(mode):
    return mode.lstrip("0") == "40000"

contract = json.loads(
    CONTRACT.read_text(
        encoding="utf-8"
    )
)

manifest = json.loads(
    OBJECT_MANIFEST.read_text(
        encoding="utf-8"
    )
)

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

review_record = json.loads(
    REVIEW_RECORD.read_text(
        encoding="utf-8"
    )
)

if hashlib.sha256(
    AUTH.read_bytes()
).hexdigest() != \
   "c8725561b71ecc72fb0d5da93b968eed70c4d7948a83baa2dd28eff66d045f8e":
    fail("AUTHORIZATION_SHA")

if hashlib.sha256(
    REVIEW_RECORD.read_bytes()
).hexdigest() != \
   "3ac5ac4d3c68a9726fdd2c6148d8121c270f94b19eeb714dd2fb76684ebe934f":
    fail("REVIEW_RECORD_SHA")

if hashlib.sha256(
    REVIEW.read_bytes()
).hexdigest() != \
   "72f5eb515529ee509140d606066c38b743cea76ad34a1272f982ef99b028e2d1":
    fail("COMPLETED_REVIEW_SHA")

if hashlib.sha256(
    ORIGINAL_MANIFEST.read_bytes()
).hexdigest() != \
   "b417548998afb9636d3c24e5abdb9a90588fb82dea74e4342ea637a84bc42fb9":
    fail("ORIGINAL_PACKAGE_MANIFEST_SHA")

if contract["open_AF_items"] != [
    "AF04",
    "AF07",
    "AF08",
    "AF09"
]:
    fail("OPEN_AF_ITEMS")

if contract["closed_PASS_items_not_reopened"] != [
    "AF01",
    "AF02",
    "AF03",
    "AF05",
    "AF06",
    "AF10"
]:
    fail("CLOSED_AF_ITEMS")

if review_record[
    "human_review"
]["overall_decision"] != "REVISION_REQUIRED":
    fail("BOUND_HUMAN_REVIEW_RESULT")

if review_record[
    "human_review"
]["open_items"] != contract["open_AF_items"]:
    fail("BOUND_OPEN_ITEM_SET")

if set(
    auth["authorized_corrective_package_requirements"]
) != {
    f"GE{i:02d}"
    for i in range(1, 11)
}:
    fail("GE01_GE10_SET")

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

if contract["status"] != \
   "EVIDENCE_ONLY_REVIEW_CANDIDATE":
    fail("CONTRACT_STATUS")

for key, value in contract[
    "governance_effects"
].items():
    if value is not False:
        fail("PROHIBITED_EFFECT|" + key)

records = manifest["objects"]

if manifest["object_count"] != len(records):
    fail("OBJECT_COUNT")

objects = {}

for rec in records:
    required = {
        "logical_role",
        "logical_roles",
        "git_object_type",
        "expected_git_oid",
        "raw_content_size",
        "raw_content_sha256",
        "file",
    }

    if set(rec) != required:
        fail(
            "OBJECT_MANIFEST_FIELDS|"
            + rec.get(
                "expected_git_oid",
                "UNKNOWN"
            )
        )

    obj_type = rec["git_object_type"]

    if obj_type not in {
        "commit",
        "tree",
        "blob"
    }:
        fail(
            "OBJECT_TYPE|"
            + obj_type
        )

    oid = rec["expected_git_oid"]

    p = HERE / rec["file"]

    if not p.is_file():
        fail(
            "OBJECT_FILE_MISSING|"
            + rec["file"]
        )

    raw = p.read_bytes()

    if len(raw) != rec["raw_content_size"]:
        fail(
            "OBJECT_SIZE|"
            + oid
        )

    if sha256(raw) != rec["raw_content_sha256"]:
        fail(
            "OBJECT_RAW_SHA256|"
            + oid
        )

    recomputed = git_oid(
        obj_type,
        raw
    )

    if recomputed != oid:
        fail(
            "OBJECT_OID|"
            + oid
            + "|"
            + recomputed
        )

    key = (
        obj_type,
        oid
    )

    if key in objects:
        fail(
            "DUPLICATE_OBJECT_RECORD|"
            + oid
        )

    objects[key] = raw

type_counts = {
    "commit":
        sum(
            t == "commit"
            for t, _ in objects
        ),

    "tree":
        sum(
            t == "tree"
            for t, _ in objects
        ),

    "blob":
        sum(
            t == "blob"
            for t, _ in objects
        )
}

if type_counts != manifest[
    "object_type_counts"
]:
    fail("OBJECT_TYPE_COUNTS")

def get_raw(obj_type, oid):
    key = (
        obj_type,
        oid
    )

    if key not in objects:
        fail(
            "REQUIRED_OBJECT_NOT_EXPORTED|"
            + obj_type
            + "|"
            + oid
        )

    return objects[key]

def get_tree(oid):
    return parse_tree(
        get_raw(
            "tree",
            oid
        )
    )

def parse_commit(oid):
    raw = get_raw(
        "commit",
        oid
    )

    header = raw.split(
        b"\n\n",
        1
    )[0]

    tree_values = []
    parent_values = []

    for line in header.splitlines():
        if line.startswith(
            b"tree "
        ):
            tree_values.append(
                line[5:].decode("ascii")
            )

        elif line.startswith(
            b"parent "
        ):
            parent_values.append(
                line[7:].decode("ascii")
            )

    if len(tree_values) != 1:
        fail(
            "COMMIT_TREE_CARDINALITY|"
            + oid
        )

    return {
        "tree":
            tree_values[0],

        "parents":
            parent_values
    }

cp = contract["checkpoint"]
pp = contract["parent"]

checkpoint_oid = cp["commit_oid"]
parent_oid = pp["commit_oid"]

checkpoint_commit = parse_commit(
    checkpoint_oid
)

parent_commit = parse_commit(
    parent_oid
)

if checkpoint_commit["tree"] != cp[
    "root_tree_oid"
]:
    fail("CHECKPOINT_COMMIT_ROOT_TREE")

if checkpoint_commit["parents"] != [
    cp["exact_parent_oid"]
]:
    fail("CHECKPOINT_EXACT_PARENT")

if cp["exact_parent_oid"] != parent_oid:
    fail("CONTRACT_PARENT_BINDING")

if parent_commit["tree"] != pp[
    "root_tree_oid"
]:
    fail("PARENT_COMMIT_ROOT_TREE")

def resolve(root_oid, path):
    parts = [
        x
        for x in path.split("/")
        if x
    ]

    current = root_oid

    if not parts:
        return {
            "mode":
                "040000",

            "oid":
                root_oid
        }

    for idx, part in enumerate(parts):
        entries = get_tree(
            current
        )

        item = entries.get(
            part
        )

        if item is None:
            return None

        last = (
            idx
            == len(parts) - 1
        )

        if last:
            return item

        if not is_tree_mode(
            item["mode"]
        ):
            return None

        current = item["oid"]

    return None

shared = contract[
    "shared_subtree_bindings"
]

cp_config = resolve(
    cp["root_tree_oid"],
    "config"
)

pp_config = resolve(
    pp["root_tree_oid"],
    "config"
)

if cp_config is None or pp_config is None:
    fail("CONFIG_TREE_MISSING")

if not is_tree_mode(cp_config["mode"]):
    fail("CHECKPOINT_CONFIG_NOT_TREE")

if not is_tree_mode(pp_config["mode"]):
    fail("PARENT_CONFIG_NOT_TREE")

if cp_config["oid"] != \
   shared["checkpoint_config_tree_oid"]:
    fail("CHECKPOINT_CONFIG_BINDING")

if pp_config["oid"] != \
   shared["parent_config_tree_oid"]:
    fail("PARENT_CONFIG_BINDING")

if cp_config["oid"] != pp_config["oid"]:
    fail("CONFIG_TREE_NONIDENTITY")

cp_docs = resolve(
    cp["root_tree_oid"],
    "documentation"
)

pp_docs = resolve(
    pp["root_tree_oid"],
    "documentation"
)

if cp_docs is None or pp_docs is None:
    fail("DOCUMENTATION_TREE_MISSING")

if cp_docs["oid"] != \
   shared["checkpoint_documentation_tree_oid"]:
    fail("CHECKPOINT_DOC_BINDING")

if pp_docs["oid"] != \
   shared["parent_documentation_tree_oid"]:
    fail("PARENT_DOC_BINDING")

if cp_docs["oid"] != pp_docs["oid"]:
    fail("DOCUMENTATION_TREE_NONIDENTITY")

for label, binding in contract[
    "core_path_bindings"
].items():
    path = binding["path"]

    a = resolve(
        cp["root_tree_oid"],
        path
    )

    b = resolve(
        pp["root_tree_oid"],
        path
    )

    if a is None:
        fail(
            "CORE_PATH_MISSING_CHECKPOINT|"
            + label
        )

    if b is None:
        fail(
            "CORE_PATH_MISSING_PARENT|"
            + label
        )

    if is_tree_mode(a["mode"]):
        fail(
            "CORE_TARGET_NOT_BLOB|"
            + label
        )

    if is_tree_mode(b["mode"]):
        fail(
            "CORE_TARGET_NOT_BLOB_PARENT|"
            + label
        )

    if a["oid"] != binding[
        "checkpoint_blob_oid"
    ]:
        fail(
            "CORE_CHECKPOINT_BLOB_BINDING|"
            + label
        )

    if b["oid"] != binding[
        "parent_blob_oid"
    ]:
        fail(
            "CORE_PARENT_BLOB_BINDING|"
            + label
        )

    if a["oid"] != b["oid"]:
        fail(
            "CORE_BLOB_NONIDENTITY|"
            + label
        )

    raw_blob = get_raw(
        "blob",
        a["oid"]
    )

    file_sha = sha256(
        raw_blob
    )

    if file_sha != binding[
        "expected_file_sha256"
    ]:
        fail(
            "CORE_GOVERNED_SHA256|"
            + label
        )

for item in contract[
    "absence_proofs"
]:
    path = item["path"]

    a = resolve(
        cp["root_tree_oid"],
        path
    )

    b = resolve(
        pp["root_tree_oid"],
        path
    )

    if a is not None:
        fail(
            "ABSENCE_CHECKPOINT|"
            + path
        )

    if b is not None:
        fail(
            "ABSENCE_PARENT|"
            + path
        )

def list_leaves(
    tree_oid,
    prefix=""
):
    out = []

    entries = get_tree(
        tree_oid
    )

    for name in sorted(entries):
        item = entries[name]

        path = (
            prefix + "/" + name
            if prefix
            else name
        )

        if is_tree_mode(
            item["mode"]
        ):
            out.extend(
                list_leaves(
                    item["oid"],
                    path
                )
            )
        else:
            out.append(path)

    return out

def compare_trees(
    a_oid,
    b_oid,
    prefix=""
):
    if a_oid == b_oid:
        return []

    a = get_tree(
        a_oid
    )

    b = get_tree(
        b_oid
    )

    changes = []

    for name in sorted(
        set(a) | set(b)
    ):
        ia = a.get(name)
        ib = b.get(name)

        path = (
            prefix + "/" + name
            if prefix
            else name
        )

        if ia == ib:
            continue

        if ia is None:
            if is_tree_mode(
                ib["mode"]
            ):
                changes.extend(
                    list_leaves(
                        ib["oid"],
                        path
                    )
                )
            else:
                changes.append(path)

            continue

        if ib is None:
            if is_tree_mode(
                ia["mode"]
            ):
                changes.extend(
                    list_leaves(
                        ia["oid"],
                        path
                    )
                )
            else:
                changes.append(path)

            continue

        if (
            is_tree_mode(ia["mode"])
            and
            is_tree_mode(ib["mode"])
        ):
            changes.extend(
                compare_trees(
                    ia["oid"],
                    ib["oid"],
                    path
                )
            )
        else:
            changes.append(path)

    return changes

scope = contract[
    "original_package_change_scope"
]

package_path = scope[
    "package_path"
]

cp_package = resolve(
    cp["root_tree_oid"],
    package_path
)

pp_package = resolve(
    pp["root_tree_oid"],
    package_path
)

if cp_package is None:
    fail("CHECKPOINT_PACKAGE_PATH_MISSING")

if not is_tree_mode(
    cp_package["mode"]
):
    fail("CHECKPOINT_PACKAGE_NOT_TREE")

if cp_package["oid"] != scope[
    "checkpoint_package_tree_oid"
]:
    fail("CHECKPOINT_PACKAGE_TREE_BINDING")

if pp_package is not None:
    fail("PACKAGE_PATH_NOT_ABSENT_IN_PARENT")

changes = sorted(
    compare_trees(
        cp["root_tree_oid"],
        pp["root_tree_oid"]
    )
)

expected_changes = sorted(
    scope[
        "expected_changed_leaf_paths"
    ]
)

if changes != expected_changes:
    fail(
        "PORTABLE_CHANGED_PATH_SET|"
        + repr(
            sorted(
                set(changes)
                ^ set(expected_changes)
            )
        )
    )

if len(changes) != 22:
    fail(
        "PORTABLE_CHANGED_PATH_COUNT|"
        + str(len(changes))
    )

prefix = package_path + "/"

if any(
    not path.startswith(prefix)
    for path in changes
):
    fail("PORTABLE_CHANGED_PATH_SCOPE")

focus_text = FOCUSED_REVIEW.read_text(
    encoding="utf-8"
).replace(
    "\r\n",
    "\n"
).replace(
    "\r",
    "\n"
)

for rid in (
    "AF04",
    "AF07",
    "AF08",
    "AF09",
):
    heading = re.search(
        r"^##\s+"
        + rid
        + r"\b.*$",
        focus_text,
        re.M
    )

    if not heading:
        fail(
            "FOCUSED_REVIEW_HEADING|"
            + rid
        )

    tail = focus_text[
        heading.end():
    ]

    nxt = re.search(
        r"^##\s+",
        tail,
        re.M
    )

    section = (
        tail[:nxt.start()]
        if nxt
        else tail
    )

    decisions = re.findall(
        r"^Decision:[ \t]*(.*?)[ \t]*$",
        section,
        re.M
    )

    if decisions != [""]:
        fail(
            "FOCUSED_REVIEW_NOT_BLANK|"
            + rid
        )

overall = re.findall(
    r"^Overall decision:[ \t]*(.*?)[ \t]*$",
    focus_text,
    re.M
)

if overall != [""]:
    fail("FOCUSED_OVERALL_NOT_BLANK")

for label in (
    "Human reviewer role",
    "Human reviewer name",
    "Human reviewer signature / recorded confirmation",
    "Human reviewer date",
):
    values = re.findall(
        "^"
        + re.escape(label)
        + r":[ \t]*(.*?)[ \t]*$",
        focus_text,
        re.M
    )

    if values != [""]:
        fail(
            "FOCUSED_REVIEWER_NOT_BLANK|"
            + label
        )

print("RAW_GIT_OBJECT_ID_RECOMPUTATION=PASS")
print("CHECKPOINT_COMMIT_OBJECT=PASS")
print("PARENT_COMMIT_OBJECT=PASS")
print("CHECKPOINT_PARENT_RELATIONSHIP=PASS")
print("CHECKPOINT_ROOT_TREE_BINDING=PASS")
print("PARENT_ROOT_TREE_BINDING=PASS")
print("RAW_BINARY_TREE_PARSING=PASS")
print("CONFIG_TREE_IDENTITY=PASS")
print("DOCUMENTATION_TREE_IDENTITY=PASS")
print("CORE_PATH_COMMIT_TREE_BLOB_BINDINGS=PASS")
print("CORE_ARTIFACT_GOVERNED_SHA256_VALUES=PASS")
print("ACTIVE_V2_HASH_PATH_ABSENCE_FROM_RAW_TREES=PASS")
print("ACTIVE_VERSION_DISPATCH_PATH_ABSENCE_FROM_RAW_TREES=PASS")
print("CURL_JSON_PATH_ABSENCE_FROM_RAW_TREES=PASS")
print("ORIGINAL_PACKAGE_ABSENT_IN_PARENT=PASS")
print("ORIGINAL_PACKAGE_TREE_BINDING=PASS")
print("PORTABLE_CHANGED_LEAF_PATH_COUNT=22")
print("PORTABLE_CHANGED_PATH_SCOPE=ORIGINAL_PACKAGE_ONLY")
print("AF04_AF07_AF08_AF09_REREVIEW_INITIAL_STATE=BLANK")
print("SYNTHETIC_HUMAN_REREVIEW_DECISION=NO")
print("REPOSITORY_ACCESS_REQUIRED=NO")
print("GIT_EXECUTABLE_REQUIRED=NO")
print("PORTABLE_RAW_GIT_OBJECT_CORRECTIVE_PROOF=PASS")
