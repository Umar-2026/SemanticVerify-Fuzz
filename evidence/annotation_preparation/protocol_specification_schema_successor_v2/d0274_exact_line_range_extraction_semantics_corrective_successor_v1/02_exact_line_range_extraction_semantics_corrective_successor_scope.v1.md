# D0274 Exact Line-Range Extraction Semantics Corrective Successor

## Role

D0274 is a contract-only corrective successor.

D0273 remains historically unchanged. D0273 designated D0274 as the
bounded retained-evidence materialization execution.

Subsequent read-only static recovery found the historical D0265/D0266
artifacts record the target locators, one-read boundary, extracted-unit
hashes, and related component concepts, but do not freeze one coherent
line-range-to-text extraction algorithm.

In particular, the recovered verifier logic does not expose an explicit
LINE_RANGE parser or actual snapshot line-index/slice implementation.

Therefore D0274 performs no snapshot-content read and performs no
materialization.

## Exact extraction algorithm frozen by D0274

A later materialization transaction must use
`D0274-LINE-RANGE-UTF8-EXTRACTION-ALGORITHM-V1`.

For each authorized candidate snapshot:

1. Read the exact authorized snapshot once into raw bytes.
2. Verify byte count, SHA-256, and Git blob OID before extraction.
3. Decode the exact bytes using strict UTF-8 with no BOM removal,
   normalization, or whitespace trimming.
4. Parse locators only with:
   `^L([1-9][0-9]*)-L([1-9][0-9]*)$`.
5. Use one-based inclusive line numbering.
6. Segment decoded text using Python `splitlines()` semantics without
   retaining line terminators.
7. Select `lines[start_line - 1:end_line]`.
8. Join selected lines using exactly one LF character (`\n`).
9. Add no prefix, suffix, trimming, or terminal newline.
10. Compute SHA-256 over the UTF-8 bytes of that exact extracted text.

JSON serialization quotes and JSONL record newlines are not part of the
unit hash.

## Historical-hash compatibility gate

Candidates 8 and 9 already have five frozen D0266 extracted-unit hashes.

A later D0275 transaction must reproduce all five hashes exactly.

Any mismatch is fail-closed: no durable D0275 materialization result may be
accepted.

Candidate 6 unit hashes may be computed only using the same frozen
algorithm and only after all five candidate-8/9 compatibility anchors
match.

Passing this compatibility gate may establish implementation compatibility
with the already frozen D0266 hashes. D0274 itself does not claim
historical algorithm equivalence before execution.

## D0275

D0275 is the prospective bounded retained-evidence materialization
execution.

D0274 does not authorize D0275 execution.

D0275 may only be authorized after D0274 independently passes its
verification/freeze checkpoint.

## D0276

D0276 is the prospective later branch-local positional adjudication.

D0274 does not authorize D0276.

D0276 may not be authorized before D0275 executes and may not execute
before D0275 independently passes its verification/freeze checkpoint.

## Prohibitions

D0274 performs no:

- snapshot-content read;
- materialization;
- positional adjudication;
- positional-status assignment;
- target-evidence rejudgment;
- locator filtering or reselection;
- new locator discovery;
- reference following;
- source reopening;
- Class06 reclassification;
- sufficiency mutation;
- B2;
- analyzer;
- baseline;
- repair.
