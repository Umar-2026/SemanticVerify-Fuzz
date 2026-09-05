# Decision 0234 — Authorize Bounded B1 Accounting Source and Domain Acquisition Without Execution

Date: 05 September 2026

Status:

`B1_ACCOUNTING_SOURCE_AND_DOMAIN_ACQUISITION_AUTHORIZED_NOT_EXECUTED`

## Governance basis

Decision0233 commit:

`0db3754bb07e27b5895c15d3b2dddb05009ac647`

Decision0233 tree:

`7dd9f21c914b41b9ad2d802fdf77561553e87dd4`

Decision0233 manifest:

`c608ad15a5a345cb0f525389cb70c9a478057c3e44fa265538ed259a150ccc0b`

## Authorization

Decision0234 authorizes future B1:

`B1=ACCOUNTING_SOURCE_AND_DOMAIN_ACQUISITION`

`B1_AUTHORIZED=YES`

Decision0234 does not execute B1.

`B1_EXECUTED_BY_D0234=NO`

## Exact two-source scope

Enumeration source:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser01_aser02_aser04_aser07/enumeration_sources_exact/01_semantic_unit_carrier_admissibility_matrix.v1.json`

SHA-256:

`44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12`

Traceability source:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_semantic_role_relation_formalization_v1/03_v4_semantic_unit_context_and_leaf_traceability.v1.json`

SHA-256:

`6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4`

No additional source is authorized.

`SOURCE_SCOPE_EXPANSION_AUTHORIZED=NO`

## Authorized future operations

A separately authored B1 execution may read the exact two source byte streams,
record provenance and detached hashes, parse each source independently, derive
source-local Req06/Req14 accounting-domain input records, canonicalize those
records under adopted D0227 rules, and package the resulting B1 acquisition
artifacts.

Designated future execution package:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0235_b1_accounting_source_domain_acquisition_v1`

Decision0234 does not create that package.

## B1 cannot become B5

`CROSS_SOURCE_JOIN_AUTHORIZED=NO`

`CONCRETE_SOURCE_UNIT_CARRIER_MAPPING_AUTHORIZED=NO`

No new enumeration-to-traceability join is authorized.

## Later phases

`B2_DOMAIN_FREEZE_AUTHORIZED=NO`

`B3_FORWARD_WITNESS_AUTHORIZED=NO`

`B4_REVERSE_WITNESS_AUTHORIZED=NO`

`B5_MAPPING_AUTHORIZED=NO`

`B6_DETERMINATION_AUTHORIZED=NO`

`B7_RECLASSIFICATION_AUTHORIZED=NO`

## No result established

`REQ06_REQ14_SATISFACTION_ESTABLISHED=NO`

`REQ06_REQ14_VIOLATION_ESTABLISHED=NO`

`SCHEMA_V2_SEMANTIC_LOSSLESSNESS_ESTABLISHED=NO`

`ACCOUNTING_DOMAIN_COMPLETENESS_ESTABLISHED=NO`

## Other non-authorizations

`ACTIVE_SCHEMA_V2_MATERIALIZATION_AUTHORIZED=NO`

`ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

## Lifecycle distinction

`OPERATIONAL_AUTHORIZATION_CREATED=YES`

`OPERATIONAL_EXECUTION_PERFORMED=NO`

A read-only verification of Decision0234 is required before a separate D0235
B1 execution package may read or parse the authorized source bytes.

## Protected one-time verifiers

D0226 R03 remains permanently retired and must never be rerun.

D0221 R03 remains permanently retired and must never be rerun.

D0220 A02 remains superseded unexecuted and must never be executed.

## D0234 package

Path:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0234_b1_accounting_source_domain_acquisition_authorization_v1`

Manifest SHA-256:

`bcd12a48d3a67322d8cbb8af42e3fb5e6aa4e021150cda98f86bc19c136ab90c`
