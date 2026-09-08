# D0286 — Execute RQ Evaluation From Frozen Dataset

## Decision

D0286 executes the RQ evaluation experiments authorized by D0285.

The execution consumes only the frozen evaluation dataset artifact.

No evidence, dataset, or label mutation is performed.

## Parent Binding

D0285 authorization:

`5a22172`

D0284 frozen evaluation dataset:

`344c902`

D0281 final evidence accounting manifest:

`2974826`

## Execution Scope

Executed:

- RQ1 defect distribution evaluation
- RQ2 detection performance evaluation
- RQ3 path-sensitive effectiveness evaluation
- RQ5 cross-library transfer evaluation

## Execution Boundary

Allowed:

- analyzer execution
- metric computation
- result recording

Forbidden:

- new evidence acquisition
- evidence mutation
- dataset mutation
- label mutation
- repair execution

## Status

D0286_AUTHORIZED=YES

D0286_EXECUTED=YES
