# Decision 0051 — Protocol-Specification Schema V2 Successor Author Checkpoint

## Candidate

Path:

`config/schemas/protocol_specification.v2.schema.json`

Protocol-specification schema version:

`2.0.0`

SHA-256:

`c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956`

Size:

`43030` bytes

The candidate is byte-identical to the ephemeral candidate created during the
previous safely aborted attempt. That attempt did not commit any artifact and
failed only because the script searched an incorrect V4 representation-policy
path.

The corrected binding paths are:

`$.approved_v4_representation_policy_binding.exact_value`

and

`$.formal_insufficiency_argument.required_losslessness_contract`

Their canonical SHA-256 values are:

`dd645ad929e40bcfa2af2353817d55ad76596f464991f2417c4ac1b57c0be408`

and

`c869079bfbd395b479e2dd8f2f1bcc31aabeababe0e24fc1542c6d35d210602e`.

## Status

`AUTHOR_CHECKPOINT_INDEPENDENT_HUMAN_REVIEW_REQUIRED`

Schema V2 is a candidate only and is **not activated**.

Frozen Schema V1 remains unchanged.

## Structural design

Schema V2 provides first-class generic carriers for:

- multiple resource identities and resource types;
- typed resource relations and membership;
- VALID / VIOLATION-MUST / VIOLATION-MAY / UNKNOWN;
- first-class UNKNOWN preservation;
- feasible-state joins;
- path-sensitive and set-valued reasoning;
- ownership-sensitive effects;
- return-sensitive conditions;
- structured rule payloads;
- structured exit obligations;
- forward semantic accounting;
- reverse semantic accounting.

Normative objects are closed.

No opaque payload escape carrier exists.

Event kinds remain only:

`API_CALL`, `BRANCH`, `FUNCTION_EXIT`.

## Exact approved V4 bindings

Representation-policy source:

`$.approved_v4_representation_policy_binding.exact_value`

Field count:

`10`

Canonical SHA-256:

`dd645ad929e40bcfa2af2353817d55ad76596f464991f2417c4ac1b57c0be408`

Losslessness source:

`$.formal_insufficiency_argument.required_losslessness_contract`

Requirement count:

`17`

Canonical SHA-256:

`c869079bfbd395b479e2dd8f2f1bcc31aabeababe0e24fc1542c6d35d210602e`

These bindings do not constitute a positive curl-V4-to-V2 mapping.

## V1 compatibility

Existing zlib and libpcap canonical specifications remain unchanged under
Schema V1 version `1.0.0`.

No migration or rewrite is authorized.

## Governance boundaries

Decision 0019 is not superseded.

The canonical curl path remains:

`config/protocol_specifications/curl.json`

The existing content-hash contract is unchanged.

Schema V2 cannot yet be used for canonical curl materialization.

## Non-authorization

This checkpoint does not authorize:

- Schema V2 activation;
- Decision-0019 amendment or supersession;
- canonical-path-map modification;
- hash-contract modification;
- positive curl-V4-to-V2 mapping;
- curl.json;
- analyzer implementation or execution;
- baseline execution;
- controlled LLM review;
- repair.

## Immutability

Exact Schema V2 becomes immutable at this author checkpoint.

Any correction requires a separately authorized successor.

## Next boundary

`CREATE_INDEPENDENT_REVIEW_PACKAGE_FOR_PROTOCOL_SPECIFICATION_SCHEMA_V2`
