#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).parent
CORRECTIVE = ROOT / "corrective_successor_exact"

EXPECTED_D0227_MANIFEST_SHA = (
    "db90747fb8f586992c524e5c541a1414bb12349b874ca4fa8a709c4ae0f17ab8"
)

EXPECTED_RETURNED_REVIEW_SHA = (
    "daf3ac553885e3a8547cb48c9271015434d1b0c8f33cc51a3afd083f4e73627e"
)

EXPECTED_ENUM_SHA = (
    "44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12"
)

EXPECTED_TRACE_SHA = (
    "6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4"
)

EXPECTED_D0226_R03_SHA = (
    "c2f87816e6e5b3bf299bec8af9a563959ccced0774dcef3117009e1f3f111bbd"
)

EXPECTED_D0226_SENTINEL_SHA = (
    "784cc8cf4ce1c60915960af1bad8a127213752fdde502559b4581c3c937bf804"
)

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

# ------------------------------------------------------------
# Copied D0227 package must be complete and checksum-valid.
# ------------------------------------------------------------

d0227_manifest = (
    CORRECTIVE /
    "16_governed_corrective_successor_v5.SHA256SUMS"
)

assert d0227_manifest.is_file()
assert sha(d0227_manifest) == EXPECTED_D0227_MANIFEST_SHA

lines = [
    line
    for line in d0227_manifest.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

assert len(lines) == 22

listed = set()

for line in lines:
    digest, rel = line.split("  ", 1)

    path = CORRECTIVE / rel

    assert path.is_file(), rel
    assert sha(path) == digest, rel

    listed.add(rel)

actual = {
    p.relative_to(CORRECTIVE).as_posix()
    for p in CORRECTIVE.rglob("*")
    if p.is_file()
}

assert (
    actual
    == listed | {
        "16_governed_corrective_successor_v5.SHA256SUMS"
    }
)

assert len(actual) == 23

# ------------------------------------------------------------
# Existing source bytes are present in the review package.
# ------------------------------------------------------------

enum = (
    CORRECTIVE /
    "existing_source_copies_exact/"
    "01_semantic_unit_enumeration_source.EXACT_COPY.v1.json"
)

trace = (
    CORRECTIVE /
    "existing_source_copies_exact/"
    "02_semantic_unit_traceability_source.EXACT_COPY.v1.json"
)

assert sha(enum) == EXPECTED_ENUM_SHA
assert sha(trace) == EXPECTED_TRACE_SHA

# ------------------------------------------------------------
# Prior human review exact copy.
# ------------------------------------------------------------

prior = (
    ROOT /
    "04_predecessor_returned_rereview.EXACT_COPY.v1.md"
)

assert sha(prior) == EXPECTED_RETURNED_REVIEW_SHA

prior_text = (
    prior.read_bytes()
    .decode("utf-8")
    .replace("\r\n", "\n")
)

assert prior_text.count("[x] REVISION_REQUIRED") == 3
assert prior_text.count("[x] PASS") == 0

# ------------------------------------------------------------
# D0227 technical candidate semantics.
# ------------------------------------------------------------

delta = json.loads(
    (
        CORRECTIVE /
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

assert (
    delta["next_review_source_packaging"]["enumeration_source_sha256"]
    == EXPECTED_ENUM_SHA
)

assert (
    delta["next_review_source_packaging"]["traceability_source_sha256"]
    == EXPECTED_TRACE_SHA
)

# ------------------------------------------------------------
# D0226 consumption evidence inside copied D0227 candidate.
# ------------------------------------------------------------

consumption = json.loads(
    (
        CORRECTIVE /
        "08_d0226_r03_consumption_record.v1.json"
    ).read_text(encoding="utf-8")
)

assert consumption["r03_sha256"] == EXPECTED_D0226_R03_SHA
assert consumption["execution_attempt_count"] == 1
assert consumption["execution_result"] == "PASS"
assert consumption["state"] == "PERMANENTLY_RETIRED"
assert consumption["rerun_authorized"] is False

assert (
    consumption["sentinel_copy"]["sha256"]
    == EXPECTED_D0226_SENTINEL_SHA
)

# ------------------------------------------------------------
# Blank human review form.
# ------------------------------------------------------------

form = (
    ROOT /
    "01_blank_independent_human_rereview_form.MANUAL_REVIEW_COPY.v1.md"
)

text = form.read_text(encoding="utf-8")

assert "[x]" not in text
assert "[X]" not in text

assert text.count("- [ ] PASS") == 3
assert text.count("- [ ] REVISION_REQUIRED") == 3
assert text.count("- [ ] I confirm") == 1

for field in [
    "Reviewer name:",
    "Reviewer role:",
    "Review date:",
    "Reviewer confirmation / signature:",
]:
    matches = [
        line
        for line in text.splitlines()
        if line.startswith(field)
    ]

    assert len(matches) == 1
    assert matches[0].strip() == field

assert not re.search(
    r"-\s*\[[xX]\]\s*(PASS|REVISION_REQUIRED)",
    text
)

# ------------------------------------------------------------
# Machine-readable D0228 lifecycle.
# ------------------------------------------------------------

meta = json.loads(
    (
        ROOT /
        "02_independent_human_rereview_package_manifest.v1.json"
    ).read_text(encoding="utf-8")
)

assert meta["decision"] == "0228"

assert (
    meta["status"]
    == "BLANK_INDEPENDENT_HUMAN_REREVIEW_PACKAGE_AUTHORED_NOT_HANDED_OFF"
)

assert meta["review_target"]["status"] == "AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR"

assert (
    meta["review_target"]["corrective_successor_manifest_sha256"]
    == EXPECTED_D0227_MANIFEST_SHA
)

assert meta["review_scope"] == ["ASER04", "ASER07"]

assert meta["source_byte_availability"]["enumeration_source_in_package"] is True
assert meta["source_byte_availability"]["traceability_source_in_package"] is True
assert meta["source_byte_availability"]["existing_sources_only"] is True
assert meta["source_byte_availability"]["new_accounting_evidence_acquired"] is False
assert meta["source_byte_availability"]["new_domain_acquired"] is False

assert meta["predecessor_review"]["sha256"] == EXPECTED_RETURNED_REVIEW_SHA
assert meta["predecessor_review"]["ASER04"] == "REVISION_REQUIRED"
assert meta["predecessor_review"]["ASER07"] == "REVISION_REQUIRED"
assert meta["predecessor_review"]["overall"] == "REVISION_REQUIRED"

form_state = meta["reviewer_form_state"]

for key, value in form_state.items():
    assert type(value) is bool
    assert value is False, key

life = meta["lifecycle"]

assert life["review_package_authored"] is True
assert life["external_handoff_authorized"] is False
assert life["external_handoff_export_prepared"] is False
assert life["external_handoff_performed"] is False
assert life["returned_rereview_received"] is False
assert life["returned_rereview_recorded"] is False
assert life["corrective_successor_approved"] is False
assert life["governance_adopted"] is False

for key, value in meta["explicit_nonauthorization"].items():
    assert type(value) is bool
    assert value is False, key

# ------------------------------------------------------------
# Recursive D0228 package manifest.
# ------------------------------------------------------------

manifest = (
    ROOT /
    "07_independent_human_rereview_package.v1.SHA256SUMS"
)

manifest_lines = [
    line
    for line in manifest.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

listed_outer = set()

for line in manifest_lines:
    digest, rel = line.split("  ", 1)

    path = ROOT / rel

    assert path.is_file(), rel
    assert sha(path) == digest, rel

    listed_outer.add(rel)

actual_outer = {
    p.relative_to(ROOT).as_posix()
    for p in ROOT.rglob("*")
    if p.is_file()
}

assert (
    actual_outer
    == listed_outer | {
        "07_independent_human_rereview_package.v1.SHA256SUMS"
    }
)

print("D0228_BLANK_INDEPENDENT_HUMAN_REREVIEW_PACKAGE_VERIFIER=PASS")
print("D0227_EXACT_CORRECTIVE_SUCCESSOR_COPY=PASS")
print("D0227_CORRECTIVE_SUCCESSOR_MANIFEST_BINDING=PASS")
print("EXISTING_ENUMERATION_SOURCE_AVAILABLE_TO_REVIEWER=YES")
print("EXISTING_TRACEABILITY_SOURCE_AVAILABLE_TO_REVIEWER=YES")
print("REVIEW_SCOPE=ASER04,ASER07")
print("ALL_REVIEWER_FIELDS_BLANK=YES")
print("REVIEWER_DECISIONS_PREFILLED=NO")
print("INDEPENDENCE_ATTESTATION_CHECKED=NO")
print("REVIEW_PACKAGE_AUTHORED=YES")
print("EXTERNAL_HANDOFF_AUTHORIZED=NO")
print("EXTERNAL_HANDOFF_EXPORT_PREPARED=NO")
print("EXTERNAL_HANDOFF_PERFORMED=NO")
print("RETURNED_REREVIEW_RECEIVED=NO")
print("RETURNED_REREVIEW_RECORDED=NO")
print("CORRECTIVE_SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTED=NO")
print("D0226_R03_STATE=PERMANENTLY_RETIRED")
print("D0226_R03_RERUN_AUTHORIZED=NO")
print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("ACTUAL_DOMAIN_ACQUISITION_AUTHORIZED=NO")
print("CONCRETE_MAPPING_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
