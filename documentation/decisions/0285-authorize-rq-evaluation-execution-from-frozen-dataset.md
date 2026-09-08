# D0285 — Authorize RQ Evaluation Execution From Frozen Dataset

## Decision

D0285 authorizes execution of SemanticVerify-Fuzz evaluation experiments
using the frozen evaluation dataset artifact produced by D0284.

The evaluation execution is bounded to predefined research questions.

## Parent Binding

D0284 evaluation dataset freeze:

`344c902`

D0283 dataset construction:

`af3c73b`

D0281 final evidence accounting manifest:

`2974826`

## Evaluation Scope

Authorized:

- RQ1 evaluation execution
- RQ2 detection accuracy evaluation
- RQ3 path-sensitive effectiveness evaluation
- RQ5 cross-library generalization evaluation

## Execution Boundary

Allowed:

- metric computation
- experiment execution
- result recording
- evaluation report generation

Forbidden:

- evidence mutation
- dataset mutation
- label mutation
- new evidence acquisition
- repair execution during evaluation

## Status

D0285_AUTHORIZED=YES
D0285_EXECUTED=NO
