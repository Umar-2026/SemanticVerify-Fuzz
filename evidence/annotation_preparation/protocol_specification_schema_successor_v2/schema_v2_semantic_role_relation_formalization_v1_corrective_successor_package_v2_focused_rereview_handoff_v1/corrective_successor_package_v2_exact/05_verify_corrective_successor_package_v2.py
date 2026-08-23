#!/usr/bin/env python3

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SRC = ROOT / "source_evidence"
FORM = ROOT / "formalization_v1_exact"
REVIEW = ROOT / "review_package_v1_exact"
HUMAN = ROOT / "completed_human_review_v1_exact"
AUTH = ROOT / "decision_0095_authorization_exact"
DECISIONS = ROOT / "governance_decisions_exact"

MANIFEST = ROOT / "01_corrective_successor_package_v2_manifest.json"
ERRATUM_JSON = ROOT / "02_srr04_lexical_accounting_erratum.v2.json"
ERRATUM_MD = ROOT / "03_srr04_lexical_accounting_erratum.v2.md"
REREVIEW = ROOT / "04_focused_rereview_packet.BLANK.v2.md"
CONSUMED = ROOT / "06_decision_0095_authorization_verifier_consumed.v1.json"
SUMS = ROOT / "07_corrective_successor_package_v2.SHA256SUMS"

UNIT = SRC / "02_v4_semantic_unit_inventory.v1.json"
CARRIER = SRC / "03_schema_v2_carrier_inventory.v1.json"
MATRIX = SRC / "04_candidate_multifield_composition_matrix.v1.json"

F01 = FORM / "01_schema_v2_semantic_role_relation_formalization.v1.json"
F02 = FORM / "02_v4_field_class_to_schema_v2_property_path_relation.v1.json"
F03 = FORM / "03_v4_semantic_unit_context_and_leaf_traceability.v1.json"
F04 = FORM / "04_schema_v2_semantic_role_relation_formalization.v1.md"
F05 = FORM / "05_pre_formalization_authorization_verifier_consumed.v1"
F06 = FORM / "06_verify_schema_v2_semantic_role_relation_formalization.v1.py"
F07 = FORM / "07_schema_v2_semantic_role_relation_formalization.v1.SHA256SUMS"

H01 = HUMAN / "01_completed_srr01_srr08_human_review.EXACT_COPY.v1.md"
H02 = HUMAN / "02_completed_srr01_srr08_human_review_record.v1.json"
H03 = HUMAN / "03_verify_repository_completed_srr01_srr08_human_review.v1.py"
H04 = HUMAN / "04_completed_srr01_srr08_human_review.v1.SHA256SUMS"

A01 = AUTH / "01_corrective_successor_package_v2_authorization.v1.json"
A02 = AUTH / "02_verify_corrective_successor_package_v2_authorization.v1.py"
A03 = AUTH / "03_corrective_successor_package_v2_authorization.v1.SHA256SUMS"
A04 = AUTH / "04_final_allowed_authorization_verifier_output.v1.txt"

EXPECTED = {
    UNIT:
        "2b39f5625658e41aeb906a1db8a4a472d9265dc3654572e60374827f0ce7fa7d",

    CARRIER:
        "0f32fb87e1396da8c37e3f74c41059560338346ae54f29df0c2d38d72deb1d6d",

    MATRIX:
        "c064cfa8c7143b537dc3bb54b8af353f56bafba3e415e7ccdb2c17efaff30d45",

    F01:
        "0efc848991f0f1580542b8d6e380c55df6d2b370147f236800621b24b51ee600",

    F02:
        "239e6492faca3bb6da0c79abdb980470e2ea76690fc1f081562ccdbf7f303a32",

    F03:
        "6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4",

    F04:
        "7b71d98c63afabc6d3b5eaf72f07e0ee2e4a6707520d80032a9d51b9540878d4",

    F05:
        "55005f555ec580c0e623033137930fa976412aa48dc0acaddc49e767d87bb391",

    F06:
        "842763889dd0958a39b9403832c97d2ea83cbbf8c91bc529931323f3e62f38b0",

    F07:
        "46cbb87c47ce4332c98a80bd769346129d7a54f5cb6aa037d62a7016025e45f6",

    REVIEW / "15_semantic_role_relation_formalization_v1_reviewer_packet.BLANK.v1.md":
        "84aa233232268866aaf9a5b8db673ed1c42e0519c7231162dece7f53a7c4ad3b",

    REVIEW / "16_verify_semantic_role_relation_formalization_v1_review_package.v1.py":
        "4ebef4df999fd0b9b506b7c4e6a9d52c30804dce58f3bb9f63d8e30ce34a831f",

    REVIEW / "17_semantic_role_relation_formalization_v1_review_package_manifest.v1.json":
        "ae8e4af6affc156e7774b61d9a360a9b630034b6d25f2fe37d620cf6c73e2ba5",

    REVIEW / "18_semantic_role_relation_formalization_v1_review_package.v1.SHA256SUMS":
        "75c40450b8a398b077c0214e16da0a20fa089e8c991a56b1bdf92d5d5fc623a1",

    H01:
        "4504b8fd74e8bd699fcdb4b600f72f706d429cee7126bc432bfe7adb1b9ba9f1",

    H02:
        "d6b0d58c6adf3ba6b5b2ad848b4ef5469c213e8b37b0bd66284ed2b437b6b106",

    H03:
        "776a8369ab658fa3f63481c6f7305c5ae5746ad031718a48bce88c3749dc32fb",

    H04:
        "f400d2faa36f5837ae8adf3e5473f78a5fb06728b1118d311db25deabb5a29f6",

    A01:
        "9555633555ed0eb918b27d877d7e8f0c2568847e3570a15919e998a27e91533e",

    A02:
        "4c4a1feca0496055035e57389f0c581542e97ac72a46d10137f657208743093b",

    A03:
        "08918d9f551ff6869b0ac96ccf95037158519ecbdd9f84623b2a041916bb8c71",

    DECISIONS / "0090-record-schema-v2-semantic-role-relation-formalization-v1-author-checkpoint.md":
        "96c5a9719101bf384022b7d8378df1a5e60abf0cb096ea5d9cbcd03be4e2a8b4",

    DECISIONS / "0093-record-recovered-schema-v2-semantic-role-relation-formalization-v1-independent-human-review-package.md":
        "c353fce2180df00cffc183cc536d2707bce870ae4bd86a1351fe5a24ab586355",

    DECISIONS / "0094-record-completed-revision-required-human-review-of-schema-v2-semantic-role-relation-formalization-v1.md":
        "8d18d8fa5c1c16e2f3502ba63abcd21b245b1ebe577c4c546586b343cd14812c",

    DECISIONS / "0095-authorize-evidence-only-corrective-successor-package-v2-for-schema-v2-semantic-role-relation-formalization-v1.md":
        "1391132c706286a975f4c9b4720d85adab842b26acc30ac9a082c69979e3308f",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_sumfile(root, sumfile):
    if not sumfile.is_file():
        fail("SUMFILE_MISSING|" + str(sumfile))

    count = 0

    for raw in sumfile.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue

        parts = raw.split(None, 1)

        if len(parts) != 2:
            fail("MALFORMED_SUM_LINE|" + raw)

        digest = parts[0]
        rel = parts[1].strip()

        if rel.startswith("*"):
            rel = rel[1:]

        target = (root / rel).resolve()

        try:
            target.relative_to(root.resolve())
        except ValueError:
            fail("SUM_PATH_ESCAPE|" + rel)

        actual = sha(target)

        if actual != digest:
            fail(
                "SUM_MISMATCH|"
                + rel
                + "|EXPECTED="
                + digest
                + "|ACTUAL="
                + actual
            )

        count += 1

    if count < 1:
        fail("EMPTY_SUMFILE|" + str(sumfile))

    return count

# ------------------------------------------------------------
# Package must be path-local and self-contained.
# ------------------------------------------------------------

script_text = Path(__file__).read_text(encoding="utf-8")

absolute_path_prefix = "/" + "openbayes" + "/"

if absolute_path_prefix in script_text:
    fail("SAFE_VERIFIER_CONTAINS_OPENBAYES_ABSOLUTE_PATH")

# ------------------------------------------------------------
# Exact immutable bindings.
# ------------------------------------------------------------

for path, expected in EXPECTED.items():
    actual = sha(path)

    if actual != expected:
        fail(
            "EXACT_BINDING|"
            + str(path.relative_to(ROOT))
            + "|ACTUAL="
            + actual
        )

formalization_sum_count = verify_sumfile(FORM, F07)

review_sum_count = verify_sumfile(
    REVIEW,
    REVIEW / "18_semantic_role_relation_formalization_v1_review_package.v1.SHA256SUMS",
)

human_sum_count = verify_sumfile(HUMAN, H04)
authorization_sum_count = verify_sumfile(AUTH, A03)

# ------------------------------------------------------------
# Decision-0095 final-run consumption proof.
# ------------------------------------------------------------

consumed = json.loads(
    CONSUMED.read_text(encoding="utf-8")
)

if consumed["authorization_verifier_sha256"] != EXPECTED[A02]:
    fail("CONSUMED_AUTH_VERIFIER_SHA")

if consumed["final_allowed_run_result"] != "PASS":
    fail("FINAL_AUTH_RUN_RESULT")

if consumed["final_allowed_run_performed"] is not True:
    fail("FINAL_AUTH_RUN_FLAG")

if consumed[
    "corrective_successor_package_v2_authoring_started_after_final_run"
] is not True:
    fail("AUTHORING_AFTER_FINAL_RUN")

if consumed["authorization_verifier_permanently_retired"] is not True:
    fail("AUTH_VERIFIER_RETIREMENT")

if consumed["authorization_verifier_must_never_be_rerun"] is not True:
    fail("AUTH_VERIFIER_NEVER_RERUN")

if sha(A04) != consumed["final_allowed_output_sha256"]:
    fail("FINAL_AUTH_OUTPUT_SHA")

if A04.stat().st_size != consumed["final_allowed_output_size_bytes"]:
    fail("FINAL_AUTH_OUTPUT_SIZE")

auth_output = A04.read_text(encoding="utf-8")

if (
    "DECISION_0095_CORRECTIVE_SUCCESSOR_PACKAGE_V2_AUTHORIZATION=PASS"
    not in auth_output
):
    fail("FINAL_AUTH_OUTPUT_PASS_MARKER")

# ------------------------------------------------------------
# Authoritative source domains.
# ------------------------------------------------------------

unit = json.loads(UNIT.read_text(encoding="utf-8"))
carrier = json.loads(CARRIER.read_text(encoding="utf-8"))
matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
relation = json.loads(F02.read_text(encoding="utf-8"))
trace = json.loads(F03.read_text(encoding="utf-8"))

leaf_rows = unit["leaf_fields"]
semantic_units = unit["semantic_units"]
carrier_rows = carrier["property_paths"]
field_analysis = matrix["field_class_analysis"]
unit_analysis = matrix["unit_analysis"]
rel_rows = relation["relations"]

if len(leaf_rows) != 531:
    fail("LEAF_COUNT")

if len(semantic_units) != 109:
    fail("SEMANTIC_UNIT_COUNT")

if len(carrier_rows) != 171:
    fail("CARRIER_PATH_COUNT")

if len(field_analysis) != 57:
    fail("MATRIX_FIELD_CLASS_COUNT")

if len(unit_analysis) != 109:
    fail("MATRIX_UNIT_ANALYSIS_COUNT")

if len(rel_rows) != 9747:
    fail("RELATION_ROW_COUNT")

# ------------------------------------------------------------
# 57 × 171 relation-domain exact binding.
# ------------------------------------------------------------

matrix_classes = {
    row["v4_field_class"]
    for row in field_analysis
}

carrier_paths = {
    row["path"]
    for row in carrier_rows
}

relation_classes = {
    row["v4_matrix_field_class"]
    for row in rel_rows
}

relation_paths = {
    row["schema_v2_property_path"]
    for row in rel_rows
}

relation_pairs = {
    (
        row["v4_matrix_field_class"],
        row["schema_v2_property_path"],
    )
    for row in rel_rows
}

expected_pairs = {
    (field_class, path)
    for field_class in matrix_classes
    for path in carrier_paths
}

if len(matrix_classes) != 57:
    fail("MATRIX_FIELD_CLASS_SET_SIZE")

if len(carrier_paths) != 171:
    fail("CARRIER_PATH_SET_SIZE")

if matrix_classes != relation_classes:
    fail("FIELD_CLASS_DOMAIN_BINDING")

if carrier_paths != relation_paths:
    fail("PROPERTY_PATH_DOMAIN_BINDING")

if relation_pairs != expected_pairs:
    fail("FULL_CARTESIAN_RELATION_BINDING")

if len(relation_pairs) != 9747:
    fail("RELATION_PAIR_UNIQUENESS")

classification_counts = Counter(
    row["classification"]
    for row in rel_rows
)

expected_classification_counts = Counter({
    "SEMANTICALLY_RELATED": 113,
    "NOT_SEMANTICALLY_RELATED": 969,
    "UNRESOLVED": 8665,
})

if classification_counts != expected_classification_counts:
    fail("RELATION_CLASSIFICATION_COUNTS")

# ------------------------------------------------------------
# Two distinct 57-element field-class vocabularies.
# ------------------------------------------------------------

unit_inventory_field_class_vocab = {
    field_class
    for row in semantic_units
    for field_class in row["field_classes"]
}

matrix_field_class_vocab = matrix_classes

if len(unit_inventory_field_class_vocab) != 57:
    fail("UNIT_INVENTORY_FIELD_CLASS_VOCAB_COUNT")

if len(matrix_field_class_vocab) != 57:
    fail("MATRIX_FIELD_CLASS_VOCAB_COUNT")

if unit_inventory_field_class_vocab == matrix_field_class_vocab:
    fail("DISTINCT_57_ELEMENT_VOCABULARIES_COLLAPSED")

# ------------------------------------------------------------
# 531 exact leaf records.
# ------------------------------------------------------------

source_leaf_by_path = {
    row["source_path"]: row
    for row in leaf_rows
}

trace_leaf_rows = trace["reviewed_leaf_fields"]

trace_leaf_by_path = {
    row["source_path"]: row
    for row in trace_leaf_rows
}

if len(source_leaf_by_path) != 531:
    fail("SOURCE_LEAF_PATH_UNIQUENESS")

if len(trace_leaf_by_path) != 531:
    fail("TRACE_LEAF_PATH_UNIQUENESS")

if source_leaf_by_path != trace_leaf_by_path:
    fail("TRACE_531_LEAF_EXACT_BINDING")

# ------------------------------------------------------------
# 109 unit inventory + matrix unit-analysis bindings.
# ------------------------------------------------------------

source_units = {
    row["unit_id"]: row
    for row in semantic_units
}

matrix_units = {
    row["unit_id"]: row
    for row in unit_analysis
}

trace_units = {
    row["unit_id"]: row
    for row in trace["semantic_unit_context_records"]
}

if not (
    len(source_units)
    == len(matrix_units)
    == len(trace_units)
    == 109
):
    fail("UNIT_DOMAIN_COUNTS")

if not (
    set(source_units)
    == set(matrix_units)
    == set(trace_units)
):
    fail("UNIT_ID_DOMAIN_BINDING")

inventory_scalar_fields = (
    "unit_id",
    "source_container",
    "source_path",
    "unit_kind",
    "value_sha256",
    "value_type",
    "leaf_count",
)

matrix_scalar_fields = (
    "unit_id",
    "source_container",
    "candidate_screening_completed",
    "negative_impossibility_proven",
    "positive_exact_mapping_proven",
)

for uid in source_units:
    s = source_units[uid]
    m = matrix_units[uid]
    t = trace_units[uid]

    for key in inventory_scalar_fields:
        if t.get(key) != s.get(key):
            fail(
                "UNIT_INVENTORY_BINDING|"
                + uid
                + "|"
                + key
            )

    for key in matrix_scalar_fields:
        if t.get(key) != m.get(key):
            fail(
                "MATRIX_UNIT_BINDING|"
                + uid
                + "|"
                + key
            )

    if t["inventory_declared_field_classes"] != s["field_classes"]:
        fail(
            "INVENTORY_FIELD_CLASS_BINDING|"
            + uid
        )

    if t["matrix_unit_analysis_field_classes"] != m["field_classes"]:
        fail(
            "MATRIX_FIELD_CLASS_BINDING|"
            + uid
        )

    if (
        t["candidate_schema_v2_carrier_families"]
        != m["candidate_schema_v2_carrier_families"]
    ):
        fail(
            "CANDIDATE_FAMILY_BINDING|"
            + uid
        )

# ------------------------------------------------------------
# Authoritative F03 family -> full carrier-family path map.
# ------------------------------------------------------------

carrier_by_family = {}

for row in carrier_rows:
    carrier_by_family.setdefault(
        row["top_level_family"],
        []
    ).append(
        row["path"]
    )

carrier_by_family = {
    family: sorted(set(paths))
    for family, paths in carrier_by_family.items()
}

for uid, t in trace_units.items():
    families = t["candidate_schema_v2_carrier_families"]

    mapping = t[
        "candidate_family_domain_paths_for_future_screening"
    ]

    if not isinstance(mapping, dict):
        fail(
            "F03_FAMILY_PATH_MAP_TYPE|"
            + uid
        )

    if set(mapping) != set(families):
        fail(
            "F03_FAMILY_PATH_MAP_KEYS|"
            + uid
        )

    for family in families:
        if family not in carrier_by_family:
            fail(
                "F03_FAMILY_ABSENT_FROM_CARRIER|"
                + uid
                + "|"
                + family
            )

        if mapping[family] != carrier_by_family[family]:
            fail(
                "F03_FAMILY_FULL_PATH_LIST_BINDING|"
                + uid
                + "|"
                + family
            )

# ------------------------------------------------------------
# Lexical-only accounting.
# ------------------------------------------------------------

lexical = [
    row
    for row in rel_rows
    if row["reviewed_lexical_only_candidate"] is True
]

lexical_counts = Counter(
    row["classification"]
    for row in lexical
)

if len(lexical) != 125:
    fail("LEXICAL_TOTAL")

if lexical_counts.get("SEMANTICALLY_RELATED", 0) != 0:
    fail("LEXICAL_RELATED")

if lexical_counts.get("UNRESOLVED", 0) != 120:
    fail("LEXICAL_UNRESOLVED")

if lexical_counts.get("NOT_SEMANTICALLY_RELATED", 0) != 5:
    fail("LEXICAL_NEGATIVE")

expected_negative_pairs = {
    (
        "EXPLICIT_GLOBAL_CLEANUP_OBLIGATION",
        "$.semantic_accounting.inventory.exit_obligation_count",
    ),
    (
        "cleanup_obligation_effect",
        "$.semantic_accounting.inventory.exit_obligation_count",
    ),
    (
        "dependent_reasoning_policy",
        "$.semantic_accounting.inventory.representation_policy_field_count",
    ),
    (
        "feasible_state_join_policy",
        "$.semantic_accounting.inventory.representation_policy_field_count",
    ),
    (
        "rule_id",
        "$.semantic_accounting.inventory.rule_count",
    ),
}

actual_negative_pairs = {
    (
        row["v4_matrix_field_class"],
        row["schema_v2_property_path"],
    )
    for row in lexical
    if row["classification"] == "NOT_SEMANTICALLY_RELATED"
}

if actual_negative_pairs != expected_negative_pairs:
    fail("FIVE_LEXICAL_EXPLICIT_NEGATIVE_PAIRS")

# ------------------------------------------------------------
# SRR04 erratum.
# ------------------------------------------------------------

erratum = json.loads(
    ERRATUM_JSON.read_text(encoding="utf-8")
)

if erratum["correction_type"] != "PRESENTATION_ACCOUNTING_ONLY":
    fail("ERRATUM_TYPE")

if erratum["relation_row_reclassification"] is not False:
    fail("ERRATUM_RECLASSIFICATION")

if erratum["relation_row_modification"] is not False:
    fail("ERRATUM_ROW_MODIFICATION")

if erratum["original_report_modification"] is not False:
    fail("ERRATUM_REPORT_MODIFICATION")

basis = erratum["machine_readable_basis"]

if basis != {
    "predicate": "reviewed_lexical_only_candidate == true",
    "total": 125,
    "SEMANTICALLY_RELATED": 0,
    "UNRESOLVED": 120,
    "NOT_SEMANTICALLY_RELATED": 5,
}:
    fail("ERRATUM_ACCOUNTING")

original_sentence = (
    "In particular, 125 lexical-screening-only pairs remain unresolved."
)

if F04.read_text(encoding="utf-8").count(original_sentence) != 1:
    fail("ORIGINAL_REPORT_SENTENCE_BINDING")

corrected = (
    "There are 125 reviewed lexical-only candidate pairs in total: "
    "120 are UNRESOLVED and five semantic_accounting pairs are "
    "NOT_SEMANTICALLY_RELATED; none are SEMANTICALLY_RELATED."
)

if erratum["corrected_statement"] != corrected:
    fail("ERRATUM_CORRECTED_STATEMENT")

if corrected not in ERRATUM_MD.read_text(encoding="utf-8"):
    fail("ERRATUM_MARKDOWN_CORRECTED_STATEMENT")

# ------------------------------------------------------------
# Original completed review remains REVISION_REQUIRED.
# ------------------------------------------------------------

human_record = json.loads(
    H02.read_text(encoding="utf-8")
)

completed_review = human_record["completed_review"]

if completed_review["overall_decision"] != "REVISION_REQUIRED":
    fail("ORIGINAL_HUMAN_REVIEW_OVERALL")

expected_original_decisions = {
    "SRR01": "PASS",
    "SRR02": "REVISION_REQUIRED",
    "SRR03": "PASS",
    "SRR04": "REVISION_REQUIRED",
    "SRR05": "REVISION_REQUIRED",
    "SRR06": "PASS",
    "SRR07": "PASS",
    "SRR08": "REVISION_REQUIRED",
}

if completed_review["decisions"] != expected_original_decisions:
    fail("ORIGINAL_HUMAN_REVIEW_DECISIONS")

# ------------------------------------------------------------
# Focused rereview packet must remain blank.
# ------------------------------------------------------------

text = REREVIEW.read_text(encoding="utf-8")

for rid in (
    "SRR02-C",
    "SRR04-C",
    "SRR05-C",
    "SRR08-C",
):
    section = re.search(
        rf"^## {re.escape(rid)}\b"
        rf"(?P<body>.*?)"
        rf"(?=^## SRR\d{{2}}-C\b|^# Overall focused decision\b)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not section:
        fail("REREVIEW_SECTION|" + rid)

    if not re.search(
        r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):[ \t]*$",
        section.group("body"),
        flags=re.MULTILINE,
    ):
        fail("REREVIEW_ITEM_NOT_BLANK|" + rid)

if not re.search(
    r"^Overall decision "
    r"\(APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2 / "
    r"REVISION_REQUIRED / FAIL\):[ \t]*$",
    text,
    flags=re.MULTILINE,
):
    fail("REREVIEW_OVERALL_NOT_BLANK")

def blank_field(prefix):
    matches = [
        line[len(prefix):]
        for line in text.splitlines()
        if line.startswith(prefix)
    ]

    if len(matches) != 1:
        fail("REREVIEW_FIELD_CARDINALITY|" + prefix)

    if matches[0].strip():
        fail("REREVIEW_FIELD_NOT_BLANK|" + prefix)

blank_field("Human reviewer name:")
blank_field("Human reviewer signature / recorded confirmation:")
blank_field("Human reviewer date:")

roles = [
    line[len("Reviewer role:"):].strip()
    for line in text.splitlines()
    if line.startswith("Reviewer role:")
]

if roles != ["Spec-Technical-Reviewer-1"]:
    fail("REREVIEW_REVIEWER_ROLE")

# ------------------------------------------------------------
# Manifest governance boundaries.
# ------------------------------------------------------------

manifest = json.loads(
    MANIFEST.read_text(encoding="utf-8")
)

if manifest[
    "status"
] != "AUTHOR_CANDIDATE_AWAITING_FOCUSED_INDEPENDENT_HUMAN_REREVIEW":
    fail("PACKAGE_STATUS")

if manifest["source_review_overall_decision"] != "REVISION_REQUIRED":
    fail("MANIFEST_SOURCE_REVIEW")

if manifest["formalization_v1_approved"] is not False:
    fail("FORMALIZATION_APPROVAL")

if manifest["focused_corrective_items"] != [
    "SRR02-C",
    "SRR04-C",
    "SRR05-C",
    "SRR08-C",
]:
    fail("FOCUSED_ITEMS")

if manifest["carried_forward_pass_items"] != [
    "SRR01",
    "SRR03",
    "SRR06",
    "SRR07",
]:
    fail("CARRIED_FORWARD_ITEMS")

for key, value in manifest["immutability"].items():
    if value is not True:
        fail("IMMUTABILITY|" + key)

review_state = manifest["human_review_state"]

if review_state["focused_rereview_packet"] != "BLANK":
    fail("FOCUSED_REVIEW_PACKET_STATE")

if review_state["focused_human_decision_exists"] is not False:
    fail("FOCUSED_DECISION_EXISTS")

if review_state["focused_human_approval_exists"] is not False:
    fail("FOCUSED_APPROVAL_EXISTS")

for key, value in manifest["bounded_nonclaims"].items():
    if value is not False:
        fail("BOUNDED_NONCLAIM|" + key)

lifecycle = manifest["authorization_verifier_lifecycle"]

if lifecycle[
    "decision_0095_authorization_verifier_final_run_completed"
] is not True:
    fail("AUTH_LIFECYCLE_FINAL_RUN")

if lifecycle[
    "decision_0095_authorization_verifier_permanently_retired"
] is not True:
    fail("AUTH_LIFECYCLE_RETIRED")

if lifecycle[
    "decision_0095_authorization_verifier_rerun_allowed"
] is not False:
    fail("AUTH_LIFECYCLE_RERUN")

# ------------------------------------------------------------
# Full package checksum closure.
# ------------------------------------------------------------

package_sum_count = verify_sumfile(ROOT, SUMS)

print("FORMALIZATION_V1_EXACT_BINDING=PASS")
print("ORIGINAL_REVIEW_PACKAGE_V1_EXACT_BINDING=PASS")
print("COMPLETED_REVISION_REQUIRED_REVIEW_EXACT_BINDING=PASS")
print("DECISION_0095_AUTHORIZATION_EXACT_BINDING=PASS")

print(f"FORMALIZATION_INTERNAL_CHECKSUM_ENTRY_COUNT={formalization_sum_count}")
print(f"REVIEW_PACKAGE_INTERNAL_CHECKSUM_ENTRY_COUNT={review_sum_count}")
print(f"COMPLETED_REVIEW_INTERNAL_CHECKSUM_ENTRY_COUNT={human_sum_count}")
print(f"AUTHORIZATION_INTERNAL_CHECKSUM_ENTRY_COUNT={authorization_sum_count}")
print(f"CORRECTIVE_PACKAGE_CHECKSUM_ENTRY_COUNT={package_sum_count}")

print("SOURCE_LEAF_FIELD_COUNT=531")
print("SOURCE_SEMANTIC_UNIT_COUNT=109")
print("SOURCE_MATRIX_FIELD_CLASS_COUNT=57")
print("SOURCE_MATRIX_UNIT_ANALYSIS_COUNT=109")
print("SOURCE_SCHEMA_V2_PROPERTY_PATH_COUNT=171")

print("RELATION_ROW_COUNT=9747")
print("RELATION_EQUALS_FULL_57x171_CARTESIAN_PRODUCT=YES")
print("RELATION_SEMANTICALLY_RELATED=113")
print("RELATION_NOT_SEMANTICALLY_RELATED=969")
print("RELATION_UNRESOLVED=8665")

print("TWO_DISTINCT_57_ELEMENT_FIELD_CLASS_VOCABULARIES=PASS")
print("F03_531_LEAF_EXACT_BINDING=PASS")
print("F03_109_UNIT_INVENTORY_BINDING=PASS")
print("F03_109_MATRIX_UNIT_ANALYSIS_BINDING=PASS")
print("F03_CANDIDATE_FAMILY_LIST_BINDING=PASS")
print("F03_FAMILY_TO_FULL_CARRIER_PATH_LIST_MAP_BINDING=PASS")

print("LEXICAL_ONLY_TOTAL=125")
print("LEXICAL_ONLY_SEMANTICALLY_RELATED=0")
print("LEXICAL_ONLY_UNRESOLVED=120")
print("LEXICAL_ONLY_NOT_SEMANTICALLY_RELATED=5")
print("FIVE_LEXICAL_ONLY_EXPLICIT_NEGATIVE_PAIRS=PASS")

print("SRR04_CORRECTION_TYPE=PRESENTATION_ACCOUNTING_ONLY")
print("SRR04_RELATION_ROW_RECLASSIFICATION=NO")
print("SRR04_RELATION_ROW_MODIFICATION=NO")

print("ORIGINAL_OVERALL_HUMAN_REVIEW=REVISION_REQUIRED")
print("FOCUSED_REREVIEW_PACKET=BLANK")
print("FOCUSED_HUMAN_DECISION_EXISTS=NO")
print("FOCUSED_HUMAN_APPROVAL_EXISTS=NO")

print("DECISION_0095_AUTHORIZATION_VERIFIER_FINAL_RUN=PASS")
print("DECISION_0095_AUTHORIZATION_VERIFIER_PERMANENTLY_RETIRED=YES")
print("DECISION_0095_AUTHORIZATION_VERIFIER_RERUN_ALLOWED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("SELF_CONTAINED_PACKAGE_LOCAL_VERIFIER=PASS")
print("CORRECTIVE_SUCCESSOR_PACKAGE_V2=PASS")
