# Exhaustive Admissible Existing-Schema-V2 Multi-Field Capability Study V1

Status: **AUTHOR_CANDIDATE**

Selected outcome:

`FURTHER_EVIDENCE_REQUIRED`

This outcome is **not yet human-approved**.

## Scope

This study evaluates whether existing active Schema V2 can losslessly represent
the exact curl V4 semantic content through native, semantically related,
structured direct or multi-field compositions while supporting deterministic
exact reverse reconstruction.

The study does not treat absence of same-named properties as impossibility.

## Complete inventories

- V4 semantic containers: 10
- V4 semantic units: 109
- V4 leaf fields: 531
- V4 semantic field classes: 57
- V4 rules: 64
- V4 exit obligations: 3
- V4 representation-policy fields: 10
- Rules carrying enforcement: 64
- Distinct enforcement classifications: 15
- Active Schema-V2 recursive property paths: 171
- Active Schema-V2 distinct property names: 123
- Open unconstrained Schema-V2 string carrier paths: 59
- Same-named V4-field / Schema-V2 property matches: 2 (`effect`, `rule_id`)

The current rule-only recomputation yields
2 verdict-to-enforcement
ambiguity groups and
2
defect+verdict-to-enforcement ambiguity groups under the explicit grouping used
by this study.

## Constructive existing-V2 path

Multiple structurally relevant Schema-V2 carrier compositions exist, including
resource/relation models, events and return classes, semantic-policy constants,
semantic-rule bindings/preconditions/effects, and exit-obligation state
requirements.

However, no complete constructive witness currently covers every V4 semantic
unit with deterministic exact forward encoding, deterministic exact reverse
reconstruction, collision freedom, and semantic noninterference.

Therefore:

`PROVEN_ADMISSIBLE_EXISTING_SCHEMA_V2_MAPPING_PATH_AVAILABLE`

is not established.

## Exhaustive negative path

All Schema-V2 carrier paths and all V4 semantic units/field classes are
inventoried and screened.

However, the admissibility contract requires **semantically related** native
carriers, while the current governance evidence does not contain a complete
machine-readable relation enumerating every admissible semantic-role
composition. Schema V2 also contains open string-valued semantically typed
carriers.

Consequently, the complete admissible multi-field composition space cannot
currently be machine-enumerated and exhaustively eliminated.

Therefore:

`PROVEN_NO_ADMISSIBLE_EXISTING_SCHEMA_V2_MAPPING_PATH_UNDER_REVIEWED_CONSTRAINTS`

is not established.

## Central unresolved exactness classes

The study retains, at minimum:

- `enforcement`
- `normative_strength_uncertainty_must_not_be_silently_strengthened`
- `resource_centered`
- `synthetic_protocol_events_invented`

as unresolved exactness classes.

Additional V4 rule/exit metadata fields also require complete constructive or
negative capability treatment.

## Selected author-candidate outcome

Because neither the complete positive proof nor the complete negative proof is
established, and because admissible-composition exhaustiveness is not presently
machine-established, Decision 0083 requires:

`FURTHER_EVIDENCE_REQUIRED`

## Governance

This is an author-candidate study result only.

It does not authorize:

- an operational positive V4-to-V2 mapping contract;
- schema-successor authoring;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution; or
- repair.

Independent human technical review is required before this study can be used
for subsequent governance.

## Next boundary

Separately authorize an independent human technical review package for
Capability Study V1.
