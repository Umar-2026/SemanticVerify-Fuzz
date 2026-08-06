#!/usr/bin/env python3

import copy
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HEAD = "382745b676cc45a4d81f087626086a22caec9d05"
EXPECTED_DRAFT_SHA256 = (
    "8a26244a7be384ce58d1a11f73650549"
    "98fd92d4c5b496e07d7b3dfa3d2a7144"
)
EXPECTED_REPORT_SHA256 = (
    "bb746da67ccdae2eeda232aba36c53ba"
    "53ec3d7830fdd726bb4f450aa2ab9b58"
)
EXPECTED_RUNNER_SHA256 = (
    "15dd19839d8bea03a7e5e9a755ea4fa8"
    "62b937f399a0f1d43548f886be8555b1"
)

REGISTRATION = ROOT / "config" / "statistical_analysis_registration.json"
SNAPSHOT = (
    ROOT
    / "evidence"
    / "gates"
    / "gate0"
    / "statistical_analysis_registration_pre_simulation.json"
)
REPORT = ROOT / "evidence" / "gates" / "gate0" / "statistical_power_curve.json"
RUNNER = ROOT / "scripts" / "run_gate0e_power_simulation.py"
VERIFIER = ROOT / "scripts" / "verify_gate0e_analysis.py"
PREPARER = ROOT / "scripts" / "prepare_gate0e_analysis_freeze.py"
DECISION = (
    ROOT
    / "documentation"
    / "decisions"
    / "0004-statistical-analysis-registration-freeze.md"
)
LOCK = ROOT / "config" / "research_lock.json"
CURRENT_STATUS = ROOT / "documentation" / "CURRENT_STATUS.md"
GATE0_README = ROOT / "evidence" / "gates" / "gate0" / "README.md"
GATE0_VERIFIER = ROOT / "scripts" / "verify_gate0.py"


def require(condition, reason):
    if not condition:
        print("GATE0E_FREEZE_PREPARATION=FAIL")
        print(f"REASON={reason}")
        raise SystemExit(1)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_path(path):
    return sha256_bytes(path.read_bytes())


def json_bytes(value):
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def replace_once(text, old, new, label):
    require(text.count(old) == 1, f"{label}: expected one replacement anchor")
    return text.replace(old, new, 1)


def run(command):
    print("RUN=" + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


require(PREPARER.is_file(), "preparation script is not in repository scripts")
require(
    subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    == EXPECTED_HEAD,
    "unexpected Git HEAD",
)

expected_status = sorted(
    [
        "?? config/statistical_analysis_registration.json",
        "?? evidence/gates/gate0/statistical_power_curve.json",
        "?? scripts/prepare_gate0e_analysis_freeze.py",
        "?? scripts/run_gate0e_power_simulation.py",
    ]
)
actual_status = sorted(
    subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    ).splitlines()
)
require(actual_status == expected_status, "unexpected repository paths")

for secret_name in ["DEEPSEEK_API_KEY", "GEMINI_API_KEY"]:
    require(not os.environ.get(secret_name), f"{secret_name} still present")

require(sha256_path(REGISTRATION) == EXPECTED_DRAFT_SHA256, "draft hash")
require(sha256_path(REPORT) == EXPECTED_REPORT_SHA256, "report hash")
require(sha256_path(RUNNER) == EXPECTED_RUNNER_SHA256, "runner hash")
require(not SNAPSHOT.exists(), "snapshot already exists")
require(not VERIFIER.exists(), "verifier already exists")
require(not DECISION.exists(), "decision already exists")

draft_bytes = REGISTRATION.read_bytes()
draft = json.loads(draft_bytes)
report = json.loads(REPORT.read_text(encoding="utf-8"))
require(draft["status"] == "DRAFT_POWER_EVIDENCE_PENDING", "draft status")
require(report["status"] == "PASS", "report status")
require(report["registration"]["sha256"] == EXPECTED_DRAFT_SHA256, "report registration link")
require(report["script_sha256"] == EXPECTED_RUNNER_SHA256, "report runner link")
require(report["summary"]["scenario_count"] == 144, "scenario count")
require(report["summary"]["conditional_mdi_reached_scenarios"] == 61, "conditional count")
require(report["summary"]["claimable_mdi_reached_scenarios"] == 61, "claimable count")
require(report["generation_authorized"] is False, "report generation")
require(report["repair_implementation_allowed"] is False, "report repair")

central = report["summary"]["central_scenarios"]
central_12 = central["12"]["claimable_mdi_at_80_percent_power"]
require(central["4"]["claimable_mdi_at_80_percent_power"] is None, "central 4")
require(central["8"]["claimable_mdi_at_80_percent_power"] is None, "central 8")
require(central_12["positive_sensitivity_gain"] == 0.1, "central gain")
require(central_12["median_macro_f1_difference"] == 0.069727, "central F1")
require(central_12["claimable_power"] == 0.8865, "central power")

active = copy.deepcopy(draft)
active["status"] = "PASS_FROZEN"
active["freeze"] = {
    "frozen_before_primary_generation": True,
    "pre_simulation_snapshot": (
        "evidence/gates/gate0/"
        "statistical_analysis_registration_pre_simulation.json"
    ),
    "pre_simulation_snapshot_sha256": EXPECTED_DRAFT_SHA256,
    "power_report": "evidence/gates/gate0/statistical_power_curve.json",
    "power_report_sha256": EXPECTED_REPORT_SHA256,
    "simulation_script": "scripts/run_gate0e_power_simulation.py",
    "simulation_script_sha256": EXPECTED_RUNNER_SHA256,
    "scenario_count": 144,
    "conditional_mdi_reached_scenarios": 61,
    "claimable_mdi_reached_scenarios": 61,
    "central_scenario": {
        "prevalence": 0.10,
        "combined_driver_library_icc": 0.05,
        "positive_conditional_detector_discordance": 0.10,
        "four_obligations_mdi_reached": False,
        "eight_obligations_mdi_reached": False,
        "twelve_obligations_positive_sensitivity_gain": 0.10,
        "twelve_obligations_median_macro_f1_difference": 0.069727,
        "twelve_obligations_claimable_power": 0.8865,
    },
    "non_reached_scenarios_trigger_sample_expansion": False,
    "generation_authorized": False,
    "repair_implementation_allowed": False,
}
active_bytes = json_bytes(active)
active_sha256 = sha256_bytes(active_bytes)

verifier_template = r'''#!/usr/bin/env python3

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

EXPECTED_ACTIVE_SHA256 = "__ACTIVE_SHA256__"
EXPECTED_SNAPSHOT_SHA256 = "__SNAPSHOT_SHA256__"
EXPECTED_REPORT_SHA256 = "__REPORT_SHA256__"
EXPECTED_RUNNER_SHA256 = "__RUNNER_SHA256__"


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
'''
verifier_source = (
    verifier_template
    .replace("__ACTIVE_SHA256__", active_sha256)
    .replace("__SNAPSHOT_SHA256__", EXPECTED_DRAFT_SHA256)
    .replace("__REPORT_SHA256__", EXPECTED_REPORT_SHA256)
    .replace("__RUNNER_SHA256__", EXPECTED_RUNNER_SHA256)
)
compile(verifier_source, str(VERIFIER), "exec")
verifier_bytes = verifier_source.encode("utf-8")
verifier_sha256 = sha256_bytes(verifier_bytes)

lock = json.loads(LOCK.read_text(encoding="utf-8"))
evaluation = lock["primary_evaluation"]
evaluation.update(
    {
        "bootstrap_replicates": 2000,
        "bootstrap_resampling_unit": "driver",
        "bootstrap_stratification": "library",
        "confidence_interval": "two-sided percentile 95%",
        "alpha_two_sided": 0.05,
        "planned_ablation_multiplicity": "Holm family-wise adjustment",
        "minimum_positive_obligations": 30,
        "minimum_positive_libraries": 5,
        "category_descriptive_threshold": 10,
        "post_hoc_sample_expansion": False,
        "analysis_registration_status": "PASS",
    }
)
lock["current_status"]["gate_0e_statistical_analysis_registration"] = "PASS"
lock["current_status"]["milestone"] = (
    "Gate 0E statistical analysis and power registration complete; "
    "generation-window protocol and final Gate 0 manifest pending"
)
lock["analysis_registration"] = {
    "status": "PASS",
    "frozen_before_primary_generation": True,
    "active_registration": "config/statistical_analysis_registration.json",
    "active_registration_sha256": active_sha256,
    "pre_simulation_snapshot": (
        "evidence/gates/gate0/"
        "statistical_analysis_registration_pre_simulation.json"
    ),
    "pre_simulation_snapshot_sha256": EXPECTED_DRAFT_SHA256,
    "power_report": "evidence/gates/gate0/statistical_power_curve.json",
    "power_report_sha256": EXPECTED_REPORT_SHA256,
    "simulation_script": "scripts/run_gate0e_power_simulation.py",
    "simulation_script_sha256": EXPECTED_RUNNER_SHA256,
    "verification_script": "scripts/verify_gate0e_analysis.py",
    "verification_script_sha256": verifier_sha256,
    "preparation_script": "scripts/prepare_gate0e_analysis_freeze.py",
    "preparation_script_sha256": sha256_path(PREPARER),
    "scenario_count": 144,
    "conditional_mdi_reached_scenarios": 61,
    "claimable_mdi_reached_scenarios": 61,
    "bootstrap_replicates": 2000,
    "minimum_precision_guard": 0.80,
    "minimum_decision_coverage_guard": 0.75,
    "post_hoc_sample_expansion": False,
    "generation_authorized": False,
    "repair_implementation_allowed": False,
}
lock_bytes = json_bytes(lock)

status_text = CURRENT_STATUS.read_text(encoding="utf-8")
status_text = replace_once(
    status_text,
    "- Current milestone: Gate 0D2 — live model qualification complete",
    "- Current milestone: Gate 0E — statistical analysis and power registration complete",
    "current milestone",
)
status_text = replace_once(
    status_text,
    "- Gate 0D2 live endpoint/capability qualification: PASS\n- Gate 1: NOT STARTED",
    "- Gate 0D2 live endpoint/capability qualification: PASS\n"
    "- Gate 0E statistical analysis and power registration: PASS\n"
    "- Gate 1: NOT STARTED",
    "Gate 0E status",
)
status_text = replace_once(
    status_text,
    "## Credential handling",
    "## Frozen statistical analysis\n\n"
    "- Primary endpoint: held-out library-macro obligation-level F1.\n"
    "- Primary paired comparison: full versus path-insensitive verifier.\n"
    "- UNKNOWN is scored incorrect; raw CFG paths are not independent samples.\n"
    "- Driver-cluster bootstrap within library strata: 2,000 replicates.\n"
    "- Precision guard: 0.80; decision-coverage guard: 0.75.\n"
    "- Power grid: 144 scenarios; 61 reached conditional and claimable 80% MDI.\n"
    "- Sparse settings do not trigger post-hoc expansion; claims are withheld.\n"
    "- Power report SHA-256:\n"
    f"  `{EXPECTED_REPORT_SHA256}`\n\n"
    "## Credential handling",
    "statistical section",
)
status_text = replace_once(
    status_text,
    "1. Freeze the statistical power and analysis registration.\n"
    "2. Freeze the exact generation-window and retry protocol.\n"
    "3. Create and verify the final Gate 0 manifest.",
    "1. Freeze the exact generation-window and retry protocol.\n"
    "2. Create and verify the final Gate 0 manifest.",
    "remaining list",
)

readme_text = GATE0_README.read_text(encoding="utf-8")
readme_text = replace_once(
    readme_text,
    "- Gate 0D2 live endpoint and capability qualification",
    "- Gate 0D2 live endpoint and capability qualification\n"
    "- Gate 0E statistical analysis and power registration",
    "README completion",
)
readme_text = replace_once(
    readme_text,
    "Gate 0 remains IN PROGRESS. Statistical registration, generation-window\n"
    "protocol, and the final Gate 0 manifest remain pending.",
    "Gate 0E evidence:\n\n"
    "- `statistical_analysis_registration_pre_simulation.json`: immutable design snapshot\n"
    "- `statistical_power_curve.json`: deterministic 144-scenario power evidence\n\n"
    "Gate 0 remains IN PROGRESS. The generation-window protocol and the final\n"
    "Gate 0 manifest remain pending.",
    "README pending text",
)

gate0_source = GATE0_VERIFIER.read_text(encoding="utf-8")
gate0_source = replace_once(
    gate0_source,
    'LOCK_PATH = ROOT / "config" / "research_lock.json"',
    'LOCK_PATH = ROOT / "config" / "research_lock.json"\n'
    'ANALYSIS_REGISTRATION_PATH = ROOT / "config" / "statistical_analysis_registration.json"\n'
    'ANALYSIS_REPORT_PATH = ROOT / "evidence" / "gates" / "gate0" / "statistical_power_curve.json"\n'
    'ANALYSIS_VERIFIER_PATH = ROOT / "scripts" / "verify_gate0e_analysis.py"',
    "Gate0 paths",
)
gate0_source = replace_once(
    gate0_source,
    'require(\n    evaluation["raw_cfg_paths_are_independent_samples"] is False,\n'
    '    "raw CFG paths incorrectly treated as independent samples"\n)',
    'require(\n    evaluation["raw_cfg_paths_are_independent_samples"] is False,\n'
    '    "raw CFG paths incorrectly treated as independent samples"\n)\n'
    'require(evaluation["bootstrap_replicates"] == 2000, "bootstrap count")\n'
    'require(evaluation["bootstrap_resampling_unit"] == "driver", "bootstrap unit")\n'
    'require(evaluation["bootstrap_stratification"] == "library", "bootstrap strata")\n'
    'require(evaluation["alpha_two_sided"] == 0.05, "alpha")\n'
    'require(evaluation["planned_ablation_multiplicity"] == "Holm family-wise adjustment", "multiplicity")\n'
    'require(evaluation["minimum_positive_obligations"] == 30, "positive obligations")\n'
    'require(evaluation["minimum_positive_libraries"] == 5, "positive libraries")\n'
    'require(evaluation["post_hoc_sample_expansion"] is False, "sample expansion")\n'
    'require(evaluation["analysis_registration_status"] == "PASS", "analysis status")',
    "Gate0 evaluation",
)
gate0_source = replace_once(
    gate0_source,
    'require(\n    current["gate_0d2_live_model_access"] == "PASS",\n'
    '    "Gate 0D2 status mismatch"\n)',
    'require(\n    current["gate_0d2_live_model_access"] == "PASS",\n'
    '    "Gate 0D2 status mismatch"\n)\n'
    'require(\n    current["gate_0e_statistical_analysis_registration"] == "PASS",\n'
    '    "Gate 0E status mismatch"\n)',
    "Gate0 current status",
)
gate0_source = replace_once(
    gate0_source,
    'require(\n    model_qualification["generation_authorized"] is False,\n'
    '    "generation authorized before Gate 0 closes"\n)',
    'require(\n    model_qualification["generation_authorized"] is False,\n'
    '    "generation authorized before Gate 0 closes"\n)\n\n'
    'analysis = lock["analysis_registration"]\n'
    'require(analysis["status"] == "PASS", "analysis lock status")\n'
    'require(analysis["active_registration_sha256"] == hashlib.sha256(ANALYSIS_REGISTRATION_PATH.read_bytes()).hexdigest(), "active registration SHA")\n'
    'require(analysis["power_report_sha256"] == hashlib.sha256(ANALYSIS_REPORT_PATH.read_bytes()).hexdigest(), "power report SHA")\n'
    'require(analysis["verification_script_sha256"] == hashlib.sha256(ANALYSIS_VERIFIER_PATH.read_bytes()).hexdigest(), "analysis verifier SHA")\n'
    'require(analysis["scenario_count"] == 144, "power scenario count")\n'
    'require(analysis["bootstrap_replicates"] == 2000, "analysis bootstrap count")\n'
    'require(analysis["post_hoc_sample_expansion"] is False, "analysis sample expansion")\n'
    'require(analysis["generation_authorized"] is False, "analysis generation")\n'
    'require(analysis["repair_implementation_allowed"] is False, "analysis repair")',
    "Gate0 analysis lock",
)
gate0_source = replace_once(
    gate0_source,
    'print("MODEL_QUALIFICATION=PASS")\nprint(f"RESEARCH_LOCK_SHA256={digest}")',
    'print("MODEL_QUALIFICATION=PASS")\n'
    'print("ANALYSIS_REGISTRATION=PASS")\n'
    'print(f"RESEARCH_LOCK_SHA256={digest}")',
    "Gate0 output",
)
compile(gate0_source, str(GATE0_VERIFIER), "exec")

decision_text = f'''# Decision 0004: Statistical Analysis Registration Freeze

- Status: Accepted
- Date: 2026-08-06
- Stage: Gate 0E

## Frozen confirmatory analysis

- Primary endpoint: held-out library-macro obligation-level F1.
- Positive class: VIOLATION, pooling MUST and MAY for the primary endpoint.
- UNKNOWN is forced to the wrong binary label and cannot improve F1.
- Primary comparison: full verifier minus path-insensitive verifier.
- Resampling: 2,000 driver-cluster bootstrap replicates within library strata.
- Inference: two-sided alpha 0.05, percentile 95% confidence interval, effect sizes.
- Planned ablations use Holm family-wise multiplicity adjustment.
- Precision must be at least 0.80 and decision coverage at least 0.75.

## Frozen sparse-outcome rules

- Fewer than 30 positive obligations or five positive libraries withholds
  confirmatory sensitivity and superiority claims.
- Categories with fewer than 10 positives receive counts and exact intervals only.
- No post-hoc sample expansion and no generation to obtain desired defects.

## Frozen power evidence

- 144 scenarios cover prevalence 5-20%, combined ICC 0.01-0.10, detector
  discordance 5-20%, and 4/8/12 eligible obligations per driver.
- 61 scenarios reached both conditional and claimable 80% MDI.
- In the central 12-obligation scenario, a 0.10 positive-sensitivity gain produced
  median macro-F1 difference 0.069727 and claimable power 0.8865.
- Non-reached scenarios are informative and narrow claims; they do not change the
  fixed generation or annotation budgets.

## Provenance

- Pre-simulation registration SHA-256: `{EXPECTED_DRAFT_SHA256}`
- Active frozen registration SHA-256: `{active_sha256}`
- Power report SHA-256: `{EXPECTED_REPORT_SHA256}`
- Simulation script SHA-256: `{EXPECTED_RUNNER_SHA256}`
- Read-only verifier SHA-256: `{verifier_sha256}`
- Freeze-preparation script SHA-256: `{sha256_path(PREPARER)}`

Primary generation remains unauthorized. Driver inspection remains unauthorized.
Repair implementation remains prohibited until Gate V.
'''

compile(verifier_source, str(VERIFIER), "exec")
json.loads(active_bytes)
json.loads(lock_bytes)

with SNAPSHOT.open("xb") as handle:
    handle.write(draft_bytes)
with VERIFIER.open("x", encoding="utf-8") as handle:
    handle.write(verifier_source)
VERIFIER.chmod(VERIFIER.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
with DECISION.open("x", encoding="utf-8") as handle:
    handle.write(decision_text)

REGISTRATION.write_bytes(active_bytes)
LOCK.write_bytes(lock_bytes)
CURRENT_STATUS.write_text(status_text, encoding="utf-8")
GATE0_README.write_text(readme_text, encoding="utf-8")
GATE0_VERIFIER.write_text(gate0_source, encoding="utf-8")

run(["python3", "scripts/scan_repository_secrets.py"])
run(["python3", "scripts/verify_gate0c_proposal.py"])
run(["python3", "scripts/verify_gate0d_documentation.py"])
run(["python3", "scripts/verify_gate0d_live.py"])
run(["python3", "scripts/verify_gate0e_analysis.py"])
run(["python3", "scripts/verify_gate0.py"])
run(["git", "diff", "--check"])

print("GATE0E_FREEZE_PREPARATION=PASS")
print(f"ACTIVE_REGISTRATION_SHA256={active_sha256}")
print(f"SNAPSHOT_SHA256={EXPECTED_DRAFT_SHA256}")
print(f"POWER_REPORT_SHA256={EXPECTED_REPORT_SHA256}")
print(f"SIMULATION_SCRIPT_SHA256={EXPECTED_RUNNER_SHA256}")
print(f"VERIFICATION_SCRIPT_SHA256={verifier_sha256}")
print("GATE0_OVERALL=IN_PROGRESS")
print("GENERATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print("STATUS=")
subprocess.run(["git", "status", "--short", "--branch"], cwd=ROOT, check=True)
