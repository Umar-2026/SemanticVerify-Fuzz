# D0289 — Generate Paper Results Traceability Manifest

## Decision

D0289 generates the paper results traceability manifest
from the frozen D0288 final evaluation report manifest.

The manifest establishes provenance mapping between
SemanticVerify-Fuzz evaluation artifacts and paper claims.

No evidence generation, dataset modification,
or result modification is performed.

## Parent Binding

D0288 final evaluation report manifest:

`80b3434`

D0287 frozen evaluation results:

`30d0d80`

D0286 RQ evaluation execution:

`1b2d549`

D0284 frozen evaluation dataset:

`344c902`

## Traceability Scope

Included:

- RQ1 → Defect prevalence analysis
- RQ2 → Detection accuracy analysis
- RQ3 → Path-sensitive verification effectiveness
- RQ5 → Cross-library generalization

