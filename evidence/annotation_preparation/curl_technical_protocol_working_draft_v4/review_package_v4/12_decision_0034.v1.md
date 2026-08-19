# Decision 0034 — curl Technical Working Draft V3 Human Review: Revision Required

## Status

Completed independent human technical review recorded.

Overall decision:

`REVISION_REQUIRED`

## Exact reviewed V3

Path:

`config/annotation/curl_technical_protocol_working_draft.v3.json`

SHA-256:

`2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2`

Size:

`41330` bytes

Author-checkpoint commit:

`d4c41e682882f6053fd6657a7f0f82a402697354`

Immutable review-package commit:

`eba2cd1766a08d6021999260e508664b415bad30`

Immutable review-package tree:

`34e6de3a5563f5c89634e6f7f0cbcd9053715678`

## Exact completed human review

Recorded repository path:

`evidence/annotation_preparation/curl_technical_protocol_working_draft_v3/completed_human_review_v3/01_completed_human_technical_review.v3.md`

SHA-256:

`9a15b13cea29bcbcbfff349c9b9bcb113a9d9a4e01afe03727d7be8dbd87c327`

Size:

`22983` bytes

Reviewer role:

`Spec-Technical-Reviewer-1`

Human reviewer:

`Abdul Raheem Shahzad`

Recorded confirmation:

`ARS`

Review date:

`19 / August / 2026`

## Item-level decisions

PASS:

- V3-RR01
- V3-RR03
- V3-RR04
- V3-RR05
- V3-RR06
- V3-RR07
- V3-RR08
- V3-RR09
- V3-RR10
- V3-RR11

REVISION_REQUIRED:

- V3-RR02
- V3-RR12

FAIL:

- none

Decision distribution:

`10 PASS / 2 REVISION_REQUIRED / 0 FAIL`

## Technical interpretation

The independent reviewer accepted the substantive protocol-rule corrections
covered by V3-RR03 through V3-RR11.

The new successor must therefore preserve those verified protocol semantics.

Revision is required because exact V3 contains stale internal successor and
governance metadata inherited from earlier V1/V2 boundaries.

The required successor must correct, among other version-specific metadata:

- internal purpose text;
- `governance.working_draft_version`;
- predecessor version/path/SHA binding;
- completed-review binding;
- successor-authorization binding;
- stale `v1_in_place_edit_authorized` naming;
- version-specific `explicit_non_claims`;
- internal successor-resolution metadata.

V3-RR12 also identified a review-package portability issue: source-path
comparison is not platform-independent. The Windows failure is attributed to
backslash-versus-forward-slash path representation, while normalized manual
comparison confirms the same approved 21 source paths and hashes.

A successor review package must therefore implement platform-independent path
comparison without changing the approved source evidence set or semantics.

## Immutable-successor rule

Exact V3 must remain immutable.

Do not edit V3 in place.

A new immutable V4 successor requires a separate explicit authorization before
authoring.

The successor may correct only the review-required metadata/governance and
review-package portability issues while preserving the accepted protocol-rule
semantics and existing evidence boundaries.

## Explicit non-authorization

Canonical `curl.json` is not authorized.

Generated-driver inspection is not authorized.

Selected-sample membership inspection is not authorized.

Gold annotation is not authorized.

Analyzer implementation or execution is not authorized.

Baseline execution is not authorized.

Repair is not authorized.

## Next boundary

`AUTHORIZE_CURL_TECHNICAL_WORKING_DRAFT_V4_SUCCESSOR`
