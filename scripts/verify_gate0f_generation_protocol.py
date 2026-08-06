#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "config/generation_execution_protocol.json"
LOCK = ROOT / "config/research_lock.json"

def require(condition, reason):
    if not condition:
        print("GATE0F_GENERATION_PROTOCOL_FREEZE=FAIL")
        print(f"REASON={reason}")
        raise SystemExit(1)

protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))

require(protocol["gate"] == "Gate 0F", "gate identity")
require(protocol["status"] == "PASS_FROZEN", "freeze status")
require(protocol["execution_window"]["window_count"] == 1, "window count")
require(protocol["execution_window"]["state"] == "FROZEN_NOT_OPEN", "window opened")

design = protocol["logical_attempt_design"]
require(len(design["models"]) == 2, "model count")
require(len(design["libraries_in_frozen_order"]) == 8, "library count")
require(design["scenarios_per_library"] == 10, "scenario count")
require(design["attempts_per_model_library_scenario"] == 5, "attempt count")
require(2 * 8 * 10 * 5 == design["logical_slot_count"] == 800, "800 arithmetic")
require(design["slot_replacement_allowed"] is False, "slot replacement")
require(design["generation_never_continues_for_target_yield"] is True, "yield chasing")
require(design["slot_order"]["global_max_in_flight_requests"] == 1, "concurrency")

request = protocol["request_contract"]
require(request["temperature"] == 0.2, "temperature")
require(request["top_p"] == 1.0, "top-p")
require(request["maximum_output_tokens"] == 8192, "maximum output")
require(request["stream"] is False, "stream")
require(request["payload_change_during_retry_allowed"] is False, "retry mutation")

retry = protocol["transport_retry_policy"]
require(retry["maximum_retries_after_initial_invocation"] == 2, "retry count")
require(retry["maximum_transport_invocations_per_logical_slot"] == 3, "invocation count")
require(retry["deterministic_backoff_seconds"] == [5, 20], "backoff")
require(retry["jitter_seconds"] == 0, "retry jitter")
require(
    "ANY_COMPLETE_HTTP_RESPONSE_INCLUDING_4XX_OR_5XX"
    in retry["non_retryable_failures"],
    "HTTP response retry prohibition",
)
require(retry["all_invocations_retained"] is True, "invocation retention")
require(retry["exhausted_slot_replaced"] is False, "failed slot replacement")

terminal = protocol["terminal_status_contract"]
require(terminal["compilation_denominator"] == "all 800 logical slots", "denominator")
require(terminal["failure_output_discard_allowed"] is False, "failure discard")

preservation = protocol["preservation_contract"]
require(preservation["raw_response_retained_per_complete_call"] is True, "raw retention")
require(preservation["api_keys_stored_printed_or_hashed"] is False, "secret handling")

pause = protocol["pause_and_amendment_contract"]
require(pause["calls_after_pause_before_resolution"] == 0, "pause leakage")
require(pause["silent_model_substitution_allowed"] is False, "model substitution")
require(pause["post_hoc_parameter_change_allowed"] is False, "parameter change")

authorization = protocol["authorization"]
require(authorization["primary_generation_authorized"] is False, "generation authorized")
require(authorization["repair_implementation_allowed"] is False, "repair enabled")
require(authorization["repair_activation_gate"] == "Gate V", "repair gate")

for secret_name in ("DEEPSEEK_API_KEY", "GEMINI_API_KEY"):
    require(not os.environ.get(secret_name), f"{secret_name} present during verifier")

locked = lock["generation_protocol"]
actual_sha = hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
require(locked["status"] == "PASS", "research lock protocol status")
require(locked["sha256"] == actual_sha, "research lock protocol hash")
require(locked["logical_attempts"] == 800, "research lock attempt count")
require(locked["primary_generation_authorized"] is False, "lock generation authorization")
require(locked["repair_implementation_allowed"] is False, "lock repair authorization")

current = lock["current_status"]
require(
    current["gate_0"] in {"IN_PROGRESS", "PASS"},
    "Gate 0 status is invalid",
)
require(current["gate_0f_generation_protocol"] == "PASS", "Gate 0F status")

print("GATE0F_GENERATION_PROTOCOL_FREEZE=PASS")
print("EXECUTION_WINDOWS=1")
print("LOGICAL_ATTEMPTS=800")
print("MAX_TRANSPORT_INVOCATIONS_PER_SLOT=3")
print("HTTP_RESPONSES_RETRIED=NO")
print("ALL_INVOCATIONS_RETAINED=YES")
print("GENERATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"PROTOCOL_SHA256={actual_sha}")
