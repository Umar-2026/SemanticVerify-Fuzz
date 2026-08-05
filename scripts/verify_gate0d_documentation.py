#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

targets = json.loads(
    (ROOT / "config" / "model_targets.json").read_text(
        encoding="utf-8"
    )
)

report = json.loads(
    (
        ROOT
        / "evidence"
        / "gates"
        / "gate0"
        / "model_documentation_qualification.json"
    ).read_text(encoding="utf-8")
)

def require(condition, reason):
    if not condition:
        print("GATE0D1_MODEL_DOCUMENTATION=FAIL")
        print(f"REASON={reason}")
        raise SystemExit(1)

design = targets["frozen_design"]

require(design["model_count"] == 2, "model count")
require(design["library_count"] == 8, "library count")
require(design["scenarios_per_library"] == 10, "scenario count")
require(design["attempts_per_scenario"] == 5, "attempt count")
require(
    2 * 8 * 10 * 5 == design["total_new_attempts"] == 800,
    "800-attempt arithmetic"
)

models = targets["models"]

require(
    [model["model_id"] for model in models]
    == [
        "deepseek-v4-flash",
        "gemini-3.1-flash-lite"
    ],
    "model identifiers"
)
require(
    models[0]["documented_served_version"]
    == "DeepSeek-V4-Flash-0731",
    "DeepSeek served version"
)
require(
    models[0]["thinking_control"]["mode"]
    == "non-thinking",
    "DeepSeek thinking mode"
)
require(
    models[1]["thinking_control"]["mode"]
    == "minimum-thinking",
    "Gemini thinking mode"
)
require(
    models[1]["thinking_control"]["generation_config"]
    ["thinkingConfig"]["thinkingLevel"]
    == "MINIMAL",
    "Gemini minimum-thinking control"
)

parameters = targets["generation_parameters"]

require(parameters["temperature"] == 0.2, "temperature")
require(parameters["top_p"] == 1.0, "top-p")
require(
    parameters["maximum_output_tokens"] == 8192,
    "maximum output"
)

require(report["status"] == "PASS", "documentation report")
require(
    report["conclusion"]
    ["both_requested_identifiers_documented"] is True,
    "model documentation"
)
require(
    report["conclusion"]["model_substitution_required"] is False,
    "unexpected substitution"
)
require(
    targets["status"]["live_endpoint_qualification"]
    == "PENDING",
    "live qualification must remain pending"
)
require(
    targets["status"]["generation_authorized"] is False,
    "generation enabled before live qualification"
)
require(
    targets["version_drift_policy"]
    ["no_post_hoc_model_substitution"] is True,
    "substitution policy"
)
require(
    report["repair_implementation_allowed"] is False,
    "repair enabled"
)

print("GATE0D1_MODEL_DOCUMENTATION=PASS")
print("MODEL_IDENTIFIERS=2")
print("MODEL_SUBSTITUTION_REQUIRED=NO")
print("LIVE_ENDPOINT_QUALIFICATION=PENDING")
print("GENERATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
