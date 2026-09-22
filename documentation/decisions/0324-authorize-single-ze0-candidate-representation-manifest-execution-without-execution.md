# D0324 — Authorize One Future ZE0 Candidate-Representation Manifest Execution

## Status

`AUTHORIZATION_AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0324 is an authorization checkpoint candidate.

D0324 does **not** execute ZE0.

No candidate representation is generated during D0324 authoring.

No ZE0 output file or output directory is created.

## Effective source checkpoint

The source checkpoint is published D0323:

`ed1b6c5fd78b8690560d472b1241fa9bcfda3635`

D0323 decision SHA-256:

`df0671d41f21e6014bfbe445b1e7f18567598ffd65b8b58dcdba3d4c5b54cb07`

D0323 machine-artifact SHA-256:

`a7ca71ba4570c23ae89b3536aab729fdc194f3c92cccf74d733a8358eca7fefa`

The frozen ZE0 contract remains:

`SVF-ZE0-CANDIDATE-REPRESENTATION-MANIFEST-CONTRACT-V1`

The frozen representation grammar remains:

`SVF-ZE0-DET-REP-GRAMMAR-V1`

## Authorization scope

Authorization ID:

`SVF-D0324-ZE0-ONE-SHOT-AUTH-V1`

After D0324 is independently verified, committed, published, and its required preauthorization integrity verification separately passes, D0324 may authorize **at most one** ZE0 execution attempt.

Future execution ID:

`SVF-ZE0-CANDIDATE-REPRESENTATION-RUN-001`

The authorized operation is limited to deterministic candidate-side representation-manifest materialization under D0323.

It does not authorize ZE1.

It does not authorize source inventory, source comparison, matching, semantic adjudication, mapping, E2, analyzer work, baseline work, or repair.

## Frozen input

The candidate namespace is:

`SCHEMA_V2_PROPERTY_PATH`

Candidate count:

`171`

Candidate manifest canonical JSON SHA-256:

`c2746447215aa5aa2be0abea3bb631043eb0bb12745cc54309881d88a5a1f908`

The frozen candidate-source governance artifact is:

`evaluation/governance_reconciliation/d0318_corrected_e1_successor_design.json`

Its SHA-256 is:

`0216b4c5b40627bd5fdf80e7258c7c16169bedd3adb956e71118c733170243d7`

Candidate order remains exact frozen ordinal order.

No candidate may be selected, omitted, added, or reordered.

## Required preauthorization integrity verification

D0324 does not permit immediate ZE0 execution merely by being authored.

After D0324 publication, a separate non-consuming integrity transaction must verify:

1. effective D0324 publication identity;
2. exact D0323 decision and machine-artifact identities;
3. exact D0318 candidate-source governance-artifact path and bytes;
4. exact candidate count of 171;
5. recomputed canonical candidate-manifest SHA-256;
6. exact candidate ordinal ordering;
7. absence of the future ZE0 output root;
8. conformance of the future implementation against the frozen synthetic test vectors.

This integrity transaction may enumerate the frozen candidate list solely to verify identity.

It may not generate a ZE0 representation value for any actual frozen candidate.

It may not create the ZE0 output root.

It may not write candidate records.

It may not read substantive source files.

A failed integrity verification fails closed before ZE0 attempt start and does not consume the one-shot authorization.

## Synthetic implementation-conformance vectors

Before any actual candidate representation is generated, the future ZE0 implementation must pass these synthetic vectors.

### Vector 1

Input:

`foo.barBaz`

Expected F1:

`["foo", "barBaz"]`

Expected F2:

`"barBaz"`

Expected F4:

`["bar", "baz"]`

### Vector 2

Input:

`foo.HTTPServer`

Expected F1:

`["foo", "HTTPServer"]`

Expected F2:

`"HTTPServer"`

Expected F4:

`["http", "server"]`

### Vector 3

Input:

`foo.x1Y2`

Expected F1:

`["foo", "x1Y2"]`

Expected F2:

`"x1Y2"`

Expected F4:

`["x1", "y2"]`

### Vector 4

Input:

`foo.foo_bar-baz`

Expected F1:

`["foo", "foo_bar-baz"]`

Expected F2:

`"foo_bar-baz"`

Expected F4:

`["foo", "bar", "baz"]`

### Vector 5

Input:

`.a.`

Expected F1:

`["", "a", ""]`

Expected F2:

`""`

Expected F4:

`[]`

Failure of any synthetic test vector fails closed before attempt start and does not consume the execution authorization.

## One-shot consumption semantics

The future D0324 authorization is **not** consumed by:

- identity verification;
- candidate enumeration performed only for identity verification;
- recomputation of the frozen candidate-manifest hash;
- execution of synthetic test vectors.

The one-shot authorization becomes consumed atomically at the first of:

1. application of any D0323 representation-generation rule to an actual frozen candidate for ZE0 materialization; or
2. first write inside the governed ZE0 output root.

Representation generation includes path segmentation, lexicalization, or construction of any F0–F6 representation for an actual frozen candidate for materialization.

After consumption:

`AUTOMATIC_RETRY_AUTHORIZED=NO`

A failed or incomplete started attempt requires a separate successor authorization.

A successfully completed ZE0 execution may not be rerun under D0324.

## Governed output

Future output root:

`evidence/representation_alignment/ZE0/candidate_representation_manifest_v1`

Future manifest:

`evidence/representation_alignment/ZE0/candidate_representation_manifest_v1/candidate_representation_manifest.json`

Future execution state:

`evidence/representation_alignment/ZE0/candidate_representation_manifest_v1/_execution_state.json`

The output root must not preexist when preauthorization integrity verification occurs.

Partial output from a consumed failed attempt may not be silently deleted, overwritten, or retried.

## Successful ZE0 completion

A successful authorized ZE0 execution must produce:

- exactly 171 candidate records;
- exact frozen candidate ordinal order;
- exact frozen raw property path for every candidate;
- exactly seven representation forms per candidate;
- only D0323 rule-generated representations;
- zero substantive-source reads;
- zero candidate-to-source comparisons;
- zero matching operations;
- zero semantic judgments;
- zero mapping operations.

The execution state must terminate as:

`COMPLETED`

The completed output requires a separate result checkpoint.

ZE1 does not become authorized automatically.

## Scientific boundary

The future ZE0 manifest remains diagnostic candidate-side representation data only.

It is not evidence.

It is not semantic support.

It is not semantic non-support.

It is not mapping.

It does not establish C4.

It does not modify the published D0321 zero-evidence result.

## Authorization state during D0324 authoring

During this authoring transaction:

`ZE0_EXECUTION_STARTED=NO`

`ZE0_EXECUTION_COMPLETED=NO`

`D0324_AUTHORIZATION_CONSUMED=NO`

`CANDIDATE_REPRESENTATION_MANIFEST_GENERATED=NO`

`ZE0_OUTPUT_ROOT_CREATED=NO`

D0324 itself is not effective until independently verified, committed, and published.

## Downstream authorization state

After D0324 publication, only the separately governed ZE0 preauthorization integrity verification is immediately permitted.

ZE0 execution additionally requires that integrity verification to pass.

`ZE1_EXECUTION_AUTHORIZED=NO`

`ZE2_EXECUTION_AUTHORIZED=NO`

`ZE3_EXECUTION_AUTHORIZED=NO`

`ZE4_EXECUTION_AUTHORIZED=NO`

`SOURCE_REPRESENTATION_INVENTORY_AUTHORIZED=NO`

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

`P8_MAPPING_AUTHORIZED=NO`

`P10_GOLD_ANNOTATION_AUTHORIZED=NO`

`P11_ANALYZER_IMPLEMENTATION_AUTHORIZED=NO`

`P11_ANALYZER_EXECUTION_AUTHORIZED=NO`

`BASELINE_EXECUTION_AUTHORIZED=NO`

`REPAIR_EXECUTION_AUTHORIZED=NO`

## D0324 authoring side-effect boundary

D0324 authoring:

- does not enumerate the actual candidate list;
- does not generate actual candidate representations;
- does not create ZE0 output;
- does not consume the future authorization;
- does not read substantive sources;
- does not execute matching;
- does not execute ZE1;
- does not execute E2;
- does not perform mapping;
- does not execute analyzer, baseline, or repair work.

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0324_SINGLE_ZE0_EXECUTION_AUTHORIZATION_AUTHOR_CANDIDATE`

No ZE0 execution is authorized by the unpublished D0324 author candidate.
