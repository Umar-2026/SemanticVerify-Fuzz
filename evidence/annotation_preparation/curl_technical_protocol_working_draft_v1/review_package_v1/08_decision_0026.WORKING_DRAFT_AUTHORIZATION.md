# Decision 0026: curl V3 Post-Freeze Technical Working-Draft Authorization

## Status

Technical curl protocol working-draft authoring is authorized after completion
of the separately approved and recorded exact curl V3 source-only
authoring-scope freeze.

This is a working-draft authorization only.

It is **not** canonical protocol-specification approval.

## Frozen scope prerequisite

Exact frozen V3 scope:

- Path: `config/annotation/curl_v3_authoring_scope.v3.json`
- SHA-256: `ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`
- Original author checkpoint commit: `7de6fc01797ae68cbd64406b850a3198f71cc702`
- Original author checkpoint tree: `c5f96b844e5803cccd04c9f64a55754dc6c77e20`
- Git blob: `931c24cc46c99f23ee352455d3e8c93e57e63401`

The separate scope freeze was committed at:

`0992b2ae03702e29471d59f192daf43a8924314d`

with tree:

`4ed8c5c1d8936eff6c9da44aee69371f0c9d4e7a`

Decision 0025 SHA-256:

`235066254503cc0729fbbf66bd640ee7042b549b9df9e26c7c6f53ee3b90937c`

The exact V3 scope remains byte-identical and MUST NOT be edited in place.

## Authorization rationale

The V3 governance sequence requires:

1. independent human review;
2. human approval for the separate scope-freeze step;
3. completed exact V3 scope freeze;
4. only then authorization of technical working-draft authoring.

Steps 1 through 3 are now complete.

Therefore technical curl protocol working-draft authoring may now begin from
the exact frozen V3 scope and its already approved source evidence.

## Authorized activity

Authorized:

- author the curl technical protocol **working draft**;
- formalize the frozen twelve-function surface into resource states,
  obligations, transitions, return-conditioned transitions, ownership rules,
  cleanup constraints, and uncertainty semantics;
- use only the already approved source evidence and frozen V3 scope as the
  evidentiary basis;
- create author-side validation artifacts for that technical working draft.

## Still prohibited

This authorization does NOT authorize:

- declaring the technical working draft canonical;
- bypassing the separate independent human technical-specification review;
- generated-driver source inspection;
- selected-sample membership use as protocol evidence;
- raw model-response inspection;
- compiler-log semantic inspection from generated drivers;
- gold-label inspection or annotation;
- analyzer implementation or execution;
- baseline execution;
- controlled LLM-review output use;
- repair implementation or repair-output inspection.

## Required technical-review boundary

The technical working draft must receive its own independent human review
before any canonical `curl.json` protocol specification is finalized.

A failure or revision request at that boundary requires an immutable successor
or correction according to the applicable governance rules.

## Current authorization state

After Decision 0026:

- V3 scope freeze authorized: YES;
- V3 scope frozen: YES;
- technical working-draft authoring authorized: YES;
- canonical curl protocol specification authorized: NO;
- generated-driver inspection authorized: NO;
- gold annotation authorized: NO;
- analyzer implementation/execution authorized: NO;
- baseline execution authorized: NO;
- repair authorized: NO.

## Next boundary

Author the source-grounded curl technical protocol working draft from the exact
frozen V3 scope and approved source evidence.

Do not inspect generated drivers or begin analyzer/repair work.
