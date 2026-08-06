#!/usr/bin/env python3

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "config" / "statistical_analysis_registration.json"
SNAPSHOT = ROOT / "evidence" / "gates" / "gate0" / "statistical_analysis_registration_pre_simulation.json"
REPORT = ROOT / "evidence" / "gates" / "gate0" / "statistical_power_curve.json"
RUNNER = ROOT / "scripts" / "run_gate0e_power_simulation.py"
LOCK = ROOT / "config" / "research_lock.json"

EXPECTED_ACTIVE_SHA256 = "c7537ce5d082de904cc7aef4d617c9ff6612b30fdb4740b0667c9eb84ca5b2d4"
EXPECTED_SNAPSHOT_SHA256 = "8a26244a7be384ce58d1a11f7365054998fd92d4c5b496e07d7b3dfa3d2a7144"
EXPECTED_REPORT_SHA256 = "bb746da67ccdae2eeda232aba36c53ba53ec3d7830fdd726bb4f450aa2ab9b58"
EXPECTED_RUNNER_SHA256 = "15dd19839d8bea03a7e5e9a755ea4fa862b937f399a0f1d43548f886be8555b1"


def require(condition, reason):
    if not condition:
        print("GATE0E_ANALYSIS_FREEZE=FAIL")
        print(f"REASON={reason}")
        raise SystemExit(1)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


require(digest(ACTIVE) == EXPECTED_ACTIVE_SHA256, "active registration hash")
require(digest(SNAPSHOT) == EXPECTED_SNAPSHOT_SHA256, "snapshot hash")
require(digest(REPORT) == EXPECTED_REPORT_SHA256, "power report hash")
require(digest(RUNNER) == EXPECTED_RUNNER_SHA256, "simulation script hash")

active = json.loads(ACTIVE.read_text(encoding="utf-8"))
snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
report = json.loads(REPORT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))

require(active["status"] == "PASS_FROZEN", "active status")
require(snapshot["status"] == "DRAFT_POWER_EVIDENCE_PENDING", "snapshot status")
normalized = copy.deepcopy(active)
normalized.pop("freeze")
normalized["status"] = "DRAFT_POWER_EVIDENCE_PENDING"
require(normalized == snapshot, "active registration differs from frozen design")

freeze = active["freeze"]
require(freeze["pre_simulation_snapshot_sha256"] == EXPECTED_SNAPSHOT_SHA256, "snapshot link")
require(freeze["power_report_sha256"] == EXPECTED_REPORT_SHA256, "report link")
require(freeze["simulation_script_sha256"] == EXPECTED_RUNNER_SHA256, "runner link")
require(freeze["scenario_count"] == 144, "freeze scenario count")
require(freeze["conditional_mdi_reached_scenarios"] == 61, "freeze conditional count")
require(freeze["claimable_mdi_reached_scenarios"] == 61, "freeze claimable count")
require(freeze["non_reached_scenarios_trigger_sample_expansion"] is False, "sample expansion")
require(freeze["generation_authorized"] is False, "freeze generation")
require(freeze["repair_implementation_allowed"] is False, "freeze repair")

require(report["status"] == "PASS", "report status")
require(report["registration"]["sha256"] == EXPECTED_SNAPSHOT_SHA256, "report snapshot")
require(report["script_sha256"] == EXPECTED_RUNNER_SHA256, "report runner")
require(report["summary"]["scenario_count"] == 144, "report scenario count")
require(report["summary"]["conditional_mdi_reached_scenarios"] == 61, "report conditional count")
require(report["summary"]["claimable_mdi_reached_scenarios"] == 61, "report claimable count")
require(report["generation_authorized"] is False, "report generation")
require(report["repair_implementation_allowed"] is False, "report repair")

power = snapshot["power_simulation"]
expected_grid = {
    (obligations, prevalence, icc, discordance)
    for obligations in power["eligible_obligations_per_driver_sensitivity_grid"]
    for prevalence in power["prevalence_grid"]
    for icc in power["combined_driver_library_icc_grid"]
    for discordance in power["positive_conditional_detector_discordance_grid"]
}
actual_grid = {
    (
        row["eligible_obligations_per_driver"],
        row["prevalence"],
        row["combined_driver_library_icc"],
        row["positive_conditional_detector_discordance"],
    )
    for row in report["scenarios"]
}
require(len(report["scenarios"]) == 144, "scenario rows")
require(actual_grid == expected_grid, "scenario grid")

conditional_count = sum(
    row["conditional_mdi_at_80_percent_power"] is not None
    for row in report["scenarios"]
)
claimable_count = sum(
    row["claimable_mdi_at_80_percent_power"] is not None
    for row in report["scenarios"]
)
require(conditional_count == 61, "derived conditional count")
require(claimable_count == 61, "derived claimable count")

analysis = lock["analysis_registration"]
require(analysis["status"] == "PASS", "research-lock analysis status")
require(analysis["active_registration_sha256"] == EXPECTED_ACTIVE_SHA256, "lock active hash")
require(analysis["pre_simulation_snapshot_sha256"] == EXPECTED_SNAPSHOT_SHA256, "lock snapshot hash")
require(analysis["power_report_sha256"] == EXPECTED_REPORT_SHA256, "lock report hash")
require(analysis["simulation_script_sha256"] == EXPECTED_RUNNER_SHA256, "lock runner hash")
require(analysis["verification_script_sha256"] == digest(Path(__file__)), "lock verifier hash")
require(analysis["generation_authorized"] is False, "lock generation")
require(analysis["repair_implementation_allowed"] is False, "lock repair")
require(lock["current_status"]["gate_0e_statistical_analysis_registration"] == "PASS", "Gate 0E status")
require(lock["current_status"]["gate_0"] == "IN_PROGRESS", "Gate 0 closed early")

print("GATE0E_ANALYSIS_FREEZE=PASS")
print("PRIMARY_ENDPOINT=HELD_OUT_LIBRARY_MACRO_OBLIGATION_F1")
print("BOOTSTRAP_REPLICATES=2000")
print("POWER_SCENARIOS=144")
print("CONDITIONAL_MDI_REACHED_SCENARIOS=61")
print("CLAIMABLE_MDI_REACHED_SCENARIOS=61")
print("POST_HOC_SAMPLE_EXPANSION=NO")
print("GENERATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"ACTIVE_REGISTRATION_SHA256={EXPECTED_ACTIVE_SHA256}")
print(f"POWER_REPORT_SHA256={EXPECTED_REPORT_SHA256}")
