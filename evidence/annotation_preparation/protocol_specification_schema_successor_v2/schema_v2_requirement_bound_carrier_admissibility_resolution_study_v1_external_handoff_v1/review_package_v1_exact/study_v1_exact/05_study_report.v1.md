# Schema-V2 Requirement-Bound Carrier Admissibility Resolution Study V1

## Status

`AUTHOR_CANDIDATE`

## Global outcome

`FURTHER_EVIDENCE_REQUIRED`

## Governance-adopted requirement basis

Exactly 17 V4 losslessness requirement identities are governance-bound.

- `BOUND_EXACT = 17`
- `BOUND_COMPOSITE = 0`
- provenance `UNRESOLVED = 0`

## Historical carrier domain

The existing carrier study remains immutable and read-only.

- semantic units: `109`
- Schema-V2 property paths: `171`
- historical Cartesian pairs: `18,639`

No historical pair was modified or reclassified.

## Requirement-level carrier result

- `ADMISSIBLE_EXACT = 0`
- `ADMISSIBLE_COMPOSITE = 0`
- `NO_ADMISSIBLE_CARRIER_PROVEN = 0`
- `UNRESOLVED = 17`

## Principal evidence gap

The historical 18,639 carrier rows bind `semantic_unit_id` to
`schema_v2_property_path`, but contain no authoritative requirement identifier.

The older 17 requirement records remain index-only placeholders with
`requirement_text = null` and `UNRESOLVED_SOURCE_BINDING`.

Those historical indices are not semantically equated to the governance-bound
canonical requirement identifiers.

Therefore no exact or composite requirement-level carrier witness can be
claimed from the authorized evidence, and absence of a witness cannot be
promoted into `NO_ADMISSIBLE_CARRIER_PROVEN`.

## Correct bounded conclusion

`FURTHER_EVIDENCE_REQUIRED`

This is not evidence that Schema V2 is insufficient. It means that the current
authorized evidence does not yet establish the required semantic crosswalk.

## Technical nonclaims

This study does not prove:

- Schema-V2 losslessness;
- carrier admissibility;
- a positive V4-to-V2 mapping;
- negative mapping impossibility; or
- whole-V4 exhaustiveness.

## Operational boundary

No operational mapping, Schema-V2 modification, schema successor, Schema V3,
`curl.json`, analyzer, baseline, or repair authority is created.

## Review boundary

Independent human review is required before governance adoption or any stronger
technical inference.
