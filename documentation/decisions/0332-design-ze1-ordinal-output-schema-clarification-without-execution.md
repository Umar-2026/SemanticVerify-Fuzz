# D0332 — Design ZE1 Ordinal and Output-Schema Clarification Without Execution

## Status

`AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

**Clarification ID:** `SVF-D0332-ZE1-ORDINAL-OUTPUT-SCHEMA-CLARIFICATION-V1`

**Authoring timestamp UTC:** `2026-09-25T11:57:10+00:00`

D0332 is a design-only corrective clarification checkpoint.

It does not execute ZE1.

It does not consume the D0331 one-shot ZE1 authorization.

It grants zero new ZE1 execution attempts.

It does not read substantive source content.

It does not read ZE0 representations, candidate records, candidate values, or
candidate representations.

It does not perform matching, overlap analysis, E2, C4 reassessment, P8
mapping, gold annotation, analyzer work, baseline execution, or repair.

## Governing lineage

Frozen D0327 design commit:

`47c9135987178ce51179949d7b333b5bd2aa7492`

D0327 decision SHA-256:

`4a6c38ccd1093a0002dd924f506b72a21a3a7940af7e7eb9e70e2c2a12931835`

D0327 machine artifact SHA-256:

`30f29c230a09779200615125334967ba6ae7e9c8a81d9230b187189b2071e336`

Effective D0331 authorization commit:

`ac5b5edb93e8693f34537bcff298e8b3ab0fc39a`

D0331 decision SHA-256:

`62d92c1f7536abf865645f230985a422788efb0f21d49ba59b218a01118c488d`

D0331 machine artifact SHA-256:

`4c2172a412f7fa005dfceabc4ed55579b7ed52375b91cba429d42ea93f5c90f2`

The D0331 authorization currently has:

`TOTAL_ZE1_EXECUTION_CAPACITY=1`

`ZE1_AUTHORIZATION_CONSUMED=NO`

`ZE1_REMAINING_ATTEMPT_CAPACITY=1`

D0332 creates:

`NEW_ZE1_ATTEMPT_CAPACITY=0`

## Reason for clarification

A non-consuming post-D0331 reconciliation established that D0327 requires the
ordered ZE1-SF3 token-occurrence stream to retain:

- source member;
- atom ordinal;
- dot-segment ordinal;
- lexical-token ordinal;
- source-atom locator.

However, the frozen D0327 artifacts did not explicitly define:

1. the atom-ordinal numbering basis;
2. the dot-segment-ordinal numbering basis;
3. the lexical-token-ordinal numbering basis;
4. the exact JSON record schema for the future inventory.

The reconciliation therefore classified direct execution as:

`UNDER_SPECIFIED_DO_NOT_CONSUME_ZE1_AUTHORIZATION`

with missing fields:

`DOT_SEGMENT_ORDINAL_BASIS`

`LEXICAL_TOKEN_ORDINAL_BASIS`

`EXACT_INVENTORY_RECORD_SCHEMA`

No source bytes or ZE1 output were read or written while reaching this
conclusion.

## Clarification boundary

D0332 does not alter the D0327 lexical/representation transformations.

The following remain unchanged:

- source universe;
- exact four frozen source members;
- exact frozen source bytes;
- source order;
- strict UTF-8 decoding;
- Unicode normalization = NONE;
- Unicode casefold = NONE;
- semantic parsing = NONE;
- source-specific semantic querying = NONE;
- stemming = NONE;
- stopword removal = NONE;
- synonym expansion = NONE;
- source-atom grammar;
- ZE1-SF0 semantics;
- ZE1-SF1 semantics;
- ZE1-SF2 semantics;
- ZE1-SF3 semantics;
- candidate-blindness;
- collision/absence semantics;
- ordered-occurrence requirement;
- scientific interpretation boundary;
- D0331 one-shot consumption event;
- D0331 maximum execution capacity.

This checkpoint clarifies deterministic indexing and serialization only.

## Ordinal bases

For the future ZE1 inventory:

### Source ordinal

Source ordinal remains the frozen D0327/D0318 source ordinal:

`ONE_BASED_GLOBAL_IN_FROZEN_SOURCE_ORDER`

Thus:

- C1-S01 = 1
- C1-S02 = 2
- C1-S03 = 3
- C1-S04 = 4

### Atom ordinal

`atom_ordinal` is:

`ONE_BASED_PER_SOURCE`

The first retained atom occurrence in each source has atom ordinal `1`.

Every retained atom occurrence increments the ordinal by one in strict
left-to-right decoded-character scan order.

Discarded maximal spans do not receive an atom ordinal.

### Dot-segment ordinal

`dot_segment_ordinal` is:

`ONE_BASED_PER_ATOM`

The first ZE1-SF1 dot segment of an atom has ordinal `1`.

Leading, internal, and trailing empty dot segments are retained and receive
ordinals.

### Lexical-token ordinal

`lexical_token_ordinal` is:

`ONE_BASED_WITHIN_DOT_SEGMENT`

The first retained ZE1-SF2 lexical token within a dot segment has ordinal `1`.

Separator-created empty lexical tokens are discarded and receive no ordinal.

A dot segment producing zero lexical tokens has an empty lexical-token list.

## Exact future inventory JSON schema

The future file:

`evidence/representation_alignment/ZE1/source_representation_inventory_v1/source_representation_inventory.json`

must be a JSON object with exactly these top-level keys:

- `design_id`
- `grammar_id`
- `clarification_id`
- `execution_id`
- `runtime_unicode_database_version`
- `source_records`
- `ordered_token_occurrence_stream`

### Fixed identity values

`design_id`:

`SVF-ZE1-CANDIDATE-BLIND-SOURCE-REPRESENTATION-INVENTORY-CONTRACT-V1`

`grammar_id`:

`SVF-ZE1-CANDIDATE-BLIND-SOURCE-REPRESENTATION-GRAMMAR-V1`

`clarification_id`:

`SVF-D0332-ZE1-ORDINAL-OUTPUT-SCHEMA-CLARIFICATION-V1`

`execution_id`:

`SVF-ZE1-SOURCE-REPRESENTATION-INVENTORY-RUN-001`

### source_records

`source_records` contains exactly four records in frozen source order.

Each source record has exactly these keys:

- `source_member_id`
- `source_ordinal`
- `source_path`
- `source_sha256`
- `git_blob_oid`
- `source_format`
- `atom_occurrences`

Each `atom_occurrences` record has exactly these keys:

- `atom_ordinal`
- `raw_atom`
- `source_atom_locator`
- `dot_segments`
- `sf3_flattened_lexical_tokens`

`source_atom_locator` has exactly these keys:

- `source_member_id`
- `atom_ordinal`
- `start_character_offset_zero_based`
- `end_character_offset_exclusive`
- `start_line_one_based`
- `start_column_one_based`

Each `dot_segments` record has exactly these keys:

- `dot_segment_ordinal`
- `raw_segment`
- `lexical_tokens`

Each `lexical_tokens` record has exactly these keys:

- `lexical_token_ordinal`
- `token`

`sf3_flattened_lexical_tokens` is an ordered JSON array of token strings.

It is the concatenation of the retained ZE1-SF2 token strings in original
dot-segment order.

## Exact ordered token-occurrence stream schema

`ordered_token_occurrence_stream` is an ordered JSON array.

It contains one record for every retained ZE1-SF3 token occurrence.

No occurrence is deduplicated.

Each record has exactly these keys:

- `source_member_id`
- `source_ordinal`
- `atom_ordinal`
- `dot_segment_ordinal`
- `lexical_token_ordinal`
- `token`
- `source_atom_locator`

The stream order is:

1. frozen source order;
2. atom order within source;
3. dot-segment order within atom;
4. lexical-token order within dot segment.

No candidate comparison or semantic grouping is permitted while constructing
this stream.

## JSON serialization convention

Both future ZE1 JSON files must be serialized as:

- UTF-8;
- `ensure_ascii=False`;
- `sort_keys=True`;
- indentation = 2 spaces;
- exactly one final newline;
- no trailing whitespace.

This convention is serialization-only and has no semantic meaning.

## Exact future execution-state JSON schema

The future file:

`evidence/representation_alignment/ZE1/source_representation_inventory_v1/_execution_state.json`

must contain exactly these top-level keys:

- `execution_id`
- `authorization_id`
- `clarification_id`
- `status`
- `runtime_unicode_database_version`
- `source_record_count`
- `source_order`
- `source_identity_verification`
- `per_source_atom_counts`
- `per_source_token_occurrence_counts`
- `total_atom_occurrence_count`
- `total_token_occurrence_count`
- `output_hashes`
- `scientific_interpretation_boundary`

### source_identity_verification

This is an ordered array in frozen source order.

Each record has exactly:

- `source_member_id`
- `source_ordinal`
- `source_path`
- `expected_sha256`
- `observed_sha256`
- `sha256_match`
- `expected_git_blob_oid`

Source SHA-256 must be checked from source bytes at the first authorized source
read during the future one-shot ZE1 execution.

That read consumes the authorization if no earlier ZE1 output write has already
consumed it.

### Count maps

`per_source_atom_counts` and `per_source_token_occurrence_counts` are JSON
objects keyed exactly by:

- `C1-S01`
- `C1-S02`
- `C1-S03`
- `C1-S04`

### output_hashes

Because an execution-state file cannot contain its own final full-file hash
without a self-reference problem, D0332 defines the required in-file output
hash record deterministically.

`output_hashes` contains exactly:

- `inventory_file_sha256`
- `inventory_canonical_json_sha256`
- `execution_state_full_file_sha256_recorded_externally`

`inventory_file_sha256` is SHA-256 of the exact UTF-8 bytes written to
`source_representation_inventory.json`, including its single final newline.

`inventory_canonical_json_sha256` is SHA-256 of the inventory object serialized
in memory using:

`json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)`

encoded as UTF-8 with no appended newline.

`execution_state_full_file_sha256_recorded_externally` must have the literal
value:

`NEXT_RESULT_CHECKPOINT`

The actual SHA-256 of the complete `_execution_state.json` file is computed only
after the file has been fully written and is recorded by the later ZE1 result
checkpoint, not embedded recursively into the execution-state file.

## Future execution status value

If the authorized ZE1 transaction completes its contracted inventory and state
writes successfully, `_execution_state.json` uses:

`status = "COMPLETED"`

D0332 does not create this file and does not assert that ZE1 has completed.

## Scientific interpretation boundary

Nothing in D0332 establishes:

- source/candidate representation overlap;
- representation mismatch;
- semantic support;
- semantic non-support;
- mapping;
- C4;
- P8 readiness;
- analyzer evidence;
- repair evidence.

The existing boundary remains:

`C4_STATUS=UNRESOLVED`

`P8_MAPPING_AUTHORIZED=NO`

## Existing D0331 authorization and execution hold

D0332 grants zero new ZE1 attempt capacity.

The already-published D0331 one-shot capacity remains historically:

`TOTAL_CAPACITY=1`

`CONSUMED=NO`

`REMAINING=1`

However, because D0332 adds a deterministic serialization/index clarification
that was not explicit in frozen D0327, ZE1 MUST NOT execute merely because
D0332 is authored, committed, or published.

A later separately governed successor must explicitly reconcile the still
unconsumed D0331 one-shot authorization with the published D0332 clarification
before substantive source reading or ZE1 output writing occurs.

Therefore D0332 itself has:

`ZE1_EXECUTION_AUTHORIZED_BY_D0332=NO`

`SUBSTANTIVE_SOURCE_READ_AUTHORIZED_BY_D0332=NO`

`ZE1_OUTPUT_WRITE_AUTHORIZED_BY_D0332=NO`

`NEW_ATTEMPT_CAPACITY_GRANTED=0`

## Downstream non-authorizations

D0332 does not authorize:

- integrity reexecution;
- ZE0 read;
- candidate read;
- candidate-representation read;
- candidate comparison;
- representation-overlap matching;
- ZE1 execution;
- ZE2;
- ZE3;
- ZE4;
- corrected E1 reexecution;
- source expansion;
- fuzzy matching;
- semantic matching;
- semantic relevance filtering;
- E2;
- E3;
- E4;
- C4;
- P8 mapping;
- P10 gold annotation;
- P11 analyzer implementation;
- P11 analyzer execution;
- baseline execution;
- repair execution.

## D0332 authoring side-effect record

`SUBSTANTIVE_SOURCE_CONTENT_READ_PERFORMED=NO`

`SOURCE_SHA256_RECOMPUTED_FROM_SOURCE_BYTES=NO`

`ZE0_MANIFEST_READ_PERFORMED=NO`

`CANDIDATE_RECORD_READ_PERFORMED=NO`

`CANDIDATE_VALUE_READ_PERFORMED=NO`

`MATCHING_PERFORMED=NO`

`ZE1_OUTPUT_WRITE_PERFORMED=NO`

`ZE1_EXECUTION_PERFORMED=NO`

`ZE1_AUTHORIZATION_CONSUMED=NO`

`ZE1_REMAINING_ATTEMPT_CAPACITY=1`

`COMMIT_PERFORMED=NO`

`PUSH_PERFORMED=NO`

## Activation lifecycle

D0332 authoring alone is not effective.

A local commit alone is not effective.

The clarification becomes effective only after:

1. independent pre-commit verification;
2. exact local commit;
3. independent post-commit verification;
4. publication of the exact reviewed D0332 commit;
5. exact remote readback confirmation.

Even after D0332 becomes effective, ZE1 remains on governance hold until a
separate successor explicitly reconciles D0331's unconsumed one-shot
authorization with D0332.

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0332_ZE1_ORDINAL_OUTPUT_SCHEMA_CLARIFICATION`


## D0332 Pre-commit Review Reconciliation

The first independent pre-commit review of the D0332 author candidate returned:

`D0332_INDEPENDENT_PRE_COMMIT_REVIEW=REVISION_REQUIRED`

with:

`PASS_CHECK_COUNT=151`

`FAIL_CHECK_COUNT=4`

`REVIEW_FINDING_COUNT=4`

No commit, push, substantive source-content read, source-byte SHA-256
recomputation, ZE0 read, candidate read, matching, ZE1 output write, or ZE1
execution occurred during that review.

The failed-review candidate byte identities were:

- D0332 decision SHA-256:
  `f71c2571bc03d43c8397446d5d4e2917ac5a4052434a523cd8940d01ddf69e15`
- D0332 machine artifact SHA-256:
  `a40204acab85ad4e4ddf3b82be953fc3b47123b5415b39d6d3fb959a14e44076`

### Finding 1 — atom-ordinal clarification provenance

The prior read-only reconciliation explicitly reported:

`ATOM_ORDINAL_EXPLICITLY_BASED=NO`

Its automated final classification nevertheless listed only:

- `DOT_SEGMENT_ORDINAL_BASIS`
- `LEXICAL_TOKEN_ORDINAL_BASIS`
- `EXACT_INVENTORY_RECORD_SCHEMA`

D0332 does not rewrite that historical three-item classifier output.

Instead, the machine artifact now separately records:

`additional_clarification_fields_not_listed_by_classifier=["ATOM_ORDINAL_BASIS"]`

The atom-ordinal basis is therefore an additional deterministic clarification
supported by the explicit prior reconciliation question, not a silently added
member of the historical classifier result.

### Finding 2 — inventory fixed identities

The inventory schema now contains machine-readable exact fixed identity values:

- `design_id = SVF-ZE1-CANDIDATE-BLIND-SOURCE-REPRESENTATION-INVENTORY-CONTRACT-V1`
- `grammar_id = SVF-ZE1-CANDIDATE-BLIND-SOURCE-REPRESENTATION-GRAMMAR-V1`
- `clarification_id = SVF-D0332-ZE1-ORDINAL-OUTPUT-SCHEMA-CLARIFICATION-V1`
- `execution_id = SVF-ZE1-SOURCE-REPRESENTATION-INVENTORY-RUN-001`

No executor inference from prose is required.

### Finding 3 — execution-state fixed identities

The execution-state schema now contains machine-readable exact fixed identity
values:

- `execution_id = SVF-ZE1-SOURCE-REPRESENTATION-INVENTORY-RUN-001`
- `authorization_id = SVF-D0331-ZE1-SINGLE-EXECUTION-AUTH-V1`
- `clarification_id = SVF-D0332-ZE1-ORDINAL-OUTPUT-SCHEMA-CLARIFICATION-V1`

### Finding 4 — exact nested scientific-boundary schema

The future `_execution_state.json` field
`scientific_interpretation_boundary` now has exactly these nested keys:

- `ZE1_inventory_is_semantic_evidence`
- `ZE1_inventory_is_protocol_support`
- `ZE1_inventory_is_semantic_non_support`
- `ZE1_inventory_is_mapping`
- `ZE1_inventory_establishes_C4`
- `ZE1_inventory_changes_D0321_zero_evidence_result`
- `ZE1_inventory_alone_establishes_representation_mismatch`

Each exact value is `false`.

These are serialization of the frozen ZE1 scientific interpretation boundary;
they do not create a new scientific conclusion.

### Scope preservation

This corrective authoring changes no source bytes, source universe,
candidate-blindness rule, ZE1-SF0/SF1/SF2/SF3 transformation, one-shot
consumption event, or attempt capacity.

Current state remains:

`ZE1_AUTHORIZATION_CONSUMED=NO`

`ZE1_REMAINING_ATTEMPT_CAPACITY=1`

`NEW_ZE1_ATTEMPT_CAPACITY_GRANTED_BY_D0332=0`

`ZE1_EXECUTION_AUTHORIZED_BY_D0332=NO`

`SUBSTANTIVE_SOURCE_READ_AUTHORIZED_BY_D0332=NO`

`ZE1_OUTPUT_WRITE_AUTHORIZED_BY_D0332=NO`

`C4_STATUS=UNRESOLVED`

`P8_MAPPING_AUTHORIZED=NO`

The next transaction is a new independent pre-commit verification of these
revised D0332 bytes.
