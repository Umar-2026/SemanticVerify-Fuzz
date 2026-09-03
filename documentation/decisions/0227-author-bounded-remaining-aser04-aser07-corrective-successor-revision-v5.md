# Decision 0227 — Author Bounded Remaining ASER04 / ASER07 Corrective Successor Revision V5

Date: 03 September 2026

Status:

`AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR`

## Authorization basis

Decision0226 commit:

`7d81279f26c700c38a010dbee7d69baabcc05fc4`

Decision0226 tree:

`6a4c1ba145f58e807e9a0d41e6c7cf6bd12debc8`

D0226 R03 first-and-only execution result:

`PASS`

D0226 R03 consumption-sentinel SHA-256:

`784cc8cf4ce1c60915960af1bad8a127213752fdde502559b4581c3c937bf804`

D0226 R03 is permanently retired and must never be rerun.

## Human-review basis

Returned review SHA-256:

`daf3ac553885e3a8547cb48c9271015434d1b0c8f33cc51a3afd083f4e73627e`

Recorded review outcome:

`ASER04=REVISION_REQUIRED`

`ASER07=REVISION_REQUIRED`

`OVERALL=REVISION_REQUIRED`

## Corrective scope

Only:

`ASER04, ASER07`

### ASER04

Revision V5 completes the missing canonical JSON string/member-name emission
contract.

The contract operates on parsed Unicode scalar values and fixes one canonical
representation for quotation marks, reverse solidus, U+0000–U+001F controls,
solidus and non-ASCII values.

Optional JSON escape forms are not permitted in canonical output.

Canonical-byte and SHA-256 test vectors are supplied, including the human
reviewer's `\n` versus `\u000a` counterexample.

### ASER07

Revision V5 makes strict ordering machine-checkable.

PASS requires:

1. freeze and witness commits are distinct;
2. the freeze commit is an ancestor of the witness creation commit;
3. the checked freeze commit equals the checksum-bound complete freeze record;
4. the checked witness commit equals the checksum-bound witness lineage.

The identical-commit case is explicitly represented as a negative test vector
even when Git ancestry reports success.

Generic exclusion of every historical witness artifact from the freeze tree is
explicitly not an independent acceptance criterion.

## Existing source copies for next review

Exact existing enumeration source:

SHA-256 `44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12`

Exact existing traceability source:

SHA-256 `6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4`

Both are included in the candidate package as byte-preserving copies to remove
the previous ZIP-only verification limitation.

This is not new accounting evidence or domain acquisition.

## Preserved PASS items

`ASER01, ASER02, ASER03, ASER05, ASER06, ASER08, ASER09`

They are not reopened.

## Approval / adoption boundary

`CORRECTIVE_SUCCESSOR_APPROVED=NO`

`GOVERNANCE_ADOPTED=NO`

`INDEPENDENT_HUMAN_REREVIEW_REQUIRED=YES`

No PASS outcome for ASER04 or ASER07 is authored by this decision.

## Operational boundary

This decision does not authorize or perform actual accounting evidence
acquisition, U/C acquisition or freeze, witness acquisition, concrete mapping,
satisfaction determination, pair reclassification, active Schema-V2
modification, analyzer work, baseline work or repair.

Decision0221 R03 remains permanently retired.

Decision0220 A02 remains superseded unexecuted.

## Governed candidate package

Path:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_acquisition_specification_study_v2_corrective_successor_for_aser04_aser07_remaining_findings_revision_v5`

Manifest SHA-256:

`db90747fb8f586992c524e5c541a1414bb12349b874ca4fa8a709c4ae0f17ab8`
