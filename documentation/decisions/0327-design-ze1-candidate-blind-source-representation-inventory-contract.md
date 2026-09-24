# D0327 — Design ZE1 Candidate-Blind Source-Representation Inventory Contract

## Status

`DESIGN_AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0327 is design-only.

D0327 does **not** authorize or execute ZE1.

D0327 does not open substantive frozen source bytes.

D0327 does not read the ZE0 candidate-representation manifest, traverse the governed candidate list, or read candidate values.

## Source-binding correction

Earlier D0327 authoring did not produce a checkpoint because a generic resolver incorrectly expected the source records to use the pair-domain field schema.

The authoritative D0318 source manifest instead uses the native fields including:

`member_id`

`path`

`sha256`

`git_blob_oid`

A subsequent read-only verifier also stopped before completion because it looked for `git_blob` rather than the native `git_blob_oid` field.

Both failures occurred before D0327 creation or ZE1 execution and consumed no execution authorization.

The corrected design binds directly and only to:

`$.frozen_substantive_source_binding`

and its exact source list:

`$.frozen_substantive_source_binding.sources`

No generic recursive source resolver is used.

## Frozen source universe

The future ZE1 source universe is exactly:

`C1-S01`

`C1-S02`

`C1-S03`

`C1-S04`

The D0318 frozen source-manifest canonical identity is:

`b6c97642ee0a3bc8de5839209a0a8546feb61beedc198c24a8c43c44b6534b52`

This identity is inherited directly from D0318.

It is not replaced with a newly invented normalization or re-canonicalization.

The exact native source metadata records, including paths, SHA-256 values, Git blob OIDs, formats, classes, roles, extraction-rule identifiers, and locators, are preserved in the D0327 machine artifact.

No additional source may be introduced.

## Candidate-blindness requirement

A future ZE1 source-inventory execution may not read:

- the ZE0 candidate-representation manifest;
- D0318 candidate records;
- candidate property-path values;
- candidate-derived representation values.

It may not use:

- candidate-specific queries;
- candidate-specific filtering;
- candidate-specific source subsets;
- candidate-specific tokenization changes;
- candidate-specific representation-rule changes;
- semantic relevance filtering.

ZE1 must therefore be generated independently of candidate-side representation values.

## Design identifiers

Design ID:

`SVF-ZE1-CANDIDATE-BLIND-SOURCE-REPRESENTATION-INVENTORY-CONTRACT-V1`

Grammar ID:

`SVF-ZE1-CANDIDATE-BLIND-SOURCE-REPRESENTATION-GRAMMAR-V1`

Reserved future execution ID:

`SVF-ZE1-SOURCE-REPRESENTATION-INVENTORY-RUN-001`

These identifiers reserve the contract namespace only.

They do not grant execution authorization.

## Future source-read contract

D0327 does not authorize substantive source reads.

A separate successor authorization is mandatory.

If ZE1 is later authorized, only the exact four frozen D0318 source byte sequences may be used.

Decoding must use strict UTF-8.

No Unicode normalization, Unicode case-folding, stemming, synonym expansion, stopword removal, semantic parsing, or source-specific semantic querying is permitted.

## Source atom grammar

The future executor must scan each decoded source left-to-right.

A source atom is a maximal contiguous character span in which each code point is one of:

- Unicode General Category Letter (`L*`);
- Unicode General Category Number (`N*`);
- literal `_`;
- literal `-`;
- literal `.`.

A maximal allowed-character span containing no Unicode Letter or Number is discarded.

Every retained occurrence is kept.

Occurrence records are not deduplicated.

The runtime Unicode database version must be recorded.

Source-atom locators must contain:

- source member ID;
- atom ordinal;
- zero-based start decoded-character offset;
- exclusive end decoded-character offset;
- one-based start line;
- one-based start column.

## Source representation forms

### ZE1-SF0-RAW-ATOM-EXACT

Exact retained source-atom string without normalization.

### ZE1-SF1-DOT-SEGMENT-SEQUENCE-EXACT

Split the raw atom on literal `.`.

Leading, internal, and trailing empty dot segments are retained.

### ZE1-SF2-PER-SEGMENT-LEXICAL-TOKEN-SEQUENCES

For each dot segment independently:

- `_` and `-` are separators;
- split an ASCII lowercase letter or digit followed by ASCII uppercase;
- split an ASCII acronym boundary before the uppercase character that begins a capitalized word;
- lowercase ASCII `A-Z` only;
- preserve digits;
- preserve non-ASCII code points;
- discard separator-created empty lexical tokens.

### ZE1-SF3-FLATTENED-LEXICAL-TOKEN-SEQUENCE

Concatenate ZE1-SF2 token sequences in original dot-segment order.

## Ordered token-occurrence stream

The future inventory must emit each ZE1-SF3 token occurrence in deterministic source order.

Every occurrence must preserve source member, atom ordinal, dot-segment ordinal, lexical-token ordinal, and the source-atom locator.

No candidate comparison or semantic grouping is performed during source inventory construction.

## Collision and absence semantics

Repeated raw-atom occurrences are retained.

Repeated token occurrences are retained.

Dot-created empty segments are retained.

Separator-created empty lexical tokens are discarded.

A representation collision does not establish semantic equivalence.

A representation collision does not establish protocol support.

Absence from the future ZE1 inventory does not establish semantic non-support.

## Synthetic-only conformance vectors

Five synthetic vectors are frozen in the D0327 machine artifact.

They contain no governed source content and no governed candidate content.

They are **not executed during D0327 authoring**.

Any future synthetic conformance execution requires a separately governed non-consuming integrity checkpoint.

## Future output contract

Reserved future output root:

`evidence/representation_alignment/ZE1/source_representation_inventory_v1`

Reserved future inventory:

`evidence/representation_alignment/ZE1/source_representation_inventory_v1/source_representation_inventory.json`

Reserved future execution state:

`evidence/representation_alignment/ZE1/source_representation_inventory_v1/_execution_state.json`

The output root must not preexist a future authorized execution.

A future inventory must contain exactly four source records in order:

`C1-S01`, `C1-S02`, `C1-S03`, `C1-S04`.

All retained atom occurrences and token occurrences must be preserved.

## Future preauthorization integrity boundary

A future integrity transaction must itself be separately governed.

Before substantive source bytes are opened, it may verify only bounded identity/precondition facts such as:

- effective D0327 publication;
- exact D0318 source-manifest identity;
- four source IDs and their order;
- frozen source paths from governance metadata;
- Git blob OIDs through Git tree metadata;
- ZE1 output-root absence;
- synthetic-only grammar conformance.

It may not:

- open substantive source bytes;
- read the ZE0 candidate representation manifest;
- traverse D0318 candidate records;
- read candidate values;
- compare candidates with sources;
- perform overlap matching;
- perform semantic adjudication.

A failure must fail closed before ZE1 attempt start.

## Future execution governance

D0327 grants no ZE1 execution authorization.

A separate ZE1 execution-authorization checkpoint is required.

The intended execution is one-shot.

The recommended future consumption boundary is:

`FIRST_SUBSTANTIVE_SOURCE_CONTENT_READ_OR_FIRST_ZE1_OUTPUT_WRITE_WHICHEVER_OCCURS_FIRST`

The recommended maximum attempt count is one.

Automatic retry after consumption should be prohibited.

The frozen SHA-256 of each source must be verified when substantive source bytes are first authorized to be read.

## Scientific interpretation boundary

A future ZE1 inventory is a deterministic source-side representation artifact only.

It is not semantic evidence.

It is not protocol support.

It is not semantic non-support.

It is not mapping evidence.

It does not establish C4.

It does not alter the D0321 zero-evidence result.

ZE1 alone cannot establish representation mismatch.

Any later candidate/source representation-overlap analysis belongs to separately governed ZE2.

## Current authorization state

`ZE1_EXECUTION_AUTHORIZED=NO`

`ZE2_EXECUTION_AUTHORIZED=NO`

`ZE3_EXECUTION_AUTHORIZED=NO`

`ZE4_EXECUTION_AUTHORIZED=NO`

`REPRESENTATION_OVERLAP_EXECUTION_AUTHORIZED=NO`

`CORRECTED_E1_REEXECUTION_AUTHORIZED=NO`

`SOURCE_EXPANSION_AUTHORIZED=NO`

`FUZZY_MATCHING_AUTHORIZED=NO`

`SEMANTIC_MATCHING_AUTHORIZED=NO`

`E2_AUTHORIZED=NO`

`E3_AUTHORIZED=NO`

`E4_AUTHORIZED=NO`

`C4_AUTHORIZED=NO`

`B2_AUTHORIZED=NO`

`POSITIVE_V4_TO_V2_MAPPING_AUTHORIZED=NO`

`CURL_JSON_MATERIALIZATION_AUTHORIZED=NO`

`P8_MAPPING_AUTHORIZED=NO`

`P10_GOLD_ANNOTATION_AUTHORIZED=NO`

`P11_ANALYZER_IMPLEMENTATION_AUTHORIZED=NO`

`P11_ANALYZER_EXECUTION_AUTHORIZED=NO`

`BASELINE_EXECUTION_AUTHORIZED=NO`

`REPAIR_EXECUTION_AUTHORIZED=NO`

## D0327 authoring transaction

`SUBSTANTIVE_SOURCE_CONTENT_READ_PERFORMED=NO`

`ZE0_MANIFEST_READ_PERFORMED=NO`

`CANDIDATE_LIST_TRAVERSED=NO`

`CANDIDATE_VALUE_READ_PERFORMED=NO`

`CANDIDATE_REPRESENTATION_VALUE_READ_PERFORMED=NO`

`SYNTHETIC_VECTORS_EXECUTED=NO`

`SOURCE_REPRESENTATION_INVENTORY_PERFORMED=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED=NO`

`MATCHING_PERFORMED=NO`

`SEMANTIC_ADJUDICATION_PERFORMED=NO`

`ZE1_EXECUTION_PERFORMED=NO`

`ZE2_EXECUTION_PERFORMED=NO`

`E2_EXECUTION_PERFORMED=NO`

`MAPPING_PERFORMED=NO`

`ANALYZER_EXECUTION_PERFORMED=NO`

`REPAIR_EXECUTION_PERFORMED=NO`

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0327_ZE1_CANDIDATE_BLIND_SOURCE_INVENTORY_DESIGN_AUTHOR_CANDIDATE`
