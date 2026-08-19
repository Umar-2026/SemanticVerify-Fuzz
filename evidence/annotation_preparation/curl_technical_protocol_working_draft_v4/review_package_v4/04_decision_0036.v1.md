# Decision 0036 — curl Technical Working Draft V4 Author Checkpoint

## Status

Working Draft V4 reached its immutable metadata-successor author checkpoint.

The earlier checkpoint attempt failed only because the pre-authoring-only V4
authorization verifier was reused after V4 legitimately existed. This
checkpoint uses stage-correct authorization-record validation and does not
reuse that V4-absence assertion.

## Exact V4 checkpoint

Path:

`config/annotation/curl_technical_protocol_working_draft.v4.json`

SHA-256:

`e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8`

Size:

`41033` bytes

Status:

`SOURCE_ONLY_TECHNICAL_WORKING_DRAFT_V4_AUTHOR_CHECKPOINT`

## Immutable predecessor

Exact V3 SHA-256:

`2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2`

V3 remains immutable.

## Review basis

Completed V3 independent human review:

`REVISION_REQUIRED`

Revision-required items:

- V3-RR02
- V3-RR12

V4 implements metadata corrections V4-C01 through V4-C06.

## Protocol preservation

All 10 protocol containers are preserved exactly in JSON semantics from V3.

Easy-handle rules: `21`

Multi-handle rules: `29`

New protocol rules: `0`

Removed protocol rules: `0`

Protocol-rule semantic change: `NONE`

## Remaining V4 review-package work

V4-P01 remains pending: implement platform-independent logical relative
source-path comparison in the V4 independent-review-package verifier.

V4-P02 remains pending: create a fresh exact V4-bound independent-review
package, manifest, verifier, checksums, and human-review packet.

Evidence class remains `PREAPPROVED_SOURCE_ONLY`.

Approved source-file count remains `21`.

## Non-authorization

Canonical `curl.json` is not authorized.

Generated-driver inspection is not authorized.

Selected-sample membership inspection is not authorized.

Gold annotation is not authorized.

Analyzer implementation or execution is not authorized.

Baseline execution is not authorized.

Repair is not authorized.

## Next boundary

`BUILD_INDEPENDENT_CURL_TECHNICAL_WORKING_DRAFT_V4_REVIEW_PACKAGE`
