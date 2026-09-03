# D0227 ASER04 / ASER07 Remaining-Findings Corrective Successor V5 — Boundary

## Status

`AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR`

This package is not governance-approved or adopted.

A new independent human re-review is required.

## Human-review basis

Returned review SHA-256:

`daf3ac553885e3a8547cb48c9271015434d1b0c8f33cc51a3afd083f4e73627e`

Recorded outcome:

- `ASER04=REVISION_REQUIRED`
- `ASER07=REVISION_REQUIRED`
- `OVERALL=REVISION_REQUIRED`

## ASER04 correction

The V5 canonicalization contract defines one exact canonical JSON string and
member-name byte representation.

Canonicalization operates on the parsed Unicode scalar-value sequence after
JSON escape decoding.

Canonical output:

- escapes U+0022 only as reverse-solidus + quotation mark;
- escapes U+005C only as two reverse solidus bytes;
- emits every U+0000 through U+001F character as lowercase six-byte
  `\u00xx` form;
- forbids the short `\b`, `\t`, `\n`, `\f`, and `\r`
  spellings in canonical output;
- emits U+002F unescaped;
- emits other valid Unicode scalar values directly as UTF-8;
- applies no Unicode normalization;
- uses exactly the same emission algorithm for member names.

The canonical test-vector artifact fixes expected canonical UTF-8 bytes and
SHA-256 values, including the reviewer's newline escape counterexample.

## ASER07 correction

Strict ordering now requires BOTH:

1. freeze and witness commits are distinct; and
2. `git merge-base --is-ancestor freeze_commit witness_commit` exits 0.

The checked freeze commit must equal
`complete_freeze_record.freeze_commit`.

The checked witness commit must equal
`witness_lineage.creation_commit`.

The identical-commit case is explicitly a FAIL even though Git ancestry
returns success.

The ordering test-vector artifact includes that exact counterexample.

Generic absence of all historical witness artifacts from the freeze tree is
not defined as a separate acceptance requirement. The temporal guarantee is
strict distinct ancestry plus exact commit binding and the already-preserved
immutable-domain / anti-circularity controls.

## Existing source bytes included for next review

This package includes exact byte-preserving copies of the already-existing
checksum-bound enumeration and traceability sources.

Enumeration SHA-256:

`44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12`

Traceability SHA-256:

`6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4`

This resolves a ZIP-only review limitation.

It is not new accounting-evidence acquisition and is not new domain
acquisition.

## Preserved PASS items

The following are not reopened:

- ASER01
- ASER02
- ASER03
- ASER05
- ASER06
- ASER08
- ASER09

## D0226 one-time authorization lifecycle

D0226 R03 was executed exactly once and returned PASS.

`D0226_R03_STATE=PERMANENTLY_RETIRED`

`D0226_R03_RERUN_AUTHORIZED=NO`

It must never be rerun.

Decision0221 R03 also remains permanently retired.

Decision0220 A02 remains superseded unexecuted.

## Operational boundary

This package does not:

- acquire actual AEA01-AEA05 accounting evidence;
- acquire or freeze actual U/C domains;
- construct actual forward or reverse witnesses;
- create concrete source-unit-to-carrier mappings;
- determine Req06/Req14 accounting satisfaction;
- reclassify any pair;
- modify active Schema V2;
- execute or authorize analyzer work;
- execute or authorize baselines;
- implement or execute repair.

## Approval / adoption

`CORRECTIVE_SUCCESSOR_APPROVED=NO`

`GOVERNANCE_ADOPTED=NO`

`INDEPENDENT_HUMAN_REREVIEW_REQUIRED=YES`
