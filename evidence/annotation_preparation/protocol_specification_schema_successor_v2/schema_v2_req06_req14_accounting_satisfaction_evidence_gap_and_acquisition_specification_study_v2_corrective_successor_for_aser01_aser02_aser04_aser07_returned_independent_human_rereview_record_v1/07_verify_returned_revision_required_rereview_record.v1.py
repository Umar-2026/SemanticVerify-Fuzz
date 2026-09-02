#!/usr/bin/env python3
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

EXPECTED_RETURNED_SHA = "8613f25eb8c971d6d38774ea7cd0ac97e8171f1e116854a843e3d346432b7618"
EXPECTED_RETURNED_SIZE = 12091
EXPECTED_A02_SHA = "c31b145422921a13f3658abc509ae12ce610ea966df3c5f0ff97410dce72c257"
EXPECTED_D0218 = "98ff5268efa4a44a09c80f0028863256188a6bbe"
EXPECTED_D0218_TREE = "ce2b6e3316dbfcc9b913b50002c83a1ed3f6913e"
EXPECTED_HANDOFF_TREE = "dae388040a574570aa7156667264abf2271e222c"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", str(repo), *args],
        text=True
    ).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--require-external", action="store_true")
    args = ap.parse_args()

    record = Path(__file__).absolute().parent
    repo = Path(git(record, "rev-parse", "--show-toplevel"))

    exact = record / "01_returned_independent_human_rereview.EXACT_COPY.v1.md"
    binding_path = record / "02_returned_rereview_source_binding.v1.json"
    consumption_path = record / "03_decision0218_a02_consumption_record.v1.json"
    output_path = record / "04_decision0218_a02_execution_output.EXACT_COPY.v1.txt"
    sentinel_path = record / "05_decision0218_a02_consumption_sentinel.EXACT_COPY.v1.json"
    boundary_path = record / "06_returned_rereview_record_boundary.v1.md"
    manifest_path = record / "08_returned_rereview_record.v1.SHA256SUMS"

    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    consumption = json.loads(consumption_path.read_text(encoding="utf-8"))
    sentinel = json.loads(sentinel_path.read_text(encoding="utf-8"))

    if sha256(exact) != EXPECTED_RETURNED_SHA:
        raise RuntimeError("EXACT_RETURNED_REVIEW_SHA_MISMATCH")
    if exact.stat().st_size != EXPECTED_RETURNED_SIZE:
        raise RuntimeError("EXACT_RETURNED_REVIEW_SIZE_MISMATCH")

    b = exact.read_bytes()
    if b.count(b"\r\n") != 114:
        raise RuntimeError("EXACT_RETURNED_REVIEW_CRLF_MISMATCH")
    if b.count(b"\n") != 114:
        raise RuntimeError("EXACT_RETURNED_REVIEW_LF_MISMATCH")
    if b.endswith(b"\n"):
        raise RuntimeError("EXACT_RETURNED_REVIEW_FINAL_NEWLINE_CHANGED")

    ext = Path(binding["external_return"]["path"])
    if args.require_external:
        if not ext.is_file():
            raise RuntimeError("EXTERNAL_RETURN_MISSING")
        if sha256(ext) != EXPECTED_RETURNED_SHA:
            raise RuntimeError("EXTERNAL_RETURN_SHA_MISMATCH")
        if ext.read_bytes() != exact.read_bytes():
            raise RuntimeError("EXTERNAL_AND_REPOSITORY_COPY_NOT_BYTE_IDENTICAL")

    if binding["authorization"]["decision0218_commit"] != EXPECTED_D0218:
        raise RuntimeError("D0218_COMMIT_BINDING_MISMATCH")
    if binding["authorization"]["decision0218_tree"] != EXPECTED_D0218_TREE:
        raise RuntimeError("D0218_TREE_BINDING_MISMATCH")
    if binding["authorization"]["decision0218_a02_sha256"] != EXPECTED_A02_SHA:
        raise RuntimeError("A02_BINDING_MISMATCH")
    if binding["authorization"]["decision0217_handoff_record_tree"] != EXPECTED_HANDOFF_TREE:
        raise RuntimeError("HANDOFF_TREE_BINDING_MISMATCH")

    facts = binding["returned_packet_facts"]
    if facts["fresh_pass_items"] != ["ASER01", "ASER02"]:
        raise RuntimeError("PASS_ITEM_MISMATCH")
    if facts["fresh_revision_required_items"] != ["ASER04", "ASER07"]:
        raise RuntimeError("REVISION_ITEM_MISMATCH")
    if facts["preserved_predecessor_pass_items_not_reopened"] != [
        "ASER03", "ASER05", "ASER06", "ASER08", "ASER09"
    ]:
        raise RuntimeError("PRESERVED_PASS_ITEM_MISMATCH")
    if facts["overall_review_decision"] != "REVISION_REQUIRED":
        raise RuntimeError("OVERALL_DECISION_MISMATCH")

    if consumption["execution_attempt_count"] != 1:
        raise RuntimeError("CONSUMPTION_COUNT_MISMATCH")
    if consumption["execution_result"] != "PASS":
        raise RuntimeError("CONSUMPTION_RESULT_MISMATCH")
    if consumption["state"] != "PERMANENTLY_RETIRED":
        raise RuntimeError("CONSUMPTION_STATE_MISMATCH")
    if consumption["rerun_authorized"] is not False:
        raise RuntimeError("RERUN_BOUNDARY_MISMATCH")

    if sentinel["execution_attempt_count"] != 1:
        raise RuntimeError("SENTINEL_COUNT_MISMATCH")
    if sentinel["execution_result"] != "PASS":
        raise RuntimeError("SENTINEL_RESULT_MISMATCH")
    if sentinel["state"] != "PERMANENTLY_RETIRED":
        raise RuntimeError("SENTINEL_STATE_MISMATCH")
    if sentinel["rerun_authorized"] is not False:
        raise RuntimeError("SENTINEL_RERUN_BOUNDARY_MISMATCH")

    output_text = output_path.read_text(encoding="utf-8")
    required_output = [
        "D0218_EXACT_RETURNED_REREVIEW_RECORDING_AUTHORIZATION_VERIFIER=PASS",
        "EXACT_RETURNED_REREVIEW_RECORDING_AUTHORIZED=YES",
        "FRESH_PASS_ITEMS=ASER01,ASER02",
        "FRESH_REVISION_REQUIRED_ITEMS=ASER04,ASER07",
        "OVERALL_REREVIEW_DECISION=REVISION_REQUIRED",
        "D0218_A02_RERUN_AUTHORIZED=NO",
    ]
    for marker in required_output:
        if marker not in output_text:
            raise RuntimeError("MISSING_EXECUTION_OUTPUT_MARKER=" + marker)

    boundary_text = boundary_path.read_text(encoding="utf-8")
    for marker in [
        "RETURNED_COMPLETED_REREVIEW_RECORDED=YES",
        "OVERALL_REREVIEW_DECISION=REVISION_REQUIRED",
        "CORRECTIVE_SUCCESSOR_APPROVED=NO",
        "CORRECTIVE_SUCCESSOR_REVISION_AUTHORIZED=NO",
        "ANALYZER_AUTHORIZED=NO",
        "BASELINE_AUTHORIZED=NO",
        "REPAIR_AUTHORIZED=NO",
    ]:
        if marker not in boundary_text:
            raise RuntimeError("MISSING_BOUNDARY_MARKER=" + marker)

    manifest_lines = [
        x for x in manifest_path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]

    expected_names = {
        "01_returned_independent_human_rereview.EXACT_COPY.v1.md",
        "02_returned_rereview_source_binding.v1.json",
        "03_decision0218_a02_consumption_record.v1.json",
        "04_decision0218_a02_execution_output.EXACT_COPY.v1.txt",
        "05_decision0218_a02_consumption_sentinel.EXACT_COPY.v1.json",
        "06_returned_rereview_record_boundary.v1.md",
        "07_verify_returned_revision_required_rereview_record.v1.py",
    }

    seen = set()

    for line in manifest_lines:
        digest, rel = line.split(None, 1)
        rel = rel.strip()
        if rel.startswith("./"):
            rel = rel[2:]
        if rel in seen:
            raise RuntimeError("DUPLICATE_MANIFEST_ENTRY=" + rel)
        seen.add(rel)
        p = record / rel
        if not p.is_file():
            raise RuntimeError("MANIFEST_FILE_MISSING=" + rel)
        if sha256(p) != digest:
            raise RuntimeError("MANIFEST_SHA_MISMATCH=" + rel)

    if seen != expected_names:
        raise RuntimeError("MANIFEST_SCOPE_MISMATCH")

    a02_repo = repo / binding["authorization"]["decision0218_a02_path"]
    if not a02_repo.is_file():
        raise RuntimeError("D0218_A02_REPOSITORY_FILE_MISSING")
    if sha256(a02_repo) != EXPECTED_A02_SHA:
        raise RuntimeError("D0218_A02_REPOSITORY_SHA_MISMATCH")

    handoff_tree = git(
        repo,
        "rev-parse",
        binding["authorization"]["decision0218_parent"] + ":" +
        binding["authorization"]["decision0217_handoff_record_path"]
    )
    if handoff_tree != EXPECTED_HANDOFF_TREE:
        raise RuntimeError("RECOMPUTED_HANDOFF_TREE_MISMATCH")

    print("D0219_RETURNED_REREVIEW_RECORD_VERIFIER=PASS")
    print("RETURNED_REREVIEW_SHA256=" + EXPECTED_RETURNED_SHA)
    print("RETURNED_REREVIEW_SIZE=12091")
    print("RETURNED_REREVIEW_CRLF_COUNT=114")
    print("RETURNED_REREVIEW_FINAL_NEWLINE_PRESENT=NO")
    print("FRESH_PASS_ITEMS=ASER01,ASER02")
    print("FRESH_REVISION_REQUIRED_ITEMS=ASER04,ASER07")
    print("PRESERVED_PASS_ITEMS=ASER03,ASER05,ASER06,ASER08,ASER09")
    print("OVERALL_REREVIEW_DECISION=REVISION_REQUIRED")
    print("D0218_A02_STATE=PERMANENTLY_RETIRED")
    print("D0218_A02_RERUN_AUTHORIZED=NO")
    print("CORRECTIVE_SUCCESSOR_REVISION_AUTHORIZED=NO")
    print("PAIR_RECLASSIFICATION_PERFORMED=NO")
    print("ANALYZER_AUTHORIZED=NO")
    print("BASELINE_AUTHORIZED=NO")
    print("REPAIR_AUTHORIZED=NO")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("D0219_RETURNED_REREVIEW_RECORD_VERIFIER=FAIL", file=sys.stderr)
        print(type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        raise
