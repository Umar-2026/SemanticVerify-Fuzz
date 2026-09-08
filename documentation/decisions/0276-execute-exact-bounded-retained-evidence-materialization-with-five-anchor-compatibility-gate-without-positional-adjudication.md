# D0276 — Execute Exact Bounded Retained-Evidence Materialization with Five-Anchor Compatibility Gate Without Positional Adjudication

## Decision

D0276 executes the exact materialization transaction authorized by
independently frozen and published D0275.

The transaction is bound to:

- D0275 transaction-design SHA256:
  `2b399b91fb2f81b7ec8b1c5a5bb515e9fe6ca7e26aced54a7921a2c9fdeb6f5b`
- D0274 extraction-algorithm object SHA256:
  `7aa7a4f11ca99ccb1bbe1cbd537b1d0eac6dd2e0019366711cb103620f85d1c1`

## Execution result

The execution:

- read candidate 6 once;
- read candidate 8 once;
- read candidate 9 once;
- performed exactly three snapshot filesystem reads;
- verified all three frozen snapshot identities;
- reproduced all four candidate-8 historical extracted-unit hashes;
- reproduced the candidate-9 historical extracted-unit hash;
- passed all five compatibility anchors;
- extracted candidate-6 units only after the five-anchor gate passed;
- did not reread candidate 6;
- materialized exactly ten retained evidence units.

The five anchor matches establish compatibility with the frozen D0266
outputs for those five exact units. They do not establish general
historical algorithm equivalence.

## Boundary

D0276 is materialization only.

No target-evidence rejudgment, positional adjudication, positional-status
assignment, Class06 reclassification, or sufficiency mutation is
performed.

D0277 remains unauthorized until D0276 independently passes its
verification/freeze/publication checkpoint.
