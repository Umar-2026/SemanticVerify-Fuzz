#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import traceback

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

EXPECTED_PARENT = (
    "7ce6da63d791a6e7aa3a5b85695b816ed852857e"
)

EXPECTED_PARENT_TREE = (
    "2a6fde07204636d2ba62bbba2baa9a4cabffa07c"
)

EXPECTED_GRANDPARENT = (
    "0e80b39bdec4c4ac98f198f67e64569a474a12c0"
)

EXPECTED_SUBJECT = (
    "decision: authorize remaining ASER04 ASER07 corrective successor"
)

EXPECTED_REVIEW_SHA = (
    "daf3ac553885e3a8547cb48c9271015434d1b0c8f33cc51a3afd083f4e73627e"
)

EXPECTED_D0225_MANIFEST_SHA = (
    "311d1ff6b6002760db6c0c0b8d2ebd78dfc6416e92194b6ef6ee8fbc6966969c"
)

OLD_R03_SENTINEL = Path(
    "/openbayes/home/"
    ".svf_d0221_r03_tree_binding_safe_corrective_revision_authorization_consumption.v1.json"
)

EXPECTED_OLD_R03_SENTINEL_SHA = (
    "cfdbc66438b313b0c3e5924f51544a1b5ada65e70bcdf74a8a6791d0a9e1ed3d"
)

D0220_SENTINEL = Path(
    "/openbayes/home/"
    ".svf_d0220_a02_corrective_successor_revision_consumption.v1.json"
)

SENTINEL = Path(
    "/openbayes/home/"
    ".svf_d0226_r03_remaining_aser04_aser07_corrective_successor_authorization_consumption.v1.json"
)

AUTH_REL = (
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
    "schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_"
    "specification_study_v2_remaining_aser04_aser07_corrective_successor_"
    "authorization_v1"
)

D0225_REL = (
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
    "schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_"
    "specification_study_v2_corrective_successor_for_aser04_aser07_source_backed_"
    "revision_v4_returned_independent_human_rereview_record_v1"
)

AUTH_RECORD = REPO / AUTH_REL / "01_remaining_corrective_authorization.v1.json"

D0225_REVIEW = (
    REPO /
    D0225_REL /
    "01_returned_independent_human_rereview.EXACT_COPY.v1.md"
)

D0225_MANIFEST = (
    REPO /
    D0225_REL /
    "07_returned_revision_required_rereview_record.v1.SHA256SUMS"
)

def git(*args):
    return subprocess.check_output(
        ["git", *args],
        cwd=REPO,
        text=True,
    ).strip()

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

def write_sentinel(obj):
    tmp = SENTINEL.with_name(
        SENTINEL.name + ".tmp"
    )

    tmp.write_text(
        json.dumps(
            obj,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    os.replace(tmp, SENTINEL)

if SENTINEL.exists():
    print(
        "ERROR=D0226_R03_ALREADY_CONSUMED",
        file=sys.stderr,
    )
    sys.exit(2)

initial = {
    "artifact_id":
        "SVF-D0226-R03-REMAINING-ASER04-ASER07-AUTHORIZATION-CONSUMPTION-V1",

    "execution_attempt_count":
        1,

    "execution_result":
        "IN_PROGRESS",

    "first_attempt_consumes_authorization":
        True,

    "rerun_authorized":
        False,

    "state":
        "PERMANENTLY_RETIRED",

    "authorization_scope": [
        "ASER04",
        "ASER07",
    ],
}

flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
fd = os.open(SENTINEL, flags, 0o600)

with os.fdopen(fd, "w", encoding="utf-8") as f:
    f.write(
        json.dumps(
            initial,
            indent=2,
            sort_keys=True,
        ) + "\n"
    )

try:
    assert REPO.is_dir()

    head = git("rev-parse", "HEAD")
    parent = git("rev-parse", "HEAD^")
    parent_tree = git("rev-parse", "HEAD^^{tree}")
    grandparent = git("rev-parse", "HEAD^^")
    branch = git("branch", "--show-current")
    subject = git("show", "-s", "--format=%s", "HEAD")

    assert parent == EXPECTED_PARENT
    assert parent_tree == EXPECTED_PARENT_TREE
    assert grandparent == EXPECTED_GRANDPARENT
    assert branch == "main"
    assert subject == EXPECTED_SUBJECT

    assert git("status", "--porcelain") == ""

    required_paths = [
        "01_remaining_corrective_authorization.v1.json",
        "02_remaining_corrective_scope_contract.v1.json",
        "03_authorize_bounded_remaining_corrective_successor_once.v1.py",
        "04_next_rereview_packaging_requirements.v1.json",
        "05_remaining_corrective_authorization_boundary.v1.md",
        "06_verify_d0226_authorization_package.v1.py",
        "07_d0226_authorization_package.v1.SHA256SUMS",
    ]

    for name in required_paths:
        subprocess.check_call(
            [
                "git",
                "cat-file",
                "-e",
                f"HEAD:{AUTH_REL}/{name}",
            ],
            cwd=REPO,
        )

    assert OLD_R03_SENTINEL.is_file()
    assert (
        sha(OLD_R03_SENTINEL)
        == EXPECTED_OLD_R03_SENTINEL_SHA
    )

    old = json.loads(
        OLD_R03_SENTINEL.read_text(
            encoding="utf-8"
        )
    )

    assert old["execution_attempt_count"] == 1
    assert old["execution_result"] == "PASS"
    assert old["state"] == "PERMANENTLY_RETIRED"
    assert old["rerun_authorized"] is False

    assert not D0220_SENTINEL.exists()

    assert sha(D0225_REVIEW) == EXPECTED_REVIEW_SHA
    assert sha(D0225_MANIFEST) == EXPECTED_D0225_MANIFEST_SHA

    record = json.loads(
        AUTH_RECORD.read_text(
            encoding="utf-8"
        )
    )

    assert record["decision"] == "0226"

    assert (
        record["authorization_state"]
        == "AUTHORED_UNCONSUMED"
    )

    assert record["corrective_scope"] == [
        "ASER04",
        "ASER07",
    ]

    assert (
        record["predecessor_review"]["overall"]
        == "REVISION_REQUIRED"
    )

    assert (
        record["predecessor_review"]["ASER04"]
        == "REVISION_REQUIRED"
    )

    assert (
        record["predecessor_review"]["ASER07"]
        == "REVISION_REQUIRED"
    )

    actual_self_sha = sha(Path(__file__))

    assert (
        record["one_time_authorizer"]["sha256"]
        == actual_self_sha
    )

    assert (
        record["one_time_authorizer"]["execution_attempt_count"]
        == 0
    )

    assert (
        record["one_time_authorizer"]["executed"]
        is False
    )

    assert (
        record["one_time_authorizer"]["first_execution_authorized"]
        is True
    )

    assert (
        record["one_time_authorizer"]["rerun_authorized_after_first_attempt"]
        is False
    )

    for value in record["explicit_nonauthorization"].values():
        assert type(value) is bool
        assert value is False

    final = {
        **initial,

        "execution_result":
            "PASS",

        "authorization_successor_commit":
            head,

        "authorization_successor_parent":
            parent,

        "authorization_successor_parent_tree":
            parent_tree,

        "authorization_successor_grandparent":
            grandparent,

        "bounded_corrective_successor_authoring_authorized":
            True,

        "authorized_remaining_corrections": {
            "ASER04": [
                "canonical_json_string_and_member_name_escaping",
                "canonical_byte_test_vectors",
                "canonical_sha256_test_vectors",
            ],

            "ASER07": [
                "strict_freeze_before_witness_ordering",
                "distinct_freeze_and_witness_commits",
                "successful_freeze_commit_ancestry",
                "checked_commit_binding_to_freeze_record_and_witness_lineage",
                "explicit_tree_state_exclusion_condition_if_required",
            ],
        },

        "next_rereview_existing_source_copy_packaging_authorized":
            True,

        "actual_corrective_successor_authored_by_this_verifier":
            False,

        "actual_accounting_evidence_acquisition_authorized":
            False,

        "actual_domain_acquisition_authorized":
            False,

        "forward_witness_acquisition_authorized":
            False,

        "reverse_witness_acquisition_authorized":
            False,

        "concrete_mapping_authorized":
            False,

        "accounting_satisfaction_determination_authorized":
            False,

        "pair_reclassification_authorized":
            False,

        "active_schema_v2_modification_authorized":
            False,

        "analyzer_authorized":
            False,

        "baseline_authorized":
            False,

        "repair_authorized":
            False,
    }

    write_sentinel(final)

    print(
        "D0226_REMAINING_CORRECTIVE_SUCCESSOR_AUTHORIZATION_VERIFIER=PASS"
    )
    print(f"AUTHORIZATION_SUCCESSOR_COMMIT={head}")
    print(f"AUTHORIZATION_SUCCESSOR_PARENT={parent}")
    print(
        "CORRECTIVE_SCOPE=ASER04,ASER07"
    )
    print(
        "ASER04_CORRECTION_SCOPE="
        "CANONICAL_JSON_STRING_ESCAPING_AND_TEST_VECTORS"
    )
    print(
        "ASER07_CORRECTION_SCOPE="
        "STRICT_FREEZE_BEFORE_WITNESS_ORDERING"
    )
    print(
        "NEXT_REREVIEW_EXISTING_SOURCE_COPY_PACKAGING_AUTHORIZED=YES"
    )
    print(
        "BOUNDED_CORRECTIVE_SUCCESSOR_AUTHORING_AUTHORIZED=YES"
    )
    print(
        "ACTUAL_CORRECTIVE_SUCCESSOR_AUTHORED_BY_THIS_VERIFIER=NO"
    )
    print(
        "ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO"
    )
    print(
        "ACTUAL_DOMAIN_ACQUISITION_AUTHORIZED=NO"
    )
    print(
        "CONCRETE_MAPPING_AUTHORIZED=NO"
    )
    print(
        "ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO"
    )
    print(
        "PAIR_RECLASSIFICATION_AUTHORIZED=NO"
    )
    print(
        "ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO"
    )
    print("ANALYZER_AUTHORIZED=NO")
    print("BASELINE_AUTHORIZED=NO")
    print("REPAIR_AUTHORIZED=NO")
    print(
        "D0226_R03_EXECUTION_ATTEMPT_COUNT_FOR_THIS_RUN=1"
    )
    print(
        "D0226_R03_STATE=PERMANENTLY_RETIRED"
    )
    print(
        "D0226_R03_RERUN_AUTHORIZED=NO"
    )

except Exception as exc:
    failed = {
        **initial,
        "execution_result":
            "FAIL",
        "failure_type":
            type(exc).__name__,
        "failure_message":
            str(exc),
        "bounded_corrective_successor_authoring_authorized":
            False,
    }

    write_sentinel(failed)

    print(
        "D0226_REMAINING_CORRECTIVE_SUCCESSOR_AUTHORIZATION_VERIFIER=FAIL",
        file=sys.stderr,
    )

    traceback.print_exc()

    sys.exit(1)
