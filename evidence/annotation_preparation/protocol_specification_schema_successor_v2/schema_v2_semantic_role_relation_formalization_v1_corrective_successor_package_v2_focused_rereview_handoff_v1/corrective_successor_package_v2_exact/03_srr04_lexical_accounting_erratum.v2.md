# SRR04 Corrective Successor Erratum V2

## Scope

This successor erratum addresses only the presentation/accounting inconsistency
identified during independent human review of Schema-V2 Semantic-Role Relation
Formalization V1.

The original Formalization V1 artifacts remain immutable.

No relation row is modified or reclassified.

## Original presentation statement

Formalization V1 states:

> In particular, 125 lexical-screening-only pairs remain unresolved.

That sentence is not consistent with the immutable machine-readable relation
rows.

## Corrected accounting

The immutable relation evidence establishes:

- reviewed lexical-only candidate pairs: 125;
- SEMANTICALLY_RELATED: 0;
- UNRESOLVED: 120; and
- NOT_SEMANTICALLY_RELATED: 5.

Therefore the corrective successor interpretation is:

> There are 125 reviewed lexical-only candidate pairs in total: 120 are UNRESOLVED and five semantic_accounting pairs are NOT_SEMANTICALLY_RELATED; none are SEMANTICALLY_RELATED.

The five lexical-only explicit-negative pairs are:

1. `EXPLICIT_GLOBAL_CLEANUP_OBLIGATION × $.semantic_accounting.inventory.exit_obligation_count`
2. `cleanup_obligation_effect × $.semantic_accounting.inventory.exit_obligation_count`
3. `dependent_reasoning_policy × $.semantic_accounting.inventory.representation_policy_field_count`
4. `feasible_state_join_policy × $.semantic_accounting.inventory.representation_policy_field_count`
5. `rule_id × $.semantic_accounting.inventory.rule_count`

## Classification boundary

This correction does not alter the relation matrix.

The original 9,747 relation rows remain byte-exact.

The existing classification totals remain:

- SEMANTICALLY_RELATED: 113;
- NOT_SEMANTICALLY_RELATED: 969;
- UNRESOLVED: 8,665.

## Nonclaims

This erratum does not prove:

- a positive operational V4-to-V2 mapping;
- impossibility of such a mapping;
- exhaustive admissible-composition elimination;
- schema-successor necessity;
- any successor-schema version;
- curl.json authorization;
- analyzer authorization;
- baseline authorization; or
- repair authorization.
