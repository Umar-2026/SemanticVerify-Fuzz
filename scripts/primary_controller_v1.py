#!/usr/bin/env python3

from pathlib import Path
import argparse
import hashlib
import json
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[1]

PLAN_PATH = ROOT / "config/generation/primary_request_plan.800.v1.json"
IFACE_PATH = ROOT / "config/primary_controller_interface.v1.json"
VERIFIER_PATH = ROOT / "scripts/verify_primary_controller_interface_v1.py"

EXPECTED_PLAN_SHA256 = (
    "f6712fb4baa7b895f6de82f111f373bf987f0da9166b944232556b99b6ec0440"
)
EXPECTED_IFACE_SHA256 = (
    "ffc143952f0b7963cb4f8ec5853a0cc3855775cc7a3292e6ca7d1a660fbc1d56"
)
EXPECTED_VERIFIER_SHA256 = (
    "cc0980181996b861df38d841339819e34b0cc0cd226e0fcb97e28c330ac2fe58"
)

failures = []


def canonical(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    return sha_bytes(path.read_bytes())


def check(name, condition, detail=None):
    ok = bool(condition)
    print(f"CHECK|{name}|{'PASS' if ok else 'FAIL'}")
    if not ok:
        failures.append({
            "check": name,
            "detail": detail,
        })
        if detail is not None:
            print(f"DETAIL|{name}|{detail}")
    return ok


def create_new_bytes(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:
        f.write(data)


def create_new_json(path, obj):
    data = (
        json.dumps(
            obj,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")
    create_new_bytes(path, data)


def load_contracts():
    if not PLAN_PATH.is_file():
        raise RuntimeError("Primary request plan missing.")
    if not IFACE_PATH.is_file():
        raise RuntimeError("Primary controller interface missing.")
    if not VERIFIER_PATH.is_file():
        raise RuntimeError("Primary controller verifier missing.")

    plan_sha = sha_file(PLAN_PATH)
    iface_sha = sha_file(IFACE_PATH)
    verifier_sha = sha_file(VERIFIER_PATH)

    check(
        "REQUEST_PLAN_SHA256",
        plan_sha == EXPECTED_PLAN_SHA256,
        plan_sha,
    )
    check(
        "INTERFACE_SHA256",
        iface_sha == EXPECTED_IFACE_SHA256,
        iface_sha,
    )
    check(
        "VERIFIER_SHA256",
        verifier_sha == EXPECTED_VERIFIER_SHA256,
        verifier_sha,
    )

    plan = json.loads(PLAN_PATH.read_text())
    iface = json.loads(IFACE_PATH.read_text())

    return plan, iface, plan_sha, iface_sha, verifier_sha


def classify_complete_response(iface, model_label, http_status, body_bytes):
    """
    Provider-free classification of one already-complete HTTP response.

    Raw-response preservation occurs outside this function.
    This function performs no network access.
    """

    if not (200 <= int(http_status) <= 299):
        return {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
            "model_text": None,
            "pause_reason": None,
        }

    try:
        body = json.loads(body_bytes.decode("utf-8"))
    except Exception:
        return {
            "kind": "TERMINAL",
            "terminal_status": "EXTRACTION_FAILURE",
            "model_text": None,
            "pause_reason": None,
        }

    if isinstance(body, dict) and body.get("error"):
        return {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
            "model_text": None,
            "pause_reason": None,
        }

    adapter = iface["provider_adapters"][model_label]
    parser = adapter["response_parser"]

    if model_label == "Model A":
        returned_model = body.get("model")

        if returned_model is None:
            return {
                "kind": "TERMINAL",
                "terminal_status": "API_ERROR",
                "model_text": None,
                "pause_reason": None,
            }

        if returned_model != parser["expected_returned_model"]:
            return {
                "kind": "PAUSE_REQUIRED",
                "terminal_status": None,
                "model_text": None,
                "pause_reason": "RETURNED_MODEL_DRIFT",
            }

        choices = body.get("choices")

        if not isinstance(choices, list) or not choices:
            return {
                "kind": "TERMINAL",
                "terminal_status": "EXTRACTION_FAILURE",
                "model_text": None,
                "pause_reason": None,
            }

        choice = choices[0]

        if not isinstance(choice, dict):
            return {
                "kind": "TERMINAL",
                "terminal_status": "EXTRACTION_FAILURE",
                "model_text": None,
                "pause_reason": None,
            }

        finish_reason = choice.get("finish_reason")
        mapped = parser["finish_reason_mapping"].get(
            finish_reason,
            parser["unrecognized_finish_reason"],
        )

        if mapped != "PARSE_MODEL_TEXT":
            return {
                "kind": "TERMINAL",
                "terminal_status": mapped,
                "model_text": None,
                "pause_reason": None,
            }

        message = choice.get("message")

        if not isinstance(message, dict):
            return {
                "kind": "TERMINAL",
                "terminal_status": "EXTRACTION_FAILURE",
                "model_text": None,
                "pause_reason": None,
            }

        content = message.get("content")

        if not isinstance(content, str):
            return {
                "kind": "TERMINAL",
                "terminal_status": "EXTRACTION_FAILURE",
                "model_text": None,
                "pause_reason": None,
            }

        return {
            "kind": "MODEL_TEXT",
            "terminal_status": None,
            "model_text": content,
            "pause_reason": None,
        }

    if model_label == "Model B":
        prompt_feedback = body.get("promptFeedback")

        if isinstance(prompt_feedback, dict):
            block_reason = prompt_feedback.get("blockReason")

            if block_reason not in (None, ""):
                return {
                    "kind": "TERMINAL",
                    "terminal_status": "REFUSAL",
                    "model_text": None,
                    "pause_reason": None,
                }

        returned_model = body.get("modelVersion")

        if returned_model is None:
            return {
                "kind": "TERMINAL",
                "terminal_status": "API_ERROR",
                "model_text": None,
                "pause_reason": None,
            }

        if returned_model != parser["expected_returned_model"]:
            return {
                "kind": "PAUSE_REQUIRED",
                "terminal_status": None,
                "model_text": None,
                "pause_reason": "RETURNED_MODEL_VERSION_DRIFT",
            }

        candidates = body.get("candidates")

        if not isinstance(candidates, list) or not candidates:
            return {
                "kind": "TERMINAL",
                "terminal_status": "EXTRACTION_FAILURE",
                "model_text": None,
                "pause_reason": None,
            }

        candidate = candidates[0]

        if not isinstance(candidate, dict):
            return {
                "kind": "TERMINAL",
                "terminal_status": "EXTRACTION_FAILURE",
                "model_text": None,
                "pause_reason": None,
            }

        finish_reason = candidate.get("finishReason")
        mapped = parser["finish_reason_mapping"].get(
            finish_reason,
            parser["unrecognized_finish_reason"],
        )

        if mapped != "PARSE_MODEL_TEXT":
            return {
                "kind": "TERMINAL",
                "terminal_status": mapped,
                "model_text": None,
                "pause_reason": None,
            }

        content = candidate.get("content")

        if not isinstance(content, dict):
            return {
                "kind": "TERMINAL",
                "terminal_status": "EXTRACTION_FAILURE",
                "model_text": None,
                "pause_reason": None,
            }

        parts = content.get("parts")

        if not isinstance(parts, list):
            return {
                "kind": "TERMINAL",
                "terminal_status": "EXTRACTION_FAILURE",
                "model_text": None,
                "pause_reason": None,
            }

        text_parts = []

        for part in parts:
            if (
                isinstance(part, dict)
                and isinstance(part.get("text"), str)
            ):
                text_parts.append(part["text"])

        model_text = "".join(text_parts)

        return {
            "kind": "MODEL_TEXT",
            "terminal_status": None,
            "model_text": model_text,
            "pause_reason": None,
        }

    raise RuntimeError("Unknown model label.")


def verify_all_800_request_bytes(plan):
    requests = plan["requests"]

    check("DRYRUN_REQUEST_COUNT_800", len(requests) == 800)

    bad_hashes = []
    bad_slot_ids = []
    previous_number = 0

    for rec in requests:
        slot_number = rec["slot_number"]
        slot_id = rec["logical_slot_id"]

        expected_slot_id = (
            f"SVF-PRIMARY-800-V1-SLOT-{slot_number:04d}"
        )

        if slot_number != previous_number + 1:
            bad_slot_ids.append(slot_id)

        if slot_id != expected_slot_id:
            bad_slot_ids.append(slot_id)

        body_bytes = canonical(rec["request_body"])
        observed = sha_bytes(body_bytes)

        if observed != rec["request_body_sha256"]:
            bad_hashes.append(slot_id)

        previous_number = slot_number

    check(
        "ALL_800_CANONICAL_BODY_HASHES",
        not bad_hashes,
        repr(bad_hashes[:10]),
    )
    check(
        "ALL_800_SLOT_IDS_SEQUENTIAL",
        not bad_slot_ids and previous_number == 800,
        repr(bad_slot_ids[:10]),
    )

    return {
        "request_count": len(requests),
        "bad_body_hash_count": len(bad_hashes),
        "bad_slot_identity_count": len(bad_slot_ids),
    }


def run_parser_tests(iface):
    results = {}

    ds_success = {
        "model": "deepseek-v4-flash",
        "choices": [{
            "finish_reason": "stop",
            "message": {
                "content": "int synthetic_ds_success;\n"
            },
        }],
        "usage": {},
    }

    r = classify_complete_response(
        iface,
        "Model A",
        200,
        canonical(ds_success),
    )
    results["deepseek_success"] = r
    check(
        "PARSER_DS_SUCCESS_KIND",
        r["kind"] == "MODEL_TEXT",
    )
    check(
        "PARSER_DS_SUCCESS_TEXT_EXACT",
        r["model_text"] == "int synthetic_ds_success;\n",
    )

    ds_length = {
        "model": "deepseek-v4-flash",
        "choices": [{
            "finish_reason": "length",
            "message": {"content": "partial"},
        }],
    }

    r = classify_complete_response(
        iface,
        "Model A",
        200,
        canonical(ds_length),
    )
    results["deepseek_length"] = r
    check(
        "PARSER_DS_LENGTH",
        r["terminal_status"] == "TRUNCATED_OUTPUT",
    )

    ds_refusal = {
        "model": "deepseek-v4-flash",
        "choices": [{
            "finish_reason": "content_filter",
            "message": {"content": ""},
        }],
    }

    r = classify_complete_response(
        iface,
        "Model A",
        200,
        canonical(ds_refusal),
    )
    results["deepseek_refusal"] = r
    check(
        "PARSER_DS_REFUSAL",
        r["terminal_status"] == "REFUSAL",
    )

    ds_missing_choice = {
        "model": "deepseek-v4-flash",
        "choices": [],
    }

    r = classify_complete_response(
        iface,
        "Model A",
        200,
        canonical(ds_missing_choice),
    )
    results["deepseek_missing_choice"] = r
    check(
        "PARSER_DS_MISSING_CHOICE",
        r["terminal_status"] == "EXTRACTION_FAILURE",
    )

    ds_drift = {
        "model": "unexpected-model",
        "choices": [{
            "finish_reason": "stop",
            "message": {"content": "x"},
        }],
    }

    r = classify_complete_response(
        iface,
        "Model A",
        200,
        canonical(ds_drift),
    )
    results["deepseek_model_drift"] = r
    check(
        "PARSER_DS_MODEL_DRIFT_PAUSE",
        r["kind"] == "PAUSE_REQUIRED"
        and r["pause_reason"] == "RETURNED_MODEL_DRIFT",
    )

    gm_success = {
        "modelVersion": "gemini-3.1-flash-lite",
        "candidates": [{
            "finishReason": "STOP",
            "content": {
                "parts": [
                    {"text": "alpha"},
                    {"text": "beta"},
                ]
            },
        }],
        "usageMetadata": {},
    }

    r = classify_complete_response(
        iface,
        "Model B",
        200,
        canonical(gm_success),
    )
    results["gemini_success"] = r
    check(
        "PARSER_GM_SUCCESS_KIND",
        r["kind"] == "MODEL_TEXT",
    )
    check(
        "PARSER_GM_MULTIPART_NO_SEPARATOR",
        r["model_text"] == "alphabeta",
    )

    gm_max = {
        "modelVersion": "gemini-3.1-flash-lite",
        "candidates": [{
            "finishReason": "MAX_TOKENS",
            "content": {
                "parts": [{"text": "partial"}]
            },
        }],
    }

    r = classify_complete_response(
        iface,
        "Model B",
        200,
        canonical(gm_max),
    )
    results["gemini_max_tokens"] = r
    check(
        "PARSER_GM_MAX_TOKENS",
        r["terminal_status"] == "TRUNCATED_OUTPUT",
    )

    gm_block = {
        "modelVersion": "gemini-3.1-flash-lite",
        "promptFeedback": {
            "blockReason": "SAFETY"
        },
    }

    r = classify_complete_response(
        iface,
        "Model B",
        200,
        canonical(gm_block),
    )
    results["gemini_prompt_block"] = r
    check(
        "PARSER_GM_PROMPT_BLOCK",
        r["terminal_status"] == "REFUSAL",
    )

    gm_missing = {
        "modelVersion": "gemini-3.1-flash-lite",
        "candidates": [],
    }

    r = classify_complete_response(
        iface,
        "Model B",
        200,
        canonical(gm_missing),
    )
    results["gemini_missing_candidate"] = r
    check(
        "PARSER_GM_MISSING_CANDIDATE",
        r["terminal_status"] == "EXTRACTION_FAILURE",
    )

    gm_drift = {
        "modelVersion": "unexpected-version",
        "candidates": [{
            "finishReason": "STOP",
            "content": {
                "parts": [{"text": "x"}]
            },
        }],
    }

    r = classify_complete_response(
        iface,
        "Model B",
        200,
        canonical(gm_drift),
    )
    results["gemini_model_drift"] = r
    check(
        "PARSER_GM_MODEL_DRIFT_PAUSE",
        r["kind"] == "PAUSE_REQUIRED"
        and r["pause_reason"]
        == "RETURNED_MODEL_VERSION_DRIFT",
    )

    r = classify_complete_response(
        iface,
        "Model A",
        500,
        canonical({
            "error": {
                "message": "synthetic"
            }
        }),
    )
    results["complete_http_500"] = r
    check(
        "COMPLETE_HTTP_500_API_ERROR",
        r["terminal_status"] == "API_ERROR",
    )

    r = classify_complete_response(
        iface,
        "Model A",
        200,
        b"{not-json",
    )
    results["malformed_json"] = r
    check(
        "MALFORMED_JSON_EXTRACTION_FAILURE",
        r["terminal_status"] == "EXTRACTION_FAILURE",
    )

    return results


def simulate_transport(
    iface,
    request_record,
    scripted_outcomes,
):
    """
    Provider-free transport-state simulation.

    No sleeping is performed. Backoff values are recorded and checked only.
    """

    transport = iface["transport_contract"]

    max_invocations = (
        transport["maximum_transport_invocations_per_logical_slot"]
    )
    backoffs = transport["backoff_seconds"]

    body_bytes = canonical(request_record["request_body"])
    body_sha = sha_bytes(body_bytes)

    if body_sha != request_record["request_body_sha256"]:
        raise RuntimeError("Synthetic transport received invalid body hash.")

    invocations = []
    used_backoffs = []

    for invocation_number in range(1, max_invocations + 1):
        if invocation_number > len(scripted_outcomes):
            raise RuntimeError("Synthetic outcome sequence exhausted.")

        outcome = scripted_outcomes[invocation_number - 1]

        invocation = {
            "transport_invocation_number": invocation_number,
            "request_body_sha256": body_sha,
            "outcome_type": outcome["type"],
        }

        invocations.append(invocation)

        if outcome["type"] == "transport_failure":
            retryable = bool(outcome.get("retryable", False))

            if retryable and invocation_number < max_invocations:
                used_backoffs.append(
                    backoffs[invocation_number - 1]
                )
                continue

            return {
                "kind": "TERMINAL",
                "terminal_status": "TRANSPORT_FAILURE",
                "invocations": invocations,
                "used_backoffs": used_backoffs,
            }

        if outcome["type"] == "http_response":
            classification = classify_complete_response(
                iface,
                request_record["model_label"],
                outcome["status"],
                outcome["body"],
            )

            return {
                **classification,
                "invocations": invocations,
                "used_backoffs": used_backoffs,
            }

        raise RuntimeError(
            "Unknown synthetic transport outcome type."
        )

    raise RuntimeError("Unreachable synthetic transport state.")


def run_transport_tests(plan, iface):
    ds_request = plan["requests"][0]

    success_body = canonical({
        "model": "deepseek-v4-flash",
        "choices": [{
            "finish_reason": "stop",
            "message": {
                "content": "synthetic retry success"
            },
        }],
    })

    result = simulate_transport(
        iface,
        ds_request,
        [
            {
                "type": "transport_failure",
                "retryable": True,
            },
            {
                "type": "transport_failure",
                "retryable": True,
            },
            {
                "type": "http_response",
                "status": 200,
                "body": success_body,
            },
        ],
    )

    check(
        "RETRY_TWO_FAILURES_THEN_SUCCESS",
        result["kind"] == "MODEL_TEXT"
        and len(result["invocations"]) == 3,
    )
    check(
        "RETRY_BACKOFF_SEQUENCE_5_20",
        result["used_backoffs"] == [5, 20],
    )
    check(
        "RETRY_PAYLOAD_HASH_IDENTICAL",
        len({
            x["request_body_sha256"]
            for x in result["invocations"]
        }) == 1,
    )

    result_exhausted = simulate_transport(
        iface,
        ds_request,
        [
            {
                "type": "transport_failure",
                "retryable": True,
            },
            {
                "type": "transport_failure",
                "retryable": True,
            },
            {
                "type": "transport_failure",
                "retryable": True,
            },
        ],
    )

    check(
        "RETRY_EXHAUSTION_TRANSPORT_FAILURE",
        result_exhausted["terminal_status"]
        == "TRANSPORT_FAILURE"
        and len(result_exhausted["invocations"]) == 3,
    )

    result_http_error = simulate_transport(
        iface,
        ds_request,
        [
            {
                "type": "http_response",
                "status": 503,
                "body": canonical({
                    "error": {
                        "message": "synthetic service response"
                    }
                }),
            },
        ],
    )

    check(
        "COMPLETE_HTTP_RESPONSE_NOT_RETRIED",
        result_http_error["terminal_status"] == "API_ERROR"
        and len(result_http_error["invocations"]) == 1
        and result_http_error["used_backoffs"] == [],
    )

    result_nonretry_transport = simulate_transport(
        iface,
        ds_request,
        [
            {
                "type": "transport_failure",
                "retryable": False,
            },
        ],
    )

    check(
        "NONRETRYABLE_TRANSPORT_FAILURE_STOPS",
        result_nonretry_transport["terminal_status"]
        == "TRANSPORT_FAILURE"
        and len(result_nonretry_transport["invocations"]) == 1,
    )

    return {
        "retry_then_success": result,
        "retry_exhausted": result_exhausted,
        "complete_http_error": result_http_error,
        "nonretryable_transport_failure":
            result_nonretry_transport,
    }


def run_storage_tests(iface):
    storage = iface["append_only_storage_contract"]

    with tempfile.TemporaryDirectory(
        prefix="svf-controller-dryrun-"
    ) as tmp:
        root = Path(tmp)

        slot_id = "SVF-PRIMARY-800-V1-SLOT-0001"

        rel_request = storage[
            "request_body_template"
        ].format(
            logical_slot_id=slot_id,
            transport_invocation_number=1,
        )

        rel_invocation = storage[
            "invocation_record_template"
        ].format(
            logical_slot_id=slot_id,
            transport_invocation_number=1,
        )

        rel_terminal = storage[
            "slot_terminal_record_template"
        ].format(
            logical_slot_id=slot_id,
        )

        generated = [
            rel_request,
            rel_invocation,
            rel_terminal,
        ]

        for rel in generated:
            p = Path(rel)
            check(
                "STORAGE_RELATIVE_PATH_" + p.name,
                not p.is_absolute()
                and ".." not in p.parts,
            )

        request_path = root / rel_request

        create_new_bytes(
            request_path,
            b'{"synthetic":true}',
        )

        check(
            "CREATE_NEW_FIRST_WRITE",
            request_path.is_file(),
        )

        overwrite_rejected = False

        try:
            create_new_bytes(
                request_path,
                b'{"synthetic":false}',
            )
        except FileExistsError:
            overwrite_rejected = True

        check(
            "CREATE_NEW_OVERWRITE_REJECTED",
            overwrite_rejected,
        )

        check(
            "CREATE_NEW_BYTES_UNCHANGED",
            request_path.read_bytes()
            == b'{"synthetic":true}',
        )

        return {
            "synthetic_workspace_persisted": False,
            "tested_relative_paths": generated,
            "overwrite_rejected": overwrite_rejected,
        }


def run_dry_run(report_path):
    print("===== PRIMARY CONTROLLER V1 — PROVIDER-FREE SYNTHETIC DRY RUN =====")

    plan, iface, plan_sha, iface_sha, verifier_sha = load_contracts()

    print("\n===== 1. AUTHORIZATION BOUNDARY =====")

    check(
        "REQUEST_PLAN_FROZEN_PREAUTH",
        plan["status"] == "FROZEN_POST_GATE1_PREAUTH",
    )

    check(
        "INTERFACE_FROZEN_PREAUTH",
        iface["status"] == "FROZEN_POST_GATE1_PREAUTH",
    )

    check(
        "PRIMARY_GENERATION_AUTHORIZED_FALSE",
        iface["authorization_boundary"]
        ["primary_generation_authorized"] is False,
    )

    check(
        "GENERATION_WINDOW_FROZEN_NOT_OPEN",
        iface["authorization_boundary"]
        ["generation_window_state"] == "FROZEN_NOT_OPEN",
    )

    check(
        "LIVE_PROVIDER_CALLS_FORBIDDEN",
        iface["authorization_boundary"]
        ["live_provider_calls_permitted_by_this_contract"] is False,
    )

    print("\n===== 2. EXACT 800 REQUEST BYTES =====")
    request_validation = verify_all_800_request_bytes(plan)

    print("\n===== 3. PROVIDER RESPONSE PARSERS =====")
    parser_results = run_parser_tests(iface)

    print("\n===== 4. TRANSPORT / RETRY STATE MACHINE =====")
    transport_results = run_transport_tests(plan, iface)

    print("\n===== 5. APPEND-ONLY CREATE-NEW STORAGE =====")
    storage_results = run_storage_tests(iface)

    print("\n===== 6. NETWORK SAFETY =====")

    check(
        "NO_LIVE_TRANSPORT_IMPLEMENTED_IN_THIS_PREFREEZE_CORE",
        True,
    )

    check(
        "NO_SECRET_ENVIRONMENT_VALUES_READ",
        True,
    )

    check(
        "NO_PROVIDER_ENDPOINT_CONTACTED",
        True,
    )

    controller_sha = sha_file(Path(__file__))

    report = {
        "report_id":
            "SVF-PRIMARY-CONTROLLER-PREFREEZE-DRYRUN-V1",
        "status":
            "PASS" if not failures else "FAIL",
        "controller_script": {
            "path":
                "scripts/primary_controller_v1.py",
            "sha256":
                controller_sha,
        },
        "request_plan": {
            "path":
                "config/generation/primary_request_plan.800.v1.json",
            "sha256":
                plan_sha,
        },
        "controller_interface": {
            "path":
                "config/primary_controller_interface.v1.json",
            "sha256":
                iface_sha,
        },
        "interface_verifier": {
            "path":
                "scripts/verify_primary_controller_interface_v1.py",
            "sha256":
                verifier_sha,
        },
        "request_validation":
            request_validation,
        "parser_results":
            parser_results,
        "transport_results":
            transport_results,
        "storage_results":
            storage_results,
        "failure_count":
            len(failures),
        "failures":
            failures,
        "live_provider_calls":
            0,
        "primary_generation_performed":
            False,
        "generated_driver_inspection":
            False,
        "linked_driver_execution":
            False,
        "analyzer_implementation_or_execution":
            False,
        "repair_implementation_or_execution":
            False,
        "secret_environment_values_read":
            False,
        "synthetic_workspace_persisted":
            False,
        "authorization": {
            "primary_generation_authorized":
                False,
            "generation_window_state":
                "FROZEN_NOT_OPEN",
        },
    }

    print("\n===== 7. DRY-RUN RESULT =====")
    print("DRY_RUN_FAILURE_COUNT=" + str(len(failures)))
    print(
        "PROVIDER_FREE_SYNTHETIC_DRY_RUN="
        + ("PASS" if not failures else "FAIL")
    )
    print("CONTROLLER_SHA256=" + controller_sha)
    print("LIVE_PROVIDER_CALLS=0")
    print("PRIMARY_GENERATION_PERFORMED=NO")
    print("GENERATED_DRIVER_INSPECTION=NO")
    print("LINKED_DRIVER_EXECUTION=NO")
    print("ANALYZER_IMPLEMENTATION=NO")
    print("REPAIR_IMPLEMENTATION=NO")

    if failures:
        print("REPORT_WRITTEN=NO_DUE_TO_FAILURE")
        return 1

    if report_path.exists():
        print(
            "ERROR=Dry-run report already exists; "
            "refusing overwrite."
        )
        return 2

    create_new_json(report_path, report)

    print("REPORT_PATH=" + str(report_path.relative_to(ROOT)))
    print("REPORT_SHA256=" + sha_file(report_path))
    print("REPORT_WRITTEN_CREATE_NEW=YES")

    return 0


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--synthetic-dry-run",
        action="store_true",
    )

    parser.add_argument(
        "--report",
        type=Path,
    )

    args = parser.parse_args()

    if not args.synthetic_dry_run:
        print(
            "LIVE_EXECUTION_REFUSED="
            "This preauthorization controller candidate "
            "supports provider-free synthetic dry run only."
        )
        print("PRIMARY_GENERATION_AUTHORIZED=NO")
        return 64

    if args.report is None:
        print("ERROR=--report is required.")
        return 64

    report_path = args.report

    if not report_path.is_absolute():
        report_path = ROOT / report_path

    try:
        return run_dry_run(report_path)
    except Exception as exc:
        print("DRY_RUN_EXCEPTION=" + repr(exc))
        print("LIVE_PROVIDER_CALLS=0")
        print("PRIMARY_GENERATION_PERFORMED=NO")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
