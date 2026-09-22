# D0323 — Design ZE0 Deterministic Candidate Representation Manifest Contract

## Status

`DESIGN_ONLY_AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0323 freezes the candidate-side representation grammar for the future ZE0 stage defined by D0322.

D0323 does **not** execute ZE0 and does not materialize the 171-record candidate representation manifest.

It performs no substantive-source read, source inventory, candidate-to-source comparison, matching, semantic adjudication, mapping, corrected-E1 rerun, gold annotation, analyzer execution, baseline execution, or repair.

## Effective source checkpoint

The source checkpoint is published D0322:

`6e193d8e5d0095e488bb6da36824e72a9b2119bc`

D0322 decision SHA-256:

`9070a0deab08fb9f4d94356ceeec61d6134ad596943c96b96c7a86d3d5a92b41`

D0322 machine-artifact SHA-256:

`329ddc3449cb0f9afb16df2d407abca378967937b523bfedc2b7cb41853e2736`

## Frozen candidate universe

ZE0 remains bound to the exact 171-candidate `SCHEMA_V2_PROPERTY_PATH` universe inherited through D0318–D0322.

Candidate manifest canonical JSON SHA-256:

`c2746447215aa5aa2be0abea3bb631043eb0bb12745cc54309881d88a5a1f908`

No candidate may be added, removed, reselected, subsetted, or reordered.

## ZE0 contract

Contract ID:

`SVF-ZE0-CANDIDATE-REPRESENTATION-MANIFEST-CONTRACT-V1`

Representation grammar ID:

`SVF-ZE0-DET-REP-GRAMMAR-V1`

ZE0 is candidate-side only.

No substantive source content is required to compute the future manifest.

`ZE0_EXECUTION_AUTHORIZED=NO`

`CANDIDATE_REPRESENTATION_MANIFEST_MATERIALIZATION_AUTHORIZED=NO`

## Deterministic path segmentation

For a frozen raw schema-V2 property-path string:

1. preserve the raw string exactly;
2. split it from left to right only on literal ASCII period `.`;
3. preserve empty segments;
4. do not modify the bytes of the resulting exact segments;
5. preserve source-string order.

This rule is:

`ZE0-R-PATH-DOT-SPLIT-V1`

No candidate-specific parsing branch is permitted.

## Deterministic lexicalization

Lexicalization rule:

`ZE0-R-ASCII-IDENTIFIER-LEXICALIZATION-V1`

For each exact path segment:

1. scan left to right;
2. treat ASCII `_` and `-` as lexical separators;
3. split at ASCII lowercase-or-digit → uppercase boundaries;
4. split acronym boundaries before an uppercase character preceded by uppercase and followed by lowercase;
5. lowercase ASCII `A-Z` only;
6. preserve decimal digits;
7. preserve non-ASCII code points without semantic normalization;
8. discard only zero-length lexical tokens introduced by separators.

There is:

- no Unicode semantic normalization;
- no stemming;
- no lemmatization;
- no synonym expansion;
- no abbreviation expansion;
- no semantic paraphrasing;
- no LLM-generated alias;
- no embedding-generated alias;
- no hand-authored candidate-specific rewrite.

## Frozen representation forms

Every future ZE0 candidate record must contain all seven forms in this exact order.

### ZE0-F0-RAW-PATH-EXACT

Exact raw schema-V2 property path.

No transformation.

### ZE0-F1-DOT-SEGMENT-SEQUENCE-EXACT

Ordered literal-dot segment sequence.

No segment-text mutation.

### ZE0-F2-LEAF-SEGMENT-EXACT

The final element of F1.

If the raw path terminates in `.`, the final empty segment remains empty.

### ZE0-F3-PARENT-LEAF-SEQUENCE-EXACT

The final two F1 segments when at least two segments exist.

For a one-segment path, F3 contains that one segment.

### ZE0-F4-LEAF-LEXICAL-TOKENS

The frozen lexicalization rule applied to F2.

### ZE0-F5-PARENT-LEAF-LEXICAL-TOKEN-SEQUENCES

The frozen lexicalization rule applied independently and in order to each F3 segment.

### ZE0-F6-ALL-SEGMENT-LEXICAL-TOKEN-SEQUENCES

The frozen lexicalization rule applied independently and in order to every F1 segment.

## Representation semantics

All seven forms are diagnostic representations only.

A representation form is not:

- evidence;
- semantic support;
- semantic non-support;
- mapping;
- candidate disposition;
- C4 closure.

Future lexical overlap would not by itself establish support.

Future lexical non-overlap would not by itself establish non-support.

## Collision policy

If two candidates later produce identical derived values, both are retained.

No collision may trigger:

- candidate merging;
- candidate removal;
- alias invention;
- semantic-equivalence judgment;
- mapping.

Identical values under different representation IDs remain separate because their structural roles differ.

Empty exact segments remain present.

An empty lexical-token array remains an empty array.

Neither condition is semantic non-support.

## Future ZE0 manifest schema

A later separately authorized ZE0 execution must materialize exactly 171 records in frozen candidate ordinal order.

Required top-level fields are:

- `artifact_type`
- `contract_id`
- `source_checkpoint_commit`
- `candidate_namespace`
- `candidate_manifest_canonical_json_sha256`
- `record_count`
- `records`
- `manifest_canonical_json_sha256`

Each record must contain:

- `candidate_ordinal`
- `schema_v2_property_path`
- `representation_grammar_id`
- `representations`

Every record must contain all seven frozen representation IDs in contract order.

The raw property path must equal its frozen input exactly.

## Future ZE0 execution invariants

Any later ZE0 execution must fail closed before manifest materialization if:

- candidate count is not exactly 171; or
- frozen candidate-manifest identity does not match
  `c2746447215aa5aa2be0abea3bb631043eb0bb12745cc54309881d88a5a1f908`.

A future ZE0 execution may not:

- read substantive source files;
- branch on candidate identity;
- manually edit generated representations;
- perform matching;
- compare candidates to sources;
- make semantic judgments;
- perform mapping.

## Lifecycle boundary

D0323 freezes the ZE0 design only.

A future ZE0 execution requires a separate authorization checkpoint.

Any future ZE0 output requires its own result checkpoint.

ZE1 does not become authorized automatically after ZE0.

`ZE1_EXECUTION_AUTHORIZED=NO`

## Existing zero-evidence result remains unchanged

D0323 does not alter D0321.

The corrected-E1 result remains:

`PAIR_RECORD_COUNT=684`

`ZERO_OCCURRENCE_PAIR_COUNT=684`

`NONZERO_OCCURRENCE_PAIR_COUNT=0`

`EVIDENCE_UNIT_COUNT=0`

`C4_STATUS=UNRESOLVED`

`CURRENT_E2_EVIDENCE_UNIT_DOMAIN_SIZE=0`

The D0319 authorization remains consumed.

`CORRECTED_E1_REEXECUTION_AUTHORIZED=NO`

`D0319_REUSE_AUTHORIZED=NO`

## Downstream authorization state

`ZE0_EXECUTION_AUTHORIZED=NO`

`ZE1_EXECUTION_AUTHORIZED=NO`

`ZE2_EXECUTION_AUTHORIZED=NO`

`ZE3_EXECUTION_AUTHORIZED=NO`

`ZE4_EXECUTION_AUTHORIZED=NO`

`CANDIDATE_REPRESENTATION_MANIFEST_MATERIALIZATION_AUTHORIZED=NO`

`SOURCE_REPRESENTATION_INVENTORY_AUTHORIZED=NO`

`REPRESENTATION_OVERLAP_EXECUTION_AUTHORIZED=NO`

`SUCCESSOR_EXTRACTION_EXECUTION_AUTHORIZED=NO`

`SOURCE_EXPANSION_AUTHORIZED=NO`

`FUZZY_MATCHING_AUTHORIZED=NO`

`SEMANTIC_MATCHING_AUTHORIZED=NO`

`E2_AUTHORIZED=NO`

`E3_AUTHORIZED=NO`

`E4_AUTHORIZED=NO`

`C4_AUTHORIZED=NO`

`B2_AUTHORIZED=NO`

`P8_MAPPING_AUTHORIZED=NO`

`P10_GOLD_ANNOTATION_AUTHORIZED=NO`

`P11_ANALYZER_IMPLEMENTATION_AUTHORIZED=NO`

`P11_ANALYZER_EXECUTION_AUTHORIZED=NO`

`BASELINE_EXECUTION_AUTHORIZED=NO`

`REPAIR_EXECUTION_AUTHORIZED=NO`

## D0323 authoring transaction

D0323 authoring reads only the previously published D0322 governance artifact.

It does not enumerate or transform the 171 candidate paths.

It does not generate representation values.

It does not generate the ZE0 manifest.

It does not read substantive source files.

It does not execute ZE1, ZE2, E2, mapping, or corrected E1.

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0323_ZE0_CANDIDATE_REPRESENTATION_MANIFEST_DESIGN_AUTHOR_CANDIDATE`

No ZE0 execution is authorized merely by authoring D0323.
