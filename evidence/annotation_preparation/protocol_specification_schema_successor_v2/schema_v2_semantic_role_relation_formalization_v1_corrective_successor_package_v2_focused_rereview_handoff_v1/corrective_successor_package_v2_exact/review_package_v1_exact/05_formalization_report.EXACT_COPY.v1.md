# Schema-V2 Semantic-Role Relation Formalization V1

Status: **AUTHOR_CANDIDATE**

Selected outcome:

`PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED`

Human-approved: **NO**

## Authoritative reviewed domains

This formalization uses only the already-reviewed Capability Study V1
inventories as domain authorities:

- 531 reviewed V4 leaf-field records from `$.leaf_fields`;
- 109 reviewed V4 semantic-unit records from `$.semantic_units`;
- 57 reviewed matrix `field_class_analysis[].v4_field_class` identifiers;
- 171 reviewed Schema-V2 `property_paths[].path` carriers;
- 123 distinct Schema-V2 property names; and
- 59 open unconstrained Schema-V2 string paths.

The raw V4 all-scalar traversal is **not** used as the 531-leaf domain
authority.

## Important 57-element vocabulary distinction

The reviewed evidence contains two different 57-element vocabularies:

1. the union of `semantic_units[].field_classes`; and
2. `field_class_analysis[].v4_field_class`.

They are not identical sets.

This formalization therefore does not equate or merge them.

The 57 x 171 semantic-role relation uses only
`field_class_analysis[].v4_field_class`.

The unit-inventory vocabulary is retained separately for 531-leaf /
109-unit traceability.

## Conservative relation policy

All 9,747 matrix-field-class / Schema-V2-path pairs are classified.

- `SEMANTICALLY_RELATED`: 113
- `NOT_SEMANTICALLY_RELATED`: 969
- `UNRESOLVED`: 8,665

`SEMANTICALLY_RELATED` is assigned only where Capability Study V1 already
contains a curated semantically-related candidate path for that matrix
field class.

`NOT_SEMANTICALLY_RELATED` is assigned only to Schema-V2
`semantic_accounting` paths because reviewed admissibility rules prohibit
semantic-accounting metadata as substitute semantic storage.

All remaining pairs are `UNRESOLVED`.

In particular, 125 lexical-screening-only pairs remain unresolved.

Absence from prior curated candidate screening is not used as negative
evidence.

## Unit and leaf traceability

All 531 reviewed leaf-field records are preserved in the traceability
artifact.

All 109 reviewed semantic units are bound to their reviewed matrix
unit-analysis records and candidate Schema-V2 carrier families.

Family expansion is recorded only as a future-screening domain; it does not
promote every path in a candidate family to `SEMANTICALLY_RELATED`.

## Current bounded result

Positive existing-Schema-V2 mapping path proven: **NO**

Negative existing-Schema-V2 mapping impossibility proven: **NO**

Admissible-composition exhaustiveness established: **NO**

Constructive positive mapping witness authored: **NO**

Exhaustive admissible-composition enumeration performed: **NO**

Schema-successor requirement determined: **NO**

## Governance

The artifact remains an author candidate.

Independent human technical review is required before it may be used for a
governance decision.
