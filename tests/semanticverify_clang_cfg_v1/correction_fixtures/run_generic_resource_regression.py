#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


def run_case(analyzer, spec, contract, resource_dir, fixture):
    command = [
        str(analyzer),
        f"--spec={spec}",
        f"--contract={contract}",
        "--state-cap=64",
        f"--extra-arg-before=-resource-dir={resource_dir}",
        str(fixture),
        "--",
        "-std=c11",
    ]
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, (fixture.name, completed.returncode, completed.stderr)
    assert not completed.stderr, (fixture.name, completed.stderr)
    return json.loads(completed.stdout)


def call_with_name(document, name):
    matches = [
        call for call in document.get("calls", [])
        if call.get("spelled_callee") == name
        or call.get("qualified_callee") == name
    ]
    assert len(matches) == 1, (name, matches)
    return matches[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--analyzer", required=True, type=Path)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--resource-dir", required=True, type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent

    acquisition = run_case(
        args.analyzer, args.spec, args.contract, args.resource_dir,
        root / "01_generic_return_pointer_acquisition.c",
    )
    acquire_call = call_with_name(acquisition, "deflateInit")
    assert acquire_call["assigned_return_variable"] == "resource", acquire_call
    assert acquire_call["resource_identity"] == "local:resource", acquire_call
    assert acquire_call["resource_expression"] == "resource", acquire_call

    single = run_case(
        args.analyzer, args.spec, args.contract, args.resource_dir,
        root / "02_generic_single_record_pointer_argument.c",
    )
    use_call = call_with_name(single, "deflate")
    assert use_call["resource_identity"] == "local:resource", use_call
    assert use_call["resource_expression"] == "resource", use_call

    ambiguous = run_case(
        args.analyzer, args.spec, args.contract, args.resource_dir,
        root / "03_generic_ambiguous_multi_resource.c",
    )
    ambiguous_call = call_with_name(ambiguous, "deflate")
    assert not ambiguous_call["resource_identity"], ambiguous_call
    assert ambiguous_call["resource_limitation"]["code"] == "U05_MISSING_EVIDENCE", ambiguous_call

    alias = run_case(
        args.analyzer, args.spec, args.contract, args.resource_dir,
        root / "04_generic_parameter_alias_boundary.c",
    )
    alias_call = call_with_name(alias, "deflate")
    assert not alias_call["resource_identity"], alias_call
    assert alias_call["resource_limitation"]["code"] == "U02_UNRESOLVED_ALIAS", alias_call

    print("TEST_GENERIC_RETURN_POINTER_ACQUISITION=PASS")
    print("TEST_GENERIC_SINGLE_RECORD_POINTER_ARGUMENT=PASS")
    print("TEST_GENERIC_AMBIGUOUS_MULTI_RESOURCE=PASS")
    print("TEST_GENERIC_PARAMETER_ALIAS_BOUNDARY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
