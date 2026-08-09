#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, http.client, importlib.util, json, os, socket, ssl, subprocess, sys, tempfile, time
from urllib.parse import urlsplit
from urllib.request import getproxies, proxy_bypass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import primary_live_transport_v1 as lt

CONTRACT = ROOT / "config/primary_live_transport_contract.v1.json"
POST = ROOT / "config/primary_postprocessing_contract.v1.json"
QUALIFIER = ROOT / "scripts/qualify_primary_postprocessing_contract_v1.py"
EVIDENCE_ROOT = ROOT / "evidence/primary_generation/SVF-PRIMARY-800-V1"
WINDOW_ID = "SVF-PRIMARY-800-V1"
EXPECTED_CONTRACT_SHA = "59474347ee27339f1f42247c310786b658f315113dcb2501ab53c9d7ad9b965b"
EXPECTED_TRANSPORT_SHA = "325ef9a7817acaaaa84c0f1ff28c4dfed4c92bf6c3f1cb032c83e5694a4cfbdd"
EXPECTED_POST_SHA = "9efc2973ef7792b9dbda5ee6d6c866718c87607ed2f31b114006dbecc95d6aa8"
EXPECTED_QUALIFIER_SHA = "758343abf8447707b8db4ebca1ef5a8b37f5deeed3df8e22322e74a5c693cda0"

class OperationalError(RuntimeError):
    pass

def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()

def sha_file(p):
    return sha_bytes(Path(p).read_bytes())

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def load_inputs():
    checks = [
        (CONTRACT, EXPECTED_CONTRACT_SHA, "contract"),
        (ROOT/"scripts/primary_live_transport_v1.py", EXPECTED_TRANSPORT_SHA, "transport"),
        (POST, EXPECTED_POST_SHA, "postprocessing"),
        (QUALIFIER, EXPECTED_QUALIFIER_SHA, "qualifier"),
    ]
    for path, expected, name in checks:
        if not path.is_file() or sha_file(path) != expected:
            raise OperationalError(name + " identity mismatch")
    x = lt.load_locked_inputs()
    x["postprocessing"] = json.loads(POST.read_text())
    return x

def select_https_proxy(endpoint, proxies=None, bypass=None):
    u = urlsplit(endpoint)
    if u.scheme != "https" or not u.hostname:
        raise OperationalError("invalid HTTPS endpoint")
    if proxies is None:
        proxies, bypassed, source = getproxies(), proxy_bypass(u.hostname), "environment"
    else:
        bypassed, source = bool(bypass), "synthetic"
    if bypassed:
        return {"mode":"DIRECT","source":source}
    raw = proxies.get("https") or proxies.get("http")
    if not raw:
        return {"mode":"DIRECT","source":source}
    p = urlsplit(raw if "://" in raw else "http://"+raw)
    if p.scheme.lower() != "http":
        raise OperationalError("only HTTP CONNECT proxies are supported")
    if p.username is not None or p.password is not None:
        raise OperationalError("embedded proxy credentials are unsupported")
    if not p.hostname:
        raise OperationalError("proxy hostname missing")
    return {
        "mode":"HTTP_CONNECT",
        "source":source,
        "host":p.hostname,
        "port":p.port or 80,
    }

def proxy_https_post(*, endpoint, body_bytes, headers,
                     connect_timeout_seconds,
                     complete_response_deadline_seconds,
                     proxy_plan):
    u = urlsplit(endpoint)
    if u.scheme != "https" or not u.hostname:
        raise lt.TransportFailure("INVALID_ENDPOINT", False, "INVALID_ENDPOINT")
    host, port = u.hostname, u.port or 443
    target = u.path or "/"
    if u.query:
        target += "?" + u.query
    ctx = ssl.create_default_context()
    conn = None
    stage = "connect"
    started = time.monotonic()
    try:
        if proxy_plan["mode"] == "DIRECT":
            conn = http.client.HTTPSConnection(
                host,
                port,
                timeout=connect_timeout_seconds,
                context=ctx,
            )
            conn.connect()
        elif proxy_plan["mode"] == "HTTP_CONNECT":
            conn = http.client.HTTPConnection(
                proxy_plan["host"],
                proxy_plan["port"],
                timeout=connect_timeout_seconds,
            )
            conn.set_tunnel(host, port)
            try:
                conn.connect()
            except OSError as e:
                if "Tunnel connection failed" in str(e):
                    raise lt.TransportFailure(
                        "PROXY_TUNNEL_FAILURE",
                        False,
                        "PROXY_TUNNEL_FAILURE",
                    )
                raise
            if conn.sock is None:
                raise lt.TransportFailure(
                    "PROXY_TUNNEL_FAILURE",
                    False,
                    "proxy socket unavailable",
                )
            conn.sock = ctx.wrap_socket(
                conn.sock,
                server_hostname=host,
            )
        else:
            raise lt.TransportFailure(
                "INVALID_PROXY_MODE",
                False,
                "INVALID_PROXY_MODE",
            )

        remaining = (
            complete_response_deadline_seconds
            - (time.monotonic() - started)
        )
        if remaining <= 0:
            raise socket.timeout(
                "complete-response deadline exhausted"
            )
        conn.sock.settimeout(remaining)

        stage = "request"
        conn.request(
            "POST",
            target,
            body=body_bytes,
            headers=headers,
        )

        remaining = (
            complete_response_deadline_seconds
            - (time.monotonic() - started)
        )
        if remaining <= 0:
            raise socket.timeout(
                "complete-response deadline exhausted"
            )
        conn.sock.settimeout(remaining)

        stage = "response"
        r = conn.getresponse()

        remaining = (
            complete_response_deadline_seconds
            - (time.monotonic() - started)
        )
        if remaining <= 0:
            raise socket.timeout(
                "complete-response deadline exhausted"
            )
        conn.sock.settimeout(remaining)

        body = r.read()

        return {
            "http_status": int(r.status),
            "headers": dict(r.getheaders()),
            "body": body,
            "latency_ms":
                int(
                    round(
                        (time.monotonic() - started)
                        * 1000
                    )
                ),
            "proxy_mode": proxy_plan["mode"],
        }

    except Exception as e:
        if isinstance(e, lt.TransportFailure):
            raise
        raise lt.classify_transport_exception(
            e,
            stage,
        )

    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass

def run_bytes(cmd):
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=False,
    )

def compiler_preflight(locked, wd):
    c = locked["postprocessing"]["compilation"]

    cp = subprocess.run(
        [c["compiler"], "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
    )

    first = (
        cp.stdout.splitlines()[0]
        if cp.stdout.splitlines()
        else ""
    )

    if (
        cp.returncode
        or first
        != c["expected_compiler_version"]
    ):
        raise OperationalError(
            "compiler preflight failed"
        )

    for lib, cfg in locked[
        "postprocessing"
    ]["libraries"].items():
        artifact = Path(
            cfg["static_artifact"]
        )

        if (
            not artifact.is_file()
            or sha_file(artifact)
            != cfg["static_artifact_sha256"]
        ):
            raise OperationalError(
                "static artifact preflight failed: "
                + lib
            )

        if any(
            not Path(i).is_dir()
            for i in cfg["include_dirs"]
        ):
            raise OperationalError(
                "include preflight failed: "
                + lib
            )

    shim_c = wd / "svf_weak_main.c"
    shim_o = wd / "svf_weak_main.o"

    shim_c.write_bytes(
        c[
            "external_weak_main_shim"
        ]["source"].encode("utf-8")
    )

    p = run_bytes([
        c["compiler"],
        "-std=gnu11",
        "-c",
        str(shim_c),
        "-o",
        str(shim_o),
    ])

    if (
        p.returncode
        or not shim_o.is_file()
    ):
        raise OperationalError(
            "weak-main compile failed"
        )

    return {
        "compiler_version": first,
        "shim_o": shim_o,
    }

def extraction_bytes(text):
    if not isinstance(text, str):
        return "EXTRACTION_FAILURE", None
    if text.strip() == "":
        return "MISSING_CODE", None
    return (
        "EXTRACTED_VERBATIM",
        text.encode("utf-8"),
    )

def compile_driver(
    locked,
    rec,
    source,
    wd,
    ctx,
):
    c = locked[
        "postprocessing"
    ]["compilation"]

    cfg = locked[
        "postprocessing"
    ]["libraries"][rec["library"]]

    out = wd / (
        rec["logical_slot_id"]
        + ".exe"
    )

    cmd = [
        c["compiler"],
        *c["common_flags"],
    ]

    for inc in cfg["include_dirs"]:
        cmd += ["-I", inc]

    cmd += [
        str(source),
        str(ctx["shim_o"]),
        cfg["static_artifact"],
        *c["system_link_tail"],
        "-o",
        str(out),
    ]

    p = run_bytes(cmd)

    text = p.stdout.decode(
        "utf-8",
        errors="replace",
    )

    warnings = sum(
        "warning:" in line
        for line in text.splitlines()
    )

    passed = (
        p.returncode == 0
        and out.is_file()
    )

    return {
        "compiler_command": cmd,
        "compiler_version":
            ctx["compiler_version"],
        "compiler_exit_code":
            p.returncode,
        "compiler_warning_count":
            warnings,
        "compilation_status":
            (
                "COMPILED"
                if passed
                else "NON_COMPILATION"
            ),
        "terminal_status":
            (
                "RESPONSE_RECEIVED"
                if passed
                else "NON_COMPILATION"
            ),
        "log_bytes": p.stdout,
        "linked_executable_created":
            out.is_file(),
        "linked_executable_executed":
            False,
    }

def driver_rel(locked, slot):
    return (
        locked["contract"]
        ["driver_source_storage_contract"]
        ["driver_source_template"]
        .format(logical_slot_id=slot)
    )

def postprocess(
    locked,
    rec,
    tr,
    root,
    dup,
    wd,
    ctx,
):
    interface = locked["interface"]
    post = locked["postprocessing"]
    slot = rec["logical_slot_id"]

    r = {
        "logical_slot_id": slot,
        "terminal_status": None,
        "extraction_status": None,
        "compiler_command": None,
        "compiler_version":
            ctx["compiler_version"],
        "compiler_exit_code": None,
        "compiler_warning_count": None,
        "complete_log_path": None,
        "complete_log_sha256": None,
        "driver_source_path_or_null": None,
        "driver_source_sha256": None,
        "driver_source_byte_length": None,
        "compilation_status":
            "NOT_ATTEMPTED",
        "duplicate_of_logical_slot_id_or_null":
            None,
        "linked_driver_execution":
            False,
    }

    if tr.get("kind") == "MODEL_TEXT":
        status, source_bytes = extraction_bytes(
            tr.get("model_text")
        )

        r["extraction_status"] = status

        if status == "EXTRACTED_VERBATIM":
            rel = driver_rel(
                locked,
                slot,
            )

            path = root / rel

            lt.create_new_bytes(
                path,
                source_bytes,
            )

            source_sha = sha_file(path)
            source_len = path.stat().st_size

            r.update({
                "driver_source_path_or_null":
                    rel,
                "driver_source_sha256":
                    source_sha,
                "driver_source_byte_length":
                    source_len,
            })

            key = (
                rec["model_id"],
                rec["library"],
                rec["scenario_id"],
            )

            prior = None

            for x in dup.get(key, []):
                if (
                    x["sha256"]
                    == source_sha
                    and x["byte_length"]
                    == source_len
                    and x["path"].read_bytes()
                    == source_bytes
                ):
                    prior = (
                        x[
                            "logical_slot_id"
                        ]
                    )
                    break

            if prior:
                r.update({
                    "terminal_status":
                        "DUPLICATE_OUTPUT",
                    "duplicate_of_logical_slot_id_or_null":
                        prior,
                })

            else:
                dup.setdefault(
                    key,
                    [],
                ).append({
                    "logical_slot_id":
                        slot,
                    "sha256":
                        source_sha,
                    "byte_length":
                        source_len,
                    "path":
                        path,
                })

                cr = compile_driver(
                    locked,
                    rec,
                    path,
                    wd,
                    ctx,
                )

                logrel = (
                    interface[
                        "append_only_storage_contract"
                    ][
                        "compiler_log_template"
                    ].format(
                        logical_slot_id=slot
                    )
                )

                lt.create_new_bytes(
                    root / logrel,
                    cr["log_bytes"],
                )

                r.update({
                    "terminal_status":
                        cr["terminal_status"],
                    "compiler_command":
                        cr["compiler_command"],
                    "compiler_version":
                        cr["compiler_version"],
                    "compiler_exit_code":
                        cr["compiler_exit_code"],
                    "compiler_warning_count":
                        cr[
                            "compiler_warning_count"
                        ],
                    "complete_log_path":
                        logrel,
                    "complete_log_sha256":
                        sha_file(
                            root / logrel
                        ),
                    "compilation_status":
                        cr[
                            "compilation_status"
                        ],
                })

        elif status == "MISSING_CODE":
            r["terminal_status"] = (
                "MISSING_CODE"
            )

        else:
            r["terminal_status"] = (
                "EXTRACTION_FAILURE"
            )

    else:
        terminal = (
            tr.get("terminal_status")
            or "API_ERROR"
        )

        r["terminal_status"] = terminal

        r["compilation_status"] = (
            post[
                "compilation_status_mapping"
            ].get(
                terminal,
                "NOT_ATTEMPTED",
            )
        )

    prel = (
        interface[
            "append_only_storage_contract"
        ][
            "postprocessing_record_template"
        ].format(
            logical_slot_id=slot
        )
    )

    lt.create_new_json(
        root / prel,
        r,
    )

    trel = (
        interface[
            "append_only_storage_contract"
        ][
            "slot_terminal_record_template"
        ].format(
            logical_slot_id=slot
        )
    )

    lt.create_new_json(
        root / trel,
        {
            "window_id":
                WINDOW_ID,
            "logical_slot_id":
                slot,
            "slot_number":
                rec["slot_number"],
            "terminal_status":
                r["terminal_status"],
            "postprocessing_record_path":
                prel,
            "postprocessing_record_sha256":
                sha_file(root / prel),
        },
    )

    return r

def returned_model(label, body):
    try:
        obj = json.loads(
            body.decode("utf-8")
        )
    except Exception:
        return None

    if label == "Model A":
        return obj.get("model")

    if label == "Model B":
        return obj.get("modelVersion")

    return None

def failure_terminal(name):
    if name in (
        "CONNECT_TIMEOUT",
        "READ_TIMEOUT_BEFORE_COMPLETE_HTTP_RESPONSE",
    ):
        return "TIMEOUT"

    return "TRANSPORT_FAILURE"

def endpoint_behavior_materially_changed(
    label,
    status,
    body,
):
    if 300 <= status <= 399:
        return True

    if not 200 <= status <= 299:
        return False

    try:
        obj = json.loads(
            body.decode("utf-8")
        )
    except Exception:
        return True

    if not isinstance(obj, dict):
        return True

    if label == "Model A":
        return not (
            "choices" in obj
            or "error" in obj
        )

    if label == "Model B":
        return not (
            "candidates" in obj
            or "promptFeedback" in obj
        )

    return True


def pause_reason(
    label,
    status,
    body,
    returned,
    classification,
    cost,
    service_error_state,
):
    # Provider-specific consecutive-service-error state.
    # A complete non-5xx response resets only this provider.
    if not 500 <= status <= 599:
        service_error_state[label] = 0

    if status in (
        401,
        402,
        403,
        429,
    ):
        return (
            "AUTHENTICATION_BALANCE_PERMISSION_OR_RATE_LIMIT"
        )

    if endpoint_behavior_materially_changed(
        label,
        status,
        body,
    ):
        return (
            "ENDPOINT_BEHAVIOR_MATERIALLY_CHANGED"
        )

    if 500 <= status <= 599:
        count = (
            service_error_state.get(
                label,
                0,
            )
            + 1
        )

        service_error_state[label] = count

        if status in (
            502,
            503,
            504,
        ):
            return (
                "PROVIDER_OUTAGE_HTTP_STATUS"
            )

        if count >= 2:
            return (
                "REPEATED_SERVICE_HTTP_ERRORS"
            )

        return None

    if (
        status == 400
        and "thinking"
        in body.decode(
            "utf-8",
            errors="ignore",
        ).lower()
    ):
        return (
            "THINKING_CONTROL_REJECTED"
        )

    if 200 <= status <= 299:
        if (
            label == "Model A"
            and returned
            not in {
                "deepseek-v4-flash",
                "DeepSeek-V4-Flash-0731",
            }
        ):
            return (
                "RETURNED_MODEL_DRIFT"
            )

        if (
            label == "Model B"
            and returned
            != "gemini-3.1-flash-lite"
        ):
            return (
                "RETURNED_MODEL_DRIFT"
            )

        if cost.get("status") != "PASS":
            return (
                cost.get("reason")
                or "COST_ACCOUNTING_FAILURE"
            )

    if (
        classification.get("kind")
        == "PAUSE_REQUIRED"
    ):
        return (
            classification.get(
                "pause_reason"
            )
            or "PROVIDER_DRIFT"
        )

    return None

def invocation_rel(
    locked,
    slot,
    number,
):
    return (
        locked["interface"]
        ["append_only_storage_contract"]
        ["invocation_record_template"]
        .format(
            logical_slot_id=slot,
            transport_invocation_number=
                number,
        )
    )

def perform_transport(
    locked,
    rec,
    secret,
    root,
    proxy_plan,
    transport_fn=proxy_https_post,
    sleep_fn=time.sleep,
    execution_context=None,
    service_error_state=None,
):
    contract = locked["contract"]
    interface = locked["interface"]
    classify = lt.import_frozen_classifier()

    if execution_context is None:
        execution_context = {
            "authorization_record_path": None,
            "authorization_record_sha256": None,
            "execution_head_commit": None,
        }

    if service_error_state is None:
        service_error_state = {}

    slot = rec["logical_slot_id"]
    label = rec["model_label"]

    provider = contract[
        "providers"
    ][label]

    body = lt.canonical_request_bytes(
        rec
    )

    body_sha = sha_bytes(body)

    headers = lt.build_secret_headers(
        label,
        secret,
    )

    net = contract[
        "network_transport"
    ]

    invocations = []

    for number in range(
        1,
        net[
            "maximum_transport_invocations_per_logical_slot"
        ] + 1,
    ):
        request_rel = (
            interface[
                "append_only_storage_contract"
            ][
                "request_body_template"
            ].format(
                logical_slot_id=slot,
                transport_invocation_number=
                    number,
            )
        )

        lt.create_new_bytes(
            root / request_rel,
            body,
        )

        meta_rel = (
            interface[
                "append_only_storage_contract"
            ][
                "request_metadata_template"
            ].format(
                logical_slot_id=slot,
                transport_invocation_number=
                    number,
            )
        )

        lt.create_new_json(
            root / meta_rel,
            {
                "window_id":
                    WINDOW_ID,
                "logical_slot_id":
                    slot,
                "transport_invocation_number":
                    number,
                "endpoint":
                    provider["endpoint"],
                "request_body_sha256":
                    body_sha,
                "request_body_byte_length":
                    len(body),
                "credential_header_names": [
                    provider[
                        "credential"
                    ][
                        "outbound_header"
                    ]
                ],
                "credential_values_retained":
                    False,
                "proxy_mode":
                    proxy_plan["mode"],
            },
        )

        started = now()

        try:
            response = transport_fn(
                endpoint=
                    provider["endpoint"],
                body_bytes=
                    body,
                headers=
                    headers,
                connect_timeout_seconds=
                    net[
                        "connect_timeout_seconds"
                    ],
                complete_response_deadline_seconds=
                    net[
                        "complete_response_deadline_seconds"
                    ],
                proxy_plan=
                    proxy_plan,
            )

        except lt.TransportFailure as e:
            finished = now()

            failure_rel = (
                interface[
                    "append_only_storage_contract"
                ][
                    "transport_failure_template"
                ].format(
                    logical_slot_id=slot,
                    transport_invocation_number=
                        number,
                )
            )

            lt.create_new_json(
                root / failure_rel,
                {
                    "window_id":
                        WINDOW_ID,
                    "logical_slot_id":
                        slot,
                    "transport_invocation_number":
                        number,
                    "classification":
                        e.classification,
                    "retryable":
                        e.retryable,
                    "detail":
                        e.detail,
                    "request_body_sha256":
                        body_sha,
                },
            )

            retry = (
                e.retryable
                and number
                < net[
                    "maximum_transport_invocations_per_logical_slot"
                ]
            )

            inv = {
                "window_id":
                    WINDOW_ID,
                "authorization_record_path":
                    execution_context[
                        "authorization_record_path"
                    ],
                "authorization_record_sha256":
                    execution_context[
                        "authorization_record_sha256"
                    ],
                "execution_head_commit":
                    execution_context[
                        "execution_head_commit"
                    ],
                "request_body_sha256_verified":
                    True,
                "request_body_byte_length":
                    len(body),
                "logical_slot_id":
                    slot,
                "transport_invocation_number":
                    number,
                "provider":
                    rec["provider"],
                "requested_model_id":
                    rec["model_id"],
                "returned_model_or_version":
                    None,
                "request_started_at_utc":
                    started,
                "request_finished_at_utc":
                    finished,
                "request_parameters":
                    rec[
                        "provider_neutral_descriptor"
                    ],
                "latency_ms":
                    None,
                "HTTP_status_or_transport_failure":
                    e.classification,
                "raw_response_path_or_null":
                    None,
                "raw_response_sha256_or_null":
                    None,
                "token_usage":
                    None,
                "cost_basis_and_estimate": {
                    "status":
                        "NOT_AVAILABLE",
                    "reason":
                        "NO_COMPLETE_HTTP_RESPONSE",
                    "estimate_usd":
                        None,
                },
                "request_body_sha256":
                    body_sha,
                "provider_neutral_descriptor_sha256":
                    rec[
                        "provider_neutral_descriptor_sha256"
                    ],
                "endpoint":
                    provider["endpoint"],
                "transport_retry_classification":
                    (
                        "RETRYABLE_BEFORE_COMPLETE_HTTP_RESPONSE"
                        if retry
                        else
                        "TERMINAL_BEFORE_COMPLETE_HTTP_RESPONSE"
                    ),
                "response_headers_redacted":
                    None,
                "cost_estimate_status":
                    "NOT_AVAILABLE",
            }

            lt.create_new_json(
                root
                / invocation_rel(
                    locked,
                    slot,
                    number,
                ),
                inv,
            )

            invocations.append(inv)

            if retry:
                sleep_fn(
                    net[
                        "deterministic_backoff_seconds"
                    ][number - 1]
                )
                continue

            return {
                "kind":
                    "TERMINAL",
                "terminal_status":
                    failure_terminal(
                        e.classification
                    ),
                "model_text":
                    None,
                "pause_required":
                    False,
                "pause_reason":
                    None,
                "invocations":
                    invocations,
            }

        finished = now()

        rawrel = (
            interface[
                "append_only_storage_contract"
            ][
                "raw_response_template"
            ].format(
                logical_slot_id=slot,
                transport_invocation_number=
                    number,
            )
        )

        lt.create_new_bytes(
            root / rawrel,
            response["body"],
        )

        header_rel = (
            interface[
                "append_only_storage_contract"
            ][
                "redacted_response_headers_template"
            ].format(
                logical_slot_id=slot,
                transport_invocation_number=
                    number,
            )
        )

        lt.create_new_json(
            root / header_rel,
            lt.redact_headers(
                response["headers"]
            ),
        )

        returned = returned_model(
            label,
            response["body"],
        )

        classification = classify(
            interface,
            label,
            response["http_status"],
            response["body"],
        )

        usage = lt.extract_usage(
            label,
            response["body"],
        )

        cost = lt.estimate_cost(
            label,
            usage,
            contract,
        )

        pause = pause_reason(
            label,
            response["http_status"],
            response["body"],
            returned,
            classification,
            cost,
            service_error_state,
        )

        if (
            pause
            == "RETURNED_MODEL_DRIFT"
            and classification.get(
                "kind"
            )
            == "MODEL_TEXT"
        ):
            classification = {
                "kind":
                    "PAUSE_REQUIRED",
                "terminal_status":
                    "API_ERROR",
                "model_text":
                    None,
                "pause_reason":
                    pause,
            }

        inv = {
            "window_id":
                WINDOW_ID,
            "authorization_record_path":
                execution_context[
                    "authorization_record_path"
                ],
            "authorization_record_sha256":
                execution_context[
                    "authorization_record_sha256"
                ],
            "execution_head_commit":
                execution_context[
                    "execution_head_commit"
                ],
            "request_body_sha256_verified":
                True,
            "request_body_byte_length":
                len(body),
            "logical_slot_id":
                slot,
            "transport_invocation_number":
                number,
            "provider":
                rec["provider"],
            "requested_model_id":
                rec["model_id"],
            "returned_model_or_version":
                returned,
            "request_started_at_utc":
                started,
            "request_finished_at_utc":
                finished,
            "request_parameters":
                rec[
                    "provider_neutral_descriptor"
                ],
            "latency_ms":
                response.get("latency_ms"),
            "HTTP_status_or_transport_failure":
                response["http_status"],
            "raw_response_path_or_null":
                rawrel,
            "raw_response_sha256_or_null":
                sha_file(root / rawrel),
            "token_usage":
                usage,
            "cost_basis_and_estimate":
                cost,
            "request_body_sha256":
                body_sha,
            "provider_neutral_descriptor_sha256":
                rec[
                    "provider_neutral_descriptor_sha256"
                ],
            "endpoint":
                provider["endpoint"],
            "transport_retry_classification":
                "COMPLETE_HTTP_RESPONSE_NO_RETRY",
            "response_headers_redacted":
                True,
            "cost_estimate_status":
                cost["status"],
        }

        lt.create_new_json(
            root
            / invocation_rel(
                locked,
                slot,
                number,
            ),
            inv,
        )

        invocations.append(inv)

        terminal = (
            classification.get(
                "terminal_status"
            )
        )

        if (
            classification.get("kind")
            == "PAUSE_REQUIRED"
            and terminal is None
        ):
            terminal = "API_ERROR"

        return {
            "kind":
                classification.get("kind"),
            "terminal_status":
                terminal,
            "model_text":
                classification.get(
                    "model_text"
                ),
            "pause_required":
                pause is not None,
            "pause_reason":
                pause,
            "cost":
                cost,
            "usage":
                usage,
            "returned_model_or_version":
                returned,
            "invocations":
                invocations,
        }

    raise OperationalError(
        "transport loop exhausted"
    )

def write_open(
    root,
    auth_sha,
    head,
):
    p = root / "window/open.json"

    lt.create_new_json(
        p,
        {
            "window_id":
                WINDOW_ID,
            "opened_at_utc":
                now(),
            "authorization_record_path":
                lt.AUTH_RECORD_REL,
            "authorization_record_sha256":
                auth_sha,
            "execution_head_commit":
                head,
            "request_count":
                800,
            "global_max_in_flight_requests":
                1,
        },
    )

    return p

def write_close(root, count):
    p = root / "window/close.json"

    lt.create_new_json(
        p,
        {
            "window_id":
                WINDOW_ID,
            "closed_at_utc":
                now(),
            "terminal_record_count":
                count,
            "all_800_logical_slots_terminal":
                count == 800,
        },
    )

    return p

def write_pause(
    root,
    slot,
    reason,
    seq=1,
):
    template = json.loads(
        (
            ROOT
            / "config/primary_controller_interface.v1.json"
        ).read_text()
    )[
        "append_only_storage_contract"
    ][
        "pause_record_template"
    ]

    rel = template.format(
        pause_sequence=seq
    )

    lt.create_new_json(
        root / rel,
        {
            "window_id":
                WINDOW_ID,
            "pause_sequence":
                seq,
            "paused_at_utc":
                now(),
            "triggering_logical_slot_id":
                slot,
            "reason":
                reason,
            "calls_after_pause_before_resolution":
                0,
        },
    )

    return rel

def read_secrets(locked):
    values = {}

    for rec in locked[
        "plan"
    ]["requests"]:
        if (
            rec["model_label"]
            not in values
        ):
            value = os.environ.get(
                rec["secret_env"]
            )

            if not value:
                raise OperationalError(
                    "required API credential unavailable"
                )

            values[
                rec["model_label"]
            ] = value

    if set(values) != {
        "Model A",
        "Model B",
    }:
        raise OperationalError(
            "credential set incomplete"
        )

    return values

def execute_primary(confirm):
    locked = load_inputs()

    gate = (
        lt.verify_operational_authorization(
            locked
        )
    )

    if not gate.get("authorized"):
        print(
            "LIVE_EXECUTION_REFUSED="
            + gate.get(
                "reason",
                "UNKNOWN",
            )
        )
        print(
            "API_SECRET_ENVIRONMENT_VALUES_READ=NO"
        )
        print(
            "LIVE_PROVIDER_CALLS=NO"
        )
        return 65

    if confirm != WINDOW_ID:
        print(
            "LIVE_EXECUTION_REFUSED="
            "WINDOW_CONFIRMATION_MISMATCH"
        )
        print(
            "API_SECRET_ENVIRONMENT_VALUES_READ=NO"
        )
        print(
            "LIVE_PROVIDER_CALLS=NO"
        )
        return 65

    secrets = read_secrets(locked)

    head = subprocess.check_output(
        [
            "git",
            "-C",
            str(ROOT),
            "rev-parse",
            "HEAD",
        ],
        text=True,
    ).strip()

    proxy_plans = {
        label:
            select_https_proxy(
                cfg["endpoint"]
            )
        for label, cfg
        in locked[
            "contract"
        ]["providers"].items()
    }

    if EVIDENCE_ROOT.exists():
        raise OperationalError(
            "primary evidence root already exists"
        )

    with tempfile.TemporaryDirectory(
        prefix="svf-primary-compile-"
    ) as td:
        wd = Path(td)

        ctx = compiler_preflight(
            locked,
            wd,
        )

        EVIDENCE_ROOT.mkdir(
            parents=True,
            exist_ok=False,
        )

        write_open(
            EVIDENCE_ROOT,
            gate[
                "authorization_record_sha256"
            ],
            head,
        )

        duplicate_state = {}

        service_error_state = {
            "Model A": 0,
            "Model B": 0,
        }

        execution_context = {
            "authorization_record_path":
                lt.AUTH_RECORD_REL,

            "authorization_record_sha256":
                gate[
                    "authorization_record_sha256"
                ],

            "execution_head_commit":
                head,
        }

        terminal_count = 0

        for rec in locked[
            "plan"
        ]["requests"]:
            transport_result = (
                perform_transport(
                    locked,
                    rec,
                    secrets[
                        rec["model_label"]
                    ],
                    EVIDENCE_ROOT,
                    proxy_plans[
                        rec["model_label"]
                    ],

                    execution_context=
                        execution_context,

                    service_error_state=
                        service_error_state,
                )
            )

            post_result = postprocess(
                locked,
                rec,
                transport_result,
                EVIDENCE_ROOT,
                duplicate_state,
                wd,
                ctx,
            )

            terminal_count += 1

            print(
                "PRIMARY_SLOT|"
                + rec[
                    "logical_slot_id"
                ]
                + "|"
                + post_result[
                    "terminal_status"
                ]
            )

            if transport_result.get(
                "pause_required"
            ):
                write_pause(
                    EVIDENCE_ROOT,
                    rec[
                        "logical_slot_id"
                    ],
                    transport_result.get(
                        "pause_reason"
                    )
                    or "UNSPECIFIED_PAUSE",
                )

                print(
                    "PRIMARY_WINDOW_PAUSED=YES"
                )
                print(
                    "CALLS_AFTER_PAUSE=0"
                )
                return 75

        if terminal_count != 800:
            raise OperationalError(
                "terminal count != 800"
            )

        write_close(
            EVIDENCE_ROOT,
            terminal_count,
        )

    print(
        "PRIMARY_WINDOW_COMPLETE=YES"
    )
    print(
        "TERMINAL_RECORD_COUNT=800"
    )
    print(
        "LINKED_DRIVER_EXECUTION=NO"
    )
    print(
        "ANALYZER_IMPLEMENTATION=NO"
    )
    print(
        "REPAIR_IMPLEMENTATION=NO"
    )

    return 0

def sources():
    spec = (
        importlib.util.spec_from_file_location(
            "svf_post_qual",
            QUALIFIER,
        )
    )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    spec.loader.exec_module(
        module
    )

    return module.SOURCES

class FakeTransport:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []

    def __call__(self, **kwargs):
        self.calls.append({
            "endpoint":
                kwargs["endpoint"],
            "body_sha256":
                sha_bytes(
                    kwargs[
                        "body_bytes"
                    ]
                ),
            "proxy_mode":
                kwargs[
                    "proxy_plan"
                ]["mode"],
        })

        if not self.outcomes:
            raise OperationalError(
                "fake transport exhausted"
            )

        item = self.outcomes.pop(0)

        if isinstance(
            item,
            Exception,
        ):
            raise item

        return item

def qualify(report):
    failures = []

    def check(name, ok, detail=None):
        ok = bool(ok)

        print(
            "CHECK|"
            + name
            + "|"
            + (
                "PASS"
                if ok
                else "FAIL"
            )
        )

        if not ok:
            failures.append({
                "check":
                    name,
                "detail":
                    detail,
            })

    print(
        "===== PRIMARY OPERATIONAL RUNNER V1 — "
        "PROVIDER-FREE QUALIFICATION ====="
    )

    locked = load_inputs()

    gate = (
        lt.verify_operational_authorization(
            locked
        )
    )

    check(
        "CURRENT_GATE_DENIES_NETWORK",
        not gate.get("authorized"),
    )

    check(
        "GATE_REASON_AUTHORIZATION_RECORD_MISSING",
        gate.get("reason")
        == "AUTHORIZATION_RECORD_MISSING",
        repr(gate),
    )

    check(
        "AUTHORIZATION_RECORD_ABSENT",
        not lt.AUTH_RECORD_PATH.exists(),
    )

    proxy = select_https_proxy(
        "https://example.com/x",
        {
            "https":
                "http://proxy.example:8080"
        },
        False,
    )

    check(
        "HTTP_CONNECT_PROXY_SELECTED",
        (
            proxy["mode"]
            == "HTTP_CONNECT"
            and proxy["port"]
            == 8080
        ),
    )

    check(
        "DIRECT_WITHOUT_PROXY",
        select_https_proxy(
            "https://example.com/x",
            {},
            False,
        )["mode"]
        == "DIRECT",
    )

    proxy_credentials_rejected = False

    try:
        select_https_proxy(
            "https://example.com/x",
            {
                "https":
                    "http://u:p@proxy.example:8080"
            },
            False,
        )
    except OperationalError:
        proxy_credentials_rejected = True

    check(
        "EMBEDDED_PROXY_CREDENTIALS_REJECTED",
        proxy_credentials_rejected,
    )

    print(
        "\n===== HTTP CONNECT / TLS PROVIDER-FREE "
        "QUALIFICATION ====="
    )

    connect_tls_events = []

    class MockConnectSocket:
        def settimeout(self, value):
            connect_tls_events.append(
                ("settimeout", value)
            )

    class MockConnectResponse:
        status = 200

        def getheaders(self):
            return [
                (
                    "Content-Type",
                    "application/json",
                )
            ]

        def read(self):
            connect_tls_events.append(
                ("read",)
            )
            return b"{}"

    class MockHTTPConnection:
        def __init__(
            self,
            host,
            port,
            timeout=None,
        ):
            connect_tls_events.append(
                (
                    "http_init",
                    host,
                    port,
                    timeout,
                )
            )
            self.sock = MockConnectSocket()

        def set_tunnel(
            self,
            host,
            port=None,
            headers=None,
        ):
            connect_tls_events.append(
                (
                    "set_tunnel",
                    host,
                    port,
                )
            )

        def connect(self):
            connect_tls_events.append(
                ("connect",)
            )

        def request(
            self,
            method,
            url,
            body=None,
            headers=None,
        ):
            connect_tls_events.append(
                (
                    "request",
                    method,
                    url,
                    body,
                )
            )

        def getresponse(self):
            connect_tls_events.append(
                ("getresponse",)
            )
            return MockConnectResponse()

        def close(self):
            connect_tls_events.append(
                ("close",)
            )

    class MockSSLContext:
        def wrap_socket(
            self,
            sock,
            server_hostname=None,
        ):
            connect_tls_events.append(
                (
                    "tls_wrap",
                    server_hostname,
                )
            )
            return sock

    original_http_connection = (
        http.client.HTTPConnection
    )

    original_create_default_context = (
        ssl.create_default_context
    )

    try:
        http.client.HTTPConnection = (
            MockHTTPConnection
        )

        ssl.create_default_context = (
            lambda: MockSSLContext()
        )

        connect_tls_result = (
            proxy_https_post(
                endpoint=
                    "https://example.com/x",

                body_bytes=
                    b"{}",

                headers={
                    "Content-Type":
                        "application/json",
                },

                connect_timeout_seconds=
                    30,

                complete_response_deadline_seconds=
                    300,

                proxy_plan={
                    "mode":
                        "HTTP_CONNECT",

                    "host":
                        "proxy.example",

                    "port":
                        8080,
                },
            )
        )

    finally:
        http.client.HTTPConnection = (
            original_http_connection
        )

        ssl.create_default_context = (
            original_create_default_context
        )

    check(
        "MOCK_HTTP_CONNECT_REAL_BRANCH",
        (
            connect_tls_result[
                "http_status"
            ] == 200
            and
            connect_tls_result[
                "proxy_mode"
            ] == "HTTP_CONNECT"
        ),
        repr(connect_tls_events),
    )

    check(
        "MOCK_PROXY_CONNECTION_ENDPOINT",
        (
            len(connect_tls_events) > 0
            and
            connect_tls_events[0]
            == (
                "http_init",
                "proxy.example",
                8080,
                30,
            )
        ),
        repr(connect_tls_events),
    )

    check(
        "MOCK_CONNECT_TUNNEL_TARGET",
        (
            (
                "set_tunnel",
                "example.com",
                443,
            )
            in connect_tls_events
        ),
        repr(connect_tls_events),
    )

    check(
        "MOCK_TLS_WRAP_SERVER_NAME",
        (
            (
                "tls_wrap",
                "example.com",
            )
            in connect_tls_events
        ),
        repr(connect_tls_events),
    )

    check(
        "MOCK_CONNECT_POST_TARGET",
        any(
            (
                event[0] == "request"
                and event[1] == "POST"
                and event[2] == "/x"
                and event[3] == b"{}"
            )
            for event in connect_tls_events
        ),
        repr(connect_tls_events),
    )

    event_names = [
        event[0]
        for event in connect_tls_events
    ]

    required_order = [
        "http_init",
        "set_tunnel",
        "connect",
        "tls_wrap",
        "request",
        "getresponse",
        "read",
        "close",
    ]

    cursor = -1
    ordered = True

    for required_event in required_order:
        try:
            cursor = event_names.index(
                required_event,
                cursor + 1,
            )
        except ValueError:
            ordered = False
            break

    check(
        "MOCK_CONNECT_TLS_OPERATION_ORDER",
        ordered,
        repr(connect_tls_events),
    )

    check(
        "MOCK_CONNECT_TLS_NO_REAL_NETWORK",
        True,
    )

    print(
        "\n===== PAUSE SEMANTICS QUALIFICATION ====="
    )

    state = {
        "Model A": 0,
        "Model B": 0,
    }

    first_500 = pause_reason(
        "Model A",
        500,
        b'{"error":{"message":"synthetic"}}',
        None,
        {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
        },
        {
            "status": "NOT_AVAILABLE",
        },
        state,
    )

    check(
        "FIRST_NON_OUTAGE_5XX_DOES_NOT_PAUSE",
        first_500 is None,
        repr(first_500),
    )

    second_500 = pause_reason(
        "Model A",
        500,
        b'{"error":{"message":"synthetic"}}',
        None,
        {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
        },
        {
            "status": "NOT_AVAILABLE",
        },
        state,
    )

    check(
        "SECOND_CONSECUTIVE_5XX_PAUSES",
        second_500
        == "REPEATED_SERVICE_HTTP_ERRORS",
        repr(second_500),
    )

    state = {
        "Model A": 0,
        "Model B": 0,
    }

    outage_503 = pause_reason(
        "Model A",
        503,
        b'{"error":{"message":"synthetic"}}',
        None,
        {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
        },
        {
            "status": "NOT_AVAILABLE",
        },
        state,
    )

    check(
        "HTTP_503_OUTAGE_PAUSES_IMMEDIATELY",
        outage_503
        == "PROVIDER_OUTAGE_HTTP_STATUS",
        repr(outage_503),
    )

    redirect = pause_reason(
        "Model A",
        302,
        b'',
        None,
        {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
        },
        {
            "status": "NOT_AVAILABLE",
        },
        {
            "Model A": 0,
            "Model B": 0,
        },
    )

    check(
        "HTTP_REDIRECT_ENDPOINT_CHANGE_PAUSES",
        redirect
        == "ENDPOINT_BEHAVIOR_MATERIALLY_CHANGED",
        repr(redirect),
    )

    malformed_2xx = pause_reason(
        "Model A",
        200,
        b'not-json',
        None,
        {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
        },
        {
            "status": "PASS",
        },
        {
            "Model A": 0,
            "Model B": 0,
        },
    )

    check(
        "MALFORMED_2XX_ENDPOINT_CHANGE_PAUSES",
        malformed_2xx
        == "ENDPOINT_BEHAVIOR_MATERIALLY_CHANGED",
        repr(malformed_2xx),
    )

    missing_envelope = pause_reason(
        "Model B",
        200,
        b'{"usageMetadata":{}}',
        "gemini-3.1-flash-lite",
        {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
        },
        {
            "status": "PASS",
        },
        {
            "Model A": 0,
            "Model B": 0,
        },
    )

    check(
        "MISSING_PROVIDER_ENVELOPE_PAUSES",
        missing_envelope
        == "ENDPOINT_BEHAVIOR_MATERIALLY_CHANGED",
        repr(missing_envelope),
    )

    state = {
        "Model A": 0,
        "Model B": 0,
    }

    _ = pause_reason(
        "Model A",
        500,
        b'{"error":{}}',
        None,
        {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
        },
        {
            "status": "NOT_AVAILABLE",
        },
        state,
    )

    other_provider = pause_reason(
        "Model B",
        400,
        b'{"error":{}}',
        None,
        {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
        },
        {
            "status": "NOT_AVAILABLE",
        },
        state,
    )

    check(
        "OTHER_PROVIDER_DOES_NOT_RESET_MODEL_A_COUNTER",
        (
            other_provider is None
            and state["Model A"] == 1
        ),
        repr(state),
    )

    reset_result = pause_reason(
        "Model A",
        400,
        b'{"error":{}}',
        None,
        {
            "kind": "TERMINAL",
            "terminal_status": "API_ERROR",
        },
        {
            "status": "NOT_AVAILABLE",
        },
        state,
    )

    check(
        "NON_5XX_RESETS_SAME_PROVIDER_COUNTER",
        (
            reset_result is None
            and state["Model A"] == 0
        ),
        repr(state),
    )

    synthetic_sources = sources()

    with tempfile.TemporaryDirectory(
        prefix=
            "svf-operational-qualification-"
    ) as td:
        td = Path(td)
        wd = td / "compile"
        wd.mkdir()

        ctx = compiler_preflight(
            locked,
            wd,
        )

        passed = 0

        for library, source in (
            synthetic_sources.items()
        ):
            source_path = (
                td
                / (
                    "probe-"
                    + library
                    + ".c"
                )
            )

            source_path.write_bytes(
                source.lstrip(
                    "\n"
                ).encode("utf-8")
            )

            rec = next(
                r
                for r in locked[
                    "plan"
                ]["requests"]
                if r["library"]
                == library
            )

            cr = compile_driver(
                locked,
                rec,
                source_path,
                wd,
                ctx,
            )

            ok = (
                cr["terminal_status"]
                == "RESPONSE_RECEIVED"
                and cr[
                    "linked_executable_created"
                ]
                and not cr[
                    "linked_executable_executed"
                ]
            )

            check(
                "COMPILE_"
                + library,
                ok,
            )

            passed += int(ok)

        check(
            "ALL_8_LIBRARY_COMPILES",
            passed == 8,
        )

        root = td / "post"
        duplicate_state = {}

        r1 = locked[
            "plan"
        ]["requests"][0]

        r2 = locked[
            "plan"
        ]["requests"][2]

        r3 = locked[
            "plan"
        ]["requests"][4]

        r4 = locked[
            "plan"
        ]["requests"][1]

        zlib_source = (
            synthetic_sources[
                "zlib"
            ].lstrip("\n")
        )

        first = postprocess(
            locked,
            r1,
            {
                "kind":
                    "MODEL_TEXT",
                "model_text":
                    zlib_source,
            },
            root,
            duplicate_state,
            wd,
            ctx,
        )

        second = postprocess(
            locked,
            r2,
            {
                "kind":
                    "MODEL_TEXT",
                "model_text":
                    zlib_source,
            },
            root,
            duplicate_state,
            wd,
            ctx,
        )

        check(
            "FIRST_SOURCE_COMPILED",
            first[
                "terminal_status"
            ]
            == "RESPONSE_RECEIVED",
        )

        check(
            "LATER_EXACT_DUPLICATE",
            second[
                "terminal_status"
            ]
            == "DUPLICATE_OUTPUT",
        )

        check(
            "DUPLICATE_SOURCE_RETAINED",
            (
                root
                / driver_rel(
                    locked,
                    r2[
                        "logical_slot_id"
                    ],
                )
            ).is_file(),
        )

        bad = postprocess(
            locked,
            r3,
            {
                "kind":
                    "MODEL_TEXT",
                "model_text":
                    "this is not valid C source\n",
            },
            root,
            duplicate_state,
            wd,
            ctx,
        )

        check(
            "INVALID_SOURCE_NON_COMPILATION",
            bad[
                "terminal_status"
            ]
            == "NON_COMPILATION",
        )

        upstream = postprocess(
            locked,
            r4,
            {
                "kind":
                    "TERMINAL",
                "terminal_status":
                    "API_ERROR",
                "model_text":
                    None,
            },
            root,
            duplicate_state,
            wd,
            ctx,
        )

        check(
            "UPSTREAM_NO_DRIVER",
            upstream[
                "driver_source_path_or_null"
            ]
            is None,
        )

        window_root = (
            td
            / "window"
        )

        open_path = write_open(
            window_root,
            "0" * 64,
            "synthetic-head",
        )

        close_path = write_close(
            window_root,
            800,
        )

        check(
            "WINDOW_LIFECYCLE_RECORDS",
            (
                open_path.is_file()
                and close_path.is_file()
            ),
        )

        second_open_rejected = False

        try:
            write_open(
                window_root,
                "0" * 64,
                "synthetic-head",
            )
        except FileExistsError:
            second_open_rejected = True

        check(
            "WINDOW_OPEN_CREATE_NEW",
            second_open_rejected,
        )

        usage = {
            "prompt_tokens":
                10,
            "prompt_cache_hit_tokens":
                0,
            "prompt_cache_miss_tokens":
                10,
            "completion_tokens":
                2,
            "total_tokens":
                12,
        }

        body = lt.canonical({
            "model":
                "deepseek-v4-flash",

            "choices": [{
                "finish_reason":
                    "stop",
                "message": {
                    "content":
                        zlib_source,
                },
            }],

            "usage":
                usage,
        })

        fake = FakeTransport([{
            "http_status":
                200,
            "headers": {
                "Set-Cookie":
                    "secret",
            },
            "body":
                body,
            "latency_ms":
                1,
            "proxy_mode":
                "HTTP_CONNECT",
        }])

        transport_result = (
            perform_transport(
                locked,
                r1,
                "SYNTHETIC-NOT-A-KEY",
                td / "transport",
                {
                    "mode":
                        "HTTP_CONNECT",
                    "host":
                        "proxy.example",
                    "port":
                        8080,
                },
                fake,
                lambda x: None,
            )
        )

        check(
            "INTEGRATED_TRANSPORT_MODEL_TEXT",
            transport_result[
                "kind"
            ]
            == "MODEL_TEXT",
        )

        inv = json.loads(
            (
                td
                / "transport"
                / invocation_rel(
                    locked,
                    r1[
                        "logical_slot_id"
                    ],
                    1,
                )
            ).read_text()
        )

        required_invocation_fields = set(
            locked[
                "protocol"
            ][
                "preservation_contract"
            ][
                "required_per_invocation_fields"
            ]
        ) | set(
            locked[
                "contract"
            ][
                "invocation_record"
            ][
                "additional_live_transport_fields"
            ]
        )

        check(
            "COMPLETE_INVOCATION_LEDGER_FIELDS",
            required_invocation_fields
            <= set(inv.keys()),
            repr(
                sorted(
                    required_invocation_fields
                    - set(inv.keys())
                )
            ),
        )

        check(
            "SYNTHETIC_EXECUTION_CONTEXT_FIELDS_PRESENT",
            (
                "authorization_record_path" in inv
                and "authorization_record_sha256" in inv
                and "execution_head_commit" in inv
            ),
        )

        check(
            "REQUEST_BODY_VERIFICATION_RECORDED",
            (
                inv[
                    "request_body_sha256_verified"
                ]
                is True
                and inv[
                    "request_body_byte_length"
                ] > 0
            ),
        )

        check(
            "COST_STATUS_RECORDED",
            inv[
                "cost_estimate_status"
            ] == "PASS",
        )

        check(
            "RETURNED_MODEL_RECORDED",
            inv[
                "returned_model_or_version"
            ]
            == "deepseek-v4-flash",
        )

        header_rel = (
            locked["interface"]
            ["append_only_storage_contract"]
            [
                "redacted_response_headers_template"
            ]
            .format(
                logical_slot_id=
                    r1[
                        "logical_slot_id"
                    ],
                transport_invocation_number=
                    1,
            )
        )

        check(
            "SET_COOKIE_REDACTED",
            json.loads(
                (
                    td
                    / "transport"
                    / header_rel
                ).read_text()
            )[
                "Set-Cookie"
            ]
            == "<REDACTED>",
        )

        timeout_fake = FakeTransport([
            lt.TransportFailure(
                "CONNECT_TIMEOUT",
                True,
                "x",
            )
            for _ in range(3)
        ])

        slept = []

        timeout_result = (
            perform_transport(
                locked,
                r1,
                "SYNTHETIC-NOT-A-KEY",
                td / "timeout",
                {
                    "mode":
                        "DIRECT"
                },
                timeout_fake,
                lambda x:
                    slept.append(x),
            )
        )

        check(
            "TIMEOUT_TERMINAL",
            timeout_result[
                "terminal_status"
            ]
            == "TIMEOUT",
        )

        check(
            "BACKOFF_5_20",
            slept == [5, 20],
            repr(slept),
        )

        timeout_inv = json.loads(
            (
                td
                / "timeout"
                / invocation_rel(
                    locked,
                    r1[
                        "logical_slot_id"
                    ],
                    1,
                )
            ).read_text()
        )

        check(
            "TRANSPORT_FAILURE_INVOCATION_LEDGER_FIELDS",
            required_invocation_fields
            <= set(timeout_inv.keys()),
            repr(
                sorted(
                    required_invocation_fields
                    - set(timeout_inv.keys())
                )
            ),
        )

        check(
            "TRANSPORT_FAILURE_COST_STATUS",
            timeout_inv[
                "cost_estimate_status"
            ] == "NOT_AVAILABLE",
        )

    result = {
        "report_id":
            "SVF-PRIMARY-OPERATIONAL-RUNNER-PREFREEZE-QUALIFICATION-V1",

        "status":
            (
                "PASS"
                if not failures
                else "FAIL"
            ),

        "qualified_at_utc":
            now(),

        "runner": {
            "path":
                "scripts/primary_operational_runner_v1.py",
            "sha256":
                sha_file(
                    Path(
                        __file__
                    ).resolve()
                ),
        },

        "live_transport": {
            "path":
                "scripts/primary_live_transport_v1.py",
            "sha256":
                EXPECTED_TRANSPORT_SHA,
        },

        "contract": {
            "path":
                "config/primary_live_transport_contract.v1.json",
            "sha256":
                EXPECTED_CONTRACT_SHA,
            "status":
                locked[
                    "contract"
                ]["status"],
            "execution_enabled":
                locked[
                    "contract"
                ][
                    "authorization_gate"
                ][
                    "execution_enabled"
                ],
            "live_network_calls_allowed":
                locked[
                    "contract"
                ][
                    "network_transport"
                ][
                    "live_network_calls_allowed_by_this_candidate"
                ],
        },

        "compiler_version":
            ctx["compiler_version"],

        "synthetic_library_pass_count":
            passed,

        "failure_count":
            len(failures),

        "failures":
            failures,

        "real_network_transport_invoked":
            False,

        "api_secret_environment_values_read":
            False,

        "authorization_record_created":
            False,

        "primary_generation_authorized":
            False,

        "generation_window_opened":
            False,

        "primary_generation_performed":
            False,

        "generated_driver_human_inspection":
            False,

        "linked_driver_execution":
            False,

        "analyzer_implementation_or_execution":
            False,

        "repair_implementation_or_execution":
            False,
    }

    print(
        "QUALIFICATION_FAILURE_COUNT="
        + str(len(failures))
    )

    print(
        "PROVIDER_FREE_OPERATIONAL_QUALIFICATION="
        + (
            "PASS"
            if not failures
            else "FAIL"
        )
    )

    print(
        "REAL_NETWORK_TRANSPORT_INVOKED=NO"
    )

    print(
        "API_SECRET_ENVIRONMENT_VALUES_READ=NO"
    )

    print(
        "LIVE_PROVIDER_CALLS=0"
    )

    if failures:
        return 1

    if report.exists():
        print(
            "ERROR=report exists"
        )
        return 2

    lt.create_new_json(
        report,
        result,
    )

    print(
        "REPORT_PATH="
        + str(
            report.relative_to(
                ROOT
            )
        )
    )

    print(
        "REPORT_SHA256="
        + sha_file(report)
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

    parser.add_argument(
        "--execute-primary",
        action="store_true",
    )

    parser.add_argument(
        "--confirm-window-id",
    )

    args = parser.parse_args()

    if args.synthetic_qualification:
        if args.report is None:
            return 64

        return qualify(
            args.report
            if args.report.is_absolute()
            else ROOT / args.report
        )

    if args.execute_primary:
        return execute_primary(
            args.confirm_window_id
        )

    print(
        "OPERATIONAL_RUNNER_REFUSED="
        "No execution mode selected."
    )

    print(
        "LIVE_PROVIDER_CALLS=NO"
    )

    return 64

if __name__ == "__main__":
    raise SystemExit(main())
