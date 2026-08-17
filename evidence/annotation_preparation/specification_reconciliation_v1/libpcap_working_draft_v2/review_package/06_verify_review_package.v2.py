from pathlib import Path
import hashlib
import json
import subprocess
import sys

EXPECTED_AUTHOR_COMMIT = "342ea862912e53b1ebec70f2e53e57db10d7846c"
EXPECTED_AUTHOR_TREE = "1e8253e52be0a0d41fbe436c738d0011a02e33fa"
EXPECTED_DRAFT_SHA = "3ee8459dd2cff6dc8f5dd538a0f8d54a9ceda740d5ea7d977a0a9d34093c3221"
EXPECTED_DRAFT_BLOB = "2f5782b744edc3e7684b459241cf079a77da1ab7"

HERE = Path(__file__).resolve()

# review_package -> libpcap_working_draft_v2 ->
# specification_reconciliation_v1 -> annotation_preparation ->
# evidence -> repository root
ROOT = HERE.parents[5]

DRAFT = ROOT / "evidence/annotation_preparation/specification_reconciliation_v1/libpcap_working_draft_v2/libpcap_source_only_working_fsm_draft.v2.json"
COPY = ROOT / "evidence/annotation_preparation/specification_reconciliation_v1/libpcap_working_draft_v2/review_package/03_libpcap_source_only_working_fsm_draft.v2.json"
BINDING = ROOT / "evidence/annotation_preparation/specification_reconciliation_v1/libpcap_working_draft_v2/review_package/01_repository_binding.v2.json"


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def git(*args):
    cp = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if cp.returncode != 0:
        raise RuntimeError(
            cp.stderr or cp.stdout
        )

    return cp.stdout.strip()


def check(label, ok):
    print(
        "VERIFY|"
        + ("PASS" if ok else "FAIL")
        + "|"
        + label
    )

    if not ok:
        sys.exit(1)


check(
    "repository root",
    git("rev-parse", "--show-toplevel")
    == str(ROOT)
)

check(
    "author commit exists",
    git(
        "rev-parse",
        EXPECTED_AUTHOR_COMMIT
    )
    == EXPECTED_AUTHOR_COMMIT
)

check(
    "author tree exact",
    git(
        "rev-parse",
        EXPECTED_AUTHOR_COMMIT + "^{tree}"
    )
    == EXPECTED_AUTHOR_TREE
)

check(
    "repository target sha256",
    sha(DRAFT)
    == EXPECTED_DRAFT_SHA
)

check(
    "package copy byte identity",
    DRAFT.read_bytes()
    == COPY.read_bytes()
)

check(
    "author commit target blob",
    git(
        "rev-parse",
        EXPECTED_AUTHOR_COMMIT
        + ":"
        + "evidence/annotation_preparation/specification_reconciliation_v1/libpcap_working_draft_v2/libpcap_source_only_working_fsm_draft.v2.json"
    )
    == EXPECTED_DRAFT_BLOB
)

binding = json.loads(
    BINDING.read_text(
        encoding="utf-8"
    )
)

check(
    "binding author commit",
    binding[
        "repository_target"
    ][
        "author_checkpoint_commit"
    ]
    == EXPECTED_AUTHOR_COMMIT
)

check(
    "binding author tree",
    binding[
        "repository_target"
    ][
        "author_checkpoint_tree"
    ]
    == EXPECTED_AUTHOR_TREE
)

check(
    "binding draft sha256",
    binding[
        "repository_target"
    ][
        "draft_sha256"
    ]
    == EXPECTED_DRAFT_SHA
)

check(
    "binding draft blob",
    binding[
        "repository_target"
    ][
        "draft_git_blob"
    ]
    == EXPECTED_DRAFT_BLOB
)

check(
    "human review incomplete",
    binding[
        "human_review_completed"
    ]
    is False
)

check(
    "canonical not frozen",
    binding[
        "canonical_specification_frozen"
    ]
    is False
)

print(
    "LIBPCAP_V2_REVIEW_PACKAGE_BINDING=PASS"
)
