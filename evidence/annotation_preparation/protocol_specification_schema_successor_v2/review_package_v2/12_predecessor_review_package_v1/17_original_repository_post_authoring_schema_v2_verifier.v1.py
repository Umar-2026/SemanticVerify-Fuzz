#!/usr/bin/env python3

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def csha(x):
    return hashlib.sha256(
        json.dumps(
            x,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()

here = Path(__file__).resolve().parent
repo = here

while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

v1p = repo / "config/schemas/protocol_specification.schema.json"
v2p = repo / "config/schemas/protocol_specification.v2.schema.json"

v4p = (
    repo /
    "config/annotation/"
    "curl_canonical_representation_mapping_contract.v4.json"
)

reviewp = (
    repo /
    "evidence/annotation_preparation/"
    "curl_canonical_representation_mapping_contract_v4/"
    "completed_human_review_v1/"
    "02_completed_v4_human_review_record.v1.json"
)

designp = here / "04_schema_v2_successor_design_record.v1.json"

curlp = repo / "config/protocol_specifications/curl.json"

V1_SHA = "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
V2_SHA = "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
V4_SHA = "9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070"
REVIEW_SHA = "292a4a569139d4b09dc341579ab25bfdba0db60e44d7b42da36cf2ab0740e53d"
REP_SHA = "dd645ad929e40bcfa2af2353817d55ad76596f464991f2417c4ac1b57c0be408"
LOSS_SHA = "c869079bfbd395b479e2dd8f2f1bcc31aabeababe0e24fc1542c6d35d210602e"

if sha(v1p) != V1_SHA:
    fail("V1_SHA")

if sha(v2p) != V2_SHA:
    fail("V2_SHA")

if v2p.stat().st_size != 43030:
    fail("V2_SIZE")

if sha(v4p) != V4_SHA:
    fail("V4_SHA")

if sha(reviewp) != REVIEW_SHA:
    fail("REVIEW_SHA")

v1 = json.loads(v1p.read_text(encoding="utf-8"))
v2 = json.loads(v2p.read_text(encoding="utf-8"))
v4 = json.loads(v4p.read_text(encoding="utf-8"))
design = json.loads(designp.read_text(encoding="utf-8"))

rep = v4["approved_v4_representation_policy_binding"]["exact_value"]
loss = v4["formal_insufficiency_argument"]["required_losslessness_contract"]

if len(rep) != 10 or csha(rep) != REP_SHA:
    fail("EXACT_V4_REPRESENTATION_POLICY")

if len(loss) != 17 or csha(loss) != LOSS_SHA:
    fail("EXACT_V4_LOSSLESSNESS")

if design["schema_v2_candidate"]["sha256"] != V2_SHA:
    fail("DESIGN_V2_SHA")

if design["schema_v2_candidate"]["size_bytes"] != 43030:
    fail("DESIGN_V2_SIZE")

if design["retry_context"][
    "previous_ephemeral_candidate_sha256"
] != V2_SHA:
    fail("RETRY_PREVIOUS_CANDIDATE_SHA")

if design["retry_context"][
    "current_candidate_byte_identical_to_previous_ephemeral_candidate"
] is not True:
    fail("RETRY_BYTE_IDENTITY")

if design["retry_context"][
    "pre_authoring_authorization_verifier_rerun"
] is not False:
    fail("PREAUTH_RERUN")

basis = design["approved_v4_basis"]

if basis["representation_policy_path"] != \
   "$.approved_v4_representation_policy_binding.exact_value":
    fail("REP_PATH")

if basis["representation_policy_field_count"] != 10:
    fail("REP_COUNT")

if basis["representation_policy_canonical_sha256"] != REP_SHA:
    fail("REP_SHA_BINDING")

if basis["representation_policy_snapshot"] != rep:
    fail("REP_SNAPSHOT")

if basis["losslessness_contract_path"] != \
   "$.formal_insufficiency_argument.required_losslessness_contract":
    fail("LOSS_PATH")

if basis["losslessness_requirement_count"] != 17:
    fail("LOSS_COUNT")

if basis["losslessness_contract_canonical_sha256"] != LOSS_SHA:
    fail("LOSS_SHA_BINDING")

if basis["losslessness_contract_snapshot"] != loss:
    fail("LOSS_SNAPSHOT")

if v2.get("additionalProperties") is not False:
    fail("V2_TOP_LEVEL_NOT_CLOSED")

expected_required = {
    "author",
    "content_sha256",
    "creation_date",
    "freeze_date",
    "library",
    "library_revision",
    "reviewer",
    "schema_version",
    "specification_id",
    "provenance",
    "resource_model",
    "events",
    "semantic_policy",
    "semantic_rules",
    "exit_obligations",
    "semantic_accounting",
}

if set(v2["required"]) != expected_required:
    fail("V2_REQUIRED_FIELDS")

if v2["properties"]["schema_version"].get("const") != "2.0.0":
    fail("V2_VERSION")

for key in (
    "author",
    "content_sha256",
    "creation_date",
    "freeze_date",
    "library",
    "library_revision",
    "reviewer",
    "specification_id",
    "provenance",
):
    if v2["properties"][key] != v1["properties"][key]:
        fail("V1_METADATA_CARRIER_CHANGED|" + key)

def walk(x, path="$"):
    if isinstance(x, dict):
        yield path, x
        for k, v in x.items():
            yield from walk(v, path + "." + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from walk(v, f"{path}[{i}]")

for path, obj in walk(v2):
    if obj.get("type") == "object":
        if obj.get("additionalProperties") is not False:
            fail("OPEN_NORMATIVE_OBJECT|" + path)

prohibited_names = {
    "payload",
    "opaque_payload",
    "metadata_blob",
    "semantic_blob",
    "escape_payload",
}

for path, obj in walk(v2):
    props = obj.get("properties")
    if isinstance(props, dict):
        overlap = prohibited_names & set(props)
        if overlap:
            fail(
                "OPAQUE_ESCAPE_PROPERTY|"
                + path
                + "|"
                + ",".join(sorted(overlap))
            )

event_enum = (
    v2["properties"]["events"]["items"]
    ["properties"]["event_kind"]["enum"]
)

if set(event_enum) != {
    "API_CALL",
    "BRANCH",
    "FUNCTION_EXIT",
}:
    fail("EVENT_KIND_BOUNDARY")

policy = v2["properties"]["semantic_policy"]

if policy["properties"]["verdict_vocabulary"]["const"] != [
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN",
]:
    fail("VERDICT_VOCABULARY")

reason = policy["properties"]["reasoning_model"]["properties"]

expected_reason = {
    "path_sensitivity":
        "PATH_SENSITIVE",

    "state_domain":
        "SET_OF_FEASIBLE_STATES",

    "join_operator":
        "UNION_OF_FEASIBLE_STATES",

    "infeasible_path_handling":
        "EXCLUDE",

    "unknown_handling":
        "FIRST_CLASS_PRESERVE",

    "ownership_sensitivity":
        "RESOURCE_OWNERSHIP_SENSITIVE",

    "return_sensitivity":
        "RETURN_PREDICATE_SENSITIVE",

    "membership_sensitivity":
        "RELATION_MEMBERSHIP_SENSITIVE",
}

for key, value in expected_reason.items():
    if reason[key].get("const") != value:
        fail("REASONING_POLICY|" + key)

agg = policy["properties"]["verdict_aggregation"]["properties"]

if agg[
    "unknown_must_not_collapse_to_valid"
].get("const") is not True:
    fail("UNKNOWN_COLLAPSE")

rm = v2["properties"]["resource_model"]["properties"]

if "resource_types" not in rm:
    fail("RESOURCE_TYPE_CARRIER")

if "relation_types" not in rm:
    fail("RELATION_TYPE_CARRIER")

rule_props = (
    v2["properties"]["semantic_rules"]
    ["items"]["properties"]
)

for key in (
    "resource_bindings",
    "relation_bindings",
    "preconditions",
    "effects",
    "verdict_if_violated",
    "source_evidence",
):
    if key not in rule_props:
        fail("STRUCTURED_RULE_CARRIER|" + key)

pre_props = rule_props["preconditions"]["properties"]

for key in (
    "resource_state_requirements",
    "relation_state_requirements",
    "return_conditions",
    "path_conditions",
):
    if key not in pre_props:
        fail("PRECONDITION_CARRIER|" + key)

effect_props = rule_props["effects"]["properties"]

for key in (
    "resource_state_updates",
    "relation_updates",
    "ownership_updates",
):
    if key not in effect_props:
        fail("EFFECT_CARRIER|" + key)

acct = v2["properties"]["semantic_accounting"]["properties"]

for key in (
    "inventory",
    "forward_complete",
    "reverse_complete",
    "forward_accounting",
    "reverse_accounting",
):
    if key not in acct:
        fail("ACCOUNTING_CARRIER|" + key)

if acct["forward_complete"].get("const") is not True:
    fail("FORWARD_COMPLETE")

if acct["reverse_complete"].get("const") is not True:
    fail("REVERSE_COMPLETE")

Draft202012Validator.check_schema(v2)
validator = Draft202012Validator(v2)

sample = {
    "author": "Schema-V2-Self-Test",
    "content_sha256": "0" * 64,
    "creation_date": "2026-08-20",
    "freeze_date": "2026-08-20",
    "library": "schema-v2-synthetic-self-test",
    "library_revision": "0" * 40,
    "reviewer": "Schema-V2-Self-Test",
    "schema_version": "2.0.0",
    "specification_id": "schema-v2.synthetic-self-test",
    "provenance": [
        {
            "content_sha256": "0" * 64,
            "evidence_id": "EV-SELF-001",
            "path_or_url": "/synthetic/schema-v2-self-test",
            "quoted_or_paraphrased_rationale":
                "Synthetic schema-expressivity validation witness only.",
            "retrieval_date": "2026-08-20",
            "source_type": "PUBLIC_HEADER",
        }
    ],
    "resource_model": {
        "resource_types": [
            {
                "resource_type_id": "RESOURCE_A",
                "resource_kind": "synthetic.resource.a",
                "identity_model": "SYMBOLIC_HANDLE",
                "states": ["ABSENT", "LIVE", "RELEASED"],
                "initial_states": ["ABSENT"],
                "permitted_exit_states": ["ABSENT", "RELEASED"],
                "ownership_tracking": "TRACKED",
            },
            {
                "resource_type_id": "RESOURCE_B",
                "resource_kind": "synthetic.resource.b",
                "identity_model": "SYMBOLIC_HANDLE",
                "states": ["ABSENT", "LIVE", "RELEASED"],
                "initial_states": ["ABSENT"],
                "permitted_exit_states": ["ABSENT", "RELEASED"],
                "ownership_tracking": "TRACKED",
            },
        ],
        "relation_types": [
            {
                "relation_type_id": "REL_A_IN_B",
                "relation_kind": "MEMBERSHIP",
                "source_resource_type_id": "RESOURCE_A",
                "target_resource_type_id": "RESOURCE_B",
                "stateful": True,
                "states": ["DETACHED", "ATTACHED"],
                "initial_states": ["DETACHED"],
                "cardinality": {
                    "source_min": 0,
                    "source_max": 1,
                    "target_min": 0,
                    "target_max": None,
                },
            }
        ],
    },
    "events": [
        {
            "event_id": "E_ATTACH",
            "event_kind": "API_CALL",
            "symbol_or_condition": "synthetic_attach",
            "affected_resource_type_ids": [
                "RESOURCE_A",
                "RESOURCE_B",
            ],
            "affected_relation_type_ids": [
                "REL_A_IN_B",
            ],
            "return_classes": [
                {
                    "return_class_id": "SUCCESS",
                    "operator": "EQ",
                    "operands": [0],
                },
                {
                    "return_class_id": "FAILURE",
                    "operator": "NE",
                    "operands": [0],
                },
            ],
        },
        {
            "event_id": "E_EXIT",
            "event_kind": "FUNCTION_EXIT",
            "symbol_or_condition": "enclosing function exit",
            "affected_resource_type_ids": [
                "RESOURCE_A",
                "RESOURCE_B",
            ],
            "affected_relation_type_ids": [
                "REL_A_IN_B",
            ],
            "return_classes": [],
        },
    ],
    "semantic_policy": {
        "verdict_vocabulary": [
            "VALID",
            "VIOLATION-MUST",
            "VIOLATION-MAY",
            "UNKNOWN",
        ],
        "reasoning_model": {
            "path_sensitivity": "PATH_SENSITIVE",
            "state_domain": "SET_OF_FEASIBLE_STATES",
            "join_operator": "UNION_OF_FEASIBLE_STATES",
            "infeasible_path_handling": "EXCLUDE",
            "unknown_handling": "FIRST_CLASS_PRESERVE",
            "ownership_sensitivity": "RESOURCE_OWNERSHIP_SENSITIVE",
            "return_sensitivity": "RETURN_PREDICATE_SENSITIVE",
            "membership_sensitivity": "RELATION_MEMBERSHIP_SENSITIVE",
        },
        "verdict_aggregation": {
            "violation_must_when":
                "ALL_FEASIBLE_PATHS_VIOLATE",
            "violation_may_when":
                "SOME_BUT_NOT_ALL_FEASIBLE_PATHS_VIOLATE",
            "valid_when":
                "NO_FEASIBLE_PATH_VIOLATES_AND_EVIDENCE_SUFFICIENT",
            "unknown_when":
                "EVIDENCE_OR_MODEL_INSUFFICIENT_FOR_SAFE_CLASSIFICATION",
            "unknown_must_not_collapse_to_valid":
                True,
        },
    },
    "semantic_rules": [
        {
            "rule_id": "SELF-R01",
            "semantic_container": "synthetic.membership",
            "rule_kind": "CROSS_RESOURCE",
            "trigger_event_ids": ["E_ATTACH"],
            "resource_bindings": [
                {
                    "binding_id": "A",
                    "resource_type_id": "RESOURCE_A",
                    "role": "MEMBER",
                    "same_identity_as": [],
                    "distinct_identity_from": ["B"],
                },
                {
                    "binding_id": "B",
                    "resource_type_id": "RESOURCE_B",
                    "role": "CONTAINER",
                    "same_identity_as": [],
                    "distinct_identity_from": ["A"],
                },
            ],
            "relation_bindings": [
                {
                    "binding_id": "AB",
                    "relation_type_id": "REL_A_IN_B",
                    "source_resource_binding_id": "A",
                    "target_resource_binding_id": "B",
                }
            ],
            "preconditions": {
                "resource_state_requirements": [
                    {
                        "resource_binding_id": "A",
                        "allowed_states": ["LIVE"],
                    },
                    {
                        "resource_binding_id": "B",
                        "allowed_states": ["LIVE"],
                    },
                ],
                "relation_state_requirements": [
                    {
                        "relation_binding_id": "AB",
                        "presence": "ABSENT",
                        "allowed_states": ["DETACHED"],
                    }
                ],
                "return_conditions": [
                    {
                        "event_id": "E_ATTACH",
                        "allowed_return_class_ids": ["SUCCESS"],
                    }
                ],
                "path_conditions": [
                    {
                        "condition_id": "P_ATTACH_REACHED",
                        "condition_kind": "EVENT_REACHED",
                        "referenced_event_id": "E_ATTACH",
                        "polarity": True,
                    }
                ],
            },
            "effects": {
                "resource_state_updates": [],
                "relation_updates": [
                    {
                        "relation_binding_id": "AB",
                        "operation": "ADD",
                        "to_states": ["ATTACHED"],
                    }
                ],
                "ownership_updates": [
                    {
                        "resource_binding_id": "A",
                        "effect": "RETAIN",
                        "transfer_target_resource_binding_id": None,
                    }
                ],
            },
            "verdict_if_violated": "VIOLATION-MAY",
            "source_evidence": ["EV-SELF-001"],
        }
    ],
    "exit_obligations": [
        {
            "exit_obligation_id": "SELF-X01",
            "semantic_container": "synthetic.exit",
            "resource_bindings": [
                {
                    "binding_id": "A",
                    "resource_type_id": "RESOURCE_A",
                    "role": "SUBJECT",
                    "same_identity_as": [],
                    "distinct_identity_from": [],
                }
            ],
            "relation_bindings": [],
            "preconditions": {
                "resource_state_requirements": [
                    {
                        "resource_binding_id": "A",
                        "allowed_states": ["LIVE"],
                    }
                ],
                "relation_state_requirements": [],
                "return_conditions": [],
                "path_conditions": [
                    {
                        "condition_id": "P_EXIT",
                        "condition_kind": "FUNCTION_EXIT_REACHED",
                        "referenced_event_id": "E_EXIT",
                        "polarity": True,
                    }
                ],
            },
            "required_resource_exit_states": [
                {
                    "resource_binding_id": "A",
                    "allowed_states": ["RELEASED"],
                }
            ],
            "required_relation_exit_states": [],
            "verdict_if_violated": "VIOLATION-MUST",
            "source_evidence": ["EV-SELF-001"],
        }
    ],
    "semantic_accounting": {
        "inventory": {
            "semantic_container_count": 2,
            "rule_count": 1,
            "exit_obligation_count": 1,
            "representation_policy_field_count": 10,
            "losslessness_requirement_count": 17,
        },
        "forward_complete": True,
        "reverse_complete": True,
        "forward_accounting": [
            {
                "source_unit_id": "SELF-R01",
                "source_container": "synthetic.membership",
                "source_unit_kind": "RULE",
                "schema_carriers": [
                    "/semantic_rules/0",
                    "/resource_model/relation_types/0",
                ],
            }
        ],
        "reverse_accounting": [
            {
                "schema_carrier": "/semantic_rules/0",
                "source_unit_ids": ["SELF-R01"],
            }
        ],
    },
}

errors = sorted(
    validator.iter_errors(sample),
    key=lambda e: list(e.path),
)

if errors:
    for e in errors[:10]:
        print(
            "SELF_TEST_ERROR|"
            + "/".join(map(str, e.path))
            + "|"
            + e.message
        )
    fail("SYNTHETIC_MULTI_RESOURCE_WITNESS")

bad = copy.deepcopy(sample)
bad["opaque_payload"] = {"hidden": "escape"}

if not list(validator.iter_errors(bad)):
    fail("OPAQUE_PAYLOAD_NOT_REJECTED")

bad2 = copy.deepcopy(sample)
bad2["events"][0]["event_kind"] = "SYNTHETIC"

if not list(validator.iter_errors(bad2)):
    fail("SYNTHETIC_EVENT_NOT_REJECTED")

claim = design["author_level_claim"]

for key in (
    "curl_v4_positive_mapping_defined",
    "curl_v4_positive_mapping_approved",
    "schema_v2_activated",
    "decision_0019_superseded",
    "curl_json_materialization_authorized",
):
    if claim[key] is not False:
        fail("UNAUTHORIZED_AUTHOR_CLAIM|" + key)

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("SCHEMA_V2_EXACT_SHA256=PASS")
print("SCHEMA_V2_EXACT_SIZE=PASS")
print("SAFE_ABORT_CANDIDATE_BYTE_REPRODUCTION=PASS")
print("EXACT_V4_REPRESENTATION_POLICY_BINDING=PASS")
print("EXACT_V4_LOSSLESSNESS_BINDING=PASS")
print("SCHEMA_V2_JSON_SCHEMA_META_VALIDATION=PASS")
print("SCHEMA_V2_TOP_LEVEL_CLOSED=YES")
print("SCHEMA_V2_NORMATIVE_OBJECTS_CLOSED=YES")
print("SCHEMA_V2_OPAQUE_ESCAPE_CARRIERS_ABSENT=YES")
print("SCHEMA_V2_SYNTHETIC_EVENT_KIND_FORBIDDEN=YES")
print("SCHEMA_V2_MULTI_RESOURCE_IDENTITY_CARRIER=PASS")
print("SCHEMA_V2_TYPED_RELATION_MEMBERSHIP_CARRIER=PASS")
print("SCHEMA_V2_FOUR_VERDICT_VOCABULARY=PASS")
print("SCHEMA_V2_FIRST_CLASS_UNKNOWN_POLICY=PASS")
print("SCHEMA_V2_PATH_SENSITIVE_POLICY=PASS")
print("SCHEMA_V2_SET_VALUED_STATE_POLICY=PASS")
print("SCHEMA_V2_FEASIBLE_STATE_JOIN_POLICY=PASS")
print("SCHEMA_V2_OWNERSHIP_SENSITIVE_CARRIER=PASS")
print("SCHEMA_V2_RETURN_SENSITIVE_CARRIER=PASS")
print("SCHEMA_V2_STRUCTURED_RULE_CARRIER=PASS")
print("SCHEMA_V2_FORWARD_ACCOUNTING_CARRIER=PASS")
print("SCHEMA_V2_REVERSE_ACCOUNTING_CARRIER=PASS")
print("SCHEMA_V2_SYNTHETIC_MULTI_RESOURCE_WITNESS=PASS")
print("SCHEMA_V2_OPAQUE_PAYLOAD_NEGATIVE_TEST=PASS")
print("SCHEMA_V2_SYNTHETIC_EVENT_NEGATIVE_TEST=PASS")
print("V4_REPRESENTATION_POLICY_10_FIELD_BINDING=PASS")
print("V4_LOSSLESSNESS_17_FIELD_BINDING=PASS")
print("FROZEN_SCHEMA_V1_IMMUTABLE=YES")
print("SCHEMA_V2_ACTIVATED=NO")
print("DECISION_0019_SUPERSEDED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("SCHEMA_V2_SUCCESSOR_AUTHOR_CHECKPOINT_VERIFICATION=PASS")
