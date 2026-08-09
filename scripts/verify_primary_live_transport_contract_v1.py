#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

BASE_COMMIT = "53f1099bcc2c1fb24c18ba388684900a79e23947"
BASE_TREE = "eb25cdeab6b2bf30d424dbd96149ee14679f127f"

DECISION = ROOT / (
    "documentation/decisions/"
    "0012-primary-generation-authorization-and-live-transport-boundary.md"
)

SCHEMA = ROOT / (
    "config/schemas/"
    "primary_generation_authorization_record.schema.json"
)

CONTRACT = ROOT / "config/primary_live_transport_contract.v1.json"

AUTH_RECORD = ROOT / (
    "evidence/generation_opening/"
    "primary_generation_authorization.v1.json"
)

EXPECTED = {
    "decision":
        "8920fb4cd379b02727f4d8efa6e675961ddc9eff48d679f8fb9f4b78f0b61609",

    "schema":
        "b49f843be81347558d9decb65793558e45bd6009a6a455a4e5ccdc04a00798a6",

    "contract":
        "59474347ee27339f1f42247c310786b658f315113dcb2501ab53c9d7ad9b965b",

    "request_plan":
        "f6712fb4baa7b895f6de82f111f373bf987f0da9166b944232556b99b6ec0440",

    "controller_interface":
        "ffc143952f0b7963cb4f8ec5853a0cc3855775cc7a3292e6ca7d1a660fbc1d56",

    "controller_core":
        "6a7f4e47086c1062f041ad461dfd0769833cefe4a49cb8fae1a7fc7644a140c2",

    "interface_verifier":
        "cc0980181996b861df38d841339819e34b0cc0cd226e0fcb97e28c330ac2fe58",

    "controller_final_dry_run":
        "0f5f17497f6d798ad81af56a3f4aede4962ce777c5904684600344caf80fa2ca",

    "controller_freeze_manifest":
        "1325f366b554b5fde90fde8153850f588ce228d54e80a8be4ad7dd987972e7e4",

    "controller_freeze_sums":
        "76eca6d1d5af2ae5c50abe5c2032b5b1d2af460e3e28f9d6448de4b4e07be6a3",

    "generation_protocol":
        "f10a6093c72e719f55d9fc8acdbc782f1e72be94a0a0a191e1b14faced19d19c",

    "postprocessing_contract":
        "9efc2973ef7792b9dbda5ee6d6c866718c87607ed2f31b114006dbecc95d6aa8",

    "model_targets":
        "c6171d0f398c422cfcb056ec1293a42c43de831e12320b28cb1762660fba1e38",

    "model_live_qualification":
        "f0b22b51684605677d4bfbfa4b187227c67093fc4c79792412797e28cb30f5c4",

    "pricing_snapshot":
        "a52e4751a1c1095cbf37183c1c658c52a26190c01a302c55710a47f168a187b6",

    "gate1_manifest":
        "5a1693ea337a547af8a75c7ca24558f188dce230db7ce40e36aa4d8130109d1c",

    "decision_0011":
        "007d1d5aff3a2d9f2ddfd6972350d379d653696a952245e46996eae8e5c88ff3",
}

LOCK_PATHS = {
    "request_plan":
        ROOT / "config/generation/primary_request_plan.800.v1.json",

    "controller_interface":
        ROOT / "config/primary_controller_interface.v1.json",

    "controller_core":
        ROOT / "scripts/primary_controller_v1.py",

    "interface_verifier":
        ROOT / "scripts/verify_primary_controller_interface_v1.py",

    "controller_final_dry_run":
        ROOT / (
            "evidence/generation_opening/primary_controller_v1/"
            "dry_run.v1.json"
        ),

    "controller_freeze_manifest":
        ROOT / (
            "evidence/generation_opening/primary_controller_v1/"
            "preauth_freeze_manifest.v1.json"
        ),

    "controller_freeze_sums":
        ROOT / (
            "evidence/generation_opening/primary_controller_v1/"
            "preauth_freeze_package.v1.SHA256SUMS"
        ),

    "generation_protocol":
        ROOT / "config/generation_execution_protocol.json",

    "postprocessing_contract":
        ROOT / "config/primary_postprocessing_contract.v1.json",

    "model_targets":
        ROOT / "config/model_targets.json",

    "model_live_qualification":
        ROOT / "evidence/gates/gate0/model_live_qualification.json",

    "pricing_snapshot":
        ROOT / (
            "evidence/gates/gate1/provider_pricing/"
            "pricing_snapshot.v2.json"
        ),

    "gate1_manifest":
        ROOT / "evidence/gates/gate1/gate1_freeze_manifest.json",

    "decision_0011":
        ROOT / (
            "documentation/decisions/"
            "0011-generation-input-provenance-and-controller-boundary.md"
        ),
}

failures = 0


def sha_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name, condition, detail=None):
    global failures

    ok = bool(condition)

    print(
        f"CHECK|{name}|"
        + ("PASS" if ok else "FAIL")
    )

    if not ok:
        failures += 1
        if detail is not None:
            print(f"DETAIL|{name}|{detail}")

    return ok


def get_head():
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        text=True,
    ).strip()


def get_tree(commit="HEAD"):
    return subprocess.check_output(
        [
            "git",
            "-C",
            str(ROOT),
            "rev-parse",
            commit + "^{tree}",
        ],
        text=True,
    ).strip()


print(
    "===== PRIMARY LIVE TRANSPORT CONTRACT "
    "VERIFIER V1 ====="
)

print("\n===== 1. REPOSITORY BASE =====")

head = get_head()
tree = get_tree()

print("HEAD=" + head)
print("TREE=" + tree)
print("PREAUTH_FREEZE_COMMIT=" + BASE_COMMIT)

ancestor = subprocess.run(
    [
        "git",
        "-C",
        str(ROOT),
        "merge-base",
        "--is-ancestor",
        BASE_COMMIT,
        "HEAD",
    ],
    text=True,
    capture_output=True,
).returncode == 0

base_tree = get_tree(BASE_COMMIT)

print("PREAUTH_FREEZE_TREE=" + base_tree)

check(
    "PREAUTH_FREEZE_COMMIT_IS_ANCESTOR",
    ancestor,
)

check(
    "PREAUTH_FREEZE_TREE_EXACT",
    base_tree == BASE_TREE,
)

print("\n===== 2. CANDIDATE FILE IDENTITIES =====")

candidate_paths = {
    "decision": DECISION,
    "schema": SCHEMA,
    "contract": CONTRACT,
}

for name, path in candidate_paths.items():
    exists = path.is_file()

    check(
        "FILE_EXISTS_" + name.upper(),
        exists,
    )

    if exists:
        observed = sha_file(path)

        print(
            f"SHA256|{name}|{observed}"
        )

        check(
            "HASH_" + name.upper(),
            observed == EXPECTED[name],
            observed,
        )

if failures:
    print("FAIL_FAST=CANDIDATE_FILE_IDENTITY")
    print("FAIL_COUNT=" + str(failures))
    print("VERIFIER_RESULT=FAIL")
    raise SystemExit(1)

print("\n===== 3. FROZEN PREAUTH DEPENDENCIES =====")

for name, path in LOCK_PATHS.items():
    exists = path.is_file()

    check(
        "LOCK_EXISTS_" + name.upper(),
        exists,
    )

    if not exists:
        continue

    observed = sha_file(path)

    print(
        f"LOCK_SHA256|{name}|{observed}"
    )

    check(
        "LOCK_HASH_" + name.upper(),
        observed == EXPECTED[name],
        observed,
    )

if failures:
    print("FAIL_FAST=FROZEN_DEPENDENCY_IDENTITY")
    print("FAIL_COUNT=" + str(failures))
    print("VERIFIER_RESULT=FAIL")
    raise SystemExit(1)

decision_text = DECISION.read_text()
decision_flat = re.sub(r"\s+", " ", decision_text).strip()
schema = json.loads(SCHEMA.read_text())
contract = json.loads(CONTRACT.read_text())

protocol = json.loads(
    LOCK_PATHS["generation_protocol"].read_text()
)

interface = json.loads(
    LOCK_PATHS["controller_interface"].read_text()
)

pricing = json.loads(
    LOCK_PATHS["pricing_snapshot"].read_text()
)

print("\n===== 4. DECISION 0012 SEMANTICS =====")

decision_checks = {
    "DECISION_STATUS_ACCEPTED":
        "- Status: Accepted" in decision_text,

    "DECISION_BINDS_BASE_COMMIT":
        BASE_COMMIT in decision_text,

    "DECISION_AUTH_RECORD_PATH":
        (
            "evidence/generation_opening/"
            "primary_generation_authorization.v1.json"
        )
        in decision_text,

    "DECISION_SCHEMA_PATH":
        (
            "config/schemas/"
            "primary_generation_authorization_record.schema.json"
        )
        in decision_text,

    "DECISION_LIVE_CONTRACT_PATH":
        "config/primary_live_transport_contract.v1.json"
        in decision_text,

    "DECISION_FROZEN_PROTOCOL_NOT_REWRITTEN":
        (
            "Frozen protocol false value is not rewritten"
            in decision_text
        ),

    "DECISION_AUTH_BEFORE_SECRET":
        (
            "before reading either API secret"
            in decision_flat
        ),

    "DECISION_WINDOW_OPEN_BEFORE_SLOT1":
        (
            "immediately before logical slot 0001"
            in decision_flat
        ),

    "DECISION_NO_REPAIR":
        "Repair remains prohibited until Gate V."
        in decision_text,
}

for name, ok in decision_checks.items():
    check(name, ok)

print("\n===== 5. AUTHORIZATION SCHEMA STRUCTURE =====")

check(
    "SCHEMA_DRAFT_2020_12",
    schema.get("$schema")
    == "https://json-schema.org/draft/2020-12/schema",
)

check(
    "SCHEMA_TOPLEVEL_OBJECT",
    schema.get("type") == "object",
)

check(
    "SCHEMA_NO_ADDITIONAL_PROPERTIES",
    schema.get("additionalProperties") is False,
)

expected_required = {
    "record_id",
    "schema_version",
    "status",
    "authorized_window_id",
    "authorized_at_utc",
    "decision_0012",
    "freeze_binding",
    "provider_requalification",
    "repository_preconditions",
    "authorization_scope",
    "safety_acknowledgements",
}

check(
    "SCHEMA_REQUIRED_TOPLEVEL_EXACT",
    set(schema.get("required", []))
    == expected_required,
)

props = schema["properties"]

check(
    "SCHEMA_RECORD_ID_CONST",
    props["record_id"]["const"]
    == "SVF-PRIMARY-GENERATION-AUTHORIZATION-V1",
)

check(
    "SCHEMA_VERSION_CONST",
    props["schema_version"]["const"] == 1,
)

check(
    "SCHEMA_STATUS_CONST",
    props["status"]["const"]
    == "AUTHORIZED_FOR_PRIMARY_WINDOW_OPEN",
)

check(
    "SCHEMA_WINDOW_CONST",
    props["authorized_window_id"]["const"]
    == "SVF-PRIMARY-800-V1",
)

check(
    "SCHEMA_AUTH_TIME_DATETIME",
    props["authorized_at_utc"].get("format")
    == "date-time",
)

decision_schema = props["decision_0012"]["properties"]

check(
    "SCHEMA_DECISION_PATH_CONST",
    decision_schema["path"]["const"]
    == (
        "documentation/decisions/"
        "0012-primary-generation-authorization-and-live-transport-boundary.md"
    ),
)

check(
    "SCHEMA_DECISION_STATUS_ACCEPTED",
    decision_schema["status"]["const"]
    == "Accepted",
)

freeze_props = props[
    "freeze_binding"
]["properties"]

expected_freeze = {
    "preauthorization_freeze_commit":
        BASE_COMMIT,

    "request_plan_sha256":
        EXPECTED["request_plan"],

    "controller_interface_sha256":
        EXPECTED["controller_interface"],

    "controller_core_sha256":
        EXPECTED["controller_core"],

    "interface_verifier_sha256":
        EXPECTED["interface_verifier"],

    "controller_freeze_manifest_sha256":
        EXPECTED["controller_freeze_manifest"],

    "generation_protocol_sha256":
        EXPECTED["generation_protocol"],

    "postprocessing_contract_sha256":
        EXPECTED["postprocessing_contract"],
}

for name, expected in expected_freeze.items():
    check(
        "SCHEMA_FREEZE_" + name.upper(),
        freeze_props[name]["const"] == expected,
    )

print("\n===== 6. PROVIDER REQUALIFICATION SCHEMA =====")

requal = props[
    "provider_requalification"
]["properties"]

check(
    "REQUAL_STATUS_PASS",
    requal["status"]["const"] == "PASS",
)

ds = requal["deepseek"]["properties"]
gm = requal["gemini"]["properties"]

check(
    "REQUAL_DS_MODEL",
    ds["requested_model_id"]["const"]
    == "deepseek-v4-flash",
)

check(
    "REQUAL_DS_ENDPOINT",
    ds["endpoint"]["const"]
    == "https://api.deepseek.com/chat/completions",
)

check(
    "REQUAL_DS_THINKING",
    ds["thinking_mode"]["const"]
    == "disabled",
)

check(
    "REQUAL_DS_RETURN_MODEL_ENUM",
    set(ds["returned_model"]["enum"])
    == {
        "deepseek-v4-flash",
        "DeepSeek-V4-Flash-0731",
    },
)

check(
    "REQUAL_GM_MODEL",
    gm["requested_model_id"]["const"]
    == "gemini-3.1-flash-lite",
)

check(
    "REQUAL_GM_RETURN_VERSION",
    gm["returned_model_version"]["const"]
    == "gemini-3.1-flash-lite",
)

check(
    "REQUAL_GM_ENDPOINT",
    gm["endpoint"]["const"]
    == (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
        "gemini-3.1-flash-lite:generateContent"
    ),
)

check(
    "REQUAL_GM_THINKING",
    gm["thinking_level"]["const"]
    == "MINIMAL",
)

print("\n===== 7. AUTHORIZATION SCOPE SCHEMA =====")

scope = props[
    "authorization_scope"
]["properties"]

check(
    "AUTH_SCOPE_PRIMARY_TRUE",
    scope["primary_generation"]["const"] is True,
)

check(
    "AUTH_SCOPE_WINDOW_TRUE",
    scope["window_open"]["const"] is True,
)

check(
    "AUTH_SCOPE_MAX_800",
    scope["maximum_logical_slots"]["const"] == 800,
)

check(
    "AUTH_SCOPE_SECOND_WINDOW_FALSE",
    scope["second_window_allowed"]["const"] is False,
)

check(
    "AUTH_SCOPE_ANALYZER_FALSE",
    scope["analyzer"]["const"] is False,
)

check(
    "AUTH_SCOPE_REPAIR_FALSE",
    scope["repair"]["const"] is False,
)

acks = props[
    "safety_acknowledgements"
]["properties"]

for key in (
    "no_generated_driver_human_inspection_during_generation",
    "no_linked_driver_execution_during_primary_compilation",
    "no_repair_before_gate_v",
    "api_secrets_never_persisted_printed_or_hashed",
    "pause_rule_binding_acknowledged",
):
    check(
        "ACK_" + key.upper(),
        acks[key]["const"] is True,
    )

print("\n===== 8. LIVE-TRANSPORT CONTRACT STATE =====")

check(
    "CONTRACT_ID",
    contract["contract_id"]
    == "SVF-PRIMARY-LIVE-TRANSPORT-V1",
)

check(
    "CONTRACT_AUTHORIZATION_READY",
    contract["status"]
    == "FROZEN_AUTHORIZATION_READY",
)

check(
    "CONSTRUCTION_BASE_COMMIT",
    contract[
        "construction_base"
    ]["commit"] == BASE_COMMIT,
)

check(
    "CONSTRUCTION_BASE_TREE",
    contract[
        "construction_base"
    ]["tree"] == BASE_TREE,
)

check(
    "CONTRACT_DECISION_SHA",
    contract["decision"]["sha256"]
    == EXPECTED["decision"],
)

check(
    "CONTRACT_DECISION_ACCEPTED",
    contract["decision"]["status"]
    == "ACCEPTED",
)

print("\n===== 9. FROZEN PACKAGE BINDINGS =====")

fp = contract[
    "frozen_preauthorization_package"
]

binding_checks = {
    "FREEZE_COMMIT":
        fp["commit"] == BASE_COMMIT,

    "REQUEST_PLAN":
        fp["request_plan"]["sha256"]
        == EXPECTED["request_plan"],

    "INTERFACE":
        fp["controller_interface"]["sha256"]
        == EXPECTED["controller_interface"],

    "CORE":
        fp["provider_free_controller_core"]["sha256"]
        == EXPECTED["controller_core"],

    "VERIFIER":
        fp["interface_verifier"]["sha256"]
        == EXPECTED["interface_verifier"],

    "DRY_RUN":
        fp["final_provider_free_dry_run"]["sha256"]
        == EXPECTED["controller_final_dry_run"],

    "FREEZE_MANIFEST":
        fp["freeze_manifest"]["sha256"]
        == EXPECTED["controller_freeze_manifest"],

    "FREEZE_SUMS":
        fp["freeze_package_sha256s"]["sha256"]
        == EXPECTED["controller_freeze_sums"],
}

for name, ok in binding_checks.items():
    check("BIND_" + name, ok)

print("\n===== 10. AUTHORIZATION GATE =====")

gate = contract["authorization_gate"]

check(
    "AUTH_RECORD_PATH_EXACT",
    gate["authorization_record_path"]
    == (
        "evidence/generation_opening/"
        "primary_generation_authorization.v1.json"
    ),
)

check(
    "AUTH_SCHEMA_PATH_EXACT",
    gate["authorization_schema_path"]
    == (
        "config/schemas/"
        "primary_generation_authorization_record.schema.json"
    ),
)

check(
    "AUTH_SCHEMA_SHA_BINDING",
    gate["authorization_schema_sha256"]
    == EXPECTED["schema"],
)

check(
    "AUTH_RECORD_CURRENTLY_ABSENT",
    gate["authorization_record_currently_exists"]
    is False,
)

check(
    "EXECUTION_CAPABILITY_ENABLED",
    gate["execution_enabled"] is True,
)

check(
    "AUTH_STATUS_REQUIRED",
    gate["required_record_status"]
    == "AUTHORIZED_FOR_PRIMARY_WINDOW_OPEN",
)

check(
    "AUTH_WINDOW_REQUIRED",
    gate["required_window_id"]
    == "SVF-PRIMARY-800-V1",
)

check(
    "AUTH_RECORD_MUST_BE_TRACKED",
    gate["authorization_record_must_be_tracked"]
    is True,
)

check(
    "AUTH_RECORD_IN_HEAD",
    gate["authorization_record_must_be_present_in_current_head"]
    is True,
)

check(
    "CLEAN_BEFORE_OPEN",
    gate["repository_must_be_clean_immediately_before_window_open"]
    is True,
)

check(
    "FREEZE_ANCESTOR_REQUIRED",
    gate["freeze_commit_must_be_ancestor_of_execution_head"]
    is True,
)

check(
    "AUTH_BEFORE_SECRET_READ",
    gate["authorization_must_be_verified_before_secret_read"]
    is True,
)

check(
    "OPEN_RECORD_BEFORE_SLOT1",
    gate["window_open_record_created_immediately_before_slot_0001"]
    is True,
)

check(
    "AUTH_FAILURE_REFUSES_NETWORK",
    gate["absence_or_failure_behavior"]
    == "REFUSE_NETWORK_ACCESS",
)

print("\n===== 11. IMMUTABLE REQUEST-BYTE BOUNDARY =====")

req = contract["immutable_request_boundary"]

check(
    "REQUEST_PLAN_SHA",
    req["request_plan_sha256"]
    == EXPECTED["request_plan"],
)

check(
    "REQUEST_COUNT_800",
    req["request_count"] == 800,
)

ser = req["canonical_body_serialization"]

check(
    "SER_ENCODING_UTF8",
    ser["encoding"] == "UTF-8",
)

check(
    "SER_SORT_KEYS",
    ser["json_sort_keys"] is True,
)

check(
    "SER_SEPARATORS",
    ser["json_separators"] == [",", ":"],
)

check(
    "SER_ENSURE_ASCII_FALSE",
    ser["ensure_ascii"] is False,
)

check(
    "SER_NO_TRAILING_LF",
    ser["trailing_lf"] is False,
)

check(
    "RETRY_PAYLOAD_CHANGE_FALSE",
    req["payload_change_during_retry_allowed"]
    is False,
)

check(
    "RETRY_BYTES_IDENTICAL",
    req["retry_payload_must_be_byte_identical"]
    is True,
)

print("\n===== 12. PROVIDER CONTRACT =====")

providers = contract["providers"]

c_ds = providers["Model A"]
c_gm = providers["Model B"]

check(
    "DS_ENDPOINT_EXACT",
    c_ds["endpoint"]
    == "https://api.deepseek.com/chat/completions",
)

check(
    "DS_MODEL_EXACT",
    c_ds["model_id"]
    == "deepseek-v4-flash",
)

check(
    "DS_SECRET_ENV",
    c_ds["credential"]["environment_variable"]
    == "DEEPSEEK_API_KEY",
)

check(
    "DS_AUTH_HEADER",
    c_ds["credential"]["outbound_header"]
    == "Authorization",
)

check(
    "DS_SECRET_AFTER_AUTH_ONLY",
    c_ds["credential"][
        "read_only_after_authorization_pass"
    ] is True,
)

check(
    "DS_SECRET_NOT_STORED",
    c_ds["credential"]["stored"] is False,
)

check(
    "DS_SECRET_NOT_PRINTED",
    c_ds["credential"]["printed"] is False,
)

check(
    "DS_SECRET_NOT_HASHED",
    c_ds["credential"]["hashed"] is False,
)

check(
    "DS_THINKING_DISABLED",
    c_ds["thinking_control"]["thinking"]["type"]
    == "disabled",
)

check(
    "GM_ENDPOINT_EXACT",
    c_gm["endpoint"]
    == (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
        "gemini-3.1-flash-lite:generateContent"
    ),
)

check(
    "GM_MODEL_EXACT",
    c_gm["model_id"]
    == "gemini-3.1-flash-lite",
)

check(
    "GM_SECRET_ENV",
    c_gm["credential"]["environment_variable"]
    == "GEMINI_API_KEY",
)

check(
    "GM_AUTH_HEADER",
    c_gm["credential"]["outbound_header"]
    == "x-goog-api-key",
)

check(
    "GM_SECRET_AFTER_AUTH_ONLY",
    c_gm["credential"][
        "read_only_after_authorization_pass"
    ] is True,
)

check(
    "GM_SECRET_NOT_STORED",
    c_gm["credential"]["stored"] is False,
)

check(
    "GM_SECRET_NOT_PRINTED",
    c_gm["credential"]["printed"] is False,
)

check(
    "GM_SECRET_NOT_HASHED",
    c_gm["credential"]["hashed"] is False,
)

check(
    "GM_THINKING_MINIMAL",
    c_gm["thinking_control"][
        "generationConfig"
    ]["thinkingConfig"]["thinkingLevel"]
    == "MINIMAL",
)

print("\n===== 13. TRANSPORT / RETRY CONTRACT =====")

net = contract["network_transport"]

check(
    "TRANSPORT_AUTHORIZATION_READY",
    net["implementation_status"]
    == "FROZEN_AUTHORIZATION_READY",
)

check(
    "LIVE_NETWORK_CAPABILITY_ENABLED",
    net["live_network_calls_allowed_by_this_candidate"]
    is True,
)

check(
    "CONNECT_TIMEOUT_30",
    net["connect_timeout_seconds"] == 30,
)

check(
    "COMPLETE_DEADLINE_300",
    net["complete_response_deadline_seconds"]
    == 300,
)

check(
    "MAX_INVOCATIONS_3",
    net["maximum_transport_invocations_per_logical_slot"]
    == 3,
)

check(
    "MAX_RETRIES_2",
    net["maximum_retries_after_initial_invocation"]
    == 2,
)

check(
    "BACKOFF_5_20",
    net["deterministic_backoff_seconds"]
    == [5, 20],
)

check(
    "JITTER_ZERO",
    net["jitter_seconds"] == 0,
)

check(
    "ONE_REQUEST_IN_FLIGHT",
    net["global_max_in_flight_requests"] == 1,
)

check(
    "TLS_VALIDATION",
    net["tls_certificate_validation_required"]
    is True,
)

check(
    "COMPLETE_HTTP_NOT_RETRYABLE",
    net["complete_http_response_is_transport_retryable"]
    is False,
)

frozen_transport = interface["transport_contract"]

check(
    "TRANSPORT_MATCH_CONNECT",
    net["connect_timeout_seconds"]
    == frozen_transport["connect_timeout_seconds"],
)

check(
    "TRANSPORT_MATCH_DEADLINE",
    net["complete_response_deadline_seconds"]
    == frozen_transport[
        "complete_response_deadline_seconds"
    ],
)

check(
    "TRANSPORT_MATCH_INVOCATIONS",
    net["maximum_transport_invocations_per_logical_slot"]
    == frozen_transport[
        "maximum_transport_invocations_per_logical_slot"
    ],
)

check(
    "TRANSPORT_MATCH_RETRIES",
    net["maximum_retries_after_initial_invocation"]
    == frozen_transport[
        "maximum_retries_after_initial_invocation"
    ],
)

check(
    "TRANSPORT_MATCH_BACKOFF",
    net["deterministic_backoff_seconds"]
    == frozen_transport["backoff_seconds"],
)

print("\n===== 14. RESPONSE PRESERVATION =====")

pres = contract["response_preservation"]

for key in (
    "raw_response_bytes_written_before_classification",
    "raw_response_sha256_required",
    "response_headers_retained_redacted",
    "credential_headers_never_retained",
    "complete_http_response_retained_even_when_error",
    "triggering_pause_response_retained",
):
    check(
        "PRES_" + key.upper(),
        pres[key] is True,
    )

check(
    "PRES_APPEND_ONLY",
    pres["write_mode"]
    == "append-only create-new; overwrite forbidden",
)

classification = contract["response_classification"]

check(
    "CLASSIFICATION_INTERFACE_AUTHORITY",
    classification[
        "provider_parser_authority"
    ]["sha256"]
    == EXPECTED["controller_interface"],
)

check(
    "CLASSIFICATION_POSTPROCESS_AUTHORITY",
    classification[
        "postprocessing_authority"
    ]["sha256"]
    == EXPECTED["postprocessing_contract"],
)

check(
    "NON2XX_API_ERROR",
    classification[
        "complete_non_2xx_http_response"
    ] == "API_ERROR",
)

check(
    "COMPLETE_HTTP_RETRY_FALSE",
    classification[
        "complete_http_response_retry"
    ] is False,
)

print("\n===== 15. COST ACCOUNTING =====")

cost = contract["cost_accounting"]

check(
    "PRICE_SHA_BOUND",
    cost["pricing_snapshot"]["sha256"]
    == EXPECTED["pricing_snapshot"],
)

check(
    "RAW_USAGE_PRESERVED",
    cost["raw_provider_usage_preserved"]
    is True,
)

check(
    "COST_ESTIMATE_REQUIRED",
    cost["estimate_required"] is True,
)

check(
    "COST_CURRENCY_USD",
    cost["currency"] == "USD",
)

ds_price = pricing["providers"]["deepseek"]["pricing"]
gm_price = pricing["providers"]["gemini"]["pricing"]

ds_cost = cost["DeepSeek"]

check(
    "DS_RATE_CACHE_HIT",
    ds_cost["rates"]["input_cache_hit"]
    == ds_price["input_cache_hit"]
    == 0.0028,
)

check(
    "DS_RATE_CACHE_MISS",
    ds_cost["rates"]["input_cache_miss"]
    == ds_price["input_cache_miss"]
    == 0.14,
)

check(
    "DS_RATE_OUTPUT",
    ds_cost["rates"]["output"]
    == ds_price["output"]
    == 0.28,
)

check(
    "DS_DIRECT_USAGE_FIELDS",
    ds_cost["usage_precedence"][0]["required_fields"]
    == [
        "prompt_cache_hit_tokens",
        "prompt_cache_miss_tokens",
        "completion_tokens",
    ],
)

check(
    "DS_DERIVED_USAGE_FIELDS",
    ds_cost["usage_precedence"][1]["required_fields"]
    == [
        "prompt_tokens",
        "prompt_tokens_details.cached_tokens",
        "completion_tokens",
    ],
)

check(
    "DS_INSUFFICIENT_USAGE_PAUSES",
    ds_cost["invalid_or_insufficient_usage"]
    == "PRESERVE_RESPONSE_AND_PAUSE_BEFORE_NEXT_CALL",
)

gm_cost = cost["Gemini"]

check(
    "GM_RATE_INPUT",
    gm_cost["rates"]["input"]
    == gm_price["text_image_video_input"]
    == 0.25,
)

check(
    "GM_RATE_OUTPUT",
    gm_cost["rates"][
        "output_including_thinking_tokens"
    ]
    == gm_price[
        "output_including_thinking_tokens"
    ]
    == 1.5,
)

check(
    "GM_REQUIRED_USAGE_FIELDS",
    gm_cost["required_usage_fields"]
    == [
        "promptTokenCount",
        "candidatesTokenCount",
    ],
)

check(
    "GM_POSITIVE_CACHE_PAUSES",
    gm_cost[
        "unexpected_positive_cachedContentTokenCount"
    ]
    == "PRESERVE_RESPONSE_AND_PAUSE_BEFORE_NEXT_CALL",
)

check(
    "GM_INSUFFICIENT_USAGE_PAUSES",
    gm_cost["invalid_or_insufficient_usage"]
    == "PRESERVE_RESPONSE_AND_PAUSE_BEFORE_NEXT_CALL",
)

print("\n===== 16. INVOCATION / PAUSE / STORAGE =====")

inv = contract["invocation_record"]

check(
    "INVOCATION_FROZEN_FIELDS_MATCH",
    inv["frozen_required_fields"]
    == protocol["preservation_contract"][
        "required_per_invocation_fields"
    ],
)

pause = contract["pause_contract"]

check(
    "PAUSE_ZERO_CALLS_AFTER",
    pause["calls_after_pause_before_resolution"]
    == 0,
)

check(
    "PAUSE_TRIGGER_PRESERVED",
    pause["triggering_invocation_preserved"]
    is True,
)

check(
    "PAUSE_REQUIRES_COMMITTED_RESOLUTION",
    pause["resume_requires_new_committed_resolution_evidence"]
    is True,
)

for frozen_condition in protocol[
    "pause_and_amendment_contract"
]["immediate_pause_conditions"]:
    check(
        "PAUSE_INCLUDES_FROZEN_"
        + re.sub(
            r"[^A-Za-z0-9]+",
            "_",
            frozen_condition,
        ).upper()[:60],
        frozen_condition in pause["conditions"],
    )

window = contract["window_and_storage"]

check(
    "WINDOW_ID_EXACT",
    window["window_id"]
    == "SVF-PRIMARY-800-V1",
)

check(
    "STORAGE_ROOT_MATCH",
    window["storage_root"]
    == interface[
        "append_only_storage_contract"
    ]["root"],
)

check(
    "WINDOW_OPEN_PATH_MATCH",
    window["window_open_record"]
    == interface[
        "append_only_storage_contract"
    ]["window_open_record"],
)

check(
    "WINDOW_CLOSE_PATH_MATCH",
    window["window_close_record"]
    == interface[
        "append_only_storage_contract"
    ]["window_close_record"],
)

check(
    "CANDIDATE_DOES_NOT_INIT_STORAGE",
    window[
        "storage_root_must_not_be_initialized_by_candidate_construction"
    ] is True,
)

print("\n===== 17. SEPARATION / NO-AUTHORIZATION =====")

sep = contract["separation"]

checks = {
    "CONTRACT_CREATES_NO_AUTH_RECORD":
        sep[
            "authorization_record_created_by_this_contract"
        ] is False,

    "WINDOW_NOT_OPENED":
        sep["generation_window_opened"] is False,

    "NO_LIVE_CALLS":
        sep["live_provider_calls_performed"] is False,

    "NO_PRIMARY_GENERATION":
        sep["primary_generation_performed"] is False,

    "NO_DRIVER_INSPECTION":
        sep[
            "generated_driver_human_inspection_allowed"
        ] is False,

    "NO_LINKED_EXECUTION":
        sep["linked_driver_execution_allowed"]
        is False,

    "NO_ANALYZER":
        sep[
            "analyzer_implementation_or_execution_allowed"
        ] is False,

    "NO_REPAIR":
        sep["repair_before_gate_v_allowed"]
        is False,

    "AUTH_RECORD_FILE_ABSENT":
        not AUTH_RECORD.exists(),

    "FROZEN_PROTOCOL_AUTH_FALSE":
        protocol["authorization"][
            "primary_generation_authorized"
        ] is False,

    "FROZEN_WINDOW_NOT_OPEN":
        protocol["execution_window"]["state"]
        == "FROZEN_NOT_OPEN",

    "PREAUTH_INTERFACE_CALLS_FALSE":
        interface["authorization_boundary"][
            "live_provider_calls_permitted_by_this_contract"
        ] is False,
}

for name, ok in checks.items():
    check(name, ok)

print("\n===== 18. SECRET-LEAK CHECK =====")

candidate_blob = (
    DECISION.read_bytes()
    + b"\n"
    + SCHEMA.read_bytes()
    + b"\n"
    + CONTRACT.read_bytes()
)

candidate_text = candidate_blob.decode(
    "utf-8",
    errors="ignore",
)

for env_name in (
    "DEEPSEEK_API_KEY",
    "GEMINI_API_KEY",
):
    value = os.environ.get(env_name)

    check(
        "NO_SECRET_VALUE_" + env_name,
        not value or value not in candidate_text,
    )

check(
    "NO_BEARER_VALUE",
    '"Authorization": "Bearer '
    not in candidate_text,
)

check(
    "NO_X_GOOG_KEY_VALUE",
    '"x-goog-api-key": "'
    not in candidate_text,
)

print("\n===== 19. CURRENT REPOSITORY CHANGE SET =====")

status = subprocess.check_output(
    [
        "git",
        "-C",
        str(ROOT),
        "status",
        "--short",
        "--untracked-files=all",
    ],
    text=True,
)

print(status.rstrip())

untracked = []

for line in status.splitlines():
    if line.startswith("?? "):
        untracked.append(line[3:])

expected_untracked = {
    "config/primary_live_transport_contract.v1.json",
    "config/schemas/primary_generation_authorization_record.schema.json",
    "documentation/decisions/"
    "0012-primary-generation-authorization-and-live-transport-boundary.md",
    "evidence/generation_opening/primary_live_transport_v1/"
    "qualification.prefreeze.v1.json",
    "evidence/generation_opening/primary_operational_runner_v1/"
    "qualification.prefreeze.v1.json",
    "scripts/primary_live_transport_v1.py",
    "scripts/primary_operational_runner_v1.py",
    "scripts/verify_primary_live_transport_contract_v1.py",
}

check(
    "EXACT_EIGHT_UNTRACKED_CANDIDATE_FILES",
    set(untracked) == expected_untracked
    and len(untracked) == 8,
    repr(untracked),
)


print(
    "\n===== 19B. OPERATIONAL RUNNER / LIVE TRANSPORT PACKAGE ====="
)

import ast as _svf_ast

OP_LIVE_TRANSPORT = ROOT / (
    "scripts/primary_live_transport_v1.py"
)

OP_LIVE_QUAL = ROOT / (
    "evidence/generation_opening/"
    "primary_live_transport_v1/"
    "qualification.prefreeze.v1.json"
)

OP_RUNNER = ROOT / (
    "scripts/primary_operational_runner_v1.py"
)

OP_RUNNER_QUAL = ROOT / (
    "evidence/generation_opening/"
    "primary_operational_runner_v1/"
    "qualification.prefreeze.v1.json"
)

OP_EXPECTED = {
    "decision":
        "8920fb4cd379b02727f4d8efa6e675961ddc9eff48d679f8fb9f4b78f0b61609",

    "contract":
        "59474347ee27339f1f42247c310786b658f315113dcb2501ab53c9d7ad9b965b",

    "live_transport":
        "325ef9a7817acaaaa84c0f1ff28c4dfed4c92bf6c3f1cb032c83e5694a4cfbdd",

    "live_qualification":
        "fb3426463864400afaf7e11dd98148f972947b05a3961d8016063693c0396858",

    "operational_runner":
        "553ac68643193e64b58be1fc2c8cfbb3d9f24e98f7c7c75834e297d5532fd84e",

    "operational_qualification":
        "66189432f694ea3d19afec7d876ea50b7a10a586b0b122d84ae5629d2e4d3cc3",
}

op_paths = {
    "decision":
        DECISION,

    "contract":
        CONTRACT,

    "live_transport":
        OP_LIVE_TRANSPORT,

    "live_qualification":
        OP_LIVE_QUAL,

    "operational_runner":
        OP_RUNNER,

    "operational_qualification":
        OP_RUNNER_QUAL,
}

for name, path in op_paths.items():
    check(
        "OP_FILE_EXISTS_"
        + name.upper(),
        path.is_file(),
    )

    if path.is_file():
        check(
            "OP_HASH_"
            + name.upper(),
            sha_file(path)
            == OP_EXPECTED[name],
            sha_file(path),
        )

live_q = json.loads(
    OP_LIVE_QUAL.read_text()
)

runner_q = json.loads(
    OP_RUNNER_QUAL.read_text()
)

runner_src = OP_RUNNER.read_text()

check(
    "LIVE_QUAL_STATUS_PASS",
    live_q.get("status")
    == "PASS",
)

check(
    "LIVE_QUAL_FAILURE_COUNT_ZERO",
    live_q.get("failure_count")
    == 0,
)

check(
    "LIVE_QUAL_BINDS_IMPLEMENTATION",
    live_q[
        "implementation"
    ]["sha256"]
    == OP_EXPECTED["live_transport"],
)

check(
    "LIVE_QUAL_BINDS_CONTRACT",
    live_q[
        "contract"
    ]["sha256"]
    == OP_EXPECTED["contract"],
)

# The persisted live-transport qualification does not contain a
# "real_https_transport_invoked" field. Do not infer or fabricate it.
# Persisted safety evidence is checked exactly as recorded.
check(
    "LIVE_QUAL_NO_PROVIDER_CALLS",
    live_q.get(
        "live_provider_calls"
    )
    == 0,
)

check(
    "LIVE_QUAL_NO_SECRET_READ",
    live_q.get(
        "api_secret_environment_values_read"
    )
    is False,
)

check(
    "LIVE_QUAL_PRIMARY_NOT_AUTHORIZED",
    live_q.get(
        "primary_generation_authorized"
    )
    is False,
)

check(
    "LIVE_QUAL_WINDOW_NOT_OPENED",
    live_q.get(
        "generation_window_opened"
    )
    is False,
)

check(
    "LIVE_QUAL_NO_PRIMARY_GENERATION",
    live_q.get(
        "primary_generation_performed"
    )
    is False,
)

check(
    "RUNNER_QUAL_STATUS_PASS",
    runner_q.get("status")
    == "PASS",
)

check(
    "RUNNER_QUAL_FAILURE_COUNT_ZERO",
    runner_q.get(
        "failure_count"
    )
    == 0,
)

check(
    "RUNNER_QUAL_BINDS_RUNNER",
    runner_q[
        "runner"
    ]["sha256"]
    == OP_EXPECTED[
        "operational_runner"
    ],
)

check(
    "RUNNER_QUAL_BINDS_TRANSPORT",
    runner_q[
        "live_transport"
    ]["sha256"]
    == OP_EXPECTED[
        "live_transport"
    ],
)

check(
    "RUNNER_QUAL_BINDS_CONTRACT",
    runner_q[
        "contract"
    ]["sha256"]
    == OP_EXPECTED["contract"],
)

check(
    "RUNNER_QUAL_NO_REAL_NETWORK",
    runner_q.get(
        "real_network_transport_invoked"
    )
    is False,
)

check(
    "RUNNER_QUAL_NO_SECRET_READ",
    runner_q.get(
        "api_secret_environment_values_read"
    )
    is False,
)

check(
    "RUNNER_QUAL_NO_PRIMARY_GENERATION",
    runner_q.get(
        "primary_generation_performed"
    )
    is False,
)

check(
    "RUNNER_QUAL_NO_DRIVER_INSPECTION",
    runner_q.get(
        "generated_driver_human_inspection"
    )
    is False,
)

check(
    "RUNNER_QUAL_NO_LINKED_EXECUTION",
    runner_q.get(
        "linked_driver_execution"
    )
    is False,
)

driver_storage = contract[
    "driver_source_storage_contract"
]

check(
    "DRIVER_SOURCE_TEMPLATE_EXACT",
    driver_storage[
        "driver_source_template"
    ]
    == "slots/{logical_slot_id}/driver.c",
)

check(
    "DRIVER_SOURCE_UTF8_NO_BOM",
    driver_storage[
        "bytes_rule"
    ].startswith(
        "UTF-8 encoding without BOM"
    ),
)

check(
    "DRIVER_SOURCE_NO_TRANSFORMATIONS",
    driver_storage[
        "transformations_allowed"
    ]
    is False,
)

check(
    "DRIVER_SOURCE_NO_NEWLINE_CHANGE",
    driver_storage[
        "newline_insertion_or_removal_allowed"
    ]
    is False,
)

check(
    "DRIVER_WRITTEN_BEFORE_DUPLICATE",
    driver_storage[
        "write_before_duplicate_classification"
    ]
    is True,
)

check(
    "DRIVER_WRITTEN_BEFORE_COMPILE",
    driver_storage[
        "write_before_compilation"
    ]
    is True,
)

check(
    "DUPLICATE_SOURCE_RETAINED",
    driver_storage[
        "duplicate_policy"
    ][
        "duplicate_source_file_retained"
    ]
    is True,
)

check(
    "DUPLICATE_SOURCE_NOT_COMPILED",
    driver_storage[
        "duplicate_policy"
    ][
        "duplicate_source_file_compiled"
    ]
    is False,
)

op_contract = contract[
    "operational_runner_contract"
]

check(
    "OP_RUNNER_PATH_EXACT",
    op_contract[
        "runner_path"
    ]
    == "scripts/primary_operational_runner_v1.py",
)

check(
    "OP_RUNNER_AUTHORIZATION_READY",
    op_contract[
        "candidate_state"
    ]
    == "FROZEN_AUTHORIZATION_READY",
)

check(
    "OP_LIVE_CLI_EXACT",
    op_contract[
        "live_cli_flag"
    ]
    == "--execute-primary",
)

proxy = op_contract[
    "proxy_policy"
]

check(
    "PROXY_ENV_DISCOVERY",
    proxy[
        "environment_proxy_discovery"
    ]
    is True,
)

check(
    "PROXY_HTTPS_PREFERRED",
    proxy[
        "https_proxy_preferred"
    ]
    is True,
)

check(
    "PROXY_HTTP_FALLBACK",
    proxy[
        "http_proxy_fallback"
    ]
    is True,
)

check(
    "PROXY_NO_PROXY_HONORED",
    proxy[
        "no_proxy_honored"
    ]
    is True,
)

check(
    "PROXY_SCHEME_HTTP",
    proxy[
        "supported_proxy_scheme"
    ]
    == "http",
)

check(
    "PROXY_CONNECT_TLS",
    "HTTP CONNECT"
    in proxy[
        "https_over_http_proxy"
    ],
)

check(
    "PROXY_CREDENTIALS_UNSUPPORTED",
    proxy[
        "embedded_proxy_credentials_supported"
    ]
    is False,
)

window = op_contract[
    "window_lifecycle"
]

check(
    "WINDOW_OPEN_PATH_EXACT",
    window[
        "open_record"
    ]
    == "window/open.json",
)

check(
    "WINDOW_CLOSE_PATH_EXACT",
    window[
        "close_record"
    ]
    == "window/close.json",
)

check(
    "WINDOW_OPEN_BEFORE_SLOT1",
    "immediately before logical slot 0001"
    in window[
        "open_record_rule"
    ],
)

check(
    "WINDOW_CLOSE_AFTER_800",
    "all 800 logical slots"
    in window[
        "close_record_rule"
    ],
)

handoff = op_contract[
    "postprocessing_handoff"
]

check(
    "OP_DRIVER_TEMPLATE_MATCHES",
    handoff[
        "driver_source_template"
    ]
    == "slots/{logical_slot_id}/driver.c",
)

check(
    "OP_COMPILER_CLANG14",
    handoff[
        "compiler"
    ]
    == "/usr/bin/clang-14",
)

check(
    "OP_WEAK_MAIN_ENABLED",
    handoff[
        "weak_main_shim"
    ]
    is True,
)

check(
    "OP_NO_LINKED_EXECUTION",
    handoff[
        "linked_driver_execution"
    ]
    is False,
)

check(
    "OP_NO_SOURCE_REPAIR",
    handoff[
        "source_repair"
    ]
    is False,
)

pause_op = op_contract[
    "pause_before_next_call"
]

endpoint_op = pause_op[
    "endpoint_behavior_material_change"
]

service_op = pause_op[
    "provider_outage_or_repeated_service_errors"
]

check(
    "ENDPOINT_REDIRECT_PAUSE",
    endpoint_op[
        "http_redirect_300_399"
    ]
    == "IMMEDIATE_PAUSE",
)

check(
    "ENDPOINT_NONJSON_2XX_PAUSE",
    endpoint_op[
        "successful_2xx_non_json_object"
    ]
    == "IMMEDIATE_PAUSE",
)

check(
    "ENDPOINT_MISSING_ENVELOPE_PAUSE",
    endpoint_op[
        "successful_2xx_missing_provider_envelope"
    ]
    == "IMMEDIATE_PAUSE",
)

check(
    "OUTAGE_STATUSES_EXACT",
    service_op[
        "immediate_outage_http_statuses"
    ]
    == [502, 503, 504],
)

check(
    "REPEATED_5XX_THRESHOLD_TWO",
    service_op[
        "repeated_error_threshold"
    ]
    == 2,
)

check(
    "SERVICE_ERRORS_PROVIDER_SCOPED",
    service_op[
        "scope"
    ]
    == "per provider/model label",
)

# Verify driver path is contract-driven rather than requiring the
# literal template to be duplicated in runner source.
runner_tree = _svf_ast.parse(
    runner_src
)

driver_rel_node = next(
    (
        node
        for node in runner_tree.body
        if (
            isinstance(
                node,
                _svf_ast.FunctionDef,
            )
            and node.name == "driver_rel"
        )
    ),
    None,
)

check(
    "RUNNER_DRIVER_REL_PRESENT",
    driver_rel_node
    is not None,
)

if driver_rel_node is not None:
    driver_rel_src = (
        _svf_ast.get_source_segment(
            runner_src,
            driver_rel_node,
        )
        or ""
    )

    check(
        "RUNNER_DRIVER_REL_READS_STORAGE_CONTRACT",
        "driver_source_storage_contract"
        in driver_rel_src,
    )

    check(
        "RUNNER_DRIVER_REL_READS_TEMPLATE",
        "driver_source_template"
        in driver_rel_src,
    )

    check(
        "RUNNER_DRIVER_REL_FORMATS_SLOT_ID",
        "logical_slot_id"
        in driver_rel_src,
    )

    synthetic_driver_path = (
        driver_storage[
            "driver_source_template"
        ].format(
            logical_slot_id=
                "SVF-PRIMARY-800-V1-SLOT-0001"
        )
    )

    check(
        "RUNNER_DRIVER_PATH_SYNTHETIC_RESOLUTION",
        synthetic_driver_path
        == (
            "slots/"
            "SVF-PRIMARY-800-V1-SLOT-0001/"
            "driver.c"
        ),
    )

runner_terms = {
    "HTTP_CONNECT":
        "HTTP_CONNECT",

    "PROXY_SET_TUNNEL":
        "set_tunnel",

    "WINDOW_OPEN":
        "window/open.json",

    "WINDOW_CLOSE":
        "window/close.json",

    "ENDPOINT_BEHAVIOR":
        "ENDPOINT_BEHAVIOR_MATERIALLY_CHANGED",

    "REPEATED_SERVICE":
        "REPEATED_SERVICE_HTTP_ERRORS",

    "AUTH_PATH":
        "authorization_record_path",

    "AUTH_SHA":
        "authorization_record_sha256",

    "EXECUTION_HEAD":
        "execution_head_commit",

    "REQUEST_SHA_VERIFIED":
        "request_body_sha256_verified",

    "REQUEST_BYTE_LENGTH":
        "request_body_byte_length",

    "COST_STATUS":
        "cost_estimate_status",
}

for name, term in runner_terms.items():
    check(
        "RUNNER_TERM_"
        + name,
        term in runner_src,
    )

perform = next(
    (
        node
        for node in runner_tree.body
        if (
            isinstance(
                node,
                _svf_ast.FunctionDef,
            )
            and node.name
            == "perform_transport"
        )
    ),
    None,
)

check(
    "RUNNER_PERFORM_TRANSPORT_PRESENT",
    perform is not None,
)

if perform is not None:
    inv_dicts = []

    for node in _svf_ast.walk(
        perform
    ):
        if not isinstance(
            node,
            _svf_ast.Assign,
        ):
            continue

        if not any(
            isinstance(
                target,
                _svf_ast.Name,
            )
            and target.id == "inv"
            for target in node.targets
        ):
            continue

        if not isinstance(
            node.value,
            _svf_ast.Dict,
        ):
            continue

        keys = {
            key.value
            for key in node.value.keys
            if (
                isinstance(
                    key,
                    _svf_ast.Constant,
                )
                and isinstance(
                    key.value,
                    str,
                )
            )
        }

        inv_dicts.append(
            keys
        )

    check(
        "RUNNER_INVOCATION_DICT_COUNT_TWO",
        len(inv_dicts)
        == 2,
        repr(
            [
                sorted(x)
                for x in inv_dicts
            ]
        ),
    )

    required_invocation_fields = (
        set(
            protocol[
                "preservation_contract"
            ][
                "required_per_invocation_fields"
            ]
        )
        |
        set(
            contract[
                "invocation_record"
            ][
                "additional_live_transport_fields"
            ]
        )
    )

    for idx, keys in enumerate(
        inv_dicts,
        1,
    ):
        check(
            "RUNNER_INVOCATION_"
            + str(idx)
            + "_ALL_REQUIRED_FIELDS",
            required_invocation_fields
            <= keys,
            repr(
                sorted(
                    required_invocation_fields
                    - keys
                )
            ),
        )

expected_additive = {
    "authorization_record_path",
    "authorization_record_sha256",
    "execution_head_commit",
    "request_body_sha256_verified",
    "request_body_byte_length",
    "endpoint",
    "transport_invocation_number",
    "transport_retry_classification",
    "response_headers_redacted",
    "cost_estimate_status",
}

check(
    "CONTRACT_ADDITIVE_INVOCATION_FIELDS_EXACT",
    set(
        contract[
            "invocation_record"
        ][
            "additional_live_transport_fields"
        ]
    )
    == expected_additive,
)

check(
    "CONTRACT_FROZEN_AUTHORIZATION_READY",
    contract["status"]
    == "FROZEN_AUTHORIZATION_READY",
)

check(
    "CONTRACT_EXECUTION_CAPABILITY_ENABLED",
    contract[
        "authorization_gate"
    ][
        "execution_enabled"
    ]
    is True,
)

check(
    "CONTRACT_LIVE_NETWORK_CAPABILITY_ENABLED",
    contract[
        "network_transport"
    ][
        "live_network_calls_allowed_by_this_candidate"
    ]
    is True,
)

check(
    "CONTRACT_IMPLEMENTATION_AUTHORIZATION_READY",
    contract[
        "network_transport"
    ][
        "implementation_status"
    ]
    == "FROZEN_AUTHORIZATION_READY",
)

check(
    "OP_AUTH_RECORD_STILL_ABSENT",
    not AUTH_RECORD.exists(),
)

print("\n===== 20. FINAL RESULT =====")

print("FAIL_COUNT=" + str(failures))

print(
    "VERIFIER_RESULT="
    + ("PASS" if failures == 0 else "FAIL")
)

print("AUTHORIZATION_RECORD_CREATED=NO")
print("API_SECRETS_READ=NO")
print("LIVE_PROVIDER_CALLS=NO")
print("PRIMARY_GENERATION_AUTHORIZED=NO")
print("GENERATION_WINDOW_STATE=FROZEN_NOT_OPEN")
print("PRIMARY_GENERATION_PERFORMED=NO")
print("GENERATED_DRIVER_INSPECTION=NO")
print("ANALYZER_IMPLEMENTATION=NO")
print("REPAIR_IMPLEMENTATION=NO")
print("FILES_WRITTEN_BY_VERIFIER=NO")

raise SystemExit(0 if failures == 0 else 1)
