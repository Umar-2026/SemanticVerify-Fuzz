# Decision 0050 — Authorize Protocol-Specification Schema V2 Successor Authoring

## Basis

Exact curl Mapping Contract V4 has completed independent human review.

Result:

`10 PASS / 0 REVISION_REQUIRED / 0 FAIL`

Overall:

`APPROVE_V4_RR10_CORRECTED_SCHEMA_INSUFFICIENCY_PROOF`

The scoped conclusion is independently approved:

`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`

## Frozen V1 schema

Path:

`config/schemas/protocol_specification.schema.json`

SHA-256:

`7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34`

Protocol-specification schema version:

`1.0.0`

V1 remains immutable and must not be edited, replaced, or deleted.

Existing frozen zlib and libpcap specifications remain governed by V1.

## Authorized V2 candidate

Reserved candidate path:

`config/schemas/protocol_specification.v2.schema.json`

Target protocol-specification schema version:

`2.0.0`

This decision authorizes **authoring only**.

It does not activate or approve V2.

## Required representational scope

The V2 candidate must provide first-class structural representation sufficient
for the independently reviewed curl V4 requirements, including:

- multi-resource identity;
- typed resource relations and EASY/MULTI membership;
- VALID / VIOLATION-MUST / VIOLATION-MAY / UNKNOWN;
- first-class UNKNOWN semantics;
- feasible-state join policy;
- path-sensitive and set-valued-state reasoning;
- ownership-sensitive semantics;
- return-sensitive semantics;
- structured rule payloads;
- forward and reverse semantic accounting;
- structured provenance;
- freeze/content-hash compatibility.

It must structurally account for the complete approved curl V4 boundary:

- 10 semantic containers;
- 64 rules;
- 3 exit obligations;
- all four structural-obstruction classes;
- complete representation policy;
- complete losslessness contract.

Opaque free-form payload packing and synthetic semantic protocol events are not
acceptable escape mechanisms.

## Decision 0019 boundary

The curl canonical specification path remains:

`config/protocol_specifications/curl.json`

Decision 0019 is **not** superseded by this authorization.

Its current requirement that canonical specifications validate against the
unmodified frozen V1 schema remains active.

Therefore V2 cannot be used for canonical curl materialization until a separate
future governance action explicitly approves V2 and supersedes/amends the
relevant Decision-0019 schema-binding rule.

## Content-hash boundary

The current hash contract remains:

`config/protocol_content_hash_canonicalization.v1.json`

SHA-256:

`5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f`

It is not modified by this authorization.

Any required V2 hash-contract successor must be separately governed.

## Non-authorization

This decision does not authorize:

- modification of the V1 schema;
- activation of Schema V2;
- Decision-0019 supersession;
- canonical-path-map modification;
- content-hash-contract modification;
- protocol-obligation-contract modification;
- positive V4-to-V2 mapping;
- curl.json;
- curl canonical freeze;
- analyzer implementation or execution;
- baseline execution;
- controlled LLM review;
- repair.

## Review requirement

After authoring, exact Schema V2 must reach an immutable author checkpoint and
undergo independent human technical review before any activation or downstream
mapping can be considered.

## Next boundary

`AUTHOR_PROTOCOL_SPECIFICATION_SCHEMA_V2_SUCCESSOR_CANDIDATE`
