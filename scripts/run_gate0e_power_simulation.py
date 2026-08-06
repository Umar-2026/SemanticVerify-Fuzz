#!/usr/bin/env python3

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REGISTRATION = ROOT / "config" / "statistical_analysis_registration.json"
REPORT = ROOT / "evidence" / "gates" / "gate0" / "statistical_power_curve.json"
EXPECTED_HEAD = "382745b676cc45a4d81f087626086a22caec9d05"
EXPECTED_REGISTRATION_SHA256 = (
    "8a26244a7be384ce58d1a11f73650549"
    "98fd92d4c5b496e07d7b3dfa3d2a7144"
)


def require(condition, reason):
    if not condition:
        print("GATE0E_POWER_SIMULATION=FAIL")
        print(f"REASON={reason}")
        raise SystemExit(1)


def rounded(value):
    return round(float(value), 6)


def scenario_seed(master_seed, *parts):
    material = "|".join(str(part) for part in (master_seed, *parts))
    digest = hashlib.sha256(material.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def beta_parameters(mean, rho):
    concentration = (1.0 / rho) - 1.0
    clipped = np.clip(mean, 1e-6, 1.0 - 1e-6)
    return clipped * concentration, (1.0 - clipped) * concentration


def generate_gold(
    simulations,
    libraries,
    drivers_per_library,
    obligations_per_driver,
    prevalence,
    icc,
    library_fraction,
    driver_fraction,
    baseline_sensitivity,
    precision_value,
    seed,
):
    rng = np.random.default_rng(seed)
    rho_library = icc * library_fraction
    rho_driver = icc * driver_fraction

    alpha_l, beta_l = beta_parameters(prevalence, rho_library)
    library_prevalence = rng.beta(
        alpha_l,
        beta_l,
        size=(simulations, libraries),
    )

    alpha_d, beta_d = beta_parameters(
        library_prevalence[..., None],
        rho_driver,
    )
    driver_prevalence = rng.beta(
        alpha_d,
        beta_d,
        size=(simulations, libraries, drivers_per_library),
    )

    positives = rng.binomial(
        obligations_per_driver,
        driver_prevalence,
    )
    negatives = obligations_per_driver - positives
    false_positive_rate = (
        prevalence
        * baseline_sensitivity
        * (1.0 - precision_value)
        / (precision_value * (1.0 - prevalence))
    )
    shared_false_positives = rng.binomial(
        negatives,
        false_positive_rate,
    )
    return positives, shared_false_positives, false_positive_rate


def simulate_delta(
    positives,
    shared_false_positives,
    baseline_sensitivity,
    discordance,
    gain,
    minimum_positive_obligations,
    minimum_positive_libraries,
    seed,
):
    rng = np.random.default_rng(seed)
    full_only_probability = (discordance + gain) / 2.0
    baseline_only_probability = (discordance - gain) / 2.0
    both_correct_probability = (
        baseline_sensitivity - baseline_only_probability
    )

    full_only = rng.binomial(positives, full_only_probability)
    remaining = positives - full_only
    baseline_only = rng.binomial(
        remaining,
        baseline_only_probability / (1.0 - full_only_probability),
    )
    remaining -= baseline_only
    both_correct = rng.binomial(
        remaining,
        both_correct_probability / (1.0 - discordance),
    )

    tp_baseline = (both_correct + baseline_only).sum(axis=2)
    tp_full = (both_correct + full_only).sum(axis=2)
    total_positive = positives.sum(axis=2)
    false_positive = shared_false_positives.sum(axis=2)
    fn_baseline = total_positive - tp_baseline
    fn_full = total_positive - tp_full

    baseline_denominator = (
        2 * tp_baseline + false_positive + fn_baseline
    )
    full_denominator = 2 * tp_full + false_positive + fn_full
    baseline_f1 = np.divide(
        2 * tp_baseline,
        baseline_denominator,
        out=np.zeros_like(tp_baseline, dtype=float),
        where=baseline_denominator != 0,
    )
    full_f1 = np.divide(
        2 * tp_full,
        full_denominator,
        out=np.zeros_like(tp_full, dtype=float),
        where=full_denominator != 0,
    )

    macro_difference = (full_f1 - baseline_f1).mean(axis=1)
    positive_library_count = (total_positive > 0).sum(axis=1)
    eligible = (
        (total_positive.sum(axis=1) >= minimum_positive_obligations)
        & (positive_library_count >= minimum_positive_libraries)
    )
    return macro_difference, eligible


def first_mdi(effect_curve, power_field, target_power):
    return next(
        (
            row
            for row in effect_curve
            if row[power_field] is not None
            and row[power_field] >= target_power
        ),
        None,
    )


require(not REPORT.exists(), "power report already exists")
require(
    hashlib.sha256(REGISTRATION.read_bytes()).hexdigest()
    == EXPECTED_REGISTRATION_SHA256,
    "registration SHA-256 mismatch",
)

head = subprocess.check_output(
    ["git", "rev-parse", "HEAD"],
    cwd=ROOT,
    text=True,
).strip()
require(head == EXPECTED_HEAD, "unexpected Git HEAD")

status_lines = sorted(
    subprocess.check_output(
        [
            "git",
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()
)
expected_status_lines = sorted(
    [
        "?? config/statistical_analysis_registration.json",
        "?? scripts/run_gate0e_power_simulation.py",
    ]
)
require(
    status_lines == expected_status_lines,
    "unexpected repository paths before simulation",
)

registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
power = registration["power_simulation"]
primary = registration["primary_analysis"]
runtime = power["runtime_lock"]
require(sys.version.split()[0] == runtime["python"], "Python drift")
require(np.__version__ == runtime["numpy"], "NumPy drift")
require(registration["status"] == "DRAFT_POWER_EVIDENCE_PENDING", "status")
require(registration["authorization"]["primary_generation_authorized"] is False, "generation")
require(registration["authorization"]["repair_implementation_allowed"] is False, "repair")

simulations = power["simulation_replicates_per_scenario"]
libraries = power["held_out_library_count"]
drivers_per_library = power["planning_drivers_per_held_out_library"]
baseline_sensitivity = power["baseline_effective_sensitivity"]
precision_value = power["baseline_population_precision_planning_value"]
master_seed = power["master_seed"]
target_power = power["target_power"]
alpha = primary["significance"]["alpha_two_sided"]
minimum_positive_obligations = primary["claim_guards"]["minimum_positive_obligations"]
minimum_positive_libraries = primary["claim_guards"]["minimum_positive_libraries"]
effect_step = power["positive_sensitivity_gain_step"]
library_fraction = power["icc_split"]["library_fraction"]
driver_fraction = power["icc_split"]["driver_fraction"]

scenarios = []
for obligations_per_driver in power[
    "eligible_obligations_per_driver_sensitivity_grid"
]:
    for prevalence in power["prevalence_grid"]:
        for icc in power["combined_driver_library_icc_grid"]:
            positives, shared_fp, false_positive_rate = generate_gold(
                simulations,
                libraries,
                drivers_per_library,
                obligations_per_driver,
                prevalence,
                icc,
                library_fraction,
                driver_fraction,
                baseline_sensitivity,
                precision_value,
                scenario_seed(
                    master_seed,
                    "gold",
                    obligations_per_driver,
                    prevalence,
                    icc,
                ),
            )
            for discordance in power[
                "positive_conditional_detector_discordance_grid"
            ]:
                null_delta, null_eligible = simulate_delta(
                    positives,
                    shared_fp,
                    baseline_sensitivity,
                    discordance,
                    0.0,
                    minimum_positive_obligations,
                    minimum_positive_libraries,
                    scenario_seed(
                        master_seed,
                        "delta",
                        obligations_per_driver,
                        prevalence,
                        icc,
                        discordance,
                        0.0,
                    ),
                )
                eligible_null = null_delta[null_eligible]
                critical_value = (
                    float(np.quantile(eligible_null, 1.0 - alpha / 2.0))
                    if eligible_null.size >= 200
                    else None
                )

                effect_curve = []
                effect_steps = int(round(discordance / effect_step))
                for step in range(1, effect_steps + 1):
                    gain = round(step * effect_step, 10)
                    delta, eligible = simulate_delta(
                        positives,
                        shared_fp,
                        baseline_sensitivity,
                        discordance,
                        gain,
                        minimum_positive_obligations,
                        minimum_positive_libraries,
                        scenario_seed(
                            master_seed,
                            "delta",
                            obligations_per_driver,
                            prevalence,
                            icc,
                            discordance,
                            gain,
                        ),
                    )
                    eligible_count = int(eligible.sum())
                    if critical_value is None or eligible_count == 0:
                        conditional_power = None
                        claimable_power = None
                    else:
                        significant = delta > critical_value
                        conditional_power = float(
                            significant[eligible].mean()
                        )
                        claimable_power = float(
                            (significant & eligible).mean()
                        )

                    effect_curve.append(
                        {
                            "positive_sensitivity_gain": rounded(gain),
                            "median_macro_f1_difference": rounded(
                                np.median(delta)
                            ),
                            "eligibility_probability": rounded(
                                eligible.mean()
                            ),
                            "conditional_power_given_eligibility": (
                                None
                                if conditional_power is None
                                else rounded(conditional_power)
                            ),
                            "claimable_power": (
                                None
                                if claimable_power is None
                                else rounded(claimable_power)
                            ),
                        }
                    )

                scenarios.append(
                    {
                        "eligible_obligations_per_driver": obligations_per_driver,
                        "prevalence": prevalence,
                        "combined_driver_library_icc": icc,
                        "positive_conditional_detector_discordance": discordance,
                        "baseline_false_positive_rate": rounded(
                            false_positive_rate
                        ),
                        "null_eligible_simulations": int(
                            null_eligible.sum()
                        ),
                        "null_critical_value": (
                            None
                            if critical_value is None
                            else rounded(critical_value)
                        ),
                        "conditional_mdi_at_80_percent_power": first_mdi(
                            effect_curve,
                            "conditional_power_given_eligibility",
                            target_power,
                        ),
                        "claimable_mdi_at_80_percent_power": first_mdi(
                            effect_curve,
                            "claimable_power",
                            target_power,
                        ),
                        "effect_curve": effect_curve,
                    }
                )

central_scenarios = {
    str(obligations): next(
        scenario
        for scenario in scenarios
        if scenario["eligible_obligations_per_driver"] == obligations
        and scenario["prevalence"] == 0.10
        and scenario["combined_driver_library_icc"] == 0.05
        and scenario["positive_conditional_detector_discordance"] == 0.10
    )
    for obligations in power[
        "eligible_obligations_per_driver_sensitivity_grid"
    ]
}

report = {
    "schema_version": "1.0.0",
    "gate": "Gate 0E",
    "status": "PASS",
    "planning_only": True,
    "registration": {
        "path": "config/statistical_analysis_registration.json",
        "sha256": EXPECTED_REGISTRATION_SHA256,
    },
    "source_commit_before_registration": EXPECTED_HEAD,
    "script_sha256": hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest(),
    "primary_endpoint": primary["endpoint"],
    "simulation_contract": power,
    "summary": {
        "scenario_count": len(scenarios),
        "conditional_mdi_reached_scenarios": sum(
            scenario["conditional_mdi_at_80_percent_power"] is not None
            for scenario in scenarios
        ),
        "claimable_mdi_reached_scenarios": sum(
            scenario["claimable_mdi_at_80_percent_power"] is not None
            for scenario in scenarios
        ),
        "central_scenarios": central_scenarios,
        "non_reached_interpretation": (
            "The preregistered design does not expand. If actual minimum-"
            "positive guards fail, confirmatory superiority and sensitivity "
            "claims are withheld."
        ),
    },
    "scenarios": scenarios,
    "runtime": {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
    },
    "generation_authorized": False,
    "repair_implementation_allowed": False,
}

with REPORT.open("x", encoding="utf-8") as handle:
    json.dump(report, handle, indent=2, sort_keys=True)
    handle.write("\n")

report_sha256 = hashlib.sha256(REPORT.read_bytes()).hexdigest()
print("GATE0E_POWER_SIMULATION=PASS")
print(f"SCENARIOS={len(scenarios)}")
print(
    "CONDITIONAL_MDI_REACHED_SCENARIOS="
    + str(report["summary"]["conditional_mdi_reached_scenarios"])
)
print(
    "CLAIMABLE_MDI_REACHED_SCENARIOS="
    + str(report["summary"]["claimable_mdi_reached_scenarios"])
)
for obligations, scenario in central_scenarios.items():
    print(
        f"CENTRAL_SCENARIO_OBLIGATIONS_{obligations}="
        + json.dumps(
            {
                "conditional_mdi": scenario[
                    "conditional_mdi_at_80_percent_power"
                ],
                "claimable_mdi": scenario[
                    "claimable_mdi_at_80_percent_power"
                ],
            },
            sort_keys=True,
        )
    )
print("GENERATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"REPORT_SHA256={report_sha256}")
