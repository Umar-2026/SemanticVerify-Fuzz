# Successor to Decision 0019 for Version-Dispatched Canonical Protocol Specifications

Status: ACTIVE UPON EXPLICIT SCHEMA V2 ACTIVATION DECISION

## Historical preservation

Decision 0019 remains immutable and historically authoritative for the V1
canonicalization era.

It is not edited in place.

## Canonical root

The canonical root remains:

`config/protocol_specifications/`

The existing per-library canonical path convention remains unchanged.

## Version-dispatched schema validation

For any future canonical protocol specification:

- if `schema_version` is exactly `1.0.0`, validate against
  `config/schemas/protocol_specification.schema.json`;

- if `schema_version` is exactly `2.0.0`, validation may occur against
  `config/schemas/protocol_specification.v2.schema.json` only after the
  exact V2 schema and exact V2 hash contract have both been activated by a
  later reviewed governance decision;

- any other, absent, malformed, or ambiguous schema version is rejected.

No heuristic fallback between schema versions is permitted.

## Hash/canonicalization dispatch

V1 artifacts remain governed by:

`config/protocol_content_hash_canonicalization.v1.json`

V2 artifacts may be governed by:

`config/protocol_content_hash_canonicalization.v2.json`

only after that exact contract has been independently reviewed and activated.

The V1 contract is not silently reused for V2.

## Frozen V1 artifacts

Existing frozen canonical zlib and libpcap artifacts remain immutable.

They are not rewritten, migrated, normalized, or rehashed merely because V2
becomes available for future V2 artifacts.

## Separation from semantic mapping

Schema activation defines representational eligibility only.

It does not prove a lossless semantic mapping from curl technical V4 to Schema
V2 and does not authorize such a mapping.

## Explicit non-effects

This successor does not itself create curl.json and does not authorize analyzer
implementation/execution, baseline execution, or repair.

## Activation condition

This text is operative only upon adoption by the explicit reviewed Schema V2 activation
decision. Before that adoption, this finalized active-form text remains review evidence only.
