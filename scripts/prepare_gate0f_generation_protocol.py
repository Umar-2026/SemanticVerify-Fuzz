#!/usr/bin/env python3
"""Prepare the proposal-locked Gate 0F generation execution protocol.

This script is intentionally preparation-only: it writes auditable protocol
files, updates Gate 0 status documents, and runs read-only verifiers.  It does
not call either model API, authorize primary generation, or commit changes.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path


EXPECTED_HEAD = "1b9aa8b2d2b3cd3d041501f70de0c29558c5deee"
EXPECTED_PROPOSAL_SHA256 = (
    "3abc92ee7ac0100a6b9ac148a2ad2a4ca"
    "71d187677cb84abf1545de29afb4a21"
)
EXPECTED_REGISTRATION_SHA256 = (
    "c7537ce5d082de904cc7aef4d617c9ff"
    "6612b30fdb4740b0667c9eb84ca5b2d4"
)
EXPECTED_LIVE_REPORT_SHA256 = (
    "f0b22b51684605677d4bfbfa4b187227"
    "c67093fc4c79792412797e28cb30f5c4"
)

ROOT = Path.cwd().resolve()
SELF_REL = "scripts/prepare_gate0f_generation_protocol.py"
PROTOCOL_REL = "config/generation_execution_protocol.json"
VERIFIER_REL = "scripts/verify_gate0f_generation_protocol.py"
DECISION_REL = (
    "documentation/decisions/"
    "0005-generation-window-and-transport-retry-freeze.md"
)
LOCK_REL = "config/research_lock.json"
STATUS_REL = "documentation/CURRENT_STATUS.md"
README_REL = "evidence/gates/gate0/README.md"


def fail(reason: str) -> None:
    print("GATE0F_GENERATION_PROTOCOL_PREPARATION=FAIL")
    print(f"REASON={reason}")
    raise SystemExit(1)


def require(condition: bool, reason: str) -> None:
    if not condition:
        fail(reason)


def run(args: list[str], *, capture: bool = False) -> str:
    print("RUN=" + " ".join(args))
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=capture,
    )
    if capture:
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        output = result.stdout
    else:
        output = ""
    require(result.returncode == 0, f"command failed: {' '.join(args)}")
    return output


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read JSON {path.relative_to(ROOT)}: {error}")


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


require(ROOT.name == "semanticverify-fuzz-research", "wrong repository directory")
require((ROOT / ".git").exists(), "repository metadata missing")

head = run(["git", "rev-parse", "HEAD"], capture=True).strip()
require(head == EXPECTED_HEAD, f"unexpected HEAD: {head}")

status_lines = [
    line
    for line in run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        capture=True,
    ).splitlines()
    if line
]
require(
    status_lines in ([], [f"?? {SELF_REL}"]),
    f"unexpected pre-existing changes: {status_lines}",
)

for secret_name in ("DEEPSEEK_API_KEY", "GEMINI_API_KEY"):
    require(not os.environ.get(secret_name), f"{secret_name} must be unset")

proposal = (
    ROOT
    / "provenance/proposal/"
    "SemanticVerify-Fuzz_Verification-First_Staged-Repair_Proposal.docx"
)
registration_path = ROOT / "config/statistical_analysis_registration.json"
live_report_path = ROOT / "evidence/gates/gate0/model_live_qualification.json"

require(proposal.is_file(), "authoritative proposal missing")
require(digest(proposal) == EXPECTED_PROPOSAL_SHA256, "proposal hash mismatch")
require(
    digest(registration_path) == EXPECTED_REGISTRATION_SHA256,
    "frozen statistical registration hash mismatch",
)
require(
    digest(live_report_path) == EXPECTED_LIVE_REPORT_SHA256,
    "live qualification report hash mismatch",
)

protocol = {
    "schema_version": "1.0.0",
    "gate": "Gate 0F",
    "status": "PASS_FROZEN",
    "authority": {
        "proposal_sha256": EXPECTED_PROPOSAL_SHA256,
        "proposal_sections": [
            "7.5 Fixed generation design and sampling-bias control",
            "15. Pre-Experiment Registration Checklist",
        ],
        "interpretation": (
            "The proposal fixes the experiment and permits retries only for "
            "transport failure. Gate 0F supplies the missing operational "
            "constants without changing the 800-attempt design."
        ),
    },
    "execution_window": {
        "window_id": "SVF-PRIMARY-800-V1",
        "window_count": 1,
        "state": "FROZEN_NOT_OPEN",
        "opening_preconditions": [
            "final Gate 0 manifest is PASS",
            "Gate 1 specification foundation is PASS",
            "system prompt and all 80 scenario bindings are frozen",
            "both provider capabilities still match Gate 0D2",
            "price-sheet snapshots and library source locks are archived",
            "an explicit committed authorization record exists",
        ],
        "opened_at_utc_rule": "timestamp immediately before logical slot 0001",
        "closed_at_utc_rule": (
            "timestamp after all 800 logical slots have terminal records"
        ),
        "pause_intervals": "append-only UTC start/end/reason records",
        "calendar_timestamps": {
            "opened_at_utc": None,
            "closed_at_utc": None,
        },
        "calendar_timestamp_null_reason": (
            "No primary call is authorized. Actual timestamps are written "
            "only by the future execution controller."
        ),
        "no_second_window_without_amendment": True,
    },
    "logical_attempt_design": {
        "models": [
            {
                "label": "Model A",
                "provider": "DeepSeek",
                "model_id": "deepseek-v4-flash",
                "expected_response_model": "deepseek-v4-flash",
                "documented_served_version": "DeepSeek-V4-Flash-0731",
                "thinking_mode": "disabled",
            },
            {
                "label": "Model B",
                "provider": "Google Gemini Developer API",
                "model_id": "gemini-3.1-flash-lite",
                "expected_response_model_version": "gemini-3.1-flash-lite",
                "thinking_mode": "MINIMAL",
            },
        ],
        "libraries_in_frozen_order": [
            "zlib",
            "libpcap",
            "curl",
            "cJSON",
            "libtiff",
            "libvpx",
            "c-ares",
            "lcms",
        ],
        "scenarios_per_library": 10,
        "attempts_per_model_library_scenario": 5,
        "logical_slot_count": 800,
        "slot_denominator_never_expands": True,
        "slot_replacement_allowed": False,
        "generation_never_continues_for_target_yield": True,
        "slot_order": {
            "type": "canonical_model-paired_sequential",
            "nesting": [
                "library frozen order",
                "scenario S01 through S10",
                "replicate R01 through R05",
                "Model A then Model B",
            ],
            "global_max_in_flight_requests": 1,
            "order_change_allowed": False,
        },
    },
    "request_contract": {
        "system_prompt": "FROZEN_AT_GATE_1",
        "scenario_manifest": "FROZEN_AT_GATE_1",
        "prompt_exclusions": [
            "protocol rules",
            "defect examples",
            "verifier output",
            "manual labels",
            "repair feedback",
        ],
        "temperature": 0.2,
        "top_p": 1.0,
        "top_p_rule": "send where supported; otherwise record provider default",
        "maximum_output_tokens": 8192,
        "stream": False,
        "seed_rule": (
            "Record supplied seed when supported; otherwise record null and "
            "the provider default. Never substitute an unregistered seed."
        ),
        "payload_change_during_retry_allowed": False,
    },
    "timeout_contract": {
        "connect_timeout_seconds": 30,
        "complete_response_deadline_seconds": 300,
        "timeout_is_distinct_terminal_status": True,
    },
    "transport_retry_policy": {
        "retry_scope": "same logical slot and byte-identical secret-free payload",
        "maximum_retries_after_initial_invocation": 2,
        "maximum_transport_invocations_per_logical_slot": 3,
        "deterministic_backoff_seconds": [5, 20],
        "jitter_seconds": 0,
        "retryable_failures": [
            "DNS_RESOLUTION_FAILURE",
            "TCP_CONNECT_FAILURE",
            "TLS_HANDSHAKE_FAILURE",
            "CONNECTION_RESET_BEFORE_COMPLETE_HTTP_RESPONSE",
            "CONNECT_TIMEOUT",
            "READ_TIMEOUT_BEFORE_COMPLETE_HTTP_RESPONSE",
        ],
        "non_retryable_failures": [
            "ANY_COMPLETE_HTTP_RESPONSE_INCLUDING_4XX_OR_5XX",
            "PROVIDER_API_ERROR_BODY",
            "REFUSAL_OR_SAFETY_BLOCK",
            "TRUNCATED_OUTPUT",
            "MISSING_CODE",
            "DUPLICATE_OUTPUT",
            "EXTRACTION_FAILURE",
            "NON_COMPILATION",
        ],
        "retry_invocations_are_new_experimental_attempts": False,
        "all_invocations_retained": True,
        "exhausted_retry_result": "TRANSPORT_FAILURE_TERMINAL",
        "exhausted_slot_replaced": False,
    },
    "terminal_status_contract": {
        "exactly_one_terminal_status_per_logical_slot": True,
        "statuses": [
            "RESPONSE_RECEIVED",
            "REFUSAL",
            "TIMEOUT",
            "API_ERROR",
            "TRUNCATED_OUTPUT",
            "MISSING_CODE",
            "DUPLICATE_OUTPUT",
            "EXTRACTION_FAILURE",
            "NON_COMPILATION",
            "TRANSPORT_FAILURE",
        ],
        "compilation_denominator": "all 800 logical slots",
        "failure_output_discard_allowed": False,
    },
    "preservation_contract": {
        "write_mode": "append-only with create-new semantics",
        "raw_response_retained_per_complete_call": True,
        "transport_failure_record_retained_per_invocation": True,
        "request_payload_retained_secret_free": True,
        "response_headers_retained_secret_redacted": True,
        "sha256_for_every_retained_blob": True,
        "required_per_invocation_fields": [
            "window_id",
            "logical_slot_id",
            "transport_invocation_number",
            "provider",
            "requested_model_id",
            "returned_model_or_version",
            "request_started_at_utc",
            "request_finished_at_utc",
            "request_parameters",
            "latency_ms",
            "HTTP_status_or_transport_failure",
            "raw_response_path_or_null",
            "raw_response_sha256_or_null",
            "token_usage",
            "cost_basis_and_estimate",
        ],
        "required_per_slot_postprocessing_fields": [
            "terminal_status",
            "extraction_status",
            "compiler_command",
            "compiler_version",
            "compiler_exit_code",
            "complete_log_path",
        ],
        "api_keys_stored_printed_or_hashed": False,
    },
    "pause_and_amendment_contract": {
        "immediate_pause_conditions": [
            "returned model or served version differs from frozen target",
            "non-thinking or minimum-thinking control is rejected",
            "endpoint behavior materially changes",
            "authentication, balance, permission, or rate-limit HTTP response",
            "provider outage or repeated service HTTP errors",
            "preservation or manifest write fails",
            "request payload differs from frozen bytes",
        ],
        "triggering_slot_and_response_are_preserved": True,
        "calls_after_pause_before_resolution": 0,
        "resume_requirements": [
            "root cause recorded",
            "integrity of all prior records verified",
            "capability requalification passes",
            "preregistration amendment committed when required",
        ],
        "silent_model_substitution_allowed": False,
        "post_hoc_parameter_change_allowed": False,
    },
    "quarantine_contract": {
        "automated_preservation_and_build_allowed_after_authorization": True,
        "human_inspection_of_held_out_driver_content": False,
        "held_out_release_condition": "proposal-defined analyzer/specification freeze",
        "repair_prompt_output_or_feedback_allowed": False,
    },
    "authorization": {
        "primary_generation_authorized": False,
        "reason": (
            "Gate 0 is still in progress and Gate 1 prompts/scenarios are not frozen."
        ),
        "repair_implementation_allowed": False,
        "repair_activation_gate": "Gate V",
    },
}

protocol_path = ROOT / PROTOCOL_REL
require(not protocol_path.exists(), f"refusing to overwrite {PROTOCOL_REL}")
write_json(protocol_path, protocol)

verifier_source = r'''#!/usr/bin/env python3
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
require(current["gate_0"] == "IN_PROGRESS", "Gate 0 closed early")
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
'''

verifier_path = ROOT / VERIFIER_REL
require(not verifier_path.exists(), f"refusing to overwrite {VERIFIER_REL}")
verifier_path.write_text(verifier_source, encoding="utf-8")
verifier_path.chmod(verifier_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

decision = """# Decision 0005: Generation Window and Transport-Retry Freeze

- Status: Accepted
- Date: 2026-08-06
- Stage: Gate 0F

## Proposal authority

Section 7.5 fixes 800 logical attempts, complete raw-output preservation,
distinct failure statuses, and retries only for transport failure. The
pre-experiment checklist requires one archived generation window and a frozen
retry policy. This decision supplies only the operational constants that the
proposal leaves unspecified.

## Frozen execution contract

- One campaign: `SVF-PRIMARY-800-V1`.
- Exactly 800 logical slots: 2 models x 8 libraries x 10 scenarios x 5 runs.
- Sequential canonical model-paired order; one request in flight globally.
- No failed slot is replaced and generation never expands to obtain a desired
  compilation or defect yield.
- Temperature 0.2, top-p 1.0 where supported, maximum output 8,192 tokens,
  streaming disabled, and provider seed/default behavior recorded.

## Retry boundary

Only failures before a complete HTTP response may be retried. A logical slot
has at most two retries after its first invocation, with deterministic waits of
5 and 20 seconds. Every invocation is retained. Any complete HTTP response,
including 4xx or 5xx, is an experimental API outcome and is never retried.

## Stop and preservation rules

Returned-model/version drift, rejection of thinking controls, material endpoint
change, authentication/balance/rate-limit failure, preservation failure, or
payload drift pauses further calls immediately. The triggering record is kept.
No silent model substitution, parameter change, slot replacement, or output
discard is allowed.

## Authorization

This freeze does not open the window. Primary generation remains unauthorized
until the final Gate 0 manifest, Gate 1 specification freeze, exact prompts and
80 scenario bindings, source locks, price snapshots, and a committed execution
authorization all pass. Repair remains prohibited until Gate V.
"""

decision_path = ROOT / DECISION_REL
require(not decision_path.exists(), f"refusing to overwrite {DECISION_REL}")
decision_path.parent.mkdir(parents=True, exist_ok=True)
decision_path.write_text(decision, encoding="utf-8")

protocol_sha = digest(protocol_path)
lock_path = ROOT / LOCK_REL
lock = read_json(lock_path)
require("generation_protocol" not in lock, "research lock already has generation_protocol")

lock["generation_protocol"] = {
    "status": "PASS",
    "path": PROTOCOL_REL,
    "sha256": protocol_sha,
    "window_id": "SVF-PRIMARY-800-V1",
    "window_state": "FROZEN_NOT_OPEN",
    "logical_attempts": 800,
    "maximum_transport_invocations_per_logical_slot": 3,
    "all_invocations_retained": True,
    "complete_http_responses_retried": False,
    "primary_generation_authorized": False,
    "repair_implementation_allowed": False,
}

current = lock["current_status"]
require(current["gate_0"] == "IN_PROGRESS", "Gate 0 status changed")
require(
    current.get("gate_0e_statistical_analysis_registration") == "PASS",
    "Gate 0E is not PASS",
)
current["gate_0f_generation_protocol"] = "PASS"
current["milestone"] = (
    "Gate 0F generation-window and transport-retry protocol complete; "
    "final Gate 0 manifest pending"
)
write_json(lock_path, lock)

status_path = ROOT / STATUS_REL
status_text = status_path.read_text(encoding="utf-8")
require("Gate 0E" in status_text, "CURRENT_STATUS lacks Gate 0E marker")

status_text, milestone_replacements = re.subn(
    r"(?m)^- Current milestone:.*$",
    "- Current milestone: Gate 0F — generation-window and "
    "transport-retry protocol complete",
    status_text,
    count=1,
)
require(milestone_replacements == 1, "cannot update CURRENT_STATUS milestone")

if "Gate 0F generation" not in status_text:
    marker = "- Gate 0E"
    lines = status_text.splitlines()
    insertion = None
    for index, line in enumerate(lines):
        if line.startswith(marker):
            insertion = index + 1
    require(insertion is not None, "cannot locate Gate 0E status line")
    lines.insert(
        insertion,
        "- Gate 0F generation-window and transport-retry protocol: PASS",
    )
    status_text = "\n".join(lines) + "\n"

status_text = status_text.replace(
    "Gate 0E statistical analysis and power registration complete",
    "Gate 0F generation-window and transport-retry protocol complete",
)
status_text = status_text.replace(
    "1. Freeze the exact generation-window and retry protocol.\n"
    "2. Create and verify the final Gate 0 manifest.",
    "1. Create and verify the final Gate 0 manifest.",
)
status_text = status_text.replace(
    "generation-window protocol and final Gate 0 manifest remain pending",
    "final Gate 0 manifest remains pending",
)
status_text = status_text.replace(
    "generation-window protocol, and the final Gate 0 manifest remain pending",
    "the final Gate 0 manifest remains pending",
)
status_path.write_text(status_text, encoding="utf-8")

readme_path = ROOT / README_REL
readme_text = readme_path.read_text(encoding="utf-8")
if "Gate 0F generation-window" not in readme_text:
    completed_marker = "- Gate 0E"
    readme_lines = readme_text.splitlines()
    insertion = None
    for index, line in enumerate(readme_lines):
        if line.startswith(completed_marker):
            insertion = index + 1
    require(insertion is not None, "cannot locate Gate 0E README line")
    readme_lines.insert(
        insertion,
        "- Gate 0F generation-window and transport-retry protocol",
    )
    readme_text = "\n".join(readme_lines) + "\n"

readme_text = readme_text.replace(
    "Statistical registration, generation-window\n"
    "protocol, and the final Gate 0 manifest remain pending.",
    "The final Gate 0 manifest remains pending.",
)
readme_text = readme_text.replace(
    "generation-window protocol, and the final Gate 0 manifest remain pending",
    "the final Gate 0 manifest remains pending",
)
readme_path.write_text(readme_text, encoding="utf-8")

for command in [
    ["python3", "scripts/verify_gate0c_proposal.py"],
    ["python3", "scripts/verify_gate0d_documentation.py"],
    ["python3", "scripts/verify_gate0d_live.py"],
    ["python3", "scripts/verify_gate0e_analysis.py"],
    ["python3", VERIFIER_REL],
    ["python3", "scripts/verify_gate0.py"],
    ["git", "diff", "--check"],
]:
    run(command)

print("GATE0F_GENERATION_PROTOCOL_PREPARATION=PASS")
print("EXECUTION_WINDOW=SVF-PRIMARY-800-V1")
print("EXECUTION_WINDOW_STATE=FROZEN_NOT_OPEN")
print("LOGICAL_ATTEMPTS=800")
print("TRANSPORT_RETRIES_AFTER_INITIAL=2")
print("TRANSPORT_BACKOFF_SECONDS=5,20")
print("COMPLETE_HTTP_RESPONSES_RETRIED=NO")
print("ALL_INVOCATIONS_RETAINED=YES")
print("GATE0_OVERALL=IN_PROGRESS")
print("GENERATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"PROTOCOL_SHA256={protocol_sha}")
print("STATUS=")
subprocess.run(["git", "status", "--short", "--branch"], cwd=ROOT, check=False)
