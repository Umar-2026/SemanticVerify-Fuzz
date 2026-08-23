# Decision 0095 — Authorize Evidence-Only Corrective Successor Package V2 for Schema-V2 Semantic-Role Relation Formalization V1

Status: CORRECTIVE SUCCESSOR PACKAGE V2 AUTHORING AUTHORIZED — PACKAGE NOT YET AUTHORED

## Basis

Decision 0094 immutably recorded the completed independent human review of
Schema-V2 Semantic-Role Relation Formalization V1.

The original review outcome remains:

`REVISION_REQUIRED`

Focused revision items:

- SRR02
- SRR04
- SRR05
- SRR08

Carried-forward PASS items:

- SRR01
- SRR03
- SRR06
- SRR07

The original completed review and its overall REVISION_REQUIRED decision
remain immutable historical evidence.

## SRR02 corrective authorization

Corrective Successor Package V2 must include byte-exact copies of:

1. `02_v4_semantic_unit_inventory.v1.json`
   - SHA-256: `2b39f5625658e41aeb906a1db8a4a472d9265dc3654572e60374827f0ce7fa7d`
   - 531 reviewed leaf fields
   - 109 reviewed semantic units

2. `03_schema_v2_carrier_inventory.v1.json`
   - SHA-256: `0f32fb87e1396da8c37e3f74c41059560338346ae54f29df0c2d38d72deb1d6d`
   - 171 Schema-V2 property paths

3. `04_candidate_multifield_composition_matrix.v1.json`
   - SHA-256: `c064cfa8c7143b537dc3bb54b8af353f56bafba3e415e7ccdb2c17efaff30d45`
   - 57 matrix field classes
   - 109 unit-analysis records

The corrective package must machine-check exact binding from these reviewed
source domains to the immutable Formalization V1 derived evidence.

## SRR04 corrective authorization

The 9,747 relation rows are immutable and must not be reclassified.

The reviewed machine-readable relation establishes:

- lexical-only predicate:
  `reviewed_lexical_only_candidate == true`
- total lexical-only pairs: 125
- SEMANTICALLY_RELATED: 0
- UNRESOLVED: 120
- NOT_SEMANTICALLY_RELATED: 5

Therefore the original report sentence:

> In particular, 125 lexical-screening-only pairs remain unresolved.

must not be edited in place.

Corrective Successor Package V2 must instead provide an explicit successor
erratum stating:

> There are 125 reviewed lexical-only candidate pairs in total: 120 are
> UNRESOLVED and five semantic_accounting pairs are
> NOT_SEMANTICALLY_RELATED; none are SEMANTICALLY_RELATED.

The five explicit-negative pairs are:

1. EXPLICIT_GLOBAL_CLEANUP_OBLIGATION ×
   `$.semantic_accounting.inventory.exit_obligation_count`
2. cleanup_obligation_effect ×
   `$.semantic_accounting.inventory.exit_obligation_count`
3. dependent_reasoning_policy ×
   `$.semantic_accounting.inventory.representation_policy_field_count`
4. feasible_state_join_policy ×
   `$.semantic_accounting.inventory.representation_policy_field_count`
5. rule_id ×
   `$.semantic_accounting.inventory.rule_count`

This is a presentation/accounting erratum only.

No relation-row reclassification is authorized.

## SRR05 corrective authorization

The corrective package must provide self-contained machine-verifiable binding
between:

- all 531 reviewed leaf records;
- all 109 reviewed semantic units;
- the Formalization V1 unit/leaf traceability artifact; and
- all 109 reviewed matrix unit-analysis records.

Carrier-family screening context must remain distinct from semantic
relatedness classification.

## SRR08 corrective authorization

The corrective package must be self-contained.

Its safe verifier must run using package-local inputs and must not depend on
the original repository-relative source layout.

It must verify at minimum:

- exact source hashes;
- reviewed-domain structural counts;
- source-to-derived bindings;
- 9,747 relation-row preservation;
- 125 / 120 / 5 lexical-only accounting;
- the five explicit-negative pairs;
- successor erratum correctness;
- original Formalization V1 immutability;
- original Review Package V1 immutability;
- original REVISION_REQUIRED human-review immutability; and
- all bounded governance nonclaims.

## Focused human rereview requirement

Corrective Successor Package V2 must contain a blank focused rereview packet
for exactly:

- SRR02-C
- SRR04-C
- SRR05-C
- SRR08-C

Allowed item decisions:

- PASS
- REVISION_REQUIRED
- FAIL

Allowed overall focused decisions:

- APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2
- REVISION_REQUIRED
- FAIL

Reviewer role:

`Spec-Technical-Reviewer-1`

Human decisions and reviewer identity must remain blank at package
checkpoint.

SRR01, SRR03, SRR06, and SRR07 remain carried-forward PASS items and are not
silently rewritten or re-adjudicated.

## Immutable boundaries

Decision 0095 does not authorize modification of:

- Formalization V1;
- any of its 9,747 relation rows;
- the original Formalization V1 report;
- Review Package V1;
- its immutable blank reviewer packet;
- the completed human review;
- Decision 0093; or
- Decision 0094.

## Explicit non-authorizations

Decision 0095 does not authorize:

- approval of Formalization V1;
- operational V4-to-V2 mapping;
- constructive positive mapping witness;
- a proof of mapping impossibility;
- exhaustive admissible-composition proof;
- schema-successor authoring;
- successor-schema version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## Authorization-verifier lifecycle

The Decision-0095 verifier is a pre-corrective-package-authoring verifier.

It may be run while Corrective Successor Package V2 does not exist.

Immediately before package authoring it must run its final allowed time.

Once any Corrective Successor Package V2 artifact is authored, the
Decision-0095 authorization verifier is permanently retired and must never be
rerun.

## Next boundary

Run the Decision-0095 authorization verifier its final allowed time, then
author Corrective Successor Package V2 using only the authorized
evidence-correction scope.
