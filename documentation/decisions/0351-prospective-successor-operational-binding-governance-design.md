# D0351 — Prospective Successor Operational Binding Governance Design

**Status:** Unreviewed design author-candidate; not effective.

**Effective authorization baseline:** D0349 `b7f869c445acb1a81d45fc0b8ff1ba5745fe4481`.

## 1. Purpose and limits

D0350 has completed independent static source review: 68 PASS, 0 findings. This establishes static coverage only, not runtime compatibility.

The corrected V2 source and D0350 manifest remain untracked and uncommitted. The frozen V1 source and historical D0346 preflight receipt remain immutable.

This D0351 design does not grant permission to modify operational bindings, commit V2, run tests, publish a corrected freeze, conduct preflight or consume any one-shot authorization.

## 2. Seven unresolved blockers

### B1 — IMPLEMENTATION_FREEZE_IDENTITY

**Observed:** verify_freeze_identity still binds the historical D0346 implementation file set, V1 path, SHA-256 and Git blob identity.

**Proposed disposition:** A separately authorized successor verifier must bind only the corrected committed source path, SHA-256, Git blob identity and future freeze lineage. Historical D0346 metadata remains immutable.

### B2 — PREFLIGHT_EXACT_PARENT

**Observed:** preflight_identity requires the historical D0345 direct parent and original V1 source path.

**Proposed disposition:** Future preflight must verify the separately authorized corrected freeze parent and exact corrected source identity without relaxing worktree, branch or remote checks.

### B3 — PREFLIGHT_RECEIPT_BINDING

**Observed:** verify_preflight_receipt requires the historical D0345/D0346 commit relationship and original receipt binding.

**Proposed disposition:** Require a new non-consuming receipt with corrected freeze SHA, parent, source SHA, runtime identities and independent review. Never reuse the old receipt.

### B4 — READINESS_RESULT_FREEZE_BINDING

**Observed:** verify_effective_readiness_result retains the historical D0345 direct-parent expectation.

**Proposed disposition:** A future successor readiness result must bind the corrected effective freeze and independently approved successor authorization without changing the fifteen frozen readiness check IDs.

### B5 — READINESS_AUDIT_COMMAND_PATH

**Observed:** ReadinessReadGuard retains the original V1 Git hash-object command-path allowlist.

**Proposed disposition:** A future narrowly approved command-path binding may identify the exact corrected V2 file only. Do not generalize subprocess command allowlists.

### B6 — D0349_DIRECT_PARENT_LINEAGE_COLLISION

**Observed:** D0349 currently requires a corrected freeze to have D0349 as its exact direct parent. Prospective intervening governance commits would make that rule unsatisfied.

**Proposed disposition:** Before a corrected freeze can be committed, publish a separate effective prospective authorization amendment. It must explicitly set the corrected freeze's direct parent to that future authorization commit or another exactly specified and independently approved lineage. D0351 design is not that amendment.

### B7 — F1_F2_STATIC_ONLY_VALIDATION

**Observed:** D0350 completed 68/68 independent static checks, but no runtime compatibility or synthetic fixture execution.

**Proposed disposition:** Any future bounded compatibility testing requires separate authorization, clear non-consuming isolation and independent review. It must never enter D0345 readiness or create a ZE2 execution attempt.

## 3. Eight prospective governance rules

### R1 — SUCCESSOR_LINEAGE_AMENDMENT

Do not reinterpret D0349-A2 silently. A future separately reviewed, committed, published and remotely verified authorization must establish the replacement exact-parent rule.

### R2 — BOUNDED_OPERATIONAL_BINDING_SCOPE

Only B1-B5 bindings may be prospectively reconciled, and only after explicit authorization. Preserve historical V1 and its D0346 freeze unchanged.

### R3 — D0350_CANDIDATE_INTEGRITY

Bind future consideration to the exact D0350 V2 source SHA-256 and D0350 authoring manifest. Do not silently edit or stage these artifacts.

### R4 — INDEPENDENT_NONCONSUMING_VALIDATION

F1/F2 runtime validation, if later authorized, must use separately bounded non-scientific fixtures and cannot run any preflight, readiness or ZE2 one-shot mode.

### R5 — CORRECTED_FREEZE_GATE

No source commit or corrected freeze until an independently effective successor authorization expressly permits it. A corrected freeze needs postcommit review, GitHub publication and exact remote readback.

### R6 — NEW_PREFLIGHT_RECEIPT_GATE

A new exact-binding non-consuming preflight requires separate authorization after a corrected freeze is effective, followed by independent receipt review.

### R7 — ONE_SHOT_HANDOFF_AND_SCIENCE_FIREWALL

No readiness handoff or consumption is performed by design or source authoring. Keep the original one remaining readiness attempt and one remaining ZE2 attempt blocked until separate effective gates.

### R8 — FROZEN_SCIENTIFIC_SEMANTICS

Preserve D0336 matching/output semantics, D0343 regeneration/attestation semantics, D0344 sequence and all fifteen D0345 readiness check identities and order.

## 4. Critical ancestry disposition

D0349-A2 currently requires the effective D0349 commit to be the corrected freeze's exact direct parent. Publishing D0351 or later governance commits does not automatically satisfy or amend that requirement.

A future separate authorization must explicitly define the amended exact-parent rule and become effective through independent review, separate local commit, postcommit review, GitHub publication and independent exact remote readback before any corrected freeze commit.

The future authorization commit SHA cannot be predetermined in this design.

## 5. Source evidence identities

- Frozen V1 SHA-256: `42ce966e66ea855e7a701277f907dda585d33831773b6f9b35c9c5aed528c935`
- D0350 V2 SHA-256: `1ba6cf7825692a6b0c35d8a6baa3cabc2a4f629db06e80d99d1ef7d7ca0e0a1f`
- D0350 manifest SHA-256: `59e91f3dca7393aa8348eb6b00805ad1d075fa5640ac9dacfc0bb2c7832b4283`
- Original D0346 receipt SHA-256: `b83a2af73b56dde23f5c3d2280db50b81d30b79d2beae808462cd2295ce83020`

## 6. Separate future gates

1. Independent D0351 precommit design review.
2. Separate D0351 design-only commit.
3. Independent D0351 postcommit review.
4. Separate GitHub publication.
5. Independent exact GitHub remote readback.
6. Separately authored and reviewed successor authorization.
7. Separate authorization publication and remote verification.
8. Only then reconsider bounded operational source authoring, testing and corrected freeze eligibility.
9. Require a new preflight and independent receipt review.
10. Require separate pre-readiness safety disposition.
11. Preserve readiness and ZE2 one-shot consumption gates.

## 7. Current disposition

- D0351 authorization established: **NO**.
- D0350 source committed: **NO**.
- Corrected freeze authorized: **NO**.
- Preflight authorized: **NO**.
- Readiness attempt exercisable: **NO**.
- ZE2 execution GO: **NO**.
- Remaining readiness capacity: **1**.
- Remaining ZE2 capacity: **1**.
- C4: **UNRESOLVED**.
- P8 mapping: **NOT AUTHORIZED**.
