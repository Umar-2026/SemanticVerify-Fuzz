#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import inspect
import json
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import primary_same_window_resume_v1 as resume
import primary_operational_runner_v1 as pr

REPORT = (
    REPO
    / "evidence/generation_opening/"
      "same_window_resume_v1/"
      "qualification.v1.json"
)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def canonical(obj):
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def main():
    if REPORT.exists():
        raise RuntimeError(
            "qualification report already exists"
        )

    checks = []

    def check(name, condition, detail=None):
        checks.append({
            "name":
                name,

            "status":
                (
                    "PASS"
                    if condition
                    else "FAIL"
                ),

            "detail":
                detail,
        })

        print(
            "CHECK|"
            + name
            + "|"
            + (
                "PASS"
                if condition
                else "FAIL"
            )
            + (
                "|"
                + str(detail)
                if detail is not None
                else ""
            )
        )

        if not condition:
            raise RuntimeError(
                name
            )

    print(
        "===== PROVIDER-FREE SAME-WINDOW RESUME QUALIFICATION ====="
    )

    locked = resume.load_inputs()

    check(
        "TRANSFORM_REPLACEMENT_COUNT_ONE",
        resume.TRANSFORM_REPLACEMENT_COUNT
        == 1,
    )

    boundary = (
        resume.validate_resume_boundary(
            locked
        )
    )

    check(
        "PAUSE_FREEZE_PACKAGE_4115",
        boundary[
            "package_entry_count"
        ]
        == 4115,
    )

    check(
        "TERMINAL_PREFIX_472",
        boundary[
            "terminal_slot_count"
        ]
        == 472,
    )

    check(
        "FIRST_RESUME_SLOT_473",
        boundary[
            "first_resume_slot"
        ]
        == 473,
    )

    check(
        "REMAINING_SLOTS_328",
        boundary[
            "remaining_slot_count"
        ]
        == 328,
    )

    check(
        "EXTRACTED_COUNT_402",
        boundary[
            "duplicate_extracted_count"
        ]
        == 402,
    )

    check(
        "CANONICAL_COUNT_362",
        boundary[
            "duplicate_canonical_count"
        ]
        == 362,
    )

    check(
        "DUPLICATE_COUNT_40",
        boundary[
            "duplicate_record_count"
        ]
        == 40,
    )

    check(
        "SERVICE_ERROR_STATE_ZERO_ZERO",
        boundary[
            "service_error_state"
        ]
        == {
            "Model A": 0,
            "Model B": 0,
        },
        boundary[
            "service_error_state"
        ],
    )

    gate = (
        resume.verify_resume_authorization(
            locked
        )
    )

    check(
        "RESUME_AUTHORIZATION_FAIL_CLOSED",
        gate.get(
            "authorized"
        )
        is False,
        gate,
    )

    check(
        "RESUME_AUTHORIZATION_MISSING_REASON",
        gate.get(
            "reason"
        )
        == "RESUME_AUTHORIZATION_RECORD_MISSING",
        gate,
    )

    # --------------------------------------------------------
    # Compiler/library preflight remains reproducible.
    # --------------------------------------------------------

    with tempfile.TemporaryDirectory(
        prefix="svf-resume-preflight-"
    ) as td:
        ctx = pr.compiler_preflight(
            locked,
            Path(td),
        )

        check(
            "COMPILER_VERSION_EXACT",
            ctx[
                "compiler_version"
            ]
            == locked[
                "postprocessing"
            ][
                "compilation"
            ][
                "expected_compiler_version"
            ],
        )

        check(
            "WEAK_MAIN_OBJECT_CREATED",
            ctx[
                "shim_o"
            ].is_file(),
        )

    # --------------------------------------------------------
    # Decision-0013 positive zero-output case.
    # --------------------------------------------------------

    usage = {
        "promptTokenCount":
            177,

        "totalTokenCount":
            177,
    }

    refusal = {
        "kind":
            "TERMINAL",

        "terminal_status":
            "REFUSAL",
    }

    cost = resume.estimate_cost_resume(
        "Model B",
        usage,
        locked[
            "contract"
        ],
        refusal,
        200,
    )

    check(
        "ZERO_OUTPUT_COST_PASS",
        cost.get(
            "status"
        )
        == "PASS",
        cost,
    )

    check(
        "ZERO_OUTPUT_COST_BASIS",
        cost.get(
            "basis"
        )
        == "DERIVED_ZERO_CANDIDATE_REFUSAL_TOKEN_BALANCE",
        cost,
    )

    check(
        "ZERO_OUTPUT_CANDIDATE_ZERO",
        cost.get(
            "candidate_tokens"
        )
        == 0,
        cost,
    )

    check(
        "ZERO_OUTPUT_COST_EXACT",
        abs(
            cost.get(
                "estimate_usd"
            )
            - 0.00004425
        )
        < 1e-15,
        cost,
    )

    # Non-refusal does not receive the amendment.
    normal = {
        "kind":
            "MODEL_TEXT",

        "terminal_status":
            "RESPONSE_RECEIVED",
    }

    normal_cost = (
        resume.estimate_cost_resume(
            "Model B",
            usage,
            locked[
                "contract"
            ],
            normal,
            200,
        )
    )

    check(
        "NON_REFUSAL_MISSING_CANDIDATE_STILL_PAUSES",
        normal_cost.get(
            "status"
        )
        == "PAUSE_REQUIRED",
        normal_cost,
    )

    # Token-balance mismatch does not receive amendment.
    bad_usage = {
        "promptTokenCount":
            177,

        "totalTokenCount":
            178,
    }

    bad_cost = (
        resume.estimate_cost_resume(
            "Model B",
            bad_usage,
            locked[
                "contract"
            ],
            refusal,
            200,
        )
    )

    check(
        "TOKEN_BALANCE_MISMATCH_STILL_PAUSES",
        bad_cost.get(
            "status"
        )
        == "PAUSE_REQUIRED",
        bad_cost,
    )

    # Positive cached usage remains a pause.
    cached_usage = {
        "promptTokenCount":
            177,

        "totalTokenCount":
            177,

        "cachedContentTokenCount":
            1,
    }

    cached_cost = (
        resume.estimate_cost_resume(
            "Model B",
            cached_usage,
            locked[
                "contract"
            ],
            refusal,
            200,
        )
    )

    check(
        "POSITIVE_CACHE_STILL_PAUSES",
        cached_cost.get(
            "status"
        )
        == "PAUSE_REQUIRED",
        cached_cost,
    )

    # Thoughts can be included only if total balances.
    thoughts_usage = {
        "promptTokenCount":
            177,

        "thoughtsTokenCount":
            5,

        "totalTokenCount":
            182,
    }

    thoughts_cost = (
        resume.estimate_cost_resume(
            "Model B",
            thoughts_usage,
            locked[
                "contract"
            ],
            refusal,
            200,
        )
    )

    check(
        "ZERO_CANDIDATE_WITH_THOUGHTS_PASS",
        thoughts_cost.get(
            "status"
        )
        == "PASS"
        and thoughts_cost.get(
            "thoughts_tokens"
        )
        == 5,
        thoughts_cost,
    )

    # --------------------------------------------------------
    # Exercise the transformed actual frozen transport branch
    # with a provider-free scripted response.
    # --------------------------------------------------------

    rec = (
        locked[
            "plan"
        ][
            "requests"
        ][473]
    )

    check(
        "SYNTHETIC_SLOT_IS_MODEL_B",
        rec[
            "logical_slot_id"
        ]
        == "SVF-PRIMARY-800-V1-SLOT-0474"
        and rec[
            "model_label"
        ]
        == "Model B",
        {
            "slot":
                rec[
                    "logical_slot_id"
                ],

            "model":
                rec[
                    "model_label"
                ],
        },
    )

    response_body = canonical({
        "modelVersion":
            "gemini-3.1-flash-lite",

        "promptFeedback": {
            "blockReason":
                "SAFETY",
        },

        "usageMetadata": {
            "promptTokenCount":
                177,

            "totalTokenCount":
                177,
        },
    })

    provider_calls = {
        "count": 0,
    }

    def fake_transport(**kwargs):
        provider_calls[
            "count"
        ] += 1

        return {
            "http_status":
                200,

            "headers": {
                "Content-Type":
                    "application/json",
            },

            "body":
                response_body,

            "latency_ms":
                1,
        }

    fake_secret = (
        "SVF_SYNTHETIC_SECRET_MUST_NOT_PERSIST"
    )

    with tempfile.TemporaryDirectory(
        prefix="svf-resume-transport-positive-"
    ) as td:
        root = Path(td)

        result = (
            resume.perform_transport_resume(
                locked,
                rec,
                fake_secret,
                root,
                {
                    "mode":
                        "DIRECT",

                    "source":
                        "synthetic",
                },
                transport_fn=
                    fake_transport,
                sleep_fn=
                    lambda seconds: None,
                execution_context={
                    "authorization_record_path":
                        "synthetic",

                    "authorization_record_sha256":
                        "0" * 64,

                    "execution_head_commit":
                        "synthetic",
                },
                service_error_state={
                    "Model A": 0,
                    "Model B": 0,
                },
            )
        )

        check(
            "SYNTHETIC_REFUSAL_TERMINAL",
            result.get(
                "terminal_status"
            )
            == "REFUSAL",
            result.get(
                "terminal_status"
            ),
        )

        check(
            "SYNTHETIC_REFUSAL_NO_PAUSE",
            result.get(
                "pause_required"
            )
            is False,
            result.get(
                "pause_reason"
            ),
        )

        check(
            "SYNTHETIC_REFUSAL_COST_PASS",
            result.get(
                "cost",
                {}
            ).get(
                "status"
            )
            == "PASS",
            result.get(
                "cost"
            ),
        )

        check(
            "SYNTHETIC_REFUSAL_COST_BASIS",
            result.get(
                "cost",
                {}
            ).get(
                "basis"
            )
            == "DERIVED_ZERO_CANDIDATE_REFUSAL_TOKEN_BALANCE",
            result.get(
                "cost"
            ),
        )

        secret_hits = 0

        for path in root.rglob("*"):
            if (
                path.is_file()
                and fake_secret.encode(
                    "utf-8"
                )
                in path.read_bytes()
            ):
                secret_hits += 1

        check(
            "SYNTHETIC_SECRET_NOT_PERSISTED",
            secret_hits == 0,
            secret_hits,
        )

    check(
        "SCRIPTED_TRANSPORT_INVOCATION_COUNT_ONE",
        provider_calls[
            "count"
        ]
        == 1,
        provider_calls,
    )

    # --------------------------------------------------------
    # Negative actual transport-path test.
    # --------------------------------------------------------

    bad_response_body = canonical({
        "modelVersion":
            "gemini-3.1-flash-lite",

        "promptFeedback": {
            "blockReason":
                "SAFETY",
        },

        "usageMetadata": {
            "promptTokenCount":
                177,

            "totalTokenCount":
                178,
        },
    })

    def fake_bad_transport(**kwargs):
        return {
            "http_status":
                200,

            "headers": {
                "Content-Type":
                    "application/json",
            },

            "body":
                bad_response_body,

            "latency_ms":
                1,
        }

    with tempfile.TemporaryDirectory(
        prefix="svf-resume-transport-negative-"
    ) as td:
        bad_result = (
            resume.perform_transport_resume(
                locked,
                rec,
                fake_secret,
                Path(td),
                {
                    "mode":
                        "DIRECT",

                    "source":
                        "synthetic",
                },
                transport_fn=
                    fake_bad_transport,
                sleep_fn=
                    lambda seconds: None,
                execution_context={
                    "authorization_record_path":
                        "synthetic",

                    "authorization_record_sha256":
                        "0" * 64,

                    "execution_head_commit":
                        "synthetic",
                },
                service_error_state={
                    "Model A": 0,
                    "Model B": 0,
                },
            )
        )

        check(
            "SYNTHETIC_BAD_BALANCE_PAUSES",
            bad_result.get(
                "pause_required"
            )
            is True,
            bad_result,
        )

        check(
            "SYNTHETIC_BAD_BALANCE_REASON",
            bad_result.get(
                "pause_reason"
            )
            == "INVALID_USAGE_METADATA",
            bad_result,
        )

    # --------------------------------------------------------
    # Static execution-order proof.
    # --------------------------------------------------------

    execute_source = (
        inspect.getsource(
            resume.execute_resume
        )
    )

    gate_pos = (
        execute_source.find(
            "verify_resume_authorization"
        )
    )

    boundary_pos = (
        execute_source.find(
            "validate_resume_boundary"
        )
    )

    compiler_pos = (
        execute_source.find(
            "pr.compiler_preflight"
        )
    )

    secrets_pos = (
        execute_source.find(
            "pr.read_secrets"
        )
    )

    marker_pos = (
        execute_source.find(
            "write_resume_marker"
        )
    )

    transport_pos = (
        execute_source.find(
            "perform_transport_resume"
        )
    )

    check(
        "AUTHORIZATION_BEFORE_SECRET_READ",
        (
            0 <= gate_pos
            < secrets_pos
        ),
        {
            "authorization":
                gate_pos,

            "secrets":
                secrets_pos,
        },
    )

    check(
        "BOUNDARY_BEFORE_SECRET_READ",
        (
            0 <= boundary_pos
            < secrets_pos
        ),
        {
            "boundary":
                boundary_pos,

            "secrets":
                secrets_pos,
        },
    )

    check(
        "COMPILER_PREFLIGHT_BEFORE_SECRET_READ",
        (
            0 <= compiler_pos
            < secrets_pos
        ),
        {
            "compiler":
                compiler_pos,

            "secrets":
                secrets_pos,
        },
    )

    check(
        "SECRET_READ_BEFORE_RESUME_MARKER",
        (
            0 <= secrets_pos
            < marker_pos
        ),
        {
            "secrets":
                secrets_pos,

            "marker":
                marker_pos,
        },
    )

    check(
        "RESUME_MARKER_BEFORE_FIRST_TRANSPORT",
        (
            0 <= marker_pos
            < transport_pos
        ),
        {
            "marker":
                marker_pos,

            "transport":
                transport_pos,
        },
    )

    check(
        "ORIGINAL_WRITE_OPEN_NOT_CALLED",
        "write_open("
        not in execute_source,
    )

    check(
        "PLAN_SLICE_STARTS_AFTER_472",
        '["requests"\n            ][472:]'
        in execute_source
        or "[472:]"
        in execute_source,
    )

    # --------------------------------------------------------
    # Primary evidence remains untouched.
    # --------------------------------------------------------

    check(
        "NO_SLOT_0473_CREATED",
        not (
            resume.PRIMARY_ROOT
            / "slots/"
              "SVF-PRIMARY-800-V1-SLOT-0473"
        ).exists(),
    )

    check(
        "NO_RESUME_MARKER_CREATED",
        not resume.RESUME_MARKER_PATH.exists(),
    )

    check(
        "NO_PAUSE_0002_CREATED",
        not resume.PAUSE_0002_PATH.exists(),
    )

    check(
        "WINDOW_CLOSE_STILL_ABSENT",
        not resume.WINDOW_CLOSE_PATH.exists(),
    )

    report = {
        "record_id":
            "SVF-SAME-WINDOW-RESUME-V1-PROVIDER-FREE-QUALIFICATION",

        "schema_version":
            1,

        "status":
            "PASS",

        "performed_at_utc":
            (
                datetime.now(
                    timezone.utc
                )
                .replace(
                    microsecond=0
                )
                .isoformat()
            ),

        "provider_calls":
            0,

        "api_secret_environment_values_read":
            False,

        "primary_generation_calls":
            0,

        "first_resume_slot_generated":
            False,

        "second_window_created":
            False,

        "slot_0472_retried":
            False,

        "raw_model_response_human_inspection":
            False,

        "generated_driver_human_inspection":
            False,

        "driver_bytes_read_mechanically_for_integrity_only":
            True,

        "analyzer_implementation":
            False,

        "repair_implementation":
            False,

        "transform_replacement_count":
            resume.TRANSFORM_REPLACEMENT_COUNT,

        "boundary_summary": {
            "terminal_slot_count":
                boundary[
                    "terminal_slot_count"
                ],

            "remaining_slot_count":
                boundary[
                    "remaining_slot_count"
                ],

            "canonical_duplicate_state_count":
                boundary[
                    "duplicate_canonical_count"
                ],

            "duplicate_record_count":
                boundary[
                    "duplicate_record_count"
                ],

            "service_error_state":
                boundary[
                    "service_error_state"
                ],

            "prior_invocation_count":
                boundary[
                    "prior_invocation_count"
                ],
        },

        "checks":
            checks,
    }

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with REPORT.open(
        "x",
        encoding="utf-8",
        newline="\n",
    ) as f:
        json.dump(
            report,
            f,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        f.write("\n")

    print(
        "QUALIFICATION_REPORT="
        + str(
            REPORT.relative_to(
                REPO
            )
        )
    )

    print(
        "QUALIFICATION_STATUS=PASS"
    )

    print(
        "LIVE_PROVIDER_CALLS=0"
    )

    print(
        "API_SECRET_VALUES_READ=NO"
    )

    print(
        "PRIMARY_WINDOW_RESUMED=NO"
    )

    print(
        "SLOT_0473_GENERATED=NO"
    )

    print(
        "SECOND_WINDOW_CREATED=NO"
    )

    print(
        "ANALYZER_IMPLEMENTATION=NO"
    )

    print(
        "REPAIR_IMPLEMENTATION=NO"
    )

    print(
        "===== PROVIDER-FREE SAME-WINDOW RESUME QUALIFICATION FINISHED ====="
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
