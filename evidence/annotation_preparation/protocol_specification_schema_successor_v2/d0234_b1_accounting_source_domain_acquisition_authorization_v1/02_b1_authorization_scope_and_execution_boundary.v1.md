# D0234 — B1 Accounting Source and Domain Acquisition Authorization

## Status

`B1_ACCOUNTING_SOURCE_AND_DOMAIN_ACQUISITION_AUTHORIZED_NOT_EXECUTED`

Decision0234 creates a bounded authorization for future B1 execution.

`B1_AUTHORIZED=YES`

`B1_EXECUTED_BY_D0234=NO`

## Exact source scope

Only the following two existing governed sources are authorized.

### Enumeration source

Path:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser01_aser02_aser04_aser07/enumeration_sources_exact/01_semantic_unit_carrier_admissibility_matrix.v1.json`

SHA-256:

`44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12`

Git blob:

`b50e1bb81f7eb8842c7bdc9bd5cb9df5a56ed861`

D0227 exact copy:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser04_aser07_remaining_findings_revision_v5/existing_source_copies_exact/01_semantic_unit_enumeration_source.EXACT_COPY.v1.json`

### Traceability source

Path:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_semantic_role_relation_formalization_v1/03_v4_semantic_unit_context_and_leaf_traceability.v1.json`

SHA-256:

`6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4`

Git blob:

`877225ffab98272684726b8a1caf5db5fe0946e5`

D0227 exact copy:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser04_aser07_remaining_findings_revision_v5/existing_source_copies_exact/02_semantic_unit_traceability_source.EXACT_COPY.v1.json`

No additional source is authorized.

`SOURCE_SCOPE_EXPANSION_AUTHORIZED=NO`

`UNLISTED_EXTERNAL_SOURCE_ACQUISITION_AUTHORIZED=NO`

## Authorized future B1 operations

A separately authored future B1 execution may:

1. read the exact checksum-bound bytes of the two authorized sources;
2. record byte identity and provenance;
3. parse each authorized source independently;
4. derive source-local Req06/Req14 accounting-domain input records;
5. canonicalize those derived B1 records under the adopted D0227 rules; and
6. package B1 outputs with detached hashes.

The future B1 execution package is designated as:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0235_b1_accounting_source_domain_acquisition_v1`

Decision0234 does not create that package.

## No cross-source mapping in B1

B1 may not join enumeration records with traceability records to create a new
source-unit/carrier mapping.

`CROSS_SOURCE_JOIN_AUTHORIZED=NO`

`CONCRETE_SOURCE_UNIT_CARRIER_MAPPING_AUTHORIZED=NO`

B1 source-local acquisition must remain distinct from future B5 mapping.

## B1 / B2 separation

`B1_MAY_PREPARE_DOMAIN_INPUTS=YES`

`B1_MAY_DECLARE_DOMAIN_FROZEN=NO`

`B1_MAY_CREATE_FREEZE_RECORD=NO`

`B1_MAY_CREATE_FREEZE_COMMIT=NO`

`B2_DOMAIN_FREEZE_AUTHORIZED=NO`

A separate post-B1 authorization is required for B2.

## Later phases remain unauthorized

`B3_FORWARD_WITNESS_AUTHORIZED=NO`

`B4_REVERSE_WITNESS_AUTHORIZED=NO`

`B5_MAPPING_AUTHORIZED=NO`

`B6_DETERMINATION_AUTHORIZED=NO`

`B7_RECLASSIFICATION_AUTHORIZED=NO`

## No substantive result

`REQ06_REQ14_SATISFACTION_ESTABLISHED=NO`

`REQ06_REQ14_VIOLATION_ESTABLISHED=NO`

`SCHEMA_V2_SEMANTIC_LOSSLESSNESS_ESTABLISHED=NO`

`ACCOUNTING_DOMAIN_COMPLETENESS_ESTABLISHED=NO`

Decision0234 authorizes future acquisition only. It performs no acquisition,
freeze, witness work, mapping, determination, or reclassification.

## Other boundaries

`ACTIVE_SCHEMA_V2_MATERIALIZATION_AUTHORIZED=NO`

`ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

`OPERATIONAL_AUTHORIZATION_CREATED=YES`

`OPERATIONAL_EXECUTION_PERFORMED=NO`

## Protected verifier lifecycle

D0226 R03 remains permanently retired and must never be rerun.

D0221 R03 remains permanently retired and must never be rerun.

D0220 A02 remains superseded unexecuted and must never be executed.
