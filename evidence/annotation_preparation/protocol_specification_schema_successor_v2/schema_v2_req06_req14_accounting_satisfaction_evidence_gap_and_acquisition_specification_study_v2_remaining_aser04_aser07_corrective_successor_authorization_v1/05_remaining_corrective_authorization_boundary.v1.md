# D0226 Remaining ASER04 / ASER07 Corrective-Successor Authorization Boundary

## Predecessor human outcome

The exact D0225 returned human re-review records:

- `ASER04=REVISION_REQUIRED`
- `ASER07=REVISION_REQUIRED`
- `OVERALL=REVISION_REQUIRED`

Returned-review SHA-256:

`daf3ac553885e3a8547cb48c9271015434d1b0c8f33cc51a3afd083f4e73627e`

## Bounded authorization

Decision0226 authorizes one fresh corrective-successor specification revision
limited to the remaining ASER04 and ASER07 findings.

It does not itself author that corrective successor.

### ASER04

Authorized work is limited to completing the canonical JSON
string/member-name serialization contract and associated canonical-byte and
SHA-256 test vectors.

The successor may define exact handling for control characters, quotation
marks, reverse solidus, optional escapes, non-ASCII Unicode characters and
the interaction with the existing Unicode-normalization policy.

### ASER07

Authorized work is limited to making freeze-before-witness ordering strict and
machine-checkable.

At minimum the successor may require:

- distinct freeze and witness commits;
- successful ancestry from freeze commit to witness commit;
- binding of the checked freeze commit to the complete freeze record;
- binding of the checked witness commit to witness lineage;
- independent recomputation rather than self-declared booleans;
- positive and negative test vectors including the identical-commit case.

If the intended freeze checkpoint must exclude witness artifacts, the successor
may also define and verify that tree-state exclusion condition.

## Next independent re-review package

The next review package may include exact byte-preserving copies of the
already-existing checksum-bound enumeration and traceability source artifacts.

This is packaging of existing evidence only.

It is not authorization for new accounting evidence acquisition or new domain
acquisition.

## Preserved PASS items

The following remain preserved and are not reopened:

- ASER01
- ASER02
- ASER03
- ASER05
- ASER06
- ASER08
- ASER09

## One-time authorization lifecycle

The newly authored D0226 R03 begins in:

`AUTHORED_UNCONSUMED`

Execution attempt count:

`0`

Only its first execution is authorized.

Its first execution attempt consumes the authorization whether PASS or FAIL.

After that first attempt:

`RERUN_AUTHORIZED=NO`

The bounded corrective successor must not be governed-authored before a PASS
consumption of D0226 R03.

Decision0221 R03 remains permanently retired and must never be rerun.

Decision0220 A02 remains superseded unexecuted and must never be executed.

## Operational nonauthorization

Decision0226 does not authorize:

- actual accounting-evidence acquisition;
- actual U/C domain acquisition;
- actual domain freeze;
- forward or reverse witness acquisition;
- concrete source-to-carrier mapping;
- accounting-satisfaction determination;
- pair reclassification;
- active Schema-V2 modification;
- analyzer implementation or execution;
- baseline execution;
- repair implementation or execution;
- governance adoption.

## Current status

`CORRECTIVE_SUCCESSOR_APPROVED=NO`

`GOVERNANCE_ADOPTED=NO`

`ACTUAL_CORRECTIVE_SUCCESSOR_AUTHORED=NO`
