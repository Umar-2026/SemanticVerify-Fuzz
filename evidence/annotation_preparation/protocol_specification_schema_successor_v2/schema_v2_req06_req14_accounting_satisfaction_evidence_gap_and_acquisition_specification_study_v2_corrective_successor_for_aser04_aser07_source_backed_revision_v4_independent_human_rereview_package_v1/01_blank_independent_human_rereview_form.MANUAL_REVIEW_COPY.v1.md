# Independent Human Re-Review Form — D0222 Source-Backed Corrective Successor

## Reviewer-completed metadata

Reviewer name: ______________________________

Reviewer role: ______________________________

Review date: ______________________________

Reviewer confirmation / signature: ______________________________

Independence attestation:

[ ] I confirm that I performed this re-review independently and that the
decisions, rationale, notes, and signature below are my own human judgments.

## Review target

Governed candidate:

`Decision0222 — AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR`

Corrective re-review scope:

- ASER04
- ASER07

Preserved PASS items are contextual non-regression constraints and are not
being reopened by this re-review:

- ASER01
- ASER02
- ASER03
- ASER05
- ASER06
- ASER08
- ASER09

The reviewer should inspect the exact D0222 corrective-successor package under:

`corrective_successor_exact/`

The prior returned independent human re-review that required these corrections
is supplied as:

`04_predecessor_returned_rereview.EXACT_COPY.v1.md`

No reviewer outcome is prefilled in this form.

---

# ASER04 — Re-review

## Correction A — Frozen source-unit metadata

Verify that the revised design no longer invents source metadata from the
identifier prefix or from a synthetic constant.

Verify that, for each enumerated source unit, the future governed source-unit
domain derives:

- `source_container` from the exact checksum-bound traceability record
  `source_container`;
- `source_path` from the exact checksum-bound traceability record
  `source_path`;
- `source_unit_kind` from the exact checksum-bound traceability record
  `unit_kind`;
- `source_provenance_sha256` from the exact checksum-bound traceability record
  `value_sha256`.

Verify that the complete traceability artifact is separately checksum-bound and
that the enumeration identifier set must equal the traceability `unit_id` set.

Reviewer notes:

______________________________________________________________________________

______________________________________________________________________________

## Correction B — Uniqueness and count/coverage binding

Verify that the future AEA01/AEA02/AEA03/AEA04 design provides deterministic
machine-checkable treatment of:

- unique source-unit identifiers;
- unique carrier-candidate identifiers;
- unique frozen-carrier identifiers;
- unique forward/reverse relation membership;
- `record_count` binding to actual records;
- forward coverage binding to frozen U and forward records;
- reverse coverage binding to frozen C and reverse records.

Reviewer notes:

______________________________________________________________________________

______________________________________________________________________________

## Correction C — Finalized AEA02 closure

Verify that:

- finalized AEA02 permits only `INCLUDED` or `EXCLUDED`;
- `UNRESOLVED` count must be zero before freeze;
- frozen C must equal exactly the candidate identifiers whose disposition is
  `INCLUDED`.

Reviewer notes:

______________________________________________________________________________

______________________________________________________________________________

## Correction D — Hashing and canonicalization

Verify that:

- the self-referential own-hash problem has been removed;
- hashes are detached from the artifact being hashed;
- string canonicalization is deterministic;
- numeric canonicalization is deterministic;
- identifier-set arrays have deterministic ordering;
- command argv ordering is preserved rather than sorted.

Reviewer notes:

______________________________________________________________________________

______________________________________________________________________________

## ASER04 reviewer decision

[ ] PASS

[ ] REVISION_REQUIRED

ASER04 rationale:

______________________________________________________________________________

______________________________________________________________________________

______________________________________________________________________________

---

# ASER07 — Re-review

## Correction A — AEA03/AEA04 witness lineage

Verify that AEA03 and AEA04 lineage is no longer an unrestricted object and
that the complete required lineage fields are formally required.

Reviewer notes:

______________________________________________________________________________

______________________________________________________________________________

## Correction B — Complete freeze record

Verify that the separate formal complete-freeze-record schema requires the
necessary freeze identity, commits, U/C paths and SHA-256 values,
enumeration-source identity, traceability-source identity,
carrier-candidate-source identity, predecessor hashes, and derivation-input
hashes.

Reviewer notes:

______________________________________________________________________________

______________________________________________________________________________

## Correction C — AEA05 freeze-event closure

Verify that AEA05 contains complete freeze-event metadata and that the
cross-artifact contract requires that metadata to equal the checksum-bound
complete freeze record rather than functioning as an unverified declaration.

Reviewer notes:

______________________________________________________________________________

______________________________________________________________________________

## Correction D — Independently recomputed verifier evidence

Verify that ancestry, immutable-domain, and C-domain-closure evidence is
represented through checksum-bound verifier-output artifacts containing the
relevant:

- verifier identity and SHA-256;
- exact command argv;
- evaluated commits;
- evaluated Git objects;
- evaluated object SHA-256 values;
- individual check results;
- exit code;
- stdout/stderr SHA-256 identities.

Verify that later satisfaction evaluation must independently recompute required
checks rather than trust self-declared `true` booleans.

Reviewer notes:

______________________________________________________________________________

______________________________________________________________________________

## Correction E — Ordering / freeze prerequisites

Verify that the future lifecycle requires, before freeze/satisfaction
evaluation:

- zero unresolved carrier candidates;
- exact equality of frozen C and the `INCLUDED` candidate set;
- domain freeze before witness construction;
- independent verifier-evidence closure before AEA05 provenance closure;
- AEA05 provenance closure before satisfaction evaluation.

Reviewer notes:

______________________________________________________________________________

______________________________________________________________________________

## ASER07 reviewer decision

[ ] PASS

[ ] REVISION_REQUIRED

ASER07 rationale:

______________________________________________________________________________

______________________________________________________________________________

______________________________________________________________________________

---

# Overall independent human re-review decision

[ ] PASS

[ ] REVISION_REQUIRED

Overall rationale:

______________________________________________________________________________

______________________________________________________________________________

______________________________________________________________________________

Additional reviewer notes:

______________________________________________________________________________

______________________________________________________________________________

______________________________________________________________________________

Reviewer confirmation / signature: ______________________________

Review date: ______________________________
