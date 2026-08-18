# curl V3 RR01 Corrected Evidence Independent Re-Review Packet

## Purpose

This is a narrowly scoped independent human re-review of the previously
blocking `V3-RR01`.

The prior completed V3 review recorded:

- V3-RR01: `REVISION_REQUIRED`
- V3-RR02: `PASS`
- V3-RR03: `PASS`
- V3-RR04: `PASS`
- overall: `REVISION_REQUIRED`

This re-review does not silently overwrite those historical decisions.

Its purpose is to determine whether the two V3-RR01 blockers have now been
resolved by immutable correction evidence.

## Exact V3 target

Path:

`config/annotation/curl_v3_authoring_scope.v3.json`

SHA-256:

`ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`

Author checkpoint commit:

`7de6fc01797ae68cbd64406b850a3198f71cc702`

Author checkpoint tree:

`c5f96b844e5803cccd04c9f64a55754dc6c77e20`

Git blob:

`931c24cc46c99f23ee352455d3e8c93e57e63401`

The V3 scope itself has not been edited after the prior review.

## Exact V2 predecessor

Path:

`config/annotation/curl_v2_authoring_scope.v2.json`

SHA-256:

`f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df`

## Historical Decision 0023

Immutable SHA-256:

`c774bb667930ef9ceaedc5ca5d25e88d57da3ffefa10de639ef6a20f7d2271d1`

The prior reviewer identified a malformed predecessor-SHA presentation line in
Decision 0023.

Decision 0023 has not been edited in place.

## Corrective Decision 0024

SHA-256:

`df22dc70c572407c1968859f6fd86a20d847062b2130a08484670c06a340915b`

Commit:

`36400fa2028df6ccaf176780ba8ff21017a68262`

Tree:

`d7afbc0a4c159530f5687c93dca2bad823e55f77`

Git blob:

`ca72e87d5668c649eb64db8fc04f457eeebc5d0c`

Decision 0024 preserves Decision 0023 as immutable historical evidence and
records the corrected predecessor binding without modifying the V3 scope
semantics.

## Independently resolvable Git witness

The package contains:

`10_minimal_git_witness_v1/02_curl_v3_rr01_minimal_git_witness.v1.tar.gz`

SHA-256:

`3710cd5b49fa3e80610724756bae7376fc196c23de36f2f110ab6074d256e181`

The witness is intended to contain exactly:

- 2 commit objects;
- 6 tree objects;
- 2 file blobs.

The only file blobs are the exact V3 scope and Decision 0024.

Parent commit objects and unrelated file blobs are intentionally excluded.

Run:

`python3 10_minimal_git_witness_v1/03_verify_minimal_git_witness.v1.py`

Expected final result:

`QUARANTINE_SAFE_MINIMAL_GIT_WITNESS_VERIFICATION=PASS`

## Mandatory decisions

For each corrected RR01 item choose exactly one:

`PASS`

`REVISION_REQUIRED`

`FAIL`

### RR01-R1 — Exact immutable V3 target and V2 predecessor

Decision:

Notes:

Confirm:

- exact V3 SHA-256 is correct;
- exact V3 Git blob is correct;
- exact V2 predecessor SHA-256 is correct;
- V3 and V2 remain immutable;
- V3 has not been edited in place after the prior review.

### RR01-R2 — Independently resolvable V3 commit/tree/blob evidence

Decision:

Notes:

Using only the supplied minimal Git witness, independently confirm:

- commit
  `7de6fc01797ae68cbd64406b850a3198f71cc702`
  exists as a commit object;
- its root tree resolves to
  `c5f96b844e5803cccd04c9f64a55754dc6c77e20`;
- path
  `config/annotation/curl_v3_authoring_scope.v3.json`
  resolves to blob
  `931c24cc46c99f23ee352455d3e8c93e57e63401`;
- that blob has SHA-256
  `ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`.

### RR01-R3 — Decision 0023 immutable correction

Decision:

Notes:

Confirm:

- historical Decision 0023 remains byte-preserved at SHA-256
  `c774bb667930ef9ceaedc5ca5d25e88d57da3ffefa10de639ef6a20f7d2271d1`;
- Decision 0024 is a separate immutable correction record;
- Decision 0024 correctly records the V2 predecessor SHA-256 as
  `f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df`;
- Decision 0024 does not modify the exact V3 protocol-semantic surface.

### RR01-R4 — Witness quarantine and minimality

Decision:

Notes:

Confirm that the supplied witness contains exactly:

- 2 commit objects;
- 6 tree objects;
- 2 file blobs;

and that:

- the only file blobs are the exact V3 scope and Decision 0024;
- parent-history commit objects are absent;
- unrelated generated-driver, gold-label, analyzer-output, baseline-output,
  LLM-review-output, and repair-output blobs are not exposed.

## Overall re-review decision

Choose exactly one:

`APPROVE_EXACT_V3_SCOPE_FOR_FREEZE`

`REVISION_REQUIRED`

`FAIL`

Overall decision:

Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

Notes:

## Decision interpretation

`APPROVE_EXACT_V3_SCOPE_FOR_FREEZE` may be chosen only if the reviewer is
satisfied that the previously blocking RR01 evidence defects are resolved and
finds no new blocking issue.

That decision authorizes only the subsequent **separate V3 scope-freeze
operation**.

It does NOT directly authorize technical working-draft authoring.

Technical working-draft authoring remains prohibited until the exact approved
V3 scope subsequently completes its separate freeze boundary.

No assistant-generated or synthetic human approval is permitted.
