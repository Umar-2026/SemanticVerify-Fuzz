# D0271 Sufficient-Branch Positional-Inference Adjudication Authorization Scope

## Source binding

D0271 is authorization-only and is bound to frozen/published D0270:

`f7c0461fd281f443547b79ce89b6a544ea299106`

D0270 primary SHA-256:

`95dd66ab7ff15c6785a70d44dbb930ffe6086de1b83d1baa1e6d261f2eb96f22`

Post-D0270 successor-branch governance design SHA-256:

`68d1d6c4580f1e5683a122810f36d5b83f958de2dcfda2b62e25241d6437eaf1`

## Target branch

Branch:

`S1_SUFFICIENT_POSITIONAL_BRANCH`

Candidates:

`6,8,9`

Frozen entry state:

`FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION`

Authorized future operation:

`SEPARATE_POSITIONAL_INFERENCE_ADJUDICATION`

## Authorization boundary

D0271 authorizes only a future bounded branch-local positional-inference
adjudication for candidates 6, 8, and 9.

D0271 does not execute that adjudication.

The designated execution decision is:

`D0272`

D0272 execution is prohibited until D0271 has passed a separate independent
read-only verification checkpoint.

No D0251 snapshot content read is authorized.

No original source blob reopening is authorized.

No new evidence acquisition is authorized.

No result reselection, evidence rejudgment, historical-result mutation, or
sufficiency-result mutation is authorized.

No candidate may migrate between branches.

No cross-branch backflow is authorized.

No global positional status assignment is authorized by D0271.

No Class06 reclassification is authorized by D0271.

The indeterminate branch `1,2` remains untouched.

The insufficient branch `3,5,7,10` remains untouched.

No C4, C5, C6, B2, active Schema V2 materialization, analyzer, baseline, or
repair operation is authorized.

## Next checkpoint

`INDEPENDENT_READ_ONLY_VERIFY_D0271_AUTHORIZATION_BEFORE_D0272_EXECUTION`
