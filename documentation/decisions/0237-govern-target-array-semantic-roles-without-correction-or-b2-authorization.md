# Decision 0237 — Govern Target-Array Semantic Roles Without Corrective Execution or B2 Authorization

Date: 05 September 2026

Status:

`TARGET_ARRAY_SEMANTIC_ROLES_GOVERNED_WITHOUT_CORRECTIVE_EXECUTION_OR_B2_AUTHORIZATION`

## Pre-existing-role result

The strict D0234-tree audit found no pre-existing explicit field-to-array-role
binding for either target field.

`PREEXISTING_EXPLICIT_FIELD_TO_ARRAY_ROLE_BINDING_FOUND=NO`

This decision therefore creates a new explicit governance contract rather
than claiming discovery of a historical contract.

`D0237_CREATES_NEW_EXPLICIT_ROLE_GOVERNANCE=YES`

## Governed field roles

`candidate_schema_v2_carrier_families`

is governed as:

`COLLECTION_SEMANTIC_ROLE=IDENTIFIER_SET_ARRAY`

`SEMANTIC_ORDER=ORDER_IRRELEVANT`

`CANONICAL_ORDER=ASCENDING_LEXICOGRAPHIC_EXACT_UTF8_BYTES`

`DUPLICATE_VALUES_ALLOWED=NO`

`matrix_unit_analysis_field_classes`

is governed identically.

Array position does not encode priority, ranking, temporal order, execution
order, or source precedence.

## D0236 consequence

D0236 contains 109 observed
`candidate_schema_v2_carrier_families` arrays. Seventy-seven are not in exact
UTF-8 ascending order and none contain duplicate values.

`D0236_TARGET1_NONCONFORMING_ARRAY_COUNT=77`

D0236 contains 109 observed
`matrix_unit_analysis_field_classes` arrays. None are unsorted and none
contain duplicate values.

`D0236_TARGET2_NONCONFORMING_ARRAY_COUNT=0`

Therefore:

`D0236_FULL_TARGET_ARRAY_SEMANTICS_CONFORMANCE=NO`

`FUTURE_CORRECTIVE_SUCCESSOR_REQUIRED=YES`

## No corrective execution

D0237 does not modify D0236 and does not reorder any array.

`D0236_MODIFIED=NO`

`TARGET_ARRAY_VALUES_CHANGED=NO`

`TARGET_ARRAYS_REORDERED=NO`

`B1_REEXECUTED=NO`

A corrective successor requires separate explicit authorization and
execution.

`D0238_CORRECTIVE_EXECUTION_AUTHORIZED=NO`

## No B2-B7 authorization

`B2_AUTHORIZED=NO`

`B3_AUTHORIZED=NO`

`B4_AUTHORIZED=NO`

`B5_AUTHORIZED=NO`

`B6_AUTHORIZED=NO`

`B7_AUTHORIZED=NO`

`DOMAIN_FREEZE_CREATED=NO`

`FORWARD_WITNESS_ACQUIRED=NO`

`REVERSE_WITNESS_ACQUIRED=NO`

`CROSS_SOURCE_JOIN_PERFORMED=NO`

`CONCRETE_SOURCE_UNIT_CARRIER_MAPPING_CREATED=NO`

`REQ06_REQ14_DETERMINATION_PERFORMED=NO`

`PAIR_RECLASSIFICATION_PERFORMED=NO`

## Other boundaries

`ACTIVE_SCHEMA_V2_MATERIALIZATION_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

## Next governance requirement

Read-only verify D0237. Only after that verification may a separate bounded
authorization for a corrective successor be considered. That future
correction may address the 77 nonconforming
`candidate_schema_v2_carrier_families` arrays, but it must not create B2
authorization, freeze, mapping, or Req06/Req14 determination by implication.

## Package

Path:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0237_target_array_semantic_role_governance_v1`

Manifest SHA-256:

`d0d16581d995b6651330dbbd97d5c6cd87c9f761ab457891348786e00085a87e`
