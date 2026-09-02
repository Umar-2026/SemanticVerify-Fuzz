#!/usr/bin/env python3
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

EXPECTED_PARENT = 'f480347f329d89765db6a7d13d30ae6ebf929bb2'
EXPECTED_PARENT_TREE = '64ac36956e46d8307441ccef58b41f5ff4419303'
EXPECTED_RECORD_REL = 'evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser01_aser02_aser04_aser07_returned_independent_human_rereview_record_v1'
EXPECTED_RECORD_TREE = '3e20186e0a4b674c326b0dbab3e380a16a256020'
EXPECTED_RETURNED_SHA = '8613f25eb8c971d6d38774ea7cd0ac97e8171f1e116854a843e3d346432b7618'
EXPECTED_RETURNED_SIZE = 12091

AUTH_REL = Path('evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_aser04_aser07_revision_authorization_v1')
AUTH_JSON_NAME = "01_bounded_corrective_successor_revision_authorization.v1.json"
SCRIPT_NAME = '02_authorize_bounded_corrective_successor_revision_once.v1.py'
SENTINEL = Path('/openbayes/home/.svf_d0220_a02_corrective_successor_revision_consumption.v1.json')

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git(path, *args):
    return subprocess.check_output(
        ["git", "-C", str(path), *args],
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
    if SENTINEL.exists():
        print("D0220_A02_ALREADY_CONSUMED=YES", file=sys.stderr)
        print("D0220_A02_RERUN_AUTHORIZED=NO", file=sys.stderr)
        return 97

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    state = {
        "sentinel_id": "SVF-D0220-A02-FIRST-AND-ONLY-CONSUMPTION-SENTINEL-V1",
        "consumed_at_utc": now,
        "execution_attempt_count": 1,
        "execution_result": "PENDING",
        "first_attempt_consumes_authorization": True,
        "rerun_authorized": False,
        "state": "PERMANENTLY_RETIRED"
    }

    fd = os.open(str(SENTINEL), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(state, indent=2, sort_keys=True) + "\n")

    result = dict(state)

    try:
        here = Path(__file__).absolute()
        repo = Path(git(here.parent, "rev-parse", "--show-toplevel"))

        head = git(repo, "rev-parse", "HEAD")
        parent = git(repo, "rev-parse", "HEAD^")
        parent_tree = git(repo, "rev-parse", "HEAD^{tree}")
        branch = git(repo, "branch", "--show-current")
        status = git(repo, "status", "--porcelain")

        if parent != EXPECTED_PARENT:
            raise RuntimeError("AUTHORIZATION_PARENT_MISMATCH")
        if parent_tree != EXPECTED_PARENT_TREE:
            raise RuntimeError("AUTHORIZATION_PARENT_TREE_MISMATCH")
        if branch != "main":
            raise RuntimeError("BRANCH_NOT_MAIN")
        if status:
            raise RuntimeError("REPOSITORY_NOT_CLEAN")

        record_tree = git(repo, "rev-parse", "HEAD^:" + EXPECTED_RECORD_REL)

        if record_tree != EXPECTED_RECORD_TREE:
            raise RuntimeError("D0219_RECORD_TREE_MISMATCH")

        review = repo / EXPECTED_RECORD_REL / "01_returned_independent_human_rereview.EXACT_COPY.v1.md"

        if not review.is_file():
            raise RuntimeError("RECORDED_RETURNED_REREVIEW_MISSING")
        if sha256(review) != EXPECTED_RETURNED_SHA:
            raise RuntimeError("RECORDED_RETURNED_REREVIEW_SHA_MISMATCH")
        if review.stat().st_size != EXPECTED_RETURNED_SIZE:
            raise RuntimeError("RECORDED_RETURNED_REREVIEW_SIZE_MISMATCH")

        auth_path = repo / AUTH_REL / AUTH_JSON_NAME
        auth = json.loads(auth_path.read_text(encoding="utf-8"))

        script_path = repo / AUTH_REL / SCRIPT_NAME
        script_sha = sha256(script_path)

        if auth["one_time_verifier"]["sha256"] != script_sha:
            raise RuntimeError("A02_SHA_BINDING_MISMATCH")

        if auth["decision"] != "0220":
            raise RuntimeError("DECISION_BINDING_MISMATCH")

        if auth["corrective_scope"]["revision_required_items"] != ["ASER04", "ASER07"]:
            raise RuntimeError("CORRECTIVE_SCOPE_MISMATCH")

        if auth["corrective_scope"]["fresh_pass_items_preserved"] != ["ASER01", "ASER02"]:
            raise RuntimeError("FRESH_PASS_PRESERVATION_MISMATCH")

        if auth["corrective_scope"]["predecessor_pass_items_preserved"] != [
            "ASER03", "ASER05", "ASER06", "ASER08", "ASER09"
        ]:
            raise RuntimeError("PREDECESSOR_PASS_PRESERVATION_MISMATCH")

        for key, value in auth["explicit_nonauthorization"].items():
            if value is not False:
                raise RuntimeError("NONAUTHORIZATION_VIOLATION=" + key)

        result.update({
            "authorization_commit": head,
            "authorization_parent": parent,
            "execution_exit_code": 0,
            "execution_result": "PASS",
            "one_time_verifier_sha256": script_sha,
            "returned_rereview_sha256": EXPECTED_RETURNED_SHA
        })

        write_json_atomic(SENTINEL, result)

        print("D0220_BOUNDED_ASER04_ASER07_CORRECTIVE_REVISION_AUTHORIZATION_VERIFIER=PASS")
        print("AUTHORIZATION_COMMIT=" + head)
        print("AUTHORIZATION_PARENT=" + parent)
        print("D0219_RETURNED_REREVIEW_RECORD_TREE=" + record_tree)
        print("RETURNED_REREVIEW_SHA256=" + EXPECTED_RETURNED_SHA)
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
        print("D0220_A02_EXECUTION_ATTEMPT_COUNT_FOR_THIS_RUN=1")
        print("D0220_A02_RERUN_AUTHORIZED=NO")
        return 0

    except Exception as exc:
        result.update({
            "execution_exit_code": 1,
            "execution_result": "FAIL",
            "failure_type": type(exc).__name__,
            "failure_message": str(exc)
        })
        write_json_atomic(SENTINEL, result)

        print("D0220_BOUNDED_ASER04_ASER07_CORRECTIVE_REVISION_AUTHORIZATION_VERIFIER=FAIL", file=sys.stderr)
        print("D0220_A02_RERUN_AUTHORIZED=NO", file=sys.stderr)
        print(type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
