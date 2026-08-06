#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "config" / "research_lock.json"
ANALYSIS_REGISTRATION_PATH = ROOT / "config" / "statistical_analysis_registration.json"
ANALYSIS_REPORT_PATH = ROOT / "evidence" / "gates" / "gate0" / "statistical_power_curve.json"
ANALYSIS_VERIFIER_PATH = ROOT / "scripts" / "verify_gate0e_analysis.py"

def require(condition, message):
    if not condition:
        raise SystemExit(f"GATE0A_REPOSITORY_BOOTSTRAP=FAIL\nREASON={message}")

with LOCK_PATH.open("r", encoding="utf-8") as handle:
    lock = json.load(handle)

expected_title = (
    "SemanticVerify-Fuzz: Resource-Centered, Path-Sensitive "
    "Verification and Constrained Repair of API-Protocol "
    "Violations in LLM-Generated Fuzz Drivers"
)
require(lock["project"]["title"] == expected_title, "title mismatch")

contribution_ids = [item["id"] for item in lock["contributions"]]
rq_ids = [item["id"] for item in lock["research_questions"]]
require(contribution_ids == ["C1", "C2", "C3", "C4"], "C1-C4 lock mismatch")
require(rq_ids == ["RQ1", "RQ2", "RQ3", "RQ4", "RQ5"], "RQ1-RQ5 lock mismatch")

design = lock["experimental_design"]
calculated_total = (
    design["model_count"]
    * design["library_count"]
    * design["scenarios_per_library"]
    * design["attempts_per_scenario_per_model"]
)
require(calculated_total == 800, "2x8x10x5 arithmetic is not 800")
require(design["total_new_attempts"] == 800, "stored total is not 800")
require(len(design["models"]) == 2, "model count mismatch")
require(len(design["libraries"]) == 8, "library count mismatch")

roles = [item["role"] for item in design["libraries"]]
require(roles.count("development") == 1, "development role count must be 1")
require(roles.count("validation") == 1, "validation role count must be 1")
require(roles.count("held-out") == 6, "held-out role count must be 6")

require(
    [item["name"] for item in design["libraries"]] == [
        "zlib", "libpcap", "curl", "cJSON",
        "libtiff", "libvpx", "c-ares", "lcms"
    ],
    "library order or membership mismatch"
)
require(
    all(
        item["qualification_status"] == "PASS"
        for item in design["models"]
    ),
    "Gate 0D2 model qualification is not PASS"
)

stage = lock["stage_policy"]
require(stage["current_stage"] == "Stage A - verification", "wrong active stage")
require(stage["repair_implementation_allowed"] is False, "repair enabled too early")
require(stage["repair_activation_gate"] == "Gate V", "repair gate mismatch")
require(stage["no_backflow"] is True, "no-backflow rule missing")
require(stage["stage_a_outputs"] == ["RQ1", "RQ2", "RQ3", "RQ5"], "Stage A RQ mismatch")
require(stage["stage_b_outputs"] == ["RQ4"], "Stage B RQ mismatch")

fresh = lock["fresh_start"]
require(fresh["enabled"] is True, "fresh-start flag missing")
require(fresh["carry_over_prior_implementation"] is False, "old implementation enabled")
require(fresh["carry_over_prior_data"] is False, "old data enabled")
require(fresh["carry_over_prior_labels"] is False, "old labels enabled")
require(fresh["carry_over_prior_results"] is False, "old results enabled")

verdicts = lock["verdict_contract"]
require(
    verdicts["serialized_labels"] == [
        "VALID", "VIOLATION-MUST", "VIOLATION-MAY", "UNKNOWN"
    ],
    "verdict contract mismatch"
)
require(verdicts["unknown_is_valid"] is False, "UNKNOWN converted to VALID")

evaluation = lock["primary_evaluation"]
require(evaluation["minimum_precision_guard"] == 0.80, "precision guard mismatch")
require(
    evaluation["minimum_decision_coverage_guard"] == 0.75,
    "decision-coverage guard mismatch"
)
require(
    evaluation["raw_cfg_paths_are_independent_samples"] is False,
    "raw CFG paths incorrectly treated as independent samples"
)
require(evaluation["bootstrap_replicates"] == 2000, "bootstrap count")
require(evaluation["bootstrap_resampling_unit"] == "driver", "bootstrap unit")
require(evaluation["bootstrap_stratification"] == "library", "bootstrap strata")
require(evaluation["alpha_two_sided"] == 0.05, "alpha")
require(evaluation["planned_ablation_multiplicity"] == "Holm family-wise adjustment", "multiplicity")
require(evaluation["minimum_positive_obligations"] == 30, "positive obligations")
require(evaluation["minimum_positive_libraries"] == 5, "positive libraries")
require(evaluation["post_hoc_sample_expansion"] is False, "sample expansion")
require(evaluation["analysis_registration_status"] == "PASS", "analysis status")

repair = lock["repair_design"]
require(
    repair["implementation_status"] == "PROHIBITED_UNTIL_GATE_V",
    "repair status mismatch"
)
require(
    repair["confirmatory_minimum_eligible_natural_defects"] == 20,
    "repair minimum mismatch"
)
require(repair["stratified_cap"] == 40, "repair cap mismatch")
require(len(repair["acceptance_gates"]) == 5, "repair must have five gates")

current = lock["current_status"]

require(current["gate_0"] == "IN_PROGRESS", "Gate 0 closed too early")
require(
    current["gate_0d_model_qualification"] == "PASS",
    "Gate 0D qualification status mismatch"
)
require(
    current["gate_0d2_live_model_access"] == "PASS",
    "Gate 0D2 status mismatch"
)
require(
    current["gate_0e_statistical_analysis_registration"] == "PASS",
    "Gate 0E status mismatch"
)

model_qualification = lock["model_qualification"]

require(
    model_qualification["live_access_status"] == "PASS",
    "live model access is not PASS"
)
require(
    model_qualification["live_report_sha256"]
    == "f0b22b51684605677d4bfbfa4b187227c67093fc4c79792412797e28cb30f5c4",
    "live report SHA mismatch"
)
require(
    model_qualification["generation_authorized"] is False,
    "generation authorized before Gate 0 closes"
)

analysis = lock["analysis_registration"]
require(analysis["status"] == "PASS", "analysis lock status")
require(analysis["active_registration_sha256"] == hashlib.sha256(ANALYSIS_REGISTRATION_PATH.read_bytes()).hexdigest(), "active registration SHA")
require(analysis["power_report_sha256"] == hashlib.sha256(ANALYSIS_REPORT_PATH.read_bytes()).hexdigest(), "power report SHA")
require(analysis["verification_script_sha256"] == hashlib.sha256(ANALYSIS_VERIFIER_PATH.read_bytes()).hexdigest(), "analysis verifier SHA")
require(analysis["scenario_count"] == 144, "power scenario count")
require(analysis["bootstrap_replicates"] == 2000, "analysis bootstrap count")
require(analysis["post_hoc_sample_expansion"] is False, "analysis sample expansion")
require(analysis["generation_authorized"] is False, "analysis generation")
require(analysis["repair_implementation_allowed"] is False, "analysis repair")

generation_protocol = lock["generation_protocol"]
generation_protocol_path = ROOT / generation_protocol["path"]

require(
    generation_protocol["status"] == "PASS",
    "Gate 0F generation protocol is not PASS"
)
require(
    generation_protocol_path.is_file(),
    "Gate 0F generation protocol file missing"
)

generation_protocol_sha256 = hashlib.sha256(
    generation_protocol_path.read_bytes()
).hexdigest()

require(
    generation_protocol_sha256 == generation_protocol["sha256"],
    "Gate 0F generation protocol SHA mismatch"
)

generation_protocol_document = json.loads(
    generation_protocol_path.read_text(encoding="utf-8")
)

require(
    generation_protocol_document["status"] == "PASS_FROZEN",
    "Gate 0F protocol is not frozen"
)
require(
    generation_protocol_document["logical_attempt_design"]
    ["logical_slot_count"] == 800,
    "Gate 0F logical attempt count mismatch"
)
require(
    generation_protocol_document["execution_window"]["state"]
    == "FROZEN_NOT_OPEN",
    "generation window opened before authorization"
)
require(
    generation_protocol_document["authorization"]
    ["primary_generation_authorized"] is False,
    "primary generation enabled before Gate 0 closes"
)
require(
    generation_protocol_document["authorization"]
    ["repair_implementation_allowed"] is False,
    "repair enabled before Gate V"
)
require(
    current["gate_0f_generation_protocol"] == "PASS",
    "Gate 0F current status mismatch"
)

digest = hashlib.sha256(LOCK_PATH.read_bytes()).hexdigest()

print("GATE0A_REPOSITORY_BOOTSTRAP=PASS")
print("GATE0_OVERALL=IN_PROGRESS")
print("CURRENT_STAGE=STAGE_A_VERIFICATION")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print("CONTRIBUTIONS=4")
print("RESEARCH_QUESTIONS=5")
print("LIBRARIES=8")
print("NEW_GENERATION_ATTEMPTS=800")
print("MODEL_QUALIFICATION=PASS")
print("ANALYSIS_REGISTRATION=PASS")
print("GENERATION_PROTOCOL=PASS")
print(f"RESEARCH_LOCK_SHA256={digest}")
