# D0276 Exact Bounded Retained-Evidence Materialization Execution

## Role

D0276 is the exact bounded retained-evidence materialization execution
authorized by independently frozen and published D0275.

D0276 is materialization only.

It does not perform target-evidence rejudgment, positional adjudication,
positional-status assignment, or Class06 reclassification.

## Execution

The transaction:

- reads candidate 6 snapshot exactly once;
- reads candidate 8 snapshot exactly once;
- reads candidate 9 snapshot exactly once;
- performs exactly three successful snapshot filesystem reads;
- verifies exact byte count, SHA-256, and Git blob OID for each snapshot;
- applies the frozen D0274 line-range extraction algorithm;
- validates all four candidate-8 historical extracted-unit hashes;
- validates the one candidate-9 historical extracted-unit hash;
- requires all five historical compatibility anchors to match;
- extracts candidate-6 units only after all five anchors match;
- extracts candidate-6 units from the already-held bytes without rereading;
- materializes exactly ten retained evidence units.

The five candidate-8/9 compatibility-anchor matches establish output
compatibility with the already frozen D0266 extracted-unit hashes for
those five exact units.

They do not establish general historical algorithm equivalence.

## Durable output

The primary result retains exact extracted target-evidence-unit text for
all ten bound locators together with SHA-256 values.

The output is materialization evidence only.

No materialized text is assigned a positional status in D0276.

## D0277

D0277 remains unauthorized.

Any later positional adjudication requires a separate authorization after
D0276 has independently passed verification/freeze/publication.

## Explicit non-results

D0276 does not:

- acquire new evidence;
- perform source reopening;
- perform locator reselection;
- perform locator filtering;
- perform semantic rejudgment;
- change sufficiency;
- assign REQUIRED, NOT_REQUIRED, or INDETERMINATE;
- reclassify Class06;
- authorize B2;
- execute analyzer work;
- execute baseline work;
- execute repair.
