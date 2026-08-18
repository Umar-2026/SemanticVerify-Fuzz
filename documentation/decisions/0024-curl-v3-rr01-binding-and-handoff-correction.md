# Decision 0024: curl V3 RR01 Binding and External-Handoff Correction

Status: Author-side immutable successor/correction record; independent human
re-review required before any curl V3 scope freeze.

Date: 2026-08-18

## Purpose

This decision records the minimal immutable correction path required by the
completed independent human review of the exact curl V3 source-only
authoring-scope successor.

This decision does **not** modify the exact V3 scope bytes.

This decision does **not** modify Decision 0023 in place.

This decision does **not** authorize curl V3 scope freeze.

This decision does **not** authorize technical protocol working-draft
authoring, canonical specification finalization, generated-driver inspection,
gold annotation, analyzer implementation/execution, baseline execution, or
repair.

## Exact V3 scope remains unchanged

The exact immutable V3 scope remains:

- Path: `config/annotation/curl_v3_authoring_scope.v3.json`
- SHA-256: `ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`
- Author checkpoint commit: `7de6fc01797ae68cbd64406b850a3198f71cc702`
- Author checkpoint tree: `c5f96b844e5803cccd04c9f64a55754dc6c77e20`
- Git blob: `931c24cc46c99f23ee352455d3e8c93e57e63401`

The locally verified Git relation is:

`7de6fc01797ae68cbd64406b850a3198f71cc702`

→ tree

`c5f96b844e5803cccd04c9f64a55754dc6c77e20`

→ path `config/annotation/curl_v3_authoring_scope.v3.json`

→ blob

`931c24cc46c99f23ee352455d3e8c93e57e63401`

→ SHA-256

`ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`

The V3 scope is not edited in place.

## Exact V2 predecessor remains unchanged

The exact immutable V2 predecessor remains:

- Path: `config/annotation/curl_v2_authoring_scope.v2.json`
- SHA-256: `f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df`
- Author checkpoint commit: `fae56e4f5196fd0460046723ef9d6a4e26234612`
- Author checkpoint tree: `0cb044dd10d48908895425512f5a2e7c1e8633b9`

V2 remains immutable.

## Decision 0023 historical record

Decision 0023 remains preserved at:

`documentation/decisions/0023-curl-v3-rr07-authorization-boundary-successor.md`

SHA-256:

`c774bb667930ef9ceaedc5ca5d25e88d57da3ffefa10de639ef6a20f7d2271d1`

Decision 0023 contains one malformed duplicate predecessor-SHA label line:

`- SHA-256: $ config/annotation/curl_v2_authoring_scope.v2.json`

The immediately following line contains the actual correct V2 SHA-256.

Decision 0023 MUST NOT be edited in place.

For RR01 provenance/binding purposes, this Decision 0024 supersedes Decision
0023's malformed predecessor-SHA presentation while preserving Decision 0023
as immutable historical evidence.

The correct V2 predecessor binding is exactly:

- Path: `config/annotation/curl_v2_authoring_scope.v2.json`
- SHA-256: `f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df`

No protocol semantic statement from the exact V3 scope is changed by this
correction.

## Completed V3 independent human review

The completed review is preserved at:

`evidence/annotation_preparation/curl_v3_authoring_scope_successor/human_review_v3/01_completed_human_review.v3.md`

SHA-256:

`3e77a9456d49ccd0001ad839b1e2a32478d45a05cc94b0ba115cdd667a45afb9`

Repository review-record commit:

`713587c654f9c24f8fd3e7a3b3ad3638ec81a6fe`

Repository review-record tree:

`c1bebcd5a2e46ee3c00917e23571aac5074dd603`

The governing review outcome is:

- V3-RR01: `REVISION_REQUIRED`
- V3-RR02: `PASS`
- V3-RR03: `PASS`
- V3-RR04: `PASS`
- Overall: `REVISION_REQUIRED`

The reviewer confirmed that the V3 RR07 authorization-boundary correction is
correct, V2-RR01 through V2-RR06 semantics remain preserved, and downstream
activities remain unauthorized.

## RR01 blocker A: independently resolvable Git evidence

The first remaining RR01 blocker is external verifiability of the claimed V3
author commit/tree/blob chain.

The next corrected external handoff MUST therefore contain independently
resolvable Git object evidence sufficient for the independent reviewer to
verify:

1. author commit `7de6fc01797ae68cbd64406b850a3198f71cc702`;
2. its root tree `c5f96b844e5803cccd04c9f64a55754dc6c77e20`;
3. path `config/annotation/curl_v3_authoring_scope.v3.json`;
4. target Git blob `931c24cc46c99f23ee352455d3e8c93e57e63401`;
5. target SHA-256 `ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`.

The evidence mechanism must be independently usable outside the research
working repository.

A Git bundle or another self-contained Git-object representation may be used
only if it preserves the review quarantine and exposes no prohibited
generated-driver, gold-label, analyzer-output, baseline-output, LLM-review,
or repair evidence.

## RR01 blocker B: corrected Decision 0023 provenance

This Decision 0024 is the immutable successor/correction record for the
malformed Decision 0023 predecessor-SHA presentation.

The corrected external handoff MUST include both:

- immutable historical Decision 0023; and
- this immutable Decision 0024 correction record.

The reviewer must be able to verify that Decision 0023 itself was not edited.

## Why V4 is not selected at this boundary

The completed human review passed V3-RR02, V3-RR03, and V3-RR04.

The subsequent repository inspection also confirmed that the exact V3
commit/tree/blob/SHA chain resolves locally and that the identified Decision
0023 defect is outside the V3 scope JSON.

Therefore the selected minimal correction path does not create a V4 scope
successor at this boundary.

This is not a human approval decision.

If the independent human re-review determines that the corrected immutable
Decision 0024 plus independently resolvable Git evidence is insufficient, no
scope freeze may occur and a V4 successor or other reviewer-required immutable
correction must be created.

## Required re-review boundary

A corrected external handoff must be prepared for independent human re-review
of the previously blocking V3-RR01 evidence.

The re-review must verify:

1. exact V3 SHA-256 and Git blob;
2. independently resolvable author commit → tree → path → blob relation;
3. exact immutable V2 predecessor;
4. immutable Decision 0023;
5. this Decision 0024 correction record;
6. completed prior V3 review;
7. continued preservation of the source-only quarantine.

No assistant-synthesized approval is allowed.

## Current authorization state

At creation of Decision 0024:

- V3 human review completed: YES, with overall `REVISION_REQUIRED`;
- V3 scope freeze authorized: NO;
- V3 scope frozen: NO;
- technical working-draft authoring authorized: NO;
- canonical curl specification authorized: NO;
- generated-driver inspection authorized: NO;
- gold annotation authorized: NO;
- analyzer implementation/execution authorized: NO;
- baseline execution authorized: NO;
- repair authorized: NO.

## Next boundary

Prepare a corrected immutable V3 RR01 external re-review handoff containing
Decision 0024 and independently resolvable, quarantine-safe Git binding
evidence.

Do not freeze V3 and do not begin technical working-draft authoring before a
real independent human reviewer resolves the blocking RR01 re-review.
