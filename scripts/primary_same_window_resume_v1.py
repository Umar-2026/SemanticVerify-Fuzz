#!/usr/bin/env python3
from pathlib import Path
import argparse
import ast
import hashlib
import inspect
import json
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import primary_operational_runner_v1 as pr
import primary_live_transport_v1 as lt

WINDOW_ID = "SVF-PRIMARY-800-V1"

PRIMARY_ROOT = (
    REPO
    / "evidence/primary_generation/"
      "SVF-PRIMARY-800-V1"
)

RESUME_CONTRACT_PATH = (
    REPO
    / "config/primary_same_window_resume_contract.v1.json"
)

RESUME_AUTH_SCHEMA_PATH = (
    REPO
    / "config/schemas/"
      "primary_resume_authorization_record.schema.json"
)

RESUME_AUTH_REL = (
    "evidence/generation_opening/"
    "primary_same_window_resume_authorization.v1.json"
)

RESUME_AUTH_PATH = (
    REPO
    / RESUME_AUTH_REL
)

DECISION_0013_PATH = (
    REPO
    / "documentation/decisions/"
      "0013-gemini-zero-output-usage-and-same-window-resume.md"
)

PAUSE_RESOLUTION_CONTRACT_PATH = (
    REPO
    / "config/primary_pause_resolution_contract.v1.json"
)

RESOLUTION_RECORD_PATH = (
    PRIMARY_ROOT
    / "ledger/resolutions/resolution-0001.json"
)

PAUSE_FREEZE_PACKAGE_PATH = (
    PRIMARY_ROOT
    / "freeze/pause-0001/"
      "pause_freeze_package.v1.SHA256SUMS"
)

PAUSE_FREEZE_MANIFEST_PATH = (
    PRIMARY_ROOT
    / "freeze/pause-0001/"
      "pause_freeze_manifest.v1.json"
)

WINDOW_OPEN_PATH = (
    PRIMARY_ROOT
    / "window/open.json"
)

WINDOW_CLOSE_PATH = (
    PRIMARY_ROOT
    / "window/close.json"
)

PAUSE_0001_PATH = (
    PRIMARY_ROOT
    / "ledger/pauses/pause-0001.json"
)

PAUSE_0002_PATH = (
    PRIMARY_ROOT
    / "ledger/pauses/pause-0002.json"
)

RESUME_MARKER_REL = (
    "ledger/resumes/resume-0001.json"
)

RESUME_MARKER_PATH = (
    PRIMARY_ROOT
    / RESUME_MARKER_REL
)


class ResumeOperationalError(RuntimeError):
    pass


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    return sha_bytes(Path(path).read_bytes())


def read_json(path):
    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )


def git(*args, binary=False):
    return subprocess.check_output(
        [
            "git",
            "-C",
            str(REPO),
            *args,
        ],
        text=not binary,
    )


def git_success(*args):
    cp = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            *args,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return cp.returncode == 0


def is_nonnegative_int(value):
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value >= 0
    )


def load_resume_contract():
    if not RESUME_CONTRACT_PATH.is_file():
        raise ResumeOperationalError(
            "resume contract missing"
        )

    contract = read_json(
        RESUME_CONTRACT_PATH
    )

    if (
        contract.get("contract_id")
        != "SVF-PRIMARY-SAME-WINDOW-RESUME-V1"
    ):
        raise ResumeOperationalError(
            "resume contract identity mismatch"
        )

    if (
        contract.get("status")
        != "FROZEN_IMPLEMENTATION_READY_RESUME_NOT_AUTHORIZED"
    ):
        raise ResumeOperationalError(
            "resume contract state mismatch"
        )

    expected_impl = (
        contract[
            "implementation"
        ][
            "sha256"
        ]
    )

    if (
        sha_file(Path(__file__).resolve())
        != expected_impl
    ):
        raise ResumeOperationalError(
            "resume implementation hash mismatch"
        )

    schema_sha = (
        contract[
            "resume_authorization_schema"
        ][
            "sha256"
        ]
    )

    if (
        not RESUME_AUTH_SCHEMA_PATH.is_file()
        or sha_file(
            RESUME_AUTH_SCHEMA_PATH
        )
        != schema_sha
    ):
        raise ResumeOperationalError(
            "resume authorization schema mismatch"
        )

    return contract


def load_inputs():
    locked = pr.load_inputs()
    resume_contract = load_resume_contract()

    bindings = (
        resume_contract[
            "frozen_bindings"
        ]
    )

    exact_paths = {
        "decision_0013":
            DECISION_0013_PATH,

        "pause_resolution_contract":
            PAUSE_RESOLUTION_CONTRACT_PATH,

        "resolution_record":
            RESOLUTION_RECORD_PATH,

        "frozen_runner":
            REPO
            / "scripts/"
              "primary_operational_runner_v1.py",

        "frozen_transport":
            REPO
            / "scripts/"
              "primary_live_transport_v1.py",

        "frozen_postprocessing":
            REPO
            / "config/"
              "primary_postprocessing_contract.v1.json",

        "pause_freeze_package":
            PAUSE_FREEZE_PACKAGE_PATH,

        "pause_freeze_manifest":
            PAUSE_FREEZE_MANIFEST_PATH,

        "window_open":
            WINDOW_OPEN_PATH,

        "pause_0001":
            PAUSE_0001_PATH,
    }

    for label, path in exact_paths.items():
        expected = bindings[
            label + "_sha256"
        ]

        if (
            not path.is_file()
            or sha_file(path) != expected
        ):
            raise ResumeOperationalError(
                "frozen binding mismatch: "
                + label
            )

    locked[
        "resume_contract"
    ] = resume_contract

    return locked


def verify_pause_freeze_package(
    resume_contract,
):
    expected_count = (
        resume_contract[
            "pause_freeze_integrity"
        ][
            "package_entry_count"
        ]
    )

    count = 0

    for line in (
        PAUSE_FREEZE_PACKAGE_PATH
        .read_text(
            encoding="utf-8"
        )
        .splitlines()
    ):
        expected_sha, rel = line.split(
            "  ",
            1,
        )

        path = REPO / rel

        if (
            not path.is_file()
            or sha_file(path)
            != expected_sha
        ):
            raise ResumeOperationalError(
                "pause freeze package mismatch: "
                + rel
            )

        count += 1

    if count != expected_count:
        raise ResumeOperationalError(
            "pause freeze package count mismatch"
        )

    return count


def estimate_cost_resume(
    model_label,
    usage,
    contract,
    classification,
    http_status,
):
    if (
        model_label == "Model B"
        and isinstance(http_status, int)
        and 200 <= http_status <= 299
        and isinstance(
            classification,
            dict,
        )
        and classification.get(
            "terminal_status"
        )
        == "REFUSAL"
        and isinstance(
            usage,
            dict,
        )
        and "candidatesTokenCount"
        not in usage
    ):
        prompt = usage.get(
            "promptTokenCount"
        )

        total = usage.get(
            "totalTokenCount"
        )

        thoughts_raw = usage.get(
            "thoughtsTokenCount",
            0,
        )

        cached_raw = usage.get(
            "cachedContentTokenCount",
            0,
        )

        tool_raw = usage.get(
            "toolUsePromptTokenCount",
            0,
        )

        valid = (
            is_nonnegative_int(prompt)
            and is_nonnegative_int(total)
            and is_nonnegative_int(
                thoughts_raw
            )
            and is_nonnegative_int(
                cached_raw
            )
            and is_nonnegative_int(
                tool_raw
            )
            and cached_raw == 0
            and tool_raw == 0
            and total
            == prompt
            + thoughts_raw
        )

        if valid:
            rates = (
                contract[
                    "cost_accounting"
                ][
                    "Gemini"
                ][
                    "rates"
                ]
            )

            estimate = (
                prompt
                * rates[
                    "input"
                ]
                + thoughts_raw
                * rates[
                    "output_including_thinking_tokens"
                ]
            ) / 1_000_000

            return {
                "status":
                    "PASS",

                "basis":
                    "DERIVED_ZERO_CANDIDATE_REFUSAL_TOKEN_BALANCE",

                "prompt_tokens":
                    prompt,

                "candidate_tokens":
                    0,

                "thoughts_tokens":
                    thoughts_raw,

                "cached_content_tokens":
                    0,

                "tool_use_prompt_tokens":
                    0,

                "estimate_usd":
                    estimate,
            }

    return lt.estimate_cost(
        model_label,
        usage,
        contract,
    )


def build_perform_transport_resume():
    source = inspect.getsource(
        pr.perform_transport
    )

    module = ast.parse(
        source
    )

    if (
        len(module.body) != 1
        or not isinstance(
            module.body[0],
            ast.FunctionDef,
        )
    ):
        raise ResumeOperationalError(
            "unexpected perform_transport source shape"
        )

    fn = module.body[0]
    fn.name = (
        "perform_transport_resume"
    )

    class Rewrite(ast.NodeTransformer):
        def __init__(self):
            self.count = 0

        def visit_Call(self, node):
            self.generic_visit(node)

            if (
                isinstance(
                    node.func,
                    ast.Attribute,
                )
                and isinstance(
                    node.func.value,
                    ast.Name,
                )
                and node.func.value.id
                == "lt"
                and node.func.attr
                == "estimate_cost"
            ):
                self.count += 1

                replacement = ast.Call(
                    func=ast.Name(
                        id=
                            "estimate_cost_resume",
                        ctx=ast.Load(),
                    ),
                    args=[
                        *node.args,
                        ast.Name(
                            id="classification",
                            ctx=ast.Load(),
                        ),
                        ast.Subscript(
                            value=ast.Name(
                                id="response",
                                ctx=ast.Load(),
                            ),
                            slice=ast.Constant(
                                value="http_status"
                            ),
                            ctx=ast.Load(),
                        ),
                    ],
                    keywords=[],
                )

                return ast.copy_location(
                    replacement,
                    node,
                )

            return node

    rewrite = Rewrite()
    module = rewrite.visit(
        module
    )

    ast.fix_missing_locations(
        module
    )

    if rewrite.count != 1:
        raise ResumeOperationalError(
            "expected exactly one cost-call rewrite"
        )

    namespace = dict(
        pr.perform_transport.__globals__
    )

    namespace[
        "estimate_cost_resume"
    ] = estimate_cost_resume

    compiled = compile(
        module,
        "<same-window-resume-transform>",
        "exec",
    )

    exec(
        compiled,
        namespace,
    )

    return (
        namespace[
            "perform_transport_resume"
        ],
        rewrite.count,
    )


(
    perform_transport_resume,
    TRANSFORM_REPLACEMENT_COUNT,
) = build_perform_transport_resume()


def reconstruct_service_error_state():
    records = []

    ledger_dir = (
        PRIMARY_ROOT
        / "ledger/invocations"
    )

    for path in ledger_dir.glob(
        "*.json"
    ):
        obj = read_json(path)

        slot_id = obj.get(
            "logical_slot_id"
        )

        if not isinstance(
            slot_id,
            str,
        ):
            continue

        try:
            slot = int(
                slot_id.rsplit(
                    "-",
                    1,
                )[1]
            )
        except Exception:
            continue

        if slot > 472:
            raise ResumeOperationalError(
                "unexpected invocation after slot 0472"
            )

        invocation = obj.get(
            "transport_invocation_number"
        )

        if not isinstance(
            invocation,
            int,
        ):
            raise ResumeOperationalError(
                "invalid invocation number"
            )

        records.append(
            (
                slot,
                invocation,
                obj,
            )
        )

    records.sort(
        key=lambda x: (
            x[0],
            x[1],
        )
    )

    state = {
        "Model A": 0,
        "Model B": 0,
    }

    model_map = {
        "deepseek-v4-flash":
            "Model A",

        "gemini-3.1-flash-lite":
            "Model B",
    }

    for _, _, obj in records:
        label = model_map.get(
            obj.get(
                "requested_model_id"
            )
        )

        if label is None:
            continue

        status = obj.get(
            "HTTP_status_or_transport_failure"
        )

        if not isinstance(
            status,
            int,
        ):
            continue

        if 500 <= status <= 599:
            state[label] += 1
        else:
            state[label] = 0

    return (
        state,
        len(records),
    )


def reconstruct_duplicate_state(
    locked,
):
    plan = (
        locked[
            "plan"
        ][
            "requests"
        ]
    )

    if len(plan) != 800:
        raise ResumeOperationalError(
            "request plan count mismatch"
        )

    dup = {}
    canonical_by_slot = {}

    extracted = 0
    canonical_count = 0
    duplicate_count = 0

    for number in range(
        1,
        473,
    ):
        slot_id = (
            WINDOW_ID
            + f"-SLOT-{number:04d}"
        )

        pp_path = (
            PRIMARY_ROOT
            / "slots"
            / slot_id
            / "postprocessing.json"
        )

        if not pp_path.is_file():
            raise ResumeOperationalError(
                "missing prior postprocessing: "
                + slot_id
            )

        pp = read_json(
            pp_path
        )

        if (
            pp.get(
                "logical_slot_id"
            )
            != slot_id
        ):
            raise ResumeOperationalError(
                "prior postprocessing id mismatch"
            )

        extraction = pp.get(
            "extraction_status"
        )

        source_rel = pp.get(
            "driver_source_path_or_null"
        )

        source_sha = pp.get(
            "driver_source_sha256"
        )

        source_len = pp.get(
            "driver_source_byte_length"
        )

        duplicate_of = pp.get(
            "duplicate_of_logical_slot_id_or_null"
        )

        if extraction != "EXTRACTED_VERBATIM":
            continue

        extracted += 1

        if not isinstance(
            source_rel,
            str,
        ):
            raise ResumeOperationalError(
                "extracted source path missing"
            )

        source_path = (
            PRIMARY_ROOT
            / source_rel
        )

        if not source_path.is_file():
            raise ResumeOperationalError(
                "prior driver source missing"
            )

        actual_bytes = (
            source_path.read_bytes()
        )

        actual_sha = (
            hashlib.sha256(
                actual_bytes
            ).hexdigest()
        )

        if (
            actual_sha != source_sha
            or len(actual_bytes)
            != source_len
        ):
            raise ResumeOperationalError(
                "prior driver source integrity mismatch"
            )

        rec = plan[
            number - 1
        ]

        key = (
            rec[
                "model_id"
            ],
            rec[
                "library"
            ],
            rec[
                "scenario_id"
            ],
        )

        if duplicate_of is None:
            item = {
                "logical_slot_id":
                    slot_id,

                "sha256":
                    actual_sha,

                "byte_length":
                    len(actual_bytes),

                "path":
                    source_path,
            }

            dup.setdefault(
                key,
                [],
            ).append(
                item
            )

            canonical_by_slot[
                slot_id
            ] = (
                key,
                item,
            )

            canonical_count += 1

        else:
            prior = canonical_by_slot.get(
                duplicate_of
            )

            if prior is None:
                raise ResumeOperationalError(
                    "duplicate target is not prior canonical"
                )

            prior_key, prior_item = prior

            if prior_key != key:
                raise ResumeOperationalError(
                    "duplicate group mismatch"
                )

            if (
                prior_item[
                    "sha256"
                ]
                != actual_sha
                or prior_item[
                    "byte_length"
                ]
                != len(actual_bytes)
                or prior_item[
                    "path"
                ].read_bytes()
                != actual_bytes
            ):
                raise ResumeOperationalError(
                    "duplicate byte identity mismatch"
                )

            duplicate_count += 1

    if (
        extracted != 402
        or canonical_count != 362
        or duplicate_count != 40
    ):
        raise ResumeOperationalError(
            "duplicate reconstruction count mismatch"
        )

    return {
        "duplicate_state":
            dup,

        "extracted_count":
            extracted,

        "canonical_count":
            canonical_count,

        "duplicate_count":
            duplicate_count,

        "group_count":
            len(dup),
    }


def validate_resume_boundary(
    locked,
):
    resume_contract = (
        locked[
            "resume_contract"
        ]
    )

    package_count = (
        verify_pause_freeze_package(
            resume_contract
        )
    )

    if not WINDOW_OPEN_PATH.is_file():
        raise ResumeOperationalError(
            "window open record missing"
        )

    if WINDOW_CLOSE_PATH.exists():
        raise ResumeOperationalError(
            "window already closed"
        )

    if not PAUSE_0001_PATH.is_file():
        raise ResumeOperationalError(
            "pause-0001 missing"
        )

    if PAUSE_0002_PATH.exists():
        raise ResumeOperationalError(
            "pause-0002 already exists"
        )

    if RESUME_MARKER_PATH.exists():
        raise ResumeOperationalError(
            "resume marker already exists"
        )

    pause = read_json(
        PAUSE_0001_PATH
    )

    if (
        pause.get(
            "pause_sequence"
        )
        != 1
        or pause.get(
            "reason"
        )
        != "INVALID_USAGE_METADATA"
        or pause.get(
            "triggering_logical_slot_id"
        )
        != (
            WINDOW_ID
            + "-SLOT-0472"
        )
        or pause.get(
            "calls_after_pause_before_resolution"
        )
        != 0
    ):
        raise ResumeOperationalError(
            "pause-0001 semantic mismatch"
        )

    slot_root = (
        PRIMARY_ROOT
        / "slots"
    )

    seen = []

    for path in slot_root.glob(
        "SVF-PRIMARY-800-V1-SLOT-*"
    ):
        if not path.is_dir():
            continue

        try:
            number = int(
                path.name.rsplit(
                    "-",
                    1,
                )[1]
            )
        except Exception:
            continue

        seen.append(
            number
        )

    seen.sort()

    if seen != list(
        range(
            1,
            473,
        )
    ):
        raise ResumeOperationalError(
            "prior slot prefix is not exactly 0001-0472"
        )

    plan = (
        locked[
            "plan"
        ][
            "requests"
        ]
    )

    if (
        len(plan) != 800
        or plan[471][
            "logical_slot_id"
        ]
        != (
            WINDOW_ID
            + "-SLOT-0472"
        )
        or plan[472][
            "logical_slot_id"
        ]
        != (
            WINDOW_ID
            + "-SLOT-0473"
        )
        or plan[799][
            "logical_slot_id"
        ]
        != (
            WINDOW_ID
            + "-SLOT-0800"
        )
    ):
        raise ResumeOperationalError(
            "resume plan boundary mismatch"
        )

    duplicate_info = (
        reconstruct_duplicate_state(
            locked
        )
    )

    (
        service_state,
        invocation_count,
    ) = (
        reconstruct_service_error_state()
    )

    if service_state != {
        "Model A": 0,
        "Model B": 0,
    }:
        raise ResumeOperationalError(
            "service-error state mismatch at pause boundary"
        )

    return {
        "package_entry_count":
            package_count,

        "terminal_slot_count":
            472,

        "first_resume_slot":
            473,

        "remaining_slot_count":
            328,

        "duplicate_state":
            duplicate_info[
                "duplicate_state"
            ],

        "duplicate_extracted_count":
            duplicate_info[
                "extracted_count"
            ],

        "duplicate_canonical_count":
            duplicate_info[
                "canonical_count"
            ],

        "duplicate_record_count":
            duplicate_info[
                "duplicate_count"
            ],

        "duplicate_group_count":
            duplicate_info[
                "group_count"
            ],

        "service_error_state":
            service_state,

        "prior_invocation_count":
            invocation_count,
    }


def _record_is_tracked_and_in_head(
    rel,
):
    if not git_success(
        "ls-files",
        "--error-unmatch",
        "--",
        rel,
    ):
        return False

    cp = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            "cat-file",
            "-e",
            "HEAD:" + rel,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return cp.returncode == 0


def verify_resume_authorization(
    locked,
):
    resume_contract = (
        locked[
            "resume_contract"
        ]
    )

    if not RESUME_AUTH_PATH.is_file():
        return {
            "authorized":
                False,

            "reason":
                "RESUME_AUTHORIZATION_RECORD_MISSING",
        }

    try:
        record = read_json(
            RESUME_AUTH_PATH
        )
    except Exception:
        return {
            "authorized":
                False,

            "reason":
                "RESUME_AUTHORIZATION_RECORD_INVALID_JSON",
        }

    try:
        import jsonschema

        schema = read_json(
            RESUME_AUTH_SCHEMA_PATH
        )

        validator = (
            jsonschema.Draft202012Validator(
                schema
            )
        )

        errors = sorted(
            validator.iter_errors(
                record
            ),
            key=lambda e:
                list(e.path),
        )

        if errors:
            return {
                "authorized":
                    False,

                "reason":
                    "RESUME_AUTHORIZATION_SCHEMA_INVALID",
            }

    except ImportError:
        return {
            "authorized":
                False,

            "reason":
                "JSONSCHEMA_UNAVAILABLE",
        }

    if not _record_is_tracked_and_in_head(
        RESUME_AUTH_REL
    ):
        return {
            "authorized":
                False,

            "reason":
                "RESUME_AUTHORIZATION_NOT_TRACKED_IN_HEAD",
        }

    worktree_status = git(
        "status",
        "--porcelain",
        "--untracked-files=all",
    )

    if worktree_status.strip():
        return {
            "authorized":
                False,

            "reason":
                "REPOSITORY_NOT_CLEAN_BEFORE_RESUME",
        }

    record_sha = sha_file(
        RESUME_AUTH_PATH
    )

    committed_record = git(
        "show",
        "HEAD:" + RESUME_AUTH_REL,
        binary=True,
    )

    if (
        sha_bytes(
            committed_record
        )
        != record_sha
    ):
        return {
            "authorized":
                False,

            "reason":
                "RESUME_AUTHORIZATION_WORKTREE_HEAD_MISMATCH",
        }

    if (
        record[
            "decision_0013"
        ][
            "sha256"
        ]
        != resume_contract[
            "frozen_bindings"
        ][
            "decision_0013_sha256"
        ]
    ):
        return {
            "authorized":
                False,

            "reason":
                "DECISION_0013_BINDING_MISMATCH",
        }

    if (
        record[
            "pause_resolution_contract"
        ][
            "sha256"
        ]
        != resume_contract[
            "frozen_bindings"
        ][
            "pause_resolution_contract_sha256"
        ]
    ):
        return {
            "authorized":
                False,

            "reason":
                "PAUSE_RESOLUTION_BINDING_MISMATCH",
        }

    current_resume_contract_sha = (
        sha_file(
            RESUME_CONTRACT_PATH
        )
    )

    if (
        record[
            "resume_contract"
        ][
            "sha256"
        ]
        != current_resume_contract_sha
    ):
        return {
            "authorized":
                False,

            "reason":
                "RESUME_CONTRACT_BINDING_MISMATCH",
        }

    implementation = (
        record[
            "implementation"
        ]
    )

    if (
        implementation[
            "sha256"
        ]
        != resume_contract[
            "implementation"
        ][
            "sha256"
        ]
    ):
        return {
            "authorized":
                False,

            "reason":
                "RESUME_IMPLEMENTATION_BINDING_MISMATCH",
        }

    freeze_commit = (
        implementation[
            "freeze_commit"
        ]
    )

    if not git_success(
        "merge-base",
        "--is-ancestor",
        freeze_commit,
        "HEAD",
    ):
        return {
            "authorized":
                False,

            "reason":
                "RESUME_IMPLEMENTATION_FREEZE_NOT_ANCESTOR",
        }

    try:
        frozen_script = git(
            "show",
            freeze_commit
            + ":scripts/"
              "primary_same_window_resume_v1.py",
            binary=True,
        )
    except subprocess.CalledProcessError:
        return {
            "authorized":
                False,

            "reason":
                "RESUME_IMPLEMENTATION_NOT_IN_FREEZE_COMMIT",
        }

    if (
        sha_bytes(
            frozen_script
        )
        != resume_contract[
            "implementation"
        ][
            "sha256"
        ]
    ):
        return {
            "authorized":
                False,

            "reason":
                "RESUME_IMPLEMENTATION_FREEZE_HASH_MISMATCH",
        }

    pause_freeze_commit = (
        resume_contract[
            "pause_freeze_integrity"
        ][
            "pause_freeze_commit"
        ]
    )

    if not git_success(
        "merge-base",
        "--is-ancestor",
        pause_freeze_commit,
        "HEAD",
    ):
        return {
            "authorized":
                False,

            "reason":
                "PAUSE_FREEZE_NOT_ANCESTOR",
        }

    provider = (
        record[
            "provider_requalification"
        ]
    )

    report_rel = provider[
        "report_path"
    ]

    report_path = (
        REPO
        / report_rel
    )

    if (
        not report_path.is_file()
        or sha_file(
            report_path
        )
        != provider[
            "report_sha256"
        ]
    ):
        return {
            "authorized":
                False,

            "reason":
                "PROVIDER_REQUALIFICATION_REPORT_MISMATCH",
        }

    if not _record_is_tracked_and_in_head(
        report_rel
    ):
        return {
            "authorized":
                False,

            "reason":
                "PROVIDER_REQUALIFICATION_NOT_COMMITTED",
        }

    report = read_json(
        report_path
    )

    if report.get(
        "status"
    ) != "PASS":
        return {
            "authorized":
                False,

            "reason":
                "PROVIDER_REQUALIFICATION_NOT_PASS",
        }

    if (
        provider[
            "deepseek"
        ][
            "status"
        ]
        != "PASS"
        or provider[
            "gemini"
        ][
            "status"
        ]
        != "PASS"
    ):
        return {
            "authorized":
                False,

            "reason":
                "PROVIDER_CAPABILITY_STATUS_NOT_PASS",
        }

    if WINDOW_CLOSE_PATH.exists():
        return {
            "authorized":
                False,

            "reason":
                "PRIMARY_WINDOW_ALREADY_CLOSED",
        }

    if not PAUSE_0001_PATH.is_file():
        return {
            "authorized":
                False,

            "reason":
                "PAUSE_0001_MISSING",
        }

    if PAUSE_0002_PATH.exists():
        return {
            "authorized":
                False,

            "reason":
                "PAUSE_0002_ALREADY_EXISTS",
        }

    if RESUME_MARKER_PATH.exists():
        return {
            "authorized":
                False,

            "reason":
                "RESUME_MARKER_ALREADY_EXISTS",
        }

    return {
        "authorized":
            True,

        "reason":
            "PASS",

        "authorization_record_path":
            RESUME_AUTH_REL,

        "authorization_record_sha256":
            record_sha,

        "implementation_freeze_commit":
            freeze_commit,
    }


def write_resume_marker(
    gate,
    execution_head,
):
    lt.create_new_json(
        RESUME_MARKER_PATH,
        {
            "window_id":
                WINDOW_ID,

            "resume_sequence":
                1,

            "resumed_at_utc":
                pr.now(),

            "resolved_pause_sequence":
                1,

            "first_logical_slot_id":
                (
                    WINDOW_ID
                    + "-SLOT-0473"
                ),

            "authorization_record_path":
                gate[
                    "authorization_record_path"
                ],

            "authorization_record_sha256":
                gate[
                    "authorization_record_sha256"
                ],

            "implementation_freeze_commit":
                gate[
                    "implementation_freeze_commit"
                ],

            "execution_head_commit":
                execution_head,
        },
    )


def execute_resume(confirm):
    locked = load_inputs()

    gate = verify_resume_authorization(
        locked
    )

    if not gate.get(
        "authorized"
    ):
        print(
            "RESUME_EXECUTION_REFUSED="
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
            "RESUME_EXECUTION_REFUSED="
            "WINDOW_CONFIRMATION_MISMATCH"
        )
        print(
            "API_SECRET_ENVIRONMENT_VALUES_READ=NO"
        )
        print(
            "LIVE_PROVIDER_CALLS=NO"
        )
        return 65

    boundary = validate_resume_boundary(
        locked
    )

    with tempfile.TemporaryDirectory(
        prefix="svf-primary-resume-compile-"
    ) as td:
        wd = Path(td)

        compiler_ctx = (
            pr.compiler_preflight(
                locked,
                wd,
            )
        )

        # Secrets are intentionally read only after:
        # 1) committed resume authorization PASS,
        # 2) window confirmation PASS,
        # 3) paused-state integrity PASS,
        # 4) compiler/library preflight PASS.
        secrets = pr.read_secrets(
            locked
        )

        execution_head = git(
            "rev-parse",
            "HEAD",
        ).strip()

        proxy_plans = {
            label:
                pr.select_https_proxy(
                    cfg[
                        "endpoint"
                    ]
                )

            for label, cfg
            in locked[
                "contract"
            ][
                "providers"
            ].items()
        }

        execution_context = {
            "authorization_record_path":
                gate[
                    "authorization_record_path"
                ],

            "authorization_record_sha256":
                gate[
                    "authorization_record_sha256"
                ],

            "execution_head_commit":
                execution_head,
        }

        duplicate_state = (
            boundary[
                "duplicate_state"
            ]
        )

        service_error_state = dict(
            boundary[
                "service_error_state"
            ]
        )

        terminal_count = 472

        write_resume_marker(
            gate,
            execution_head,
        )

        for rec in (
            locked[
                "plan"
            ][
                "requests"
            ][472:]
        ):
            transport_result = (
                perform_transport_resume(
                    locked,
                    rec,
                    secrets[
                        rec[
                            "model_label"
                        ]
                    ],
                    PRIMARY_ROOT,
                    proxy_plans[
                        rec[
                            "model_label"
                        ]
                    ],
                    execution_context=
                        execution_context,
                    service_error_state=
                        service_error_state,
                )
            )

            post_result = pr.postprocess(
                locked,
                rec,
                transport_result,
                PRIMARY_ROOT,
                duplicate_state,
                wd,
                compiler_ctx,
            )

            terminal_count += 1

            print(
                "PRIMARY_RESUME_SLOT|"
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
                pr.write_pause(
                    PRIMARY_ROOT,
                    rec[
                        "logical_slot_id"
                    ],
                    transport_result.get(
                        "pause_reason"
                    )
                    or "UNSPECIFIED_PAUSE",
                    seq=2,
                )

                print(
                    "PRIMARY_WINDOW_PAUSED=YES"
                )
                print(
                    "PAUSE_SEQUENCE=2"
                )
                print(
                    "CALLS_AFTER_PAUSE=0"
                )

                return 75

        if terminal_count != 800:
            raise ResumeOperationalError(
                "terminal count != 800"
            )

        pr.write_close(
            PRIMARY_ROOT,
            terminal_count,
        )

    print(
        "PRIMARY_WINDOW_COMPLETE=YES"
    )
    print(
        "TERMINAL_RECORD_COUNT=800"
    )
    print(
        "SAME_WINDOW_RESUME_COMPLETE=YES"
    )

    return 0


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--execute-resume",
        action="store_true",
    )

    parser.add_argument(
        "--confirm-window-id",
    )

    args = parser.parse_args()

    if args.execute_resume:
        return execute_resume(
            args.confirm_window_id
        )

    locked = load_inputs()

    gate = verify_resume_authorization(
        locked
    )

    print(
        "SAME_WINDOW_RESUME_IMPLEMENTATION=READY"
    )

    print(
        "CURRENT_RESUME_AUTHORIZED="
        + (
            "YES"
            if gate.get(
                "authorized"
            )
            else "NO"
        )
    )

    print(
        "CURRENT_RESUME_GATE_REASON="
        + gate.get(
            "reason",
            "UNKNOWN",
        )
    )

    print(
        "LIVE_PROVIDER_CALLS=NO"
    )

    print(
        "API_SECRET_ENVIRONMENT_VALUES_READ=NO"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
