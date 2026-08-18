# Decision 0030 — curl Technical Working Draft V2 Successor Author Checkpoint

## Status

Author checkpoint created.

## Predecessor

Working Draft V1 remains immutable.

V1 SHA-256:

`80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6`

V1 completed independent human technical review:

`REVISION_REQUIRED`

Completed human-review SHA-256:

`e253340d540a06cd24af501c569154869ac0324d677995b7266349ba097973cc`

V2 successor authorization commit:

`eba1cb67f5a7c6b2ea8348634f397204a2bbb0d3`

## Exact V2 author target

Path:

`config/annotation/curl_technical_protocol_working_draft.v2.json`

SHA-256:

`63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31`

## Human-review corrections implemented

The V2 successor implements the bounded corrections required by
TS-RR05 through TS-RR14.

These include:

- return-conditioned `curl_multi_cleanup`;
- failed-cleanup conservative state and outstanding cleanup obligation;
- exactly four machine-readable verdicts;
- explicit D1, D2, and cleanup-specific D4 mappings;
- D5 `VIOLATION-MUST` for outstanding explicit global cleanup at exit;
- non-enforceable multi-cleanup ordering recommendation;
- D6 `VIOLATION-MUST` for plain post-error multi-perform repetition;
- explicit complete remove-and-re-add recovery;
- feasible-state verdict joins for the NULL `curl_easy_init` state set;
- D7 `VIOLATION-MUST` for wrong-multi removal;
- state-sensitive D8 `VIOLATION-MUST` for final-reference global cleanup
  while modeled resources remain live.

## Frozen boundaries

The twelve-function curl API surface is unchanged.

The pinned curl revision is unchanged.

The frozen V3 source-only scope is unchanged.

The authoritative scenario manifest is unchanged.

The approved source-evidence class is unchanged.

Working Draft V1 was not edited in place.

## Explicit non-authorization

This author checkpoint does not approve Working Draft V2.

It does not authorize canonical `curl.json`.

It does not authorize generated-driver inspection.

It does not authorize selected-sample membership inspection.

It does not authorize gold annotation.

It does not authorize analyzer implementation or execution.

It does not authorize baseline execution.

It does not authorize repair.

The exact V2 successor requires a new independent human technical review.

## Next boundary

`BUILD_CURL_TECHNICAL_WORKING_DRAFT_V2_INDEPENDENT_REVIEW_PACKAGE`
