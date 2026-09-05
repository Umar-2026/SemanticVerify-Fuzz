# Decision 0238 — Authorize Bounded Target-Array Canonical-Order Corrective Execution Without B2 Authorization

Date: 05 September 2026

Status:

`D0239_TARGET_ARRAY_CANONICAL_ORDER_CORRECTIVE_EXECUTION_AUTHORIZED_NOT_EXECUTED`

## Authorization-only nature

D0238 creates a bounded operational authorization for a future D0239
corrective successor.

`D0238_ITSELF_PERFORMS_ARRAY_CORRECTION=NO`

`D0239_CORRECTIVE_EXECUTION_AUTHORIZED=YES`

`D0239_EXECUTION_PERFORMED=NO`

## Authorized correction

Authorized field:

`candidate_schema_v2_carrier_families`

Governed collection role:

`IDENTIFIER_SET_ARRAY`

Authorized operation:

`SORT_EACH_TARGET_ARRAY_ASCENDING_BY_EXACT_UTF8_BYTES`

Exact bounds:

`TARGET1_OCCURRENCE_COUNT=109`

`TARGET1_EXACT_REORDER_COUNT=77`

`TARGET1_DUPLICATE_ARRAY_COUNT=0`

`TARGET1_MEMBERSHIP_CHANGE_AUTHORIZED=NO`

`TARGET1_ELEMENT_INSERTION_AUTHORIZED=NO`

`TARGET1_ELEMENT_DELETION_AUTHORIZED=NO`

`TARGET1_ELEMENT_VALUE_CHANGE_AUTHORIZED=NO`

The field:

`matrix_unit_analysis_field_classes`

already conforms and is not authorized for correction.

`TARGET2_OCCURRENCE_COUNT=109`

`TARGET2_EXACT_REORDER_COUNT=0`

`TARGET2_CORRECTION_AUTHORIZED=NO`

## Exact hash binding

D0236 trace-domain predecessor:

`TRACE_DOMAIN_SHA256=d02d67addc0af427d71da66588ce6e1020017007dbdae76b3ef0c6cb3d5b625d`

Expected D0239 corrected trace-domain successor:

`EXPECTED_D0239_TRACE_DOMAIN_SHA256=9cee6cb560179386da9104d12d353a581dfe8c6149c5890b19c13b0973efc9f2`

`EXPECTED_D0239_TRACE_DOMAIN_SIZE_BYTES=486907`

`EXACT_CHANGED_JSON_PATH_COUNT=77`

`UNEXPECTED_NON_TARGET_CHANGE_COUNT=0`

## Designated D0239 package

`DESIGNATED_D0239_EXECUTION_PACKAGE=evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0239_target_array_canonical_order_corrective_successor_v1`

D0239 may create only the bounded corrective successor artifacts required
to realize and verify this correction.

## Historical immutability

`D0236_MUST_REMAIN_IMMUTABLE=YES`

`D0237_MUST_REMAIN_IMMUTABLE=YES`

`ORIGINAL_AUTHORIZED_SOURCES_MUST_NOT_BE_REPARSED=YES`

`B1_MUST_NOT_BE_REEXECUTED=YES`

## B2-B7 remain unauthorized

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

## Claims not established

D0238 does not establish:

`FULL_D0227_CANONICAL_CONFORMANCE=NO`

`ACCOUNTING_DOMAIN_COMPLETENESS_ESTABLISHED=NO`

`B2_READINESS_ESTABLISHED=NO`

`REQ06_REQ14_SATISFACTION_ESTABLISHED=NO`

`REQ06_REQ14_VIOLATION_ESTABLISHED=NO`

`SCHEMA_V2_SEMANTIC_LOSSLESSNESS_ESTABLISHED=NO`

## Other boundaries

`ACTIVE_SCHEMA_V2_MATERIALIZATION_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

## Next step

Read-only verify D0238. D0239 must not execute until that authorization
checkpoint is independently verified.

## Package

Path:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0238_target_array_corrective_execution_authorization_v1`

Manifest SHA-256:

`280add229ff56b7fa45d7f75acf2c174b9ea956f91cf1c830584e4052073c525`
