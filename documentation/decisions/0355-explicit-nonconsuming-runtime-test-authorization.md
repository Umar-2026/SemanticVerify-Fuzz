# D0355 — Explicit Non-Consuming Runtime-Test Authorization

**Status:** Unreviewed authorization author-candidate; not effective.

**Baseline:** D0354 (`6fe35cf7088a62234b8dc93f856d047778363a81`).

## 1. Authorization purpose

D0354 is independently published and remotely verified. It is a
design-only governance artifact, not permission to execute tests.

This D0355 candidate specifies prospective, bounded authorization
for isolated non-consuming tests. It is not effective at authoring.

## 2. Exact proposed scope

Only three validation groups from the immutable D0354 design
are in scope:

- F1: nine subprocess pipe-FD provenance cases.
- F2: one positive and ten negative in-memory synthetic cases.
- B1-B5: eleven successor operational-binding negative cases.

The total proposed scope is 31 distinct cases.

No scenario has been executed. No runtime result is claimed.

## 3. Activation requirements

Independent pre-commit review, a separate authorization-only
local commit, independent post-commit review, separate GitHub
publication, and independent exact remote readback are required.

Even after those gates pass, runtime execution remains blocked
until a separately authored and reviewed test harness, exact
fixture and source identities, independently verified isolation,
and a distinct execution GO checkpoint all exist.

A published authorization alone is not an execution GO decision.

## 4. Mandatory isolation

Use a new short-lived isolated process per future case.

The disposable environment must deny production repository
mutations, real Git hooks, real remote access, ZE0/ZE1 scientific
payload access, ZE2 output-root access or existence tests, and
production preflight/readiness/ZE2 entrypoints.

Failure to demonstrate isolation means NO execution.

Do not bypass subprocess audit hooks, generalize Git command
allowlists or introduce a blanket integer-FD exception.

## 5. Independent test evidence

Every eventual case must have recorded fixture identity,
expected result, observed result, exact rejection code where
applicable, harness identity and isolated-process identity.

Require proof of no production data access, no repository
mutation and no one-shot authorization consumption.

All results require independent review.

## 6. Outstanding authorization-proof issue

U3 remains unresolved. A future freeze-specific authorization
cannot be established merely from Git ancestry or a supplied
commit SHA.

The separately approved authorization evidence must be
independently verified. A failing or unverifiable negative case
must not be treated as passing.

Any change to V3 requires a distinct prospective remediation
authorization. D0355 does not authorize source changes.

## 7. Frozen invariants

D0336 matching, D0343 F0-F6 and ZE0 attestation,
D0344 consumed operation order, and all fifteen D0345 readiness
check identities remain unchanged.

D0346 V1 and its original receipt remain immutable.
D0350 V2 and manifest remain immutable.
D0353 V3 and manifest remain unchanged and uncommitted.

No preflight, readiness or ZE2 attempt is authorized or consumed.

## 8. Current disposition

- D0355 authorization effective: NO.
- Runtime tests authorized now: NO.
- Synthetic execution authorized now: NO.
- Test harness authored: NO.
- D0353 source commit authorized: NO.
- Corrected freeze authorized: NO.
- Preflight authorized: NO.
- Readiness exercisable: NO.
- Readiness capacity remaining: 1.
- ZE2 execution GO: NO.
- ZE2 capacity remaining: 1.
- C4: UNRESOLVED.
- P8: NOT AUTHORIZED.

## 9. Required future independent gates

1. `D0355_INDEPENDENT_PRECOMMIT_AUTHORIZATION_REVIEW`
2. `D0355_SEPARATE_AUTHORIZATION_ONLY_LOCAL_COMMIT`
3. `D0355_INDEPENDENT_POSTCOMMIT_AUTHORIZATION_REVIEW`
4. `D0355_SEPARATE_GITHUB_AUTHORIZATION_PUBLICATION`
5. `D0355_INDEPENDENT_EXACT_REMOTE_READBACK`
6. `SEPARATE_ISOLATED_TEST_HARNESS_AUTHORING`
7. `INDEPENDENT_TEST_HARNESS_AND_ISOLATION_REVIEW`
8. `SEPARATE_EXACT_TEST_INPUT_AND_ISOLATION_CHECKPOINT`
9. `SEPARATELY_AUTHORIZED_NONCONSUMING_RUNTIME_EXECUTION`
10. `INDEPENDENT_RUNTIME_RESULT_EVIDENCE_REVIEW`
11. `SEPARATE_SOURCE_REMEDIATION_AUTHORIZATION_IF_NEEDED`
12. `SEPARATE_FREEZE_SPECIFIC_AUTHORIZATION`
13. `SEPARATE_NEW_PREFLIGHT_AUTHORIZATION`
14. `SEPARATE_ONE_SHOT_READINESS_GATE`
15. `SEPARATE_ZE2_EXECUTION_GATE`
