# D0349 — Prospective Successor Correction Authorization Candidate

**Identity:** `SVF-D0349-PROSPECTIVE-SUCCESSOR-CORRECTION-AUTHORIZATION-CANDIDATE-V1`

**Status:** Unreviewed author-candidate; not effective.

**Effective predecessor:** D0348 design commit `918d91e2aba41e39e51358df622012d8272c8c2e`.

## 1. Purpose and present authorization boundary

This candidate proposes a strictly prospective correction authorization
for the D0347-F1 and D0347-F2 issues. It does not edit or retroactively
invalidate D0345, D0346, D0347 or D0348.

D0349's effective commit is not yet known. Merely creating or committing
these files does not establish authorization.

Only after independent review, separate local commit, independent
postcommit review, GitHub publication and exact remote readback may
the D0349 decision become effective.

Even if effective, its immediate prospective grant covers **bounded
corrected-source authoring and independent static review only**.
A corrected freeze, preflight, readiness and ZE2 require their own
separate gates.

## 2. D0349-A1 — Authorization identity and publication

D0349 shall have a unique published commit identity. The future effective
commit must be independently read back from GitHub `refs/heads/main`.
No inferred or local-only SHA is sufficient.

Effectiveness may permit separate bounded source authoring and
independent static review; no immediate scientific execution is granted.

## 3. D0349-A2 — Exact prospective freeze ancestry

Frozen historical chain:

- D0345: `06ab9ff6f9563c7f854a538bcb7124279bab2347`
- D0346: `db02f5bc49f95182d29690438fb62b8d9fe992de`
- D0347: `9a3baecf71b108ed554d8c5221bd9ca3075cf36e`
- D0348: `918d91e2aba41e39e51358df622012d8272c8c2e`

The proposed corrected freeze must have the verified effective D0349
commit as its exact **direct parent**. Its ancestry must include the
historical chain above.

This rule prospectively supersedes the original D0345 direct-parent
condition **only for a separately reviewed corrected successor freeze**.
It does not edit the D0345 requirement or alter D0346 history.

Any intervening commit demands a new explicit prospective amendment.
Corrected freeze authorization and commitment are separate transactions.

## 4. D0349-A3 — Single-attempt handoff

The sole remaining D0345 readiness attempt is currently unconsumed
and non-exercisable; ZE2 also retains one unconsumed attempt.

D0349 does **not** perform an authorization handoff.

A future separate pre-readiness safety disposition must establish:

1. The corrected freeze is independently reviewed and effective.
2. A new exact-binding non-consuming preflight receipt is independently
   reviewed.
3. The historical D0346 readiness route is not simultaneously
   executable.
4. The sole remaining readiness attempt can be rebound exclusively,
   with unique lineage and single-consumption accounting.
5. No duplicate or additional attempt capacity is created.

Only an authorized readiness transaction may record actual consumption.

## 5. D0349-A4 — New preflight receipt

The historical D0346 receipt SHA-256 is:

`b83a2af73b56dde23f5c3d2280db50b81d30b79d2beae808462cd2295ce83020`

It remains immutable and is never renamed, overwritten or reused.

A future new receipt must independently bind the corrected freeze SHA,
parent SHA, corrected implementation SHA-256, effective successor
authorization, frozen runtime and hook identities, applicable readiness
check identities, and non-consumption status.

Receipt creation and independent review are separate transactions.
No new preflight is run by this D0349 authoring transaction.

## 6. D0349-A5 — Bounded correction scope

### F1: Subprocess pipe-FD handling

The frozen Python audit guard conflicts with integer pipe-descriptor
operations used by metadata subprocess handling.

Permitted prospective correction scope:

- Explicitly established authorized metadata-subprocess provenance
- Narrow pipe-FD lifecycle validation and bounded usage
- FIFO checks as an additional condition, never sufficient provenance
- Preservation of frozen file-path and command allowlists
- Default-deny behavior for unrecognized access

A blanket integer-FD exemption is prohibited. A Python audit hook is
not a kernel-level security boundary. Independent source review must
assess whether the proposed correction actually enforces its boundaries.

### F2: Existing synthetic attestation coverage

Permit bounded positive and negative fixture coverage for existing
attestation and structural checks, including the positive case using
`representations=None`.

Do not introduce representation-content validation absent from D0343,
change `schema_v2_property_path` regeneration, or relax D0336 matching.

The synthetic vectors may only execute inside a separately authorized
readiness attempt, not during design authoring, static review or preflight.

### Scientific invariants

Preserve D0336, D0343 and D0344 semantics. Preserve all fifteen D0345
readiness check identities and their order, apart from a separately
effective and explicitly scoped amendment.

No ZE0/ZE1 scientific payload reads, no ZE2 reserved output-root test,
and no ZE2 scientific execution are authorized here.

## 7. D0349-A6 — Pre-readiness independent safety gate

A future readiness attempt requires all of:

- Effective D0349 authorization with exact GitHub readback
- Independently reviewed corrected source
- Separately authorized corrected freeze and exact GitHub readback
- New non-consuming preflight receipt bound to that freeze
- Independent receipt review
- Explicit exclusion of competing historical readiness routes
- Separate affirmative pre-readiness safety disposition
- Preservation of the sole readiness-attempt capacity

The ZE2 output-root test remains reserved for its authorized readiness
check; the synthetic vectors remain reserved for readiness as specified.

ZE2 execution remains separately gated after readiness effectiveness.

## 8. Strict transaction sequence

1. Independent D0349 precommit authorization review
2. Separate D0349 local commit
3. Independent D0349 postcommit review
4. Separate GitHub publication
5. Independent exact GitHub remote readback
6. Separate bounded corrected-source authoring
7. Independent corrected-source static review
8. Separate corrected-freeze authorization and commit
9. Independent corrected-freeze postcommit review
10. Separate corrected-freeze GitHub publication
11. Independent corrected-freeze remote readback
12. New non-consuming preflight and independent receipt review
13. Separate pre-readiness safety disposition
14. Only then consider the single remaining readiness attempt
15. Only after effective readiness consider separate ZE2 execution

## 9. Explicit current-state disposition

**D0349 effective authorization:** NO.

**Corrected implementation authoring currently authorized:** NO.

**Corrected freeze currently authorized:** NO.

**Readiness attempt currently exercisable:** NO.

**ZE2 execution GO:** NO.

**D0345 readiness capacity:** 1 unconsumed.

**ZE2 execution capacity:** 1 unconsumed.

**C4:** UNRESOLVED.

**P8 mapping:** NOT AUTHORIZED.
