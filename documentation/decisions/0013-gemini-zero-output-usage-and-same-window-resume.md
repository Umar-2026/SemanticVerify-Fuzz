# Decision 0013: Gemini zero-output usage normalization and governed same-window resume

- Status: Accepted
- Recorded at UTC: 2026-08-09T17:11:59+00:00
- Primary window: `SVF-PRIMARY-800-V1`
- Pause sequence: `0001`
- Pause-freeze commit: `25931bfe3f479bdde49a4da2d6731d152a929c41`
- Pause-freeze tree: `b85f1d7e305cb69599ec26c6ad73f3aba450010e`

## 1. Context

The first primary generation window was opened once and remains the same
experimental window. Execution stopped after logical slot 0472 under the
frozen pause-before-next-call rule.

The triggering slot is
`SVF-PRIMARY-800-V1-SLOT-0472`.

The preserved invocation had:

- HTTP status `200`;
- returned model/version `gemini-3.1-flash-lite`;
- frozen request-body hash verification `true`;
- terminal response classification `REFUSAL`;
- `promptTokenCount = 177`;
- `totalTokenCount = 177`;
- no serialized `candidatesTokenCount`;
- no serialized `thoughtsTokenCount`;
- no serialized `cachedContentTokenCount`;
- frozen cost-accounting result `PAUSE_REQUIRED`;
- pause reason `INVALID_USAGE_METADATA`.

The triggering response, invocation ledger, postprocessing record and pause
record remain immutable.

## 2. Root cause

The frozen Gemini cost rule required both `promptTokenCount` and
`candidatesTokenCount` to be serialized.

That requirement is stricter than needed for the observed zero-output refusal
case.

Google's Gemini GenerateContent API documents that a blocked prompt can return
no candidates and defines `candidatesTokenCount` as the total token count
across generated response candidates.

ProtoJSON permits default-valued scalar fields without explicit presence to be
omitted from JSON serialization.

Accordingly, the missing field is not treated generally as proof of malformed
usage. Instead this project adopts the narrow deterministic normalization
defined below.

Authoritative external references used for this resolution:

- https://ai.google.dev/api/generate-content
- https://protobuf.dev/programming-guides/json/

These references motivate the rule but do not alter preserved provider bytes.

## 3. Narrow Gemini zero-output normalization

For Model B only, a missing `candidatesTokenCount` may be normalized to zero
for cost estimation only when every condition below holds:

1. a complete HTTP 2xx response was preserved;
2. the frozen response parser classified the result as terminal `REFUSAL`;
3. `usageMetadata` is present as an object;
4. `promptTokenCount` is a non-negative integer;
5. `candidatesTokenCount` is absent;
6. `thoughtsTokenCount` is absent or a non-negative integer;
7. `cachedContentTokenCount` is absent or zero;
8. `toolUsePromptTokenCount`, if present, is zero;
9. `totalTokenCount` is a non-negative integer; and
10. `totalTokenCount == promptTokenCount + thoughtsTokenCount_or_zero`.

When all conditions hold:

- `candidatesTokenCount_for_cost = 0`;
- absent `thoughtsTokenCount` remains zero under the already-frozen rule;
- absent `cachedContentTokenCount` remains zero;
- the cost-estimate basis is recorded as
  `DERIVED_ZERO_CANDIDATE_REFUSAL_TOKEN_BALANCE`;
- provider response bytes and original usage metadata are not modified.

If any condition fails, the existing preserve-and-pause behavior remains.

This amendment changes cost interpretation only. It does not change response
classification, terminal-status precedence, retry semantics, request bytes,
model targets, thinking controls, extraction, duplicate detection or
compilation semantics.

## 4. Slot 0472 treatment

Slot 0472 is not retried, replaced, regenerated or reclassified.

Its original invocation ledger remains unchanged with
`cost_estimate_status = PAUSE_REQUIRED`.

An additive resolution record may state the governed derived cost estimate:

- prompt tokens: `177`;
- candidate tokens for cost: `0`;
- thinking tokens for cost: `0`;
- cached-content tokens: `0`;
- Standard-paid Gemini input rate: `0.25 USD / 1M tokens`;
- Standard-paid output-including-thinking rate: `1.5 USD / 1M tokens`;
- derived estimate: `0.00004425 USD`.

The original ledger remains the historical record of why execution paused.

## 5. Same-window continuation

Any later continuation remains within `SVF-PRIMARY-800-V1`.

It is not a second primary window.

The existing `window/open.json` is retained and no second open record may be
created.

The governed continuation boundary is:

- already terminal: slots `0001` through `0472`;
- first eligible continuation slot: `0473`;
- final planned slot: `0800`;
- remaining logical slots: `328`.

Slots `0001` through `0472` must never be replayed.

Slot `0472` must never be retried.

Provider-neutral descriptors, rendered prompts, exact provider request bodies,
model pairing, scenario order and replicate order remain those of the frozen
800-slot request plan.

## 6. State reconstruction before continuation

A resume implementation must reconstruct state mechanically from frozen
evidence without human inspection of generated driver contents.

Before slot 0473 it must verify:

1. the pause-freeze commit is an ancestor of the execution HEAD;
2. all 4115 pause-freeze package entries verify;
3. slots 0001--0472 are contiguous and terminal;
4. all prior invocation and postprocessing records required by the freeze are
   present;
5. pause sequence 0001 remains unchanged with zero calls after pause;
6. no slot 0473 or later primary artifact already exists;
7. `window/close.json` is absent;
8. repository state satisfies the resume authorization contract;
9. both provider capabilities have been freshly requalified;
10. exact frozen compiler/library artifacts still verify.

Duplicate-state reconstruction must preserve the original duplicate authority:
within the same requested model ID, library and scenario, the earliest
successfully extracted exact driver-source bytes remain canonical. Prior
driver bytes may be read mechanically for hashing/comparison but must not be
human-inspected.

Provider-specific consecutive-service-error state must also be reconstructed
or independently proven at the pause boundary before any resumed provider
call.

## 7. Further pauses

The next pause, if any, must use append-only `pause-0002.json`; prior pause
records must not be overwritten.

No provider call may occur after a new pause until another governed resolution
is committed.

## 8. Completion

Only after all 800 logical slots have terminal records may the existing window
receive its single append-only `window/close.json`.

Completion must count the already frozen 472 terminal slots plus the 328
continuation slots.

## 9. Implementation boundary

This decision does not itself authorize resume or any live provider call.

The frozen fresh-window runner and its historical contract remain immutable.

A separate additive same-window resume contract and resume implementation must
be created, provider-free qualified, frozen and committed.

After that implementation freeze:

1. fresh provider capability requalification must pass and be committed;
2. a separate explicit resume-authorization record must be committed;
3. operational resume authorization must pass before secrets are read;
4. continuation may then begin at slot 0473 only.

## 10. Separation

This decision authorizes no analyzer implementation or execution, no repair,
no human inspection of generated driver contents, and no execution of linked
generated drivers.

The verification-first boundary remains unchanged.
