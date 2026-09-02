# Decision 0222 — Author Source-Backed Bounded Corrective Successor Revision for ASER04 and ASER07

Date: 02 September 2026

Status:

`AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR`

## Authorization checkpoint

Decision0221 commit:

`25658132f010ce00fc9cce04f974c1d1a88c45b8`

Decision0221 tree:

`fa9536d486361589a7699cd893a3f9156de756a5`

Decision0221 first-and-only successor verifier SHA-256:

`04200a09526bffec25d77702f877b9d21b4ed7da407976c9e4510284e7ee6d08`

## First-and-only authorization consumption

Decision0221 R03 was executed exactly once.

Result:

`PASS`

Execution attempt count:

`1`

State after execution:

`PERMANENTLY_RETIRED`

Rerun authorized:

`NO`

Consumption sentinel SHA-256:

`cfdbc66438b313b0c3e5924f51544a1b5ada65e70bcdf74a8a6791d0a9e1ed3d`

Execution stdout SHA-256:

`199ed76258688270626e986782fc11735bbcebd28be93107207691a73ee02a73`

Execution stderr SHA-256:

`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

Decision0220 A02 remains:

`SUPERSEDED_UNEXECUTED`

It was never executed and must never be executed.

## Corrected V4 preconsumption freeze

Frozen V4 manifest SHA-256:

`f59555f88d27213e1883d73672d508132aa9d61980cc3bb45100b438a7f4a63e`

Frozen V4 binding SHA-256:

`58722158bcc4ec22a02e26f1187a83a7a3e413a7bfed0d71781ca055c88c436e`

The exact frozen source-backed V4 bytes are promoted by this decision to the
governed corrective-successor state without rewriting those frozen bytes.

Governed package path:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser04_aser07_source_backed_revision_v4`

Governed package manifest SHA-256:

`fc35dc047816da91cb3c664840f640050349662a0badb179839d59cb1035f48c`

## Corrective scope

Only:

`ASER04, ASER07`

remain in corrective scope.

Fresh PASS preserved:

`ASER01, ASER02`

Predecessor PASS preserved:

`ASER03, ASER05, ASER06, ASER08, ASER09`

No PASS item is reopened.

## ASER04 corrective design

Future AEA01 source-unit identifiers remain derived from the exact frozen
109-unit enumeration source.

For each source-unit identifier, source metadata is obtained from the unique
checksum-bound semantic-unit traceability record with the same identifier:

`source_container = traceability.source_container`

`source_path = traceability.source_path`

`source_unit_kind = traceability.unit_kind`

`source_provenance_sha256 = traceability.value_sha256`

The complete traceability artifact is separately checksum-bound.

Identifier-prefix inference is not used.

A synthetic constant source-unit kind is not used.

Future AEA01-AEA04 uniqueness, record-count, coverage, AEA02 closure, and
forward/reverse consistency are subject to explicit machine-checkable
cross-artifact invariants.

Self-referential artifact hashing is removed through detached hashing.

## ASER07 corrective design

AEA03 and AEA04 lineage are closed formal objects with the complete required
lineage fields.

A separate complete domain-freeze-record schema is supplied.

AEA05 includes complete freeze-event metadata and must match the bound freeze
record.

Ancestry, immutable-domain, and C-domain-closure claims require
checksum-addressed independently recomputed verifier-output records.

Zero unresolved candidates and exact equality between frozen C and INCLUDED
candidate membership are mandatory before future freeze/satisfaction
evaluation.

## Evidence boundary

This decision authors specification artifacts only.

It does not acquire actual accounting evidence.

It does not construct or freeze U or C.

It does not create forward or reverse witnesses.

It does not create a concrete source-unit-to-schema-carrier mapping.

It does not determine accounting satisfaction.

It does not reclassify any pair.

It does not modify active Schema V2.

It does not authorize generated-driver inspection, gold annotation, analyzer,
baseline, or repair work.

## Review lifecycle

This corrective successor is:

`AUTHOR_CANDIDATE`

It is not approved by this authoring decision.

It is not governance-adopted.

A new independent human re-review of the ASER04/ASER07 corrective scope is
required before any later approval or governance adoption.
