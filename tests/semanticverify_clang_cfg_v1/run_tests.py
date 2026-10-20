#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

EXPECTED_SPEC_SHA256 = "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1"
EXPECTED_SOURCE_LOCK_SHA256 = "2be6bd713ce179bdc7f66e67ba1108f4bca5383372bbe653ac924cc290ab7f0e"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_analyzer(analyzer: Path, spec: Path, contract: Path, fixture: Path,
                 zlib_include: Path, clang_resource_dir: Path) -> tuple[str, dict]:
    cmd = [
        str(analyzer),
        f"--spec={spec}",
        f"--contract={contract}",
        "--state-cap=64",
        f"--extra-arg-before=-resource-dir={clang_resource_dir}",
        str(fixture),
        "--",
        "-std=c11",
        f"-I{zlib_include}",
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise AssertionError(
            f"analyzer failed rc={p.returncode}\nCOMMAND={' '.join(cmd)}\n"
            f"STDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}"
        )
    lines = [x for x in p.stdout.splitlines() if x.strip()]
    if len(lines) != 1:
        raise AssertionError(f"expected one JSON line, got {len(lines)}\n{p.stdout}")
    return lines[0], json.loads(lines[0])


def event_map(spec: dict) -> dict[str, str]:
    out = {}
    for e in spec["events"]:
        if e["event_kind"] != "API_CALL":
            continue
        head = e["symbol_or_condition"].split(";", 1)[0]
        for part in head.split(" or "):
            symbol = part.strip()
            if symbol:
                out[symbol] = e["event_id"]
    return out


def find_call(obj: dict, event_id: str):
    return [c for c in obj["calls"] if c["event_id"] == event_id]


def judgments(obj: dict, *, event_id=None, resource_id=None, rule_id=None):
    out = []
    for j in obj["judgments"]:
        if event_id is not None and j["event_id"] != event_id:
            continue
        if resource_id is not None and j["resource_id"] != resource_id:
            continue
        if rule_id is not None and rule_id not in j["rule_ids"]:
            continue
        out.append(j)
    return out


def assert_verdict(obj, verdict, *, rule_id=None, event_id=None, resource_id=None):
    js = judgments(obj, event_id=event_id, resource_id=resource_id, rule_id=rule_id)
    if not any(j["verdict"] == verdict for j in js):
        raise AssertionError(
            f"expected verdict={verdict} rule={rule_id} event={event_id} resource={resource_id}; "
            f"observed={[(j['verdict'], j['rule_ids'], j['event_id'], j['resource_id']) for j in obj['judgments']]}"
        )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analyzer", type=Path)
    ap.add_argument("--repo-root", required=True, type=Path)
    ap.add_argument("--zlib-include", required=True, type=Path)
    ap.add_argument("--clang-resource-dir", type=Path)
    ap.add_argument("--preflight-only", action="store_true")
    ns = ap.parse_args()

    root = ns.repo_root.resolve()
    spec_path = root / "config/protocol_specifications/zlib.json"
    contract_path = root / "config/protocol_obligation_contract.json"
    source_lock_path = root / "config/library_source_build_lock.json"
    fixture_dir = root / "tests/semanticverify_clang_cfg_v1/fixtures"

    assert sha256(spec_path) == EXPECTED_SPEC_SHA256
    assert sha256(source_lock_path) == EXPECTED_SOURCE_LOCK_SHA256

    spec = load_json(spec_path)
    source_lock = load_json(source_lock_path)
    zlib_lock = [x for x in source_lock["libraries"] if x["name"] == "zlib"]
    assert len(zlib_lock) == 1
    assert zlib_lock[0]["source"]["peeled_commit"] == spec["library_revision"]
    assert source_lock["build_environment"]["clang"] == "14.0.0"

    header_record = [x for x in spec["provenance"] if x["evidence_id"] == "EV-ZLIB-H-001"]
    assert len(header_record) == 1
    pinned_header = ns.zlib_include / "zlib.h"
    assert pinned_header.is_file(), f"pinned zlib.h missing: {pinned_header}"
    assert sha256(pinned_header) == header_record[0]["content_sha256"], (
        f"zlib.h hash mismatch: got={sha256(pinned_header)} "
        f"expected={header_record[0]['content_sha256']}"
    )

    if ns.preflight_only:
        print("PREFLIGHT_SPEC_SHA256=PASS")
        print("PREFLIGHT_SOURCE_LOCK_SHA256=PASS")
        print("PREFLIGHT_ZLIB_REVISION_BINDING=PASS")
        print("PREFLIGHT_CLANG_LOCK_VERSION=14.0.0")
        print("PREFLIGHT_PINNED_ZLIB_HEADER_SHA256=PASS")
        return 0

    if ns.analyzer is None:
        raise SystemExit("--analyzer is required unless --preflight-only is used")
    if ns.clang_resource_dir is None:
        raise SystemExit(
            "--clang-resource-dir is required unless --preflight-only is used"
        )
    resource_stddef = ns.clang_resource_dir / "include" / "stddef.h"
    if not resource_stddef.is_file():
        raise SystemExit(
            f"Clang resource header missing: {resource_stddef}"
        )

    emap = event_map(spec)
    required_symbols = ["deflateInit", "deflate", "deflateEnd", "inflateInit", "inflate", "inflateEnd"]
    for sym in required_symbols:
        assert sym in emap, f"canonical spec lacks required development symbol: {sym}"

    cases = {}
    for fixture in sorted(fixture_dir.glob("*.c")):
        out1, obj1 = run_analyzer(
            ns.analyzer, spec_path, contract_path, fixture,
            ns.zlib_include, ns.clang_resource_dir,
        )
        out2, obj2 = run_analyzer(
            ns.analyzer, spec_path, contract_path, fixture,
            ns.zlib_include, ns.clang_resource_dir,
        )
        assert out1 == out2, f"nondeterministic JSON: {fixture.name}"
        assert obj1 == obj2
        assert obj1["schema_version"] == "1.0.0"
        assert obj1["development_snapshot_git_head"] == "UNVERIFIABLE_NO_DOT_GIT"
        assert obj1["claimed_authoritative_head"] is False
        assert obj1["final_repository_evidence"] is False
        assert obj1["specification"]["library_revision"] == spec["library_revision"]
        assert obj1["functions"], f"no in-scope functions: {fixture.name}"
        assert any(f["cfg_built"] for f in obj1["functions"]), f"CFG absent: {fixture.name}"
        assert any(f["blocks"] for f in obj1["functions"]), f"CFG blocks absent: {fixture.name}"
        for c in obj1["calls"]:
            assert c["source_location"]["line"] > 0
            assert c["source_location"]["column"] > 0
            assert c["cfg_block_id"] >= 0
        for j in obj1["judgments"]:
            assert j["cfg_block_path"], f"missing CFG witness path: {fixture.name} {j}"
            assert j["witness"] or j["event_id"] == "E11_FUNCTION_EXIT"
        cases[fixture.name] = obj1

    # AST/event extraction and return-variable/resource identity.
    d = cases["01_correct_deflate.c"]
    init_calls = find_call(d, emap["deflateInit"])
    assert init_calls and init_calls[0]["assigned_return_variable"] == "rc"
    assert init_calls[0]["resource_identity"] == "local:strm"
    assert init_calls[0]["arguments"]
    assert any(b["successors"] for f in d["functions"] for b in f["blocks"])

    i = cases["02_correct_inflate.c"]
    init_calls = find_call(i, emap["inflateInit"])
    assert init_calls and init_calls[0]["assigned_return_variable"] == "rc"
    assert init_calls[0]["resource_identity"] == "local:strm"

    # Init-before-use and failed-init branch refinement.
    assert_verdict(cases["03_use_before_init.c"], "VIOLATION-MUST", rule_id="ZLIB-R01")
    assert_verdict(cases["04_use_on_init_failure_branch.c"], "VIOLATION-MUST", rule_id="ZLIB-R03")
    assert_verdict(cases["09_inflate_use_on_init_failure_branch.c"], "VIOLATION-MUST", rule_id="ZLIB-R04")

    # Released-state lifecycle violations for both protocol families.
    assert_verdict(cases["10_deflate_use_after_end.c"], "VIOLATION-MUST", rule_id="ZLIB-R05")
    assert_verdict(cases["11_inflate_use_after_end.c"], "VIOLATION-MUST", rule_id="ZLIB-R05")
    assert_verdict(cases["12_double_deflate_end.c"], "VIOLATION-MUST", rule_id="ZLIB-R06")
    assert_verdict(cases["13_double_inflate_end.c"], "VIOLATION-MUST", rule_id="ZLIB-R06")

    # Stream-end ordering and ownership-preserving reset semantics.
    assert_verdict(cases["14_deflate_after_stream_end.c"], "VIOLATION-MUST", rule_id="ZLIB-R10")
    assert_verdict(cases["15_deflate_reset_before_init.c"], "VIOLATION-MUST", rule_id="ZLIB-R12")
    assert_verdict(cases["16_inflate_reset_before_init.c"], "VIOLATION-MUST", rule_id="ZLIB-R12")
    assert_verdict(cases["17_valid_deflate_reset.c"], "VALID", rule_id="ZLIB-R12")
    assert_verdict(cases["18_valid_inflate_reset.c"], "VALID", rule_id="ZLIB-R12")

    # inflateCopy must not overwrite a live destination.
    assert_verdict(
        cases["19_inflate_copy_over_live_destination.c"],
        "VIOLATION-MUST",
        rule_id="ZLIB-R14",
        resource_id="local:destination",
    )

    # Dictionary ordering.
    assert_verdict(
        cases["20_valid_deflate_dictionary_ready.c"],
        "VALID",
        rule_id="ZLIB-R11",
        resource_id="local:stream",
    )
    assert_verdict(
        cases["21_deflate_dictionary_before_init.c"],
        "VIOLATION-MUST",
        rule_id="ZLIB-R11",
        resource_id="local:stream",
    )

    active_dictionary = judgments(
        cases[
            "22_deflate_dictionary_active_requires_raw_evidence.c"
        ],
        event_id="E05_DEFLATE_SET_DICTIONARY",
        resource_id="local:stream",
        rule_id="ZLIB-R11",
    )
    assert any(
        j["verdict"] == "UNKNOWN"
        and "U01_UNSUPPORTED_SEMANTICS"
            in j["limitation_codes"]
        for j in active_dictionary
    ), active_dictionary
    assert not any(
        j["verdict"] == "VALID"
        for j in active_dictionary
    ), active_dictionary

    # Cleanup obligations and path quantification.
    assert_verdict(cases["05_missing_cleanup_one_exit.c"], "VIOLATION-MAY", rule_id="ZLIB-R07", resource_id="local:strm")
    assert_verdict(cases["06_cleanup_all_exits.c"], "VALID", rule_id="ZLIB-R07", resource_id="local:strm")

    # Independent resources.
    two = cases["07_two_independent_streams.c"]
    assert any(c["resource_identity"] == "local:a" for c in two["calls"])
    assert any(c["resource_identity"] == "local:b" for c in two["calls"])
    assert_verdict(two, "VALID", rule_id="ZLIB-R07", resource_id="local:a")
    assert_verdict(two, "VALID", rule_id="ZLIB-R07", resource_id="local:b")

    # Unsupported alias/wrapper must never silently become VALID.
    u = cases["08_unsupported_alias_wrapper.c"]
    assert any(l["code"] in {"U01_UNSUPPORTED_SEMANTICS", "U02_UNRESOLVED_ALIAS"} for l in u["limitations"])
    assert any(j["verdict"] == "UNKNOWN" for j in u["judgments"]), u["judgments"]

    print("TEST_AST_CALL_EXTRACTION=PASS")
    print("TEST_CFG_BLOCKS_EDGES=PASS")
    print("TEST_RETURN_VARIABLE_BINDING=PASS")
    print("TEST_RESOURCE_IDENTITY=PASS")
    print("TEST_BRANCH_REFINEMENT=PASS")
    print("TEST_RELEASED_STATE_VIOLATIONS=PASS")
    print("TEST_STREAM_END_AND_RESET_ORDERING=PASS")
    print("TEST_INFLATE_COPY_DESTINATION_OVERWRITE=PASS")
    print("TEST_DEFLATE_DICTIONARY_ORDERING=PASS")
    print("TEST_CLEANUP_MULTIPLE_EXITS=PASS")
    print("TEST_MUST_MAY_UNKNOWN=PASS")
    print("TEST_DETERMINISTIC_JSON=PASS")
    print("TEST_WITNESS_SOURCE_LOCATIONS=PASS")
    print("TEST_PINNED_ZLIB_HEADER_IDENTITY=PASS")
    print("TEST_CLANG_RESOURCE_DIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
