#!/usr/bin/env python3

from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys


D0268_COMMIT = "b90b15a547766dc38851181c6d38ea8f329f4cb9"
D0268_TREE = "3dcb4c33918930ddd4a18d9836c5f8c28762a913"
D0268_SUBJECT = (
    "decision: execute bounded D0266 validated targeted positive-evidence "
    "successor sufficiency resolution"
)

REMOTE_PUBLISHED_FLOOR = D0268_COMMIT

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

D0258_PRIMARY = (
    BASE
    / "d0258_bounded_positional_inference_evidence_sufficiency_assessment_execution_v1"
    / "01_bounded_positional_inference_evidence_sufficiency_assessment_execution.v1.json"
)

D0260_PRIMARY = (
    BASE
    / "d0260_d0258_full_result_independent_content_and_sufficiency_revalidation_execution_v1"
    / "01_d0258_full_result_independent_content_and_sufficiency_revalidation_execution.v1.json"
)

D0262_PRIMARY = (
    BASE
    / "d0262_d0260_mismatch_sufficiency_successor_adjudication_execution_v1"
    / "01_d0260_mismatch_sufficiency_successor_adjudication_execution.v1.json"
)

D0268_PRIMARY = (
    BASE
    / "d0268_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_execution_v1"
    / "01_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_execution.v1.json"
)

EXPECTED_SHA = {
    D0258_PRIMARY:
        "4aa389ad41c3a532c61c3b38aa397da6dccebb96d3384bb6a22d1e0af6462e60",
    D0260_PRIMARY:
        "2b643b788509bff45b0a0756f530da4c5da90cd0d523347917d49d83660da807",
    D0262_PRIMARY:
        "542bb55d2405b95120e88b5a8051eda36df6f560e6c8cc854c20dec54b63ea36",
    D0268_PRIMARY:
        "f23144605bfca713a8d7110f09bde7b9782115c4af4cca6ce3b45e1fb50c11cd",
}

UNIVERSE_SHA = (
    "a87715860953980ae9a39fc89a3c8242683189d79098240566a325c7944cfe85"
)

D0269_PACKAGE = (
    BASE
    / "d0269_successor_result_universe_materialization_authorization_v1"
)

D0269_RECORD = (
    D0269_PACKAGE
    / "01_successor_result_universe_materialization_authorization.v1.json"
)

D0269_SCOPE = (
    D0269_PACKAGE
    / "02_successor_result_universe_materialization_authorization_scope.v1.md"
)

D0269_VERIFIER = (
    D0269_PACKAGE
    / "03_verify_successor_result_universe_materialization_authorization.v1.py"
)

D0269_MANIFEST = (
    D0269_PACKAGE
    / "04_successor_result_universe_materialization_authorization.v1.SHA256SUMS"
)

D0269_DECISION = Path(
    "documentation/decisions/"
    "0269-authorize-successor-result-universe-materialization-from-frozen-resolved-components-without-execution.md"
)

D0269_SUBJECT = (
    "decision: authorize successor result-universe materialization "
    "from frozen resolved components without execution"
)

ENUM = {
    "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION",
    "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED",
    "SUFFICIENCY_REMAINS_INDETERMINATE",
}


def die(msg):
    print("SAFE_D0269_VERIFIER=FAIL")
    print("FAIL_REASON=" + msg)
    raise SystemExit(1)


def git(repo, *args, check=True):
    p = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if check and p.returncode != 0:
        die("git command failed: git " + " ".join(args))

    return p


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate_dicts(obj, index):
    out = []

    def walk(x):
        if isinstance(x, dict):
            if x.get("candidate_index") == index:
                out.append(x)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(obj)
    return out


def unique_values(dicts, predicate):
    vals = []

    for d in dicts:
        for k, v in d.items():
            if isinstance(v, str) and predicate(k.lower(), v):
                vals.append(v)

    return sorted(set(vals))


parser = argparse.ArgumentParser()
parser.add_argument("--precommit", action="store_true")
args = parser.parse_args()

repo_probe = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

if repo_probe.returncode != 0:
    die("not inside git repository")

repo = Path(repo_probe.stdout.strip())

head = git(repo, "rev-parse", "HEAD").stdout.strip()
origin = git(repo, "rev-parse", "origin/main").stdout.strip()

# origin/main is mutable publication metadata, not scientific evidence.
# Require only that the independently verified/frozen D0268 checkpoint
# remains contained in the published remote lineage.  This preserves
# descendant-rerunnable verification after later verified checkpoints
# are published.
git(repo, "merge-base", "--is-ancestor", REMOTE_PUBLISHED_FLOOR, origin)

tree = git(repo, "rev-parse", f"{D0268_COMMIT}^{{tree}}").stdout.strip()
subject = git(
    repo,
    "show",
    "-s",
    "--format=%s",
    D0268_COMMIT,
).stdout.strip()

if tree != D0268_TREE:
    die("D0268 tree mismatch")

if subject != D0268_SUBJECT:
    die("D0268 subject mismatch")

if args.precommit:
    if head != D0268_COMMIT:
        die("precommit HEAD must equal D0268")
else:
    decision_commit = git(
        repo,
        "log",
        "-1",
        "--format=%H",
        "--",
        str(D0269_DECISION),
    ).stdout.strip()

    if not decision_commit:
        die("cannot resolve committed D0269 decision")

    decision_subject = git(
        repo,
        "show",
        "-s",
        "--format=%s",
        decision_commit,
    ).stdout.strip()

    decision_parent = git(
        repo,
        "rev-parse",
        f"{decision_commit}^",
    ).stdout.strip()

    if decision_subject != D0269_SUBJECT:
        die("D0269 subject mismatch")

    if decision_parent != D0268_COMMIT:
        die("D0269 parent is not exact D0268")

    ancestry = git(
        repo,
        "merge-base",
        "--is-ancestor",
        decision_commit,
        head,
        check=False,
    )

    if ancestry.returncode != 0:
        die("D0269 is not ancestor-or-equal of current HEAD")

for rel, expected in EXPECTED_SHA.items():
    path = repo / rel

    if not path.is_file():
        die("missing frozen primary: " + str(rel))

    if sha256(path) != expected:
        die("frozen primary SHA mismatch: " + str(rel))

record_path = repo / D0269_RECORD
scope_path = repo / D0269_SCOPE
verifier_path = repo / D0269_VERIFIER
manifest_path = repo / D0269_MANIFEST
decision_path = repo / D0269_DECISION

for path in [
    record_path,
    scope_path,
    verifier_path,
    manifest_path,
    decision_path,
]:
    if not path.is_file():
        die("missing D0269 artifact: " + str(path.relative_to(repo)))

raw_record = record_path.read_bytes()

try:
    record = json.loads(raw_record.decode("utf-8"))
except Exception:
    die("D0269 record JSON decode failed")

canonical_record = json.dumps(
    record,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

if raw_record != canonical_record:
    die("D0269 record is not exact canonical JSON")

if raw_record.endswith(b"\n"):
    die("D0269 canonical record unexpectedly has final LF")

for rel, expected in EXPECTED_SHA.items():
    if sha256(repo / rel) != expected:
        die("frozen identity changed during verification")

d0260 = json.loads((repo / D0260_PRIMARY).read_text(encoding="utf-8"))
d0262 = json.loads((repo / D0262_PRIMARY).read_text(encoding="utf-8"))
d0268 = json.loads((repo / D0268_PRIMARY).read_text(encoding="utf-8"))

matched = {}

for idx in [1, 2, 3, 6, 7, 10]:
    ds = candidate_dicts(d0260, idx)

    if not ds:
        die(f"missing D0260 candidate {idx}")

    independent = unique_values(
        ds,
        lambda k, v: "independent" in k and "result" in k and v in ENUM,
    )

    recorded = unique_values(
        ds,
        lambda k, v:
            "recorded" in k and
            "d0258" in k and
            "result" in k and
            v in ENUM,
    )

    comparison = unique_values(
        ds,
        lambda k, v: "comparison" in k and v == "REVALIDATION_MATCH",
    )

    if len(independent) != 1:
        die(f"D0260 candidate {idx} independent result not unique")

    if len(recorded) != 1:
        die(f"D0260 candidate {idx} D0258 result not unique")

    if independent[0] != recorded[0]:
        die(f"D0260 candidate {idx} match disagreement")

    if comparison != ["REVALIDATION_MATCH"]:
        die(f"D0260 candidate {idx} not a verified match")

    matched[idx] = independent[0]

expected_matched = {
    1: "SUFFICIENCY_REMAINS_INDETERMINATE",
    2: "SUFFICIENCY_REMAINS_INDETERMINATE",
    3: "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED",
    6: "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION",
    7: "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED",
    10: "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED",
}

if matched != expected_matched:
    die("matched-six result profile mismatch")

ds5 = candidate_dicts(d0262, 5)

r5 = unique_values(
    ds5,
    lambda k, v: "successor" in k and "result" in k and v in ENUM,
)

if r5 != [
    "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED"
]:
    die("candidate 5 D0262 successor result mismatch")

r0268 = d0268.get("candidate_successor_sufficiency_resolutions")

if not isinstance(r0268, list):
    die("D0268 candidate resolution list missing")

if [r.get("candidate_index") for r in r0268] != [8, 9]:
    die("D0268 candidate order mismatch")

sufficient = (
    "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION"
)

r8 = r0268[0].get("successor_sufficiency_result")
r9 = r0268[1].get("successor_sufficiency_result")

if r8 != sufficient or r9 != sufficient:
    die("D0268 candidate 8/9 result mismatch")

universe = [
    {
        "candidate_index": 1,
        "source_component":
            "D0258_RESULT_CONFIRMED_BY_D0260_REVALIDATION_MATCH",
        "successor_sufficiency_result": matched[1],
    },
    {
        "candidate_index": 2,
        "source_component":
            "D0258_RESULT_CONFIRMED_BY_D0260_REVALIDATION_MATCH",
        "successor_sufficiency_result": matched[2],
    },
    {
        "candidate_index": 3,
        "source_component":
            "D0258_RESULT_CONFIRMED_BY_D0260_REVALIDATION_MATCH",
        "successor_sufficiency_result": matched[3],
    },
    {
        "candidate_index": 5,
        "source_component":
            "D0262_VERIFIED_SUCCESSOR_RESOLUTION",
        "successor_sufficiency_result": r5[0],
    },
    {
        "candidate_index": 6,
        "source_component":
            "D0258_RESULT_CONFIRMED_BY_D0260_REVALIDATION_MATCH",
        "successor_sufficiency_result": matched[6],
    },
    {
        "candidate_index": 7,
        "source_component":
            "D0258_RESULT_CONFIRMED_BY_D0260_REVALIDATION_MATCH",
        "successor_sufficiency_result": matched[7],
    },
    {
        "candidate_index": 8,
        "source_component":
            "D0268_VERIFIED_SUCCESSOR_RESOLUTION",
        "successor_sufficiency_result": r8,
    },
    {
        "candidate_index": 9,
        "source_component":
            "D0268_VERIFIED_SUCCESSOR_RESOLUTION",
        "successor_sufficiency_result": r9,
    },
    {
        "candidate_index": 10,
        "source_component":
            "D0258_RESULT_CONFIRMED_BY_D0260_REVALIDATION_MATCH",
        "successor_sufficiency_result": matched[10],
    },
]

universe_bytes = json.dumps(
    universe,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

if hashlib.sha256(universe_bytes).hexdigest() != UNIVERSE_SHA:
    die("successor result-universe SHA mismatch")

binding = record.get("successor_result_universe_binding")

if not isinstance(binding, dict):
    die("universe binding missing")

if binding.get("candidate_count") != 9:
    die("candidate count binding mismatch")

if binding.get("candidate_order") != [1, 2, 3, 5, 6, 7, 8, 9, 10]:
    die("candidate order binding mismatch")

if binding.get("canonical_projection_sha256") != UNIVERSE_SHA:
    die("universe hash binding mismatch")

if binding.get("candidate_results") != universe:
    die("bound universe differs from recomputed universe")

summary = binding.get("summary", {})

if summary != {
    "sufficient_count": 3,
    "sufficient_indices": [6, 8, 9],
    "insufficient_count": 4,
    "insufficient_indices": [3, 5, 7, 10],
    "indeterminate_count": 2,
    "indeterminate_indices": [1, 2],
}:
    die("summary binding mismatch")

if binding.get("candidate_4_included") is not False:
    die("candidate 4 inclusion boundary mismatch")

contract = record.get("materialization_contract", {})

required_contract = {
    "semantics":
        "AGGREGATION_OF_ALREADY_RESOLVED_COMPONENTS_ONLY",
    "successor_result_universe_materialization_authorized": True,
    "successor_result_universe_materialization_executed": False,
    "execution_allowed_before_independent_d0269_checkpoint": False,
    "result_reselection_authorized": False,
    "evidence_rejudgment_authorized": False,
    "new_semantic_adjudication_authorized": False,
    "new_evidence_acquisition_authorized": False,
    "d0251_snapshot_content_read_authorized": False,
    "original_source_blob_reopen_authorized": False,
    "historical_result_mutation_authorized": False,
    "materialized_universe_must_equal_bound_projection": True,
    "materialized_universe_must_preserve_candidate_order": True,
}

if contract != required_contract:
    die("materialization contract mismatch")

boundaries = record.get("execution_boundaries", {})

required_false_boundaries = [
    "positional_status_adjudication_authorized",
    "positional_status_assignment_authorized",
    "class06_reclassification_authorized",
    "c4_authorized",
    "c5_authorized",
    "c6_authorized",
    "b2_readiness_established",
    "b2_authorized",
    "b2_executed",
    "active_schema_v2_materialization_authorized",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
]

for key in required_false_boundaries:
    if boundaries.get(key) is not False:
        die("forbidden boundary enabled: " + key)

if record.get("authorizing_decision") != "D0269":
    die("authorizing decision mismatch")

if record.get("designated_execution_decision") != "D0270":
    die("designated execution decision mismatch")

if record.get("next_required_checkpoint") != (
    "INDEPENDENT_READ_ONLY_VERIFY_D0269_AUTHORIZATION_BEFORE_D0270_EXECUTION"
):
    die("next checkpoint mismatch")

scope = scope_path.read_text(encoding="utf-8")
decision = decision_path.read_text(encoding="utf-8")

required_scope_phrases = [
    "AGGREGATION_OF_ALREADY_RESOLVED_COMPONENTS_ONLY",
    "No D0251 snapshot content read is authorized.",
    "D0270 execution is not allowed before an independent read-only D0269",
    "6, 8, and 9",
    "3, 5, 7, and 10",
    "1 and 2",
]

for phrase in required_scope_phrases:
    if phrase not in scope:
        die("required scope phrase missing: " + phrase)

required_decision_phrases = [
    "This authorization does not execute D0270.",
    "a87715860953980ae9a39fc89a3c8242683189d79098240566a325c7944cfe85",
    "D0270 execution remains prohibited until D0269 has been independently verified",
    "No push is authorized by this decision.",
]

for phrase in required_decision_phrases:
    if phrase not in decision:
        die("required decision phrase missing: " + phrase)

manifest_lines = manifest_path.read_text(encoding="utf-8").splitlines()

expected_manifest_names = [
    D0269_RECORD.name,
    D0269_SCOPE.name,
    D0269_VERIFIER.name,
]

if len(manifest_lines) != 3:
    die("manifest entry count is not 3")

seen_names = []

for line in manifest_lines:
    parts = line.split(None, 1)

    if len(parts) != 2:
        die("malformed manifest entry")

    expected_hash, filename = parts
    filename = filename.lstrip("*")

    if "/" in filename:
        die("manifest filename must be package-local")

    seen_names.append(filename)

    path = repo / D0269_PACKAGE / filename

    if not path.is_file():
        die("manifest target missing: " + filename)

    if sha256(path) != expected_hash:
        die("manifest hash mismatch: " + filename)

if seen_names != expected_manifest_names:
    die("manifest entry order/name mismatch")

print("D0269_SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_AUTHORIZATION_VERIFIER=PASS")
print("D0268_FROZEN_PARENT_BINDING=PASS")
print("D0269_RESOLVED_COMPONENT_IDENTITY_BINDING=PASS")
print("D0269_SUCCESSOR_RESULT_UNIVERSE_BINDING=PASS")
print("D0269_AUTHORIZATION_SEMANTICS=PASS")
print("D0270_SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_AUTHORIZED=YES")
print("D0270_SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_EXECUTED=NO")
print("D0270_EXECUTION_ALLOWED_BEFORE_INDEPENDENT_D0269_CHECKPOINT=NO")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0269_VERIFIER=NO")
print("RESULT_RESELECTION_PERFORMED_BY_D0269_VERIFIER=NO")
print("EVIDENCE_REJUDGED_BY_D0269_VERIFIER=NO")
print("POSITIONAL_STATUS_ADJUDICATION_AUTHORIZED=NO")
print("POSITIONAL_STATUS_ASSIGNED=NO")
print("CLASS06_RECLASSIFICATION_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("SAFE_D0269_VERIFIER=PASS")
