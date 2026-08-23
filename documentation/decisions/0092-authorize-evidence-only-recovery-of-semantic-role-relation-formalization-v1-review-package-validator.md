# Decision 0092 — Authorize Evidence-Only Recovery of Semantic-Role Relation Formalization V1 Review-Package Validator

Status: VALIDATOR RECOVERY AUTHORIZED — PACKAGE FINALIZATION NOT YET COMPLETE

## Failure context

Decision 0091 authorized creation of Independent Human Technical Review
Package V1.

Its pre-review-package authorization verifier ran its final allowed time,
returned PASS, and is permanently retired.

The Review Package V1 artifacts were then authored.

Before package commit, the newly authored safe package validator failed with:

`FAIL|PACKET_ITEM_DECISION_NOT_BLANK`

No Decision-0092 package checkpoint had yet been created.

The partially authored package was preserved rather than deleted because the
Decision-0091 pre-package verifier had already been consumed.

## Root-cause diagnosis

Independent line-based inspection confirms:

- SRR01 through SRR08 decision fields are actually blank;
- the overall human decision is actually blank;
- human reviewer name is blank;
- human reviewer confirmation/signature is blank; and
- human reviewer date is blank.

The failure is caused by the package validator's use of:

`\s*`

at line tails.

In Python regular expressions, `\s` includes newline characters. The
validator therefore consumes the newline following a blank Decision field
and captures:

`Reviewer notes:`

as though it were the Decision value.

Using horizontal-whitespace-only matching:

`[ \t]*`

correctly returns an empty decision value.

Therefore the defect is a validator-only defect, not a reviewer-packet
semantic defect.

## Preserved pre-recovery evidence

Blank reviewer packet SHA-256:

`84aa233232268866aaf9a5b8db673ed1c42e0519c7231162dece7f53a7c4ad3b`

Buggy package validator SHA-256:

`0148c69a7b76190fcb52e05b6c4fcffbddd7316b1dabfcb2a493c6042b3b5bf4`

Package manifest SHA-256:

`ae8e4af6affc156e7774b61d9a360a9b630034b6d25f2fe37d620cf6c73e2ba5`

Pre-recovery checksum-manifest SHA-256:

`a4de27038a599505768f78dfb48041d3701fa5d15fc2111850734d5f5259df99`

Decision-0091 consumption-marker SHA-256:

`2ea22aedeca53f2e372ef938e468b60be8bf13a41dac995ec76eec95063566ee`

The Decision-0091 pre-review-package verifier remains permanently retired
and must never be rerun.

## Authorized recovery

Decision 0092 authorizes only:

1. evidence-only correction of
   `16_verify_semantic_role_relation_formalization_v1_review_package.v1.py`
   so line-tail blank-field validation uses horizontal whitespace rather
   than newline-consuming whitespace; and

2. regeneration of
   `18_semantic_role_relation_formalization_v1_review_package.v1.SHA256SUMS`
   solely to bind the corrected validator bytes.

Files 01 through 15 must remain byte-exact.

File 17 must remain byte-exact.

In particular, the immutable blank reviewer packet must not be edited.

## Required recovery result

After the correction:

- the safe package validator must PASS;
- the package checksum manifest must PASS;
- SRR01 through SRR08 must remain blank;
- the overall human decision must remain blank;
- reviewer identity fields must remain blank;
- Formalization V1 remains AUTHOR_CANDIDATE;
- PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED remains not human-approved.

## Recovery authorization verifier lifecycle

The Decision-0092 recovery verifier is pre-validator-recovery only.

It may run while P16 and P18 remain at their diagnosed pre-recovery hashes.

It must run its final allowed time immediately before P16/P18 correction.

After correction begins, the recovery verifier is permanently retired and
must never be rerun.

## Explicit non-authorizations

Decision 0092 does not authorize:

- rerunning the Decision-0091 pre-review-package verifier;
- editing the blank human reviewer packet;
- editing review scope or exact-copy evidence;
- editing the package manifest;
- creating or synthesizing a human review decision;
- prepopulating reviewer identity;
- approving Formalization V1;
- approving PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED;
- exhaustive admissible-composition enumeration;
- constructive positive mapping-witness authoring;
- operational V4-to-V2 or V4-to-successor mapping;
- active Schema-V2 modification;
- schema-successor authoring;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## Next boundary

Run the Decision-0092 recovery verifier its final allowed time, correct only
P16, regenerate only P18, safely validate Review Package V1, and record the
recovered immutable package as Decision 0093.
