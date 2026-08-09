#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import string
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "head": "76a0178e3abfc6c724c2a4e1d4506681bf81a639",
    "tree": "19894ce2dff3c908b9449a35471da5984791d942",

    "system_prompt":
        "d67e1f168fcbcb8fbe85ffc38cd1e646487be094de20afbff0a7d9b5cbe1bd61",
    "user_template":
        "8691601cfd2a7a0ccfd93d6015182078aa0e174dd0d8579c447b0d54150fa745",
    "scenario_manifest":
        "a7ab361e6e2d41d9051e48bc7626f0be37c1df9ec35f788a9a019b010054a2db",
    "generation_protocol":
        "f10a6093c72e719f55d9fc8acdbc782f1e72be94a0a0a191e1b14faced19d19c",
    "model_targets":
        "c6171d0f398c422cfcb056ec1293a42c43de831e12320b28cb1762660fba1e38",
    "postprocessing":
        "9efc2973ef7792b9dbda5ee6d6c866718c87607ed2f31b114006dbecc95d6aa8",
    "decision_0011":
        "007d1d5aff3a2d9f2ddfd6972350d379d653696a952245e46996eae8e5c88ff3",
    "gate1_manifest":
        "5a1693ea337a547af8a75c7ca24558f188dce230db7ce40e36aa4d8130109d1c",
    "pricing_snapshot":
        "a52e4751a1c1095cbf37183c1c658c52a26190c01a302c55710a47f168a187b6",

    "request_plan":
        "f6712fb4baa7b895f6de82f111f373bf987f0da9166b944232556b99b6ec0440",
    "interface":
        "ffc143952f0b7963cb4f8ec5853a0cc3855775cc7a3292e6ca7d1a660fbc1d56",

    "user_message_bundle":
        "75402e26962a5ad384efb7a2613f44ffd49ef51d70020d20ceff1d05b210d840",
    "slot_bundle":
        "976dbabecddee7daf720703e681ac4e50d4c5774d7a11cd5dc502fa95b48eb71",
    "neutral_bundle":
        "32b5df5b330b96d38ffb7b1ac9b1d162af6a05d7f08757ee9e5a4dbe7368f2f3",
    "body_bundle":
        "a15e0d6ce304eb77e871560e3a4a513368ad63219c73bf2dc1364422746198db",

    "historical_model_visible":
        "14b6d91841b63fed6776f312bfec5c5c4b523661bee4f0c00da79c563fdd8df2",
    "historical_request_bundle":
        "5dc64268d13a7770937a52763f509894888e97dc1d1d737d1e97c91390b3f976",
}

PATHS = {
    "system_prompt": ROOT / "config/generation/system_prompt.v1.txt",
    "user_template": ROOT / "config/generation/user_message_template.v1.txt",
    "scenario_manifest":
        ROOT / "config/generation/scenario_bindings.80.v10.json",
    "generation_protocol":
        ROOT / "config/generation_execution_protocol.json",
    "model_targets":
        ROOT / "config/model_targets.json",
    "postprocessing":
        ROOT / "config/primary_postprocessing_contract.v1.json",
    "decision_0011":
        ROOT / "documentation/decisions/"
        "0011-generation-input-provenance-and-controller-boundary.md",
    "gate1_manifest":
        ROOT / "evidence/gates/gate1/gate1_freeze_manifest.json",
    "pricing_snapshot":
        ROOT / "evidence/gates/gate1/provider_pricing/pricing_snapshot.v2.json",
    "request_plan":
        ROOT / "config/generation/primary_request_plan.800.v1.json",
    "interface":
        ROOT / "config/primary_controller_interface.v1.json",
}

failures = 0


def canonical(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(p.read_bytes())


def check(name, condition, detail=None):
    global failures
    ok = bool(condition)
    print(f"CHECK|{name}|{'PASS' if ok else 'FAIL'}")
    if not ok:
        failures += 1
        if detail is not None:
            print(f"DETAIL|{name}|{detail}")
    return ok


def get_head():
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        text=True
    ).strip()


def get_tree():
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD^{tree}"],
        text=True
    ).strip()


def contains_secret_value(blob):
    text = blob.decode("utf-8", errors="ignore")
    for env_name in ("DEEPSEEK_API_KEY", "GEMINI_API_KEY"):
        value = os.environ.get(env_name)
        if value and value in text:
            return True
    return False


print("===== PRIMARY CONTROLLER INTERFACE VERIFIER V1 =====")

print("\n===== 1. BASE REPOSITORY =====")
head = get_head()
tree = get_tree()
print("HEAD=" + head)
print("TREE=" + tree)

base_ancestor = subprocess.run(
    [
        "git", "-C", str(ROOT),
        "merge-base", "--is-ancestor",
        EXPECTED["head"], "HEAD",
    ],
    text=True,
    capture_output=True,
).returncode == 0

base_tree = subprocess.check_output(
    [
        "git", "-C", str(ROOT),
        "rev-parse",
        EXPECTED["head"] + "^{tree}",
    ],
    text=True,
).strip()

print("CONSTRUCTION_BASE_COMMIT=" + EXPECTED["head"])
print("CONSTRUCTION_BASE_TREE=" + base_tree)

check(
    "CONSTRUCTION_BASE_IS_ANCESTOR",
    base_ancestor,
)
check(
    "CONSTRUCTION_BASE_TREE_EXACT",
    base_tree == EXPECTED["tree"],
)

print("\n===== 2. REQUIRED FILE IDENTITIES =====")
for name, path in PATHS.items():
    exists = path.is_file()
    check("FILE_EXISTS_" + name.upper(), exists)

    if exists and name in EXPECTED:
        digest = sha_file(path)
        print(f"SHA256|{name}|{digest}")
        check(
            "HASH_" + name.upper(),
            digest == EXPECTED[name],
            digest,
        )

if failures:
    print("\nFAIL_FAST=REQUIRED_FILE_OR_HASH_FAILURE")
    print("FAIL_COUNT=" + str(failures))
    print("VERIFIER_RESULT=FAIL")
    raise SystemExit(1)

system_prompt = PATHS["system_prompt"].read_text()
template = PATHS["user_template"].read_text()
scenario_doc = json.loads(PATHS["scenario_manifest"].read_text())
protocol = json.loads(PATHS["generation_protocol"].read_text())
targets = json.loads(PATHS["model_targets"].read_text())
post = json.loads(PATHS["postprocessing"].read_text())
plan = json.loads(PATHS["request_plan"].read_text())
iface = json.loads(PATHS["interface"].read_text())

print("\n===== 3. AUTHORIZATION / SEPARATION BOUNDARY =====")
check(
    "PROTOCOL_AUTHORIZATION_FALSE",
    protocol["authorization"]["primary_generation_authorized"] is False,
)
check(
    "PROTOCOL_WINDOW_FROZEN",
    protocol["execution_window"]["state"] == "FROZEN_NOT_OPEN",
)
check(
    "PLAN_STATUS_FROZEN_PREAUTH",
    plan["status"] == "FROZEN_POST_GATE1_PREAUTH",
)
check(
    "INTERFACE_STATUS_FROZEN_PREAUTH",
    iface["status"] == "FROZEN_POST_GATE1_PREAUTH",
)
check(
    "PLAN_AUTHORIZATION_FALSE",
    plan["authorization"]["primary_generation_authorized"] is False,
)
check(
    "PLAN_PROVIDER_CALLS_FALSE",
    plan["authorization"]["provider_calls_allowed_by_this_plan"] is False,
)
check(
    "INTERFACE_AUTHORIZATION_FALSE",
    iface["authorization_boundary"]["primary_generation_authorized"] is False,
)
check(
    "INTERFACE_LIVE_CALLS_FALSE",
    iface["authorization_boundary"]
    ["live_provider_calls_permitted_by_this_contract"] is False,
)
check(
    "SYNTHETIC_DRY_RUN_REQUIRED",
    iface["authorization_boundary"]
    ["provider_free_synthetic_controller_dry_run_required"] is True,
)
check(
    "SEPARATE_OPEN_AUTH_REQUIRED",
    iface["authorization_boundary"]
    ["separate_committed_generation_opening_authorization_required"] is True,
)
check(
    "DRIVER_INSPECTION_FALSE",
    iface["authorization_boundary"]
    ["generated_driver_human_inspection_allowed"] is False,
)
check(
    "ANALYZER_IMPLEMENTATION_FALSE",
    iface["authorization_boundary"]
    ["analyzer_implementation_allowed"] is False,
)
check(
    "REPAIR_IMPLEMENTATION_FALSE",
    iface["authorization_boundary"]
    ["repair_implementation_allowed"] is False,
)
check(
    "POSTPROCESSING_FROZEN",
    post["status"] == "PASS_FROZEN",
)
check(
    "POSTPROCESSING_NO_DRIVER_EXECUTION",
    post["separation"]["linked_driver_execution_allowed"] is False,
)
check(
    "POSTPROCESSING_NO_ANALYZER",
    post["separation"]["analyzer_execution_allowed"] is False,
)
check(
    "POSTPROCESSING_NO_REPAIR",
    post["separation"]["repair_execution_allowed"] is False,
)

print("\n===== 4. HISTORICAL PROVENANCE BOUNDARY =====")
hist = plan["historical_gate1_provenance"]

check(
    "HISTORICAL_MODEL_VISIBLE_HASH",
    hist["model_visible_bundle_sha256"]
    == EXPECTED["historical_model_visible"],
)
check(
    "HISTORICAL_REQUEST_HASH",
    hist["historical_assembled_80_request_bundle_sha256"]
    == EXPECTED["historical_request_bundle"],
)
check(
    "HISTORICAL_HASH_NOT_EXECUTABLE_BYTE_CONTRACT",
    hist["historical_assembled_bundle_is_executable_byte_contract"] is False,
)
check(
    "INTERFACE_HISTORICAL_POLICY",
    "provenance-only"
    in iface["governance"]["historical_assembled_request_hash_policy"],
)

print("\n===== 5. TEMPLATE / 80 USER MESSAGE RECONSTRUCTION =====")
formatter = string.Formatter()
fields = [
    field
    for _, field, _, _ in formatter.parse(template)
    if field is not None
]

check(
    "TEMPLATE_FIELDS_EXACT",
    fields == [
        "library",
        "scenario_id",
        "task",
        "comma-separated required_feature_symbols",
    ],
)

bindings = scenario_doc.get("bindings", [])
check("BINDING_COUNT_80", len(bindings) == 80)

libraries = protocol["logical_attempt_design"]["libraries_in_frozen_order"]

check(
    "LIBRARY_ORDER_EXACT",
    libraries == [
        "zlib",
        "libpcap",
        "curl",
        "cJSON",
        "libtiff",
        "libvpx",
        "c-ares",
        "lcms",
    ],
)

by_key = {}
message_records = []

for binding in bindings:
    library = binding.get("library")
    scenario_id = binding.get("scenario_id")
    mv = binding.get("model_visible", {})
    symbols = mv.get("required_feature_symbols")
    task = mv.get("task")

    if not (
        isinstance(library, str)
        and isinstance(scenario_id, str)
        and isinstance(task, str)
        and isinstance(symbols, list)
        and all(isinstance(x, str) for x in symbols)
    ):
        check("BINDING_STRUCTURE", False, repr(binding))
        continue

    key = (library, scenario_id)

    if key in by_key:
        check("UNIQUE_BINDING_" + library + "_" + scenario_id, False)
        continue

    message = template.format_map({
        "library": library,
        "scenario_id": scenario_id,
        "task": task,
        "comma-separated required_feature_symbols": ", ".join(symbols),
    })

    check(
        "MESSAGE_FINAL_LF_" + library + "_" + scenario_id,
        message.endswith("\n"),
    )

    by_key[key] = message
    message_records.append({
        "library": library,
        "scenario_id": scenario_id,
        "user_message": message,
    })

expected_keys = [
    (library, f"S{i:02d}")
    for library in libraries
    for i in range(1, 11)
]

check(
    "BINDING_CANONICAL_ORDER",
    list(by_key.keys()) == expected_keys,
)

message_bundle_sha = sha_bytes(canonical(message_records))
print("RECONSTRUCTED_USER_MESSAGE_BUNDLE_SHA256=" + message_bundle_sha)

check(
    "USER_MESSAGE_BUNDLE_HASH",
    message_bundle_sha == EXPECTED["user_message_bundle"],
)

print("\n===== 6. 800 SLOT RECONSTRUCTION =====")
models = protocol["logical_attempt_design"]["models"]

check(
    "MODEL_ORDER_EXACT",
    [m["label"] for m in models] == ["Model A", "Model B"],
)

slot_basis = []
expected_slots = []

slot_number = 0

for library in libraries:
    for scenario_num in range(1, 11):
        scenario_id = f"S{scenario_num:02d}"

        for replicate_num in range(1, 6):
            replicate_id = f"R{replicate_num:02d}"

            for model in models:
                slot_number += 1

                basis = {
                    "library": library,
                    "model_id": model["model_id"],
                    "model_label": model["label"],
                    "replicate_id": replicate_id,
                    "scenario_id": scenario_id,
                    "slot_number": slot_number,
                }

                slot_basis.append(basis)

                expected_slots.append({
                    **basis,
                    "logical_slot_id":
                        f"SVF-PRIMARY-800-V1-SLOT-{slot_number:04d}",
                })

check("DERIVED_SLOT_COUNT_800", slot_number == 800)

slot_bundle_sha = sha_bytes(canonical(slot_basis))
print("RECONSTRUCTED_SLOT_BUNDLE_SHA256=" + slot_bundle_sha)

check(
    "SLOT_BUNDLE_HASH",
    slot_bundle_sha == EXPECTED["slot_bundle"],
)

print("\n===== 7. PROVIDER TARGETS / ADAPTER CONTRACT =====")
target_by_label = {
    x["label"]: x
    for x in targets["models"]
}

ds = target_by_label["Model A"]
gm = target_by_label["Model B"]

check(
    "DEEPSEEK_MODEL_ID",
    ds["model_id"] == "deepseek-v4-flash",
)
check(
    "GEMINI_MODEL_ID",
    gm["model_id"] == "gemini-3.1-flash-lite",
)
check(
    "DEEPSEEK_TARGET_THINKING_DISABLED",
    ds["thinking_control"]["rest_body"]["thinking"]["type"]
    == "disabled",
)
check(
    "GEMINI_TARGET_THINKING_MINIMAL",
    gm["thinking_control"]["generation_config"]
    ["thinkingConfig"]["thinkingLevel"]
    == "MINIMAL",
)

adapters = iface["provider_adapters"]

check(
    "DEEPSEEK_ENDPOINT_EXACT",
    adapters["Model A"]["endpoint"]
    == "https://api.deepseek.com/chat/completions",
)
check(
    "GEMINI_ENDPOINT_EXACT",
    adapters["Model B"]["endpoint"]
    == (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.1-flash-lite:generateContent"
    ),
)
check(
    "DEEPSEEK_INTERFACE_THINKING_DISABLED",
    adapters["Model A"]["thinking_control"]["thinking"]["type"]
    == "disabled",
)
check(
    "GEMINI_INTERFACE_THINKING_MINIMAL",
    adapters["Model B"]["thinking_control"]
    ["generationConfig"]["thinkingConfig"]["thinkingLevel"]
    == "MINIMAL",
)
check(
    "DEEPSEEK_SECRET_ENV_ONLY",
    adapters["Model A"]["authentication"]["secret_env"]
    == "DEEPSEEK_API_KEY",
)
check(
    "GEMINI_SECRET_ENV_ONLY",
    adapters["Model B"]["authentication"]["secret_env"]
    == "GEMINI_API_KEY",
)
check(
    "DEEPSEEK_SECRET_NOT_RETAINED",
    adapters["Model A"]["authentication"]["secret_value_retained"]
    is False,
)
check(
    "GEMINI_SECRET_NOT_RETAINED",
    adapters["Model B"]["authentication"]["secret_value_retained"]
    is False,
)

print("\n===== 8. EXACT 800 REQUEST PLAN VERIFICATION =====")
requests = plan["requests"]

check("REQUEST_COUNT_FIELD_800", plan["request_count"] == 800)
check("REQUEST_ARRAY_COUNT_800", len(requests) == 800)

neutral_descriptors = []
body_hash_envelope = []

per_request_failures_before = failures

for index, expected_slot in enumerate(expected_slots):
    rec = requests[index]
    slot_id = expected_slot["logical_slot_id"]
    key = (
        expected_slot["library"],
        expected_slot["scenario_id"],
    )
    user_message = by_key[key]

    for field in (
        "library",
        "model_id",
        "model_label",
        "replicate_id",
        "scenario_id",
        "slot_number",
        "logical_slot_id",
    ):
        if rec.get(field) != expected_slot[field]:
            check(
                "REQUEST_SLOT_IDENTITY_" + slot_id,
                False,
                field,
            )

    model_label = expected_slot["model_label"]

    if model_label == "Model A":
        expected_provider = "DeepSeek"
        expected_endpoint = (
            "https://api.deepseek.com/chat/completions"
        )
        expected_secret_env = "DEEPSEEK_API_KEY"

        expected_body = {
            "model": "deepseek-v4-flash",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            "temperature": 0.2,
            "top_p": 1.0,
            "max_tokens": 8192,
            "stream": False,
            "thinking": {
                "type": "disabled",
            },
        }

    else:
        expected_provider = "Google Gemini Developer API"
        expected_endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/"
            "models/gemini-3.1-flash-lite:generateContent"
        )
        expected_secret_env = "GEMINI_API_KEY"

        expected_body = {
            "systemInstruction": {
                "parts": [
                    {"text": system_prompt}
                ]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": user_message}
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 1.0,
                "maxOutputTokens": 8192,
                "thinkingConfig": {
                    "thinkingLevel": "MINIMAL",
                },
            },
        }

    expected_neutral = {
        "window_id": "SVF-PRIMARY-800-V1",
        "logical_slot_id": slot_id,
        "slot_number": expected_slot["slot_number"],
        "library": expected_slot["library"],
        "scenario_id": expected_slot["scenario_id"],
        "replicate_id": expected_slot["replicate_id"],
        "model_label": model_label,
        "provider": expected_provider,
        "requested_model_id": expected_slot["model_id"],
        "system_prompt_sha256": EXPECTED["system_prompt"],
        "user_message_sha256":
            sha_bytes(user_message.encode("utf-8")),
        "temperature": 0.2,
        "top_p": 1.0,
        "maximum_output_tokens": 8192,
        "stream": False,
        "seed": None,
        "seed_transmitted": False,
        "seed_rule":
            "provider default; null recorded because no frozen "
            "provider seed is supplied",
    }

    neutral_sha = sha_bytes(canonical(expected_neutral))
    body_sha = sha_bytes(canonical(expected_body))

    if rec.get("provider") != expected_provider:
        check("REQUEST_PROVIDER_" + slot_id, False)

    if rec.get("endpoint") != expected_endpoint:
        check("REQUEST_ENDPOINT_" + slot_id, False)

    if rec.get("secret_env") != expected_secret_env:
        check("REQUEST_SECRET_ENV_" + slot_id, False)

    if rec.get("secret_in_body") is not False:
        check("REQUEST_SECRET_IN_BODY_" + slot_id, False)

    if rec.get("http_method") != "POST":
        check("REQUEST_METHOD_" + slot_id, False)

    if rec.get("content_type") != "application/json":
        check("REQUEST_CONTENT_TYPE_" + slot_id, False)

    if rec.get("provider_neutral_descriptor") != expected_neutral:
        check("REQUEST_NEUTRAL_DESCRIPTOR_" + slot_id, False)

    if rec.get("provider_neutral_descriptor_sha256") != neutral_sha:
        check("REQUEST_NEUTRAL_HASH_" + slot_id, False)

    if rec.get("request_body") != expected_body:
        check("REQUEST_BODY_" + slot_id, False)

    if rec.get("request_body_sha256") != body_sha:
        check("REQUEST_BODY_HASH_" + slot_id, False)

    neutral_descriptors.append(expected_neutral)
    body_hash_envelope.append({
        "logical_slot_id": slot_id,
        "endpoint": expected_endpoint,
        "request_body_sha256": body_sha,
    })

if failures == per_request_failures_before:
    print("CHECK|ALL_800_REQUEST_RECORDS_EXACT|PASS")
else:
    print("CHECK|ALL_800_REQUEST_RECORDS_EXACT|FAIL")

neutral_bundle_sha = sha_bytes(canonical(neutral_descriptors))
body_bundle_sha = sha_bytes(canonical(body_hash_envelope))

print(
    "RECONSTRUCTED_PROVIDER_NEUTRAL_DESCRIPTOR_BUNDLE_SHA256="
    + neutral_bundle_sha
)
print(
    "RECONSTRUCTED_PROVIDER_BODY_HASH_BUNDLE_SHA256="
    + body_bundle_sha
)

check(
    "NEUTRAL_BUNDLE_HASH",
    neutral_bundle_sha == EXPECTED["neutral_bundle"],
)
check(
    "BODY_BUNDLE_HASH",
    body_bundle_sha == EXPECTED["body_bundle"],
)

print("\n===== 9. PLAN / INTERFACE CROSS-BINDING =====")
check(
    "PLAN_BINDS_USER_MESSAGE_BUNDLE",
    plan["new_executable_integrity"]
    ["rendered_80_user_message_bundle_sha256"]
    == EXPECTED["user_message_bundle"],
)
check(
    "PLAN_BINDS_SLOT_BUNDLE",
    plan["new_executable_integrity"]
    ["derived_800_slot_bundle_sha256"]
    == EXPECTED["slot_bundle"],
)
check(
    "PLAN_BINDS_NEUTRAL_BUNDLE",
    plan["new_executable_integrity"]
    ["provider_neutral_descriptor_bundle_sha256"]
    == EXPECTED["neutral_bundle"],
)
check(
    "PLAN_BINDS_BODY_BUNDLE",
    plan["new_executable_integrity"]
    ["provider_body_hash_bundle_sha256"]
    == EXPECTED["body_bundle"],
)
check(
    "INTERFACE_BINDS_REQUEST_PLAN",
    iface["request_plan"]["sha256"]
    == EXPECTED["request_plan"],
)
check(
    "INTERFACE_BINDS_REQUEST_COUNT",
    iface["request_plan"]["request_count"] == 800,
)
check(
    "INTERFACE_BINDS_NEUTRAL_BUNDLE",
    iface["request_plan"]
    ["provider_neutral_descriptor_bundle_sha256"]
    == EXPECTED["neutral_bundle"],
)
check(
    "INTERFACE_BINDS_BODY_BUNDLE",
    iface["request_plan"]["provider_body_hash_bundle_sha256"]
    == EXPECTED["body_bundle"],
)

print("\n===== 10. LOCKED INPUT CROSS-BINDING =====")
for name in (
    "system_prompt",
    "user_template",
    "scenario_manifest",
    "generation_protocol",
    "model_targets",
    "postprocessing",
    "pricing_snapshot",
):
    entry = iface["locked_inputs"][name]
    check(
        "INTERFACE_LOCK_" + name.upper(),
        entry["sha256"] == EXPECTED[name],
    )

check(
    "DECISION_0011_BINDING",
    iface["governance"]["decision_0011"]["sha256"]
    == EXPECTED["decision_0011"],
)
check(
    "GATE1_MANIFEST_BINDING",
    iface["governance"]["gate1_freeze_manifest"]["sha256"]
    == EXPECTED["gate1_manifest"],
)

print("\n===== 11. TRANSPORT CONTRACT =====")
transport = iface["transport_contract"]
frozen_retry = protocol["transport_retry_policy"]
frozen_timeout = protocol["timeout_contract"]

check(
    "CONNECT_TIMEOUT",
    transport["connect_timeout_seconds"]
    == frozen_timeout["connect_timeout_seconds"]
    == 30,
)
check(
    "COMPLETE_RESPONSE_DEADLINE",
    transport["complete_response_deadline_seconds"]
    == frozen_timeout["complete_response_deadline_seconds"]
    == 300,
)
check(
    "MAX_TRANSPORT_INVOCATIONS",
    transport["maximum_transport_invocations_per_logical_slot"]
    == frozen_retry["maximum_transport_invocations_per_logical_slot"]
    == 3,
)
check(
    "MAX_RETRIES",
    transport["maximum_retries_after_initial_invocation"]
    == frozen_retry["maximum_retries_after_initial_invocation"]
    == 2,
)
check(
    "BACKOFF_EXACT",
    transport["backoff_seconds"]
    == frozen_retry["deterministic_backoff_seconds"]
    == [5, 20],
)
check(
    "NO_JITTER",
    transport["jitter_seconds"]
    == frozen_retry["jitter_seconds"]
    == 0,
)
check(
    "PAYLOAD_BYTE_IDENTICAL_ON_RETRY",
    transport["payload_must_be_byte_identical_across_transport_retry"]
    is True,
)
check(
    "RETRY_ONLY_BEFORE_COMPLETE_HTTP_RESPONSE",
    transport["transport_retry_only_before_complete_http_response"]
    is True,
)
check(
    "ALL_INVOCATIONS_RETAINED",
    transport["all_transport_invocations_retained"] is True,
)

print("\n===== 12. TERMINAL STATUS CONTRACT =====")
slot_contract = iface["slot_terminal_contract"]
frozen_statuses = protocol["terminal_status_contract"]["statuses"]

check(
    "TERMINAL_STATUS_VOCABULARY_EXACT",
    slot_contract["terminal_statuses"] == frozen_statuses,
)
check(
    "EXACTLY_ONE_TERMINAL_STATUS",
    slot_contract["exactly_one_terminal_status_per_logical_slot"]
    is True,
)
check(
    "FIXED_DENOMINATOR_800",
    slot_contract["fixed_denominator"] == 800,
)
check(
    "POSTPROCESSING_HASH_BOUND",
    slot_contract["postprocessing_contract_sha256"]
    == EXPECTED["postprocessing"],
)

print("\n===== 13. APPEND-ONLY STORAGE CONTRACT =====")
storage = iface["append_only_storage_contract"]

check(
    "STORAGE_ROOT_EXACT",
    storage["root"]
    == "evidence/primary_generation/SVF-PRIMARY-800-V1",
)
check(
    "CREATE_NEW_OVERWRITE_FORBIDDEN",
    storage["write_mode"]
    == "append-only create-new; overwrite forbidden",
)
check(
    "SHA_EVERY_BLOB",
    storage["sha256_required_for_every_retained_blob"] is True,
)
check(
    "SECRETS_FORBIDDEN_IN_RETAINED_REQUESTS",
    storage["secrets_forbidden_in_retained_request_artifacts"] is True,
)

required_templates = (
    "window_open_record",
    "window_close_record",
    "invocation_record_template",
    "slot_terminal_record_template",
    "pause_record_template",
    "request_body_template",
    "request_metadata_template",
    "raw_response_template",
    "redacted_response_headers_template",
    "transport_failure_template",
    "postprocessing_record_template",
    "compiler_log_template",
)

for key in required_templates:
    value = storage.get(key)
    check(
        "STORAGE_TEMPLATE_" + key.upper(),
        isinstance(value, str)
        and value
        and not value.startswith("/")
        and ".." not in Path(value).parts,
    )

print("\n===== 14. RESPONSE CLASSIFICATION BOUNDARY =====")
mapping = iface["complete_http_response_mapping"]

check(
    "NON_2XX_COMPLETE_IS_API_ERROR",
    mapping["non_2xx_complete_http_response"] == "API_ERROR",
)
check(
    "PROVIDER_ERROR_BODY_IS_API_ERROR",
    mapping["provider_api_error_body"] == "API_ERROR",
)
check(
    "COMPLETE_HTTP_NOT_RETRYABLE",
    mapping["complete_http_response_is_transport_retryable"] is False,
)
check(
    "RAW_RESPONSE_BEFORE_CLASSIFICATION",
    mapping["raw_response_preserved_before_classification"] is True,
)

ds_parser = adapters["Model A"]["response_parser"]
gm_parser = adapters["Model B"]["response_parser"]

check(
    "DS_STOP_PARSE",
    ds_parser["finish_reason_mapping"]["stop"]
    == "PARSE_MODEL_TEXT",
)
check(
    "DS_LENGTH_TRUNCATED",
    ds_parser["finish_reason_mapping"]["length"]
    == "TRUNCATED_OUTPUT",
)
check(
    "GM_STOP_PARSE",
    gm_parser["finish_reason_mapping"]["STOP"]
    == "PARSE_MODEL_TEXT",
)
check(
    "GM_MAX_TOKENS_TRUNCATED",
    gm_parser["finish_reason_mapping"]["MAX_TOKENS"]
    == "TRUNCATED_OUTPUT",
)
check(
    "GM_PROMPT_BLOCK_REFUSAL",
    gm_parser["prompt_block_mapping"]
    == "any non-empty promptFeedback.blockReason => REFUSAL",
)

print("\n===== 15. SECRET LEAK CHECK =====")
candidate_blob = (
    PATHS["request_plan"].read_bytes()
    + b"\n"
    + PATHS["interface"].read_bytes()
)

check(
    "NO_ENV_SECRET_VALUE_IN_CANDIDATES",
    not contains_secret_value(candidate_blob),
)

candidate_text = candidate_blob.decode("utf-8", errors="ignore")

check(
    "NO_AUTHORIZATION_HEADER_VALUE_IN_PLAN",
    "\"Authorization\":\"Bearer "
    not in candidate_text,
)
check(
    "NO_GOOGLE_API_KEY_HEADER_VALUE_IN_PLAN",
    "\"x-goog-api-key\":"
    not in candidate_text,
)

print("\n===== 16. NO-EXECUTION / NO-REPAIR BOUNDARY =====")
handoff = iface["postprocessing_handoff"]

check(
    "RAW_RESPONSE_BEFORE_EXTRACTION",
    handoff["raw_response_preserved_before_extraction"] is True,
)
check(
    "VERBATIM_MODEL_TEXT",
    handoff["provider_model_text_preserved_verbatim"] is True,
)
check(
    "NO_LINKED_DRIVER_EXECUTION",
    handoff["linked_driver_execution_allowed"] is False,
)
check(
    "NO_ANALYZER_EXECUTION",
    handoff["analyzer_execution_allowed"] is False,
)
check(
    "NO_REPAIR_EXECUTION",
    handoff["repair_execution_allowed"] is False,
)
check(
    "NO_REPAIR_BEFORE_GATE_V",
    handoff["repair_before_gate_v_allowed"] is False,
)

print("\n===== 17. FINAL RESULT =====")
print("FAIL_COUNT=" + str(failures))
print(
    "VERIFIER_RESULT="
    + ("PASS" if failures == 0 else "FAIL")
)
print("FILES_WRITTEN_BY_VERIFIER=NO")
print("LIVE_PROVIDER_CALLS=NO")
print("PRIMARY_GENERATION_PERFORMED=NO")
print("GENERATED_DRIVER_INSPECTION=NO")
print("ANALYZER_IMPLEMENTATION=NO")
print("REPAIR_IMPLEMENTATION=NO")

raise SystemExit(0 if failures == 0 else 1)
