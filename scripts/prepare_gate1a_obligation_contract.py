#!/usr/bin/env python3

import datetime
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path


ROOT = Path("/openbayes/home/semanticverify-fuzz-research").resolve()
EXPECTED_HEAD = "dd3326c7c88e7fba07a8d68bc2aa3e8d868074d2"

SELF_REL = "scripts/prepare_gate1a_obligation_contract.py"
CONTRACT_REL = "config/protocol_obligation_contract.json"
PROTOCOL_SCHEMA_REL = "config/schemas/protocol_specification.schema.json"
INSTANCE_SCHEMA_REL = (
    "config/schemas/normalized_obligation_instance.schema.json"
)
REPORT_REL = "evidence/gates/gate1/gate1a_obligation_contract.json"
README_REL = "evidence/gates/gate1/README.md"
DECISION_REL = (
    "documentation/decisions/"
    "0007-gate1a-obligation-schema-and-normalization-freeze.md"
)
VERIFIER_REL = "scripts/verify_gate1a_obligation_contract.py"
LOCK_REL = "config/research_lock.json"
STATUS_REL = "documentation/CURRENT_STATUS.md"
GATE0_FINAL_VERIFIER_REL = "scripts/verify_gate0_final_manifest.py"

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


def fail(reason):
    print("GATE1A_OBLIGATION_CONTRACT_PREPARATION=FAIL")
    print(f"REASON={reason}")
    raise SystemExit(1)


def require(condition, reason):
    if not condition:
        fail(reason)


def run(command, expected_codes=(0,)):
    print("RUN=" + " ".join(command))
    result = subprocess.run(command, cwd=ROOT, check=False)
    require(
        result.returncode in expected_codes,
        "command failed: " + " ".join(command),
    )
    return result


def capture(command):
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(
        result.returncode == 0,
        "command failed: " + " ".join(command),
    )
    return result.stdout.strip()


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


def write_new_text(relative, text, executable=False):
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
require(
    capture(["git", "rev-parse", "HEAD"]) == EXPECTED_HEAD,
    "unexpected HEAD",
)

status_before = capture(
    ["git", "status", "--porcelain", "--untracked-files=all"]
)
allowed_before = {f"?? {SELF_REL}"}
actual_before = set(status_before.splitlines()) if status_before else set()
require(
    actual_before <= allowed_before,
    f"unexpected pre-existing worktree changes: {sorted(actual_before)}",
)

require(
    not os.environ.get("DEEPSEEK_API_KEY")
    and not os.environ.get("GEMINI_API_KEY"),
    "API keys must not be loaded for Gate 1A",
)

proposal_path = ROOT / PROPOSAL_REL
require(proposal_path.is_file(), "authoritative proposal missing")
require(
    digest(proposal_path) == EXPECTED_PROPOSAL_SHA256,
    "authoritative proposal SHA-256 mismatch",
)

gate0_manifest_path = (
    ROOT / "evidence/gates/gate0/gate0_final_manifest.json"
)
require(gate0_manifest_path.is_file(), "Gate 0 final manifest missing")
require(
    digest(gate0_manifest_path) == EXPECTED_GATE0_MANIFEST_SHA256,
    "Gate 0 final manifest changed",
)

for command in [
    ["python3", "scripts/verify_gate0c_proposal.py"],
    ["python3", "scripts/verify_gate0d_documentation.py"],
    ["python3", "scripts/verify_gate0d_live.py"],
    ["python3", "scripts/verify_gate0e_analysis.py"],
    ["python3", "scripts/verify_gate0f_generation_protocol.py"],
    ["python3", "scripts/verify_gate0_final_manifest.py"],
    ["python3", "scripts/verify_gate0.py"],
]:
    run(command)

timestamp = (
    datetime.datetime.now(datetime.timezone.utc)
    .replace(microsecond=0)
    .isoformat()
)

protocol_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://semanticverify-fuzz.invalid/schema/protocol-specification-1.0.0",
    "title": "SemanticVerify-Fuzz protocol specification",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "specification_id",
        "library",
        "library_revision",
        "resource_kind",
        "states",
        "initial_state",
        "events",
        "transitions",
        "permitted_exit_states",
        "obligations",
        "provenance",
        "author",
        "reviewer",
        "creation_date",
        "freeze_date",
        "content_sha256",
    ],
    "properties": {
        "schema_version": {"const": "1.0.0"},
        "specification_id": {
            "type": "string",
            "pattern": "^[a-z0-9][a-z0-9._-]*$",
        },
        "library": {"type": "string", "minLength": 1},
        "library_revision": {"type": "string", "minLength": 1},
        "resource_kind": {"type": "string", "minLength": 1},
        "states": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {"type": "string", "minLength": 1},
        },
        "initial_state": {"type": "string", "minLength": 1},
        "events": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["event_id", "event_kind", "symbol_or_condition"],
                "properties": {
                    "event_id": {"type": "string", "minLength": 1},
                    "event_kind": {
                        "enum": ["API_CALL", "BRANCH", "FUNCTION_EXIT"],
                    },
                    "symbol_or_condition": {"type": "string", "minLength": 1},
                },
            },
        },
        "transitions": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "transition_id",
                    "from_states",
                    "event_id",
                    "to_states",
                    "return_predicate",
                    "ownership_effect",
                ],
                "properties": {
                    "transition_id": {"type": "string", "minLength": 1},
                    "from_states": {
                        "type": "array",
                        "minItems": 1,
                        "uniqueItems": True,
                        "items": {"type": "string", "minLength": 1},
                    },
                    "event_id": {"type": "string", "minLength": 1},
                    "to_states": {
                        "type": "array",
                        "minItems": 1,
                        "uniqueItems": True,
                        "items": {"type": "string", "minLength": 1},
                    },
                    "return_predicate": {"type": ["string", "null"]},
                    "ownership_effect": {
                        "enum": [
                            "NONE",
                            "ACQUIRE",
                            "BORROW",
                            "TRANSFER_IN",
                            "TRANSFER_OUT",
                            "RELEASE",
                            "UNKNOWN",
                        ]
                    },
                },
            },
        },
        "permitted_exit_states": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {"type": "string", "minLength": 1},
        },
        "obligations": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "rule_id",
                    "resource_kind",
                    "triggering_event_or_function_exit",
                    "required_pre_state_or_exit_condition",
                    "permitted_transitions",
                    "return_predicate",
                    "ownership_effect",
                    "cleanup_responsibility",
                    "defect_category",
                    "severity",
                    "source_evidence",
                    "specification_author",
                    "creation_date",
                    "freeze_date",
                    "library_revision",
                    "content_sha256",
                ],
                "properties": {
                    "rule_id": {"type": "string", "minLength": 1},
                    "resource_kind": {"type": "string", "minLength": 1},
                    "triggering_event_or_function_exit": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "required_pre_state_or_exit_condition": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "permitted_transitions": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "return_predicate": {"type": ["string", "null"]},
                    "ownership_effect": {
                        "enum": [
                            "NONE",
                            "ACQUIRE",
                            "BORROW",
                            "TRANSFER_IN",
                            "TRANSFER_OUT",
                            "RELEASE",
                            "UNKNOWN",
                        ]
                    },
                    "cleanup_responsibility": {"type": "string", "minLength": 1},
                    "defect_category": {
                        "enum": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"],
                    },
                    "severity": {
                        "enum": ["LOW", "MEDIUM", "HIGH", "UNSPECIFIED"],
                    },
                    "source_evidence": {
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "string", "minLength": 1},
                    },
                    "specification_author": {"type": "string", "minLength": 1},
                    "creation_date": {
                        "type": "string",
                        "format": "date",
                    },
                    "freeze_date": {"type": "string", "format": "date"},
                    "library_revision": {"type": "string", "minLength": 1},
                    "content_sha256": {
                        "type": "string",
                        "pattern": "^[0-9a-f]{64}$",
                    },
                },
            },
        },
        "provenance": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "evidence_id",
                    "source_type",
                    "path_or_url",
                    "retrieval_date",
                    "quoted_or_paraphrased_rationale",
                    "content_sha256",
                ],
                "properties": {
                    "evidence_id": {"type": "string", "minLength": 1},
                    "source_type": {
                        "enum": [
                            "OFFICIAL_API_DOCUMENTATION",
                            "PUBLIC_HEADER",
                            "PINNED_IMPLEMENTATION_SOURCE",
                            "PINNED_UPSTREAM_TEST",
                            "PREDECLARED_UPSTREAM_EXAMPLE",
                        ]
                    },
                    "path_or_url": {"type": "string", "minLength": 1},
                    "retrieval_date": {"type": "string", "format": "date"},
                    "quoted_or_paraphrased_rationale": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "content_sha256": {
                        "type": "string",
                        "pattern": "^[0-9a-f]{64}$",
                    },
                },
            },
        },
        "author": {"type": "string", "minLength": 1},
        "reviewer": {"type": "string", "minLength": 1},
        "creation_date": {"type": "string", "format": "date"},
        "freeze_date": {"type": "string", "format": "date"},
        "content_sha256": {
            "type": "string",
            "pattern": "^[0-9a-f]{64}$",
        },
    },
}

instance_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://semanticverify-fuzz.invalid/schema/normalized-obligation-instance-1.0.0",
    "title": "SemanticVerify-Fuzz normalized protocol-obligation instance",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "obligation_instance_id",
        "driver_id",
        "resource_identity",
        "rule_id",
        "program_point_or_exit",
        "abstract_context",
        "eligibility",
        "out_of_scope_reason",
        "required_condition",
        "observed_state_set",
        "relevant_branch_predicate_class",
        "raw_witness_paths",
        "verdict",
        "unknown_limitation_codes",
        "defect_category",
        "severity",
        "source_evidence",
    ],
    "properties": {
        "schema_version": {"const": "1.0.0"},
        "obligation_instance_id": {"type": "string", "minLength": 1},
        "driver_id": {"type": "string", "minLength": 1},
        "resource_identity": {"type": "string", "minLength": 1},
        "rule_id": {"type": "string", "minLength": 1},
        "program_point_or_exit": {"type": "string", "minLength": 1},
        "abstract_context": {"type": "string", "minLength": 1},
        "eligibility": {"enum": ["IN_SCOPE", "OUT_OF_SCOPE"]},
        "out_of_scope_reason": {"type": ["string", "null"]},
        "required_condition": {"type": "string", "minLength": 1},
        "observed_state_set": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {"type": "string", "minLength": 1},
        },
        "relevant_branch_predicate_class": {
            "type": "string",
            "minLength": 1,
        },
        "raw_witness_paths": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "verdict": {
            "type": ["string", "null"],
            "enum": [
                "VALID",
                "VIOLATION-MUST",
                "VIOLATION-MAY",
                "UNKNOWN",
                None,
            ],
        },
        "unknown_limitation_codes": {
            "type": "array",
            "uniqueItems": True,
            "items": {
                "enum": [
                    "U01_UNSUPPORTED_SEMANTICS",
                    "U02_UNRESOLVED_ALIAS",
                    "U03_UNRESOLVED_INDIRECT_CALL",
                    "U04_STATE_CAP_EXHAUSTION",
                    "U05_MISSING_EVIDENCE",
                    "U06_OUT_OF_MODEL_INTERACTION",
                    "U07_UNSUPPORTED_SIDE_EFFECT",
                ]
            },
        },
        "defect_category": {
            "type": ["string", "null"],
            "enum": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", None],
        },
        "severity": {
            "enum": ["LOW", "MEDIUM", "HIGH", "UNSPECIFIED"],
        },
        "source_evidence": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
    },
    "allOf": [
        {
            "if": {"properties": {"eligibility": {"const": "OUT_OF_SCOPE"}}},
            "then": {
                "properties": {
                    "verdict": {"const": None},
                    "out_of_scope_reason": {"type": "string", "minLength": 1},
                }
            },
        },
        {
            "if": {"properties": {"verdict": {"const": "UNKNOWN"}}},
            "then": {
                "properties": {
                    "unknown_limitation_codes": {"minItems": 1}
                }
            },
        },
    ],
}

protocol_schema_path = ROOT / PROTOCOL_SCHEMA_REL
instance_schema_path = ROOT / INSTANCE_SCHEMA_REL
require(
    not protocol_schema_path.exists(),
    f"refusing to overwrite {PROTOCOL_SCHEMA_REL}",
)
require(
    not instance_schema_path.exists(),
    f"refusing to overwrite {INSTANCE_SCHEMA_REL}",
)
write_json(protocol_schema_path, protocol_schema)
write_json(instance_schema_path, instance_schema)
protocol_schema_sha256 = digest(protocol_schema_path)
instance_schema_sha256 = digest(instance_schema_path)

contract = {
    "schema_version": "1.0.0",
    "gate": "Gate 1A",
    "status": "PASS_FROZEN",
    "title": "Protocol Obligation, Verdict, and Normalization Contract",
    "authority": {
        "proposal_path": PROPOSAL_REL,
        "proposal_sha256": EXPECTED_PROPOSAL_SHA256,
        "proposal_sections": [
            "4.1 Fuzz-driver-specific protocol obligation",
            "4.2 Evaluation unit and path normalization",
            "4.3 Three base outcomes and violation quantifiers",
            "4.4 Soundness and completeness boundary",
            "7.2 Defect taxonomy",
            "7.3 Protocol-specification creation and leakage control",
            "12 Gate 1 specification foundation",
            "15 Pre-Experiment Registration Checklist",
        ],
    },
    "frozen_at_utc": timestamp,
    "scope": {
        "language": "C and C-compatible fuzz drivers",
        "primary_unit": "normalized protocol-obligation instance",
        "formalism_is_engineering_representation": True,
        "universal_c_correctness_claim": False,
        "raw_cfg_paths_are_independent_samples": False,
        "library_specific_rules_in_this_artifact": False,
        "analyzer_implementation_in_this_artifact": False,
    },
    "machine_readable_schemas": {
        "protocol_specification": {
            "path": PROTOCOL_SCHEMA_REL,
            "sha256": protocol_schema_sha256,
            "json_schema_draft": "2020-12",
        },
        "normalized_obligation_instance": {
            "path": INSTANCE_SCHEMA_REL,
            "sha256": instance_schema_sha256,
            "json_schema_draft": "2020-12",
        },
    },
    "protocol_specification": {
        "notation": "P=(S,s0,A,delta,F,Omega)",
        "elements": {
            "S": "finite set of abstract resource states",
            "s0": "initial abstract resource state",
            "A": "API and branch events",
            "delta": (
                "return- and ownership-conditioned transition relation"
            ),
            "F": "permitted exit states",
            "Omega": "protocol obligations",
        },
        "required_top_level_fields": [
            "schema_version",
            "specification_id",
            "library",
            "library_revision",
            "resource_kind",
            "states",
            "initial_state",
            "events",
            "transitions",
            "permitted_exit_states",
            "obligations",
            "provenance",
            "author",
            "reviewer",
            "creation_date",
            "freeze_date",
            "content_sha256",
        ],
    },
    "obligation_rule_required_fields": [
        "rule_id",
        "resource_kind",
        "triggering_event_or_function_exit",
        "required_pre_state_or_exit_condition",
        "permitted_transitions",
        "return_predicate",
        "ownership_effect",
        "cleanup_responsibility",
        "defect_category",
        "severity",
        "source_evidence",
        "specification_author",
        "creation_date",
        "freeze_date",
        "library_revision",
        "content_sha256",
    ],
    "normalized_obligation_instance": {
        "notation": (
            "O=<driver,resource,rule,program-point-or-exit,"
            "abstract-context>"
        ),
        "identity_fields": [
            "driver_id",
            "resource_identity",
            "rule_id",
            "program_point_or_exit",
            "abstract_context",
        ],
        "required_evidence_fields": [
            "required_condition",
            "observed_state_set",
            "relevant_branch_predicate_class",
            "raw_witness_paths",
        ],
        "one_call_site_may_instantiate_multiple_obligations": True,
        "one_defect_may_involve_multiple_call_sites": True,
    },
    "equivalent_path_normalization": {
        "merge_only_when_all_equal": [
            "normalized obligation identity",
            "abstract resource identity",
            "required condition",
            "observed state set",
            "relevant branch predicate class",
        ],
        "raw_paths_retained_as_evidence": True,
        "raw_paths_counted_as_independent_samples": False,
        "normalization_frozen_before_analyzer_or_baseline_scoring": True,
    },
    "reporting_levels": [
        {
            "level": "obligation",
            "role": "primary detector and statistical unit",
        },
        {
            "level": "adjudicated defect",
            "role": "merge obligations representing the same root cause",
        },
        {
            "level": "driver",
            "role": "whether at least one confirmed defect is present",
        },
    ],
    "eligibility_contract": {
        "values": ["IN_SCOPE", "OUT_OF_SCOPE"],
        "recorded_separately_from_verdict": True,
        "out_of_scope_receives_validity_verdict": False,
        "out_of_scope_reason_required": True,
    },
    "verdict_contract": {
        "base_outcomes": ["VALID", "VIOLATION", "UNKNOWN"],
        "serialized_labels": [
            "VALID",
            "VIOLATION-MUST",
            "VIOLATION-MAY",
            "UNKNOWN",
        ],
        "operational_meanings": {
            "VALID": (
                "All analyzer-consistent abstract states reaching the "
                "obligation satisfy the required condition within the "
                "declared analysis bounds."
            ),
            "VIOLATION-MUST": (
                "Every analyzer-consistent abstract state reaching the "
                "obligation violates the required condition, or every "
                "relevant exit violates a cleanup obligation."
            ),
            "VIOLATION-MAY": (
                "At least one analyzer-consistent state violates and at "
                "least one does not, or bounded merging prevents MUST "
                "while retaining an abstract witness."
            ),
            "UNKNOWN": (
                "The bounded analyzer cannot justify VALID or VIOLATION."
            ),
        },
        "unknown_is_valid": False,
        "unknown_on_eligible_gold_primary_scoring": "INCORRECT",
        "must_may_describe_abstract_states_not_all_concrete_executions": True,
    },
    "unknown_limitation_codes": [
        {
            "code": "U01_UNSUPPORTED_SEMANTICS",
            "meaning": "required semantics are unsupported",
        },
        {
            "code": "U02_UNRESOLVED_ALIAS",
            "meaning": "resource aliasing cannot be resolved within scope",
        },
        {
            "code": "U03_UNRESOLVED_INDIRECT_CALL",
            "meaning": "an indirect call target cannot be resolved",
        },
        {
            "code": "U04_STATE_CAP_EXHAUSTION",
            "meaning": "the frozen abstract-state cap is exhausted",
        },
        {
            "code": "U05_MISSING_EVIDENCE",
            "meaning": "required specification or program evidence is missing",
        },
        {
            "code": "U06_OUT_OF_MODEL_INTERACTION",
            "meaning": "an interaction falls outside the declared model",
        },
        {
            "code": "U07_UNSUPPORTED_SIDE_EFFECT",
            "meaning": "a relevant side effect is unsupported or unmodelled",
        },
    ],
    "defect_taxonomy": {
        "D1": "Use before successful initialization",
        "D2": "Use after failed initialization or activation",
        "D3": "Use after close, destroy, end, or release",
        "D4": "Double close, destroy, end, or release",
        "D5": "Missing cleanup on a success or failure exit",
        "D6": "Invalid API call ordering or missing prerequisite call",
        "D7": (
            "Ownership misuse: freeing borrowed data, failing transferred "
            "ownership, or wrong owner"
        ),
        "D8": (
            "Conditionally invalid cleanup or cleanup under the wrong "
            "state or return condition"
        ),
    },
    "excluded_unless_entailed_by_frozen_obligation": [
        "buffer overflow",
        "arbitrary semantic mistake",
        "security-boundary violation",
        "entry-point adequacy",
        "general vulnerability detection",
    ],
    "provenance_schema": {
        "approved_source_types": [
            "pinned official API documentation",
            "public headers at the pinned revision",
            "pinned implementation source",
            "pinned upstream tests",
            "predeclared upstream usage examples",
        ],
        "evidence_item_required_fields": [
            "source_type",
            "path_or_url",
            "retrieval_date",
            "quoted_or_paraphrased_rationale",
            "content_sha256",
        ],
        "rule_authorship_required_fields": [
            "author",
            "reviewer",
            "creation_date",
            "revision",
            "freeze_date",
        ],
        "second_review_checks": [
            "evidence completeness",
            "transition consistency",
            "ownership effects",
            "terminal states",
            "unsupported conditions",
        ],
    },
    "leakage_controls": {
        "prohibited_before_specification_freeze": [
            "generated experimental drivers",
            "manual gold labels",
            "analyzer output",
            "repair output",
            "defect-triggering mutations",
            "post hoc issue searches prompted by observed failures",
        ],
        "held_out_protocols_frozen_before_driver_open_or_annotation": True,
        "specification_and_analyzer_errors_coded_separately": True,
        "held_out_primary_result_remains_frozen_after_specification_error": True,
        "corrected_result_role": "SECONDARY_SENSITIVITY_ANALYSIS_ONLY",
    },
    "stage_boundaries": {
        "current_stage": "Stage A - verification",
        "primary_generation_authorized": False,
        "held_out_driver_inspection_allowed": False,
        "analyzer_implementation_authorized_by_gate1a": False,
        "repair_implementation_allowed": False,
        "repair_activation_gate": "Gate V",
    },
}

contract_path = ROOT / CONTRACT_REL
require(not contract_path.exists(), f"refusing to overwrite {CONTRACT_REL}")
write_json(contract_path, contract)
contract_sha256 = digest(contract_path)

report = {
    "schema_version": "1.0.0",
    "gate": "Gate 1A",
    "status": "PASS",
    "frozen_at_utc": timestamp,
    "contract_path": CONTRACT_REL,
    "contract_sha256": contract_sha256,
    "proposal_sha256": EXPECTED_PROPOSAL_SHA256,
    "machine_readable_schema_count": 2,
    "protocol_schema_sha256": protocol_schema_sha256,
    "normalized_instance_schema_sha256": instance_schema_sha256,
    "taxonomy_categories": 8,
    "serialized_verdicts": 4,
    "unknown_limitation_codes": 7,
    "reporting_levels": 3,
    "raw_cfg_paths_are_independent_samples": False,
    "unknown_is_valid": False,
    "library_specific_rules_created": False,
    "system_prompt_created": False,
    "scenario_bindings_created": 0,
    "live_api_calls_performed": 0,
    "generated_drivers_created": 0,
    "held_out_driver_inspection_allowed": False,
    "analyzer_implementation_created": False,
    "primary_generation_authorized": False,
    "repair_implementation_allowed": False,
}

report_path = ROOT / REPORT_REL
require(not report_path.exists(), f"refusing to overwrite {REPORT_REL}")
write_json(report_path, report)
report_sha256 = digest(report_path)

readme = """# Gate 1 Evidence

Gate 1 establishes the specification foundation required by the authoritative
proposal. It does not authorize primary generation, held-out driver inspection,
analyzer implementation, or repair implementation.

Completed:

- Gate 1A: protocol-obligation schema, verdict contract, D1-D8 taxonomy,
  UNKNOWN limitation codes, provenance fields, and equivalent-path
  normalization contract.

Pending:

- Sampling, blind-annotation, adjudication, and exposure-quarantine protocol.
- Frozen system prompt and all 80 exact library-specific scenario bindings.
- Eight source/build locks, provider price snapshots, and final Gate 1 manifest.

Library-specific protocol rules begin with zlib at Gate 2. Six held-out protocol
files and scenarios must be frozen before their generated drivers are opened or
annotated.
"""
write_new_text(README_REL, readme)

decision = f"""# Decision 0007: Gate 1A Obligation Schema and Normalization Freeze

- Status: Accepted
- Date: {timestamp[:10]}
- Stage: Stage A — verification
- Gate: Gate 1A

## Decision

The project freezes the proposal-defined protocol representation
`P=(S,s0,A,delta,F,Omega)` and the primary normalized evaluation unit
`O=<driver,resource,rule,program-point-or-exit,abstract-context>`.

Raw CFG paths are retained only as evidence. They are merged when the normalized
obligation identity, abstract resource identity, required condition, observed
state set, and relevant branch-predicate class agree. Raw paths are never
independent statistical samples.

Eligibility is separate from verdict. The three base outcomes are VALID,
VIOLATION, and UNKNOWN; VIOLATION is quantified as MUST or MAY, producing four
serialized labels. UNKNOWN is never VALID and is incorrect on eligible gold
instances for the primary endpoint.

The D1-D8 proposal taxonomy, provenance fields, approved evidence classes,
prohibited pre-freeze inputs, and seven explicit UNKNOWN limitation codes are
frozen in `{CONTRACT_REL}`. Two Draft 2020-12 machine-readable schemas freeze
the protocol-file and normalized-obligation record shapes.

## Boundary

This decision creates no library-specific protocol rule, system prompt,
scenario binding, generated driver, analyzer implementation, held-out
inspection, or repair implementation. Gate 1 remains in progress. Primary
generation remains unauthorized, and repair remains prohibited until Gate V.
"""
write_new_text(DECISION_REL, decision)

verifier = r'''#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "config/protocol_obligation_contract.json"
PROTOCOL_SCHEMA = ROOT / "config/schemas/protocol_specification.schema.json"
INSTANCE_SCHEMA = ROOT / "config/schemas/normalized_obligation_instance.schema.json"
REPORT = ROOT / "evidence/gates/gate1/gate1a_obligation_contract.json"
LOCK = ROOT / "config/research_lock.json"
PROPOSAL = (
    ROOT
    / "provenance/proposal"
    / "SemanticVerify-Fuzz_Verification-First_Staged-Repair_Proposal.docx"
)

EXPECTED_PROPOSAL_SHA256 = (
    "3abc92ee7ac0100a6b9ac148a2ad2a4ca"
    "71d187677cb84abf1545de29afb4a21"
)


def require(condition, reason):
    if not condition:
        print("GATE1A_OBLIGATION_CONTRACT=FAIL")
        print(f"REASON={reason}")
        raise SystemExit(1)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


require(CONTRACT.is_file(), "contract missing")
require(PROTOCOL_SCHEMA.is_file(), "protocol schema missing")
require(INSTANCE_SCHEMA.is_file(), "instance schema missing")
require(REPORT.is_file(), "freeze report missing")
require(LOCK.is_file(), "research lock missing")
require(PROPOSAL.is_file(), "proposal missing")
require(digest(PROPOSAL) == EXPECTED_PROPOSAL_SHA256, "proposal SHA")

contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
protocol_schema = json.loads(PROTOCOL_SCHEMA.read_text(encoding="utf-8"))
instance_schema = json.loads(INSTANCE_SCHEMA.read_text(encoding="utf-8"))
report = json.loads(REPORT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))

require(contract["gate"] == "Gate 1A", "gate")
require(contract["status"] == "PASS_FROZEN", "contract status")
schemas = contract["machine_readable_schemas"]
require(
    schemas["protocol_specification"]["path"]
    == PROTOCOL_SCHEMA.relative_to(ROOT).as_posix(),
    "protocol schema path",
)
require(
    schemas["protocol_specification"]["sha256"] == digest(PROTOCOL_SCHEMA),
    "protocol schema SHA",
)
require(
    schemas["normalized_obligation_instance"]["path"]
    == INSTANCE_SCHEMA.relative_to(ROOT).as_posix(),
    "instance schema path",
)
require(
    schemas["normalized_obligation_instance"]["sha256"]
    == digest(INSTANCE_SCHEMA),
    "instance schema SHA",
)
require(
    protocol_schema["$schema"]
    == "https://json-schema.org/draft/2020-12/schema",
    "protocol schema draft",
)
require(
    instance_schema["$schema"]
    == "https://json-schema.org/draft/2020-12/schema",
    "instance schema draft",
)
require(
    set(contract["protocol_specification"]["required_top_level_fields"])
    == set(protocol_schema["required"]),
    "protocol required fields",
)
require(
    instance_schema["properties"]["verdict"]["enum"]
    == ["VALID", "VIOLATION-MUST", "VIOLATION-MAY", "UNKNOWN", None],
    "instance verdict enum",
)
require(
    contract["protocol_specification"]["notation"]
    == "P=(S,s0,A,delta,F,Omega)",
    "protocol notation",
)
require(
    contract["normalized_obligation_instance"]["identity_fields"]
    == [
        "driver_id",
        "resource_identity",
        "rule_id",
        "program_point_or_exit",
        "abstract_context",
    ],
    "normalized identity",
)
require(
    contract["equivalent_path_normalization"]
    ["raw_paths_counted_as_independent_samples"] is False,
    "raw path independence",
)
require(
    contract["eligibility_contract"]
    ["recorded_separately_from_verdict"] is True,
    "eligibility separation",
)
require(
    contract["eligibility_contract"]
    ["out_of_scope_receives_validity_verdict"] is False,
    "out-of-scope verdict",
)

verdicts = contract["verdict_contract"]
require(
    verdicts["base_outcomes"] == ["VALID", "VIOLATION", "UNKNOWN"],
    "base outcomes",
)
require(
    verdicts["serialized_labels"]
    == ["VALID", "VIOLATION-MUST", "VIOLATION-MAY", "UNKNOWN"],
    "serialized labels",
)
require(verdicts["unknown_is_valid"] is False, "UNKNOWN treated valid")
require(
    verdicts["unknown_on_eligible_gold_primary_scoring"] == "INCORRECT",
    "UNKNOWN scoring",
)

taxonomy = contract["defect_taxonomy"]
require(list(taxonomy) == [f"D{i}" for i in range(1, 9)], "D1-D8")

unknown_codes = [
    item["code"] for item in contract["unknown_limitation_codes"]
]
require(len(unknown_codes) == 7, "UNKNOWN code count")
require(len(set(unknown_codes)) == 7, "duplicate UNKNOWN code")

require(
    contract["leakage_controls"]
    ["held_out_protocols_frozen_before_driver_open_or_annotation"] is True,
    "held-out leakage control",
)

stage = contract["stage_boundaries"]
require(stage["current_stage"] == "Stage A - verification", "stage")
require(stage["primary_generation_authorized"] is False, "generation")
require(stage["held_out_driver_inspection_allowed"] is False, "inspection")
require(stage["analyzer_implementation_authorized_by_gate1a"] is False, "analyzer")
require(stage["repair_implementation_allowed"] is False, "repair")
require(stage["repair_activation_gate"] == "Gate V", "repair gate")

contract_sha = digest(CONTRACT)
report_sha = digest(REPORT)

require(report["status"] == "PASS", "report status")
require(report["contract_sha256"] == contract_sha, "report contract SHA")
require(report["machine_readable_schema_count"] == 2, "schema count")
require(
    report["protocol_schema_sha256"] == digest(PROTOCOL_SCHEMA),
    "report protocol schema SHA",
)
require(
    report["normalized_instance_schema_sha256"] == digest(INSTANCE_SCHEMA),
    "report instance schema SHA",
)
require(report["taxonomy_categories"] == 8, "report taxonomy")
require(report["serialized_verdicts"] == 4, "report verdicts")
require(report["unknown_limitation_codes"] == 7, "report UNKNOWN codes")
require(report["scenario_bindings_created"] == 0, "scenario content created")
require(report["live_api_calls_performed"] == 0, "live calls")
require(report["generated_drivers_created"] == 0, "generated drivers")
require(report["primary_generation_authorized"] is False, "report generation")
require(report["repair_implementation_allowed"] is False, "report repair")

gate1 = lock["gate1_foundation"]
gate1a = gate1["gate1a_obligation_contract"]
require(gate1["status"] == "IN_PROGRESS", "Gate 1 foundation status")
require(gate1a["status"] == "PASS", "Gate 1A status")
require(gate1a["contract_path"] == CONTRACT.relative_to(ROOT).as_posix(), "lock path")
require(gate1a["contract_sha256"] == contract_sha, "lock contract SHA")
require(gate1a["report_path"] == REPORT.relative_to(ROOT).as_posix(), "report path")
require(gate1a["report_sha256"] == report_sha, "lock report SHA")
require(
    gate1a["protocol_schema_sha256"] == digest(PROTOCOL_SCHEMA),
    "lock protocol schema SHA",
)
require(
    gate1a["normalized_instance_schema_sha256"] == digest(INSTANCE_SCHEMA),
    "lock instance schema SHA",
)
require(gate1["primary_generation_authorized"] is False, "lock generation")
require(gate1["held_out_driver_inspection_allowed"] is False, "lock inspection")
require(gate1["repair_implementation_allowed"] is False, "lock repair")

current = lock["current_status"]
require(current["gate_0"] == "PASS", "Gate 0 status")
require(current["gate_1"] == "IN_PROGRESS", "Gate 1 status")
require(current["gate_1a_obligation_contract"] == "PASS", "Gate 1A current status")
require(lock["stage_policy"]["repair_implementation_allowed"] is False, "stage repair")

print("GATE1A_OBLIGATION_CONTRACT=PASS")
print("PROTOCOL_FORMALISM=P_S_s0_A_delta_F_Omega")
print("PRIMARY_UNIT=NORMALIZED_PROTOCOL_OBLIGATION")
print("MACHINE_READABLE_SCHEMAS=2")
print("DEFECT_CATEGORIES=8")
print("SERIALIZED_VERDICTS=4")
print("UNKNOWN_LIMITATION_CODES=7")
print("RAW_CFG_PATHS_INDEPENDENT_SAMPLES=NO")
print("LIBRARY_SPECIFIC_RULES_CREATED=NO")
print("SCENARIO_BINDINGS_CREATED=0")
print("LIVE_API_CALLS_PERFORMED=NO")
print("GENERATION_AUTHORIZED=NO")
print("HELD_OUT_DRIVER_INSPECTION_ALLOWED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"CONTRACT_SHA256={contract_sha}")
print(f"PROTOCOL_SCHEMA_SHA256={digest(PROTOCOL_SCHEMA)}")
print(f"INSTANCE_SCHEMA_SHA256={digest(INSTANCE_SCHEMA)}")
print(f"REPORT_SHA256={report_sha}")
'''
write_new_text(VERIFIER_REL, verifier, executable=True)

lock_path = ROOT / LOCK_REL
lock = read_json(lock_path)
current = lock["current_status"]
require(current["gate_0"] == "PASS", "Gate 0 is not PASS")
require(current["gate_1"] == "NOT_STARTED", "Gate 1 already started")
require("gate1_foundation" not in lock, "Gate 1 lock already exists")

current["gate_1"] = "IN_PROGRESS"
current["gate_1a_obligation_contract"] = "PASS"
current["milestone"] = (
    "Gate 1A obligation schema and normalization contract complete; "
    "Gate 1 specification foundation remains in progress"
)

lock["gate1_foundation"] = {
    "status": "IN_PROGRESS",
    "gate1a_obligation_contract": {
        "status": "PASS",
        "contract_path": CONTRACT_REL,
        "contract_sha256": contract_sha256,
        "report_path": REPORT_REL,
        "report_sha256": report_sha256,
        "protocol_schema_path": PROTOCOL_SCHEMA_REL,
        "protocol_schema_sha256": protocol_schema_sha256,
        "normalized_instance_schema_path": INSTANCE_SCHEMA_REL,
        "normalized_instance_schema_sha256": instance_schema_sha256,
        "taxonomy_categories": 8,
        "serialized_verdicts": 4,
        "unknown_limitation_codes": 7,
        "raw_cfg_paths_are_independent_samples": False,
    },
    "primary_generation_authorized": False,
    "held_out_driver_inspection_allowed": False,
    "analyzer_implementation_authorized": False,
    "repair_implementation_allowed": False,
    "repair_activation_gate": "Gate V",
}
write_json(lock_path, lock)

status_path = ROOT / STATUS_REL
status_text = status_path.read_text(encoding="utf-8")

old_milestone = (
    "- Current milestone: Gate 0 complete — research design frozen; "
    "Gate 1 specification foundation pending"
)
new_milestone = (
    "- Current milestone: Gate 1A — obligation schema and normalization "
    "contract complete"
)
require(status_text.count(old_milestone) == 1, "status milestone marker")
status_text = status_text.replace(old_milestone, new_milestone, 1)

old_gate1 = "- Gate 1: NOT STARTED"
new_gate1 = (
    "- Gate 1: IN PROGRESS\n"
    "- Gate 1A obligation schema and normalization contract: PASS"
)
require(status_text.count(old_gate1) == 1, "Gate 1 status marker")
status_text = status_text.replace(old_gate1, new_gate1, 1)

old_next = """## Next authorized work

1. Begin Gate 1 — specification foundation.
2. Freeze protocol-source provenance, the system prompt, and all 80 scenario bindings.
3. Freeze eight library source/build locks and provider price-sheet snapshots.
4. Create a separate committed execution authorization before any primary call.
"""
new_next = """## Next authorized work

1. Continue Gate 1 with the sampling, blind-annotation, adjudication, and exposure-quarantine protocol.
2. Freeze the system prompt and all 80 exact library-specific scenario bindings.
3. Freeze eight library source/build locks and provider price-sheet snapshots.
4. Close Gate 1 with a verified manifest; generation still requires later explicit authorization.
"""
require(status_text.count(old_next) == 1, "next-work marker")
status_text = status_text.replace(old_next, new_next, 1)
status_path.write_text(status_text, encoding="utf-8")

gate0_verifier_path = ROOT / GATE0_FINAL_VERIFIER_REL
gate0_source = gate0_verifier_path.read_text(encoding="utf-8")
old_guard = (
    'require(current["gate_1"] == "NOT_STARTED", '
    '"Gate 1 started early")'
)
new_guard = (
    'require(\n'
    '    current["gate_1"] in {"NOT_STARTED", "IN_PROGRESS", "PASS"},\n'
    '    "Gate 1 lifecycle status",\n'
    ')'
)
require(gate0_source.count(old_guard) == 1, "Gate 0 lifecycle guard")
gate0_source = gate0_source.replace(old_guard, new_guard, 1)
gate0_verifier_path.write_text(gate0_source, encoding="utf-8")

for command in [
    ["python3", "scripts/scan_repository_secrets.py"],
    ["python3", "scripts/verify_gate0c_proposal.py"],
    ["python3", "scripts/verify_gate0d_documentation.py"],
    ["python3", "scripts/verify_gate0d_live.py"],
    ["python3", "scripts/verify_gate0e_analysis.py"],
    ["python3", "scripts/verify_gate0f_generation_protocol.py"],
    ["python3", "scripts/verify_gate0_final_manifest.py"],
    ["python3", "scripts/verify_gate0.py"],
    ["python3", VERIFIER_REL],
    ["git", "diff", "--check"],
]:
    run(command)

require(
    digest(gate0_manifest_path) == EXPECTED_GATE0_MANIFEST_SHA256,
    "Gate 0 final manifest mutated",
)

print("GATE1A_OBLIGATION_CONTRACT_PREPARATION=PASS")
print("GATE0_IMMUTABLE_INPUTS_MUTATED=NO")
print("GATE1_STATUS=IN_PROGRESS")
print("GATE1A_STATUS=PASS")
print("LIBRARY_SPECIFIC_RULES_CREATED=NO")
print("SYSTEM_PROMPT_CREATED=NO")
print("SCENARIO_BINDINGS_CREATED=0")
print("LIVE_API_CALLS_PERFORMED=NO")
print("GENERATION_AUTHORIZED=NO")
print("HELD_OUT_DRIVER_INSPECTION_ALLOWED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"CONTRACT_SHA256={contract_sha256}")
print(f"PROTOCOL_SCHEMA_SHA256={protocol_schema_sha256}")
print(f"INSTANCE_SCHEMA_SHA256={instance_schema_sha256}")
print(f"REPORT_SHA256={report_sha256}")
print("STATUS=")
run(["git", "status", "--short", "--branch"])
