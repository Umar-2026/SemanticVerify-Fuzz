# D0275 Exact Bounded Retained-Evidence Materialization Execution Authorization

## Role

D0275 is an authorization-only corrective successor.

D0274 remains historically unchanged. D0274 designated D0275 as the
prospective bounded retained-evidence materialization checkpoint but did
not authorize D0275 execution.

The subsequent read-only design binding established that a durable
preexecution authorization must bind the exact transaction before any
snapshot content is read.

Therefore D0275 performs no snapshot-content read and performs no
materialization.

## Exact transaction binding

D0275 binds exactly:

- transaction-design SHA256:
  `2b399b91fb2f81b7ec8b1c5a5bb515e9fe6ca7e26aced54a7921a2c9fdeb6f5b`
- extraction-algorithm object SHA256:
  `7aa7a4f11ca99ccb1bbe1cbd537b1d0eac6dd2e0019366711cb103620f85d1c1`
- candidates: 6, 8, 9
- total locators: 10
- candidate 6 locators: 5
- candidate 8 locators: 4
- candidate 9 locators: 1
- candidate 8/9 historical compatibility anchors: 5

No locator filtering, reselection, or new locator discovery is authorized.

## D0276 authorization

D0275 authorizes D0276 as the exact bounded retained-evidence
materialization execution.

D0276 may execute only after D0275 independently passes its
verification/freeze checkpoint.

D0276 must execute exactly the frozen transaction design bound above.

Each candidate snapshot may be read at most once; total successful
snapshot filesystem reads may not exceed three.

All five frozen candidate-8/9 historical extracted-unit hashes must match.

Any mismatch fails closed and prohibits a durable D0276 materialization
result.

Candidate 6 extraction may occur only after all five candidate-8/9
compatibility anchors match.

Durable output may be created only atomically after all identity, parsing,
bounds, hash-anchor, and completeness checks pass.

## D0277 boundary

D0277 is the prospective later branch-local positional adjudication.

D0275 does not authorize D0277.

D0277 may not be authorized before D0276 executes and may not execute
before D0276 independently passes its verification/freeze checkpoint.

## Prohibitions

D0275 performs no:

- snapshot-content read;
- materialization;
- target-evidence rejudgment;
- positional adjudication;
- positional-status assignment;
- Class06 reclassification;
- sufficiency mutation;
- branch migration;
- B2;
- analyzer;
- baseline;
- repair.
