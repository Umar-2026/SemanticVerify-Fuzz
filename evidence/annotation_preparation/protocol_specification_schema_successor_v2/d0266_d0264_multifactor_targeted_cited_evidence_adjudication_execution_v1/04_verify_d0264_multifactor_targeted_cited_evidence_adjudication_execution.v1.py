#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")
BASE = Path("evidence/annotation_preparation/protocol_specification_schema_successor_v2")

D0265_COMMIT = "49267874286e72e26414969175333e5301b8fab2"
D0265_RECORD_SHA = "314db022baffcb5a7115e88968df380dc8635229482a71d7049511cd50415927"
D0264_COMMIT = "28a2eb573c88bedd8a0f2b527814cfd8ebe8406e"

D0265_RECORD = REPO / BASE / "d0265_d0264_multifactor_targeted_cited_evidence_adjudication_authorization_v1/01_d0264_multifactor_targeted_cited_evidence_adjudication_authorization.v1.json"
D0264_PRIMARY = REPO / BASE / "d0264_d0262_unresolved_three_way_discrepancy_basis_characterization_execution_v1/01_d0262_unresolved_three_way_discrepancy_basis_characterization_execution.v1.json"
D0258_PRIMARY = REPO / BASE / "d0258_bounded_positional_inference_evidence_sufficiency_assessment_execution_v1/01_bounded_positional_inference_evidence_sufficiency_assessment_execution.v1.json"
D0260_PRIMARY = REPO / BASE / "d0260_d0258_full_result_independent_content_and_sufficiency_revalidation_execution_v1/01_d0258_full_result_independent_content_and_sufficiency_revalidation_execution.v1.json"
D0262_PRIMARY = REPO / BASE / "d0262_d0260_mismatch_sufficiency_successor_adjudication_execution_v1/01_d0260_mismatch_sufficiency_successor_adjudication_execution.v1.json"

D0264_PRIMARY_SHA = "45cfc7e3105120e9ede8eb74d54b987c3a57c0e3010eb4c8e028178d1990bf09"
D0258_PRIMARY_SHA = "4aa389ad41c3a532c61c3b38aa397da6dccebb96d3384bb6a22d1e0af6462e60"
D0260_PRIMARY_SHA = "2b643b788509bff45b0a0756f530da4c5da90cd0d523347917d49d83660da807"
D0262_PRIMARY_SHA = "542bb55d2405b95120e88b5a8051eda36df6f560e6c8cc854c20dec54b63ea36"

TARGET_LOCATOR_UNIVERSE_SHA = "0be5087f66e27dce13ad2271ea69c8cce58441ef318ceb8c624b9c4ab0d30bea"
TARGET_MAPPING_UNIVERSE_SHA = "37bf22a6c4367a803802b8d3f66aea50fbf6e6784661d77f1bf7d9fe1534f06f"
BLIND_SHA = "0bb75cf6eef2ab817ccf87a368056dc37684c60c68aa5c51a0974810d1889d2a"
PART_A_TRACE_SHA = "6d9e3cfb788d1d46690ac02c6e39ed1ba3ccc84cae386b828d644f22f6bd36f2"

PACKAGE_REL = BASE / "d0266_d0264_multifactor_targeted_cited_evidence_adjudication_execution_v1"

PRIMARY_NAME = "01_d0264_multifactor_targeted_cited_evidence_adjudication_execution.v1.json"
SCOPE_NAME = "02_d0264_multifactor_targeted_cited_evidence_adjudication_execution_scope.v1.md"
TRACE_NAME = "03_d0264_multifactor_targeted_cited_evidence_adjudication_execution_trace.v1.jsonl"
SELF_NAME = "04_verify_d0264_multifactor_targeted_cited_evidence_adjudication_execution.v1.py"
MANIFEST_NAME = "05_d0264_multifactor_targeted_cited_evidence_adjudication_execution.v1.SHA256SUMS"

EST = "EXPLICIT_POSITIONAL_ASSOCIATION_SUPPORT_ESTABLISHED"
NOT = "EXPLICIT_POSITIONAL_ASSOCIATION_SUPPORT_NOT_ESTABLISHED"
AMB = "TARGET_EVIDENCE_UNIT_REMAINS_AMBIGUOUS"

VALID = "TARGETED_POSITIVE_EVIDENCE_VALIDATED"
NOT_VALID = "TARGETED_POSITIVE_EVIDENCE_NOT_VALIDATED"
INDET = "TARGETED_POSITIVE_EVIDENCE_REMAINS_INDETERMINATE"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(REPO), *args],
        text=True,
    ).strip()

def load_json_no_dups(path):
    raw = path.read_bytes()
    def hook(pairs):
        out = {}
        for k, v in pairs:
            assert k not in out
            out[k] = v
        return out
    obj = json.loads(raw.decode("utf-8"), object_pairs_hook=hook)
    return obj, raw

def canonical_bytes(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")

def candidate_record(obj, idx, required_key):
    found = []
    def walk(v):
        if isinstance(v, dict):
            if str(v.get("candidate_index")) == str(idx) and required_key in v:
                found.append(v)
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(obj)
    assert len(found) == 1
    return found[0]

def aggregate(locator_records):
    js = [x["target_evidence_judgment"] for x in locator_records]
    if EST in js:
        return VALID
    if all(x == NOT for x in js):
        return NOT_VALID
    return INDET

def expected_provenance(idx, targets, source_objects):
    out = []
    for kind, value in targets:
        bindings = []
        for source_name, obj, result_key, evidence_key in source_objects:
            rec = candidate_record(obj, idx, result_key)
            refs = rec.get(evidence_key, [])
            matches = [
                r for r in refs
                if r.get("locator_kind") == kind
                and r.get("locator_value") == value
            ]
            if matches:
                purposes = sorted({
                    r.get("evidence_purpose")
                    for r in matches
                    if r.get("evidence_purpose") is not None
                })
                bindings.append({
                    "source_record":source_name,
                    "recorded_result":rec[result_key],
                    "evidence_purposes":purposes,
                })
        assert bindings
        out.append({
            "locator_kind":kind,
            "locator_value":value,
            "source_bindings":bindings,
        })
    return out

ap = argparse.ArgumentParser()
ap.add_argument("--package-root", default=None)
ap.add_argument("--precommit", action="store_true")
args = ap.parse_args()

pkg = Path(args.package_root) if args.package_root else REPO / PACKAGE_REL

primary_path = pkg / PRIMARY_NAME
scope_path = pkg / SCOPE_NAME
trace_path = pkg / TRACE_NAME
self_path = pkg / SELF_NAME
manifest_path = pkg / MANIFEST_NAME

assert sha(D0265_RECORD) == D0265_RECORD_SHA
assert sha(D0264_PRIMARY) == D0264_PRIMARY_SHA
assert sha(D0258_PRIMARY) == D0258_PRIMARY_SHA
assert sha(D0260_PRIMARY) == D0260_PRIMARY_SHA
assert sha(D0262_PRIMARY) == D0262_PRIMARY_SHA

if args.precommit:
    assert git("rev-parse", "HEAD") == D0265_COMMIT
else:
    primary_rel = str(PACKAGE_REL / PRIMARY_NAME)
    d0266_commit = git(
        "log", "--diff-filter=A", "-1", "--format=%H", "--", primary_rel
    )
    assert d0266_commit
    assert git("rev-parse", f"{d0266_commit}^") == D0265_COMMIT
    assert git("merge-base", "--is-ancestor", d0266_commit, "HEAD") == ""

manifest_lines = [
    x for x in manifest_path.read_text(encoding="utf-8").splitlines()
    if x.strip()
]
assert len(manifest_lines) == 4

expected_names = {PRIMARY_NAME, SCOPE_NAME, TRACE_NAME, SELF_NAME}
seen_names = set()

for line in manifest_lines:
    digest, name = line.split("  ", 1)
    assert len(digest) == 64
    assert name in expected_names
    assert sha(pkg / name) == digest
    seen_names.add(name)

assert seen_names == expected_names
assert MANIFEST_NAME not in seen_names

primary, primary_bytes = load_json_no_dups(primary_path)
assert primary_bytes == canonical_bytes(primary)
assert not primary_bytes.endswith(b"\n")

assert set(primary.keys()) == {
    "adjudication_id",
    "authorization_binding",
    "d0264_multifactor_input_binding",
    "targeted_locator_universe_binding",
    "targeted_snapshot_mapping_binding",
    "blind_adjudication_contract",
    "candidate_targeted_adjudications",
    "adjudication_summary",
    "execution_boundaries",
    "results",
    "next_required_checkpoint",
}

assert primary["authorization_binding"]["d0265_authorization_commit"] == D0265_COMMIT
assert primary["d0264_multifactor_input_binding"]["d0264_commit"] == D0264_COMMIT

assert primary["targeted_locator_universe_binding"] == {
    "target_locator_count":5,
    "sha256":TARGET_LOCATOR_UNIVERSE_SHA,
}
assert primary["targeted_snapshot_mapping_binding"] == {
    "candidate_count":2,
    "sha256":TARGET_MAPPING_UNIVERSE_SHA,
}

blind_contract = primary["blind_adjudication_contract"]
assert blind_contract["blind_judgment_record_sha256"] == BLIND_SHA
assert blind_contract["blind_judgment_count"] == 5
assert blind_contract["source_attribution_gate_opened_only_after_all_five_judgments_recorded_and_hashed"] is True
assert blind_contract["post_gate_blind_judgment_mutation_allowed"] is False
assert set(blind_contract["allowed_judgments"]) == {EST, NOT, AMB}

cands = primary["candidate_targeted_adjudications"]
assert [x["candidate_index"] for x in cands] == [8, 9]
assert len(cands[0]["target_locator_records"]) == 4
assert len(cands[1]["target_locator_records"]) == 1

all_locator_records = (
    cands[0]["target_locator_records"] +
    cands[1]["target_locator_records"]
)
assert len(all_locator_records) == 5

for row in all_locator_records:
    assert set(row.keys()) == {
        "candidate_index",
        "locator_kind",
        "locator_value",
        "extracted_unit_sha256",
        "target_evidence_judgment",
        "bounded_judgment_rationale",
    }
    assert row["target_evidence_judgment"] in {EST, NOT, AMB}
    assert len(row["extracted_unit_sha256"]) == 64

assert aggregate(cands[0]["target_locator_records"]) == cands[0]["targeted_positive_evidence_result"]
assert aggregate(cands[1]["target_locator_records"]) == cands[1]["targeted_positive_evidence_result"]

assert cands[0]["targeted_positive_evidence_result"] == VALID
assert cands[1]["targeted_positive_evidence_result"] == VALID

summary = primary["adjudication_summary"]
assert summary == {
    "candidate_count":2,
    "validated_count":2,
    "not_validated_count":0,
    "indeterminate_count":0,
}

# Reconstruct exact normalized blind record from committed primary.
blind_ids = [
    "D0266-U01",
    "D0266-U02",
    "D0266-U03",
    "D0266-U04",
    "D0266-U05",
]

reconstructed = []
for blind_id, row in zip(blind_ids, all_locator_records):
    reconstructed.append({
        "blind_unit_id":blind_id,
        "candidate_index":row["candidate_index"],
        "locator_kind":row["locator_kind"],
        "locator_value":row["locator_value"],
        "extracted_unit_sha256":row["extracted_unit_sha256"],
        "target_evidence_judgment":row["target_evidence_judgment"],
        "bounded_judgment_rationale":row["bounded_judgment_rationale"],
    })

blind_bytes = (
    "\n".join(
        json.dumps(x, ensure_ascii=False, separators=(",", ":"))
        for x in reconstructed
    ) + "\n"
).encode("utf-8")

assert hashlib.sha256(blind_bytes).hexdigest() == BLIND_SHA

o0258, _ = load_json_no_dups(D0258_PRIMARY)
o0260, _ = load_json_no_dups(D0260_PRIMARY)
o0262, _ = load_json_no_dups(D0262_PRIMARY)

source_objects = [
    ("D0258", o0258,
     "positional_inference_evidence_sufficiency_result",
     "evidence_references"),
    ("D0260", o0260,
     "independent_sufficiency_result",
     "independent_evidence_references"),
    ("D0262", o0262,
     "tie_breaker_sufficiency_result",
     "tie_breaker_evidence_references"),
]

p8 = expected_provenance(
    8,
    [
        ("LINE_RANGE","L50-L50"),
        ("LINE_RANGE","L51-L51"),
        ("LINE_RANGE","L61-L61"),
        ("LINE_RANGE","L84-L84"),
    ],
    source_objects,
)
p9 = expected_provenance(
    9,
    [("LINE_RANGE","L195-L195")],
    source_objects,
)

assert cands[0]["post_gate_source_provenance_binding"] == p8
assert cands[1]["post_gate_source_provenance_binding"] == p9

trace_lines = trace_path.read_bytes().splitlines(keepends=True)
assert len(trace_lines) == 11

part_a_prefix = b"".join(trace_lines[:4])
assert hashlib.sha256(part_a_prefix).hexdigest() == PART_A_TRACE_SHA

appended = [
    json.loads(x.decode("utf-8"))
    for x in trace_lines[4:]
]

expected_stage_names = [
    "MARK_BLIND_TARGETED_ADJUDICATION_ABOUT_TO_BEGIN",
    "ADJUDICATE_ALL_CANDIDATE_008_TARGET_LOCATORS",
    "DURABLY_RECORD_CANDIDATE_008_AGGREGATE",
    "ADJUDICATE_ALL_CANDIDATE_009_TARGET_LOCATORS",
    "DURABLY_RECORD_CANDIDATE_009_AGGREGATE",
    "HASH_BLIND_JUDGMENT_RECORD_AND_OPEN_SOURCE_ATTRIBUTION_GATE",
    "BIND_POST_GATE_PRIOR_SOURCE_PROVENANCE_WITHOUT_CHANGING_BLIND_JUDGMENTS",
]

assert [x["stage"] for x in appended] == [5,6,7,8,9,10,11]
assert [x["stage_name"] for x in appended] == expected_stage_names
assert appended[5]["blind_judgment_record_sha256"] == BLIND_SHA
assert appended[5]["source_attribution_gate_open"] is True
assert appended[6]["blind_judgments_mutated"] is False

bounds = primary["execution_boundaries"]
assert bounds["part_a_snapshot_filesystem_read_count"] == 2
assert bounds["part_b_snapshot_filesystem_read_count"] == 0
assert bounds["snapshot_reread_after_part_a"] is False
assert bounds["semantic_rejudgment_by_part_b"] is False
assert bounds["final_sufficiency_result_selection"] is False
assert bounds["positional_status_assignment"] is False
assert bounds["class06_reclassification"] is False

results = primary["results"]
assert results["candidate_8_targeted_positive_evidence_result"] == VALID
assert results["candidate_9_targeted_positive_evidence_result"] == VALID
assert results["final_sufficiency_result_selected"] is False
assert results["positional_status_assigned"] is False
assert results["class06_reclassified"] is False
assert results["successor_result_universe_materialization_authorized"] is False

assert primary["next_required_checkpoint"] == \
    "INDEPENDENT_READ_ONLY_VERIFY_D0266_TARGETED_EVIDENCE_ADJUDICATION_WITHOUT_D0251_SNAPSHOT_REREAD"

print("D0266_TARGETED_EVIDENCE_ADJUDICATION_EXECUTION_VERIFIER=PASS")
print("D0265_AUTHORIZATION_BINDING=PASS")
print("D0264_MULTIFACTOR_INPUT_BINDING=PASS")
print("D0266_TARGETED_LOCATOR_UNIVERSE_BINDING=PASS")
print("D0266_TARGETED_SNAPSHOT_MAPPING_BINDING=PASS")
print("D0266_PRIMARY_JSON_CANONICALIZATION=PASS")
print("D0266_EXACT_CANDIDATE_ORDER_8_9=PASS")
print("D0266_EXACT_FIVE_LOCATOR_RECORDS=PASS")
print("D0266_BLIND_JUDGMENT_RECORD_RECONSTRUCTION=PASS")
print("D0266_BLIND_GATE_ORDERING=PASS")
print("D0266_POST_GATE_SOURCE_PROVENANCE_BINDING=PASS")
print("D0266_AGGREGATION_FORMULA=PASS")
print("D0266_SUMMARY_COUNTS=PASS")
print("D0266_TRACE_RECORD_COUNT_11=PASS")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0266_SAFE_VERIFIER=NO")
print("D0266_SAFE_VERIFIER_REJUDGED_TARGET_EVIDENCE=NO")
print("D0266_SAFE_VERIFIER_SELECTED_FINAL_SUFFICIENCY_RESULT=NO")
print("D0266_SAFE_VERIFIER_ASSIGNED_POSITIONAL_STATUS=NO")
print("D0266_SAFE_VERIFIER_RECLASSIFIED_CLASS06=NO")
print("SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("SAFE_D0266_VERIFIER=PASS")
