# D0227 Independent Human Re-Review Form — Manual Review Copy

## Review target

Decision0227 — `AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR`

Corrective scope:

- ASER04
- ASER07

The corrective candidate remains unapproved and unadopted unless a later
governance decision records the result of this independent human re-review.

## Reviewer metadata

Reviewer name:

Reviewer role:

Review date:

Reviewer confirmation / signature:

## Independence attestation

- [ ] I confirm that I performed this re-review independently and that the
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

- [ ] PASS
- [ ] REVISION_REQUIRED

ASER04 reviewer rationale / required correction if any:


---

# ASER07 — Strict freeze-before-witness ordering

## Review question

Does D0227 now establish strict, machine-checkable freeze-before-witness
ordering rather than merely non-strict Git ancestry?

Please independently examine at least:

- `corrective_successor_exact/04_future_domain_freeze_lineage_and_ordering_control.v5.json`
- `corrective_successor_exact/05_strict_freeze_before_witness_test_vectors.v1.json`
- `corrective_successor_exact/06_cross_artifact_machine_invariants.v3.json`
- the copied complete-freeze and independent-verifier schemas under
  `corrective_successor_exact/predecessor_support_exact/`

Specific points to verify:

1. freeze commit and witness creation commit must be distinct;
2. `git merge-base --is-ancestor freeze_commit witness_commit` must succeed;
3. the identical-commit counterexample fails despite Git ancestry success;
4. the checked freeze commit is bound to the checksum-bound complete freeze
   record;
5. the checked witness commit is bound to witness lineage;
6. the required verifier checks cannot be replaced by a self-declared boolean;
7. the stated tree-exclusion position is technically adequate and does not
   silently weaken strict temporal ordering.

## ASER07 reviewer decision

- [ ] PASS
- [ ] REVISION_REQUIRED

ASER07 reviewer rationale / required correction if any:


---

# Existing source-byte availability

The package now contains exact checksum-bound copies of both sources that were
absent from the previous ZIP-only review:

- semantic-unit enumeration source;
- semantic-unit traceability source.

Please verify whether their inclusion resolves the prior source-byte
availability limitation relevant to this re-review.

Source-byte availability comments:


---

# Preserved items

The following prior PASS items are context only and are not reopened by this
focused re-review unless the reviewer identifies a direct contradiction caused
by the D0227 ASER04/ASER07 correction:

- ASER01
- ASER02
- ASER03
- ASER05
- ASER06
- ASER08
- ASER09

---

# Overall independent human re-review decision

- [ ] PASS
- [ ] REVISION_REQUIRED

Overall rationale:


Additional reviewer notes:


