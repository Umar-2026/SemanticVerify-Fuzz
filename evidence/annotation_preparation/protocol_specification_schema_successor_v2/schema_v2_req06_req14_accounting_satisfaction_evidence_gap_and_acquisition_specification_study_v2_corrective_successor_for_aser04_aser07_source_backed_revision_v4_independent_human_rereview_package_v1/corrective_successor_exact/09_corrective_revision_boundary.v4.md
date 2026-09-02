# D0222 ASER04/ASER07 Source-Backed Corrective Revision V4 — Boundary

## Status

`AUTHOR_CANDIDATE_SPECIFICATION_ONLY_PREBUILD`

This package is not yet a governed Decision0222 successor.

Decision0221 R03 has not been executed by this prebuild.

## Corrective scope

Only:

- ASER04
- ASER07

are under correction.

Preserved PASS items are not reopened:

- ASER01
- ASER02
- ASER03
- ASER05
- ASER06
- ASER08
- ASER09

## Source-unit metadata derivation

The governed source-unit identifier set is enumerated from:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser01_aser02_aser04_aser07/enumeration_sources_exact/01_semantic_unit_carrier_admissibility_matrix.v1.json`

SHA-256:

`44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12`

The exact source-unit metadata source is:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_semantic_role_relation_formalization_v1/03_v4_semantic_unit_context_and_leaf_traceability.v1.json`

SHA-256:

`6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4`

For each enumerated source unit `u`, exactly one traceability record `r`
must exist with:

`r.unit_id == u`

Future AEA01 metadata is derived only as follows:

`source_container = r.source_container`

`source_path = r.source_path`

`source_unit_kind = r.unit_kind`

`source_provenance_sha256 = r.value_sha256`

No identifier-prefix inference is permitted.

No constant synthetic source-unit kind is permitted.

AEA01 separately binds the complete traceability artifact SHA-256.

## Evidence boundary

This package specifies future evidence structure only.

It does not construct AEA01-AEA05 evidence instances.

It does not construct or freeze U or C.

It does not create forward or reverse witnesses.

It does not create a concrete source-unit-to-carrier mapping.

It does not determine accounting satisfaction.

It does not reclassify any pair.

It does not modify active Schema V2.

It does not authorize analyzer, baseline, or repair execution.

## Required lifecycle

If later authorized and authored as the governed corrective successor,
its status remains:

`AUTHOR_CANDIDATE`

A new independent human re-review is required before any governance adoption.
