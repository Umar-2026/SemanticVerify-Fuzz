#!/usr/bin/env python3
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

EXPECTED_D0220_COMMIT = "57d84382ccdbe8784f06f33e9d99505192426c3a"
EXPECTED_D0220_TREE = "dc9affb71e0b23c89f591e93997b842ffc90a528"
EXPECTED_D0219_COMMIT = "f480347f329d89765db6a7d13d30ae6ebf929bb2"
EXPECTED_D0219_TREE = "64ac36956e46d8307441ccef58b41f5ff4419303"

EXPECTED_RECORD_REL = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser01_aser02_aser04_aser07_returned_independent_human_rereview_record_v1"
EXPECTED_RECORD_TREE = "3e20186e0a4b674c326b0dbab3e380a16a256020"
EXPECTED_RETURNED_SHA = "8613f25eb8c971d6d38774ea7cd0ac97e8171f1e116854a843e3d346432b7618"
EXPECTED_RETURNED_SIZE = 12091

OLD_AUTH_JSON_REL = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_aser04_aser07_revision_authorization_v1/01_bounded_corrective_successor_revision_authorization.v1.json"
OLD_A02_REL = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_aser04_aser07_revision_authorization_v1/02_authorize_bounded_corrective_successor_revision_once.v1.py"
OLD_A02_SHA = "d38ed4efd7db411d9feb303f60b1f467dc4d057c99df5d47b9488295f940abca"
OLD_SENTINEL = Path("/openbayes/home/.svf_d0220_a02_corrective_successor_revision_consumption.v1.json")

NEW_AUTH_REL = Path("evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_aser04_aser07_revision_authorization_v1_tree_binding_safe_successor_v1")
NEW_AUTH_JSON_NAME = "02_tree_binding_safe_corrective_revision_authorization_successor.v1.json"
SCRIPT_NAME = "03_authorize_bounded_corrective_successor_revision_once.v2.py"
NEW_SENTINEL = Path("/openbayes/home/.svf_d0221_r03_tree_binding_safe_corrective_revision_authorization_consumption.v1.json")

EXPECTED_D0221_SCOPE = sorted([
    "documentation/decisions/0221-supersede-unexecuted-defective-d0220-a02-and-author-tree-binding-safe-corrective-revision-authorization-successor.md",
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_aser04_aser07_revision_authorization_v1_tree_binding_safe_successor_v1/01_d0220_a02_static_defect_and_unexecuted_supersession_record.v1.json",
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_aser04_aser07_revision_authorization_v1_tree_binding_safe_successor_v1/02_tree_binding_safe_corrective_revision_authorization_successor.v1.json",
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_aser04_aser07_revision_authorization_v1_tree_binding_safe_successor_v1/03_authorize_bounded_corrective_successor_revision_once.v2.py",
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_aser04_aser07_revision_authorization_v1_tree_binding_safe_successor_v1/04_tree_binding_safe_corrective_revision_scope_contract.v1.json",
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_aser04_aser07_revision_authorization_v1_tree_binding_safe_successor_v1/05_tree_binding_safe_authorization_successor_boundary.v1.md"
])

OLD_DEFECT_SOURCE_PATTERN = 'parent_tree = git(repo, "rev-parse", "HEAD^{tree}")'

def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", str(repo), *args],
        text=True,
        stderr=subprocess.STDOUT
    ).strip()

def write_json_atomic(path, obj):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )
    os.replace(tmp, path)

def main():
    if NEW_SENTINEL.exists():
        print("D0221_R03_ALREADY_CONSUMED=YES", file=sys.stderr)
        print("D0221_R03_RERUN_AUTHORIZED=NO", file=sys.stderr)
        return 97

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    state = {
        "sentinel_id": "SVF-D0221-R03-FIRST-AND-ONLY-CONSUMPTION-SENTINEL-V1",
        "consumed_at_utc": now,
        "execution_attempt_count": 1,
        "execution_result": "PENDING",
        "first_attempt_consumes_authorization": True,
        "rerun_authorized": False,
        "state": "PERMANENTLY_RETIRED"
    }

    fd = os.open(
        str(NEW_SENTINEL),
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o600
    )

    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(state, indent=2, sort_keys=True) + "\n")

    result = dict(state)

    try:
        here = Path(__file__).absolute()
        repo = Path(git(here.parent, "rev-parse", "--show-toplevel"))

        head = git(repo, "rev-parse", "HEAD")

        d0220_commit = git(repo, "rev-parse", "HEAD^")
        d0220_tree = git(
            repo,
            "rev-parse",
            d0220_commit + "^{tree}"
        )

        d0219_commit = git(
            repo,
            "rev-parse",
            d0220_commit + "^"
        )
        d0219_tree = git(
            repo,
            "rev-parse",
            d0219_commit + "^{tree}"
        )

        branch = git(repo, "branch", "--show-current")
        status = git(repo, "status", "--porcelain")

        if d0220_commit != EXPECTED_D0220_COMMIT:
            raise RuntimeError("D0220_COMMIT_MISMATCH")

        if d0220_tree != EXPECTED_D0220_TREE:
            raise RuntimeError("D0220_TREE_MISMATCH")

        if d0219_commit != EXPECTED_D0219_COMMIT:
            raise RuntimeError("D0219_COMMIT_MISMATCH")

        if d0219_tree != EXPECTED_D0219_TREE:
            raise RuntimeError("D0219_TREE_MISMATCH")

        if branch != "main":
            raise RuntimeError("BRANCH_NOT_MAIN")

        if status:
            raise RuntimeError("REPOSITORY_NOT_CLEAN")

        scope_text = git(
            repo,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            d0220_commit,
            head
        )

        actual_scope = sorted(
            x.strip()
            for x in scope_text.splitlines()
            if x.strip()
        )

        if actual_scope != EXPECTED_D0221_SCOPE:
            raise RuntimeError("D0221_SCOPE_MISMATCH")

        old_a02 = repo / OLD_A02_REL

        if not old_a02.is_file():
            raise RuntimeError("D0220_A02_MISSING")

        if sha256(old_a02) != OLD_A02_SHA:
            raise RuntimeError("D0220_A02_SHA_MISMATCH")

        old_src = old_a02.read_text(encoding="utf-8")

        if OLD_DEFECT_SOURCE_PATTERN not in old_src:
            raise RuntimeError("D0220_STATIC_DEFECT_PATTERN_NOT_PRESENT")

        if OLD_SENTINEL.exists():
            raise RuntimeError("D0220_A02_SENTINEL_UNEXPECTEDLY_EXISTS")

        old_auth = json.loads(
            (repo / OLD_AUTH_JSON_REL).read_text(encoding="utf-8")
        )

        if old_auth["decision"] != "0220":
            raise RuntimeError("D0220_AUTHORIZATION_BINDING_MISMATCH")

        if old_auth["corrective_scope"]["revision_required_items"] != [
            "ASER04", "ASER07"
        ]:
            raise RuntimeError("D0220_CORRECTIVE_SCOPE_MISMATCH")

        record_tree = git(
            repo,
            "rev-parse",
            EXPECTED_D0219_COMMIT + ":" + EXPECTED_RECORD_REL
        )

        if record_tree != EXPECTED_RECORD_TREE:
            raise RuntimeError("D0219_RECORD_TREE_MISMATCH")

        review = (
            repo /
            EXPECTED_RECORD_REL /
            "01_returned_independent_human_rereview.EXACT_COPY.v1.md"
        )

        if not review.is_file():
            raise RuntimeError("RETURNED_REREVIEW_MISSING")

        if sha256(review) != EXPECTED_RETURNED_SHA:
            raise RuntimeError("RETURNED_REREVIEW_SHA_MISMATCH")

        if review.stat().st_size != EXPECTED_RETURNED_SIZE:
            raise RuntimeError("RETURNED_REREVIEW_SIZE_MISMATCH")

        new_auth = json.loads(
            (repo / NEW_AUTH_REL / NEW_AUTH_JSON_NAME).read_text(
                encoding="utf-8"
            )
        )

        script_path = repo / NEW_AUTH_REL / SCRIPT_NAME
        script_sha = sha256(script_path)

        if new_auth["decision"] != "0221":
            raise RuntimeError("D0221_AUTHORIZATION_BINDING_MISMATCH")

        if new_auth["one_time_successor_verifier"]["sha256"] != script_sha:
            raise RuntimeError("D0221_R03_SHA_MISMATCH")

        if new_auth["corrective_scope"]["revision_required_items"] != [
            "ASER04", "ASER07"
        ]:
            raise RuntimeError("CORRECTIVE_SCOPE_MISMATCH")

        if new_auth["corrective_scope"]["fresh_pass_items_preserved"] != [
            "ASER01", "ASER02"
        ]:
            raise RuntimeError("FRESH_PASS_PRESERVATION_MISMATCH")

        if new_auth["corrective_scope"]["predecessor_pass_items_preserved"] != [
            "ASER03", "ASER05", "ASER06", "ASER08", "ASER09"
        ]:
            raise RuntimeError("PREDECESSOR_PASS_PRESERVATION_MISMATCH")

        old_state = new_auth["superseded_d0220_a02"]

        if old_state["execution_attempt_count"] != 0:
            raise RuntimeError("D0220_A02_ATTEMPT_COUNT_MISMATCH")

        if old_state["consumed"] is not False:
            raise RuntimeError("D0220_A02_CONSUMPTION_STATE_MISMATCH")

        if old_state["state"] != "SUPERSEDED_UNEXECUTED":
            raise RuntimeError("D0220_A02_STATE_MISMATCH")

        if old_state["execution_authorized"] is not False:
            raise RuntimeError("D0220_A02_EXECUTION_STILL_AUTHORIZED")

        for key, value in new_auth["explicit_nonauthorization"].items():
            if value is not False:
                raise RuntimeError("NONAUTHORIZATION_VIOLATION=" + key)

        result.update({
            "authorization_successor_commit": head,
            "authorization_successor_parent": d0220_commit,
            "execution_exit_code": 0,
            "execution_result": "PASS",
            "one_time_successor_verifier_sha256": script_sha,
            "returned_rereview_sha256": EXPECTED_RETURNED_SHA,
            "superseded_d0220_a02_sha256": OLD_A02_SHA
        })

        write_json_atomic(NEW_SENTINEL, result)

        print("D0221_TREE_BINDING_SAFE_CORRECTIVE_REVISION_AUTHORIZATION_VERIFIER=PASS")
        print("AUTHORIZATION_SUCCESSOR_COMMIT=" + head)
        print("AUTHORIZATION_SUCCESSOR_PARENT=" + d0220_commit)
        print("D0220_SOURCE_AUTHORIZATION_TREE=" + d0220_tree)
        print("D0219_RETURNED_REREVIEW_RECORD_TREE=" + record_tree)

        print("D0220_A02_EXECUTION_ATTEMPT_COUNT=0")
        print("D0220_A02_STATE=SUPERSEDED_UNEXECUTED")
        print("D0220_A02_EXECUTION_AUTHORIZED=NO")

        print("CORRECTIVE_REVISION_ITEMS=ASER04,ASER07")
        print("FRESH_PASS_ITEMS_PRESERVED=ASER01,ASER02")
        print("PREDECESSOR_PASS_ITEMS_PRESERVED=ASER03,ASER05,ASER06,ASER08,ASER09")

        print("BOUNDED_CORRECTIVE_SUCCESSOR_REVISION_AUTHORING_AUTHORIZED=YES")
        print("BOUNDED_CORRECTIVE_SUCCESSOR_REVISION_AUTHORED_BY_THIS_VERIFIER=NO")

        print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
        print("ACTUAL_DOMAIN_ACQUISITION_AUTHORIZED=NO")
        print("FORWARD_WITNESS_ACQUISITION_AUTHORIZED=NO")
        print("REVERSE_WITNESS_ACQUISITION_AUTHORIZED=NO")
        print("CONCRETE_MAPPING_AUTHORIZED=NO")
        print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
        print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
        print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
        print("ANALYZER_AUTHORIZED=NO")
        print("BASELINE_AUTHORIZED=NO")
        print("REPAIR_AUTHORIZED=NO")

        print("D0221_R03_EXECUTION_ATTEMPT_COUNT_FOR_THIS_RUN=1")
        print("D0221_R03_RERUN_AUTHORIZED=NO")

        return 0

    except Exception as exc:
        result.update({
            "execution_exit_code": 1,
            "execution_result": "FAIL",
            "failure_type": type(exc).__name__,
            "failure_message": str(exc)
        })

        write_json_atomic(NEW_SENTINEL, result)

        print(
            "D0221_TREE_BINDING_SAFE_CORRECTIVE_REVISION_AUTHORIZATION_VERIFIER=FAIL",
            file=sys.stderr
        )
        print("D0221_R03_RERUN_AUTHORIZED=NO", file=sys.stderr)
        print(type(exc).__name__ + ": " + str(exc), file=sys.stderr)

        return 1

if __name__ == "__main__":
    raise SystemExit(main())
