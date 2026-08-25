# CWXR07-S2 Independent Human-Review Instructions

## Scope

Review only `CWXR07-S2`.

Do not reopen CWXR01–CWXR06 or CWXR08.

Do not reinterpret, replace, overwrite, or upgrade the completed CWXR07-S1 review.

Historical CWXR07-S1 remains:

`REVISION_REQUIRED`

## Review question

Determine whether the supplied CWXR07-S2 package satisfies only the following bounded criterion:

1. supplied-file byte integrity;
2. checksum-closure integrity;
3. internal consistency of the preserved Decision-0147 A02 script/output/consumption-record bindings;
4. internal consistency among supplied preserved repository-record assertions;
5. consistency of bounded-claim language with the evidence actually supplied.

For this review, internal consistency means absence of contradiction among the supplied preserved files and assertions within the bounded package.

It does not mean independent reproduction of underlying Git, repository, or runtime facts.

## Explicit exclusions

A CWXR07-S2 PASS must not be interpreted as independent proof of:

1. Decision-0147 → Decision-0148 Git parentage;
2. Decision-0148 Study V1 tree identity;
3. tracked Decision-0147 A02 path-history correctness;
4. repository contradiction-search correctness or completeness;
5. an externally observed actual-process exactly-once execution fact;
6. a global no-rerun fact.

Historical assertions concerning these subjects are included only as preserved provenance.

## PASS meaning

A PASS means only that the supplied package satisfies the five bounded CWXR07-S2 positive-scope requirements.

A PASS does not retroactively change CWXR07-S1 from `REVISION_REQUIRED` to PASS.

A PASS does not itself authorize governance adoption, analyzer implementation, baseline execution, or repair.

## Reviewer decision

Choose exactly one:

`PASS`

`REVISION_REQUIRED`

`FAIL`

Complete only the reviewer-completion fields in the supplied editable reviewer packet.

Reviewer identity, decision, notes, attestation, and date must be provided by the genuine independent human reviewer and must not be supplied or inferred by the authors.
