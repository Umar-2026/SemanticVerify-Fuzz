# D0352 — Prospective Successor Operational Binding Authorization Amendment

**Status:** Unreviewed authorization author-candidate; not effective.

**Exact authoring baseline:** D0351 `d90999ea9b06e85cda383ccf7325f123b885e238`.

## 1. Purpose and current authorization boundary

D0351 is an independently published and remotely verified governance design only. It granted no operational permission.

D0350 V2 source completed a 68/68 independent static review with zero findings, but no runtime compatibility or synthetic fixture execution occurred.

This D0352 document is a prospective authorization candidate. Its publication gates must complete independently before any conditional source-authoring grant becomes effective.

D0352 does not immediately authorize source staging, source commit, corrected freeze, preflight, readiness or ZE2 execution.

## 2. Seven documented D0351 blockers

### B1 — IMPLEMENTATION_FREEZE_IDENTITY

**Existing blocker:** verify_freeze_identity still binds the historical D0346 implementation file set, V1 path, SHA-256 and Git blob identity.

**D0351 proposed disposition:** A separately authorized successor verifier must bind only the corrected committed source path, SHA-256, Git blob identity and future freeze lineage. Historical D0346 metadata remains immutable.

### B2 — PREFLIGHT_EXACT_PARENT

**Existing blocker:** preflight_identity requires the historical D0345 direct parent and original V1 source path.

**D0351 proposed disposition:** Future preflight must verify the separately authorized corrected freeze parent and exact corrected source identity without relaxing worktree, branch or remote checks.

### B3 — PREFLIGHT_RECEIPT_BINDING

**Existing blocker:** verify_preflight_receipt requires the historical D0345/D0346 commit relationship and original receipt binding.

**D0351 proposed disposition:** Require a new non-consuming receipt with corrected freeze SHA, parent, source SHA, runtime identities and independent review. Never reuse the old receipt.

### B4 — READINESS_RESULT_FREEZE_BINDING

**Existing blocker:** verify_effective_readiness_result retains the historical D0345 direct-parent expectation.

**D0351 proposed disposition:** A future successor readiness result must bind the corrected effective freeze and independently approved successor authorization without changing the fifteen frozen readiness check IDs.

### B5 — READINESS_AUDIT_COMMAND_PATH

**Existing blocker:** ReadinessReadGuard retains the original V1 Git hash-object command-path allowlist.

**D0351 proposed disposition:** A future narrowly approved command-path binding may identify the exact corrected V2 file only. Do not generalize subprocess command allowlists.

### B6 — D0349_DIRECT_PARENT_LINEAGE_COLLISION

**Existing blocker:** D0349 currently requires a corrected freeze to have D0349 as its exact direct parent. Prospective intervening governance commits would make that rule unsatisfied.

**D0351 proposed disposition:** Before a corrected freeze can be committed, publish a separate effective prospective authorization amendment. It must explicitly set the corrected freeze's direct parent to that future authorization commit or another exactly specified and independently approved lineage. D0351 design is not that amendment.

### B7 — F1_F2_STATIC_ONLY_VALIDATION

**Existing blocker:** D0350 completed 68/68 independent static checks, but no runtime compatibility or synthetic fixture execution.

**D0351 proposed disposition:** Any future bounded compatibility testing requires separate authorization, clear non-consuming isolation and independent review. It must never enter D0345 readiness or create a ZE2 execution attempt.

## 3. Eight proposed D0352 authorization decisions

### A1 — PROSPECTIVE_AUTHORIZATION_EFFECTIVENESS

This D0352 candidate provides no immediate grant. It becomes effective only after independent precommit review, separate design-authorized local commit, independent postcommit review, separate GitHub publication, and independent exact remote-main readback. Any failed gate keeps the proposed authorization inactive.

### A2 — PROSPECTIVE_D0349_EXACT_PARENT_AMENDMENT

Only after D0352 is effective, prospectively replace D0349-A2 for a future corrected freeze: the corrected freeze commit must have as its exact direct parent the independently published and exactly remote-verified commit granting that specific corrected freeze. The grant commit SHA must be explicitly established before the freeze is staged. No intervening commit is permitted. D0352 itself does not grant a corrected freeze and is not automatically the freeze's direct parent. D0345/D0346 history and the original D0349 record are unchanged.

### A3 — BOUNDED_OPERATIONAL_SOURCE_AUTHORING

After D0352 effectiveness, authorize authoring only prospective corrections for D0351 blockers B1 through B5, on a separately identified new successor source candidate. Preserve the exact already reviewed D0350 V2 source and manifest without silent edits, and keep D0346 V1 frozen. No source staging or commit is granted by this authorization.

### A4 — CORRECTED_FREEZE_AND_PREFLIGHT_BINDINGS

Future separately reviewed implementation freeze metadata must bind the corrected source path, SHA-256, Git blob identity, exact effective corrected-freeze authorization commit and exact direct parent. A new non-consuming preflight receipt must bind that corrected freeze and the frozen runtime and hook identities. The original D0346 receipt must never be reused or rewritten. Neither a freeze nor preflight is authorized by this D0352 candidate.

### A5 — F1_F2_AND_SCIENTIFIC_SEMANTICS_FIREWALL

Retain the reviewed D0350 F1/F2 candidate identity and existing attestation semantics. Preserve default-deny file and subprocess audit boundaries, with no blanket integer-FD exemption, FIFO-only provenance shortcut, or broadened subprocess allowlist. Preserve D0336 matching/output semantics, D0343 attestation and F0-F6 semantics, D0344 consumed sequence and all fifteen D0345 readiness check identities and order.

### A6 — INDEPENDENT_REVIEW_AND_NONCONSUMING_TEST_GATES

Any later B1-B5 successor source candidate requires separate independent static review. F1 subprocess pipe-FD runtime compatibility and F2 synthetic behavior remain unverified. No runtime compatibility tests, fixture execution, corrected freeze, preflight, readiness attempt, or ZE2 run may occur without separate action-specific authorization and the applicable independent reviews.

### A7 — EXCLUSIVE_ONE_SHOT_READINESS_HANDOFF

The original D0345 remaining readiness capacity stays one, unconsumed, blocked. The ZE2 execution capacity stays one, unconsumed, blocked. No parallel D0346 readiness route or reuse of its receipt is permitted. Future handoff requires an effective corrected freeze, a newly reviewed preflight receipt and a separate independent safety disposition.

### A8 — SCIENTIFIC_GOVERNANCE_CONTINUITY

C4 remains unresolved. P8 curl V4-to-V2 mapping remains unauthorized. No ZE0 or ZE1 scientific payload reads, ZE2 output-root existence test, readiness invocation, ZE2 execution or one-shot consumption is authorized by this amendment.

## 4. Prospective exact-direct-parent amendment

The original D0349-A2 direct-parent rule remains an immutable historical authorization record. It is not silently rewritten.

Only following independent D0352 effectiveness, a corrected freeze must use the exact independently published and remotely verified authorization commit that specifically grants that corrected freeze as its direct parent.

That future authorization SHA must be established before staging the freeze; intervening commits are forbidden.

D0352 does not itself authorize any corrected freeze. A future freeze-specific authorization is required.

## 5. B1-B5 source-authoring scope

Once independently effective, D0352 proposes authoring a new distinct successor source candidate to reconcile D0351 operational bindings B1 through B5 only.

The reviewed D0350 V2 source and manifest must remain unchanged. The historical D0346 V1 implementation and original preflight receipt remain immutable.

Source authoring does not imply source commitment, runtime verification or corrected freeze authorization.

## 6. Scientific semantics and safety firewall

Preserve D0336 matching and output semantics, D0343 F0-F6 regeneration and ZE0 attestation, D0344 consumed sequence, and all fifteen D0345 readiness checks in exact order.

No blanket integer-FD exemption, FIFO-only provenance shortcut or unrestricted subprocess command allowlist is permitted.

F1 subprocess runtime compatibility and F2 synthetic execution remain separately gated and unverified.

## 7. Evidence identities

- Frozen D0346 V1 SHA-256: `42ce966e66ea855e7a701277f907dda585d33831773b6f9b35c9c5aed528c935`
- D0350 V2 candidate SHA-256: `1ba6cf7825692a6b0c35d8a6baa3cabc2a4f629db06e80d99d1ef7d7ca0e0a1f`
- D0350 manifest SHA-256: `59e91f3dca7393aa8348eb6b00805ad1d075fa5640ac9dacfc0bb2c7832b4283`
- D0349 authorization SHA-256: `e4409993f4e9642d123443946200a19fc805e761f3d1b6be819d961033665413`
- D0351 design SHA-256: `4f0b3ea1d48fa1686f86f68bc10fd1559e04111b994958d14d627b3ca2d90454`
- Original D0346 preflight receipt SHA-256: `b83a2af73b56dde23f5c3d2280db50b81d30b79d2beae808462cd2295ce83020`

## 8. Separate future governance gates

1. `D0352_INDEPENDENT_PRECOMMIT_AUTHORIZATION_REVIEW`
2. `D0352_SEPARATE_LOCAL_AUTHORIZATION_COMMIT`
3. `D0352_INDEPENDENT_POSTCOMMIT_AUTHORIZATION_REVIEW`
4. `D0352_SEPARATE_GITHUB_PUBLICATION`
5. `D0352_INDEPENDENT_EXACT_REMOTE_READBACK`
6. `SEPARATE_B1_B5_SUCCESSOR_SOURCE_AUTHORING`
7. `INDEPENDENT_B1_B5_SOURCE_STATIC_REVIEW`
8. `SEPARATE_NONCONSUMING_RUNTIME_TEST_AUTHORIZATION_IF_NEEDED`
9. `INDEPENDENT_NONCONSUMING_TEST_EVIDENCE_REVIEW_IF_EXECUTED`
10. `SEPARATE_EXPLICIT_CORRECTED_FREEZE_AUTHORIZATION`
11. `INDEPENDENT_CORRECTED_FREEZE_AUTHORIZATION_PUBLICATION_AND_READBACK`
12. `SEPARATE_CORRECTED_FREEZE_COMMIT`
13. `INDEPENDENT_CORRECTED_FREEZE_POSTCOMMIT_REVIEW`
14. `CORRECTED_FREEZE_GITHUB_PUBLICATION_AND_EXACT_READBACK`
15. `SEPARATELY_AUTHORIZED_NEW_NONCONSUMING_PREFLIGHT`
16. `INDEPENDENT_NEW_PREFLIGHT_RECEIPT_REVIEW`
17. `SEPARATE_PRE_READINESS_SAFETY_DISPOSITION`
18. `SEPARATE_ONE_SHOT_READINESS_AUTHORIZATION_HANDOFF`
19. `SEPARATE_ONE_SHOT_READINESS_ATTEMPT`
20. `SEPARATE_ZE2_EXECUTION_CHECKPOINTS`

## 9. Current nonauthorization disposition

- D0352 effective now: **NO**.
- D0350 V2 source committed: **NO**.
- B1-B5 operational source authoring performed: **NO**.
- Corrected freeze authorized: **NO**.
- New preflight authorized: **NO**.
- Readiness attempt exercisable: **NO**.
- Remaining readiness attempt capacity: **1**.
- ZE2 execution GO: **NO**.
- Remaining ZE2 execution capacity: **1**.
- C4 status: **UNRESOLVED**.
- P8 mapping: **NOT AUTHORIZED**.
