# Decision 0090 — Record Schema-V2 Semantic-Role Relation Formalization V1 Author Checkpoint

Status: AUTHOR-CANDIDATE ADDITIONAL CAPABILITY EVIDENCE RECORDED — HUMAN REVIEW REQUIRED

## Authorization basis

Decision 0089 authorized Schema-V2 Semantic-Role Relation Formalization V1
under the human-approved bounded result:

`FURTHER_EVIDENCE_REQUIRED`

Decision-0089 commit:

`68f78c52e70e3f9b7a4efa62b8dfb4c85f299ede`

Decision-0089 authorization SHA-256:

`d2e6199f18f9b352992f0a2ee22190e1d173fcf52ae79f9b7c59883c1e4b6594`

## Corrected reviewed-domain basis

The formalization does not use an all-scalar raw-V4 traversal as the
531-leaf domain.

Its authoritative reviewed domains are:

- 531 leaf-field records from the reviewed semantic-unit inventory;
- 109 semantic units from the reviewed semantic-unit inventory;
- 57 `field_class_analysis[].v4_field_class` identifiers from the reviewed
  candidate composition matrix;
- 171 Schema-V2 property paths from the reviewed carrier inventory;
- 123 distinct Schema-V2 property names; and
- 59 open unconstrained Schema-V2 string carrier paths.

## Important two-domain distinction

The reviewed evidence contains two distinct 57-element vocabularies:

1. the union of semantic-unit inventory `field_classes`; and
2. the composition-matrix `field_class_analysis[].v4_field_class` domain.

The two sets are not equal.

Decision 0090 does not assert equivalence between them.

The 57 x 171 semantic-role relation is defined only over the reviewed
composition-matrix `v4_field_class` domain.

The semantic-unit inventory vocabulary remains separate traceability
metadata for the 531 leaves and 109 semantic units.

## Conservative complete pair partition

All 9,747 matrix-field-class / Schema-V2-property-path pairs are accounted
for.

- SEMANTICALLY_RELATED: 113
- NOT_SEMANTICALLY_RELATED: 969
- UNRESOLVED: 8,665
- lexical-screening-only pairs retained as unresolved: 125

SEMANTICALLY_RELATED is assigned only to pairs already explicitly curated
as semantically related candidate paths in Capability Study V1.

NOT_SEMANTICALLY_RELATED is assigned only where the Schema-V2 carrier is
under semantic_accounting, because reviewed admissibility rules explicitly
forbid semantic_accounting as substitute semantic storage.

All other pairs remain UNRESOLVED.

Absence from earlier candidate screening is not used as negative proof.

Lexical screening alone is not promoted to semantic relatedness.

## Traceability

All 531 reviewed leaf records are preserved in the traceability artifact.

All 109 semantic units are bound to their corresponding reviewed unit
analysis and candidate Schema-V2 carrier families.

Carrier-family expansion is retained only as future-screening context and
does not automatically classify every member path as semantically related.

## Formalization artifacts

Summary SHA-256:

`0efc848991f0f1580542b8d6e380c55df6d2b370147f236800621b24b51ee600`

57 x 171 relation SHA-256:

`239e6492faca3bb6da0c79abdb980470e2ea76690fc1f081562ccdbf7f303a32`

531-leaf / 109-unit traceability SHA-256:

`6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4`

Markdown report SHA-256:

`7b71d98c63afabc6d3b5eaf72f07e0ee2e4a6707520d80032a9d51b9540878d4`

Safe verifier SHA-256:

`842763889dd0958a39b9403832c97d2ea83cbbf8c91bc529931323f3e62f38b0`

Checksum manifest SHA-256:

`46cbb87c47ce4332c98a80bd769346129d7a54f5cb6aa037d62a7016025e45f6`

## Author-candidate outcome

Selected outcome:

`PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED`

Human-approved:

`NO`

Independent human technical review is required before governance use.

## Bounded technical meaning

`POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO`

`NEGATIVE_EXISTING_V2_MAPPING_PATH_IMPOSSIBILITY_PROVEN=NO`

`ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO`

No constructive positive mapping witness has been authored.

No exhaustive admissible-composition enumeration has been performed.

No schema-successor requirement has been determined.

## Decision-0089 verifier retirement

The Decision-0089 pre-formalization authorization verifier ran its final
allowed time immediately before formalization creation.

Verifier SHA-256:

`feb7cd4dfcbcecc30630ca464d037a70cd6651593bdc30b231a301eb76028d79`

Final-run output SHA-256:

`14a3a6a49b83b173cb2b0c332fe422b6731efcdf973f2354836a91cf3e075a4d`

Final-run output size:

`1146`

It is permanently retired and must never be rerun.

Previously retired verifiers remain retired.

## Explicit non-authorizations

Decision 0090 does not authorize:

- governance use of Formalization V1 before independent human review;
- exhaustive admissible-composition enumeration or elimination;
- constructive positive mapping-witness authoring;
- operational V4-to-V2 mapping;
- operational V4-to-successor mapping;
- positive mapping authorization;
- active Schema-V2 modification;
- schema-successor authoring;
- Schema V3;
- successor-version preselection;
- curl.json creation;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## Next boundary

Separately authorize an independent human technical review package for
Schema-V2 Semantic-Role Relation Formalization V1.
