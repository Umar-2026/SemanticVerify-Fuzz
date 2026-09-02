#!/usr/bin/env python3
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

EXPECTED_PARENT = '366b0846e637c71bf6ce947ba74ab4ac86307d97'
EXPECTED_PARENT_TREE = '00028ed75eaafdc9e3ab69313a3ef83ef185ef03'
EXPECTED_HANDOFF_REL = 'evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser01_aser02_aser04_aser07_independent_human_rereview_package_v1_external_handoff_record_v1'
EXPECTED_HANDOFF_TREE = 'dae388040a574570aa7156667264abf2271e222c'

RETURNED = Path('/openbayes/home/50_req06_req14_accounting_gap_corrective_successor_Ndeem_independent_human_rereview_form.MANUAL_REVIEW_COPY.v1.md')
EXPECTED_RETURNED_SHA256 = '8613f25eb8c971d6d38774ea7cd0ac97e8171f1e116854a843e3d346432b7618'
EXPECTED_RETURNED_SIZE = 12091

AUTH_REL = Path('evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser01_aser02_aser04_aser07_returned_independent_human_rereview_recording_authorization_v1')
AUTH_JSON_NAME = "01_exact_returned_revision_required_rereview_recording_authorization.v1.json"
SCRIPT_NAME = '02_authorize_exact_returned_revision_required_rereview_recording_once.v1.py'

SENTINEL = Path('/openbayes/home/.svf_d0218_a02_returned_rereview_recording_consumption.v1.json')

def sha256_path(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git(path, *args):
    return subprocess.check_output(
        ["git", "-C", str(path), *args],
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()

def write_json_atomic(path, obj):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)

def main():
    if SENTINEL.exists():
        print("D0218_A02_ALREADY_CONSUMED=YES", file=sys.stderr)
        print("D0218_A02_RERUN_AUTHORIZED=NO", file=sys.stderr)
        return 97

    started = datetime.datetime.now(datetime.timezone.utc).isoformat()

    initial = {
        "sentinel_id": "SVF-D0218-A02-FIRST-AND-ONLY-CONSUMPTION-SENTINEL-V1",
        "consumed_at_utc": started,
        "execution_attempt_count": 1,
        "execution_result": "PENDING",
        "first_attempt_consumes_authorization": True,
        "rerun_authorized": False,
        "state": "PERMANENTLY_RETIRED"
    }

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(str(SENTINEL), flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(initial, indent=2, sort_keys=True) + "\n")

    result = dict(initial)

    try:
        here = Path(__file__).absolute()
        repo = Path(git(here.parent, "rev-parse", "--show-toplevel"))

        head = git(repo, "rev-parse", "HEAD")
        parent = git(repo, "rev-parse", "HEAD^")
        parent_tree = git(repo, "rev-parse", "HEAD^^{tree}")
        branch = git(repo, "branch", "--show-current")
        status = git(repo, "status", "--porcelain")
        handoff_tree = git(repo, "rev-parse", "HEAD^:" + EXPECTED_HANDOFF_REL)

        if parent != EXPECTED_PARENT:
            raise RuntimeError("AUTHORIZATION_PARENT_MISMATCH")
        if parent_tree != EXPECTED_PARENT_TREE:
            raise RuntimeError("AUTHORIZATION_PARENT_TREE_MISMATCH")
        if branch != "main":
            raise RuntimeError("BRANCH_NOT_MAIN")
        if status:
            raise RuntimeError("REPOSITORY_NOT_CLEAN")
        if handoff_tree != EXPECTED_HANDOFF_TREE:
            raise RuntimeError("D0217_HANDOFF_TREE_MISMATCH")

        if not RETURNED.is_file():
            raise RuntimeError("RETURNED_REVIEW_MISSING")
        if sha256_path(RETURNED) != EXPECTED_RETURNED_SHA256:
            raise RuntimeError("RETURNED_REVIEW_SHA256_MISMATCH")
        if RETURNED.stat().st_size != EXPECTED_RETURNED_SIZE:
            raise RuntimeError("RETURNED_REVIEW_SIZE_MISMATCH")

        auth_json_path = repo / AUTH_REL / AUTH_JSON_NAME
        auth = json.loads(auth_json_path.read_text(encoding="utf-8"))

        script_repo_path = repo / AUTH_REL / SCRIPT_NAME
        script_sha = sha256_path(script_repo_path)

        if script_sha != auth["one_time_verifier"]["sha256"]:
            raise RuntimeError("ONE_TIME_VERIFIER_SHA256_MISMATCH")

        if auth["decision"] != "0218":
            raise RuntimeError("AUTHORIZATION_DECISION_MISMATCH")
        if auth["returned_review"]["sha256"] != EXPECTED_RETURNED_SHA256:
            raise RuntimeError("AUTHORIZATION_RETURNED_SHA_BINDING_MISMATCH")
        if auth["returned_packet_facts"]["overall_review_decision"] != "REVISION_REQUIRED":
            raise RuntimeError("OVERALL_DECISION_BINDING_MISMATCH")
        if auth["returned_packet_facts"]["fresh_pass_items"] != ["ASER01", "ASER02"]:
            raise RuntimeError("FRESH_PASS_ITEMS_BINDING_MISMATCH")
        if auth["returned_packet_facts"]["fresh_revision_required_items"] != ["ASER04", "ASER07"]:
            raise RuntimeError("FRESH_REVISION_ITEMS_BINDING_MISMATCH")

        result.update({
            "authorization_commit": head,
            "authorization_parent": parent,
            "authorization_parent_tree": parent_tree,
            "execution_exit_code": 0,
            "execution_result": "PASS",
            "one_time_verifier_sha256": script_sha,
            "returned_review_sha256": EXPECTED_RETURNED_SHA256,
            "returned_review_size_bytes": EXPECTED_RETURNED_SIZE
        })
        write_json_atomic(SENTINEL, result)

        print("D0218_EXACT_RETURNED_REREVIEW_RECORDING_AUTHORIZATION_VERIFIER=PASS")
        print("AUTHORIZATION_COMMIT=" + head)
        print("AUTHORIZATION_PARENT=" + parent)
        print("D0217_HANDOFF_RECORD_TREE=" + handoff_tree)
        print("RETURNED_REREVIEW_SHA256=" + EXPECTED_RETURNED_SHA256)
        print("RETURNED_REREVIEW_SIZE=" + str(EXPECTED_RETURNED_SIZE))
        print("FRESH_PASS_ITEMS=ASER01,ASER02")
        print("FRESH_REVISION_REQUIRED_ITEMS=ASER04,ASER07")
        print("PRESERVED_PREDECESSOR_PASS_ITEMS=ASER03,ASER05,ASER06,ASER08,ASER09")
        print("OVERALL_REREVIEW_DECISION=REVISION_REQUIRED")
        print("EXACT_RETURNED_REREVIEW_RECORDING_AUTHORIZED=YES")
        print("EXACT_RETURNED_REREVIEW_RECORDED_BY_THIS_VERIFIER=NO")
        print("CORRECTIVE_SUCCESSOR_REVISION_AUTHORIZED=NO")
        print("ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
        print("DOMAIN_ACQUISITION_AUTHORIZED=NO")
        print("FORWARD_WITNESS_ACQUISITION_AUTHORIZED=NO")
        print("REVERSE_WITNESS_ACQUISITION_AUTHORIZED=NO")
        print("CONCRETE_MAPPING_AUTHORIZED=NO")
        print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
        print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
        print("SCHEMA_MODIFICATION_AUTHORIZED=NO")
        print("ANALYZER_AUTHORIZED=NO")
        print("BASELINE_AUTHORIZED=NO")
        print("REPAIR_AUTHORIZED=NO")
        print("D0218_A02_EXECUTION_ATTEMPT_COUNT_FOR_THIS_RUN=1")
        print("D0218_A02_RERUN_AUTHORIZED=NO")
        return 0

    except Exception as exc:
        result.update({
            "execution_exit_code": 1,
            "execution_result": "FAIL",
            "failure_type": type(exc).__name__,
            "failure_message": str(exc)
        })
        write_json_atomic(SENTINEL, result)
        print("D0218_EXACT_RETURNED_REREVIEW_RECORDING_AUTHORIZATION_VERIFIER=FAIL", file=sys.stderr)
        print("D0218_A02_RERUN_AUTHORIZED=NO", file=sys.stderr)
        print(type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
