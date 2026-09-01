#!/usr/bin/env python3

from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile

BASE = Path(__file__).resolve().parent

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

D0215_COMMIT = (
    "53d0ced3daa2aa1b3dc6464ac77a3793704905b8"
)


def stop(code, detail=""):
    print(
        "STOP|"
        + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


def sha(raw):
    return hashlib.sha256(
        raw
    ).hexdigest()


parser = argparse.ArgumentParser()

parser.add_argument(
    "--require-initial-external-form",
    action="store_true",
)

args = parser.parse_args()


manifest = json.loads(
    (
        BASE
        / "01_external_handoff_manifest.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

consumption = json.loads(
    (
        BASE
        / "02_decision0216_a02_consumption_record.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

sentinel_raw = (
    BASE
    / "04_decision0216_a02_consumption_sentinel.EXACT_COPY.v1.json"
).read_bytes()

sentinel = json.loads(
    sentinel_raw.decode(
        "utf-8"
    )
)


if manifest.get("status") != (
    "HANDED_OFF_AWAITING_GENUINE_EXTERNAL_INDEPENDENT_HUMAN_REREVIEW"
):
    stop("HANDOFF_STATUS_INVALID")


if consumption.get(
    "execution_attempt_count"
) != 1:
    stop("D0216_A02_COUNT_INVALID")

if consumption.get(
    "execution_result"
) != "PASS":
    stop("D0216_A02_RESULT_INVALID")

if consumption.get(
    "state"
) != "PERMANENTLY_RETIRED":
    stop("D0216_A02_STATE_INVALID")

if consumption.get(
    "rerun_authorized"
) is not False:
    stop("D0216_A02_RERUN_STATE_INVALID")


for key in (
    "execution_attempt_count",
    "execution_result",
    "state",
    "rerun_authorized",
):
    if sentinel.get(key) != consumption.get(key):
        stop(
            "D0216_SENTINEL_CONSUMPTION_MISMATCH",
            key,
        )


output_raw = (
    BASE
    / "03_decision0216_a02_execution_output.EXACT_COPY.v1.txt"
).read_bytes()

if sha(output_raw) != consumption[
    "execution_output_sha256"
]:
    stop("D0216_OUTPUT_EXACT_COPY_INVALID")

if sha(sentinel_raw) != consumption[
    "consumption_sentinel_sha256"
]:
    stop("D0216_SENTINEL_EXACT_COPY_INVALID")


source = manifest["source"]

if source.get(
    "decision0215_commit"
) != D0215_COMMIT:
    stop("SOURCE_COMMIT_INVALID")


expected_source_entries = source[
    "source_entries"
]

for rec in expected_source_entries:
    raw = subprocess.check_output(
        [
            "git",
            "-C",
            str(REPO),
            "cat-file",
            "blob",
            rec["git_blob"],
        ]
    )

    if sha(raw) != rec["sha256"]:
        stop(
            "SOURCE_BLOB_SHA_INVALID",
            rec["source_path"],
        )

    if len(raw) != rec["size_bytes"]:
        stop(
            "SOURCE_BLOB_SIZE_INVALID",
            rec["source_path"],
        )

    current_oid = subprocess.check_output(
        [
            "git",
            "-C",
            str(REPO),
            "rev-parse",
            f"{D0215_COMMIT}:{rec['source_path']}",
        ],
        text=True,
    ).strip()

    if current_oid != rec["git_blob"]:
        stop(
            "SOURCE_PATH_BLOB_BINDING_INVALID",
            rec["source_path"],
        )


zip_meta = manifest[
    "external_handoff_zip"
]

zip_path = Path(
    zip_meta["path"]
)

if not zip_path.is_file():
    stop("EXTERNAL_ZIP_MISSING")

zip_raw = zip_path.read_bytes()

if sha(zip_raw) != zip_meta[
    "sha256"
]:
    stop("EXTERNAL_ZIP_SHA_INVALID")

if len(zip_raw) != zip_meta[
    "size_bytes"
]:
    stop("EXTERNAL_ZIP_SIZE_INVALID")


prefix = Path(
    source["source_package_path"]
).name

expected_zip_names = sorted(
    prefix
    + "/"
    + rec[
        "package_relative_path"
    ]
    for rec in expected_source_entries
)

with zipfile.ZipFile(
    zip_path,
    mode="r",
) as zf:
    if sorted(
        zf.namelist()
    ) != expected_zip_names:
        stop("EXTERNAL_ZIP_ENTRY_SET_INVALID")

    for rec in expected_source_entries:
        arcname = (
            prefix
            + "/"
            + rec[
                "package_relative_path"
            ]
        )

        raw = zf.read(
            arcname
        )

        if sha(raw) != rec[
            "sha256"
        ]:
            stop(
                "EXTERNAL_ZIP_ENTRY_SHA_INVALID",
                arcname,
            )

        if len(raw) != rec[
            "size_bytes"
        ]:
            stop(
                "EXTERNAL_ZIP_ENTRY_SIZE_INVALID",
                arcname,
            )


manual_meta = manifest[
    "external_manual_review_copy"
]

source_blank_raw = subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "show",
        (
            manual_meta["source_commit"]
            + ":"
            + manual_meta["source_path"]
        ),
    ]
)

if sha(source_blank_raw) != manual_meta[
    "initial_sha256"
]:
    stop("MANUAL_INITIAL_SOURCE_SHA_INVALID")

if len(source_blank_raw) != manual_meta[
    "initial_size_bytes"
]:
    stop("MANUAL_INITIAL_SOURCE_SIZE_INVALID")


manual_path = Path(
    manual_meta["path"]
)

current_matches_initial = False

if manual_path.is_file():
    current_raw = manual_path.read_bytes()

    current_matches_initial = (
        sha(current_raw)
        == manual_meta[
            "initial_sha256"
        ]
        and len(current_raw)
        == manual_meta[
            "initial_size_bytes"
        ]
    )


if (
    args.require_initial_external_form
    and not current_matches_initial
):
    stop(
        "EXTERNAL_MANUAL_FORM_NO_LONGER_INITIAL_BLANK_COPY"
    )


print(
    "D0217_EXTERNAL_INDEPENDENT_HUMAN_REREVIEW_HANDOFF_VERIFIER=PASS"
)

print(
    "HANDOFF_STATUS=HANDED_OFF_AWAITING_GENUINE_EXTERNAL_INDEPENDENT_HUMAN_REREVIEW"
)

print(
    "EXTERNAL_ZIP_VERIFIED=YES"
)

print(
    "EXTERNAL_ZIP_ENTRY_COUNT="
    + str(
        len(
            expected_source_entries
        )
    )
)

print(
    "EXTERNAL_MANUAL_COPY_INITIAL_SOURCE_BINDING_VERIFIED=YES"
)

print(
    "EXTERNAL_MANUAL_COPY_CURRENTLY_MATCHES_INITIAL="
    + (
        "YES"
        if current_matches_initial
        else "NO"
    )
)

print(
    "HUMAN_REREVIEW_PERFORMED_AT_HANDOFF_CREATION=NO"
)

print(
    "HUMAN_FIELDS_SYNTHESIZED=NO"
)

print(
    "RETURNED_REREVIEW_RECORDING_AUTHORIZED=NO"
)

print(
    "CORRECTIVE_SUCCESSOR_GOVERNANCE_ADOPTED=NO"
)

print(
    "D0216_A02_EXECUTION_ATTEMPT_COUNT=1"
)

print(
    "D0216_A02_RESULT=PASS"
)

print(
    "D0216_A02_STATE=PERMANENTLY_RETIRED"
)

print(
    "D0216_A02_RERUN_AUTHORIZED=NO"
)

print(
    "ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO"
)

print(
    "CONCRETE_MAPPING_AUTHORIZED=NO"
)

print(
    "ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO"
)

print(
    "PAIR_RECLASSIFICATION_AUTHORIZED=NO"
)

print(
    "ANALYZER_AUTHORIZED=NO"
)

print(
    "BASELINE_AUTHORIZED=NO"
)

print(
    "REPAIR_AUTHORIZED=NO"
)
