# Independent Human Re-Review Form — D0222 Source-Backed Corrective Successor

## Reviewer-completed metadata

Reviewer name: Muhammad Nadeem Nadir

Reviewer role: Spec-Tecnical-Adjudicator-1

Review date: 03 / September / 2026

Reviewer confirmation / signature: MN_Lodhi

Independence attestation:
I confirm that I performed this re-review independently and that the
decisions, rationale, notes, and signature below are my own human judgments.

## Review target

Governed candidate:

Decision0222 — AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR

Corrective re-review scope:

- ASER04
- ASER07

Preserved PASS items are contextual non-regression constraints and are
not reopened:

- ASER01
- ASER02
- ASER03
- ASER05
- ASER06
- ASER08
- ASER09

Review basis:

Only the supplied ZIP and its included corrective-successor artifacts,
predecessor review, manifests and supporting records were considered.
Embedded author conclusions were assessed rather than accepted as proof.

---

# ASER04 — Re-review

## Correction A — Frozen source-unit metadata

Reviewer notes:

The revised specification replaces identifier-prefix inference and
synthetic constants with an explicit field-level join to the
checksum-bound traceability source:

- source_container = traceability.source_container
- source_path = traceability.source_path
- source_unit_kind = traceability.unit_kind
- source_provenance_sha256 = traceability.value_sha256

It requires exactly one traceability record per enumerated identifier,
rejects duplicate traceability identifiers, and requires equality
between the enumeration identifier set and the traceability unit_id
set. The complete traceability artifact has a separate fixed SHA-256
binding.

The AEA01 and AEA03 schemas now include the metadata needed for the
FC04 comparison. This addresses the predecessor metadata-design defect.

Limitation: the referenced enumeration and traceability source bytes
are not included in this ZIP. The derivation algorithm and binding
requirements can therefore be reviewed, but the actual source contents,
109-record correspondence and metadata values cannot be independently
reverified from this ZIP alone.

---

## Correction B — Uniqueness and count/coverage binding

Reviewer notes:

The revised design uses identifier-keyed maps, prohibits duplicate
JSON member names, and requires unique forward/reverse relation-array
members. The accompanying cross-artifact invariants bind:

- source identifiers to the fixed enumeration;
- carrier candidates to the frozen candidate source;
- frozen carriers to INCLUDED dispositions;
- forward-record keys to frozen U;
- reverse-record keys to frozen C;
- record counts to actual map membership;
- coverage summaries to independently recomputed domain and relation
  counts.

These rules address the requested uniqueness, cardinality and coverage
relationships at specification level. Duplicate JSON keys must be
rejected before parsing silently collapses them. Acceptance requires
both schema validation and the cross-artifact checks; schema validation
alone is insufficient.

No populated accounting evidence was evaluated.

---

## Correction C — Finalized AEA02 closure

Reviewer notes:

Finalized AEA02 now permits only INCLUDED or EXCLUDED dispositions.
The specification requires unresolved_count == 0 before freeze and
requires frozen C to equal exactly the candidate identifiers marked
INCLUDED. Candidate and carrier counts are tied to actual map sizes.

This addresses the predecessor unresolved-candidate and carrier-set
mismatch defects at specification level.

These closure rules establish consistency relative to the frozen
candidate source. They do not independently establish that the source
is authoritative or that each inclusion/exclusion is substantively
justified.

---

## Correction D — Hashing and canonicalization

Reviewer notes:

The in-band own-hash problem is addressed by detached hashing over
complete canonical artifact bytes.

The contract specifies integer-only numeric syntax, prohibits exponent
notation, leading zeroes and negative zero, defines UTF-8 ordering for
object names and identifier-set arrays, and preserves command argv
ordering.

However, deterministic JSON string serialization remains incomplete.
The contract specifies Unicode comparison and normalization behavior
but does not select an exact JSON escape representation.

For example:

{"s":"\n"}
{"s":"\u000a"}

Both decode to the same string containing U+000A, but their serialized
bytes and SHA-256 values differ. The supplied rules do not identify
which representation is canonical.

Required correction: define exact string and member-name escaping,
including control characters, quotation marks, backslashes, optional
escapes and non-ASCII characters. Provide canonical-byte and hash test
vectors demonstrating consistent serialization.

---

## ASER04 reviewer decision

[ ] PASS

[x] REVISION_REQUIRED

ASER04 rationale:

The revised metadata derivation, representable FC04 fields, uniqueness,
count/coverage relationships, finalized-C rules and detached hashing
substantially address the predecessor findings.

Nevertheless, the string-escaping gap prevents independent
implementations from deriving uniquely specified canonical bytes and
hashes. ASER04 should remain REVISION_REQUIRED until that contract is
completed.

The absence of the referenced source bytes is an additional ZIP-only
verification limitation, not evidence that those source claims are
false.

---

# ASER07 — Re-review

## Correction A — AEA03/AEA04 witness lineage

Reviewer notes:

AEA03 and AEA04 now define closed lineage objects requiring all nine
specified fields:

- witness_id
- creation_timestamp_utc
- creation_commit
- creation_commit_parent
- domain_freeze_commit
- u_domain_sha256
- c_domain_sha256
- predecessor_hashes
- derivation_input_hashes

Additional lineage fields are rejected. This corrects the predecessor
unrestricted-object defect.

Field presence and format do not prove lineage truth; independent
verification of the recorded relationships remains necessary.

---

## Correction B — Complete freeze record

Reviewer notes:

A separate closed complete-freeze-record schema is supplied. It
requires all 16 specified fields covering freeze identity and time,
freeze commit and parent, U/C paths and hashes, enumeration-source
identity, traceability-source identity, carrier-candidate-source
identity, predecessor hashes and derivation-input hashes.

The predecessor missing-schema and missing-field defects are addressed
at specification level. No actual freeze event is established by this
schema.

---

## Correction C — AEA05 freeze-event closure

Reviewer notes:

AEA05 embeds complete freeze-event metadata and separately binds the
complete freeze record by path and detached hash.

The embedded freeze-schema body matches the standalone freeze schema.
Invariant L04 requires the embedded metadata to equal the parsed
content of the checksum-bound complete freeze record.

This addresses the unverified-declaration defect at design level,
subject to resolving the shared canonical-string serialization issue
identified under ASER04.

---

## Correction D — Independently recomputed verifier evidence

Reviewer notes:

The revised verifier-output schema requires verifier identity and hash,
exact command argv, evaluated commits, evaluated Git objects and
SHA-256 values, individual check results, exit code, stdout/stderr
hashes and generation time.

AEA05 requires checksum-bound outputs for ancestry, immutable-domain
and C-domain-closure verification. V03 expressly requires later
satisfaction evaluation to independently recompute the required checks
rather than trust self-declared true booleans.

This materially corrects the previous verifier-evidence representation.
However, independently repeating an insufficient ancestry predicate
does not establish strict ordering. That remaining defect is recorded
under Correction E.

---

## Correction E — Ordering / freeze prerequisites

Reviewer notes:

The specification explicitly requires zero unresolved candidates and
exact equality between frozen C and the INCLUDED candidate set before
freeze.

Its phase sequence places U/C freeze before witness construction,
independent verifier-evidence closure before AEA05 provenance closure,
and AEA05 closure before satisfaction evaluation.

However, the specified ancestry predicate and invariant L02 require
only:

git merge-base --is-ancestor <domain_freeze_commit> <witness_commit>

with exit code 0.

This command also succeeds when both arguments identify the same
commit. A synthetic diagnostic confirmed that behavior. Consequently,
the specified check does not establish strict freeze-before-witness
commit ordering.

Required correction: require distinct freeze and witness commits
together with successful ancestry, and bind the checked commits to
the complete freeze record and witness lineage. Preserve explicit
anti-circular derivation restrictions. If the freeze checkpoint must
exclude witness artifacts, state and verify that tree-state condition.

This finding concerns the control specification; it does not allege
that an actual witness was constructed prematurely.

---

## ASER07 reviewer decision

[ ] PASS

[x] REVISION_REQUIRED

ASER07 rationale:

The closed witness-lineage schemas, complete freeze schema, AEA05
metadata equality and independently recomputed verifier-output
requirements address major predecessor deficiencies.

The remaining ancestry predicate nevertheless permits identical
freeze and witness commits. The intended phase sequence is not a
substitute for a check establishing strict ordering. ASER07 should
remain REVISION_REQUIRED until this condition is explicitly enforced.

---

# Overall independent human re-review decision

[ ] PASS

[x] REVISION_REQUIRED

Overall rationale:

The supplied package is internally checksum-consistent:

- Outer package checksum list: 25/25 matches.
- Governed-successor checksum list: 18/18 matches.
- Preconsumption checksum list: 10/10 matches.
- Candidate exact-copy inventory: all 19 listed files present.
- Preconsumption file bindings: all 10 hashes and byte sizes match.

The corrective successor substantially improves metadata derivation,
uniqueness, count/coverage binding, finalized-C closure, lineage
schemas, freeze records and verifier provenance.

Approval is not recommended because two technical gaps remain:

1. JSON string escaping is not uniquely specified, leaving canonical
   bytes and detached hashes ambiguous.

2. The ancestry predicate accepts identical freeze and witness commits,
   so it does not establish strict freeze-before-witness ordering.

Correct these contracts and include tests addressing the identified
counterexamples before the next review.

Additional reviewer notes:

The referenced enumeration and traceability source bytes are absent.
If the next review must independently verify source contents using
only its ZIP, include those existing checksum-bound source copies.
This does not request new accounting evidence or domain acquisition.

Preserved PASS items remain contextual and are not reopened or claimed
as freshly reproduced findings. The identified defects remain within
ASER04 and ASER07.

Historical PREBUILD/preconsumption status strings are explained by
the supplied governed-status overlay and are not treated as an
unresolved status contradiction.

Checksum agreement does not authenticate human identity, external
governance or repository history. No packaged verifier or one-time
authorization program was executed during this technical assessment.

This review does not establish Req06/Req14 satisfaction or violation,
semantic losslessness, governance approval or adoption. It authorizes
no accounting-evidence acquisition, U/C acquisition or freeze, witness
acquisition, concrete mapping, satisfaction determination, pair
reclassification, schema modification, analyzer execution, baseline
execution or repair.

Reviewer confirmation / signature: MN_Lodhi

Review date: 03 / September / 2026