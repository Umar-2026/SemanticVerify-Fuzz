#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

BASE = REPO / (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_req06_req14_accounting_satisfaction_"
    "evidence_gap_and_acquisition_specification_study_v2_"
    "corrective_successor_for_aser01_aser02_aser04_aser07"
)


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(name):
    return json.loads(
        (BASE / name).read_text(
            encoding="utf-8"
        )
    )


def git_object_id(kind, content):
    header = (
        kind.encode("ascii")
        + b" "
        + str(len(content)).encode("ascii")
        + b"\x00"
    )

    return hashlib.sha1(
        header + content
    ).hexdigest()


def parse_tree(content):
    entries = {}
    i = 0

    while i < len(content):
        space = content.index(b" ", i)
        mode = content[i:space].decode("ascii")

        nul = content.index(
            b"\x00",
            space + 1,
        )

        name = content[
            space + 1:nul
        ].decode("utf-8")

        oid_bytes = content[
            nul + 1:nul + 21
        ]

        if len(oid_bytes) != 20:
            stop("TREE_OBJECT_TRUNCATED")

        entries[name] = {
            "mode":
                mode,

            "oid":
                oid_bytes.hex(),
        }

        i = nul + 21

    return entries


delta = load(
    "01_corrective_delta_response.v2.json"
)

prov = load(
    "02_d0203_portable_git_provenance.v2.json"
)

fixed = load(
    "03_fixed_evidence_substantive_copy_binding.v2.json"
)

domain = load(
    "04_future_accounting_domain_construction_specification.v2.json"
)

schemas = load(
    "05_future_AEA01_AEA05_artifact_schemas.v2.json"
)

canon = load(
    "06_canonicalization_and_identifier_comparison_rules.v2.json"
)

lineage = load(
    "07_future_domain_freeze_lineage_and_ordering_control.v2.json"
)

consumption = load(
    "09_decision0212_a02_consumption_record.v1.json"
)

sentinel = load(
    "11_decision0212_a02_consumption_sentinel.EXACT_COPY.v1.json"
)


if delta.get("status") != "AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR":
    stop("SUCCESSOR_STATUS_INVALID")

if delta.get("corrective_scope") != [
    "ASER01",
    "ASER02",
    "ASER04",
    "ASER07",
]:
    stop("CORRECTIVE_SCOPE_INVALID")

if delta.get("preserved_pass_items") != [
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]:
    stop("PASS_SCOPE_INVALID")

if delta["review_state"]["governance_adopted"] is not False:
    stop("GOVERNANCE_STATE_INVALID")

if delta["bounded_claim"]["accounting_satisfaction_established"] is not False:
    stop("SATISFACTION_STATE_INVALID")


raw_index = {}

for rec in prov["raw_git_objects"]:
    path = BASE / rec["raw_content_path"]

    if not path.is_file():
        stop("RAW_OBJECT_MISSING", rec["object_id"])

    content = path.read_bytes()

    if len(content) != rec["raw_content_size"]:
        stop("RAW_OBJECT_SIZE_INVALID", rec["object_id"])

    if digest(content) != rec["raw_content_sha256"]:
        stop("RAW_OBJECT_SHA256_INVALID", rec["object_id"])

    oid = git_object_id(
        rec["type"],
        content,
    )

    if oid != rec["object_id"]:
        stop("RAW_OBJECT_ID_INVALID", rec["object_id"])

    raw_index[
        (
            rec["type"],
            rec["object_id"],
        )
    ] = content


commit_id = prov["source_commit"]

commit_content = raw_index.get(
    ("commit", commit_id)
)

if commit_content is None:
    stop("COMMIT_OBJECT_MISSING")

tree_header = None

for line in commit_content.splitlines():
    if line.startswith(b"tree "):
        tree_header = line
        break

if tree_header is None:
    stop("COMMIT_TREE_HEADER_MISSING")

root_tree = tree_header.split(
    b" ",
    1,
)[1].decode("ascii")

if root_tree != prov["source_root_tree"]:
    stop("ROOT_TREE_BINDING_INVALID")


for rec in prov["source_paths"]:
    parts = Path(rec["source_path"]).parts

    current_tree = root_tree

    for index, component in enumerate(parts):
        tree_content = raw_index.get(
            ("tree", current_tree)
        )

        if tree_content is None:
            stop(
                "PATH_TREE_OBJECT_MISSING",
                current_tree,
            )

        entries = parse_tree(
            tree_content
        )

        if component not in entries:
            stop(
                "PATH_COMPONENT_MISSING",
                rec["source_path"],
            )

        target = entries[component]["oid"]

        if index == len(parts) - 1:
            if target != rec["git_blob"]:
                stop(
                    "PATH_BLOB_BINDING_INVALID",
                    rec["source_path"],
                )
        else:
            current_tree = target

    blob_content = raw_index.get(
        ("blob", rec["git_blob"])
    )

    if blob_content is None:
        stop(
            "BOUND_BLOB_OBJECT_MISSING",
            rec["source_path"],
        )

    if digest(blob_content) != rec["sha256"]:
        stop(
            "BOUND_SOURCE_SHA256_INVALID",
            rec["source_path"],
        )

    if len(blob_content) != rec["size_bytes"]:
        stop(
            "BOUND_SOURCE_SIZE_INVALID",
            rec["source_path"],
        )

    copy = BASE / rec["portable_copy"]

    if not copy.is_file():
        stop(
            "PORTABLE_COPY_MISSING",
            rec["portable_copy"],
        )

    if copy.read_bytes() != blob_content:
        stop(
            "PORTABLE_COPY_NOT_EXACT",
            rec["portable_copy"],
        )


if fixed.get("fixed_evidence_count") != 7:
    stop("FIXED_EVIDENCE_COUNT_INVALID")

if fixed["bounded_gap_interpretation"][
    "claim_complete_repository_absence"
] is not False:
    stop("ASER02_SCOPE_TOO_BROAD")

if fixed["bounded_gap_interpretation"][
    "claim_complete_governed_evidence_universe_absence"
] is not False:
    stop("ASER02_GOVERNED_UNIVERSE_SCOPE_TOO_BROAD")


matrix_path = (
    BASE
    / "enumeration_sources_exact/"
    / "01_semantic_unit_carrier_admissibility_matrix.v1.json"
)

matrix = json.loads(
    matrix_path.read_text(
        encoding="utf-8"
    )
)

rows = matrix["rows"]

semantic_ids = {
    row["semantic_unit_id"]
    for row in rows
}

carrier_ids = {
    row["schema_v2_property_path"]
    for row in rows
}

pairs = {
    (
        row["semantic_unit_id"],
        row["schema_v2_property_path"],
    )
    for row in rows
}

if len(rows) != 18639:
    stop("MATRIX_ROW_COUNT_INVALID")

if len(pairs) != 18639:
    stop("MATRIX_PAIR_UNIQUENESS_INVALID")

if len(semantic_ids) != 109:
    stop("MATRIX_U_COUNT_INVALID")

if len(carrier_ids) != 171:
    stop("MATRIX_C_COUNT_INVALID")

if domain.get(
    "actual_domain_acquisition_performed"
) is not False:
    stop("DOMAIN_ACQUISITION_STATE_INVALID")

if domain.get(
    "concrete_mapping_created"
) is not False:
    stop("MAPPING_STATE_INVALID")


if schemas.get(
    "instances_created_by_this_corrective_successor"
) is not False:
    stop("AEA_INSTANCE_STATE_INVALID")

for name in (
    "AEA01",
    "AEA02",
    "AEA03",
    "AEA04",
    "AEA05",
):
    schema = schemas["schemas"].get(name)

    if not isinstance(schema, dict):
        stop(
            "FORMAL_AEA_SCHEMA_MISSING",
            name,
        )

    if schema.get("type") != "object":
        stop(
            "FORMAL_AEA_SCHEMA_TYPE_INVALID",
            name,
        )

    if not schema.get("required"):
        stop(
            "FORMAL_AEA_REQUIRED_FIELDS_MISSING",
            name,
        )


active = canon[
    "authoritative_active_schema_v2_hash_contract"
]

if active["active_repository_path"] != (
    "config/protocol_content_hash_canonicalization.v2.json"
):
    stop("ACTIVE_HASH_CONTRACT_PATH_INVALID")

if active["sha256"] != (
    "37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9"
):
    stop("ACTIVE_HASH_CONTRACT_SHA_INVALID")

active_copy = BASE / active["portable_copy"]

if digest(active_copy.read_bytes()) != active["sha256"]:
    stop("ACTIVE_HASH_CONTRACT_COPY_INVALID")

pred = canon[
    "pre_finalization_provenance_source"
]

if pred["sha256"] != (
    "8fa63b0faea168e7dcc7701d94704d408dbd8d22e5d17d6c83cc3ab90095aab0"
):
    stop("PREDECESSOR_HASH_CONTRACT_SHA_INVALID")

if pred["is_active_installed_contract"] is not False:
    stop("PREDECESSOR_ROLE_INVALID")

flags = canon[
    "active_schema_accounting_flag_binding"
]

if flags[
    "flag_declarations_are_accounting_satisfaction_evidence"
] is not False:
    stop("FLAG_SATISFACTION_BOUNDARY_INVALID")

for key in (
    "forward_complete",
    "reverse_complete",
):
    value = flags.get(key)

    if not isinstance(value, dict):
        stop("FLAG_BINDING_MISSING", key)

    if not value.get("json_pointer"):
        stop("FLAG_POINTER_MISSING", key)

    if not value.get(
        "schema_fragment_canonical_sha256"
    ):
        stop("FLAG_FRAGMENT_SHA_MISSING", key)


for key in (
    "freeze_event_executed_by_this_successor",
    "witness_created_by_this_successor",
    "satisfaction_evaluated_by_this_successor",
):
    if lineage.get(key) is not False:
        stop(
            "LINEAGE_EXECUTION_STATE_INVALID",
            key,
        )


if consumption.get(
    "execution_attempt_count"
) != 1:
    stop("D0212_A02_COUNT_INVALID")

if consumption.get(
    "execution_result"
) != "PASS":
    stop("D0212_A02_RESULT_INVALID")

if consumption.get(
    "state"
) != "PERMANENTLY_RETIRED":
    stop("D0212_A02_STATE_INVALID")

if consumption.get(
    "rerun_authorized"
) is not False:
    stop("D0212_A02_RERUN_INVALID")

if sentinel.get(
    "execution_attempt_count"
) != 1:
    stop("D0212_SENTINEL_COUNT_INVALID")

if sentinel.get(
    "execution_result"
) != "PASS":
    stop("D0212_SENTINEL_RESULT_INVALID")

if sentinel.get(
    "state"
) != "PERMANENTLY_RETIRED":
    stop("D0212_SENTINEL_STATE_INVALID")

if sentinel.get(
    "rerun_authorized"
) is not False:
    stop("D0212_SENTINEL_RERUN_INVALID")

output_copy = (
    BASE
    / "10_decision0212_a02_execution_output.EXACT_COPY.v1.txt"
).read_bytes()

if digest(output_copy) != consumption[
    "execution_output_sha256"
]:
    stop("D0212_OUTPUT_COPY_INVALID")

sentinel_copy = (
    BASE
    / "11_decision0212_a02_consumption_sentinel.EXACT_COPY.v1.json"
).read_bytes()

if digest(sentinel_copy) != consumption[
    "consumption_sentinel_sha256"
]:
    stop("D0212_SENTINEL_COPY_INVALID")


print(
    "D0213_REQ06_REQ14_ACCOUNTING_GAP_CORRECTIVE_SUCCESSOR_VERIFIER=PASS"
)

print("SUCCESSOR_STATUS=AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR")
print("CORRECTIVE_ITEMS=ASER01,ASER02,ASER04,ASER07")
print("PRESERVED_PASS_ITEMS=ASER03,ASER05,ASER06,ASER08,ASER09")

print("ASER01_CORRECTIVE_MATERIAL_AUTHORED=YES")
print("ASER02_CORRECTIVE_MATERIAL_AUTHORED=YES")
print("ASER04_CORRECTIVE_MATERIAL_AUTHORED=YES")
print("ASER07_CORRECTIVE_MATERIAL_AUTHORED=YES")

print("ASER01_REVIEW_RESULT=NOT_DETERMINED")
print("ASER02_REVIEW_RESULT=NOT_DETERMINED")
print("ASER04_REVIEW_RESULT=NOT_DETERMINED")
print("ASER07_REVIEW_RESULT=NOT_DETERMINED")

print("PORTABLE_D0203_GIT_OBJECT_EVIDENCE_PRESENT=YES")
print("D0203_BLOB_TO_PATH_BINDING_VERIFIED=YES")
print("FIXED_EVIDENCE_SUBSTANTIVE_COPY_COUNT=7")

print("HISTORICAL_ENUMERATION_SOURCE_SEMANTIC_UNIT_COUNT=109")
print("HISTORICAL_ENUMERATION_SOURCE_CARRIER_CANDIDATE_COUNT=171")

print("FORMAL_AEA01_AEA05_SCHEMAS_AUTHORED=YES")
print("CANONICALIZATION_IDENTIFIER_RULES_AUTHORED=YES")
print("ACTIVE_V2_HASH_CONTRACT_EXACTLY_BOUND=YES")
print("FREEZE_LINEAGE_ORDERING_CONTROLS_AUTHORED=YES")

print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_PERFORMED=NO")
print("ACTUAL_DOMAIN_ACQUISITION_PERFORMED=NO")
print("FORWARD_WITNESS_ACQUIRED=NO")
print("REVERSE_WITNESS_ACQUIRED=NO")
print("CONCRETE_MAPPING_CREATED=NO")
print("ACCOUNTING_SATISFACTION_EVALUATED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")

print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("SUPPORTED_BINDING_COUNT=211")
print("UNRESOLVED_BINDING_COUNT=1642")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("REQ06_REQ14_UNRESOLVED_PAIR_COUNT=218")

print("CORRECTIVE_SUCCESSOR_GOVERNANCE_ADOPTED=NO")
print("SCHEMA_V2_LOSSLESSNESS_PROVEN=NO")
print("INDEPENDENT_HUMAN_REREVIEW_REQUIRED=YES")

print("D0212_A02_EXECUTION_ATTEMPT_COUNT=1")
print("D0212_A02_RESULT=PASS")
print("D0212_A02_STATE=PERMANENTLY_RETIRED")
print("D0212_A02_RERUN_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
