#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "config/protocol_specifications/zlib.json"
SRC = ROOT / "src/semanticverify_clang_cfg_v1/main.cpp"
FIX = ROOT / "tests/semanticverify_clang_cfg_v1/fixtures"

spec = json.loads(SPEC.read_text(encoding="utf-8"))
source = SRC.read_text(encoding="utf-8")
assert "RecursiveASTVisitor" in source
assert "CFG::buildCFG" in source
assert "llvm/Support/JSON.h" in source
assert "U02_UNRESOLVED_ALIAS" in source
assert "U03_UNRESOLVED_INDIRECT_CALL" in source
assert "U04_STATE_CAP_EXHAUSTION" in source
assert "UNVERIFIABLE_NO_DOT_GIT" in source

# No source regex scanner is used as the analyzer mechanism.
for forbidden in ["std::regex", "<regex>", "re.compile("]:
    assert forbidden not in source, forbidden
for hardcoded_api in ["deflateInit", "deflateInit2", "inflateInit", "inflateInit2", "deflateEnd", "inflateEnd", "deflateReset", "inflateReset", "deflateSetDictionary", "inflateCopy"]:
    assert hardcoded_api not in source, f"hard-coded zlib API identity in analyzer: {hardcoded_api}"
for hardcoded_return_constant in ["Z_OK", "Z_STREAM_END"]:
    assert hardcoded_return_constant not in source, f"hard-coded zlib return constant in analyzer: {hardcoded_return_constant}"

# Required development fixtures are zlib-only and use the real header.
fixtures = sorted(FIX.glob("*.c"))
assert len(fixtures) == 22, len(fixtures)
for p in fixtures:
    text = p.read_text(encoding="utf-8")
    assert '#include "zlib.h"' in text

# Fixture API spellings must come from the frozen event table.
symbols = set()
for e in spec["events"]:
    if e["event_kind"] != "API_CALL":
        continue
    head = e["symbol_or_condition"].split(";", 1)[0]
    symbols.update(x.strip() for x in head.split(" or ") if x.strip())
for required in ["deflateInit", "deflate", "deflateEnd", "deflateReset", "inflateInit", "inflate", "inflateEnd", "inflateReset", "inflateCopy", "deflateSetDictionary"]:
    assert required in symbols

# No final held-out library names are referenced by the new analyzer/tests.
joined = source + "\n" + "\n".join(p.read_text(encoding="utf-8") for p in fixtures)
for heldout in ["curl", "cJSON", "libtiff", "libvpx", "c-ares", "lcms"]:
    assert heldout not in joined, heldout

print("STATIC_SPEC_DRIVEN_EVENT_LOADING=PASS")
print("STATIC_NO_REGEX_SOURCE_SCANNER=PASS")
print("STATIC_NO_HARDCODED_ZLIB_API_IDENTITIES=PASS")
print("STATIC_TWENTY_TWO_ZLIB_ONLY_FIXTURES=PASS")
print("STATIC_NO_HELDOUT_REFERENCES=PASS")


# Verify the canonical specification contains the exact initial-slice rules.
rule_ids = {o["rule_id"] for o in spec["obligations"]}
for rule in ["ZLIB-R01", "ZLIB-R02", "ZLIB-R03", "ZLIB-R04", "ZLIB-R07", "ZLIB-R08", "ZLIB-R13"]:
    assert rule in rule_ids, rule
for rule in ["ZLIB-R05", "ZLIB-R06"]:
    assert rule in rule_ids, rule
for rule in ["ZLIB-R10", "ZLIB-R11", "ZLIB-R12", "ZLIB-R14"]:
    assert rule in rule_ids, rule

# Verify event semantic roles can be derived from frozen transitions rather than API-name tables.
by_event = {}
for t in spec["transitions"]:
    by_event.setdefault(t["event_id"], []).append(t)
event_roles = {}
for e in spec["events"]:
    if e["event_kind"] != "API_CALL":
        continue
    ts = by_event.get(e["event_id"], [])
    has_acquire = any(t["ownership_effect"] == "ACQUIRE" for t in ts)
    has_release = any(t["ownership_effect"] == "RELEASE" for t in ts)
    eq = set()
    ne = set()
    for t in ts:
        pred = t.get("return_predicate") or ""
        if pred.startswith("return == "):
            eq.add(pred[len("return == "):].split()[0].rstrip(";"))
        if pred.startswith("return != "):
            ne.add(pred[len("return != "):].split()[0].rstrip(";"))
    event_symbols = [
        symbol.strip()
        for symbol in e["symbol_or_condition"]
            .split(";", 1)[0].split(" or ")
        if symbol.strip()
    ]
    has_ordering_rule = any(
        obligation["defect_category"] == "D6"
        and any(
            symbol in obligation[
                "triggering_event_or_function_exit"
            ]
            for symbol in event_symbols
        )
        for obligation in spec["obligations"]
    )
    all_ownership_preserving = (
        bool(ts)
        and all(
            t["ownership_effect"] == "NONE"
            for t in ts
        )
    )
    all_state_preserving = (
        bool(ts)
        and all(
            t["from_states"] == t["to_states"]
            for t in ts
        )
    )

    if has_acquire:
        role = "init"
    elif has_release:
        role = "end"
    elif eq & ne:
        role = "use"
    elif (
        len(ts) > 1
        and has_ordering_rule
        and all_ownership_preserving
        and all_state_preserving
    ):
        role = "ordered_configuration"
    elif len(ts) == 1:
        role = "state_transition"
    else:
        role = "unsupported_current_slice"
    event_roles[e["event_id"]] = role
assert sum(v == "init" for v in event_roles.values()) >= 2
assert sum(v == "end" for v in event_roles.values()) >= 2
assert sum(v == "use" for v in event_roles.values()) >= 2
assert sum(v == "ordered_configuration" for v in event_roles.values()) == 1
assert sum(v == "state_transition" for v in event_roles.values()) == 2
print("STATIC_INITIAL_SLICE_RULES_PRESENT=PASS")
print("STATIC_MILESTONE2_R05_R06_RULES_PRESENT=PASS")
print("STATIC_MILESTONE3_R10_R12_RULES_PRESENT=PASS")
print("STATIC_MILESTONE4_R14_RULE_PRESENT=PASS")
print("STATIC_MILESTONE5_R11_RULE_PRESENT=PASS")
print("STATIC_EVENT_ROLES_DERIVED_FROM_FROZEN_TRANSITIONS=PASS")
