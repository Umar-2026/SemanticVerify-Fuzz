# curl Mapping Contract V4 — Independent Human Technical Review
## Exact target
V4 SHA-256:
`9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070`
Size:
`26601`
Author checkpoint commit:
`390acaac338c1259dc67632d42db137707366e36`
Author checkpoint tree:
`f426da2294cda67aa89d5e062245d64ce2eb3a48`
Internal review target:
`Exact immutable V4 corrective schema-insufficiency proof.`
Author outcome:
`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`
This remains an author conclusion pending independent review.
For every item use exactly:
`PASS`
`REVISION_REQUIRED`
`FAIL`
### V4-RR01 — Portable original Git-object binding
Decision: PASS
Notes: The portable Git-object verifier completed successfully. Independent Git
object-ID recomputation confirmed checkpoint commit
390acaac338c1259dc67632d42db137707366e36, root tree
f426da2294cda67aa89d5e062245d64ce2eb3a48, config tree
81b8c745c8014897a530c0cfabaa9f0265e37e2a, config/annotation tree
75b41982c19e97e0a1aa31f09eb0a73601d936e1, and exact V4 blob
231ec484927a58e9515bb54789ede6b6abb95ac0.

The raw tree entries establish the exact repository path
config/annotation/curl_canonical_representation_mapping_contract.v4.json.
The supplied blob is byte-for-byte identical to
03_exact_v4_mapping_contract.v4.json, has size 26601 bytes, and has
SHA-256
9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070.

The handoff contains every raw Git object required to recompute the
checkpoint, root-tree binding, target path, target blob ID, exact bytes,
SHA-256, and size. Unrelated repository blob contents are not required for
this path-specific verification. The evidence is independently portable.

Run:
`17_git_object_proof/07_verify_git_object_proof.v1.py`
Independently verify the checkpoint commit object ID, root-tree binding,
`config/annotation` path, exact V4 blob object ID, V4 SHA-256, and V4 size.
Confirm the evidence is independently portable without requiring unrelated
repository blob contents.

### V4-RR02 — Correct successor and predecessor immutability
Decision: PASS
Notes: Exact V3 remains bound to SHA-256
ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97,
size 24750 bytes, author checkpoint
eeffef65a0ab2c9982e0cb708376635b096fec07, and tree
de149c84681855ca1b00f306df4f04cc6debe4d3.

The completed V3 review remains bound to SHA-256
96afd2a552443ecbdb321f8087612a0771838216272cb8fd43d14f8b8e203b14
and records 9 PASS, 1 REVISION_REQUIRED, and 0 FAIL, with overall decision
REVISION_REQUIRED. Its item-decision map confirms V3-RR01 through V3-RR09
passed and only V3-RR10 required revision.

The completed-review record identifies exact V3 as immutable and records
in_place_edit_authorized=false. Decision 0046 likewise requires the RR10
correction to use a separately authorized successor.

The V4 authorization separately identifies the versioned V4 target,
authorizes only corrective authoring, prohibits self-approval, and requires
a new independent review. Exact V4 has its own path, SHA-256, size,
checkpoint commit, and tree. V4 is therefore a separately authorized
corrective successor rather than an in-place rewrite of immutable V3.

Confirm exact V3 remains immutable with overall human decision
REVISION_REQUIRED and only V3-RR10 requiring correction.
Confirm exact V4 is a separately authorized corrective successor rather than
an in-place rewrite of V3.

### V4-RR03 — Exact V3-RR10 review-target correction
Decision: PASS
Notes: Exact V3 contains the stale value
"Exact immutable V2 schema-insufficiency proof." at
$.independent_review_requirement.review_target, matching the independently
recorded V3-RR10 defect.

The separately issued V4 corrective authorization requires the same JSON
location to contain exactly
"Exact immutable V4 corrective schema-insufficiency proof."

Independent inspection of exact V4 confirmed that its
independent_review_requirement.review_target exactly equals the authorized
V4 value. The V4 author-checkpoint record also identifies the old and new
values and records author_level_correction_complete=true.

The internal V4 review-target field now agrees with the V4 repository
binding, author checkpoint, review-package manifest, README, reviewer
packet, exact V4 SHA-256
9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070,
and versioned V4 path. Exact V4 therefore unambiguously identifies itself,
rather than V2 or V3, as the current independent-review target.

Confirm exact V3 contained the stale value:
`Exact immutable V2 schema-insufficiency proof.`
Confirm exact V4 contains at:
`$.independent_review_requirement.review_target`
exactly:
`Exact immutable V4 corrective schema-insufficiency proof.`
Confirm the current artifact therefore unambiguously identifies itself as the
independent review target.

### V4-RR04 — Preservation of V3 substantive proof semantics
Decision: PASS
Notes: Independent full-object comparison of exact V3 and exact V4 found only 10
leaf-level differences. Every difference is authorized successor or
governance metadata: contract kind, version, schema ID, purpose,
immutability wording, corrected review target, V3 predecessor binding, V4
authorization binding, corrective-successor metadata, and the versioned
next boundary.

The complete formal_insufficiency_argument is exactly equal between V3 and
V4, with identical canonical hash
a8bf99889bd7a8320d8cc702b9eaae0d7d309c77f485e73343356cd240e70f54.
The complete approved V4 representation-policy binding, semantic-container
hash map, frozen inventory, frozen-schema facts, all four structural
obstruction witnesses, retained V2 section hashes, scoped conclusion,
author outcome, and downstream non-authorizations are also exactly equal.

No protocol rule, obstruction, admissibility constraint, carrier
classification, losslessness requirement, representation-policy field,
verdict rule, accounting requirement, or scoped proof conclusion was
weakened or strengthened. Structural proof content outside the authorized
successor/governance metadata remains unchanged.

Confirm V4 preserves the substantive V3 frozen-schema insufficiency proof
without semantic weakening or strengthening.
Confirm structural proof content outside authorized successor/governance
metadata remains unchanged.

### V4-RR05 — Complete V4 representation-policy correction retained
Decision: PASS
Notes: Exact V4 retains the complete approved technical-V4 representation-policy
binding unchanged from exact V3. Independent comparison confirmed that
the V3 and V4 approved_v4_representation_policy_binding objects are
exactly equal.

The binding contains exactly the same 10 fields as approved technical V4,
with no missing, additional, or duplicate accounting entry. Its complete
exact_value object equals the approved representation_policy, every
field-accounting entry has accounting_status=EXPLICITLY_BOUND and
preservation_required=true, and every accounted exact value matches the
approved policy.

Independent canonical serialization produced SHA-256
dd645ad929e40bcfa2af2353817d55ad76596f464991f2417c4ac1b57c0be408,
matching the retained binding.

Ownership-sensitive and return-sensitive policy values both remain
explicitly bound with exact_value=true and preservation_required=true.
The formal required losslessness contract also retains
ownership_sensitive_semantics_preserved=true and
return_sensitive_semantics_preserved=true. The complete V3
representation-policy correction is therefore preserved in exact V4.

Confirm the complete exact approved 10-field curl V4 representation-policy
binding remains preserved.
Confirm ownership-sensitive and return-sensitive preservation remain explicit.

### V4-RR06 — Complete retained losslessness boundary
Decision: PASS
Notes: Exact V4 retains the complete 17-field V3 required losslessness contract.
Independent comparison found exact equality, with no missing V3 key and no
changed retained value.

V4 explicitly requires preservation of membership sensitivity, ownership
sensitivity, return sensitivity, path sensitivity, set-valued-state
reasoning, first-class UNKNOWN, the four-verdict contract, forward
accounting, and reverse accounting. The complete exact representation-policy
binding additionally preserves normative-strength uncertainty,
resource-centered semantics, synthetic_protocol_events_invented=false,
and the prohibition on silently converting UNKNOWN to VALID.

V4 explicitly requires all 10 approved semantic containers, all 64 rule
records, and all 3 exit obligations to be preserved/accounted for.
Independent recomputation confirmed exactly 10 matching semantic-container
hashes, rule-family counts of 10 global-runtime, 21 easy-handle, 29
multi-handle, and 4 cross-resource rules, totaling 64, and exactly 3 exit
obligations.

The machine-verdict inventory remains exactly VALID, VIOLATION-MUST,
VIOLATION-MAY, and UNKNOWN. No required semantic class, policy field,
verdict, rule record, exit obligation, or accounting direction was silently
dropped.

Confirm membership sensitivity, ownership sensitivity, return sensitivity,
path sensitivity, set-valued reasoning, first-class UNKNOWN, four-verdict
semantics, forward accounting, reverse accounting, all 10 semantic
containers, 64 rule records, and 3 exit obligations remain required.
Confirm no required semantic class is silently dropped.

### V4-RR07 — Structural obstruction and admissibility preservation
Decision: PASS
Notes: Independent deep comparison confirmed that exact V4 preserves all four
structural obstruction witnesses, the complete frozen inventory, the
complete frozen-schema structural facts, all admissibility constraints,
all five candidate-carrier classifications, the claim scope, theorem
identifier, and scoped proof conclusion exactly as V3.

The four witness records remain V2-O1 through V2-O4 and have identical
content and canonical hash
99d30d1dfe79d0c4505548311591d18159ba0adb1a3839cb20c5ce1849f2b7e9.
The frozen inventory and frozen-schema structural-fact hashes also match
exactly.

All admissibility constraints remain unchanged, and the carrier classes
retain their original INADMISSIBLE or ABSENT_FOR_REQUIRED_V4_CONCEPTS
classifications. The scoped proof conclusion and its limitation excluding
a universal mathematical-impossibility claim for every arbitrary encoding
are unchanged.

No structural obstruction, inventory fact, schema fact, admissibility
constraint, carrier classification, theorem scope, or proof conclusion was
added, removed, weakened, or strengthened.

Confirm all four retained structural obstruction witnesses, frozen inventory,
frozen-schema structural facts, admissibility constraints, candidate carrier
classifications, and scoped proof conclusion remain preserved.

### V4-RR08 — Corrected frozen-schema insufficiency conclusion
Decision: PASS
Notes: Under the corrected V4 governance target and complete retained
losslessness boundary, the scoped frozen-schema insufficiency conclusion
remains supported.

V4 now unambiguously identifies the exact immutable V4 corrective proof as
its independent-review target. Its complete 17-field required losslessness
contract is exactly equal to V3 and retains the complete representation
policy, ownership and return sensitivity, membership and path sensitivity,
set-valued reasoning, first-class UNKNOWN, four-verdict semantics, forward
and reverse accounting, all 10 semantic containers, 64 rules, and 3 exit
obligations.

The retained four-verdict and feasible-state join obstruction remains
independently decisive. The frozen schema has no same-purpose first-class
carrier for the four machine verdicts, feasible-state join policy,
first-class UNKNOWN, or the rule prohibiting silent conversion of UNKNOWN
to VALID.

Adding a carrier would require schema modification or supersession.
Opaque string packing, synthetic semantic events, and repurposing protocol
fields for machine-policy semantics remain inadmissible. The V4 governance
correction creates no new carrier and changes no admissibility constraint.

No admissible deterministic lossless forward-and-reverse mapping under the
exact current constraints was identified. The conclusion remains limited
to the exact frozen schema, exact approved technical-V4 semantics, and
retained authorization/admissibility constraints. It is not a claim that
every theoretically imaginable arbitrary encoding is mathematically
impossible.

Under the exact corrected V4 governance and complete losslessness boundary,
determine whether the scoped conclusion remains supported:

`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`

This is not a claim that every theoretically imaginable arbitrary encoding is
mathematically impossible.

### V4-RR09 — No unauthorized semantic, schema, or materialization action
Decision: PASS
Notes: Exact V4 does not add, remove, or change protocol rules. The substantive V3 and V4 protocol-semantic bindings, frozen inventory, structural facts, obstruction witnesses, losslessness requirements, admissibility constraints, and carrier classifications remain unchanged.
V4 explicitly records protocol-rule addition, removal, and semantic change; semantic protocol-event invention; opaque payload packing; and frozen-schema modification as not allowed.
The packaged frozen canonical schema has SHA-256:
7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34
This exactly matches the V4 frozen-schema binding and the predecessor V3 binding.
V4 records that no positive mapping algorithm is defined or approved, canonical materialization is not safe or authorized, and curl.json is neither authorized nor created. Independent enumeration of the handoff archive found no curl.json member.

Confirm V4 does not add/remove/change protocol rules, invent semantic protocol
events, use opaque payload packing, modify the frozen canonical schema,
approve a positive mapping, or create `curl.json`.

### V4-RR10 — Governance consequence and next boundary
Decision: PASS
Notes: Approval of exact V4 establishes only the independently reviewed technical need for a separately governed canonical-schema-successor process. V4 records that a schema successor is technically required, but it is not authorized by this contract or by this review.
V4 does not authorize canonical-schema-successor authoring, canonical-schema modification, curl.json materialization, analyzer implementation or execution, baseline execution, positive-mapping approval, or repair.
The V4 checkpoint record marks exact V4 as immutable after its author checkpoint. The V4 immutability policy requires any later correction to use another separately authorized successor. Exact V4 must therefore remain immutable after review.

Confirm approval of exact V4 would establish only the independently reviewed
technical need for a separately governed canonical-schema-successor process.
Confirm V4 itself does not authorize schema-successor authoring, schema
modification, `curl.json`, analyzer implementation/execution, baseline
execution, or repair.
Confirm exact V4 must remain immutable after review.

## Overall technical review decision
Choose exactly one:
`APPROVE_V4_RR10_CORRECTED_SCHEMA_INSUFFICIENCY_PROOF`
`REVISION_REQUIRED`
`FAIL`

Overall decision: APPROVE_V4_RR10_CORRECTED_SCHEMA_INSUFFICIENCY_PROOF
Notes: All V4-RR01 through V4-RR10 are assessed PASS based on the reviewed primary evidence. Final package verification passed, including the exact V4 SHA-256 and size, portable Git-object binding, exact V4 self-review target, V3-RR10 correction, and preservation of V3 substantive proof semantics.
The corrected complete losslessness boundary supports the scoped conclusion:
FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED
This approval establishes only the independently reviewed technical need for a separately governed canonical-schema-successor process. It does not authorize schema-successor authoring, schema modification, a positive mapping, curl.json, analyzer implementation or execution, baseline execution, or repair.

Exact V4 must remain immutable. No quarantined evidence was used.
## Reviewer identity
Reviewer role ID: `Spec-Technical-Reviewer-1`
Human reviewer name: Abdul Raheem Shahzad
Human reviewer signature / recorded confirmation: ARS
Human reviewer date: 20 / August / 2026

## Evidence quarantine
Do not use generated-driver source, selected-sample membership, raw model
responses, generated-driver compiler-log semantic content, gold labels,
analyzer output, baseline output, LLM-review output, or repair output.

## Post-review rule
No synthetic or assistant-generated human approval is permitted.
Exact V4 remains immutable after its author checkpoint.
Approval of this proof does not authorize a canonical-schema successor or
`curl.json`.