# D0274 — Establish Exact Line-Range Extraction Semantics, Redesignate Materialization to D0275, and Positional Adjudication to D0276 Without Execution

## Decision

D0274 is a contract-only corrective successor.

D0273 remains historically unchanged. It designated D0274 as the bounded
retained-evidence materialization execution.

Read-only recovery established that the historical D0265/D0266 artifacts
contain target locators, snapshot-read accounting, extracted-unit hashes,
and individual extraction-related concepts, but do not freeze one coherent
line-range-to-text extraction algorithm.

Recovered bindings:

- preexecution discovery SHA256: fadecb41853811786e51280f611cddef903ec2766225f6baa676901ecd43b92d
- static extraction AST bundle SHA256: 2015a42ac77d58470d1e1b5e25bfabc2be53216df03b75f378bd4cb53cda5f6f
- D0266 extraction trace bundle SHA256: 4bf7b6f95700303b959a2da14c7fddb1132ddabb92e1520c323999af3eaff554
- historical extraction recovery SHA256: 2c3af32c75d6354a62a51827226f45941b6439c63406673def4707298e42370c
- candidate 8/9 expected-unit hash binding SHA256: e8cd38f69aeeaffa7e8fa9854740319f1da35c67278772a46cab8aca2fec1102

Therefore D0274 does not read snapshot bytes and does not execute
materialization.

## Exact algorithm

D0274 freezes
`D0274-LINE-RANGE-UTF8-EXTRACTION-ALGORITHM-V1`.

The later materializer must:

1. read each authorized snapshot once;
2. verify byte count, raw-byte SHA-256, and Git blob OID;
3. strict-decode exact bytes as UTF-8;
4. parse only `^L([1-9][0-9]*)-L([1-9][0-9]*)$`;
5. use one-based inclusive line numbering;
6. segment with Python `splitlines()` semantics without terminators;
7. select `lines[start-1:end]`;
8. join selected lines with exactly one LF;
9. apply no trimming and no terminal newline; and
10. SHA-256 the UTF-8 bytes of that exact extracted text.

## Compatibility gate

A later D0275 execution must reproduce all five frozen candidate-8/9
D0266 extracted-unit hashes.

Any mismatch fails closed and prevents a durable D0275 materialization
result.

Candidate-6 unit hashes may be accepted only after all five candidate-8/9
anchors match and must use exactly the same D0274 algorithm.

D0274 makes no historical-equivalence claim before that compatibility gate
is executed.

## Successor redesignation

D0275 becomes the prospective bounded retained-evidence materialization
execution checkpoint.

D0274 does not authorize D0275 execution. Independent verification/freeze
of D0274 is required first.

D0276 becomes the prospective separate branch-local positional-adjudication
checkpoint.

D0274 does not authorize D0276. D0276 cannot be authorized before D0275
executes and cannot execute before D0275 independently passes its
verification/freeze checkpoint.

No positional adjudication, positional assignment, Class06 reclassification,
sufficiency mutation, B2, analyzer, baseline, or repair occurs in D0274.
