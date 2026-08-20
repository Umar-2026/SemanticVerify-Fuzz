# curl Mapping Contract V3 — Independent Human Technical Review

## Exact target

V3 SHA-256:

`ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97`

Size:

`24750`

Author checkpoint commit:

`eeffef65a0ab2c9982e0cb708376635b096fec07`

Author checkpoint tree:

`de149c84681855ca1b00f306df4f04cc6debe4d3`

Author outcome:

`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`

This remains an author conclusion pending independent review.

For every item use exactly:

`PASS`

`REVISION_REQUIRED`

`FAIL`

### V3-RR01 — Portable original Git-object binding
Decision: PASS
Notes: The portable Git-object verifier completed successfully. Independent Git
object-ID recomputation confirmed checkpoint commit
eeffef65a0ab2c9982e0cb708376635b096fec07, declared root tree
de149c84681855ca1b00f306df4f04cc6debe4d3, config tree
bb5b4b4e1c0cc695af56a47385f40b1a45e4189f, config/annotation tree
c354db29238056a4d34ac0546ed5bc10e4e723aa, and exact V3 blob
000d7e3e811bf6f34821ac967d8a6c9f520e1388.

The raw tree entries establish the complete path
config/annotation/curl_canonical_representation_mapping_contract.v3.json.
The supplied blob is byte-for-byte identical to
03_exact_v3_mapping_contract.v3.json, has size 24750 bytes, and has
SHA-256
ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97.

The evidence includes every Git object required to recompute the checkpoint
commit, root-tree binding, target path, and target blob while deliberately
excluding unrelated repository blob contents. Those unrelated contents are
not required to verify this path-specific binding. The predecessor RR01
portability problem is therefore resolved.

Run `17_git_object_proof/07_verify_git_object_proof.v1.py`.

Independently confirm the original checkpoint commit object ID, its declared
root tree, the tree path `config/annotation`, the exact V3 blob object ID,
V3 SHA-256, and V3 size.

Confirm the evidence is sufficient to resolve the predecessor RR01 portability
problem without requiring access to unrelated repository blob contents.

### V3-RR02 — Correct successor and predecessor immutability
Decision: PASS
Notes: Exact V2 remains bound to SHA-256
f2badbc07895e8baff078a0ce617ceb6ff02d39c7634a9e38b3b8a46a18d811c
and size 18515 bytes. The completed V2 review remains bound to SHA-256
d688196db67da6cf9e359046ab612e78117fc54c9166122a9523729270df50d5
and records 8 PASS, 2 REVISION_REQUIRED, and 0 FAIL, with overall decision
REVISION_REQUIRED.

The completed-review record retains V2-RR01=REVISION_REQUIRED and
V2-RR08=REVISION_REQUIRED. It explicitly records that later local Git
verification does not retroactively change the V2-RR01 human decision.
Decision 0043 preserves the same historical result.

The V3 authorization identifies exact V2 as immutable and records
in_place_edit_authorized=false. Decision 0044 separately authorizes only
a V3 corrective successor and expressly preserves the V2-RR01
REVISION_REQUIRED result.

Exact V3 is a distinct versioned artifact with SHA-256
ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97,
size 24750 bytes, and its own author checkpoint. V3 is therefore a
separately authorized corrective successor rather than an in-place or
retroactive rewrite of V2.

Confirm exact V2 remains immutable, its human decision remains
REVISION_REQUIRED, and V3 is a separately authorized corrective successor.

Confirm the V2 RR01 human decision has not been retroactively rewritten.

### V3-RR03 — Complete exact V4 representation-policy binding
Decision: PASS
Notes: Exact approved curl V4 contains a 10-field representation_policy object.
Independent field-set comparison confirmed that V3 binds exactly those 10
fields with no missing, additional, or duplicate accounting entry.

V3 records field_count=10 and provides the complete exact policy object
under approved_v4_representation_policy_binding.exact_value. That object
is semantically identical to exact V4 representation_policy.

Every field-accounting record has
accounting_status=EXPLICITLY_BOUND and preservation_required=true. Each
recorded exact value matches V4, including
synthetic_protocol_events_invented=false and the complete exact
set_valued_state_reasoning string.

Independent canonical serialization and SHA-256 computation produced
dd645ad929e40bcfa2af2353817d55ad76596f464991f2417c4ac1b57c0be408,
matching V3's canonical_semantic_sha256.

The formal required losslessness contract also requires both
complete_exact_v4_representation_policy_machine_checkably_bound=true and
complete_exact_v4_representation_policy_preserved=true. The complete exact
V4 representation-policy boundary is therefore explicitly and
machine-checkably bound.

Confirm V3 binds the complete exact 10-field V4 `representation_policy`.

Confirm canonical semantic SHA-256:

`dd645ad929e40bcfa2af2353817d55ad76596f464991f2417c4ac1b57c0be408`

Confirm every field has exact-value accounting and preservation_required=true.

### V3-RR04 — Ownership-sensitive preservation
Decision: PASS
Notes: Exact V2 did not contain
ownership_sensitive_semantics_preserved inside its formal required
losslessness contract, confirming the ownership-related omission recorded
by V2-RR08.

The V3 corrective authorization explicitly requires ownership-sensitive
semantic preservation. Exact V3 now contains
ownership_sensitive_semantics_preserved=true directly inside
formal_insufficiency_argument.required_losslessness_contract.

Exact approved V4 records representation_policy.ownership_sensitive=true.
V3 binds that exact value, and the corresponding field-accounting record
has exact_value=true, preservation_required=true, and
accounting_status=EXPLICITLY_BOUND.

The required ownership-sensitive semantic class is therefore explicitly
included in the corrected formal losslessness boundary. This closes the
ownership-related V2-RR08 omission without modifying immutable V2.

Confirm `ownership_sensitive_semantics_preserved=true` is explicitly inside
the formal required losslessness contract.

Confirm this closes the ownership-related V2-RR08 omission.

### V3-RR05 — Return-sensitive preservation
Decision: PASS
Notes: Exact V2 did not contain return_sensitive_semantics_preserved inside its
formal required losslessness contract, confirming the return-related
omission identified by V2-RR08.

The V3 corrective authorization explicitly requires return-sensitive
semantic preservation. Exact V3 now contains
return_sensitive_semantics_preserved=true directly inside
formal_insufficiency_argument.required_losslessness_contract.

Exact approved V4 records representation_policy.return_sensitive=true.
V3 binds that exact value, and its corresponding field-accounting record
has exact_value=true, preservation_required=true, and
accounting_status=EXPLICITLY_BOUND.

Return-sensitive semantics are therefore explicitly included in the
corrected formal losslessness boundary. This closes the return-related
V2-RR08 omission without modifying immutable V2.


Confirm `return_sensitive_semantics_preserved=true` is explicitly inside the
formal required losslessness contract.

Confirm this closes the return-related V2-RR08 omission.

### V3-RR06 — Complete retained semantic-accounting boundary
Decision: PASS
Notes: Exact V3 retains every key and value from the V2 formal required
losslessness contract. Independent comparison found no missing V2 key and
no changed retained value. The retained contract explicitly requires
membership sensitivity, path sensitivity, set-valued-state reasoning,
first-class UNKNOWN, the four-verdict contract, forward accounting,
reverse accounting, all 10 V4 semantic containers, all 64 rule records,
and all 3 exit obligations.

Independent recomputation confirmed that V3 binds exactly 10 approved V4
semantic containers and that every recorded container hash matches exact
V4. Exact V4 contains 10 global-runtime, 21 easy-handle, 29 multi-handle,
and 4 cross-resource rules, totaling 64, together with 3 exit obligations.
These counts match V3's frozen inventory.

The four allowed verdicts remain exactly VALID, VIOLATION-MUST,
VIOLATION-MAY, and UNKNOWN. Complete representation-policy preservation
also retains the rule that UNKNOWN must never silently become VALID.

V3 adds seven corrective requirements covering the complete exact V4
representation policy, ownership sensitivity, return sensitivity,
normative-strength uncertainty, resource-centered semantics, and the
false synthetic-event policy. No original required semantic class is
missing or weakened, and no newly required representation-policy field is
silently dropped.


Confirm V3 also retains membership sensitivity, path sensitivity,
set-valued-state reasoning, first-class UNKNOWN, four-verdict semantics,
forward accounting, reverse accounting, all 10 V4 semantic containers,
64 rule records, and 3 exit obligations.

Confirm no required semantic class is silently dropped.

### V3-RR07 — Preservation of valid V2 proof evidence
Decision: PASS
Notes: Independent deep comparison of exact V2 and exact V3 confirmed that the
frozen inventory, frozen-schema structural facts, all four structural
obstruction witnesses, admissibility constraints, candidate carrier
classes, claim scope, theorem identifier, proof conclusion, author
outcome, and approved V4 semantic-container hash map are unchanged.

All hashes recorded in V3's v2_preserved_proof_section_hashes were
independently recomputed from exact V2 and matched. The four retained
witnesses remain exactly V2-O1 through V2-O4, and the five considered
carrier classes retain their original classifications and reasons.

No retained proof fact, obstruction, admissibility rule, or scoped
conclusion was weakened or strengthened. V3's substantive additions are
limited to the corrected complete representation-policy and formal
losslessness-accounting requirements authorized in response to V2-RR08.
The valid V2 proof evidence is therefore preserved exactly.


Confirm V3 preserves the V2 frozen inventory, frozen-schema structural facts,
four structural obstruction witnesses, admissibility constraints, considered
carrier classes, and scoped proof conclusion without semantic weakening or
strengthening.

### V3-RR08 — Corrected frozen-schema insufficiency conclusion
Decision: PASS
Notes: Under V3's corrected complete required losslessness boundary, the scoped
frozen-schema insufficiency conclusion remains supported. The corrected
contract contains 17 explicit preservation/accounting requirements,
including the complete exact V4 representation policy, ownership
sensitivity, return sensitivity, all retained V2 requirements, and
forward and reverse accounting.

The retained V2-O2 witness remains independently decisive. Exact approved
V4 requires four machine verdicts, feasible-state verdict joining,
first-class UNKNOWN, and the rule that UNKNOWN must never silently become
VALID. Independent inspection of the frozen canonical schema found no
same-purpose first-class structural carrier for those machine-policy
semantics.

Adding a carrier would require schema modification or supersession.
Packing the semantics into free-form strings would violate the opaque
payload prohibition. Inventing API, branch, or function-exit events would
violate the synthetic-event prohibition. Using protocol states,
transitions, or obligations for machine-verdict and join-policy meanings
would repurpose their defined semantics.

The V3 corrective additions do not remove or weaken this obstruction and
cannot create a previously absent admissible carrier. No admissible
deterministic lossless forward-and-reverse mapping under the exact current
constraints was identified.

The conclusion remains deliberately scoped to the exact frozen schema,
exact approved V4 semantics, and exact authorization/admissibility
constraints. It is not a claim that every theoretically imaginable
arbitrary encoding is mathematically impossible.

Under the corrected complete losslessness boundary, determine whether the
scoped conclusion remains supported:

`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`

Do not interpret this as a claim that every theoretically imaginable arbitrary
encoding is mathematically impossible.

### V3-RR09 — No unauthorized semantic or schema action
Decision: PASS
Notes: Exact V3 preserves the V2 approved-V4 semantic-container hash map, frozen
inventory, and all four structural obstruction witnesses. The bound
inventory remains 64 protocol rules across the same four rule families,
and no semantic-container hash changed. No protocol rule was added,
removed, strengthened, weakened, or semantically changed.

V3 retains semantic_protocol_event_invention_allowed=false and binds the
exact V4 policy synthetic_protocol_events_invented=false with preservation
required. It also retains opaque_payload_packing_allowed=false and the
classification of opaque free-form string encoding as inadmissible.

The frozen canonical schema remains byte-bound by SHA-256
7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34.
V3 records schema_modification_allowed=false,
schema_successor_creation_allowed=false, and
canonical_schema_successor_authorized=false.

V3 defines and approves no positive mapping:
positive_mapping_algorithm_defined=false,
positive_mapping_algorithm_approved=false,
positive_mapping_candidate_authored=false, and
lossless_v4_to_frozen_schema_mapping_proven=false.

V3 records curl_json_creation_authorized=false, curl_json_created=false,
and canonical_materialization_safe=false. No curl.json file is present in
the handoff. V3 therefore performs no unauthorized protocol-semantic,
schema, mapping, or canonical-materialization action.

Confirm V3 does not add/remove/change protocol rules, invent semantic protocol
events, use opaque payload packing, modify the frozen schema, define an
approved positive mapping, or create `curl.json`.

### V3-RR10 — Governance consequence
Decision: REVISION_REQUIRED
Notes: Exact V3 correctly distinguishes technical schema-successor necessity from
governance authorization. It records
canonical_schema_successor_required=true while separately recording
canonical_schema_successor_authorized=false and
schema_successor_authorized_by_this_contract=false.

V3 also correctly leaves schema-successor authoring, analyzer
implementation and execution, baseline execution, repair, schema
modification, positive mapping approval, and curl.json materialization
unauthorized. Its immutability policy correctly states that exact V3 is
immutable after the author checkpoint and that any further correction
requires a separately authorized successor.

However, exact V3 contains an incorrect predecessor review-target binding
at $.independent_review_requirement.review_target. Its value is:

"Exact immutable V2 schema-insufficiency proof."

This V3 review must target exact immutable V3, not V2. The field conflicts
with the V3 repository binding, author checkpoint, review-package manifest,
and reviewer packet, all of which identify exact V3 SHA-256
ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97
as the current review target.

Required correction: keep exact V3 immutable and create a separately
authorized corrective successor whose independent_review_requirement
unambiguously identifies the exact immutable corrective-successor artifact
as its review target. Preserve all current non-authorizations, proof
semantics, representation-policy corrections, portable Git-object
requirements, and immutability rules. The corrected successor must receive
a new author checkpoint and independent human review.

No schema-successor authoring or downstream action is authorized by this
revision-required decision.

Confirm approval of V3 would establish only an independently reviewed
technical need for a separately governed canonical-schema-successor process.

Confirm V3 itself does not authorize schema-successor authoring, analyzer
implementation/execution, baseline execution, or repair.

Confirm exact V3 must remain immutable after review.

## Overall technical review decision

Choose exactly one:

`APPROVE_V3_CORRECTED_SCHEMA_INSUFFICIENCY_PROOF`

`REVISION_REQUIRED`

`FAIL`
Overall decision: REVISION_REQUIRED
Notes: Exact V3 successfully resolves both defects identified by the completed V2
review. It includes portable Git-object evidence that independently binds
the V3 checkpoint commit, root tree, config/annotation path, exact V3 Git
blob, SHA-256, and size. It also corrects the V2-RR08 accounting omission
by explicitly preserving ownership-sensitive semantics, return-sensitive
semantics, and the complete exact 10-field approved V4
representation_policy.

V3 retains all valid V2 proof evidence without semantic weakening or
strengthening, including the frozen inventory, frozen-schema structural
facts, four obstruction witnesses, admissibility constraints, considered
carrier classes, and scoped proof conclusion. The corrected complete
losslessness boundary retains all 10 V4 semantic containers, 64 rule
records, 3 exit obligations, four verdicts, membership and path
sensitivity, set-valued reasoning, first-class UNKNOWN, and forward and
reverse accounting.

The scoped technical conclusion
FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED
remains supported. V3 performs no unauthorized protocol-rule, schema,
positive-mapping, synthetic-event, opaque-packing, or curl.json action.

However, exact V3 cannot be approved because its internal governance
binding at $.independent_review_requirement.review_target incorrectly
states:

"Exact immutable V2 schema-insufficiency proof."

The current independent review target is exact immutable V3, SHA-256
ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97.
Although the V3 repository binding, author checkpoint, package manifest,
and reviewer packet correctly identify V3, the contradictory internal
review_target field prevents an unambiguous V3 governance boundary.

Required correction: exact V3 must remain immutable. Create a separately
authorized corrective successor whose independent_review_requirement
unambiguously identifies that exact successor artifact as the review
target. Preserve the complete V3 proof, portable Git-object requirements,
representation-policy corrections, all non-authorizations, and the
immutability policy. Establish a new author checkpoint and conduct a new
independent human review.

This REVISION_REQUIRED decision does not authorize canonical-schema
successor authoring, schema modification, curl.json, a positive mapping,
analyzer implementation or execution, baseline execution, or repair.


## Reviewer identity
Reviewer role ID: `Spec-Technical-Reviewer-1`
Human reviewer name: Abdul Raheem Shahzad
Human reviewer signature / recorded confirmation: ARS
Human reviewer date: 20 / August / 2026

## Evidence quarantine

Do not use generated-driver source, selected-sample membership, raw model
responses, compiler-log semantic contents, gold labels, analyzer output,
baseline output, LLM-review output, or repair output.

## Post-review rule

No synthetic or assistant-generated human approval is permitted.

Exact V3 remains immutable.

Approval does not authorize a schema successor or `curl.json`.