# D0275 — Authorize D0276 Exact Bounded Retained-Evidence Materialization and Defer Positional Adjudication to D0277 Without Execution

## Decision

D0275 is an authorization-only corrective successor.

D0274 remains historically unchanged.

The read-only D0275 transaction design is now exactly bound:

- transaction-design SHA256:
  `2b399b91fb2f81b7ec8b1c5a5bb515e9fe6ca7e26aced54a7921a2c9fdeb6f5b`
- extraction-algorithm object SHA256:
  `7aa7a4f11ca99ccb1bbe1cbd537b1d0eac6dd2e0019366711cb103620f85d1c1`
- candidate count: 3
- candidate order: 6, 8, 9
- total bound locator count: 10
- candidate-8/9 historical compatibility anchors: 5

D0275 itself performs no snapshot-content read and no materialization.

## D0276 authorization

D0275 authorizes D0276 as the exact bounded retained-evidence
materialization execution.

D0276 may not execute before D0275 has passed independent read-only
verification/freeze.

D0276 must execute exactly the transaction design bound above.

Each candidate snapshot may be read at most once and total snapshot
filesystem reads may not exceed three.

All five frozen candidate-8/9 extracted-unit SHA-256 anchors must match.

Any anchor mismatch is fail-closed and prohibits a durable D0276 result.

Candidate 6 extraction may occur only after all five anchors match and must
use the already-held candidate-6 raw bytes without a second snapshot read.

Durable materialization output may be created only atomically after every
identity, decode, locator, bounds, compatibility-anchor, and completeness
check succeeds.

## D0277

D0277 becomes the prospective later branch-local positional-adjudication
checkpoint.

D0275 does not authorize D0277.

D0277 may not be authorized before D0276 executes and may not execute
before D0276 independently passes its verification/freeze checkpoint.

No target-evidence rejudgment, positional adjudication, positional-status
assignment, Class06 reclassification, sufficiency mutation, B2, analyzer,
baseline, or repair occurs in D0275.
