# Decision 0065 — Authorize Explicit Schema V2 Activation Execution

Status: AUTHORIZED — ACTIVATION EXECUTION NOT YET PERFORMED

## Basis

The read-only activation-readiness assessment at repository commit
`7c32d7a51d2a93de254c1bdc52237b1896f924bf` passed.

The following human-review gates are closed:

- Schema V2 candidate approval: PASS
- activation-governance approval: PASS
- V2 hash active-form approval: PASS
- activation-artifact AF01–AF10 state: 10 PASS / 0 REVISION_REQUIRED / 0 FAIL

## Exact future activation actions authorized

A later atomic activation execution may install, without transformation:

1. `evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_hash_contract_finalization_package_v1/02_active_form_v2_hash_contract.REVIEW_CANDIDATE.json`
   SHA-256 `37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9`

   to:

   `config/protocol_content_hash_canonicalization.v2.json`

2. `evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_artifact_finalization_package_v1/02_active_form_version_dispatch.REVIEW_CANDIDATE.json`
   SHA-256 `67a96c3eda8de95fa6c55342d5d33ea725e16cea8af21fcb4f3b8945b9d4eeee`

   to:

   `config/protocol_specification_schema_version_dispatch.v1.json`

The destination bytes must be exactly identical to the reviewed source bytes.

## Decision-0019 successor adoption

The future explicit activation decision must adopt by exact SHA-bound reference
the reviewed successor:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_artifact_finalization_package_v1/05_active_form_decision_0019_successor.REVIEW_CANDIDATE.md`

SHA-256:

`a96f9d8b6811a9f9170a18de9ff8be6f80a3704b9e6a13c59fbb88e423bec3bb`

The future explicit activation decision path is reserved as:

`documentation/decisions/0066-activate-schema-v2-and-adopt-decision-0019-successor.md`

Historical Decision 0019 remains byte-immutable.

## Required non-interference

The activation execution must not modify:

- `config/schemas/protocol_specification.v2.schema.json`
- `config/protocol_content_hash_canonicalization.v1.json`
- `documentation/decisions/0019-canonical-library-protocol-specification-path-convention.md`
- `config/protocol_specifications/zlib.json`
- `config/protocol_specifications/libpcap.json`

## Explicitly not authorized

Decision 0065 does not authorize:

- positive V4-to-V2 mapping;
- creation of `curl.json`;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## Current state

This authorization does not itself install either active artifact, adopt the
Decision-0019 successor, or activate Schema V2.

## Next boundary

Execute the exact explicit Schema V2 activation under Decision 0065 as a
separate atomic governance step.
