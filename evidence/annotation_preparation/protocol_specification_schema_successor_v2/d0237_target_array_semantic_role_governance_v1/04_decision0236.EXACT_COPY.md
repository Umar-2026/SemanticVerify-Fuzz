# Decision 0236 — Create D0235 B1 Whitespace/Hash Corrective Successor and Source-Local Role Refinement Without B2 Authorization

Date: 05 September 2026

Status:

`D0235_B1_WHITESPACE_HASH_CORRECTIVE_SUCCESSOR_WITH_ARRAY_ROLE_UNRESOLVED`

## Historical predecessor

Decision0235 commit:

`3cda6cf4ea79434b8ed899ff3b5d28a8dc68d205`

Decision0235 tree:

`acb702e968c762d215976a91d25897580722dd3b`

Decision0235 manifest:

`e463755f26608bae56096518e31a2033b6ea3b9821132909350df858708a5c57`

Decision0235 remains immutable.

`D0235_HISTORICAL_B1_EXECUTION_PRESERVED=YES`

`B1_REEXECUTED_BY_D0236=NO`

`ORIGINAL_AUTHORIZED_SOURCES_REPARSED_BY_D0236=NO`

## Established correction

The four D0235 child JSON artifacts had a final LF while the adopted D0227
JSON contract specifies no insignificant whitespace.

D0236 creates successor child bytes that are exactly the D0235 child bytes
with that single final LF removed.

`FOUR_CHILD_SUCCESSORS_DIFFER_ONLY_BY_FINAL_LF_REMOVAL=YES`

Their SHA-256 values are rebound in the D0236 successor record.

`FOUR_CHILD_HASHES_REBOUND_TO_SUCCESSOR_BYTES=YES`

Because target-array semantic roles remain unresolved, Decision0236 does not
claim that those successor child bytes satisfy every D0227 array-semantic
requirement.

`FULL_D0227_ARRAY_SEMANTICS_CONFORMANCE=NOT_ESTABLISHED`

`FULL_D0227_CANONICAL_HASH_TARGET_CONFORMANCE=NOT_ESTABLISHED`

## Target-array boundary

`candidate_schema_v2_carrier_families_OCCURRENCES=109`

`candidate_schema_v2_carrier_families_UTF8_UNSORTED_OCCURRENCES=77`

`matrix_unit_analysis_field_classes_OCCURRENCES=109`

`matrix_unit_analysis_field_classes_UTF8_UNSORTED_OCCURRENCES=0`

No explicit governed binding establishes either exact field as an
`identifier_set_arrays` field.

Therefore:

`TARGET_ARRAY_ORDER_CHANGED_BY_D0236=NO`

`TARGET_ARRAY_IDENTIFIER_SET_ROLE_GOVERNED=NO`

The 77 observed unsorted candidate-family arrays are preserved exactly.

## Source-local role refinement

`PRIMARY_ENUMERATION_PAIR_ROW=18639`

`ENUMERATION_METADATA_OR_AUXILIARY=5`

`REVIEWED_LEAF_FIELD=531`

`SEMANTIC_UNIT_CONTEXT=109`

`NESTED_CANDIDATE_DOMAIN_PATH_CONTEXT=97`

`TRACEABILITY_METADATA_OR_AUXILIARY=3`

This classification is derived only from committed D0235 outputs.

`OBSERVED_SOURCE_LOCAL_VALUES_CHANGED=NO`

`CROSS_SOURCE_JOIN_PERFORMED=NO`

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

`CONCRETE_SOURCE_UNIT_CARRIER_MAPPING_CREATED=NO`

`REQ06_REQ14_DETERMINATION_PERFORMED=NO`

`PAIR_RECLASSIFICATION_PERFORMED=NO`

## No substantive conclusion

`B2_DOMAIN_COMPLETENESS_ESTABLISHED=NO`

`REQ06_REQ14_SATISFACTION_ESTABLISHED=NO`

`REQ06_REQ14_VIOLATION_ESTABLISHED=NO`

`SCHEMA_V2_SEMANTIC_LOSSLESSNESS_ESTABLISHED=NO`

## Other boundaries

`ACTIVE_SCHEMA_V2_MATERIALIZATION_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

## Next governance requirement

Decision0236 must be read-only verified. The semantic role of the two target
array fields must then be separately resolved or governed before any B2
complete-accounting-domain-freeze authorization is considered.

## Package

Path:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0236_d0235_b1_canonicalization_role_refinement_corrective_successor_v1`

Manifest SHA-256:

`9a8703e59b8869f0b884993f4c7d1e4106596f08dd65033d3e088768b783dcbd`
