# Schema-V2 Relation-Informed Exhaustive Admissible Composition Study V1

Status: `AUTHOR_CANDIDATE`

## Bound scope

- Active schema: Schema V2 `2.0.0`.
- Reviewed field-class/property-path relation pairs: `9,747`.
- Matrix relation-domain field classes: `57`.
- Schema-V2 property paths: `171`.
- Reviewed semantic units: `109`.
- Source leaf records: `531`.
- Losslessness requirements in scope by Decision 0102: `17`.

## Relation accounting

- `SEMANTICALLY_RELATED`: 113.
- `NOT_SEMANTICALLY_RELATED`: 969.
- `UNRESOLVED`: 8665.

The complete reviewed 57×171 field-class relation domain is accounted for.

## Conservative admissibility rules

- `SEMANTICALLY_RELATED` may serve as positive relation evidence.
- `UNRESOLVED` is not promoted to positive evidence.
- `NOT_SEMANTICALLY_RELATED` is excluded from semantic-storage compositions.
- Lexical screening and candidate-family membership are not semantic proof.
- Open or unconstrained string capacity is not semantic-losslessness proof.
- The matrix field-class vocabulary and unit-inventory field-class vocabulary are not merged or equated.

## Exhaustiveness result

- Field-class relation-domain completeness: `TRUE`.
- Semantic-unit inventory completeness: `TRUE`.
- Exact bound 17-item requirement inventory discovered in authorized inputs: `FALSE`.
- Semantic-unit-to-carrier admissibility-domain completeness: `FALSE`.
- Joint cross-unit coherence search completeness: `FALSE`.
- Whole-V4 admissible-composition universe proven complete: `FALSE`.

## Outcome

`FURTHER_EVIDENCE_REQUIRED`

The study does not identify a positive existing-Schema-V2 whole-V4 mapping witness and does not prove negative existing-Schema-V2 mapping impossibility.

The reason is not merely that brute-force search was omitted. The current bound evidence does not provide a sound basis for declaring the whole-V4 semantic-unit composition universe complete without violating one or more reviewed constraints: promoting unresolved relations, equating distinct field-class vocabularies, or interpreting screening/storage capacity as semantic proof.

Accordingly, a positive or negative global conclusion would exceed the approved evidence.

## Governance boundary

This is an author-candidate technical study. Independent human review is required before governance use.

The study does not authorize operational mapping, active Schema-V2 modification, schema-successor authoring, Schema V3, `curl.json`, analyzer implementation/execution, baseline execution, or repair.
