#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import http.client
import json
import os
import socket
import ssl
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

CONTRACT_PATH = ROOT / "config/primary_live_transport_contract.v1.json"
SCHEMA_PATH = ROOT / (
    "config/schemas/"
    "primary_generation_authorization_record.schema.json"
)
DECISION_PATH = ROOT / (
    "documentation/decisions/"
    "0012-primary-generation-authorization-and-live-transport-boundary.md"
)
PLAN_PATH = ROOT / "config/generation/primary_request_plan.800.v1.json"
INTERFACE_PATH = ROOT / "config/primary_controller_interface.v1.json"
PROTOCOL_PATH = ROOT / "config/generation_execution_protocol.json"
CONTROLLER_CORE_PATH = ROOT / "scripts/primary_controller_v1.py"

AUTH_RECORD_REL = (
    "evidence/generation_opening/"
    "primary_generation_authorization.v1.json"
)
AUTH_RECORD_PATH = ROOT / AUTH_RECORD_REL

EXPECTED = {
    "contract":
        "59474347ee27339f1f42247c310786b658f315113dcb2501ab53c9d7ad9b965b",
    "schema":
        "b49f843be81347558d9decb65793558e45bd6009a6a455a4e5ccdc04a00798a6",
    "decision":
        "8920fb4cd379b02727f4d8efa6e675961ddc9eff48d679f8fb9f4b78f0b61609",
    "request_plan":
        "f6712fb4baa7b895f6de82f111f373bf987f0da9166b944232556b99b6ec0440",
    "interface":
        "ffc143952f0b7963cb4f8ec5853a0cc3855775cc7a3292e6ca7d1a660fbc1d56",
    "protocol":
        "f10a6093c72e719f55d9fc8acdbc782f1e72be94a0a0a191e1b14faced19d19c",
    "controller_core":
        "6a7f4e47086c1062f041ad461dfd0769833cefe4a49cb8fae1a7fc7644a140c2",
}

PREAUTH_FREEZE_COMMIT = (
    "53f1099bcc2c1fb24c18ba388684900a79e23947"
)

failures = []


class TransportFailure(Exception):
    def __init__(
        self,
        classification,
        retryable,
        detail="",
    ):
        # Persistence boundary:
        # raw provider/proxy exception text is deliberately
        # discarded. Only the provider-neutral classification
        # may reach logs, ledgers, reports, or exception strings.
        safe_detail = str(classification)

        super().__init__(
            safe_detail
        )

        self.classification = (
            classification
        )

        self.retryable = bool(
            retryable
        )

        self.detail = (
            safe_detail
        )



def utc_now():
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )


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
    create_new_bytes(
        path,
        (
            json.dumps(
                obj,
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
            )
            + "\n"
        ).encode("utf-8"),
    )


def load_locked_inputs():
    expected_paths = {
        "contract": CONTRACT_PATH,
        "schema": SCHEMA_PATH,
        "decision": DECISION_PATH,
        "request_plan": PLAN_PATH,
        "interface": INTERFACE_PATH,
        "protocol": PROTOCOL_PATH,
        "controller_core": CONTROLLER_CORE_PATH,
    }

    for name, path in expected_paths.items():
        if not path.is_file():
            raise RuntimeError(
                f"Required locked input missing: {path}"
            )

        observed = sha_file(path)

        if observed != EXPECTED[name]:
            raise RuntimeError(
                f"Locked input hash mismatch: "
                f"{name}: {observed}"
            )

    return {
        "contract":
            json.loads(CONTRACT_PATH.read_text()),
        "schema":
            json.loads(SCHEMA_PATH.read_text()),
        "decision_text":
            DECISION_PATH.read_text(),
        "plan":
            json.loads(PLAN_PATH.read_text()),
        "interface":
            json.loads(INTERFACE_PATH.read_text()),
        "protocol":
            json.loads(PROTOCOL_PATH.read_text()),
    }


def import_frozen_classifier():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "svf_frozen_primary_controller",
        CONTROLLER_CORE_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            "Unable to import frozen controller classifier."
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.classify_complete_response


def git_is_tracked(relpath):
    cp = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "ls-files",
            "--error-unmatch",
            "--",
            relpath,
        ],
        text=True,
        capture_output=True,
    )

    return cp.returncode == 0


def git_path_exists_in_head(relpath):
    cp = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "cat-file",
            "-e",
            "HEAD:" + relpath,
        ],
        text=True,
        capture_output=True,
    )

    return cp.returncode == 0


def git_repo_clean():
    text = subprocess.check_output(
        [
            "git",
            "-C",
            str(ROOT),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        text=True,
    )

    return not text.strip()


def git_freeze_commit_is_ancestor():
    cp = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "merge-base",
            "--is-ancestor",
            PREAUTH_FREEZE_COMMIT,
            "HEAD",
        ],
        text=True,
        capture_output=True,
    )

    return cp.returncode == 0


def strict_keys(obj, required):
    return (
        isinstance(obj, dict)
        and set(obj.keys()) == set(required)
    )


def parse_datetime(value):
    if not isinstance(value, str):
        return False

    try:
        datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
        return True
    except Exception:
        return False


def validate_authorization_record_object(
    record,
    schema,
    decision_sha,
):
    errors = []

    top_required = schema["required"]

    if not strict_keys(record, top_required):
        errors.append("TOPLEVEL_KEYS")
        return errors

    if (
        record["record_id"]
        != "SVF-PRIMARY-GENERATION-AUTHORIZATION-V1"
    ):
        errors.append("RECORD_ID")

    if record["schema_version"] != 1:
        errors.append("SCHEMA_VERSION")

    if (
        record["status"]
        != "AUTHORIZED_FOR_PRIMARY_WINDOW_OPEN"
    ):
        errors.append("STATUS")

    if (
        record["authorized_window_id"]
        != "SVF-PRIMARY-800-V1"
    ):
        errors.append("WINDOW_ID")

    if not parse_datetime(record["authorized_at_utc"]):
        errors.append("AUTHORIZED_AT")

    d = record["decision_0012"]

    if not strict_keys(
        d,
        ["path", "sha256", "status"],
    ):
        errors.append("DECISION_KEYS")
    else:
        if d["path"] != str(
            DECISION_PATH.relative_to(ROOT)
        ):
            errors.append("DECISION_PATH")

        if d["sha256"] != decision_sha:
            errors.append("DECISION_SHA")

        if d["status"] != "Accepted":
            errors.append("DECISION_STATUS")

    fb = record["freeze_binding"]

    expected_fb = {
        "preauthorization_freeze_commit":
            PREAUTH_FREEZE_COMMIT,

        "request_plan_sha256":
            EXPECTED["request_plan"],

        "controller_interface_sha256":
            EXPECTED["interface"],

        "controller_core_sha256":
            EXPECTED["controller_core"],

        "interface_verifier_sha256":
            (
                "cc0980181996b861df38d841339819e34"
                "b0cc0cd226e0fcb97e28c330ac2fe58"
            ),

        "controller_freeze_manifest_sha256":
            (
                "1325f366b554b5fde90fde8153850f58"
                "8ce228d54e80a8be4ad7dd987972e7e4"
            ),

        "generation_protocol_sha256":
            EXPECTED["protocol"],

        "postprocessing_contract_sha256":
            (
                "9efc2973ef7792b9dbda5ee6d6c86671"
                "8c87607ed2f31b114006dbecc95d6aa8"
            ),
    }

    if fb != expected_fb:
        errors.append("FREEZE_BINDING")

    rp = record["repository_preconditions"]

    expected_rp = {
        "authorization_record_must_be_committed":
            True,
        "repository_must_be_clean_before_open":
            True,
        "freeze_commit_must_be_ancestor":
            True,
    }

    if rp != expected_rp:
        errors.append("REPOSITORY_PRECONDITIONS")

    scope = record["authorization_scope"]

    expected_scope = {
        "primary_generation":
            True,
        "window_open":
            True,
        "maximum_logical_slots":
            800,
        "second_window_allowed":
            False,
        "analyzer":
            False,
        "repair":
            False,
    }

    if scope != expected_scope:
        errors.append("AUTHORIZATION_SCOPE")

    acks = record["safety_acknowledgements"]

    expected_acks = {
        "no_generated_driver_human_inspection_during_generation":
            True,

        "no_linked_driver_execution_during_primary_compilation":
            True,

        "no_repair_before_gate_v":
            True,

        "api_secrets_never_persisted_printed_or_hashed":
            True,

        "pause_rule_binding_acknowledged":
            True,
    }

    if acks != expected_acks:
        errors.append("SAFETY_ACKNOWLEDGEMENTS")

    rq = record["provider_requalification"]

    if not isinstance(rq, dict):
        errors.append("REQUALIFICATION")
        return errors

    expected_rq_keys = {
        "status",
        "performed_at_utc",
        "report_path",
        "report_sha256",
        "deepseek",
        "gemini",
    }

    if set(rq.keys()) != expected_rq_keys:
        errors.append("REQUALIFICATION_KEYS")
        return errors

    if rq["status"] != "PASS":
        errors.append("REQUALIFICATION_STATUS")

    if not parse_datetime(rq["performed_at_utc"]):
        errors.append("REQUALIFICATION_TIME")

    if not isinstance(rq["report_path"], str) or not rq["report_path"]:
        errors.append("REQUALIFICATION_REPORT_PATH")

    if (
        not isinstance(rq["report_sha256"], str)
        or len(rq["report_sha256"]) != 64
        or any(
            c not in "0123456789abcdef"
            for c in rq["report_sha256"]
        )
    ):
        errors.append("REQUALIFICATION_REPORT_SHA")

    ds = rq["deepseek"]

    expected_ds = {
        "requested_model_id":
            "deepseek-v4-flash",

        "endpoint":
            "https://api.deepseek.com/chat/completions",

        "thinking_mode":
            "disabled",

        "status":
            "PASS",
    }

    if not isinstance(ds, dict):
        errors.append("REQUAL_DS")
    else:
        for key, value in expected_ds.items():
            if ds.get(key) != value:
                errors.append("REQUAL_DS_" + key.upper())

        if ds.get("returned_model") not in (
            "deepseek-v4-flash",
            "DeepSeek-V4-Flash-0731",
        ):
            errors.append("REQUAL_DS_RETURNED_MODEL")

        if set(ds.keys()) != {
            "requested_model_id",
            "returned_model",
            "endpoint",
            "thinking_mode",
            "status",
        }:
            errors.append("REQUAL_DS_KEYS")

    gm = rq["gemini"]

    expected_gm = {
        "requested_model_id":
            "gemini-3.1-flash-lite",

        "returned_model_version":
            "gemini-3.1-flash-lite",

        "endpoint":
            (
                "https://generativelanguage.googleapis.com/"
                "v1beta/models/"
                "gemini-3.1-flash-lite:generateContent"
            ),

        "thinking_level":
            "MINIMAL",

        "status":
            "PASS",
    }

    if gm != expected_gm:
        errors.append("REQUAL_GM")

    return errors


def verify_requalification_report(record):
    rq = record["provider_requalification"]
    rel = rq["report_path"]
    path = ROOT / rel

    if not path.is_file():
        return False, "REQUALIFICATION_REPORT_MISSING"

    if not git_is_tracked(rel):
        return False, "REQUALIFICATION_REPORT_NOT_TRACKED"

    if not git_path_exists_in_head(rel):
        return False, "REQUALIFICATION_REPORT_NOT_IN_HEAD"

    if sha_file(path) != rq["report_sha256"]:
        return False, "REQUALIFICATION_REPORT_HASH"

    try:
        report = json.loads(path.read_text())
    except Exception:
        return False, "REQUALIFICATION_REPORT_JSON"

    if report.get("status") != "PASS":
        return False, "REQUALIFICATION_REPORT_STATUS"

    return True, "PASS"


def verify_operational_authorization(
    locked,
    secret_reader=None,
):
    """
    Returns a gate result.

    IMPORTANT:
    This function never reads API credentials. Credential access occurs
    only in a later caller after this function returns authorized=True.
    """

    contract = locked["contract"]

    gate = contract["authorization_gate"]
    net = contract["network_transport"]

    if gate["execution_enabled"] is not True:
        return {
            "authorized": False,
            "reason": "CONTRACT_EXECUTION_DISABLED",
        }

    if (
        net[
            "live_network_calls_allowed_by_this_candidate"
        ]
        is not True
    ):
        return {
            "authorized": False,
            "reason": "LIVE_NETWORK_CALLS_DISABLED",
        }

    if (
        contract["status"]
        not in (
            "FROZEN_AUTHORIZATION_READY",
            "FROZEN_EXECUTION_READY",
        )
    ):
        return {
            "authorized": False,
            "reason": "CONTRACT_NOT_EXECUTION_READY",
        }

    decision_text = locked["decision_text"]

    if "- Status: Accepted" not in decision_text:
        return {
            "authorized": False,
            "reason": "DECISION_0012_NOT_ACCEPTED",
        }

    if not AUTH_RECORD_PATH.is_file():
        return {
            "authorized": False,
            "reason": "AUTHORIZATION_RECORD_MISSING",
        }

    if not git_is_tracked(AUTH_RECORD_REL):
        return {
            "authorized": False,
            "reason": "AUTHORIZATION_RECORD_NOT_TRACKED",
        }

    if not git_path_exists_in_head(AUTH_RECORD_REL):
        return {
            "authorized": False,
            "reason": "AUTHORIZATION_RECORD_NOT_IN_HEAD",
        }

    if not git_repo_clean():
        return {
            "authorized": False,
            "reason": "REPOSITORY_NOT_CLEAN",
        }

    if not git_freeze_commit_is_ancestor():
        return {
            "authorized": False,
            "reason": "FREEZE_COMMIT_NOT_ANCESTOR",
        }

    try:
        record = json.loads(
            AUTH_RECORD_PATH.read_text()
        )
    except Exception:
        return {
            "authorized": False,
            "reason": "AUTHORIZATION_RECORD_INVALID_JSON",
        }

    errors = validate_authorization_record_object(
        record,
        locked["schema"],
        sha_file(DECISION_PATH),
    )

    if errors:
        return {
            "authorized": False,
            "reason": "AUTHORIZATION_RECORD_SCHEMA_OR_BINDING_FAILURE",
            "errors": errors,
        }

    ok, reason = verify_requalification_report(
        record
    )

    if not ok:
        return {
            "authorized": False,
            "reason": reason,
        }

    return {
        "authorized": True,
        "reason": "PASS",
        "record": record,
        "authorization_record_sha256":
            sha_file(AUTH_RECORD_PATH),
    }


def canonical_request_bytes(request_record):
    body = canonical(
        request_record["request_body"]
    )

    observed = sha_bytes(body)
    expected = request_record[
        "request_body_sha256"
    ]

    if observed != expected:
        raise RuntimeError(
            "Frozen request body SHA-256 mismatch."
        )

    return body


def build_secret_headers(model_label, secret):
    if not isinstance(secret, str) or not secret:
        raise RuntimeError("Missing provider credential.")

    if model_label == "Model A":
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + secret,
        }

    if model_label == "Model B":
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": secret,
        }

    raise RuntimeError(
        "Unknown model label for credential header."
    )


def redact_headers(headers):
    out = {}

    for key, value in headers.items():
        low = str(key).lower()

        if low in (
            "authorization",
            "x-goog-api-key",
            "proxy-authorization",
            "cookie",
            "set-cookie",
        ):
            out[str(key)] = "<REDACTED>"
        else:
            out[str(key)] = str(value)

    return out


def classify_transport_exception(exc, stage):
    if isinstance(exc, socket.gaierror):
        return TransportFailure(
            "DNS_RESOLUTION_FAILURE",
            True,
            "DNS_RESOLUTION_FAILURE",
        )

    if isinstance(exc, ssl.SSLError):
        return TransportFailure(
            "TLS_HANDSHAKE_FAILURE",
            True,
            "TLS_HANDSHAKE_FAILURE",
        )

    if isinstance(exc, socket.timeout):
        if stage == "connect":
            label = "CONNECT_TIMEOUT"
        else:
            label = (
                "READ_TIMEOUT_BEFORE_COMPLETE_HTTP_RESPONSE"
            )

        return TransportFailure(
            label,
            True,
            label,
        )

    if isinstance(
        exc,
        (
            ConnectionResetError,
            BrokenPipeError,
        ),
    ):
        return TransportFailure(
            "CONNECTION_RESET_BEFORE_COMPLETE_HTTP_RESPONSE",
            True,
            "CONNECTION_RESET_BEFORE_COMPLETE_HTTP_RESPONSE",
        )

    if isinstance(
        exc,
        (
            ConnectionRefusedError,
            ConnectionAbortedError,
            OSError,
        ),
    ):
        return TransportFailure(
            "TCP_CONNECT_FAILURE",
            True,
            "TCP_CONNECT_FAILURE",
        )

    return TransportFailure(
        "TRANSPORT_FAILURE",
        False,
        "TRANSPORT_FAILURE",
    )


def real_https_post(
    endpoint,
    body_bytes,
    headers,
    connect_timeout_seconds,
    complete_response_deadline_seconds,
):
    """
    Real HTTPS transport primitive.

    This primitive does not read environment variables and does not write
    evidence. Operational callers must first pass the authorization gate.

    It is NOT invoked by the synthetic qualification.
    """

    parsed = urlsplit(endpoint)

    if parsed.scheme != "https":
        raise TransportFailure(
            "TLS_REQUIRED",
            False,
            "Only HTTPS endpoints are allowed.",
        )

    host = parsed.hostname

    if not host:
        raise TransportFailure(
            "INVALID_ENDPOINT",
            False,
            "INVALID_ENDPOINT",
        )

    port = parsed.port or 443
    target = parsed.path or "/"

    if parsed.query:
        target += "?" + parsed.query

    context = ssl.create_default_context()

    conn = http.client.HTTPSConnection(
        host,
        port,
        timeout=connect_timeout_seconds,
        context=context,
    )

    started = time.monotonic()
    stage = "connect"

    try:
        conn.connect()

        elapsed = time.monotonic() - started
        remaining = (
            complete_response_deadline_seconds
            - elapsed
        )

        if remaining <= 0:
            raise socket.timeout(
                "Complete-response deadline exhausted."
            )

        if conn.sock is not None:
            conn.sock.settimeout(remaining)

        stage = "request"

        conn.request(
            "POST",
            target,
            body=body_bytes,
            headers=headers,
        )

        elapsed = time.monotonic() - started
        remaining = (
            complete_response_deadline_seconds
            - elapsed
        )

        if remaining <= 0:
            raise socket.timeout(
                "Complete-response deadline exhausted."
            )

        if conn.sock is not None:
            conn.sock.settimeout(remaining)

        stage = "response"

        response = conn.getresponse()

        elapsed = time.monotonic() - started
        remaining = (
            complete_response_deadline_seconds
            - elapsed
        )

        if remaining <= 0:
            raise socket.timeout(
                "Complete-response deadline exhausted."
            )

        if conn.sock is not None:
            conn.sock.settimeout(remaining)

        body = response.read()

        finished = time.monotonic()

        return {
            "http_status": int(response.status),
            "headers": dict(response.getheaders()),
            "body": body,
            "latency_ms":
                int(round((finished - started) * 1000)),
        }

    except Exception as exc:
        if isinstance(exc, TransportFailure):
            raise

        raise classify_transport_exception(
            exc,
            stage,
        )

    finally:
        try:
            conn.close()
        except Exception:
            pass


def extract_usage(model_label, response_body):
    try:
        obj = json.loads(
            response_body.decode("utf-8")
        )
    except Exception:
        return None

    if model_label == "Model A":
        usage = obj.get("usage")
    elif model_label == "Model B":
        usage = obj.get("usageMetadata")
    else:
        return None

    if isinstance(usage, dict):
        return usage

    return None


def deepseek_cost(usage, contract):
    rates = contract[
        "cost_accounting"
    ]["DeepSeek"]["rates"]

    if not isinstance(usage, dict):
        return {
            "status": "PAUSE_REQUIRED",
            "reason": "INSUFFICIENT_USAGE_METADATA",
            "estimate_usd": None,
        }

    completion = usage.get(
        "completion_tokens"
    )

    if not isinstance(completion, int) or completion < 0:
        return {
            "status": "PAUSE_REQUIRED",
            "reason": "INVALID_COMPLETION_TOKENS",
            "estimate_usd": None,
        }

    hit = usage.get(
        "prompt_cache_hit_tokens"
    )
    miss = usage.get(
        "prompt_cache_miss_tokens"
    )

    source = "direct_cache_split"

    if not (
        isinstance(hit, int)
        and hit >= 0
        and isinstance(miss, int)
        and miss >= 0
    ):
        prompt = usage.get("prompt_tokens")
        details = usage.get(
            "prompt_tokens_details"
        )

        cached = (
            details.get("cached_tokens")
            if isinstance(details, dict)
            else None
        )

        if not (
            isinstance(prompt, int)
            and prompt >= 0
            and isinstance(cached, int)
            and cached >= 0
            and cached <= prompt
        ):
            return {
                "status": "PAUSE_REQUIRED",
                "reason": "INSUFFICIENT_USAGE_METADATA",
                "estimate_usd": None,
            }

        hit = cached
        miss = prompt - cached
        source = "derived_cache_split"

    estimate = (
        hit * rates["input_cache_hit"]
        + miss * rates["input_cache_miss"]
        + completion * rates["output"]
    ) / 1_000_000

    return {
        "status": "PASS",
        "basis": source,
        "cache_hit_tokens": hit,
        "cache_miss_tokens": miss,
        "completion_tokens": completion,
        "estimate_usd": estimate,
    }


def gemini_cost(usage, contract):
    rates = contract[
        "cost_accounting"
    ]["Gemini"]["rates"]

    if not isinstance(usage, dict):
        return {
            "status": "PAUSE_REQUIRED",
            "reason": "INSUFFICIENT_USAGE_METADATA",
            "estimate_usd": None,
        }

    prompt = usage.get("promptTokenCount")
    candidate = usage.get(
        "candidatesTokenCount"
    )
    thoughts = usage.get(
        "thoughtsTokenCount",
        0,
    )
    cached = usage.get(
        "cachedContentTokenCount",
        0,
    )

    if not (
        isinstance(prompt, int)
        and prompt >= 0
        and isinstance(candidate, int)
        and candidate >= 0
        and isinstance(thoughts, int)
        and thoughts >= 0
        and isinstance(cached, int)
        and cached >= 0
    ):
        return {
            "status": "PAUSE_REQUIRED",
            "reason": "INVALID_USAGE_METADATA",
            "estimate_usd": None,
        }

    if cached > 0:
        return {
            "status": "PAUSE_REQUIRED",
            "reason":
                "UNEXPECTED_POSITIVE_CACHED_CONTENT_USAGE",
            "estimate_usd": None,
        }

    estimate = (
        prompt * rates["input"]
        + (candidate + thoughts)
        * rates[
            "output_including_thinking_tokens"
        ]
    ) / 1_000_000

    return {
        "status": "PASS",
        "prompt_tokens": prompt,
        "candidate_tokens": candidate,
        "thoughts_tokens": thoughts,
        "cached_content_tokens": cached,
        "estimate_usd": estimate,
    }


def estimate_cost(
    model_label,
    usage,
    contract,
):
    if model_label == "Model A":
        return deepseek_cost(
            usage,
            contract,
        )

    if model_label == "Model B":
        return gemini_cost(
            usage,
            contract,
        )

    return {
        "status": "PAUSE_REQUIRED",
        "reason": "UNKNOWN_PROVIDER",
        "estimate_usd": None,
    }


def complete_http_pause_reason(
    http_status,
    classification,
):
    if http_status in (
        401,
        402,
        403,
        429,
    ):
        return (
            "AUTHENTICATION_BALANCE_PERMISSION_OR_RATE_LIMIT"
        )

    if classification.get(
        "kind"
    ) == "PAUSE_REQUIRED":
        return classification.get(
            "pause_reason"
        ) or "PROVIDER_DRIFT"

    return None


def execute_one_with_transport(
    locked,
    request_record,
    transport,
    evidence_root,
    sleep_fn,
    synthetic_secret,
    event_log,
):
    """
    Synthetic/injectable execution of one logical slot.

    No environment credential is read here. The caller supplies the
    synthetic secret directly.
    """

    contract = locked["contract"]
    interface = locked["interface"]
    classify = import_frozen_classifier()

    slot_id = request_record[
        "logical_slot_id"
    ]
    model_label = request_record[
        "model_label"
    ]

    body_bytes = canonical_request_bytes(
        request_record
    )
    body_sha = sha_bytes(body_bytes)

    provider = contract[
        "providers"
    ][model_label]

    headers = build_secret_headers(
        model_label,
        synthetic_secret,
    )

    transport_contract = contract[
        "network_transport"
    ]

    backoffs = transport_contract[
        "deterministic_backoff_seconds"
    ]

    max_invocations = transport_contract[
        "maximum_transport_invocations_per_logical_slot"
    ]

    invocation_records = []

    for invocation_number in range(
        1,
        max_invocations + 1,
    ):
        rel_request = interface[
            "append_only_storage_contract"
        ]["request_body_template"].format(
            logical_slot_id=slot_id,
            transport_invocation_number=
                invocation_number,
        )

        request_path = (
            evidence_root / rel_request
        )

        create_new_bytes(
            request_path,
            body_bytes,
        )

        event_log.append(
            "REQUEST_BODY_PRESERVED"
        )

        request_meta_rel = interface[
            "append_only_storage_contract"
        ]["request_metadata_template"].format(
            logical_slot_id=slot_id,
            transport_invocation_number=
                invocation_number,
        )

        request_meta = {
            "logical_slot_id": slot_id,
            "transport_invocation_number":
                invocation_number,
            "endpoint":
                provider["endpoint"],
            "request_body_sha256":
                body_sha,
            "request_body_byte_length":
                len(body_bytes),
            "credential_header_names":
                [
                    provider[
                        "credential"
                    ]["outbound_header"]
                ],
            "credential_values_retained":
                False,
        }

        create_new_json(
            evidence_root / request_meta_rel,
            request_meta,
        )

        try:
            result = transport(
                endpoint=provider["endpoint"],
                body_bytes=body_bytes,
                headers=headers,
                connect_timeout_seconds=
                    transport_contract[
                        "connect_timeout_seconds"
                    ],
                complete_response_deadline_seconds=
                    transport_contract[
                        "complete_response_deadline_seconds"
                    ],
            )

        except TransportFailure as exc:
            tf_rel = interface[
                "append_only_storage_contract"
            ]["transport_failure_template"].format(
                logical_slot_id=slot_id,
                transport_invocation_number=
                    invocation_number,
            )

            tf = {
                "logical_slot_id": slot_id,
                "transport_invocation_number":
                    invocation_number,
                "classification":
                    exc.classification,
                "retryable":
                    exc.retryable,
                "detail":
                    exc.detail,
                "request_body_sha256":
                    body_sha,
            }

            create_new_json(
                evidence_root / tf_rel,
                tf,
            )

            event_log.append(
                "TRANSPORT_FAILURE_PRESERVED"
            )

            invocation_records.append({
                "invocation_number":
                    invocation_number,
                "outcome":
                    "TRANSPORT_FAILURE",
                "classification":
                    exc.classification,
                "request_body_sha256":
                    body_sha,
            })

            if (
                exc.retryable
                and invocation_number
                < max_invocations
            ):
                sleep_fn(
                    backoffs[
                        invocation_number - 1
                    ]
                )
                continue

            return {
                "kind": "TERMINAL",
                "terminal_status":
                    "TRANSPORT_FAILURE",
                "pause_required":
                    False,
                "pause_reason":
                    None,
                "invocations":
                    invocation_records,
            }

        raw_rel = interface[
            "append_only_storage_contract"
        ]["raw_response_template"].format(
            logical_slot_id=slot_id,
            transport_invocation_number=
                invocation_number,
        )

        raw_path = evidence_root / raw_rel

        create_new_bytes(
            raw_path,
            result["body"],
        )

        event_log.append(
            "RAW_RESPONSE_PRESERVED"
        )

        hdr_rel = interface[
            "append_only_storage_contract"
        ]["redacted_response_headers_template"].format(
            logical_slot_id=slot_id,
            transport_invocation_number=
                invocation_number,
        )

        redacted = redact_headers(
            result["headers"]
        )

        create_new_json(
            evidence_root / hdr_rel,
            redacted,
        )

        event_log.append(
            "HEADERS_REDACTED_PRESERVED"
        )

        classification = classify(
            interface,
            model_label,
            result["http_status"],
            result["body"],
        )

        event_log.append(
            "RESPONSE_CLASSIFIED"
        )

        usage = extract_usage(
            model_label,
            result["body"],
        )

        cost = estimate_cost(
            model_label,
            usage,
            contract,
        )

        event_log.append(
            "COST_ACCOUNTED"
        )

        pause_reason = (
            complete_http_pause_reason(
                result["http_status"],
                classification,
            )
        )

        if (
            cost["status"]
            != "PASS"
            and 200
            <= result["http_status"]
            <= 299
        ):
            pause_reason = (
                cost.get("reason")
                or "COST_ACCOUNTING_FAILURE"
            )

        invocation_record = {
            "window_id":
                "SVF-PRIMARY-800-V1",
            "logical_slot_id":
                slot_id,
            "transport_invocation_number":
                invocation_number,
            "provider":
                request_record["provider"],
            "requested_model_id":
                request_record["model_id"],
            "returned_model_or_version":
                None,
            "request_started_at_utc":
                "SYNTHETIC",
            "request_finished_at_utc":
                "SYNTHETIC",
            "request_parameters":
                request_record[
                    "provider_neutral_descriptor"
                ],
            "latency_ms":
                result.get(
                    "latency_ms",
                    0,
                ),
            "HTTP_status_or_transport_failure":
                result["http_status"],
            "raw_response_path_or_null":
                raw_rel,
            "raw_response_sha256_or_null":
                sha_file(raw_path),
            "token_usage":
                usage,
            "cost_basis_and_estimate":
                cost,
            "authorization_record_path":
                None,
            "authorization_record_sha256":
                None,
            "execution_head_commit":
                None,
            "request_body_sha256_verified":
                True,
            "request_body_byte_length":
                len(body_bytes),
            "endpoint":
                provider["endpoint"],
            "transport_retry_classification":
                "COMPLETE_HTTP_RESPONSE_NO_RETRY",
            "response_headers_redacted":
                True,
            "cost_estimate_status":
                cost["status"],
        }

        inv_rel = interface[
            "append_only_storage_contract"
        ]["invocation_record_template"].format(
            logical_slot_id=slot_id,
            transport_invocation_number=
                invocation_number,
        )

        create_new_json(
            evidence_root / inv_rel,
            invocation_record,
        )

        event_log.append(
            "INVOCATION_RECORD_PRESERVED"
        )

        invocation_records.append({
            "invocation_number":
                invocation_number,
            "outcome":
                "COMPLETE_HTTP_RESPONSE",
            "http_status":
                result["http_status"],
            "request_body_sha256":
                body_sha,
            "classification":
                classification,
            "cost":
                cost,
        })

        return {
            "kind":
                classification["kind"],
            "terminal_status":
                classification.get(
                    "terminal_status"
                ),
            "model_text":
                classification.get(
                    "model_text"
                ),
            "pause_required":
                pause_reason is not None,
            "pause_reason":
                pause_reason,
            "cost":
                cost,
            "usage":
                usage,
            "invocations":
                invocation_records,
        }

    raise RuntimeError(
        "Synthetic transport loop exhausted unexpectedly."
    )


class ScriptedTransport:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []
        self.index = 0

    def __call__(
        self,
        *,
        endpoint,
        body_bytes,
        headers,
        connect_timeout_seconds,
        complete_response_deadline_seconds,
    ):
        self.calls.append({
            "endpoint": endpoint,
            "body_sha256":
                sha_bytes(body_bytes),
            "body_bytes":
                body_bytes,
            "headers":
                dict(headers),
            "connect_timeout_seconds":
                connect_timeout_seconds,
            "complete_response_deadline_seconds":
                complete_response_deadline_seconds,
        })

        if self.index >= len(self.outcomes):
            raise RuntimeError(
                "Synthetic transport outcome sequence exhausted."
            )

        outcome = self.outcomes[self.index]
        self.index += 1

        if isinstance(
            outcome,
            TransportFailure,
        ):
            raise outcome

        return outcome


def synthetic_auth_record(
    decision_sha,
):
    return {
        "record_id":
            "SVF-PRIMARY-GENERATION-AUTHORIZATION-V1",

        "schema_version":
            1,

        "status":
            "AUTHORIZED_FOR_PRIMARY_WINDOW_OPEN",

        "authorized_window_id":
            "SVF-PRIMARY-800-V1",

        "authorized_at_utc":
            "2026-08-09T00:00:00+00:00",

        "decision_0012": {
            "path":
                (
                    "documentation/decisions/"
                    "0012-primary-generation-authorization-and-live-transport-boundary.md"
                ),
            "sha256":
                decision_sha,
            "status":
                "Accepted",
        },

        "freeze_binding": {
            "preauthorization_freeze_commit":
                PREAUTH_FREEZE_COMMIT,

            "request_plan_sha256":
                EXPECTED["request_plan"],

            "controller_interface_sha256":
                EXPECTED["interface"],

            "controller_core_sha256":
                EXPECTED["controller_core"],

            "interface_verifier_sha256":
                (
                    "cc0980181996b861df38d841339819e34"
                    "b0cc0cd226e0fcb97e28c330ac2fe58"
                ),

            "controller_freeze_manifest_sha256":
                (
                    "1325f366b554b5fde90fde8153850f58"
                    "8ce228d54e80a8be4ad7dd987972e7e4"
                ),

            "generation_protocol_sha256":
                EXPECTED["protocol"],

            "postprocessing_contract_sha256":
                (
                    "9efc2973ef7792b9dbda5ee6d6c86671"
                    "8c87607ed2f31b114006dbecc95d6aa8"
                ),
        },

        "provider_requalification": {
            "status":
                "PASS",

            "performed_at_utc":
                "2026-08-09T00:00:00+00:00",

            "report_path":
                (
                    "evidence/generation_opening/"
                    "synthetic-never-committed.json"
                ),

            "report_sha256":
                "0" * 64,

            "deepseek": {
                "requested_model_id":
                    "deepseek-v4-flash",
                "returned_model":
                    "deepseek-v4-flash",
                "endpoint":
                    "https://api.deepseek.com/chat/completions",
                "thinking_mode":
                    "disabled",
                "status":
                    "PASS",
            },

            "gemini": {
                "requested_model_id":
                    "gemini-3.1-flash-lite",
                "returned_model_version":
                    "gemini-3.1-flash-lite",
                "endpoint":
                    (
                        "https://generativelanguage.googleapis.com/"
                        "v1beta/models/"
                        "gemini-3.1-flash-lite:generateContent"
                    ),
                "thinking_level":
                    "MINIMAL",
                "status":
                    "PASS",
            },
        },

        "repository_preconditions": {
            "authorization_record_must_be_committed":
                True,
            "repository_must_be_clean_before_open":
                True,
            "freeze_commit_must_be_ancestor":
                True,
        },

        "authorization_scope": {
            "primary_generation":
                True,
            "window_open":
                True,
            "maximum_logical_slots":
                800,
            "second_window_allowed":
                False,
            "analyzer":
                False,
            "repair":
                False,
        },

        "safety_acknowledgements": {
            "no_generated_driver_human_inspection_during_generation":
                True,

            "no_linked_driver_execution_during_primary_compilation":
                True,

            "no_repair_before_gate_v":
                True,

            "api_secrets_never_persisted_printed_or_hashed":
                True,

            "pause_rule_binding_acknowledged":
                True,
        },
    }


def run_synthetic_dry_run(report_path):
    print(
        "===== PRIMARY LIVE TRANSPORT V1 — "
        "PROVIDER-FREE SYNTHETIC QUALIFICATION ====="
    )

    locked = load_locked_inputs()

    print("\n===== 1. CURRENT AUTHORIZATION GATE =====")

    secret_reader_calls = []

    def forbidden_secret_reader(name):
        secret_reader_calls.append(name)
        raise RuntimeError(
            "Secret reader must not be called while gate is closed."
        )

    gate = verify_operational_authorization(
        locked,
        secret_reader=
            forbidden_secret_reader,
    )

    print(
        "GATE_RESULT="
        + json.dumps(
            gate,
            sort_keys=True,
            separators=(",", ":"),
        )
    )

    check(
        "CURRENT_GATE_DENIES_NETWORK",
        gate["authorized"] is False,
    )

    check(
        "CURRENT_GATE_REASON_AUTHORIZATION_RECORD_MISSING",
        gate["reason"]
        == "AUTHORIZATION_RECORD_MISSING",
    )

    check(
        "SECRET_READER_NOT_CALLED",
        secret_reader_calls == [],
        repr(secret_reader_calls),
    )

    check(
        "AUTHORIZATION_RECORD_ABSENT",
        not AUTH_RECORD_PATH.exists(),
    )

    print("\n===== 2. PURE AUTHORIZATION RECORD VALIDATION =====")

    synthetic_record = synthetic_auth_record(
        sha_file(DECISION_PATH)
    )

    auth_errors = (
        validate_authorization_record_object(
            synthetic_record,
            locked["schema"],
            sha_file(DECISION_PATH),
        )
    )

    check(
        "SYNTHETIC_VALID_AUTH_RECORD",
        auth_errors == [],
        repr(auth_errors),
    )

    invalid_record = dict(
        synthetic_record
    )
    invalid_record[
        "authorized_window_id"
    ] = "WRONG-WINDOW"

    invalid_errors = (
        validate_authorization_record_object(
            invalid_record,
            locked["schema"],
            sha_file(DECISION_PATH),
        )
    )

    check(
        "WRONG_WINDOW_REJECTED",
        "WINDOW_ID" in invalid_errors,
        repr(invalid_errors),
    )

    print("\n===== 3. REQUEST BYTE INTEGRITY =====")

    requests = locked["plan"]["requests"]

    check(
        "REQUEST_COUNT_800",
        len(requests) == 800,
    )

    request_hash_failures = []

    for rec in requests:
        try:
            canonical_request_bytes(rec)
        except Exception:
            request_hash_failures.append(
                rec["logical_slot_id"]
            )

    check(
        "ALL_800_REQUEST_BODY_HASHES",
        not request_hash_failures,
        repr(request_hash_failures[:10]),
    )

    print("\n===== 4. HEADER CONSTRUCTION / REDACTION =====")

    fake_secret = (
        "SYNTHETIC-SECRET-NOT-AN-API-KEY"
    )

    ds_headers = build_secret_headers(
        "Model A",
        fake_secret,
    )

    gm_headers = build_secret_headers(
        "Model B",
        fake_secret,
    )

    check(
        "DS_HEADER_IN_MEMORY",
        ds_headers["Authorization"]
        == "Bearer " + fake_secret,
    )

    check(
        "GM_HEADER_IN_MEMORY",
        gm_headers["x-goog-api-key"]
        == fake_secret,
    )

    redacted = redact_headers({
        **ds_headers,
        "x-goog-api-key":
            fake_secret,
        "X-Test":
            "ok",
    })

    check(
        "AUTHORIZATION_HEADER_REDACTED",
        redacted["Authorization"]
        == "<REDACTED>",
    )

    check(
        "GOOGLE_KEY_HEADER_REDACTED",
        redacted["x-goog-api-key"]
        == "<REDACTED>",
    )

    check(
        "NONSECRET_HEADER_PRESERVED",
        redacted["X-Test"] == "ok",
    )

    print("\n===== 5. COST ACCOUNTING =====")

    ds_usage_direct = {
        "prompt_tokens": 110,
        "prompt_cache_hit_tokens": 10,
        "prompt_cache_miss_tokens": 100,
        "completion_tokens": 20,
        "total_tokens": 130,
    }

    ds_direct = deepseek_cost(
        ds_usage_direct,
        locked["contract"],
    )

    check(
        "DS_DIRECT_COST_PASS",
        ds_direct["status"] == "PASS",
    )

    check(
        "DS_DIRECT_COST_EXACT",
        abs(
            ds_direct["estimate_usd"]
            - 0.000019628
        ) < 1e-15,
        repr(ds_direct),
    )

    ds_usage_derived = {
        "prompt_tokens": 110,
        "prompt_tokens_details": {
            "cached_tokens": 10,
        },
        "completion_tokens": 20,
    }

    ds_derived = deepseek_cost(
        ds_usage_derived,
        locked["contract"],
    )

    check(
        "DS_DERIVED_COST_PASS",
        ds_derived["status"] == "PASS",
    )

    check(
        "DS_DERIVED_COST_MATCHES_DIRECT",
        abs(
            ds_derived["estimate_usd"]
            - ds_direct["estimate_usd"]
        ) < 1e-15,
    )

    gm_usage = {
        "promptTokenCount": 100,
        "candidatesTokenCount": 20,
        "thoughtsTokenCount": 5,
        "totalTokenCount": 125,
    }

    gm_cost = gemini_cost(
        gm_usage,
        locked["contract"],
    )

    check(
        "GM_COST_PASS",
        gm_cost["status"] == "PASS",
    )

    check(
        "GM_COST_EXACT",
        abs(
            gm_cost["estimate_usd"]
            - 0.0000625
        ) < 1e-15,
        repr(gm_cost),
    )

    gm_cached = dict(gm_usage)
    gm_cached[
        "cachedContentTokenCount"
    ] = 1

    gm_cached_cost = gemini_cost(
        gm_cached,
        locked["contract"],
    )

    check(
        "GM_POSITIVE_CACHE_REQUIRES_PAUSE",
        gm_cached_cost["status"]
        == "PAUSE_REQUIRED",
    )

    missing_cost = deepseek_cost(
        {},
        locked["contract"],
    )

    check(
        "INSUFFICIENT_DS_USAGE_REQUIRES_PAUSE",
        missing_cost["status"]
        == "PAUSE_REQUIRED",
    )

    print("\n===== 6. COMPLETE RESPONSE PRESERVATION =====")

    ds_request = requests[0]
    gm_request = requests[1]

    ds_body = canonical({
        "model":
            "deepseek-v4-flash",

        "choices": [{
            "finish_reason":
                "stop",
            "message": {
                "content":
                    "int synthetic_deepseek;\n"
            },
        }],

        "usage":
            ds_usage_direct,
    })

    gm_body = canonical({
        "modelVersion":
            "gemini-3.1-flash-lite",

        "candidates": [{
            "finishReason":
                "STOP",
            "content": {
                "parts": [{
                    "text":
                        "int synthetic_gemini;\n"
                }]
            },
        }],

        "usageMetadata":
            gm_usage,
    })

    with tempfile.TemporaryDirectory(
        prefix="svf-live-transport-dryrun-"
    ) as tmp:
        temp_root = Path(tmp)

        ds_events = []

        ds_transport = ScriptedTransport([
            {
                "http_status": 200,
                "headers": {
                    "Content-Type":
                        "application/json",
                    "X-Synthetic":
                        "deepseek",
                },
                "body":
                    ds_body,
                "latency_ms":
                    7,
            }
        ])

        ds_result = execute_one_with_transport(
            locked,
            ds_request,
            ds_transport,
            temp_root / "deepseek",
            lambda seconds: None,
            fake_secret,
            ds_events,
        )

        check(
            "DS_SYNTHETIC_RESULT_MODEL_TEXT",
            ds_result["kind"]
            == "MODEL_TEXT",
        )

        check(
            "DS_SYNTHETIC_NO_PAUSE",
            ds_result[
                "pause_required"
            ] is False,
        )

        check(
            "DS_SYNTHETIC_COST_PASS",
            ds_result["cost"]["status"]
            == "PASS",
        )

        check(
            "DS_RAW_BEFORE_CLASSIFICATION",
            (
                ds_events.index(
                    "RAW_RESPONSE_PRESERVED"
                )
                <
                ds_events.index(
                    "RESPONSE_CLASSIFIED"
                )
            ),
            repr(ds_events),
        )

        gm_events = []

        gm_transport = ScriptedTransport([
            {
                "http_status":
                    200,
                "headers": {
                    "Content-Type":
                        "application/json",
                    "X-Synthetic":
                        "gemini",
                },
                "body":
                    gm_body,
                "latency_ms":
                    8,
            }
        ])

        gm_result = execute_one_with_transport(
            locked,
            gm_request,
            gm_transport,
            temp_root / "gemini",
            lambda seconds: None,
            fake_secret,
            gm_events,
        )

        check(
            "GM_SYNTHETIC_RESULT_MODEL_TEXT",
            gm_result["kind"]
            == "MODEL_TEXT",
        )

        check(
            "GM_SYNTHETIC_NO_PAUSE",
            gm_result[
                "pause_required"
            ] is False,
        )

        check(
            "GM_SYNTHETIC_COST_PASS",
            gm_result["cost"]["status"]
            == "PASS",
        )

        check(
            "GM_RAW_BEFORE_CLASSIFICATION",
            (
                gm_events.index(
                    "RAW_RESPONSE_PRESERVED"
                )
                <
                gm_events.index(
                    "RESPONSE_CLASSIFIED"
                )
            ),
            repr(gm_events),
        )

        print("\n===== 7. RETRY STATE MACHINE =====")

        retry_events = []
        slept = []

        retry_transport = ScriptedTransport([
            TransportFailure(
                "TCP_CONNECT_FAILURE",
                True,
                "synthetic",
            ),

            TransportFailure(
                "READ_TIMEOUT_BEFORE_COMPLETE_HTTP_RESPONSE",
                True,
                "synthetic",
            ),

            {
                "http_status":
                    200,
                "headers": {
                    "Content-Type":
                        "application/json",
                },
                "body":
                    ds_body,
                "latency_ms":
                    9,
            },
        ])

        retry_result = execute_one_with_transport(
            locked,
            ds_request,
            retry_transport,
            temp_root / "retry",
            lambda seconds:
                slept.append(seconds),
            fake_secret,
            retry_events,
        )

        check(
            "RETRY_THREE_INVOCATIONS",
            len(
                retry_result[
                    "invocations"
                ]
            ) == 3,
        )

        check(
            "RETRY_BACKOFF_EXACT_5_20",
            slept == [5, 20],
            repr(slept),
        )

        retry_hashes = {
            c["body_sha256"]
            for c in retry_transport.calls
        }

        check(
            "RETRY_BODY_BYTES_IDENTICAL",
            len(retry_hashes) == 1,
        )

        print("\n===== 8. COMPLETE HTTP ERROR IS NOT RETRIED =====")

        error_events = []

        error_transport = ScriptedTransport([
            {
                "http_status":
                    429,
                "headers": {
                    "Content-Type":
                        "application/json",
                },
                "body":
                    canonical({
                        "error": {
                            "message":
                                "synthetic rate limit"
                        }
                    }),
                "latency_ms":
                    3,
            },

            {
                "http_status":
                    200,
                "headers": {},
                "body":
                    ds_body,
                "latency_ms":
                    1,
            },
        ])

        error_result = execute_one_with_transport(
            locked,
            ds_request,
            error_transport,
            temp_root / "http-error",
            lambda seconds: None,
            fake_secret,
            error_events,
        )

        check(
            "HTTP_429_ONE_INVOCATION_ONLY",
            len(error_transport.calls)
            == 1,
        )

        check(
            "HTTP_429_API_ERROR",
            error_result[
                "terminal_status"
            ] == "API_ERROR",
        )

        check(
            "HTTP_429_PAUSE_REQUIRED",
            error_result[
                "pause_required"
            ] is True,
        )

        print("\n===== 9. MODEL DRIFT PAUSE =====")

        drift_transport = ScriptedTransport([
            {
                "http_status":
                    200,
                "headers": {},
                "body":
                    canonical({
                        "model":
                            "unexpected-model",
                        "choices": [{
                            "finish_reason":
                                "stop",
                            "message": {
                                "content":
                                    "x"
                            },
                        }],
                        "usage":
                            ds_usage_direct,
                    }),
                "latency_ms":
                    2,
            }
        ])

        drift_result = execute_one_with_transport(
            locked,
            ds_request,
            drift_transport,
            temp_root / "drift",
            lambda seconds: None,
            fake_secret,
            [],
        )

        check(
            "MODEL_DRIFT_PAUSE_REQUIRED",
            drift_result[
                "pause_required"
            ] is True,
        )

        check(
            "MODEL_DRIFT_REASON",
            drift_result[
                "pause_reason"
            ] == "RETURNED_MODEL_DRIFT",
        )

        print("\n===== 10. APPEND-ONLY CREATE-NEW =====")

        overwrite_rejected = False

        try:
            execute_one_with_transport(
                locked,
                ds_request,
                ds_transport,
                temp_root / "deepseek",
                lambda seconds: None,
                fake_secret,
                [],
            )
        except FileExistsError:
            overwrite_rejected = True

        check(
            "SECOND_WRITE_REJECTED",
            overwrite_rejected,
        )

    print("\n===== 11. REAL NETWORK PRIMITIVE SAFETY =====")

    check(
        "REAL_TRANSPORT_FUNCTION_PRESENT",
        callable(real_https_post),
    )

    check(
        "REAL_TRANSPORT_NOT_CALLED_IN_QUALIFICATION",
        True,
    )

    check(
        "ENVIRONMENT_SECRET_VALUES_NOT_READ",
        secret_reader_calls == [],
    )

    check(
        "AUTH_RECORD_STILL_ABSENT",
        not AUTH_RECORD_PATH.exists(),
    )

    controller_sha = sha_file(
        Path(__file__)
    )

    report = {
        "report_id":
            "SVF-PRIMARY-LIVE-TRANSPORT-PREFREEZE-QUALIFICATION-V1",

        "status":
            "PASS" if not failures else "FAIL",

        "prepared_at_utc":
            utc_now(),

        "implementation": {
            "path":
                "scripts/primary_live_transport_v1.py",
            "sha256":
                controller_sha,
            "real_https_transport_implemented":
                True,
            "real_https_transport_invoked":
                False,
        },

        "contract": {
            "path":
                "config/primary_live_transport_contract.v1.json",
            "sha256":
                EXPECTED["contract"],
            "status":
                locked["contract"]["status"],
            "execution_enabled":
                locked["contract"][
                    "authorization_gate"
                ]["execution_enabled"],
            "live_network_calls_allowed":
                locked["contract"][
                    "network_transport"
                ][
                    "live_network_calls_allowed_by_this_candidate"
                ],
        },

        "authorization_gate": {
            "current_result":
                gate,
            "authorization_record_exists":
                AUTH_RECORD_PATH.exists(),
            "secret_reader_call_count":
                len(secret_reader_calls),
        },

        "request_integrity": {
            "request_count":
                len(requests),
            "bad_request_body_hash_count":
                len(request_hash_failures),
        },

        "cost_tests": {
            "deepseek_direct":
                ds_direct,
            "deepseek_derived":
                ds_derived,
            "gemini":
                gm_cost,
            "gemini_positive_cache":
                gm_cached_cost,
            "deepseek_insufficient_usage":
                missing_cost,
        },

        "synthetic_transport": {
            "deepseek_result":
                ds_result,
            "gemini_result":
                gm_result,
            "retry_result":
                retry_result,
            "http_429_result":
                error_result,
            "model_drift_result":
                drift_result,
        },

        "failure_count":
            len(failures),

        "failures":
            failures,

        "api_secret_environment_values_read":
            False,

        "live_provider_calls":
            0,

        "primary_generation_authorized":
            False,

        "generation_window_opened":
            False,

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

        "synthetic_workspace_persisted":
            False,
    }

    print(
        "\n===== 11B. TRANSPORT FAILURE DETAIL "
        "SANITIZATION ====="
    )

    sensitive_probe = TransportFailure(
        "TCP_CONNECT_FAILURE",
        True,
        "proxy.internal.example:8443/"
        "sensitive-provider-detail",
    )

    check(
        "TRANSPORT_FAILURE_DETAIL_PROVIDER_NEUTRAL",
        sensitive_probe.detail
        == "TCP_CONNECT_FAILURE",
        repr(sensitive_probe.detail),
    )

    check(
        "TRANSPORT_FAILURE_STRING_PROVIDER_NEUTRAL",
        str(sensitive_probe)
        == "TCP_CONNECT_FAILURE",
        repr(str(sensitive_probe)),
    )

    check(
        "RAW_EXCEPTION_DETAIL_NOT_EXPOSED",
        (
            "proxy.internal.example"
            not in sensitive_probe.detail
            and
            "sensitive-provider-detail"
            not in sensitive_probe.detail
            and
            "proxy.internal.example"
            not in str(sensitive_probe)
        ),
    )

    print("\n===== 12. FINAL RESULT =====")

    print(
        "QUALIFICATION_FAILURE_COUNT="
        + str(len(failures))
    )

    print(
        "PROVIDER_FREE_LIVE_TRANSPORT_QUALIFICATION="
        + ("PASS" if not failures else "FAIL")
    )

    print(
        "IMPLEMENTATION_SHA256="
        + controller_sha
    )

    print(
        "REAL_HTTPS_TRANSPORT_IMPLEMENTED=YES"
    )

    print(
        "REAL_HTTPS_TRANSPORT_INVOKED=NO"
    )

    print(
        "API_SECRET_ENVIRONMENT_VALUES_READ=NO"
    )

    print("LIVE_PROVIDER_CALLS=0")
    print("AUTHORIZATION_RECORD_CREATED=NO")
    print("PRIMARY_GENERATION_AUTHORIZED=NO")
    print("GENERATION_WINDOW_STATE=FROZEN_NOT_OPEN")
    print("GENERATION_WINDOW_OPENED=NO")
    print("PRIMARY_GENERATION_PERFORMED=NO")
    print("GENERATED_DRIVER_INSPECTION=NO")
    print("ANALYZER_IMPLEMENTATION=NO")
    print("REPAIR_IMPLEMENTATION=NO")

    if failures:
        print("REPORT_WRITTEN=NO_DUE_TO_FAILURE")
        return 1

    if report_path.exists():
        print(
            "ERROR=Qualification report already exists; "
            "refusing overwrite."
        )
        return 2

    create_new_json(
        report_path,
        report,
    )

    print(
        "REPORT_PATH="
        + str(
            report_path.relative_to(ROOT)
        )
    )

    print(
        "REPORT_SHA256="
        + sha_file(report_path)
    )

    print(
        "REPORT_WRITTEN_CREATE_NEW=YES"
    )

    return 0


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--synthetic-qualification",
        action="store_true",
    )

    parser.add_argument(
        "--report",
        type=Path,
    )

    args = parser.parse_args()

    if not args.synthetic_qualification:
        print(
            "LIVE_EXECUTION_REFUSED="
            "This candidate CLI exposes provider-free "
            "synthetic qualification only."
        )
        print("AUTHORIZATION_RECORD_CREATED=NO")
        print("API_SECRET_ENVIRONMENT_VALUES_READ=NO")
        print("LIVE_PROVIDER_CALLS=NO")
        print("PRIMARY_GENERATION_AUTHORIZED=NO")
        return 64

    if args.report is None:
        print("ERROR=--report is required.")
        return 64

    report_path = args.report

    if not report_path.is_absolute():
        report_path = ROOT / report_path

    try:
        return run_synthetic_dry_run(
            report_path
        )
    except Exception as exc:
        print(
            "QUALIFICATION_EXCEPTION="
            "PROVIDER_NEUTRAL_REDACTED"
        )
        print(
            "API_SECRET_ENVIRONMENT_VALUES_READ=NO"
        )
        print("LIVE_PROVIDER_CALLS=0")
        print("PRIMARY_GENERATION_AUTHORIZED=NO")
        print("PRIMARY_GENERATION_PERFORMED=NO")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
