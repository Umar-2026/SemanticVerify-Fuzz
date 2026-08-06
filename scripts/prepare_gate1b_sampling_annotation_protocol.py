#!/usr/bin/env python3

import datetime
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path


ROOT = Path("/openbayes/home/semanticverify-fuzz-research").resolve()
EXPECTED_HEAD = "a1e0ec0ab0f9515c833d30bd4456cc76056fa0d6"

SELF_REL = "scripts/prepare_gate1b_sampling_annotation_protocol.py"
PROTOCOL_REL = "config/gold_sampling_annotation_protocol.json"
FRAME_SCHEMA_REL = "config/schemas/compilable_sampling_frame.schema.json"
ANNOTATION_SCHEMA_REL = "config/schemas/blind_annotation_record.schema.json"
EXPOSURE_SCHEMA_REL = "config/schemas/annotation_exposure_registry.schema.json"
REPORT_REL = "evidence/gates/gate1/gate1b_sampling_annotation_protocol.json"
README_REL = "evidence/gates/gate1/README.md"
DECISION_REL = (
    "documentation/decisions/"
    "0008-gate1b-sampling-blind-annotation-and-quarantine-freeze.md"
)
VERIFIER_REL = "scripts/verify_gate1b_sampling_annotation_protocol.py"
LOCK_REL = "config/research_lock.json"
STATUS_REL = "documentation/CURRENT_STATUS.md"

PROPOSAL_REL = (
    "provenance/proposal/"
    "SemanticVerify-Fuzz_Verification-First_Staged-Repair_Proposal.docx"
)
EXPECTED_PROPOSAL_SHA256 = (
    "3abc92ee7ac0100a6b9ac148a2ad2a4ca"
    "71d187677cb84abf1545de29afb4a21"
)
EXPECTED_GATE0_MANIFEST_SHA256 = (
    "d7c5495874734a0f2a82289202539d5d"
    "63ac2efbcfcffe9efca6770440ee2526"
)
EXPECTED_GATE1A_CONTRACT_SHA256 = (
    "d376667acc8c6f11e3fc66370c48796d"
    "e3afce1ab23687620b82c32424935acf"
)
EXPECTED_REGISTRATION_SHA256 = (
    "c7537ce5d082de904cc7aef4d617c9ff"
    "6612b30fdb4740b0667c9eb84ca5b2d4"
)


def fail(reason):
    print("GATE1B_SAMPLING_ANNOTATION_PREPARATION=FAIL")
    print(f"REASON={reason}")
    raise SystemExit(1)


def require(condition, reason):
    if not condition:
        fail(reason)


def capture(command):
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(result.returncode == 0, "command failed: " + " ".join(command))
    return result.stdout.strip()


def run(command):
    print("RUN=" + " ".join(command))
    result = subprocess.run(command, cwd=ROOT, check=False)
    require(result.returncode == 0, "command failed: " + " ".join(command))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_new(relative, text, executable=False):
    path = ROOT / relative
    require(not path.exists(), f"refusing to overwrite {relative}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if executable:
        path.chmod(
            path.stat().st_mode
            | stat.S_IXUSR
            | stat.S_IXGRP
            | stat.S_IXOTH
        )


require(ROOT.is_dir(), "repository missing")
require(capture(["git", "rev-parse", "HEAD"]) == EXPECTED_HEAD, "unexpected HEAD")

status_before = capture(
    ["git", "status", "--porcelain", "--untracked-files=all"]
)
actual_before = set(status_before.splitlines()) if status_before else set()
require(
    actual_before <= {f"?? {SELF_REL}"},
    f"unexpected worktree changes: {sorted(actual_before)}",
)
require(
    not os.environ.get("DEEPSEEK_API_KEY")
    and not os.environ.get("GEMINI_API_KEY"),
    "API keys must not be loaded for Gate 1B",
)

proposal_path = ROOT / PROPOSAL_REL
gate0_manifest_path = ROOT / "evidence/gates/gate0/gate0_final_manifest.json"
gate1a_path = ROOT / "config/protocol_obligation_contract.json"
registration_path = ROOT / "config/statistical_analysis_registration.json"

require(digest(proposal_path) == EXPECTED_PROPOSAL_SHA256, "proposal SHA")
require(
    digest(gate0_manifest_path) == EXPECTED_GATE0_MANIFEST_SHA256,
    "Gate 0 manifest SHA",
)
require(digest(gate1a_path) == EXPECTED_GATE1A_CONTRACT_SHA256, "Gate 1A SHA")
require(
    digest(registration_path) == EXPECTED_REGISTRATION_SHA256,
    "statistical registration SHA",
)

for command in [
    ["python3", "scripts/verify_gate0_final_manifest.py"],
    ["python3", "scripts/verify_gate0.py"],
    ["python3", "scripts/verify_gate1a_obligation_contract.py"],
]:
    run(command)

timestamp = (
    datetime.datetime.now(datetime.timezone.utc)
    .replace(microsecond=0)
    .isoformat()
)

libraries = [
    "zlib",
    "libpcap",
    "curl",
    "cJSON",
    "libtiff",
    "libvpx",
    "c-ares",
    "lcms",
]

frame_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://semanticverify-fuzz.invalid/schema/compilable-sampling-frame-1.0.0",
    "title": "Compilable-driver sampling-frame record",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "attempt_id",
        "driver_id",
        "library",
        "model_label",
        "scenario_id",
        "replicate_id",
        "compilation_status",
        "compiler_warning_count",
        "driver_sha256",
        "build_log_sha256",
    ],
    "properties": {
        "attempt_id": {"type": "string", "minLength": 1},
        "driver_id": {"type": "string", "minLength": 1},
        "library": {"enum": libraries},
        "model_label": {"enum": ["Model A", "Model B"]},
        "scenario_id": {"type": "string", "pattern": "^S(0[1-9]|10)$"},
        "replicate_id": {"type": "string", "pattern": "^R0[1-5]$"},
        "compilation_status": {"const": "COMPILED"},
        "compiler_warning_count": {"type": "integer", "minimum": 0},
        "driver_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "build_log_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    },
}

annotation_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://semanticverify-fuzz.invalid/schema/blind-annotation-record-1.0.0",
    "title": "Blind independent annotation record",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "record_id",
        "anonymized_driver_id",
        "annotator_role",
        "phase",
        "resource_identity",
        "rule_or_candidate_id",
        "program_point_or_exit",
        "relevant_branch_condition",
        "required_state",
        "observed_state",
        "discovery_decision",
        "eligibility",
        "verdict",
        "defect_category",
        "evidence_citation",
        "machine_output_exposure",
        "submitted_at_utc",
    ],
    "properties": {
        "record_id": {"type": "string", "minLength": 1},
        "anonymized_driver_id": {
            "type": "string",
            "pattern": "^SVF-GOLD-[0-9]{4}$",
        },
        "annotator_role": {"enum": ["ANNOTATOR_A", "ANNOTATOR_B"]},
        "phase": {"enum": ["DISCOVERY", "VERDICT"]},
        "resource_identity": {"type": "string", "minLength": 1},
        "rule_or_candidate_id": {"type": "string", "minLength": 1},
        "program_point_or_exit": {"type": "string", "minLength": 1},
        "relevant_branch_condition": {"type": ["string", "null"]},
        "required_state": {"type": ["string", "null"]},
        "observed_state": {"type": ["string", "null"]},
        "discovery_decision": {"enum": ["PRESENT", "ABSENT"]},
        "eligibility": {"enum": ["IN_SCOPE", "OUT_OF_SCOPE", None]},
        "verdict": {
            "enum": [
                "VALID",
                "VIOLATION-MUST",
                "VIOLATION-MAY",
                None,
            ]
        },
        "defect_category": {
            "enum": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", None]
        },
        "evidence_citation": {"type": ["string", "null"]},
        "machine_output_exposure": {"const": False},
        "submitted_at_utc": {"type": "string", "format": "date-time"},
    },
    "allOf": [
        {
            "if": {
                "properties": {"phase": {"const": "DISCOVERY"}},
                "required": ["phase"],
            },
            "then": {
                "properties": {
                    "eligibility": {"const": None},
                    "verdict": {"const": None},
                    "defect_category": {"const": None},
                }
            },
        },
        {
            "if": {
                "properties": {"phase": {"const": "VERDICT"}},
                "required": ["phase"],
            },
            "then": {
                "properties": {
                    "eligibility": {"enum": ["IN_SCOPE", "OUT_OF_SCOPE"]},
                    "evidence_citation": {"type": "string", "minLength": 1},
                }
            },
        },
        {
            "if": {
                "properties": {
                    "phase": {"const": "VERDICT"},
                    "eligibility": {"const": "OUT_OF_SCOPE"},
                },
                "required": ["phase", "eligibility"],
            },
            "then": {
                "properties": {
                    "verdict": {"const": None},
                    "defect_category": {"const": None},
                }
            },
        },
        {
            "if": {
                "properties": {
                    "phase": {"const": "VERDICT"},
                    "eligibility": {"const": "IN_SCOPE"},
                },
                "required": ["phase", "eligibility"],
            },
            "then": {
                "properties": {
                    "verdict": {
                        "enum": [
                            "VALID",
                            "VIOLATION-MUST",
                            "VIOLATION-MAY",
                        ]
                    },
                    "required_state": {"type": "string", "minLength": 1},
                    "observed_state": {"type": "string", "minLength": 1},
                    "evidence_citation": {"type": "string", "minLength": 1},
                }
            },
        },
        {
            "if": {
                "properties": {
                    "phase": {"const": "VERDICT"},
                    "eligibility": {"const": "IN_SCOPE"},
                    "verdict": {
                        "enum": ["VIOLATION-MUST", "VIOLATION-MAY"]
                    },
                },
                "required": ["phase", "eligibility", "verdict"],
            },
            "then": {
                "properties": {
                    "defect_category": {
                        "enum": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]
                    }
                }
            },
        },
        {
            "if": {
                "properties": {
                    "phase": {"const": "VERDICT"},
                    "eligibility": {"const": "IN_SCOPE"},
                    "verdict": {"const": "VALID"},
                },
                "required": ["phase", "eligibility", "verdict"],
            },
            "then": {
                "properties": {"defect_category": {"const": None}}
            },
        },
    ],
}

exposure_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://semanticverify-fuzz.invalid/schema/annotation-exposure-registry-1.0.0",
    "title": "Per-person per-driver annotation exposure registry",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "registry_record_id",
        "person_role_id",
        "anonymized_driver_id",
        "exposure_types",
        "eligible_to_annotate",
        "recorded_at_utc",
    ],
    "properties": {
        "registry_record_id": {"type": "string", "minLength": 1},
        "person_role_id": {"type": "string", "minLength": 1},
        "anonymized_driver_id": {
            "type": "string",
            "pattern": "^SVF-GOLD-[0-9]{4}$",
        },
        "exposure_types": {
            "type": "array",
            "uniqueItems": True,
            "items": {
                "enum": [
                    "SEMANTICVERIFY_OUTPUT",
                    "QUARTETFUZZ_OUTPUT",
                    "LLM_REVIEW_OUTPUT",
                    "REPAIR_OUTPUT",
                    "BASELINE_OUTPUT",
                ]
            },
        },
        "eligible_to_annotate": {"type": "boolean"},
        "recorded_at_utc": {"type": "string", "format": "date-time"},
    },
    "allOf": [
        {
            "if": {"properties": {"exposure_types": {"minItems": 1}}},
            "then": {"properties": {"eligible_to_annotate": {"const": False}}},
        }
    ],
}

for relative, value in [
    (FRAME_SCHEMA_REL, frame_schema),
    (ANNOTATION_SCHEMA_REL, annotation_schema),
    (EXPOSURE_SCHEMA_REL, exposure_schema),
]:
    path = ROOT / relative
    require(not path.exists(), f"refusing to overwrite {relative}")
    write_json(path, value)

frame_schema_sha = digest(ROOT / FRAME_SCHEMA_REL)
annotation_schema_sha = digest(ROOT / ANNOTATION_SCHEMA_REL)
exposure_schema_sha = digest(ROOT / EXPOSURE_SCHEMA_REL)

protocol = {
    "schema_version": "1.0.0",
    "gate": "Gate 1B",
    "status": "PASS_FROZEN",
    "title": "Gold Sampling, Blind Annotation, Adjudication, and Exposure Quarantine Protocol",
    "frozen_at_utc": timestamp,
    "authority": {
        "proposal_path": PROPOSAL_REL,
        "proposal_sha256": EXPECTED_PROPOSAL_SHA256,
        "proposal_sections": [
            "7.5 Fixed generation design and sampling-bias control",
            "7.6 Ground truth and blind annotation",
            "7.11 Sample-size rules and low-frequency defects",
            "7.12 Statistical analysis",
            "12 Gate 1 specification foundation",
            "15 Pre-Experiment Registration Checklist",
        ],
        "statistical_registration_path": (
            "config/statistical_analysis_registration.json"
        ),
        "statistical_registration_sha256": EXPECTED_REGISTRATION_SHA256,
        "gate1a_contract_path": "config/protocol_obligation_contract.json",
        "gate1a_contract_sha256": EXPECTED_GATE1A_CONTRACT_SHA256,
    },
    "machine_readable_schemas": {
        "compilable_sampling_frame": {
            "path": FRAME_SCHEMA_REL,
            "sha256": frame_schema_sha,
        },
        "blind_annotation_record": {
            "path": ANNOTATION_SCHEMA_REL,
            "sha256": annotation_schema_sha,
        },
        "annotation_exposure_registry": {
            "path": EXPOSURE_SCHEMA_REL,
            "sha256": exposure_schema_sha,
        },
    },
    "sampling_frame": {
        "population": "all newly generated logical attempts with compilation_status COMPILED",
        "source_attempt_count": 800,
        "eligible_status": "COMPILED",
        "noncompilable_drivers_in_gold_sampling_frame": False,
        "frame_frozen_before_selection": True,
        "driver_content_or_outcome_used_for_selection": False,
        "analyzer_baseline_or_repair_output_used_for_selection": False,
        "required_balance_metadata": [
            "library",
            "model_label",
            "scenario_id",
            "compiler_warning_count",
        ],
        "compilation_characteristic": {
            "CLEAN_COMPILE": "compiler_warning_count equals zero",
            "COMPILED_WITH_WARNINGS": "compiler_warning_count is greater than zero",
        },
    },
    "sample_size": {
        "maximum_compilable_drivers": 140,
        "if_total_compilable_at_most_140": "CENSUS",
        "if_total_compilable_above_140": "SEEDED_STRATIFIED_SAMPLE_WITHOUT_REPLACEMENT",
        "post_hoc_expansion_allowed": False,
        "generation_continues_for_target_compilable_or_defect_yield": False,
        "planning_18_per_held_out_library_is_sampling_quota": False,
    },
    "stratification": {
        "primary_strata": ["library", "model_label"],
        "maximum_primary_strata": 16,
        "library_order": libraries,
        "model_order": ["Model A", "Model B"],
        "every_nonempty_primary_stratum_receives_minimum_one_when_sampling": True,
        "scenario_is_balance_diagnostic_not_zero_probability_quota": True,
        "compilation_characteristic_is_balance_diagnostic_not_zero_probability_quota": True,
        "absence_of_scenario_or_warning_class_coverage_is_reported_not_rerolled": True,
    },
    "allocation_algorithm": {
        "name": "minimum-one capped proportional largest-remainder allocation",
        "steps": [
            "Let N_h be the number of eligible drivers in each nonempty library-by-model stratum.",
            "When total N is at most 140, select every eligible driver with probability one.",
            "When N exceeds 140, assign one slot to every nonempty stratum.",
            "Allocate remaining slots proportionally to residual capacity N_h minus one.",
            "Take each proportional allocation floor, then distribute remaining slots by descending fractional remainder.",
            "Break fractional-remainder ties by frozen library order followed by Model A then Model B.",
            "Never allocate more than N_h; repeat capped redistribution if capacity is reached.",
        ],
        "zero_inclusion_probability_for_eligible_driver": False,
    },
    "within_stratum_selection": {
        "method": "SHA-256 keyed random ranking without replacement",
        "master_seed": 2026080603,
        "ranking_material": "UTF-8 string '2026080603|<driver_id>'",
        "ranking_key": "ascending SHA-256 hex digest, then ascending driver_id",
        "selected_records": "first n_h records in each stratum",
        "replacement_allowed": False,
        "reroll_for_scenario_defect_or_warning_coverage": False,
    },
    "selection_probability_and_weights": {
        "census_inclusion_probability": 1.0,
        "sampled_stratum_inclusion_probability": "pi_h=n_h/N_h",
        "inverse_probability_weight": "w_h=N_h/n_h",
        "record_N_h_n_h_pi_h_and_w_h_for_every_selected_driver": True,
        "weighted_prevalence_required": True,
        "unweighted_counts_required": True,
        "complete_attempt_flow_required": True,
    },
    "anonymization": {
        "identifier_format": "SVF-GOLD-NNNN",
        "mapping_created_after_sample_selection": True,
        "mapping_separate_from_annotation_packets": True,
        "masked_from_primary_annotators": [
            "provider and model identity",
            "attempt and replicate identity",
            "scenario identifier and prompt text",
            "analyzer output",
            "baseline output",
            "LLM-review output",
            "repair output",
        ],
        "visible_to_primary_annotators": [
            "complete anonymized driver source",
            "library identity",
            "frozen approved protocol specification and its cited evidence",
        ],
    },
    "annotation_roles": {
        "primary_annotators": ["ANNOTATOR_A", "ANNOTATOR_B"],
        "primary_annotator_count": 2,
        "both_primary_annotators_are_non_author": True,
        "main_analyzer_or_repair_developer_is_primary_annotator": False,
        "third_adjudicator_required": True,
        "role_roster_status": "MUST_BE_SECURED_BEFORE_ANNOTATION",
        "personal_names_or_credentials_stored_in_this_protocol": False,
        "developer_label_substitution_allowed": False,
        "missing_required_personnel_result": "EXPLORATORY_ONLY",
    },
    "annotation_phases": [
        {
            "order": 1,
            "name": "INDEPENDENT_WHOLE_DRIVER_DISCOVERY",
            "rule": "Each annotator independently discovers all in-scope resources and candidate obligations from the whole driver.",
            "machine_generated_inventory_visible": False,
        },
        {
            "order": 2,
            "name": "BLINDED_UNION_CONSTRUCTION",
            "rule": "Create the normalized union of both frozen discovery submissions without disclosing authorship or verdicts.",
            "machine_generated_inventory_visible": False,
        },
        {
            "order": 3,
            "name": "INDEPENDENT_VERDICT_ASSIGNMENT",
            "rule": "Both annotators independently assign eligibility and verdict to every union obligation before adjudication.",
            "machine_generated_verdict_visible": False,
        },
        {
            "order": 4,
            "name": "THIRD_PARTY_ADJUDICATION",
            "rule": "The third adjudicator resolves discovery, normalization, eligibility, and verdict disagreements with a retained reason code.",
            "machine_generated_output_visible": False,
        },
        {
            "order": 5,
            "name": "GOLD_FREEZE",
            "rule": "Freeze the union inventory and labels before any analyzer or baseline output is revealed.",
            "irreversible_for_primary_analysis": True,
        },
    ],
    "gold_union_required_fields": [
        "outcome",
        "MUST/MAY relevance",
        "defect category",
        "resource",
        "program point or exit",
        "relevant branch condition",
        "required state",
        "observed state",
        "evidence citation",
        "adjudication reason",
    ],
    "human_gold_verdict_contract": {
        "in_scope_verdicts": [
            "VALID",
            "VIOLATION-MUST",
            "VIOLATION-MAY",
        ],
        "analyzer_unknown_is_human_gold_label": False,
        "out_of_scope_receives_validity_verdict": False,
        "verdict_phase_requires_explicit_eligibility": True,
        "violation_requires_D1_through_D8_category": True,
        "valid_requires_null_defect_category": True,
        "in_scope_required_and_observed_state_required": True,
        "verdict_evidence_citation_required": True,
    },
    "exposure_quarantine": {
        "registry_granularity": "per-person per-driver",
        "disqualifying_exposures": [
            "SemanticVerify-Fuzz output",
            "QuartetFuzz output",
            "controlled LLM-review output",
            "baseline output",
            "repair output",
        ],
        "any_disqualifying_exposure_blocks_annotation_for_that_driver": True,
        "exposure_registry_frozen_with_gold_labels": True,
        "labels_frozen_before_comparison": True,
    },
    "agreement_reporting": {
        "resource_discovery": [
            "raw agreement on the frozen union resource inventory",
            "Krippendorff alpha for binary presence when estimable",
        ],
        "obligation_discovery": [
            "raw agreement on normalized union obligations",
            "Krippendorff alpha for binary presence when estimable",
        ],
        "verdicts": [
            "raw agreement",
            "Cohen kappa for nominal human gold verdicts when estimable",
        ],
        "must_may": [
            "raw agreement among violation-labelled instances",
            "Cohen kappa when estimable",
        ],
        "undefined_chance_corrected_metric_rule": "Report NOT_ESTIMABLE and retain raw agreement and counts.",
    },
    "adjudication_reason_codes": [
        "RESOURCE_IDENTITY_DISAGREEMENT",
        "OBLIGATION_PRESENCE_DISAGREEMENT",
        "EQUIVALENT_PATH_NORMALIZATION_DISAGREEMENT",
        "SCOPE_DISAGREEMENT",
        "VERDICT_DISAGREEMENT",
        "MUST_MAY_DISAGREEMENT",
        "DEFECT_CATEGORY_DISAGREEMENT",
        "EVIDENCE_INTERPRETATION_DISAGREEMENT",
    ],
    "post_freeze_correction": {
        "primary_gold_mutation_allowed": False,
        "original_held_out_result_retained": True,
        "correction_role": "SECONDARY_SENSITIVITY_ANALYSIS_ONLY",
    },
    "authorization": {
        "primary_generation_authorized": False,
        "human_held_out_driver_inspection_allowed": False,
        "analyzer_implementation_authorized_by_gate1b": False,
        "repair_implementation_allowed": False,
        "repair_activation_gate": "Gate V",
    },
}

protocol_path = ROOT / PROTOCOL_REL
require(not protocol_path.exists(), f"refusing to overwrite {PROTOCOL_REL}")
write_json(protocol_path, protocol)
protocol_sha = digest(protocol_path)

report = {
    "schema_version": "1.0.0",
    "gate": "Gate 1B",
    "status": "PASS",
    "frozen_at_utc": timestamp,
    "protocol_path": PROTOCOL_REL,
    "protocol_sha256": protocol_sha,
    "sampling_frame_schema_sha256": frame_schema_sha,
    "annotation_schema_sha256": annotation_schema_sha,
    "exposure_schema_sha256": exposure_schema_sha,
    "maximum_gold_drivers": 140,
    "primary_sampling_strata": 16,
    "sampling_seed": 2026080603,
    "all_eligible_drivers_have_positive_inclusion_probability": True,
    "post_hoc_sample_expansion": False,
    "independent_primary_annotators_required": 2,
    "third_adjudicator_required": True,
    "developer_label_substitution_allowed": False,
    "role_roster_secured_claimed": False,
    "role_roster_required_before_annotation": True,
    "eligible_human_gold_unknown_allowed": False,
    "out_of_scope_receives_validity_verdict": False,
    "verdict_phase_requires_explicit_eligibility": True,
    "sample_drawn": False,
    "driver_content_inspected": False,
    "live_api_calls_performed": 0,
    "generated_drivers_created": 0,
    "primary_generation_authorized": False,
    "repair_implementation_allowed": False,
}

report_path = ROOT / REPORT_REL
require(not report_path.exists(), f"refusing to overwrite {REPORT_REL}")
write_json(report_path, report)
report_sha = digest(report_path)

decision = f"""# Decision 0008: Gate 1B Sampling, Blind Annotation, and Quarantine Freeze

- Status: Accepted
- Date: {timestamp[:10]}
- Stage: Stage A — verification
- Gate: Gate 1B

## Sampling decision

The gold frame contains only newly generated drivers that compile under the
future pinned build procedure. If at most 140 compile, the study uses a census.
Otherwise it draws exactly 140 without replacement using library-by-model
strata, a minimum-one capped proportional largest-remainder allocation, and the
preregistered SHA-256 ranking seed `2026080603`.

Every eligible driver has positive conditional inclusion probability. Each
selected driver records `N_h`, `n_h`, `pi_h=n_h/N_h`, and `w_h=N_h/n_h`.
Scenario and compiler-warning coverage are diagnostics, not zero-probability
quotas. No reroll, replacement, desired-yield generation, or post-hoc expansion
is allowed. The Gate 0 power-planning value of 18 held-out drivers per library
is explicitly not a sampling quota.

## Annotation decision

Two non-author annotators independently inspect each whole anonymized driver,
discover resources and obligations before verdict assignment, label the blinded
union independently, and submit records before third-party adjudication. The
main analyzer/repair developer cannot serve as a primary annotator.

Eligible human gold records use VALID, VIOLATION-MUST, or VIOLATION-MAY;
UNKNOWN remains an analyzer abstention and is not a human gold label.
OUT_OF_SCOPE records receive no validity verdict. Violations require a D1-D8
category, while VALID records carry no defect category. Every verdict-phase
record must declare IN_SCOPE or OUT_OF_SCOPE and retain an evidence citation.

A per-person per-driver exposure registry disqualifies anyone who has viewed
SemanticVerify-Fuzz, QuartetFuzz, controlled-LLM, baseline, or repair output for
that driver. Gold labels freeze before machine output is revealed. Missing two
independent annotators or a third adjudicator downgrades affected results to
exploratory; developer labels cannot substitute.

## Boundary

No sample is drawn, no driver is opened, and no model is called by this freeze.
Gate 1 remains in progress. Analyzer implementation is not authorized by Gate
1B, primary generation remains blocked, and repair remains prohibited until
Gate V.
"""
write_new(DECISION_REL, decision)

readme_path = ROOT / README_REL
readme = readme_path.read_text(encoding="utf-8")
old_completed = """- Gate 1A: protocol-obligation schema, verdict contract, D1-D8 taxonomy,
  UNKNOWN limitation codes, provenance fields, and equivalent-path
  normalization contract.
"""
new_completed = old_completed + """
- Gate 1B: positive-probability gold sampling, whole-driver blind annotation,
  third-party adjudication, agreement reporting, and per-driver exposure
  quarantine protocol.
"""
require(readme.count(old_completed) == 1, "Gate 1 README completed marker")
readme = readme.replace(old_completed, new_completed, 1)
old_pending = """- Sampling, blind-annotation, adjudication, and exposure-quarantine protocol.
- Frozen system prompt and all 80 exact library-specific scenario bindings.
"""
new_pending = """- Frozen system prompt and all 80 exact library-specific scenario bindings.
"""
require(readme.count(old_pending) == 1, "Gate 1 README pending marker")
readme = readme.replace(old_pending, new_pending, 1)
readme_path.write_text(readme, encoding="utf-8")

verifier = r'''#!/usr/bin/env python3

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
'''
write_new(VERIFIER_REL, verifier, executable=True)

lock_path = ROOT / LOCK_REL
lock = read_json(lock_path)
current = lock["current_status"]
gate1 = lock["gate1_foundation"]
require(current["gate_0"] == "PASS", "Gate 0 status")
require(current["gate_1"] == "IN_PROGRESS", "Gate 1 status")
require(current["gate_1a_obligation_contract"] == "PASS", "Gate 1A status")
require(gate1["status"] == "IN_PROGRESS", "Gate 1 foundation status")
require("gate1b_sampling_annotation_protocol" not in gate1, "Gate 1B already exists")

gate1["gate1b_sampling_annotation_protocol"] = {
    "status": "PASS",
    "protocol_path": PROTOCOL_REL,
    "protocol_sha256": protocol_sha,
    "report_path": REPORT_REL,
    "report_sha256": report_sha,
    "sampling_frame_schema_path": FRAME_SCHEMA_REL,
    "sampling_frame_schema_sha256": frame_schema_sha,
    "annotation_schema_path": ANNOTATION_SCHEMA_REL,
    "annotation_schema_sha256": annotation_schema_sha,
    "exposure_schema_path": EXPOSURE_SCHEMA_REL,
    "exposure_schema_sha256": exposure_schema_sha,
    "maximum_gold_drivers": 140,
    "sampling_seed": 2026080603,
    "post_hoc_sample_expansion": False,
    "role_roster_required_before_annotation": True,
}
current["gate_1b_sampling_annotation_protocol"] = "PASS"
current["milestone"] = (
    "Gate 1B sampling, blind annotation, adjudication, and exposure "
    "quarantine protocol complete; Gate 1 remains in progress"
)
write_json(lock_path, lock)

status_path = ROOT / STATUS_REL
status_text = status_path.read_text(encoding="utf-8")
old_milestone = (
    "- Current milestone: Gate 1A — obligation schema and normalization "
    "contract complete"
)
new_milestone = (
    "- Current milestone: Gate 1B — sampling, blind annotation, "
    "adjudication, and exposure quarantine complete"
)
require(status_text.count(old_milestone) == 1, "status milestone")
status_text = status_text.replace(old_milestone, new_milestone, 1)
old_gate1a = "- Gate 1A obligation schema and normalization contract: PASS"
new_gate1a = old_gate1a + "\n- Gate 1B sampling and blind-annotation protocol: PASS"
require(status_text.count(old_gate1a) == 1, "status Gate 1A marker")
status_text = status_text.replace(old_gate1a, new_gate1a, 1)
old_next = """1. Continue Gate 1 with the sampling, blind-annotation, adjudication, and exposure-quarantine protocol.
2. Freeze the system prompt and all 80 exact library-specific scenario bindings.
3. Freeze eight library source/build locks and provider price-sheet snapshots.
4. Close Gate 1 with a verified manifest; generation still requires later explicit authorization.
"""
new_next = """1. Freeze the system prompt and all 80 exact library-specific scenario bindings.
2. Freeze eight library source/build locks and provider price-sheet snapshots.
3. Record the required independent-annotation role roster before annotation begins.
4. Close Gate 1 with a verified manifest; generation still requires later explicit authorization.
"""
require(status_text.count(old_next) == 1, "status next-work marker")
status_text = status_text.replace(old_next, new_next, 1)
status_path.write_text(status_text, encoding="utf-8")

for command in [
    ["python3", "scripts/scan_repository_secrets.py"],
    ["python3", "scripts/verify_gate0_final_manifest.py"],
    ["python3", "scripts/verify_gate0.py"],
    ["python3", "scripts/verify_gate1a_obligation_contract.py"],
    ["python3", VERIFIER_REL],
    ["git", "diff", "--check"],
]:
    run(command)

require(
    digest(gate0_manifest_path) == EXPECTED_GATE0_MANIFEST_SHA256,
    "Gate 0 manifest mutated",
)

print("GATE1B_SAMPLING_ANNOTATION_PREPARATION=PASS")
print("GATE0_IMMUTABLE_INPUTS_MUTATED=NO")
print("GATE1A_STATUS=PASS")
print("GATE1B_STATUS=PASS")
print("SAMPLE_DRAWN=NO")
print("DRIVER_CONTENT_INSPECTED=NO")
print("ROLE_ROSTER_SECURED_CLAIMED=NO")
print("ELIGIBLE_HUMAN_GOLD_UNKNOWN_ALLOWED=NO")
print("OUT_OF_SCOPE_VALIDITY_VERDICT=NO")
print("VERDICT_PHASE_EXPLICIT_ELIGIBILITY=YES")
print("LIVE_API_CALLS_PERFORMED=NO")
print("GENERATION_AUTHORIZED=NO")
print("HELD_OUT_DRIVER_INSPECTION_ALLOWED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"PROTOCOL_SHA256={protocol_sha}")
print(f"REPORT_SHA256={report_sha}")
print("STATUS=")
run(["git", "status", "--short", "--branch"])
