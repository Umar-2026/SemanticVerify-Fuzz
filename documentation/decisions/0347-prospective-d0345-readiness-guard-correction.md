# D0347 — Prospective Readiness Guard Correction Design

**Design ID:** `SVF-D0347-PROSPECTIVE-D0345-READINESS-GUARD-AND-ATTESTATION-COVERAGE-CORRECTION-DESIGN-V1`

**Status:** Unreviewed author candidate. No successor execution
authorization or source-modification authorization is established.

## 1. Frozen state

- Effective implementation freeze: `db02f5bc49f95182d29690438fb62b8d9fe992de`
- Parent D0345: `06ab9ff6f9563c7f854a538bcb7124279bab2347`
- Frozen implementation SHA-256: `42ce966e66ea855e7a701277f907dda585d33831773b6f9b35c9c5aed528c935`
- Existing preflight receipt SHA-256: `b83a2af73b56dde23f5c3d2280db50b81d30b79d2beae808462cd2295ce83020`
- Remaining D0345 readiness capacity: 1 of 1
- Remaining ZE2 execution capacity: 1 of 1

The D0346 commit and existing preflight receipt remain immutable.

## 2. F1 — Python audit-hook pipe-FD conflict

The readiness guard is installed before frozen implementation
identity verification. Python subprocess handling uses integer pipe
file descriptors, whereas the current audit hook denies non-path
`open` arguments.

Prospective correction: only narrowly verified pipe file
descriptors, with `os.fstat` FIFO validation and explicit
metadata-subprocess provenance, may be considered for exemption.
Preserve the path allowlist, command allowlist, read accounting,
and default-deny behavior. Do not implement a blanket integer-FD
exemption or claim a Python audit hook is a kernel sandbox.

No one-shot readiness is authorized by this proposal.

## 3. F2 — Check 9 synthetic attestation coverage

The current positive synthetic record sets `representations=None`.
`attest_ze0` validates field presence, rather than representation
content. This is not automatically a defect in frozen scientific
semantics: D0343 requires regeneration from the stored
`schema_v2_property_path`.

Prospective correction: specify positive and negative synthetic
attestation checks covering exactly the previously frozen structural
and identity conditions. Do not impose new scientific data
requirements or read ZE0 scientific data during readiness.

## 4. F3 — Successor governance lineage

D0345 explicitly requires the effective D0345 commit to be the
direct parent of the operational implementation freeze commit.
That requirement was satisfied by D0346. A later source-correction
commit is not automatically authorized under the same direct-parent
condition.

A separately reviewed successor governance amendment must resolve
the corrected implementation's ancestry and effective-freeze
conditions. This design does not amend D0345, create any extra
attempt, or mark a future implementation effective.

## 5. F4 — Receipt lineage

The existing preflight receipt is valid evidence for D0346, not a
transferable receipt for a different implementation hash. Preserve
it exactly. A future authorized corrected implementation requires
a new separately generated and independently reviewed preflight
receipt.

## 6. Required separation of transactions

1. Independent D0347 design review.
2. Separate design commit, post-commit review, publication and
   remote readback.
3. Separate prospective successor governance authorization.
4. Separately authorized implementation correction and review.
5. Separate corrected implementation freeze, publication, and
   exact remote readback.
6. Separate non-consuming preflight and receipt review.
7. Separate final safety disposition before considering the single
   remaining one-shot D0345 readiness attempt.

These are proposed checkpoints, not approvals for execution.

## 7. Noninterference

This D0347 design authoring does not modify any D0345 or D0346
artifact, implement the proposed correction, perform synthetic
conformance, read ZE0/ZE1 scientific payloads, inspect the reserved
ZE2 output root, start readiness, or execute ZE2.

**Readiness GO:** NO.

**ZE2 execution GO:** NO.

**C4:** UNRESOLVED. **P8 mapping:** NOT AUTHORIZED.
