#!/usr/bin/env python3

import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

BINDING = (
    HERE
    / "05_portable_source_binding_manifest.v2.json"
)

RESOLVABILITY = (
    HERE
    / "06_portable_resolvability_manifest.v2.json"
)

PACKAGE = (
    HERE
    / "07_corrective_successor_package_v2_manifest.json"
)

REPORT = (
    HERE
    / "08_corrective_successor_package_v2_report.md"
)

SUMS = (
    HERE
    / "10_sucr01_corrective_portable_source_evidence_successor_package_v2.SHA256SUMS"
)

COMPLETED_REVIEW = (
    HERE
    / "completed_human_review_v1_exact"
    / "01_completed_SUCR01_SUCR08_human_review.EXACT_COPY.v1.md"
)

ORIGINAL_PACKET = (
    HERE
    / "original_review_package_v1_exact"
    / "20_SUCR01_SUCR08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

A02_OUT = (
    HERE
    / "03_decision0117_a02_final_output.EXACT_COPY.v1.txt"
)

CONSUMPTION = (
    HERE
    / "04_decision0117_a02_consumption_record.v1.json"
)

EXPECTED_SOURCE_CLASSES = {
    "active_schema_v2",
    "semantic_role_relation_artifact",
    "semantic_role_traceability_artifact",
    "prior_relation_informed_study_v1",
    "governance_adoption_evidence_v1",
    "decision_0109_governance_adoption",
}

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

binding = json.loads(
    BINDING.read_text(
        encoding="utf-8"
    )
)

if binding[
    "corrective_scope"
] != "SUCR01_ONLY_SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY":
    fail(
        "CORRECTIVE_SCOPE"
    )

sources = binding["sources"]

if set(sources) != EXPECTED_SOURCE_CLASSES:
    fail(
        "PORTABLE_SOURCE_CLASS_SET"
    )

if binding[
    "portable_source_class_count"
] != 6:
    fail(
        "PORTABLE_SOURCE_CLASS_COUNT"
    )

if binding[
    "all_required_source_classes_present"
] is not True:
    fail(
        "SOURCE_CLASSES_PRESENT"
    )

for name, spec in sources.items():

    target = (
        HERE
        / spec[
            "portable_package_path"
        ]
    )

    if spec[
        "binding_type"
    ] == "BYTE_EXACT_FILE":

        if not target.is_file():
            fail(
                "PORTABLE_FILE_MISSING|"
                + name
            )

        if sha(target) != \
                spec[
                    "source_sha256"
                ]:
            fail(
                "PORTABLE_FILE_SHA|"
                + name
            )

        if target.stat().st_size != \
                spec[
                    "source_size_bytes"
                ]:
            fail(
                "PORTABLE_FILE_SIZE|"
                + name
            )

        if spec[
            "portable_sha256"
        ] != spec[
            "source_sha256"
        ]:
            fail(
                "RECORDED_PORTABLE_SHA|"
                + name
            )

        if spec[
            "portable_size_bytes"
        ] != spec[
            "source_size_bytes"
        ]:
            fail(
                "RECORDED_PORTABLE_SIZE|"
                + name
            )

        if spec[
            "byte_exact_binding_verified"
        ] is not True:
            fail(
                "BYTE_EXACT_BINDING_FLAG|"
                + name
            )

    elif spec[
        "binding_type"
    ] == "EXACT_DIRECTORY_WITH_SOURCE_GIT_TREE":

        if not target.is_dir():
            fail(
                "PORTABLE_DIRECTORY_MISSING|"
                + name
            )

        expected_entries = spec[
            "portable_file_inventory"
        ]

        actual_files = sorted(
            p.relative_to(target)
            for p in target.rglob("*")
            if p.is_file()
        )

        expected_paths = sorted(
            Path(x["relative_path"])
            for x in expected_entries
        )

        if actual_files != expected_paths:
            fail(
                "PORTABLE_DIRECTORY_FILE_SET|"
                + name
            )

        by_path = {
            x["relative_path"]:
                x
            for x in expected_entries
        }

        for rel in actual_files:

            p = target / rel
            e = by_path[str(rel)]

            if sha(p) != e["sha256"]:
                fail(
                    "PORTABLE_DIRECTORY_SHA|"
                    + name
                    + "|"
                    + str(rel)
                )

            if p.stat().st_size != \
                    e["size_bytes"]:
                fail(
                    "PORTABLE_DIRECTORY_SIZE|"
                    + name
                    + "|"
                    + str(rel)
                )

            actual_exec = bool(
                os.stat(p).st_mode
                & 0o111
            )

            if actual_exec != \
                    e["executable"]:
                fail(
                    "PORTABLE_DIRECTORY_EXEC_MODE|"
                    + name
                    + "|"
                    + str(rel)
                )

        if spec[
            "portable_file_count"
        ] != len(actual_files):
            fail(
                "PORTABLE_DIRECTORY_COUNT|"
                + name
            )

        if spec[
            "portable_directory_inventory_complete"
        ] is not True:
            fail(
                "PORTABLE_DIRECTORY_COMPLETENESS|"
                + name
            )

    else:

        fail(
            "UNKNOWN_BINDING_TYPE|"
            + name
        )

res = json.loads(
    RESOLVABILITY.read_text(
        encoding="utf-8"
    )
)

if res["criterion"] != "SUCR01":
    fail(
        "RESOLVABILITY_CRITERION"
    )

if res[
    "original_decision"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_SUCR01_DECISION"
    )

if res[
    "original_overall_review"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_OVERALL_REVIEW"
    )

if set(
    res[
        "corrective_evidence_classes"
    ]
) != EXPECTED_SOURCE_CLASSES:
    fail(
        "RESOLVABILITY_SOURCE_CLASS_SET"
    )

for name, x in res[
    "corrective_evidence_classes"
].items():

    if x["present"] is not True:
        fail(
            "SOURCE_NOT_PRESENT|"
            + name
        )

    if x[
        "independently_resolvable_inside_package"
    ] is not True:
        fail(
            "SOURCE_NOT_RESOLVABLE|"
            + name
        )

if res[
    "all_required_source_classes_portable"
] is not True:
    fail(
        "ALL_SOURCES_PORTABLE"
    )

if res[
    "all_required_source_classes_resolvable_without_repository_access"
] is not True:
    fail(
        "INDEPENDENT_RESOLVABILITY"
    )

for key in (
    "original_review_modified",
    "original_overall_review_rewritten",
    "sucr02_through_sucr08_original_pass_findings_changed",
    "focused_sucr01_rereview_performed",
    "focused_sucr01_rereview_authorized",
    "review_chain_closed",
    "study_governance_adopted",
):

    if res[key] is not False:
        fail(
            "UNEXPECTED_RESOLVABILITY_STATE|"
            + key
        )

pkg = json.loads(
    PACKAGE.read_text(
        encoding="utf-8"
    )
)

if pkg[
    "package_status"
] != "AUTHOR_CANDIDATE_AWAITING_FOCUSED_SUCR01_REREVIEW":
    fail(
        "PACKAGE_STATUS"
    )

if pkg[
    "corrective_scope"
] != "SUCR01_ONLY_SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY":
    fail(
        "PACKAGE_SCOPE"
    )

review = pkg[
    "source_review_state"
]

if review["SUCR01"] != \
        "REVISION_REQUIRED":
    fail(
        "PACKAGE_SUCR01_STATE"
    )

for rid in (
    "SUCR02",
    "SUCR03",
    "SUCR04",
    "SUCR05",
    "SUCR06",
    "SUCR07",
    "SUCR08",
):

    if review[rid] != "PASS":
        fail(
            "PACKAGE_CARRIED_PASS|"
            + rid
        )

if review[
    "original_overall_review"
] != "REVISION_REQUIRED":
    fail(
        "PACKAGE_OVERALL_STATE"
    )

for key, value in pkg[
    "review_state"
].items():

    if value is not False:
        fail(
            "PREMATURE_REVIEW_STATE|"
            + key
        )

for key, value in pkg[
    "technical_nonclaims"
].items():

    if value is not False:
        fail(
            "UNEXPECTED_PERMISSION|"
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

if cons[
    "verifier_state_after_run"
] != "PERMANENTLY_RETIRED":
    fail(
        "A02_STATE"
    )

if cons[
    "rerun_authorized"
] is not False:
    fail(
        "A02_RERUN"
    )

if cons[
    "must_never_be_rerun"
] is not True:
    fail(
        "A02_RETIREMENT"
    )

if sha(A02_OUT) != \
        cons[
            "final_output_sha256"
        ]:
    fail(
        "A02_OUTPUT_SHA"
    )

if A02_OUT.stat().st_size != \
        cons[
            "final_output_size_bytes"
        ]:
    fail(
        "A02_OUTPUT_SIZE"
    )

if (
    "SUCR01_CORRECTIVE_SUCCESSOR_PACKAGE_V2_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(
        encoding="utf-8"
    )
):
    fail(
        "A02_PASS_MARKER"
    )

completed = COMPLETED_REVIEW.read_text(
    encoding="utf-8"
)

expected_decisions = {
    "SUCR01":
        "REVISION_REQUIRED",

    "SUCR02":
        "PASS",

    "SUCR03":
        "PASS",

    "SUCR04":
        "PASS",

    "SUCR05":
        "PASS",

    "SUCR06":
        "PASS",

    "SUCR07":
        "PASS",

    "SUCR08":
        "PASS",
}

for rid, expected in expected_decisions.items():

    m = re.search(
        rf"## {rid} —.*?"
        rf"Decision:\s*`([^`]+)`",
        completed,
        flags=re.DOTALL,
    )

    if not m:
        fail(
            "COMPLETED_REVIEW_DECISION_MISSING|"
            + rid
        )

    if m.group(1).strip() != expected:
        fail(
            "COMPLETED_REVIEW_DECISION|"
            + rid
        )

m = re.search(
    r"^Overall decision:\s*`([^`]+)`\s*$",
    completed,
    flags=re.MULTILINE,
)

if not m or \
        m.group(1).strip() != \
        "REVISION_REQUIRED":
    fail(
        "COMPLETED_REVIEW_OVERALL"
    )

original_blank = ORIGINAL_PACKET.read_text(
    encoding="utf-8"
)

if (
    "Package state: `BLANK — AWAITING INDEPENDENT HUMAN REVIEW`"
    not in original_blank
):
    fail(
        "ORIGINAL_REVIEW_PACKAGE_CHANGED"
    )

if SUMS.is_file():

    lines = [
        line
        for line in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 53:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for line in lines:

        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")
        target = HERE / rel

        if sha(target) != digest:
            fail(
                "CHECKSUM|"
                + rel
            )

print("CORRECTIVE_SCOPE=SUCR01_ONLY_SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY")

print("PORTABLE_SOURCE_EVIDENCE_CLASS_COUNT=6")
print("ACTIVE_SCHEMA_V2_PORTABLE_BINDING=PASS")
print("RELATION_ARTIFACT_PORTABLE_BINDING=PASS")
print("TRACEABILITY_ARTIFACT_PORTABLE_BINDING=PASS")
print("PRIOR_STUDY_V1_PORTABLE_BINDING=PASS")
print("GOVERNANCE_ADOPTION_V1_PORTABLE_BINDING=PASS")
print("DECISION_0109_PORTABLE_BINDING=PASS")

print("ALL_REQUIRED_SOURCE_CLASSES_PORTABLE=YES")
print("ALL_REQUIRED_SOURCE_CLASSES_INDEPENDENTLY_RESOLVABLE=YES")

print("ORIGINAL_SUCR01_DECISION=REVISION_REQUIRED")
print("SUCR02_SUCR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")

print("PACKAGE_STATUS=AUTHOR_CANDIDATE_AWAITING_FOCUSED_SUCR01_REREVIEW")

print("FOCUSED_SUCR01_REREVIEW_AUTHORIZED=NO")
print("FOCUSED_SUCR01_REREVIEW_COMPLETED=NO")
print("REVIEW_CHAIN_CLOSED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("POSITIVE_EXISTING_V2_MAPPING_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_PROVEN=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0117_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0117_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("SUCR01_CORRECTIVE_PORTABLE_SOURCE_EVIDENCE_SUCCESSOR_PACKAGE_V2=PASS")
