# Decision 0031 — curl Technical Working Draft V2 Human Review: Revision Required

## Status

Completed independent human technical review recorded.

Overall human-review decision:

`REVISION_REQUIRED`

## Exact reviewed working draft

Path:

`config/annotation/curl_technical_protocol_working_draft.v2.json`

SHA-256:

`63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31`

V2 author checkpoint commit:

`a9042429155a161bd5c089910e7557b907808db6`

Immutable V2 review-package commit:

`d987d39dbaaafa4ce5883b0655375e6c495bffd5`

Immutable V2 review-package tree:

`2865e1ffc414febf5694b16c5620c47d15f046d5`

## Exact completed human review

Recorded repository path:

`evidence/annotation_preparation/curl_technical_protocol_working_draft_v2/completed_human_review_v2/01_completed_human_technical_review.v2.md`

SHA-256:

`597699068c3ba7bf480204c67d88d940f400c7425442a081a18198908b1e029e`

Size:

`37832` bytes

Reviewer role:

`Spec-Technical-Reviewer-1`

Human reviewer:

`Abdul Raheem Shahzad`

Recorded confirmation:

`ARS`

Review date:

`19 / August / 2026`

## Item-level decision summary

PASS:

- V2-RR01
- V2-RR02
- V2-RR03
- V2-RR04
- V2-RR07
- V2-RR08
- V2-RR11

REVISION_REQUIRED:

- V2-RR05
- V2-RR06
- V2-RR09
- V2-RR10
- V2-RR12

FAIL:

- none

Decision distribution:

`7 PASS / 5 REVISION_REQUIRED / 0 FAIL`

## Required successor boundary

Working Draft V2 is not approved for canonicalization.

Working Draft V2 must remain immutable.

A new immutable technical-working-draft successor is required.

The successor must implement the bounded corrections specified by the completed
human review, including:

- D1/D2 coverage for invalid easy arguments to `curl_multi_add_handle` and
  `curl_multi_remove_handle`;
- `CURLM_BAD_EASY_HANDLE` and no-membership-change behavior for those cases;
- resolution of stale explicit-global-cleanup normative metadata;
- resolution of stale operative E04 review-required metadata;
- preservation of the two-state NULL `curl_easy_init` result and verdict joins;
- live-valid supplied-multi preconditions for M10 and M11;
- preservation of M11 D7 `VIOLATION-MUST` semantics;
- successor-bound rule-to-source traceability.

## Evidence boundary

No new evidence class is authorized.

Generated-driver source remains unavailable for technical-specification
authoring.

Selected-sample membership remains unavailable.

Gold annotations remain unavailable.

Analyzer output remains unavailable.

Baseline output remains unavailable.

LLM-review output remains unavailable.

Repair output remains unavailable.

## Explicit non-authorization

Canonical `curl.json` is not authorized.

Generated-driver inspection is not authorized.

Selected-sample membership inspection is not authorized.

Gold annotation is not authorized.

Analyzer implementation or execution is not authorized.

Baseline execution is not authorized.

Repair is not authorized.

## Next boundary

`AUTHORIZE_CURL_TECHNICAL_WORKING_DRAFT_V3_SUCCESSOR`
