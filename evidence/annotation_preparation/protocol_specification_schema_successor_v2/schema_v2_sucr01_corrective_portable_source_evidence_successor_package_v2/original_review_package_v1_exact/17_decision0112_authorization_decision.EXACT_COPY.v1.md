# Decision 0112 — Authorize Independent Human Review Package for Semantic-Unit Carrier Study V1

Status: REVIEW-PACKAGE AUTHORING AUTHORIZED — PACKAGE NOT YET AUTHORED

## Source checkpoint

Decision-0111 commit:

`5afa21635960e63f018a0613f0cf0f2ed787b952`

Decision-0111 tree:

`90d04b2e8e62a18ef90cbd3f0a83948646e613b1`

Study V1 Git tree:

`3f04237bdc58c2be56e85628de5923b87578a051`

Decision-0110 authorization Git tree:

`e103964df3523d8ebdd30352a4e7895d9087e854`

Decision-0111 SHA-256:

`a9db3f9aff44da0a1dc17d62daa63f4c809c6bc81f531c610b746e08f12de105`

## Review target

`Schema-V2 Semantic-Unit Carrier Admissibility and Requirement Binding Study V1`

Current study status:

`AUTHOR_CANDIDATE`

Current technical outcome:

`FURTHER_EVIDENCE_REQUIRED`

Independent human review remains required.

## Required review criteria

The package must request review of exactly:

- SUCR01 — exact Study V1 integrity and source binding;
- SUCR02 — complete 109 × 171 = 18,639 unit/carrier Cartesian domain;
- SUCR03 — conservative unit-level admissibility and anti-promotion policy;
- SUCR04 — 17-requirement provenance-binding correctness;
- SUCR05 — cross-unit coherence screening and non-promotion correctness;
- SUCR06 — soundness of FURTHER_EVIDENCE_REQUIRED;
- SUCR07 — Decision-0110 A02 lifecycle and reproducibility;
- SUCR08 — governance boundary and technical nonclaims.

Required reviewer role:

`Spec-Technical-Reviewer-1`

Allowed item decisions:

`PASS / REVISION_REQUIRED / FAIL`

Allowed overall decisions:

`APPROVE_SEMANTIC_UNIT_CARRIER_ADMISSIBILITY_AND_REQUIREMENT_BINDING_STUDY_V1 / REVISION_REQUIRED / FAIL`

## Review facts requiring explicit scrutiny

The package must expose, without promoting them beyond their evidentiary status:

- 109 semantic units;
- 171 Schema-V2 property paths;
- 18,639 complete unique Cartesian pairs;
- CANDIDATE_ADMISSIBLE = 0;
- NOT_ADMISSIBLE = 0;
- UNRESOLVED = 18,639;
- 17 losslessness requirements in scope;
- uniquely bound requirements = 0;
- unresolved requirement source bindings = 17;
- cross-unit coherence screening hits = 2;
- accepted explicit cross-unit constraints = 0;
- whole-V4 composition enumeration not performed; and
- global outcome FURTHER_EVIDENCE_REQUIRED.

## Blank review requirement

The future reviewer packet must begin blank.

No reviewer identity may be prepopulated.

No SUCR01-SUCR08 decision may be prepopulated.

No reviewer note may be prepopulated.

No overall decision may be prepopulated.

No author-synthesized human review is permitted.

## Retired verifier state

The following one-time verifiers remain permanently retired:

- Decision-0102 A02
- Decision-0104 A02
- Decision-0106 A02
- Decision-0110 A02

None may be executed during package authoring or verification.

## Decision-0112 one-time verifier

Decision-0112 A02 starts as:

`ACTIVE_UNCONSUMED`

Decision 0112 does not execute it.

It may execute exactly once immediately before review-package authoring.

Its successful final output must be preserved byte-exactly.

After that run it becomes permanently retired.

## Explicit non-authorizations

Decision 0112 does not authorize:

- a human-review decision;
- Study V1 governance adoption;
- positive existing-V2 mapping;
- negative existing-V2 mapping impossibility;
- whole-V4 exhaustiveness;
- operational mapping;
- operational mapping-contract authoring;
- active Schema V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## Authorization evidence

Review-package authorization record SHA-256:

`61b797cf443839e58ae6b3cec0f6eb72c368ea08dc0708bf4be651834706d8b8`

One-time pre-package authorization verifier SHA-256:

`1909a3e22aa39a643ed89475228ff0e47394c9b5d7b773e5f3e14e6dd891e5b0`

Authorization checksum SHA-256:

`b3b97be6c0c914a52466585dd3c4e26986e3bda70f154d9780485d663257886e`

## Next boundary

`RUN_DECISION_0112_A02_EXACTLY_ONCE_IMMEDIATELY_BEFORE_REVIEW_PACKAGE_AUTHORING`
