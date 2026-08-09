#!/usr/bin/env python3

import json
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "config/primary_postprocessing_contract.v1.json"
DECISION = ROOT / "documentation/decisions/0010-primary-postprocessing-precedence-and-duplicate-semantics.md"
PROTOCOL = ROOT / "config/generation_execution_protocol.json"

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def main():
    failures = []

    def check(name, ok, detail=""):
        print(
            "CHECK|{}|{}{}".format(
                name,
                "PASS" if ok else "FAIL",
                "|" + str(detail) if detail else ""
            )
        )
        if not ok:
            failures.append(name)

    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    d = DECISION.read_text(encoding="utf-8")

    check(
        "CONTRACT_ID",
        c["contract_id"] == "SVF-PRIMARY-POSTPROCESSING-V1"
    )

    check(
        "DECISION_REFERENCE",
        c["decision_reference"]["decision_id"] == "0010"
    )

    check(
        "STATUS_VOCABULARY",
        set(c["compilation_status_mapping"]) ==
        set(p["terminal_status_contract"]["statuses"])
    )

    check(
        "EXACTLY_ONE_TERMINAL",
        c["terminal_status_assignment"][
            "exactly_one_terminal_status_per_logical_slot"
        ] is True
    )

    check(
        "DUPLICATE_SCOPE",
        c["duplicate_policy"]["scope_fields"] == [
            "requested_model_id",
            "library",
            "scenario_id"
        ]
    )

    check(
        "DUPLICATE_NOT_COMPILED",
        c["duplicate_policy"]["duplicate_output_compiled"] is False
    )

    check(
        "DUPLICATE_NOT_REPLACED",
        c["duplicate_policy"]["duplicate_slot_replaced"] is False
    )

    check(
        "FIXED_800_DENOMINATOR",
        c["duplicate_policy"][
            "duplicate_slot_remains_in_fixed_800_denominator"
        ] is True
    )

    check(
        "SUCCESS_MAPPING",
        c["compilation_status_mapping"]["RESPONSE_RECEIVED"] == "COMPILED"
    )

    check(
        "FAILURE_MAPPING",
        c["compilation_status_mapping"]["NON_COMPILATION"]
        == "NON_COMPILATION"
    )

    check(
        "VERBATIM_SOURCE",
        c["extraction"]["provider_model_text_preserved_verbatim"] is True
    )

    check(
        "NO_SOURCE_REPAIR",
        c["compilation"]["source_repair_allowed"] is False
    )

    check(
        "NO_ENTRYPOINT_REQUIREMENT",
        c["compilation"]["entrypoint_requirement"] == "NONE"
    )

    check(
        "NO_EXECUTION",
        c["compilation"]["execute_linked_output"] is False
    )

    check(
        "NO_SANITIZERS",
        c["compilation"]["sanitizers_enabled"] is False
    )

    check(
        "NO_LIBFUZZER",
        c["compilation"]["libfuzzer_enabled"] is False
    )

    check(
        "EIGHT_LIBRARIES",
        len(c["libraries"]) == 8
    )

    for name, cfg in c["libraries"].items():
        artifact = Path(cfg["static_artifact"])

        actual = sha(artifact) if artifact.is_file() else "MISSING"

        check(
            "ARTIFACT_" + name,
            actual == cfg["static_artifact_sha256"],
            actual
        )

        check(
            "INCLUDES_" + name,
            all(Path(x).is_dir() for x in cfg["include_dirs"])
        )

    for name, item in c["input_locks"].items():
        path = ROOT / item["path"]
        actual = sha(path) if path.is_file() else "MISSING"

        check(
            "INPUT_LOCK_" + name,
            actual == item["sha256"],
            actual
        )

    authorized = p["authorization"]["primary_generation_authorized"]
    window = p["execution_window"]["state"]

    check(
        "PRIMARY_GENERATION_UNAUTHORIZED",
        authorized is False
    )

    check(
        "GENERATION_WINDOW_CLOSED",
        window == "FROZEN_NOT_OPEN"
    )

    check(
        "DECISION_DUPLICATE_TERM",
        "DUPLICATE_OUTPUT" in d
    )

    check(
        "DECISION_REPAIR_BOUNDARY",
        "Repair remains prohibited until Gate V" in d
    )

    print()
    print("CONTRACT_SHA256=" + sha(CONTRACT))
    print("DECISION_0010_SHA256=" + sha(DECISION))
    print("PROTOCOL_SHA256=" + sha(PROTOCOL))
    print("FAIL_COUNT=" + str(len(failures)))

    if failures:
        print("VERIFIER_RESULT=FAIL")
        print("FAILED_CHECKS=" + ",".join(failures))
        return 1

    print("VERIFIER_RESULT=PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
