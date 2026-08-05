#!/usr/bin/env python3

import datetime
import hashlib
import json
import os
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "model_targets.json"
REPORT_PATH = (
    ROOT
    / "evidence"
    / "gates"
    / "gate0"
    / "model_live_qualification.json"
)

def request_json(url, headers, payload=None, timeout=90):
    data = None

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request_headers = {
        "Accept": "application/json",
        "User-Agent": "SemanticVerify-Fuzz-Gate0D/1.0",
        **headers,
    }

    if payload is not None:
        request_headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        url,
        data=data,
        headers=request_headers,
        method="POST" if payload is not None else "GET",
    )

    started = time.monotonic()

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:
            body = response.read()
            latency_ms = round(
                (time.monotonic() - started) * 1000,
                3
            )

            return (
                response.status,
                json.loads(body.decode("utf-8")),
                latency_ms,
            )

    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {error.code}: {body[:2000]}"
        ) from None

def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def content_digest(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

require(CONFIG_PATH.is_file(), "model target lock missing")

config_bytes = CONFIG_PATH.read_bytes()

try:
    model_config = json.loads(config_bytes)
except json.JSONDecodeError as error:
    print("GATE0D2_LIVE_MODEL_QUALIFICATION=FAIL")
    print(f"REASON=model target lock invalid: {error}")
    print("SECRET_VALUES_STORED=NO")
    print("GENERATION_AUTHORIZED=NO")
    print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
    raise SystemExit(1)

expected_design = {
    "model_count": 2,
    "library_count": 8,
    "scenarios_per_library": 10,
    "attempts_per_scenario": 5,
    "attempts_per_model_library_cell": 50,
    "total_new_attempts": 800
}

require(
    model_config.get("frozen_design") == expected_design,
    "frozen experimental design mismatch"
)

generation_parameters = model_config.get(
    "generation_parameters",
    {}
)

require(
    generation_parameters.get("temperature") == 0.2,
    "locked temperature mismatch"
)
require(
    generation_parameters.get("top_p") == 1.0,
    "locked top-p mismatch"
)
require(
    generation_parameters.get("stream") is False,
    "locked streaming policy mismatch"
)

model_targets = model_config.get("models", [])
require(len(model_targets) == 2, "model-count mismatch")

deepseek_target = next(
    (
        model
        for model in model_targets
        if model.get("provider") == "DeepSeek"
    ),
    None
)

gemini_target = next(
    (
        model
        for model in model_targets
        if model.get("provider")
        == "Google Gemini Developer API"
    ),
    None
)

require(deepseek_target is not None, "DeepSeek target missing")
require(gemini_target is not None, "Gemini target missing")

require(
    deepseek_target.get("base_url")
    == "https://api.deepseek.com",
    "DeepSeek base-URL drift"
)
require(
    deepseek_target.get("model_id")
    == "deepseek-v4-flash",
    "DeepSeek model-ID drift"
)
require(
    deepseek_target.get("documented_served_version")
    == "DeepSeek-V4-Flash-0731",
    "DeepSeek served-version lock drift"
)
require(
    deepseek_target.get("required_secret_name")
    == "DEEPSEEK_API_KEY",
    "DeepSeek secret-name drift"
)
require(
    deepseek_target
    .get("thinking_control", {})
    .get("rest_body", {})
    .get("thinking", {})
    .get("type")
    == "disabled",
    "DeepSeek thinking-control drift"
)

require(
    gemini_target.get("base_url")
    == (
        "https://generativelanguage.googleapis.com/"
        "v1beta"
    ),
    "Gemini base-URL drift"
)
require(
    gemini_target.get("model_id")
    == "gemini-3.1-flash-lite",
    "Gemini model-ID drift"
)
require(
    gemini_target.get("documented_served_version")
    == "Stable alias: gemini-3.1-flash-lite",
    "Gemini served-version lock drift"
)
require(
    gemini_target.get("required_secret_name")
    == "GEMINI_API_KEY",
    "Gemini secret-name drift"
)
require(
    gemini_target
    .get("thinking_control", {})
    .get("generation_config", {})
    .get("thinkingConfig", {})
    .get("thinkingLevel")
    == "MINIMAL",
    "Gemini thinking-control drift"
)

for target in [deepseek_target, gemini_target]:
    require(
        target.get("documentation_status") == "PASS",
        "model documentation status is not PASS"
    )
    require(
        target.get("live_qualification_status") == "PENDING",
        "model live status is not PENDING"
    )

configuration_status = model_config.get("status", {})

require(
    configuration_status.get("documentation_qualification")
    == "PASS",
    "documentation qualification is not PASS"
)
require(
    configuration_status.get("live_endpoint_qualification")
    == "PENDING",
    "live endpoint qualification is not PENDING"
)
require(
    configuration_status.get("generation_authorized")
    is False,
    "generation unexpectedly authorized"
)

if REPORT_PATH.exists():
    print("GATE0D2_LIVE_MODEL_QUALIFICATION=REFUSED")
    print("REASON=existing live report cannot be overwritten")
    print("SECRET_VALUES_READ=NO")
    print("GENERATION_AUTHORIZED=NO")
    print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
    raise SystemExit(3)

required_secret_names = [
    deepseek_target["required_secret_name"],
    gemini_target["required_secret_name"]
]

missing = [
    name
    for name in required_secret_names
    if not os.environ.get(name)
]

if missing:
    print("GATE0D2_LIVE_MODEL_QUALIFICATION=PENDING")
    print("MISSING_SECRET_NAMES=" + ",".join(missing))
    print("NO_SECRET_VALUE_WAS_READ_OR_PRINTED=YES")
    raise SystemExit(2)

deepseek_key = os.environ["DEEPSEEK_API_KEY"]
gemini_key = os.environ["GEMINI_API_KEY"]
secret_values = [deepseek_key, gemini_key]

for secret_name, secret_value in zip(
    required_secret_names,
    secret_values
):
    require(
        secret_value == secret_value.strip(),
        f"{secret_name} has surrounding whitespace"
    )
    require(
        "\n" not in secret_value,
        f"{secret_name} contains a newline"
    )
    require(
        "\r" not in secret_value,
        f"{secret_name} contains a carriage return"
    )

try:
    ds_models_status, ds_models_body, ds_models_latency = (
        request_json(
            "https://api.deepseek.com/models",
            {
                "Authorization": f"Bearer {deepseek_key}"
            },
        )
    )

    require(
        ds_models_status == 200,
        "DeepSeek model-list status is not 200"
    )

    ds_model_ids = sorted(
        item.get("id", "")
        for item in ds_models_body.get("data", [])
        if item.get("id")
    )

    require(
        "deepseek-v4-flash" in ds_model_ids,
        "DeepSeek target absent from /models"
    )

    ds_payload = {
        "model": "deepseek-v4-flash",
        "messages": [
            {
                "role": "system",
                "content": (
                    "This is a model qualification probe. "
                    "Return a short plain-text response."
                )
            },
            {
                "role": "user",
                "content": "Return exactly: QUALIFIED"
            }
        ],
        "temperature": 0.2,
        "top_p": 1.0,
        "max_tokens": 64,
        "stream": False,
        "thinking": {
            "type": "disabled"
        }
    }

    ds_call_status, ds_call_body, ds_call_latency = (
        request_json(
            "https://api.deepseek.com/chat/completions",
            {
                "Authorization": f"Bearer {deepseek_key}"
            },
            ds_payload,
        )
    )

    require(
        ds_call_status == 200,
        "DeepSeek generation status is not 200"
    )

    ds_choices = ds_call_body.get("choices", [])
    require(ds_choices, "DeepSeek returned no choices")

    ds_content = (
        ds_choices[0]
        .get("message", {})
        .get("content", "")
    )

    require(
        ds_content.strip() == "QUALIFIED",
        "DeepSeek qualification response mismatch"
    )

    ds_response_model = ds_call_body.get("model")

    require(
        ds_response_model
        in {
            deepseek_target["model_id"],
            deepseek_target["documented_served_version"]
        },
        "DeepSeek returned unexpected model metadata"
    )

    gemini_models = []
    next_page_token = None
    gemini_models_latencies = []

    while True:
        query = {"pageSize": "1000"}

        if next_page_token:
            query["pageToken"] = next_page_token

        models_url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models?"
            + urllib.parse.urlencode(query)
        )

        gm_status, gm_body, gm_latency = request_json(
            models_url,
            {"x-goog-api-key": gemini_key},
        )

        require(
            gm_status == 200,
            "Gemini model-list status is not 200"
        )

        gemini_models_latencies.append(gm_latency)

        gemini_models.extend(
            model.get("name", "")
            for model in gm_body.get("models", [])
            if model.get("name")
        )

        next_page_token = gm_body.get("nextPageToken")

        if not next_page_token:
            break

    gemini_models = sorted(set(gemini_models))

    require(
        "models/gemini-3.1-flash-lite" in gemini_models,
        "Gemini target absent from models list"
    )

    gm_payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": "Return exactly: QUALIFIED"
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 1.0,
            "maxOutputTokens": 64,
            "thinkingConfig": {
                "thinkingLevel": "MINIMAL"
            }
        }
    }

    gm_call_status, gm_call_body, gm_call_latency = (
        request_json(
            (
                "https://generativelanguage.googleapis.com/"
                "v1beta/models/"
                "gemini-3.1-flash-lite:generateContent"
            ),
            {"x-goog-api-key": gemini_key},
            gm_payload,
        )
    )

    require(
        gm_call_status == 200,
        "Gemini generation status is not 200"
    )

    candidates = gm_call_body.get("candidates", [])
    require(candidates, "Gemini returned no candidates")

    parts = (
        candidates[0]
        .get("content", {})
        .get("parts", [])
    )

    gm_content = "".join(
        part.get("text", "")
        for part in parts
        if isinstance(part, dict)
    )

    require(
        gm_content.strip() == "QUALIFIED",
        "Gemini qualification response mismatch"
    )

    gm_response_version = gm_call_body.get("modelVersion")

    require(
        isinstance(gm_response_version, str)
        and bool(gm_response_version),
        "Gemini returned no modelVersion"
    )

    normalized_gm_version = (
        gm_response_version.removeprefix("models/")
    )

    require(
        normalized_gm_version
        == gemini_target["model_id"]
        or normalized_gm_version.startswith(
            gemini_target["model_id"] + "-"
        ),
        "Gemini returned unexpected modelVersion"
    )

    report = {
        "schema_version": "1.1.0",
        "gate": "Gate 0D2",
        "status": "PASS",
        "qualified_at_utc": (
            datetime.datetime.now(datetime.timezone.utc)
            .replace(microsecond=0)
            .isoformat()
        ),
        "model_target_lock_sha256": hashlib.sha256(
            config_bytes
        ).hexdigest(),
        "secret_handling": {
            "values_stored": False,
            "values_printed": False,
            "values_hashed": False,
            "failure_text_redacted": True
        },
        "deepseek": {
            "model_id": "deepseek-v4-flash",
            "models_http_status": ds_models_status,
            "models_latency_ms": ds_models_latency,
            "available_model_ids": ds_model_ids,
            "generation_http_status": ds_call_status,
            "generation_latency_ms": ds_call_latency,
            "response_model": ds_response_model,
            "response_id_present": bool(ds_call_body.get("id")),
            "finish_reason": ds_choices[0].get("finish_reason"),
            "response_text_chars": len(ds_content),
            "response_text_sha256": content_digest(ds_content),
            "usage": ds_call_body.get("usage", {}),
            "thinking_mode": "disabled",
            "probe_exact_match": True
        },
        "gemini": {
            "model_id": "gemini-3.1-flash-lite",
            "models_http_status": gm_status,
            "models_latency_ms": gemini_models_latencies,
            "available_model_ids": gemini_models,
            "generation_http_status": gm_call_status,
            "generation_latency_ms": gm_call_latency,
            "response_model_version": gm_response_version,
            "finish_reason": candidates[0].get("finishReason"),
            "response_text_chars": len(gm_content),
            "response_text_sha256": content_digest(gm_content),
            "usage": gm_call_body.get("usageMetadata", {}),
            "thinking_level": "MINIMAL",
            "probe_exact_match": True
        },
        "generation_authorized": False,
        "authorization_note": (
            "Live capability qualification passed, but primary "
            "generation remains blocked until final Gate 0 freeze."
        ),
        "repair_implementation_allowed": False
    }

    serialized_report = (
        json.dumps(report, indent=2, ensure_ascii=False)
        + "\n"
    ).encode("utf-8")

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".model_live_qualification.",
        suffix=".tmp",
        dir=REPORT_PATH.parent
    )
    temporary_path = Path(temporary_name)

    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(serialized_report)
            output.flush()
            os.fsync(output.fileno())

        os.chmod(temporary_path, 0o644)
        os.link(temporary_path, REPORT_PATH)
    except FileExistsError:
        raise RuntimeError(
            "live qualification report overwrite refused"
        ) from None
    finally:
        temporary_path.unlink(missing_ok=True)

    print("GATE0D2_LIVE_MODEL_QUALIFICATION=PASS")
    print("DEEPSEEK_MODEL_LIST=PASS")
    print("DEEPSEEK_NON_THINKING_CALL=PASS")
    print("GEMINI_MODEL_LIST=PASS")
    print("GEMINI_MINIMUM_THINKING_CALL=PASS")
    print("SECRET_VALUES_STORED=NO")
    print("GENERATION_AUTHORIZED=NO")
    print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
    print(
        "REPORT_SHA256="
        + hashlib.sha256(REPORT_PATH.read_bytes()).hexdigest()
    )

except Exception as error:
    reason = str(error)

    for secret_value in secret_values:
        if secret_value:
            reason = reason.replace(
                secret_value,
                "[REDACTED]"
            )

    print("GATE0D2_LIVE_MODEL_QUALIFICATION=FAIL")
    print(f"REASON={reason}")
    print("FAILURE_TEXT_SECRET_REDACTION=PASS")
    print("SECRET_VALUES_STORED=NO")
    print("GENERATION_AUTHORIZED=NO")
    print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
    raise SystemExit(1)
