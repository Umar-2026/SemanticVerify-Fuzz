# CWXR07-S2 — Narrowed Corrective Successor Criterion

## Status

`AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW`

## Historical boundary

CWXR07-S1 remains `REVISION_REQUIRED`.

CWXR07-S2 is a new narrowed corrective successor criterion. It does not rewrite, replace, upgrade, or retroactively approve CWXR07-S1.

CWXR01–CWXR06 and CWXR08 are not reopened.

## Corrective basis

The independent CWXR07-S1 reviewer supplied two corrective alternatives.

This successor follows reviewer option 2:

`FURTHER_NARROW_CWXR07_S1_TO_BYTE_INTEGRITY_AND_INTERNAL_CONSISTENCY`

No sealed Git bundle or full repository snapshot is part of CWXR07-S2.

## Positive review scope

An independent reviewer evaluating CWXR07-S2 shall determine only whether the supplied successor package establishes:

1. supplied-file byte integrity;
2. checksum-closure integrity;
3. internal consistency of the preserved Decision-0147 A02 script/output/consumption-record bindings;
4. internal consistency among the supplied preserved repository-record assertions;
5. consistency of the bounded-claim language with the evidence actually supplied.

For item 4, "internal consistency" means only that the supplied preserved assertions and bindings do not contradict one another within the bounded package. It does not mean that the underlying repository or runtime facts have been independently reproduced.

## Explicit exclusions

CWXR07-S2 does not require, establish, or permit a PASS to certify independent proof of:

1. Decision-0147 → Decision-0148 Git parentage;
2. Decision-0148 Study V1 tree identity;
3. tracked Decision-0147 A02 path-history correctness;
4. repository contradiction-search correctness or completeness;
5. an externally observed actual-process exactly-once execution fact;
6. a global no-rerun fact.

Historical records concerning these subjects may be preserved as provenance. Their preservation does not promote them to independently established facts.

## PASS meaning

A `PASS` on CWXR07-S2 certifies only that the supplied files satisfy the five positive-scope requirements above.

A `PASS` on CWXR07-S2 does not convert CWXR07-S1 from `REVISION_REQUIRED` to `PASS`.

A `PASS` on CWXR07-S2 does not by itself authorize governance adoption, analyzer implementation, baseline execution, or repair.

## Allowed independent-review decision

Choose exactly one:

`PASS`

`REVISION_REQUIRED`

`FAIL`

## Human-review requirement

CWXR07-S2 requires a new genuine independent human review.

No reviewer identity, reviewer decision, PASS, or approval is pre-populated by this author candidate.
