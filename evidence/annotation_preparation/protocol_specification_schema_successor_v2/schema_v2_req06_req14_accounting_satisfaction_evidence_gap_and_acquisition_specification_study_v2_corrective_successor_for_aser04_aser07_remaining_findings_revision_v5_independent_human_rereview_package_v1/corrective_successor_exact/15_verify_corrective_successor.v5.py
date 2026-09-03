#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent

EXPECTED = {
    "enum":
        "44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12",

    "trace":
        "6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4",

    "returned":
        "daf3ac553885e3a8547cb48c9271015434d1b0c8f33cc51a3afd083f4e73627e",

    "sentinel":
        "784cc8cf4ce1c60915960af1bad8a127213752fdde502559b4581c3c937bf804",

    "stdout":
        "75688f68b56dc946ed0831a005092cc2910d9274015fddf6b88c5d4e920cfbe3",

    "stderr":
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",

    "pre_canon":
        "ba276c2d35f6bb80c820f79df5366761dc0cbeba8c01e225367fd7f9094d7f1e",

    "pre_order":
        "a0215aae4591e7375b0c8111c07b1293304a6831e048c7a6848ef2a38c52b166",

    "pre_freeze":
        "07dccab7f486edd64a2c222171157283cc4cfac68840edcf42019a869fba168b",

    "pre_verifier":
        "3f41ed8822c57a18ae8787e7f1c14ca712fce62e93153b317a3d0a775c143d30",

    "pre_invariants":
        "b5eff20289388dcb7c551db8100238cb7fffa966b826ae7530819e155797aa7f",
}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def escape_string(value):
    out = ['"']

    for ch in value:
        cp = ord(ch)

        if 0xD800 <= cp <= 0xDFFF:
            raise ValueError("unpaired surrogate forbidden")

        if ch == '"':
            out.append('\\"')

        elif ch == "\\":
            out.append("\\\\")

        elif cp <= 0x1F:
            out.append("\\u%04x" % cp)

        else:
            out.append(ch)

    out.append('"')

    return "".join(out)

def canonical(value):
    if value is None:
        return "null"

    if value is False:
        return "false"

    if value is True:
        return "true"

    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)

    if isinstance(value, str):
        return escape_string(value)

    if isinstance(value, list):
        return "[" + ",".join(canonical(v) for v in value) + "]"

    if isinstance(value, dict):
        for key in value:
            assert isinstance(key, str)

        keys = sorted(
            value.keys(),
            key=lambda k: k.encode("utf-8")
        )

        return (
            "{"
            + ",".join(
                escape_string(k) + ":" + canonical(value[k])
                for k in keys
            )
            + "}"
        )

    raise TypeError(type(value).__name__)

# ------------------------------------------------------------------
# Exact immutable input copies.
# ------------------------------------------------------------------

assert sha(
    ROOT /
    "existing_source_copies_exact/"
    "01_semantic_unit_enumeration_source.EXACT_COPY.v1.json"
) == EXPECTED["enum"]

assert sha(
    ROOT /
    "existing_source_copies_exact/"
    "02_semantic_unit_traceability_source.EXACT_COPY.v1.json"
) == EXPECTED["trace"]

assert sha(
    ROOT /
    "13_returned_rereview.EXACT_COPY.v1.md"
) == EXPECTED["returned"]

assert sha(
    ROOT /
    "09_d0226_r03_consumption_sentinel.EXACT_COPY.v1.json"
) == EXPECTED["sentinel"]

assert sha(
    ROOT /
    "10_d0226_r03_execution_stdout.EXACT_COPY.v1.txt"
) == EXPECTED["stdout"]

assert sha(
    ROOT /
    "11_d0226_r03_execution_stderr.EXACT_COPY.v1.txt"
) == EXPECTED["stderr"]

assert sha(
    ROOT /
    "predecessor_support_exact/"
    "03_accounting_evidence_canonicalization_and_detached_hash_rules.v4.json"
) == EXPECTED["pre_canon"]

assert sha(
    ROOT /
    "predecessor_support_exact/"
    "04_future_domain_freeze_lineage_and_ordering_control.v4.json"
) == EXPECTED["pre_order"]

assert sha(
    ROOT /
    "predecessor_support_exact/"
    "01_complete_domain_freeze_record.schema.v2.json"
) == EXPECTED["pre_freeze"]

assert sha(
    ROOT /
    "predecessor_support_exact/"
    "02_independent_verifier_output_record.schema.v2.json"
) == EXPECTED["pre_verifier"]

assert sha(
    ROOT /
    "predecessor_support_exact/"
    "05_cross_artifact_machine_invariants.v2.json"
) == EXPECTED["pre_invariants"]

# ------------------------------------------------------------------
# D0226 authorization consumption.
# ------------------------------------------------------------------

sentinel = json.loads(
    (
        ROOT /
        "09_d0226_r03_consumption_sentinel.EXACT_COPY.v1.json"
    ).read_text(encoding="utf-8")
)

assert sentinel["execution_attempt_count"] == 1
assert sentinel["execution_result"] == "PASS"
assert sentinel["state"] == "PERMANENTLY_RETIRED"
assert sentinel["rerun_authorized"] is False

assert sentinel["bounded_corrective_successor_authoring_authorized"] is True
assert sentinel["next_rereview_existing_source_copy_packaging_authorized"] is True

# ------------------------------------------------------------------
# Returned human outcome.
# ------------------------------------------------------------------

review_text = (
    ROOT /
    "13_returned_rereview.EXACT_COPY.v1.md"
).read_bytes().decode("utf-8").replace("\r\n", "\n")

assert review_text.count("[x] REVISION_REQUIRED") == 3
assert review_text.count("[x] PASS") == 0

# ------------------------------------------------------------------
# ASER04 exact canonical string contract.
# ------------------------------------------------------------------

canon_contract = json.loads(
    (
        ROOT /
        "02_accounting_evidence_canonicalization_and_detached_hash_rules.v5.json"
    ).read_text(encoding="utf-8")
)

string_rule = canon_contract["canonical_json_string_serialization"]

assert string_rule["canonicalizer_id"] == "SVF_CANONICAL_JSON_UTF8_STRING_V1"
assert string_rule["unicode_normalization"] == "NONE"
assert string_rule["optional_escape_forms_allowed"] is False

assert "\\b, \\t, \\n, \\f, and \\r are forbidden" in (
    string_rule["control_character_rule"]
)

assert "U+002F MUST be emitted unescaped" in string_rule["solidus_rule"]
assert "shortest well-formed UTF-8" in string_rule["non_ascii_rule"]

vectors = json.loads(
    (
        ROOT /
        "03_canonical_json_string_test_vectors.v1.json"
    ).read_text(encoding="utf-8")
)

assert len(vectors["vectors"]) >= 10

seen = set()

for vector in vectors["vectors"]:
    seen.add(vector["id"])

    spellings = vector["source_json_spellings"]

    parsed = [
        json.loads(spelling)
        for spelling in spellings
    ]

    for value in parsed[1:]:
        assert value == parsed[0]

    output = canonical(parsed[0]).encode("utf-8")

    assert output.hex() == vector["expected_canonical_utf8_hex"]

    assert (
        hashlib.sha256(output).hexdigest()
        == vector["expected_sha256"]
    )

    assert (
        output.decode("utf-8")
        == vector["expected_canonical_json_text"]
    )

assert "S01_NEWLINE_EQUIVALENT_ESCAPES" in seen
assert "S07_MEMBER_NAME_NEWLINE_EQUIVALENCE" in seen
assert "S09_COMPOSED_NO_NORMALIZATION" in seen
assert "S10_DECOMPOSED_NO_NORMALIZATION" in seen

composed = next(
    v
    for v in vectors["vectors"]
    if v["id"] == "S09_COMPOSED_NO_NORMALIZATION"
)

decomposed = next(
    v
    for v in vectors["vectors"]
    if v["id"] == "S10_DECOMPOSED_NO_NORMALIZATION"
)

assert (
    composed["expected_canonical_utf8_hex"]
    != decomposed["expected_canonical_utf8_hex"]
)

assert (
    composed["expected_sha256"]
    != decomposed["expected_sha256"]
)

# ------------------------------------------------------------------
# ASER07 strict ordering contract and counterexamples.
# ------------------------------------------------------------------

order = json.loads(
    (
        ROOT /
        "04_future_domain_freeze_lineage_and_ordering_control.v5.json"
    ).read_text(encoding="utf-8")
)

ancestry = order["ancestry_verification"]

assert ancestry["distinct_commit_required"] is True
assert ancestry["required_ancestry_exit_code"] == 0

assert (
    ancestry["checked_freeze_commit"]
    == "complete_freeze_record.freeze_commit"
)

assert (
    ancestry["checked_witness_commit"]
    == "witness_lineage.creation_commit"
)

assert "FAIL even when" in ancestry["same_commit_rule"]

assert ancestry["required_evaluated_commit_keys"] == [
    "freeze_commit",
    "witness_commit",
]

assert set(ancestry["required_check_ids"]) == {
    "STRICT_ORDER_DISTINCT_COMMITS",
    "STRICT_ORDER_FREEZE_ANCESTOR_OF_WITNESS",
    "STRICT_ORDER_FREEZE_COMMIT_BINDING",
    "STRICT_ORDER_WITNESS_COMMIT_BINDING",
}

assert order["freeze_tree_exclusion_condition"]["required"] is False

order_vectors = json.loads(
    (
        ROOT /
        "05_strict_freeze_before_witness_test_vectors.v1.json"
    ).read_text(encoding="utf-8")
)

def evaluate(v):
    ok = (
        v["freeze_commit"] != v["witness_commit"]
        and v["ancestry_exit_code"] == 0
        and v["freeze_commit_binding_matches"] is True
        and v["witness_commit_binding_matches"] is True
    )

    return "PASS" if ok else "FAIL"

ids = set()

for vector in order_vectors["vectors"]:
    ids.add(vector["id"])
    assert evaluate(vector) == vector["expected"]

assert "O01_DISTINCT_ANCESTOR_PASS" in ids
assert "O02_IDENTICAL_COMMIT_COUNTEREXAMPLE" in ids

identical = next(
    v
    for v in order_vectors["vectors"]
    if v["id"] == "O02_IDENTICAL_COMMIT_COUNTEREXAMPLE"
)

assert identical["freeze_commit"] == identical["witness_commit"]
assert identical["ancestry_exit_code"] == 0
assert identical["expected"] == "FAIL"

# ------------------------------------------------------------------
# Cross-artifact invariants.
# ------------------------------------------------------------------

invariants = json.loads(
    (
        ROOT /
        "06_cross_artifact_machine_invariants.v3.json"
    ).read_text(encoding="utf-8")
)

by_id = {
    item["id"]: item
    for item in invariants["invariants"]
}

for required in [
    "H01",
    "H02",
    "L02",
    "L02A",
    "L02B",
    "L03",
    "L04",
    "V01",
    "V02",
    "V03",
]:
    assert required in by_id

assert "!=" in by_id["L02"]["expression"]
assert "is-ancestor" in by_id["L02"]["expression"]
assert "evaluated_commits.freeze_commit" in by_id["L02A"]["expression"]
assert "STRICT_ORDER_DISTINCT_COMMITS" in by_id["L02B"]["expression"]

# ------------------------------------------------------------------
# Source-copy provenance.
# ------------------------------------------------------------------

prov = json.loads(
    (
        ROOT /
        "07_existing_source_copy_provenance.v1.json"
    ).read_text(encoding="utf-8")
)

assert prov["enumeration_source"]["sha256"] == EXPECTED["enum"]
assert prov["traceability_source"]["sha256"] == EXPECTED["trace"]

assert prov["enumeration_source"]["new_domain_acquisition"] is False
assert prov["traceability_source"]["new_accounting_evidence_acquisition"] is False
assert prov["source_content_modified"] is False
assert prov["new_mapping_created"] is False

# ------------------------------------------------------------------
# Corrective delta / governance boundaries.
# ------------------------------------------------------------------

delta = json.loads(
    (
        ROOT /
        "01_corrective_delta_response.v5.json"
    ).read_text(encoding="utf-8")
)

assert delta["status"] == "AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR"
assert delta["corrective_scope"] == ["ASER04", "ASER07"]

assert delta["ASER04_response"]["human_pass_claimed"] is False
assert delta["ASER07_response"]["human_pass_claimed"] is False

assert delta["lifecycle"]["corrective_successor_approved"] is False
assert delta["lifecycle"]["governance_adopted"] is False
assert delta["lifecycle"]["independent_human_rereview_required"] is True

for key, value in delta["explicit_nonauthorization"].items():
    assert type(value) is bool
    assert value is False, key

# ------------------------------------------------------------------
# Recursive package manifest.
# ------------------------------------------------------------------

manifest = (
    ROOT /
    "16_governed_corrective_successor_v5.SHA256SUMS"
)

lines = [
    line
    for line in manifest.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

listed = set()

for line in lines:
    digest, rel = line.split("  ", 1)

    path = ROOT / rel

    assert path.is_file()
    assert sha(path) == digest

    listed.add(rel)

actual = {
    p.relative_to(ROOT).as_posix()
    for p in ROOT.rglob("*")
    if p.is_file()
}

assert (
    actual
    == listed | {
        "16_governed_corrective_successor_v5.SHA256SUMS"
    }
)

print("D0227_CORRECTIVE_SUCCESSOR_VERIFIER=PASS")
print("STATUS=AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR")
print("CORRECTIVE_SCOPE=ASER04,ASER07")
print("ASER04_CANONICAL_JSON_ESCAPING_CONTRACT=PASS")
print("ASER04_CANONICAL_BYTE_HASH_TEST_VECTORS=PASS")
print("ASER07_STRICT_DISTINCT_ANCESTRY_CONTRACT=PASS")
print("ASER07_IDENTICAL_COMMIT_COUNTEREXAMPLE=PASS")
print("ASER07_CHECKED_COMMIT_BINDING_CONTRACT=PASS")
print("EXISTING_ENUMERATION_SOURCE_EXACT_COPY=PASS")
print("EXISTING_TRACEABILITY_SOURCE_EXACT_COPY=PASS")
print("D0226_R03_CONSUMPTION_EVIDENCE=PASS")
print("CORRECTIVE_SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTED=NO")
print("INDEPENDENT_HUMAN_REREVIEW_REQUIRED=YES")
print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("ACTUAL_DOMAIN_ACQUISITION_AUTHORIZED=NO")
print("ACTUAL_DOMAIN_FREEZE_AUTHORIZED=NO")
print("CONCRETE_MAPPING_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
