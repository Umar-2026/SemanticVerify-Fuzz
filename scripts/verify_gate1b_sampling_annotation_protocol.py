#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "config/gold_sampling_annotation_protocol.json"
FRAME_SCHEMA = ROOT / "config/schemas/compilable_sampling_frame.schema.json"
ANNOTATION_SCHEMA = ROOT / "config/schemas/blind_annotation_record.schema.json"
EXPOSURE_SCHEMA = ROOT / "config/schemas/annotation_exposure_registry.schema.json"
REPORT = ROOT / "evidence/gates/gate1/gate1b_sampling_annotation_protocol.json"
LOCK = ROOT / "config/research_lock.json"

def require(condition, reason):
    if not condition:
        print("GATE1B_SAMPLING_ANNOTATION_PROTOCOL=FAIL")
        print(f"REASON={reason}")
        raise SystemExit(1)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for path in [PROTOCOL, FRAME_SCHEMA, ANNOTATION_SCHEMA, EXPOSURE_SCHEMA, REPORT, LOCK]:
    require(path.is_file(), f"missing: {path.relative_to(ROOT)}")

protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
report = json.loads(REPORT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
annotation_schema = json.loads(ANNOTATION_SCHEMA.read_text(encoding="utf-8"))

require(protocol["gate"] == "Gate 1B", "gate")
require(protocol["status"] == "PASS_FROZEN", "status")
require(protocol["sample_size"]["maximum_compilable_drivers"] == 140, "sample cap")
require(protocol["sample_size"]["if_total_compilable_at_most_140"] == "CENSUS", "census")
require(protocol["sample_size"]["post_hoc_expansion_allowed"] is False, "expansion")
require(protocol["sample_size"]["planning_18_per_held_out_library_is_sampling_quota"] is False, "planning quota")
require(protocol["stratification"]["primary_strata"] == ["library", "model_label"], "strata")
require(protocol["stratification"]["maximum_primary_strata"] == 16, "strata count")
require(protocol["allocation_algorithm"]["zero_inclusion_probability_for_eligible_driver"] is False, "zero inclusion")
require(protocol["within_stratum_selection"]["master_seed"] == 2026080603, "seed")
require(protocol["within_stratum_selection"]["replacement_allowed"] is False, "replacement")
require(protocol["selection_probability_and_weights"]["sampled_stratum_inclusion_probability"] == "pi_h=n_h/N_h", "probability")
require(protocol["selection_probability_and_weights"]["inverse_probability_weight"] == "w_h=N_h/n_h", "weight")

roles = protocol["annotation_roles"]
require(roles["primary_annotator_count"] == 2, "annotator count")
require(roles["both_primary_annotators_are_non_author"] is True, "non-author")
require(roles["main_analyzer_or_repair_developer_is_primary_annotator"] is False, "developer annotation")
require(roles["third_adjudicator_required"] is True, "adjudicator")
require(roles["developer_label_substitution_allowed"] is False, "substitution")
require(roles["missing_required_personnel_result"] == "EXPLORATORY_ONLY", "downgrade")

phases = protocol["annotation_phases"]
require([item["order"] for item in phases] == [1, 2, 3, 4, 5], "phase order")
require(phases[0]["name"] == "INDEPENDENT_WHOLE_DRIVER_DISCOVERY", "discovery first")
require(phases[-1]["name"] == "GOLD_FREEZE", "gold freeze")
require(protocol["exposure_quarantine"]["any_disqualifying_exposure_blocks_annotation_for_that_driver"] is True, "quarantine")

gold = protocol["human_gold_verdict_contract"]
require(gold["in_scope_verdicts"] == ["VALID", "VIOLATION-MUST", "VIOLATION-MAY"], "human gold verdicts")
require(gold["analyzer_unknown_is_human_gold_label"] is False, "gold UNKNOWN")
require(gold["out_of_scope_receives_validity_verdict"] is False, "out-of-scope verdict")
require(gold["verdict_phase_requires_explicit_eligibility"] is True, "verdict eligibility")
require(gold["violation_requires_D1_through_D8_category"] is True, "violation category")
require(gold["valid_requires_null_defect_category"] is True, "valid category")
require("UNKNOWN" not in annotation_schema["properties"]["verdict"]["enum"], "annotation UNKNOWN")

out_of_scope_rules = [
    item for item in annotation_schema["allOf"]
    if item.get("if", {}).get("properties", {}).get("eligibility")
    == {"const": "OUT_OF_SCOPE"}
]
require(len(out_of_scope_rules) == 1, "out-of-scope schema rule")
require(
    out_of_scope_rules[0]["then"]["properties"]["verdict"]
    == {"const": None},
    "out-of-scope schema verdict",
)

verdict_phase_rules = [
    item for item in annotation_schema["allOf"]
    if item.get("if", {}).get("properties")
    == {"phase": {"const": "VERDICT"}}
]
require(len(verdict_phase_rules) == 1, "verdict-phase schema rule")
require(
    verdict_phase_rules[0]["then"]["properties"]["eligibility"]
    == {"enum": ["IN_SCOPE", "OUT_OF_SCOPE"]},
    "verdict-phase schema eligibility",
)
require(
    verdict_phase_rules[0]["then"]["properties"]["evidence_citation"]
    == {"type": "string", "minLength": 1},
    "verdict-phase schema evidence",
)

schemas = protocol["machine_readable_schemas"]
require(schemas["compilable_sampling_frame"]["sha256"] == digest(FRAME_SCHEMA), "frame schema")
require(schemas["blind_annotation_record"]["sha256"] == digest(ANNOTATION_SCHEMA), "annotation schema")
require(schemas["annotation_exposure_registry"]["sha256"] == digest(EXPOSURE_SCHEMA), "exposure schema")

authorization = protocol["authorization"]
require(authorization["primary_generation_authorized"] is False, "generation")
require(authorization["human_held_out_driver_inspection_allowed"] is False, "inspection")
require(authorization["analyzer_implementation_authorized_by_gate1b"] is False, "analyzer")
require(authorization["repair_implementation_allowed"] is False, "repair")

protocol_sha = digest(PROTOCOL)
report_sha = digest(REPORT)
require(report["status"] == "PASS", "report")
require(report["protocol_sha256"] == protocol_sha, "report protocol SHA")
require(report["sample_drawn"] is False, "sample drawn")
require(report["driver_content_inspected"] is False, "content inspected")
require(report["live_api_calls_performed"] == 0, "API calls")
require(report["role_roster_secured_claimed"] is False, "unsupported roster claim")
require(report["eligible_human_gold_unknown_allowed"] is False, "report gold UNKNOWN")
require(report["out_of_scope_receives_validity_verdict"] is False, "report out-of-scope verdict")
require(report["verdict_phase_requires_explicit_eligibility"] is True, "report verdict eligibility")

gate1 = lock["gate1_foundation"]
gate1b = gate1["gate1b_sampling_annotation_protocol"]
require(gate1["status"] == "IN_PROGRESS", "Gate 1 status")
require(gate1b["status"] == "PASS", "Gate 1B status")
require(gate1b["protocol_sha256"] == protocol_sha, "lock protocol SHA")
require(gate1b["report_sha256"] == report_sha, "lock report SHA")
require(gate1b["sampling_frame_schema_sha256"] == digest(FRAME_SCHEMA), "lock frame schema")
require(gate1b["annotation_schema_sha256"] == digest(ANNOTATION_SCHEMA), "lock annotation schema")
require(gate1b["exposure_schema_sha256"] == digest(EXPOSURE_SCHEMA), "lock exposure schema")
require(lock["current_status"]["gate_1"] == "IN_PROGRESS", "current Gate 1")
require(lock["current_status"]["gate_1b_sampling_annotation_protocol"] == "PASS", "current Gate 1B")
require(gate1["primary_generation_authorized"] is False, "lock generation")
require(gate1["held_out_driver_inspection_allowed"] is False, "lock inspection")
require(gate1["analyzer_implementation_authorized"] is False, "lock analyzer")
require(gate1["repair_implementation_allowed"] is False, "lock repair")

print("GATE1B_SAMPLING_ANNOTATION_PROTOCOL=PASS")
print("GOLD_SAMPLE_MAX_COMPILABLE_DRIVERS=140")
print("CENSUS_IF_COMPILABLE_AT_MOST_140=YES")
print("PRIMARY_STRATA=LIBRARY_X_MODEL")
print("MAX_PRIMARY_STRATA=16")
print("SAMPLING_SEED=2026080603")
print("ALL_ELIGIBLE_INCLUSION_PROBABILITY_POSITIVE=YES")
print("POST_HOC_SAMPLE_EXPANSION=NO")
print("PRIMARY_ANNOTATORS_REQUIRED=2")
print("THIRD_ADJUDICATOR_REQUIRED=YES")
print("DEVELOPER_LABEL_SUBSTITUTION=NO")
print("ELIGIBLE_HUMAN_GOLD_UNKNOWN_ALLOWED=NO")
print("OUT_OF_SCOPE_VALIDITY_VERDICT=NO")
print("VERDICT_PHASE_EXPLICIT_ELIGIBILITY=YES")
print("EXPOSURE_QUARANTINE=ENFORCED")
print("SAMPLE_DRAWN=NO")
print("LIVE_API_CALLS_PERFORMED=NO")
print("GENERATION_AUTHORIZED=NO")
print("HELD_OUT_DRIVER_INSPECTION_ALLOWED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"PROTOCOL_SHA256={protocol_sha}")
print(f"REPORT_SHA256={report_sha}")
