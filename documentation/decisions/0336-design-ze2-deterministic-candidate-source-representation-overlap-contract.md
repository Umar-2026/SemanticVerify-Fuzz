# Decision 0336 — Design ZE2 deterministic candidate/source representation-overlap contract

## Status

`DESIGN_ONLY_AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0336 is design-only. It performs no ZE2 execution, no candidate/source comparison, no mapping, and no semantic adjudication.

## Evidence-based successor determination

The effective D0334 result checkpoint records successful ZE1 completion while preserving `C4_STATUS=UNRESOLVED` and `P8_MAPPING_AUTHORIZED=NO`.

The effective D0335 transport checkpoint changes only Git-LFS transport and does not authorize candidate/source matching, ZE2, C4 reassessment, P8 mapping, gold annotation, analyzer work, baseline execution, or repair.

The earlier D0322 representation-alignment governance requires revised matching semantics to be a new separately governed contract.

D0327 and the subsequent ZE1 lineage identify ZE2 as a separate future deterministic overlap stage rather than an automatic consequence of ZE1.

No post-D0335 numeric successor existed at the read-only successor scan. Therefore the next governance transaction is a new D0336 ZE2 design checkpoint rather than P8 execution.

## Governing lineage

### D0322

- commit: `6e193d8e5d0095e488bb6da36824e72a9b2119bc`
- decision: `documentation/decisions/0322-design-zero-evidence-representation-alignment-successor-governance.md`
- decision SHA-256: `9070a0deab08fb9f4d94356ceeec61d6134ad596943c96b96c7a86d3d5a92b41`
- machine artifact: `evaluation/governance_reconciliation/d0322_zero_evidence_representation_alignment_successor_design.json`
- machine artifact SHA-256: `329ddc3449cb0f9afb16df2d407abca378967937b523bfedc2b7cb41853e2736`
- role: `representation_alignment_design_only_parent`

### D0323

- commit: `ed1b6c5fd78b8690560d472b1241fa9bcfda3635`
- decision: `documentation/decisions/0323-design-ze0-deterministic-candidate-representation-manifest-contract.md`
- decision SHA-256: `df0671d41f21e6014bfbe445b1e7f18567598ffd65b8b58dcdba3d4c5b54cb07`
- machine artifact: `evaluation/governance_reconciliation/d0323_ze0_candidate_representation_manifest_design.json`
- machine artifact SHA-256: `a7ca71ba4570c23ae89b3536aab729fdc194f3c92cccf74d733a8358eca7fefa`
- role: `frozen_ZE0_candidate_representation_contract`

### D0326

- commit: `0de94e0b532dcad4184b6eb32d46a3e475fcf616`
- decision: `documentation/decisions/0326-record-successful-ze0-execution-result-without-ze1-start.md`
- decision SHA-256: `dd172b110472d080cc7e0b78f2c246061ca0e5a6e2a2af009c7919b6b07ac36d`
- machine artifact: `evaluation/governance_reconciliation/d0326_ze0_execution_result.json`
- machine artifact SHA-256: `0cf4f0233664d8abe69e55f41fbcaa28815257ac479d14a5ff13a980e237009e`
- role: `published_ZE0_result_checkpoint`

### D0327

- commit: `47c9135987178ce51179949d7b333b5bd2aa7492`
- decision: `documentation/decisions/0327-design-ze1-candidate-blind-source-representation-inventory-contract.md`
- decision SHA-256: `4a6c38ccd1093a0002dd924f506b72a21a3a7940af7e7eb9e70e2c2a12931835`
- machine artifact: `evaluation/governance_reconciliation/d0327_ze1_candidate_blind_source_representation_inventory_design.json`
- machine artifact SHA-256: `30f29c230a09779200615125334967ba6ae7e9c8a81d9230b187189b2071e336`
- role: `frozen_ZE1_source_representation_contract`

### D0332

- commit: `e2073c24b5f858465fce9e27786851ae913f0c32`
- decision: `documentation/decisions/0332-design-ze1-ordinal-output-schema-clarification-without-execution.md`
- decision SHA-256: `37c1282dd37db422c32f9608e925da7b2ecbdd5b92025f4088fcaf1b21cca934`
- machine artifact: `evaluation/governance_reconciliation/d0332_ze1_ordinal_output_schema_clarification.json`
- machine artifact SHA-256: `52baf4781e24fd7d3c17bf50df53fac67c83f1662cb70847f26060b827245a21`
- role: `frozen_ZE1_ordinal_bases_exact_output_schema_and_serialization_clarification`
### D0335

- commit: `4ddf3df73fca3f6216a73af12ae16f51ff808c5f`
- decision: `documentation/decisions/0335-design-git-lfs-transport-for-ze1-large-inventory.md`
- decision SHA-256: `2d9886f7ba9dd4260b2761ba129429e0862b487439d8fc62338731ebca332c6a`
- machine artifact: `evaluation/governance_reconciliation/d0335_git_lfs_transport_design_for_ze1_large_inventory.json`
- machine artifact SHA-256: `4ef5e32fa90625d55f953135bd8353cee86c354fa5dedebffa5e911c98fa341e`
- role: `effective_ZE1_LFS_transport_control`

### D0334

- commit: `9aff906354fa2cbd0f842ea1a733314261d082ac`
- decision: `documentation/decisions/0334-record-ze1-source-representation-inventory-result.md`
- decision SHA-256: `4a7d60ce7f5b0df8c5d0d972db46555360dbc91b81f19fc7b6c5ce85f41cd3be`
- machine artifact: `evaluation/governance_reconciliation/d0334_ze1_source_representation_inventory_result_record.json`
- machine artifact SHA-256: `528dcf01bd65a23db2165a080d0e5c924b492679107a7edd781ef494220ab84d`
- role: `published_effective_ZE1_result_checkpoint`

## Frozen input identity

ZE0 remains the already-completed candidate-side representation artifact:

- candidate records: `171`
- representation forms per candidate: `7`
- total representation values: `1197`
- candidate canonical SHA-256: `c2746447215aa5aa2be0abea3bb631043eb0bb12745cc54309881d88a5a1f908`
- ZE0 manifest SHA-256: `556096b6b6adc0708aee4903c5a4eb033231c04d7abe125d14f9dd5ad9760693`
- ZE0 execution-state SHA-256: `bc3257530de6be661c21f3cefd5e48fb75ed2e8fe60fde91bf748e77b1957f13`

ZE1 remains the already-completed source-side representation artifact:

- source records: `4`
- atom occurrences: `302082`
- token occurrences: `574824`
- scientific inventory SHA-256: `5077ad7cfbe393c3a6000348aa667ed2a0d439e11538ec65c08999537f524d7c`
- canonical inventory SHA-256: `1a732561d11f83ebbe3dde3386239dea3654dbf00e5a664a94e74dea39a6e4d8`
- execution-state SHA-256: `4abc3f43a922cbe024c02dcb62543d930895a80299467274bd9caf01d10399f4`

D0336 authoring reads neither ZE0 candidate values nor ZE1 inventory payload values.

## ZE2 contract identity

`SVF-ZE2-DETERMINISTIC-STRUCTURAL-REPRESENTATION-OVERLAP-V1`

Reserved future execution ID: `SVF-ZE2-DETERMINISTIC-REPRESENTATION-OVERLAP-RUN-001`

ZE2 is deterministic diagnostic representation overlap only.

## Exact compatibility matrix

### ZE0-F0-RAW-PATH-EXACT

- candidate shape: `STRING`
- source surface: `ZE1-SF0-RAW-ATOM`
- source scope: `FULL_SOURCE_ATOM`
- relation: `EXACT_STRING_EQUALITY`

### ZE0-F1-DOT-SEGMENT-SEQUENCE-EXACT

- candidate shape: `SEQUENCE_OF_STRINGS`
- source surface: `ZE1-SF1-DOT-SEGMENT-SEQUENCE`
- source scope: `FULL_SOURCE_ATOM_SEGMENT_SEQUENCE`
- relation: `EXACT_SEQUENCE_EQUALITY`

### ZE0-F2-LEAF-SEGMENT-EXACT

- candidate shape: `STRING`
- source surface: `ZE1-SF1-DOT-SEGMENT`
- source scope: `EACH_SOURCE_DOT_SEGMENT`
- relation: `EXACT_STRING_EQUALITY`

### ZE0-F3-PARENT-LEAF-SEQUENCE-EXACT

- candidate shape: `SEQUENCE_OF_STRINGS`
- source surface: `ZE1-SF1-DOT-SEGMENT-SEQUENCE`
- source scope: `EACH_CONTIGUOUS_TWO_SEGMENT_WINDOW`
- relation: `EXACT_SEQUENCE_EQUALITY`

### ZE0-F4-LEAF-LEXICAL-TOKENS

- candidate shape: `SEQUENCE_OF_STRINGS`
- source surface: `ZE1-SF2-LEXICAL-TOKENS`
- source scope: `EACH_SOURCE_DOT_SEGMENT`
- relation: `EXACT_SEQUENCE_EQUALITY`

### ZE0-F5-PARENT-LEAF-LEXICAL-TOKEN-SEQUENCES

- candidate shape: `SEQUENCE_OF_SEQUENCE_OF_STRINGS`
- source surface: `ZE1-SF2-LEXICAL-TOKEN-SEQUENCES`
- source scope: `EACH_CONTIGUOUS_TWO_SEGMENT_WINDOW`
- relation: `EXACT_NESTED_SEQUENCE_EQUALITY`

### ZE0-F6-ALL-SEGMENT-LEXICAL-TOKEN-SEQUENCES

- candidate shape: `SEQUENCE_OF_SEQUENCE_OF_STRINGS`
- source surface: `ZE1-SF2-LEXICAL-TOKEN-SEQUENCES`
- source scope: `FULL_SOURCE_ATOM_SEGMENT_TOKEN_SEQUENCE`
- relation: `EXACT_NESTED_SEQUENCE_EQUALITY`

## Corrective revision after independent pre-commit review

The first independent D0336 pre-commit review returned `REVISION_REQUIRED` with exactly three findings.

- prior decision SHA-256: `42d628304cdee77224e58cac34915c6c0b90f0996ea14b91a8982111fa38fc2f`
- prior machine artifact SHA-256: `d97b81813d3146d59300fd5277b861901c0de2365196da9b3cf2b3d995e6449c`
- prior review: `PASS_CHECK_COUNT=119`, `REVIEW_FINDING_COUNT=3`

`D0336-PR-001` is resolved by explicitly binding the effective D0332 clarification in the machine-readable governance inputs.

`D0336-PR-002` is resolved by recording the exact D0332 commit and byte hashes in this human-readable decision.

`D0336-PR-003` is resolved by freezing the exact candidate-representation-value byte serialization below.

No scientific execution occurred while correcting these findings.

## Candidate representation value hash serialization

Contract ID:

`SVF-ZE2-CANDIDATE-REPRESENTATION-VALUE-BYTES-V1`

Hash algorithm:

`SHA-256`

The hash input is a type-tagged and length-prefixed canonical byte serialization of the already-stored candidate representation value.

Text encoding is exact UTF-8. Unicode normalization is `NONE`. Case transformation is `NONE`.

`U64BE(n)` means exactly eight bytes containing unsigned integer `n` in big-endian byte order.

For `STRING`:

`0x53 || U64BE(LEN(UTF8(value))) || UTF8(value)`

For `SEQUENCE_OF_STRINGS`:

`0x4c || U64BE(item_count) || SERIALIZE_STRING(item_1) || ... || SERIALIZE_STRING(item_n)`

For `SEQUENCE_OF_SEQUENCE_OF_STRINGS`:

`0x4e || U64BE(outer_count) || SERIALIZE_SEQUENCE_OF_STRINGS(sequence_1) || ... || SERIALIZE_SEQUENCE_OF_STRINGS(sequence_n)`

Empty strings and empty sequences remain explicit through their type tags and zero length/count fields.

Stored sequence order is preserved exactly. No whitespace is inserted. No terminal newline is appended. JSON serialization is not used for this hash input. The candidate scientific value is not modified before hashing.
## Equality semantics

No new normalization is permitted.

- string equality: exact stored Unicode codepoint sequence equality
- sequence equality: same length and elementwise exact equality in order
- nested-sequence equality: same outer length and exact equality of every inner ordered sequence
- Unicode normalization: NONE
- casefold: NONE
- stemming: NONE
- lemmatization: NONE
- synonyms: NONE
- abbreviation expansion: NONE
- edit distance: NONE
- substring matching: NONE
- regular-expression matching: NONE
- fuzzy matching: NONE
- embedding similarity: NONE
- LLM semantic matching: NONE
- manual alias creation: NONE

Two-segment windows are adjacent ordered segment pairs only. No segment skipping, reordering, or cross-atom windows are permitted.

Every matching source occurrence remains represented. Cross-candidate collisions and cross-form identical values remain distinct. Overlap occurrence deduplication and semantic grouping are prohibited.

## Future input boundary

A separately authorized ZE2 execution may read only the frozen ZE0 manifest and frozen ZE1 inventory required by this contract.

It may not read raw D0318 candidate records, substantive frozen source files, or any expanded source universe.

It may not change ZE0 or ZE1 representation-generation rules.

## Reserved future output contract

Output root:

`evidence/representation_alignment/ZE2/deterministic_candidate_source_overlap_v1`

Overlap manifest:

`evidence/representation_alignment/ZE2/deterministic_candidate_source_overlap_v1/candidate_source_representation_overlap.json`

Execution state:

`evidence/representation_alignment/ZE2/deterministic_candidate_source_overlap_v1/_execution_state.json`

The root must not preexist a future authorized ZE2 execution.

The future manifest retains one record per candidate form, including zero-match records; therefore the expected candidate-form record count is `1197`.

## Scientific interpretation boundary

ZE2 overlap is not semantic evidence.

ZE2 overlap is not protocol support.

ZE2 non-overlap is not semantic non-support.

ZE2 overlap is not mapping.

ZE2 overlap does not establish C4.

ZE2 non-overlap does not establish C4 failure.

ZE2 does not alter the D0321 corrected-E1 zero-evidence result.

`C4_STATUS=UNRESOLVED`

`P8_MAPPING_AUTHORIZED=NO`

## Execution authorization

`ZE2_EXECUTION_AUTHORIZED=NO`

`REPRESENTATION_OVERLAP_EXECUTION_AUTHORIZED=NO`

D0336 grants zero execution attempts. A separate future execution authorization is mandatory.

ZE0 and ZE1 reruns remain prohibited.

Corrected E1 reexecution remains prohibited.

Source expansion, fuzzy matching, semantic matching, E2, E3, E4, C4, positive V4→V2 mapping, curl.json materialization, P8 mapping, P10 gold annotation, P11 analyzer implementation/execution, baselines, and repair remain unauthorized.

## Authoring noninterference

`ZE0_MANIFEST_READ_PERFORMED=NO`

`ZE0_CANDIDATE_VALUES_READ_PERFORMED=NO`

`ZE1_INVENTORY_CONTENT_READ_PERFORMED=NO`

`SUBSTANTIVE_SOURCE_CONTENT_READ_PERFORMED=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED=NO`

`REPRESENTATION_OVERLAP_PERFORMED=NO`

`ZE2_EXECUTION_PERFORMED=NO`

`MAPPING_PERFORMED=NO`

## Corrective-authoring noninterference

`D0336_PRIOR_PRECOMMIT_REVIEW=REVISION_REQUIRED_119_PASS_3_FINDINGS`

`D0336_PR_001_RESOLVED=YES`

`D0336_PR_002_RESOLVED=YES`

`D0336_PR_003_RESOLVED=YES`

`ZE0_MANIFEST_READ_PERFORMED_DURING_CORRECTION=NO`

`ZE1_INVENTORY_CONTENT_READ_PERFORMED_DURING_CORRECTION=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED_DURING_CORRECTION=NO`

`REPRESENTATION_OVERLAP_PERFORMED_DURING_CORRECTION=NO`

`ZE2_EXECUTION_PERFORMED_DURING_CORRECTION=NO`

`MAPPING_PERFORMED_DURING_CORRECTION=NO`

## Second corrective revision after fresh independent pre-commit review

The fresh independent review of the first revised D0336 author candidate returned `REVISION_REQUIRED` with `PASS_CHECK_COUNT=86` and exactly seven additional reproducibility findings.

Reviewed byte identities:

- decision SHA-256: `1cddfc11314b15f4af06fac5dba1d5c739d51c04a1978513432a99b46933c3e3`
- machine artifact SHA-256: `1023e754295ad63569d369ad4db5b9c66d106d35205a2b952183c20340d72461`

The corrections are limited to the future ZE2 output contract.

### D0336-PR-004 — candidate-form record order

The future manifest contains exactly `1197` candidate-form records.

Serialized scientific record order is frozen as:

1. exact frozen ZE0 candidate record order;
2. within each candidate, exact D0323 representation order F0 through F6.

Reordering is prohibited.

### D0336-PR-005 — source occurrence match order

Every retained `source_occurrence_matches` array is sorted stably and ascending by:

1. `source_ordinal`;
2. `atom_ordinal`;
3. `dot_segment_start_ordinal`;
4. `dot_segment_end_ordinal`.

For ordering only, a stored JSON `null` dot-segment ordinal has sort-key value `0`. The stored value itself remains `null`.

### D0336-PR-006 — match count

`match_count` is exactly:

`EXACT_LENGTH_OF_SOURCE_OCCURRENCE_MATCHES_ARRAY`

No unique-match, atom-level, source-level, or semantic count is substituted.

### D0336-PR-007 — source locator semantics

For `ZE0-F0-RAW-PATH-EXACT`, both segment ordinals are JSON `null`; the occurrence is located by the exact ZE1 source-atom locator.

For F1 and F6, segment start/end are the first and last segment ordinals of the full atom sequence.

For F2 and F4, start is the matched segment ordinal and end equals start.

For F3 and F5, start is the first ordinal of the adjacent two-segment window and end is `start + 1`.

### D0336-PR-008 — exact JSON file serialization

Serialization contract:

`SVF-ZE2-JSON-SERIALIZATION-V1`

Exact file-byte rules:

- encoding: UTF-8
- `ensure_ascii=false`
- `sort_keys=true`
- `indent=2`
- `allow_nan=false`
- line endings: LF
- exactly one final LF
- no trailing whitespace

Equivalent reference operation:

`json.dumps(object, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"`

### D0336-PR-009 — manifest schema

The future ZE2 manifest has an exact closed top-level schema consisting of:

- `artifact_type`
- `candidate_form_record_order`
- `candidate_form_records`
- `candidate_representation_value_hash_contract_id`
- `contract_id`
- `execution_id`
- `frozen_input_identity`
- `scientific_interpretation_boundary`
- `serialization_contract_id`

Additional top-level fields are prohibited.

`candidate_form_records` has exactly `1197` records and every record contains exactly:

- `candidate_index`
- `representation_id`
- `candidate_representation_value`
- `candidate_representation_value_sha256`
- `match_count`
- `source_occurrence_matches`

Each source occurrence match contains exactly:

- `source_member_id`
- `source_ordinal`
- `atom_ordinal`
- `source_atom_locator`
- `source_surface`
- `dot_segment_start_ordinal`
- `dot_segment_end_ordinal`

### D0336-PR-010 — execution-state schema and hash semantics

The future `_execution_state.json` schema is closed and requires:

- `authorization_id`
- `candidate_form_record_count`
- `candidate_record_count`
- `contract_id`
- `execution_id`
- `input_identity_verification`
- `nonzero_match_record_count`
- `output_hashes`
- `per_representation_match_summary`
- `scientific_interpretation_boundary`
- `serialization_contract_id`
- `status`
- `total_source_occurrence_match_count`
- `zero_match_record_count`

The fixed successful-state values include:

- `candidate_record_count=171`
- `candidate_form_record_count=1197`
- `status=COMPLETED`

Count invariants are mandatory:

- zero-match + nonzero-match records = 1197;
- each `match_count` equals the exact array length;
- total source occurrence matches equals the sum of all 1197 `match_count` values;
- each of the seven representation summaries contains exactly 171 candidate-form records.

Output-hash fields are exactly:

- `overlap_manifest_file_sha256`
- `overlap_manifest_canonical_json_sha256`
- `execution_state_full_file_sha256_recorded_externally`

The execution-state self-hash field contains the literal:

`NEXT_RESULT_CHECKPOINT`

The separate future result checkpoint records the actual full execution-state file SHA-256, preventing self-reference.

The overlap-manifest file SHA-256 hashes the exact serialized file bytes including the final LF.

The canonical JSON SHA-256 hashes UTF-8 bytes of compact JSON with `ensure_ascii=false`, `sort_keys=true`, separators `(",", ":")`, `allow_nan=false`, and no final newline.

### Second corrective-authoring noninterference

`D0336_PR_004_RESOLVED=YES`

`D0336_PR_005_RESOLVED=YES`

`D0336_PR_006_RESOLVED=YES`

`D0336_PR_007_RESOLVED=YES`

`D0336_PR_008_RESOLVED=YES`

`D0336_PR_009_RESOLVED=YES`

`D0336_PR_010_RESOLVED=YES`

`ZE0_MANIFEST_READ_PERFORMED_DURING_SECOND_CORRECTION=NO`

`ZE1_INVENTORY_CONTENT_READ_PERFORMED_DURING_SECOND_CORRECTION=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED_DURING_SECOND_CORRECTION=NO`

`REPRESENTATION_OVERLAP_PERFORMED_DURING_SECOND_CORRECTION=NO`

`ZE2_EXECUTION_PERFORMED_DURING_SECOND_CORRECTION=NO`

`P8_MAPPING_PERFORMED_DURING_SECOND_CORRECTION=NO`

## Activation lifecycle

D0336 authoring alone is not effective.

A local commit alone is not effective.

The exact two-file D0336 checkpoint must independently pass pre-commit review, exact local commit, independent post-commit review, publication, and exact remote readback.

Even after D0336 becomes effective, ZE2 execution remains unauthorized until a separate execution-authorization checkpoint is published and effective.

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0336_ZE2_DETERMINISTIC_OVERLAP_DESIGN_AUTHOR_CANDIDATE`
