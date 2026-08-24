#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

MATRIX = (
    HERE
    / "01_17_requirement_provenance_binding_matrix.v1.json"
)

SOURCES = (
    HERE
    / "02_source_evidence_inventory.v1.json"
)

ACCOUNTING = (
    HERE
    / "03_machine_readable_accounting.v1.json"
)

A02_OUT = (
    HERE
    / "05_decision0126_a02_final_output.EXACT_COPY.v1.txt"
)

CONSUMPTION = (
    HERE
    / "06_decision0126_a02_consumption_record.v1.json"
)

SUMS = (
    HERE
    / "08_v4_losslessness_requirement_provenance_binding_resolution_study.v1.SHA256SUMS"
)

EXPECTED_CANONICAL_SHA = (
    "c869079bfbd395b479e2dd8f2f1bcc31"
    "aabeababe0e24fc1542c6d35d210602e"
)

def fail(msg):
    print(
        "FAIL|" + msg
    )
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

def blob(rel):
    p = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            "rev-parse",
            "HEAD:" + rel,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        fail(
            "GIT_BLOB|" + rel
        )

    return p.stdout.strip()

def csha(value):
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()

def resolve_simple_json_path(obj, path):
    if not path.startswith("$."):
        fail(
            "JSON_PATH_FORMAT|" + path
        )

    cur = obj

    for token in path[2:].split("."):
        if not isinstance(cur, dict):
            fail(
                "JSON_PATH_NON_OBJECT|" + path
            )

        if token not in cur:
            fail(
                "JSON_PATH_MISSING|" + path
            )

        cur = cur[token]

    return cur

matrix = json.loads(
    MATRIX.read_text(
        encoding="utf-8"
    )
)

rows = matrix[
    "records"
]

if (
    matrix[
        "requirement_count"
    ] != 17
    or len(rows) != 17
):
    fail(
        "REQUIREMENT_COUNT"
    )

ids = [
    r[
        "requirement_id"
    ]
    for r in rows
]

if len(set(ids)) != 17:
    fail(
        "REQUIREMENT_ID_UNIQUENESS"
    )

if (
    matrix[
        "canonical_losslessness_object_sha256"
    ]
    != EXPECTED_CANONICAL_SHA
):
    fail(
        "CANONICAL_OBJECT_SHA"
    )

if any(
    r[
        "classification"
    ] != "BOUND_EXACT"
    for r in rows
):
    fail(
        "NON_EXACT_CLASSIFICATION"
    )

for r in rows:
    rid = r[
        "requirement_id"
    ]

    if r[
        "canonical_value"
    ] is not True:
        fail(
            "CANONICAL_VALUE|" + rid
        )

    if (
        r[
            "canonical_value_sha256"
        ]
        != csha(True)
    ):
        fail(
            "CANONICAL_VALUE_SHA|" + rid
        )

    for key in (
        "author_inference_used_for_binding",
        "numeric_count_used_as_identity_proof",
        "memory_reconstruction_used",
        "requirement_content_invented",
        "coincidental_17_item_array_promoted",
        "prior_placeholder_index_semantic_equivalence_claimed",
    ):
        if r[key] is not False:
            fail(
                "BOUNDARY_FLAG|"
                + key
                + "|"
                + rid
            )

    all_bindings = [
        r[
            "primary_binding"
        ],
        *r[
            "corroborating_bindings"
        ],
    ]

    for binding in all_bindings:
        rel = binding[
            "repo_relative_path"
        ]

        source = (
            REPO
            / rel
        )

        if sha(source) != binding[
            "source_sha256"
        ]:
            fail(
                "SOURCE_SHA|"
                + rid
                + "|"
                + rel
            )

        if blob(rel) != binding[
            "source_git_blob"
        ]:
            fail(
                "SOURCE_BLOB|"
                + rid
                + "|"
                + rel
            )

        source_obj = json.loads(
            source.read_text(
                encoding="utf-8"
            )
        )

        value = resolve_simple_json_path(
            source_obj,
            binding[
                "structural_location"
            ],
        )

        if value is not True:
            fail(
                "BOUND_VALUE_NOT_TRUE|"
                + rid
                + "|"
                + rel
            )

sources = json.loads(
    SOURCES.read_text(
        encoding="utf-8"
    )
)

if sources[
    "source_count"
] != 7:
    fail(
        "SOURCE_COUNT"
    )

for key in (
    "prohibited_evidence_accessed",
    "generated_driver_source_accessed",
    "selected_sample_membership_accessed",
    "raw_model_response_accessed",
    "compiler_log_semantic_contents_accessed",
    "gold_label_accessed",
    "analyzer_output_accessed",
    "baseline_output_accessed",
    "llm_review_output_accessed",
    "repair_output_accessed",
):
    if sources[key] is not False:
        fail(
            "PROHIBITED_EVIDENCE_FLAG|"
            + key
        )

for src in sources[
    "sources"
]:
    rel = src[
        "repo_relative_path"
    ]

    source = (
        REPO
        / rel
    )

    if sha(source) != src[
        "sha256"
    ]:
        fail(
            "SOURCE_INVENTORY_SHA|"
            + rel
        )

    if blob(rel) != src[
        "git_blob"
    ]:
        fail(
            "SOURCE_INVENTORY_BLOB|"
            + rel
        )

acc = json.loads(
    ACCOUNTING.read_text(
        encoding="utf-8"
    )
)

if acc[
    "requirement_count"
] != 17:
    fail(
        "ACCOUNTING_COUNT"
    )

if acc[
    "bound_exact_count"
] != 17:
    fail(
        "BOUND_EXACT_COUNT"
    )

if acc[
    "bound_composite_count"
] != 0:
    fail(
        "BOUND_COMPOSITE_COUNT"
    )

if acc[
    "unresolved_count"
] != 0:
    fail(
        "UNRESOLVED_COUNT"
    )

if (
    acc[
        "study_outcome"
    ]
    != "REQUIREMENT_PROVENANCE_RESOLVED"
):
    fail(
        "STUDY_OUTCOME"
    )

for key in (
    "prior_governance_result_modified",
    "prior_semantic_unit_carrier_pair_state_modified",
    "carrier_admissibility_claimed",
    "positive_mapping_witness_constructed",
    "negative_mapping_impossibility_proof_constructed",
    "whole_v4_admissible_composition_exhaustiveness_claimed",
):
    if acc[key] is not False:
        fail(
            "ACCOUNTING_BOUNDARY|"
            + key
        )

for key, value in acc[
    "technical_nonclaims"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_AUTHORITY|"
            + key
        )

cons = json.loads(
    CONSUMPTION.read_text(
        encoding="utf-8"
    )
)

if cons[
    "final_run_result"
] != "PASS":
    fail(
        "A02_RESULT"
    )

if (
    cons[
        "verifier_state_after_run"
    ]
    != "PERMANENTLY_RETIRED"
):
    fail(
        "A02_STATE"
    )

if cons[
    "must_never_be_rerun"
] is not True:
    fail(
        "A02_RETIREMENT"
    )

if (
    sha(A02_OUT)
    != cons[
        "final_output_sha256"
    ]
):
    fail(
        "A02_OUTPUT_SHA"
    )

if (
    "V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(
        encoding="utf-8"
    )
):
    fail(
        "A02_PASS_MARKER"
    )

if SUMS.is_file():
    lines = [
        line
        for line in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 7:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(
                len(lines)
            )
        )

    for line in lines:
        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")

        if sha(
            HERE / rel
        ) != digest:
            fail(
                "CHECKSUM|"
                + rel
            )

print(
    "V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1=PASS"
)
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("REQUIREMENT_COUNT=17")
print("BOUND_EXACT_COUNT=17")
print("BOUND_COMPOSITE_COUNT=0")
print("UNRESOLVED_COUNT=0")
print(
    "STUDY_OUTCOME=REQUIREMENT_PROVENANCE_RESOLVED"
)
print(
    "REQUIREMENT_IDENTITY_BASIS=CANONICAL_V4_LOSSLESSNESS_OBJECT_KEYS"
)
print(
    "CANONICAL_LOSSLESSNESS_OBJECT_SHA256="
    + EXPECTED_CANONICAL_SHA
)
print(
    "INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES"
)
print(
    "SEMANTIC_UNIT_CARRIER_PAIR_RECLASSIFICATION_PERFORMED=NO"
)
print(
    "EXISTING_18639_PAIR_STATE_MODIFIED=NO"
)
print("CARRIER_ADMISSIBILITY_CLAIMED=NO")
print(
    "POSITIVE_MAPPING_WITNESS_CONSTRUCTED=NO"
)
print(
    "NEGATIVE_MAPPING_IMPOSSIBILITY_PROOF_CONSTRUCTED=NO"
)
print(
    "WHOLE_V4_EXHAUSTIVENESS_CLAIMED=NO"
)
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print(
    "ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO"
)
print(
    "SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO"
)
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_CREATED=NO")
print(
    "ANALYZER_IMPLEMENTATION_AUTHORIZED=NO"
)
print(
    "ANALYZER_EXECUTION_AUTHORIZED=NO"
)
print(
    "BASELINE_EXECUTION_AUTHORIZED=NO"
)
print("REPAIR_AUTHORIZED=NO")
print(
    "DECISION_0126_A02_STATE=PERMANENTLY_RETIRED"
)
print(
    "DECISION_0126_A02_EXECUTED_BY_SAFE_VERIFIER=NO"
)
print(
    "RETIRED_A02_VERIFIERS_EXECUTED=NO"
)
