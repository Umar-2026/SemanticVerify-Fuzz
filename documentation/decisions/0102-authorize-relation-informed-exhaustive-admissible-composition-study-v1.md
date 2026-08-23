# Decision 0102 — Authorize Relation-Informed Exhaustive Admissible Composition Study V1

Status: AUTHORIZED FOR AUTHORING ONLY — STUDY NOT YET AUTHORED

## Governance basis

Decision-0101 commit:

`dd42c933687f4f6282a5929a4f7769968aeef319`

Decision-0101 tree:

`0146cd005267ac356f5e7b94873996aab97ceb57`

Formalization V1 review chain is `PASS_CLOSED` and governance-approved with
bounded technical outcome:

`PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED`

Neither a positive existing-Schema-V2 mapping nor negative mapping
impossibility nor admissible-composition exhaustiveness is currently proven.

## Authoritative active Schema V2 binding

Path:

`config/schemas/protocol_specification.v2.schema.json`

SHA-256:

`c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956`

Size:

`43030`

Git blob:

`245fc02f538c21cff5de25f4a6a3c297e915e40f`

The worktree bytes are identical to the committed HEAD bytes.

Schema V2 modification is not authorized.

## Approved relation evidence

Relation artifact:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_semantic_role_relation_formalization_v1/02_v4_field_class_to_schema_v2_property_path_relation.v1.json`

SHA-256:

`239e6492faca3bb6da0c79abdb980470e2ea76690fc1f081562ccdbf7f303a32`

Traceability artifact:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_semantic_role_relation_formalization_v1/03_v4_semantic_unit_context_and_leaf_traceability.v1.json`

SHA-256:

`6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4`

The authorized study must preserve reviewed relation semantics:

- SEMANTICALLY_RELATED may be used as positive relation evidence;
- UNRESOLVED must not silently become positive relation evidence;
- NOT_SEMANTICALLY_RELATED is excluded from admissible semantic-storage use;
- lexical screening is not semantic proof;
- absence from prior screening is not negative proof;
- the two distinct 57-element field-class vocabularies must not be merged.

## Authorized study scope

Decision 0102 authorizes authoring only of:

`Schema-V2 Relation-Informed Exhaustive Admissible Composition Study V1`

The study must cover all 109 semantic units, all 17 losslessness requirements,
Schema-V2 structural admissibility, semantic-role compatibility, joint
cross-unit coexistence/collision constraints, and explicit finite-domain
exhaustiveness accounting.

Sound equivalence, dominance, or impossibility pruning is allowed only when
explicit and auditable.

Open or unconstrained string capacity alone is not semantic-losslessness proof.

## Allowed outcomes

Only:

1. `POSITIVE_EXISTING_V2_MAPPING_WITNESS_IDENTIFIED`;
2. `NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN`;
3. `FURTHER_EVIDENCE_REQUIRED`.

Search incompleteness must remain `FURTHER_EVIDENCE_REQUIRED`.

## Review boundary

The resulting study is author-candidate only.

Independent human review is required before governance use.

## One-time verifier lifecycle

The pre-study authorization verifier is created in:

`ACTIVE_UNCONSUMED`

state.

It is intentionally NOT executed by Decision 0102.

It may execute once immediately before study authoring starts. Its successful
output must be recorded byte-exactly. After that run the verifier is permanently
retired and must never be rerun after study authoring begins.

## Explicit non-authorizations

Decision 0102 does not authorize:

- operational V4-to-V2 mapping;
- operational mapping contract;
- active Schema V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution;
- repair.

Prohibited evidence remains prohibited.

## Authorization artifact bindings

Authorization record SHA-256:

`c0370ce7e52c7dfb74e375c1a5885119f5b086be759027dc8ae09d9db80c628d`

One-time pre-study verifier SHA-256:

`6781df3a0b4fcf1c8bc2ce59b7f017106ce2a158d15e68cf5557781532f77af2`

Checksum manifest SHA-256:

`949938100623931a3146beefa49fdfa4c6c2cd7eeaeb9249fe19843fb629e15c`

## Next boundary

`RUN_AUTHORIZATION_VERIFIER_ONCE_THEN_AUTHOR_RELATION_INFORMED_EXHAUSTIVE_ADMISSIBLE_COMPOSITION_STUDY_V1`
