# D0237 Target-Array Semantic-Role Governance Boundary

## Nature of this decision

D0237 creates a new explicit collection-semantics contract.

It does not claim that either target field had a pre-existing governed
identifier-set role.

`PREEXISTING_EXPLICIT_FIELD_TO_ARRAY_ROLE_BINDING_FOUND=NO`

`D0237_CREATES_NEW_EXPLICIT_ROLE_GOVERNANCE=YES`

## Exact field bindings

`candidate_schema_v2_carrier_families`

is governed as:

`COLLECTION_SEMANTIC_ROLE=IDENTIFIER_SET_ARRAY`

`SEMANTIC_ORDER=ORDER_IRRELEVANT`

`CANONICAL_ORDER=ASCENDING_LEXICOGRAPHIC_EXACT_UTF8_BYTES`

`DUPLICATE_VALUES_ALLOWED=NO`

`SEMANTIC_INTERPRETATION=MEMBERSHIP_ONLY`

`matrix_unit_analysis_field_classes`

is governed by the same rules.

The observed position of an identifier does not encode priority, rank,
execution order, temporal order, or source precedence.

## D0236 consequence

D0236 recorded 109 occurrences of
`candidate_schema_v2_carrier_families`, of which 77 are not in exact UTF-8
ascending order and none contain duplicates.

Therefore those 77 D0236 arrays do not conform to the newly governed
identifier-set canonical ordering.

D0236 recorded 109 occurrences of
`matrix_unit_analysis_field_classes`; all are already in exact UTF-8
ascending order and none contain duplicates.

`D0236_FULL_TARGET_ARRAY_SEMANTICS_CONFORMANCE=NO`

`FUTURE_CORRECTIVE_SUCCESSOR_REQUIRED=YES`

## No corrective execution in D0237

D0237 does not reorder any array and does not edit D0236.

`TARGET_ARRAY_VALUES_CHANGED=NO`

`TARGET_ARRAYS_REORDERED=NO`

`D0236_MODIFIED=NO`

`B1_REEXECUTED=NO`

A future corrective execution requires a separate explicit authorization.

## B2-B7 remain unauthorized

`B2_AUTHORIZED=NO`

`B3_AUTHORIZED=NO`

`B4_AUTHORIZED=NO`

`B5_AUTHORIZED=NO`

`B6_AUTHORIZED=NO`

`B7_AUTHORIZED=NO`

No freeze, witness acquisition, concrete mapping, Req06/Req14 determination,
or pair reclassification is performed or authorized here.

## Other boundaries

`ACTIVE_SCHEMA_V2_MATERIALIZATION_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`
