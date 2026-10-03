# D0354 — Non-Consuming Runtime Validation Authorization Design

**Status:** Unreviewed design author-candidate. Not effective.
**Baseline:** D0352, `bc9e9a056de91b8dce50df842e6c7d06403c86b8`.

## 1. Purpose

D0353 completed an independent static review with 82 passing checks
and zero findings. This is static evidence only; no runtime compatibility,
synthetic conformance, production readiness, or ZE2 execution occurred.

D0354 describes a prospective, isolated, non-consuming runtime-validation
protocol. It does not grant permission to execute the protocol.

## 2. Required validation groups

### F1 — Subprocess pipe-FD provenance

Verify exact allowed subprocess stdout/stderr pipe behavior, owner
provenance, descriptor identity, open mode, single-use authorization
and rejection of unrelated integer FDs.

No blanket integer-FD exception, FIFO-only provenance shortcut,
subprocess wildcard, or disabled audit hook is permitted.

### F2 — Synthetic ZE0 attestation conformance

Propose one existing positive synthetic case and all ten negative
structural cases for separately authorized execution.

The real ZE0 or ZE1 scientific datasets must not be opened,
mounted or used as fixture substitutes.

### B1–B5 — Successor operational binding negatives

Use separately reviewed, in-memory mock governance inputs to assess
source SHA/blobs, exact freeze parent, independently effective
freeze-specific authorization, new receipt identities,
readiness-result bindings and the exact subprocess command path.

No real preflight or readiness mode may be entered.

## 3. Mandatory isolation boundary

Every permitted future runtime case requires a fresh, short-lived
isolated process in a disposable fixture environment.

An independent pre-execution review must establish that the environment
cannot access actual scientific payloads or the production ZE2 output
root, modify the working repository, run Git hooks, contact the
production remote, or enter production one-shot entrypoints.

Do not perform even a ZE2 output-root existence or stat test.

If isolation cannot be independently demonstrated, runtime testing
must not begin.

## 4. Unresolved authorization-proof issue

V3's freeze-parent and ancestry checks do not, by themselves,
establish whether the future parent commit contains an effective,
independently approved and remotely published freeze-specific grant.

Future governance must bind the actual authorization evidence
rather than treating an arbitrary caller-provided commit identity
as sufficient approval.

If implementation remediation is needed, author a distinct
prospective change under a separate authorization.

## 5. Frozen scientific invariants

Preserve D0336 matching/output behavior, D0343 F0–F6 regeneration
and ZE0 attestation, D0344 consumed sequence and all fifteen
D0345 readiness check IDs and order.

Keep D0346 V1 and the original receipt immutable.
Keep D0350 V2 and manifest immutable.
Do not modify D0353 V3 or its authoring manifest in D0354.

## 6. Evidence required from future runtime testing

Require a reviewed test-harness identity, isolation evidence,
fixture inputs, expected and actual outcomes, exact error codes,
pipe-FD provenance where applicable, noninterference evidence,
and an independent post-test evidence review.

No runtime evidence is claimed by this design.

## 7. Separate authorization requirement

D0354's publication, even if independently verified, is design
publication only. A later explicit, independently reviewed,
committed, published and remotely verified authorization must
grant any non-consuming runtime execution.

Test harness authoring and review must be separately gated.
The authorization must explicitly bound each fixture and
operation, with fail-closed handling of unauthorized behavior.

## 8. Current disposition

- D0354 design effective: NO.
- Runtime-test execution authorized: NO.
- Synthetic fixture execution authorized: NO.
- D0353 V3 source committed: NO.
- Corrected freeze authorized: NO.
- Preflight authorized: NO.
- Readiness exercisable: NO.
- Readiness attempt capacity remaining: 1.
- ZE2 execution GO: NO.
- ZE2 attempt capacity remaining: 1.
- C4: UNRESOLVED.
- P8 mapping: NOT AUTHORIZED.

## 9. Future independent gates

1. `D0354_INDEPENDENT_PRECOMMIT_DESIGN_REVIEW`
2. `D0354_SEPARATE_DESIGN_ONLY_LOCAL_COMMIT`
3. `D0354_INDEPENDENT_POSTCOMMIT_DESIGN_REVIEW`
4. `D0354_SEPARATE_GITHUB_DESIGN_PUBLICATION`
5. `D0354_INDEPENDENT_EXACT_REMOTE_READBACK`
6. `SEPARATE_EXPLICIT_RUNTIME_TEST_AUTHORIZATION_AUTHORING`
7. `INDEPENDENT_RUNTIME_TEST_AUTHORIZATION_REVIEW`
8. `SEPARATE_AUTHORIZATION_COMMIT_AND_PUBLICATION`
9. `INDEPENDENT_EXACT_AUTHORIZATION_REMOTE_READBACK`
10. `SEPARATE_ISOLATED_TEST_HARNESS_AUTHORING`
11. `INDEPENDENT_TEST_HARNESS_AND_ISOLATION_REVIEW`
12. `SEPARATELY_AUTHORIZED_NONCONSUMING_TEST_EXECUTION`
13. `INDEPENDENT_TEST_RESULT_EVIDENCE_REVIEW`
14. `SEPARATE_SOURCE_REMEDIATION_AUTHORIZATION_IF_NEEDED`
15. `SEPARATE_CORRECTED_FREEZE_AUTHORIZATION_GATE`
16. `SEPARATE_NEW_PREFLIGHT_AUTHORIZATION_GATE`
17. `SEPARATE_ONE_SHOT_READINESS_HANDOFF_GATE`
18. `SEPARATE_ZE2_EXECUTION_GATE`
