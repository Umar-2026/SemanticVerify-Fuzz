#!/usr/bin/env python3

import datetime
import hashlib
import json
import os
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

missing = [
    name
    for name in ["DEEPSEEK_API_KEY", "GEMINI_API_KEY"]
    if not os.environ.get(name)
]

if missing:
    print("GATE0D2_LIVE_MODEL_QUALIFICATION=PENDING")
    print("MISSING_SECRET_NAMES=" + ",".join(missing))
    print("NO_SECRET_VALUE_WAS_READ_OR_PRINTED=YES")
    raise SystemExit(2)

deepseek_key = os.environ["DEEPSEEK_API_KEY"]
gemini_key = os.environ["GEMINI_API_KEY"]

try:
    ds_models_status, ds_models_body, ds_models_latency = (
        request_json(
            "https://api.deepseek.com/models",
            {
                "Authorization": f"Bearer {deepseek_key}"
            },
        )
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

    ds_choices = ds_call_body.get("choices", [])
    require(ds_choices, "DeepSeek returned no choices")

    ds_content = (
        ds_choices[0]
        .get("message", {})
        .get("content", "")
    )

    require(bool(ds_content.strip()), "DeepSeek empty response")

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

    require(bool(gm_content.strip()), "Gemini empty response")

    report = {
        "schema_version": "1.0.0",
        "gate": "Gate 0D2",
        "status": "PASS",
        "qualified_at_utc": (
            datetime.datetime.now(datetime.timezone.utc)
            .replace(microsecond=0)
            .isoformat()
        ),
        "secret_handling": {
            "values_stored": False,
            "values_printed": False,
            "values_hashed": False
        },
        "deepseek": {
            "model_id": "deepseek-v4-flash",
            "models_http_status": ds_models_status,
            "models_latency_ms": ds_models_latency,
            "available_model_ids": ds_model_ids,
            "generation_http_status": ds_call_status,
            "generation_latency_ms": ds_call_latency,
            "response_model": ds_call_body.get("model"),
            "response_id_present": bool(ds_call_body.get("id")),
            "finish_reason": ds_choices[0].get("finish_reason"),
            "response_text_chars": len(ds_content),
            "response_text_sha256": content_digest(ds_content),
            "usage": ds_call_body.get("usage", {}),
            "thinking_mode": "disabled"
        },
        "gemini": {
            "model_id": "gemini-3.1-flash-lite",
            "models_http_status": gm_status,
            "models_latency_ms": gemini_models_latencies,
            "available_model_ids": gemini_models,
            "generation_http_status": gm_call_status,
            "generation_latency_ms": gm_call_latency,
            "response_model_version": (
                gm_call_body.get("modelVersion")
            ),
            "finish_reason": candidates[0].get("finishReason"),
            "response_text_chars": len(gm_content),
            "response_text_sha256": content_digest(gm_content),
            "usage": gm_call_body.get("usageMetadata", {}),
            "thinking_level": "MINIMAL"
        },
        "generation_authorized": False,
        "authorization_note": (
            "Live capability qualification passed, but primary "
            "generation remains blocked until final Gate 0 freeze."
        ),
        "repair_implementation_allowed": False
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

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
    print("GATE0D2_LIVE_MODEL_QUALIFICATION=FAIL")
    print(f"REASON={error}")
    print("SECRET_VALUES_STORED=NO")
    raise SystemExit(1)
