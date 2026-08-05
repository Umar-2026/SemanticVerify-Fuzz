#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "config" / "research_lock.json"

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
    all(item["qualification_status"] == "PENDING" for item in design["models"]),
    "Gate 0A must not claim unperformed model qualification"
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

digest = hashlib.sha256(LOCK_PATH.read_bytes()).hexdigest()

print("GATE0A_REPOSITORY_BOOTSTRAP=PASS")
print("GATE0_OVERALL=IN_PROGRESS")
print("CURRENT_STAGE=STAGE_A_VERIFICATION")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print("CONTRIBUTIONS=4")
print("RESEARCH_QUESTIONS=5")
print("LIBRARIES=8")
print("NEW_GENERATION_ATTEMPTS=800")
print("MODEL_QUALIFICATION=PENDING")
print(f"RESEARCH_LOCK_SHA256={digest}")
