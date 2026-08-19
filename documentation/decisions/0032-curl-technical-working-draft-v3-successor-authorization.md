# Decision 0032 — Authorize curl Technical Working Draft V3 Successor

## Status

Authorized for successor authoring only.

This decision does not create the V3 working draft.

## Predecessor

Working Draft V2:

`config/annotation/curl_technical_protocol_working_draft.v2.json`

SHA-256:

`63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31`

Completed V2 human-review commit:

`96b5ff417206fa2f1fe9e8e5c9d499561d4e6d7b`

Completed V2 human-review tree:

`6c8304aa228019c2a1d5cfe2cc4af856843ba6cd`

Completed human-review SHA-256:

`597699068c3ba7bf480204c67d88d940f400c7425442a081a18198908b1e029e`

Overall decision:

`REVISION_REQUIRED`

## Authorized successor target

The following new file may be authored after this authorization:

`config/annotation/curl_technical_protocol_working_draft.v3.json`

Expected schema ID:

`curl.technical-protocol-working-draft.v3`

Working Draft V2 must not be edited in place.

## Authorized correction scope

Only the bounded corrections required by:

- V2-RR05
- V2-RR06
- V2-RR09
- V2-RR10
- V2-RR12

may alter successor semantics.

The successor must:

1. add D1 handling for invalid easy arguments to
   `curl_multi_add_handle` and `curl_multi_remove_handle`;
2. add D2 handling for NULL failed-`curl_easy_init` arguments to those
   functions, including `CURLM_BAD_EASY_HANDLE` and no membership change;
3. resolve stale explicit-global-cleanup normative metadata;
4. resolve stale operative E04 review-required metadata;
5. preserve the two-state NULL `curl_easy_init` post-state and feasible-state
   verdict joins;
6. constrain M10 to a live valid supplied multi and a live detached easy;
7. constrain M11 to a live valid supplied multi and a live easy associated
   with a different original multi while preserving D7 semantics;
8. provide exact successor-bound rule-to-source traceability.

## Required preserved boundaries

The frozen twelve-function curl API surface remains unchanged.

The pinned curl source revision remains unchanged.

The frozen source-only scope remains unchanged.

The approved evidence class remains:

`PREAPPROVED_SOURCE_ONLY`

The same 21 approved pinned source files remain the technical evidence set.

The machine verdict set remains exactly:

- `VALID`
- `VIOLATION-MUST`
- `VIOLATION-MAY`
- `UNKNOWN`

No synthetic protocol event may be invented.

## Prohibited evidence

The successor author must not use:

- generated-driver source;
- selected-sample membership;
- raw model responses;
- generated-driver compiler-log semantic content;
- gold labels;
- analyzer output;
- baseline output;
- LLM-review output;
- repair output.

## Explicit non-authorization

This decision does not authorize canonical `curl.json`.

This decision does not authorize generated-driver inspection.

This decision does not authorize selected-sample membership inspection.

This decision does not authorize gold annotation.

This decision does not authorize analyzer implementation or execution.

This decision does not authorize baseline execution.

This decision does not authorize repair.

## Required next checkpoint

After V3 is authored, it must receive a separate author checkpoint with:

- exact V3 SHA-256;
- exact bounded-diff verification against immutable V2;
- verification of all eight required corrections;
- verification that preserved PASS findings remain unchanged;
- exact V3-bound source traceability;
- confirmation that no prohibited evidence class was used.

Only after that checkpoint may a new independent V3 human technical-review
package be considered.

## Next boundary

`AUTHOR_CURL_TECHNICAL_WORKING_DRAFT_V3_SUCCESSOR`
