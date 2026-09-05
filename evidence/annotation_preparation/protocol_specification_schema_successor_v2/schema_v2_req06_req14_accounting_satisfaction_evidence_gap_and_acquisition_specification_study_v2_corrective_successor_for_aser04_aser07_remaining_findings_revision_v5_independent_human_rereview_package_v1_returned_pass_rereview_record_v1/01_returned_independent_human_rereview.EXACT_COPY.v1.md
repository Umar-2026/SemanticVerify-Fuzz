# D0227 Independent Human Re-Review Form — Manual Review Copy

## Review target

Decision0227 — `AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR`

Corrective scope:

- ASER04
- ASER07

The corrective candidate remains unapproved and unadopted unless a later
governance decision records the result of this independent human re-review.

## Reviewer metadata

Reviewer name: Muhammad Nadeem Nadir

Reviewer role:Spec-Tech-Reviewer-1

Review date: 05/September/2026

Reviewer confirmation / signature: MN_Lodhi

## Independence attestation

[x] I confirm that I performed this re-review independently and that the
      selections and rationale below are my own review conclusions.

---

# ASER04 — Canonical JSON string/member-name serialization

## Review question

Does D0227 now provide an unambiguous, deterministic canonical JSON
string/member-name serialization rule sufficient to derive one canonical byte
sequence and SHA-256 value from a parsed JSON value?

Please independently examine at least:

- `corrective_successor_exact/02_accounting_evidence_canonicalization_and_detached_hash_rules.v5.json`
- `corrective_successor_exact/03_canonical_json_string_test_vectors.v1.json`
- `corrective_successor_exact/06_cross_artifact_machine_invariants.v3.json`
- the predecessor V4 canonicalization copy under
  `corrective_successor_exact/predecessor_support_exact/`

Specific points to verify:

1. canonicalization acts on the parsed Unicode scalar-value sequence rather
   than preserving arbitrary original JSON escape spelling;
2. quotation mark and reverse solidus have exactly one canonical spelling;
3. U+0000 through U+001F have exactly one canonical `\u00xx`-style spelling;
4. short JSON escapes do not create alternate canonical encodings;
5. solidus handling is fixed;
6. non-ASCII scalar values have a fixed UTF-8 representation;
7. Unicode normalization policy is explicit;
8. member names use the same emission rule;
9. canonical test vectors reproduce the declared bytes and SHA-256 values;
10. semantically equivalent escape spellings converge to one canonical byte
    representation where the specification says they must.

## ASER04 reviewer decision

[x] PASS
[ ] REVISION_REQUIRED

Reviewer rationale:

D0227 now defines an unambiguous parsed-value-to-canonical-byte
algorithm for JSON strings and member names. Independent recomputation
confirmed all 11 canonical byte/hash vectors and all 16 alternative
source spellings, including the \n versus \u000a counterexample.

---

## ASER07 reviewer decision

[x] PASS
[ ] REVISION_REQUIRED

Reviewer rationale:

D0227 now requires distinct freeze and witness commits, successful
Git ancestry, and exact bindings to the freeze record and witness
lineage. All five ordering vectors recomputed correctly. The
identical-commit case correctly returns FAIL despite successful
non-strict Git ancestry.

---

## Overall independent human re-review decision

[x] PASS
[ ] REVISION_REQUIRED

Overall rationale:

The two remaining D0222 findings are technically resolved. Both
checksum manifests close without mismatch (29/29 and 22/22). The
included source copies match their declared hashes and contain 18,639
unique pairs over 109 source units and 171 carrier paths. The 109
enumerated source-unit IDs exactly match the 109 traceability IDs.

This bounded PASS concerns specification sufficiency only. It does
not establish Req06/Req14 accounting satisfaction, create accounting
evidence, authorize downstream activity, or constitute governance
adoption.

Additional reviewer notes:

The package remains an AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR. This
bounded PASS does not itself constitute governance approval or
adoption.

The package records external handoff, returned-review receipt and
returned-review recording as incomplete. A separate authorized
governance action is required to advance those lifecycle states.

The included enumeration and traceability artifacts are existing
checksum-bound source copies. Their inclusion resolves the prior
ZIP-only availability limitation but does not constitute new accounting
evidence or domain acquisition.

This review does not establish Req06 or Req14 satisfaction or
violation, prove Schema-V2 semantic losslessness, or authorize domain
freeze, witness acquisition, concrete mapping, pair reclassification,
schema modification, analyzer execution, baseline execution or repair.

Checksum agreement establishes package byte consistency but does not
authenticate reviewer identity or external repository history.

The D0226 R03 material was treated only as supplied authorization-history
evidence. The retired verifier was not rerun.

Reviewer identity, independence confirmation, signature and review date
must be completed by the actual human reviewer.