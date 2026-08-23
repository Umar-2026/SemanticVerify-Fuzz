# Decision 0104 — Authorize Independent Human Review Package for Relation-Informed Exhaustive Admissible Composition Study V1

Status: AUTHORIZED FOR REVIEW-PACKAGE AUTHORING ONLY — REVIEW PACKAGE NOT YET AUTHORED

## Decision-0103 basis

Decision-0103 commit:

`320ed582665f5a17de0f81684fa829fae6f94099`

Decision-0103 tree:

`6a419a97936eeb09be81b85e86637f9b9096fbfe`

Study V1 Git tree:

`bb55744db442f718daa56f8f38733e3ef4819b1a`

Study V1 JSON SHA-256:

`a8d28b09e78e1466eb5bb0991289879b28b10abd1dd1f9197d138ca723718f6f`

Exhaustiveness-accounting SHA-256:

`ae56e06b6668c301167efdd7e81ba937848446215b49be52d1268c69a2c5d643`

Study report SHA-256:

`d0de61d7285ae8ba2c3ff2fcf2048f8c8dca145f87929a93262ab26c2e4b2642`

Study safe verifier SHA-256:

`b0ff1cb58eee830aa97c2759b54c78a96c9190c3c173a59483ee459bce8e8d22`

Decision-0103 SHA-256:

`75d962331741137325f32af5826ac07f3aa1d67914c896b629f8213974b2087f`

## Study state

Study V1 remains:

`AUTHOR_CANDIDATE`

Global technical outcome:

`FURTHER_EVIDENCE_REQUIRED`

The study does not claim:

- positive existing-Schema-V2 mapping;
- negative existing-Schema-V2 mapping impossibility;
- complete whole-V4 admissible-composition exhaustiveness.

Its conclusion has not been governance-adopted.

## Decision-0102 A02 lifecycle

The Decision-0102 study-authoring authorization verifier has already completed
its one allowed successful run.

Its successful output is preserved byte-exactly in Study V1.

Its current state is:

`PERMANENTLY_RETIRED`

It must never be rerun.

Decision 0104 does not execute it.

## Authorized review package

Decision 0104 authorizes authoring only of:

`Schema-V2 Relation-Informed Exhaustive Admissible Composition Study V1 Review Package V1`

The required independent review criteria are:

- RIAC01 — Exact Study V1 integrity and immutable source binding;
- RIAC02 — Relation-domain and classification accounting correctness;
- RIAC03 — Semantic-unit, leaf-record, and field-class-domain distinction;
- RIAC04 — Seventeen losslessness requirements and requirement-inventory limitation;
- RIAC05 — Semantic admissibility and anti-promotion rules;
- RIAC06 — Soundness of global FURTHER_EVIDENCE_REQUIRED outcome;
- RIAC07 — Decision-0102 A02 lifecycle and reproducibility;
- RIAC08 — Governance boundary and technical nonclaims.

Allowed item decisions are exactly:

- PASS;
- REVISION_REQUIRED;
- FAIL.

Allowed overall decisions are exactly:

- APPROVE_RELATION_INFORMED_EXHAUSTIVE_ADMISSIBLE_COMPOSITION_STUDY_V1;
- REVISION_REQUIRED;
- FAIL.

Required reviewer role:

`Spec-Technical-Reviewer-1`

## Reviewer-independence boundary

The review package must contain a blank manual reviewer packet.

The author must not prepopulate:

- reviewer identity;
- RIAC01-RIAC08 decisions;
- reviewer notes;
- overall decision.

The author must not synthesize a human-review decision.

## Package portability

The review package must contain enough exact evidence for independent
package-local review, including the exact Study V1 artifacts, Decision-0103
binding, relevant Decision-0102 authorization evidence, a safe package-local
verifier, manifest/checksum closure, and the blank manual reviewer packet.

Review-package authoring must not alter Study V1 bytes or change its technical
outcome.

## Explicit non-authorizations

Decision 0104 does not authorize:

- governance adoption of Study V1;
- positive existing-V2 mapping;
- negative existing-V2 mapping impossibility;
- whole-V4 exhaustiveness;
- operational V4-to-V2 mapping;
- operational mapping-contract authoring;
- active Schema V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution; or
- repair.

Prohibited evidence remains prohibited.

## Decision-0104 authorization artifacts

Authorization record SHA-256:

`1e2e8ab6752cf720345ebc0151cd4ed561cf84a82f73dc9cbcfec36eaaeb82cf`

One-time pre-review-package authorization verifier SHA-256:

`f656d264d1ec42f059c4dae2d3ee8dba79949d2aa583f3a58ee426bee896b4b0`

Authorization checksum-manifest SHA-256:

`b3707447d2a09b348e8346c96d122d997e768f3945eec2f2ab4ccd8991b9c6a7`

## One-time verifier lifecycle

The Decision-0104 pre-review-package authorization verifier is initially:

`ACTIVE_UNCONSUMED`

Decision 0104 does not execute it.

It may execute exactly once immediately before Review Package V1 authoring.

Its successful output must be preserved byte-exactly.

After that successful run it is permanently retired and must never be rerun
after package authoring begins.

## Next boundary

`RUN_DECISION_0104_AUTHORIZATION_VERIFIER_ONCE_THEN_AUTHOR_INDEPENDENT_HUMAN_REVIEW_PACKAGE_V1`
