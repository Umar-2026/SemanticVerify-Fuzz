# Decision 0340 — Clarify ZE2 candidate-index binding to the frozen ZE0 candidate ordinal

## Status

`AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0340 is a governance/schema clarification only.

It does not execute ZE2, read the ZE0 scientific manifest payload, read the ZE1
scientific inventory payload, perform candidate/source comparison, compute
representation overlap, perform mapping, annotate gold data, implement or
execute the analyzer, execute a baseline, or execute repair.

D0340 grants **zero new ZE2 execution attempts**.

## Governing effective lineage

D0340 is subordinate to the already effective ZE2 governance lineage,
including:

- D0336 effective contract commit:
  `40561ff59630f82e9fa7427632c87894ca95e08d`
- D0337 original single ZE2 execution authorization:
  `SVF-D0337-ZE2-SINGLE-EXECUTION-AUTH-V1`
- ZE2 execution ID:
  `SVF-ZE2-DETERMINISTIC-REPRESENTATION-OVERLAP-RUN-001`
- D0339 effective corrective-successor governance.

The original ZE2 execution authorization remains a single preserved attempt.
D0340 does not replace it, duplicate it, restore it, or increase its capacity.

## Governance defect requiring clarification

The frozen effective ZE0 manifest contract uses the record identifier:

`candidate_ordinal`

D0323 requires each ZE0 candidate record to contain:

- `candidate_ordinal`
- `schema_v2_property_path`
- `representation_grammar_id`
- `representations`

D0324/D0325 preserve exact frozen candidate ordinal order, and the
preauthorization integrity result verifies candidate ordinals exactly
`1` through `171`.

The effective D0336 ZE2 output contract instead requires each future
candidate-form record to contain the output field:

`candidate_index`

and currently states:

`PRESERVE_EXACT_CANDIDATE_INDEX_VALUE_FROM_FROZEN_ZE0_MANIFEST;DO_NOT_RENUMBER`

A governance-only provenance search established:

`ZE0_CONTRACT_REQUIRES_candidate_ordinal=TRUE`

`ZE0_CONTRACT_REQUIRES_candidate_index=FALSE`

`ZE2_CONTRACT_REQUIRES_candidate_index=TRUE`

`PRE_D0336_GOVERNANCE_candidate_index_FILES=0`

`PRE_D0336_GOVERNANCE_FILES_CONTAINING_BOTH_INDEX_AND_ORDINAL=0`

`IDENTIFIER_PROVENANCE_ESTABLISHED=NO`

Therefore the effective D0336 text references an input field that is not part
of the frozen ZE0 manifest schema.

D0340 does not claim that an ordinal-to-index bridge existed previously.
It records and corrects that underspecified input-field referent prospectively
for the still-unexecuted ZE2 run.

## Exact clarification

For the future governed ZE2 execution only, the D0336 output field:

`candidate_index`

is bound exactly as follows:

`candidate_index := ZE0_record.candidate_ordinal`

This is a **field-name binding only**.

The exact stored integer value of `candidate_ordinal` must be copied without
mutation into the ZE2 output field `candidate_index`.

The following are prohibited:

- zero-based conversion;
- subtracting one;
- adding one;
- Python/array/list-position substitution;
- enumeration-derived replacement;
- renumbering;
- sorting by a newly computed index;
- deriving the value from record position instead of the stored
  `candidate_ordinal`;
- candidate reordering;
- candidate dropping;
- candidate insertion;
- semantic remapping;
- schema-V4-to-V2 mapping;
- any aliasing beyond this exact schema-field binding.

Thus, if a frozen ZE0 record contains:

`candidate_ordinal = N`

then every ZE2 candidate-form record derived from that candidate must contain:

`candidate_index = N`

for the same exact `N`.

## Candidate order and count remain unchanged

D0340 does not modify candidate order.

The future ZE2 candidate order remains:

`EXACT_RECORD_ORDER_OF_FROZEN_ZE0_CANDIDATE_REPRESENTATION_MANIFEST`

The future ZE2 representation order remains the seven-form D0323 frozen order.

Expected counts remain:

- ZE0 candidate records: `171`
- representation forms per candidate: `7`
- ZE2 candidate-form records: `1197`
- per-representation candidate-form records: `171`

No record count is changed by D0340.

## Fail-closed execution requirement

During the future consuming ZE2 attempt, after the frozen ZE0 payload identity
checks PASS and before candidate/source comparison begins, the implementation
must verify:

1. every ZE0 candidate record contains `candidate_ordinal`;
2. `candidate_ordinal` is an integer;
3. stored candidate ordinals are exactly the frozen ordinal sequence in the
   frozen manifest record order;
4. each generated ZE2 `candidate_index` exactly equals the source record's
   stored `candidate_ordinal`;
5. no candidate-index value is computed from an array position.

Any violation is an execution-contract failure.

Because the preserved D0337 ZE2 authorization is one-shot, a failure occurring
after the scientific-payload consumption boundary remains consumed and is not
retryable under D0337.

D0340 does not create a retry exception.

## D0336 correction scope

D0340 supersedes only this D0336 semantic clause:

`PRESERVE_EXACT_CANDIDATE_INDEX_VALUE_FROM_FROZEN_ZE0_MANIFEST;DO_NOT_RENUMBER`

with:

`COPY_EXACT_STORED_candidate_ordinal_FROM_THE_CORRESPONDING_FROZEN_ZE0_MANIFEST_RECORD_INTO_ZE2_OUTPUT_FIELD_candidate_index;DO_NOT_RENUMBER_OR_DERIVE_FROM_RECORD_POSITION`

The output field name remains:

`candidate_index`

All other D0336 requirements remain unchanged, including:

- compatibility matrix;
- exact equality semantics;
- source surfaces;
- candidate representation values;
- candidate value hash contract;
- source occurrence locator schema;
- source occurrence ordering;
- manifest top-level schema;
- candidate-form record ordering;
- serialization contract;
- output paths;
- fixed identity values;
- count invariants;
- scientific interpretation boundary.

## ZE2 execution authorization state

D0340 adds:

`NEW_ZE2_EXECUTION_ATTEMPT_CAPACITY=0`

The preserved execution authorization remains:

`SVF-D0337-ZE2-SINGLE-EXECUTION-AUTH-V1`

with:

`TOTAL_ZE2_EXECUTION_ATTEMPT_CAPACITY=1`

`ZE2_EXECUTION_AUTHORIZATION_CONSUMED=NO`

`REMAINING_ZE2_EXECUTION_ATTEMPT_CAPACITY=1`

D0340 authoring does not make the clarification effective.

ZE2 execution remains blocked until the exact D0340 author candidate is:

1. independently pre-commit reviewed and PASS;
2. committed as a separate transaction;
3. independently post-commit reviewed and PASS;
4. published to `origin/main`;
5. confirmed by exact remote readback.

## Scientific interpretation boundary

D0340 establishes no scientific result.

`REPRESENTATION_OVERLAP_ESTABLISHED=NO`

`SEMANTIC_EVIDENCE_ESTABLISHED=NO`

`PROTOCOL_SUPPORT_ESTABLISHED=NO`

`SEMANTIC_NON_SUPPORT_ESTABLISHED=NO`

`MAPPING_ESTABLISHED=NO`

`C4_STATUS=UNRESOLVED`

`P8_MAPPING_AUTHORIZED=NO`

The ordinal-to-output-field binding is deterministic schema plumbing only.
It is not semantic mapping.

## Authoring noninterference

During D0340 authoring:

`ZE0_SCIENTIFIC_PAYLOAD_READ_PERFORMED=NO`

`ZE1_SCIENTIFIC_PAYLOAD_READ_PERFORMED=NO`

`ZE2_RESERVED_OUTPUT_ROOT_TEST_PERFORMED=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED=NO`

`REPRESENTATION_OVERLAP_PERFORMED=NO`

`ZE2_OUTPUT_WRITE_PERFORMED=NO`

`ZE2_EXECUTION_PERFORMED=NO`

`ZE2_EXECUTION_AUTHORIZATION_CONSUMED=NO`

`GIT_ADD_PERFORMED=NO`

`COMMIT_PERFORMED=NO`

`PUSH_PERFORMED=NO`

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0340_ZE2_CANDIDATE_IDENTIFIER_CLARIFICATION_AUTHOR_CANDIDATE`
