#!/usr/bin/env python3

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
