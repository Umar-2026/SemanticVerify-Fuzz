# Decision 0337 — Authorize a single ZE2 deterministic representation-overlap execution

## Status

`DESIGN_ONLY_AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0337 is authorization design only. No ZE2 execution occurs in this checkpoint.

## Governing effective contract

- D0336 commit: `40561ff59630f82e9fa7427632c87894ca95e08d`
- D0336 decision SHA-256: `a5f94caaf7035f2179902a258eafbe9e3beac9b6b5a2724d91448af09ff10cf1`
- D0336 machine artifact SHA-256: `8381b86f29e0e1a04b1c8728e4ff47f31569c20b5906f8bcdd494cebcb42f37b`

Authorization ID: `SVF-D0337-ZE2-SINGLE-EXECUTION-AUTH-V1`

Authorized contract: `SVF-ZE2-DETERMINISTIC-STRUCTURAL-REPRESENTATION-OVERLAP-V1`

Reserved execution ID: `SVF-ZE2-DETERMINISTIC-REPRESENTATION-OVERLAP-RUN-001`

## Exact attempt capacity

D0337 may make exactly one ZE2 execution attempt conditionally available after D0337 is independently reviewed, committed, published, and remotely confirmed.

`MAXIMUM_ATTEMPT_CAPACITY=1`

`SUCCESSFUL_EXECUTION_CAPACITY=1`

`AUTHORIZATION_CONSUMED_AT_AUTHORING=NO`

`AUTOMATIC_RETRY_AFTER_CONSUMPTION_AUTHORIZED=NO`

## Frozen ZE0 input

- manifest: `evidence/representation_alignment/ZE0/candidate_representation_manifest_v1/candidate_representation_manifest.json`
- Git blob OID: `09f333b71a4b8d85a68a5d54a8f32b50bb80c1a0`
- manifest SHA-256: `556096b6b6adc0708aee4903c5a4eb033231c04d7abe125d14f9dd5ad9760693`
- candidate canonical SHA-256: `c2746447215aa5aa2be0abea3bb631043eb0bb12745cc54309881d88a5a1f908`

## Frozen ZE1 input

- inventory: `evidence/representation_alignment/ZE1/source_representation_inventory_v1/source_representation_inventory.json`
- Git blob OID: `3a033de80a9945f9f3f79c84a3cf72e03c54e703`
- full scientific inventory SHA-256: `5077ad7cfbe393c3a6000348aa667ed2a0d439e11538ec65c08999537f524d7c`
- canonical JSON SHA-256: `1a732561d11f83ebbe3dde3386239dea3654dbf00e5a664a94e74dea39a6e4d8`
- expected full-file size: `570156431` bytes

The Git object for the ZE1 inventory is an LFS pointer; the scientific SHA above binds the full payload.

## Post-publication non-consuming preexecution reconciliation

Reconciliation ID: `SVF-D0337-ZE2-POSTPUBLICATION-PREEXECUTION-RECONCILIATION-V1`

Publication of D0337 alone does not make consuming permissions immediately exercisable.

Before the single attempt may consume its authorization, a separate read-only non-consuming reconciliation must PASS.

That reconciliation may verify governance identities, Git paths, Git blob OIDs, the ZE1 LFS pointer, output-root absence, and synthetic-only conformance tests.

It may not read the ZE0 manifest scientific payload, read the full ZE1 scientific inventory payload, perform candidate/source comparison, perform overlap, or write ZE2 outputs.

`ZE2_CONSUMING_PERMISSIONS_BLOCKED_UNTIL_PREEXECUTION_RECONCILIATION_PASS=YES`

## One-shot consumption boundary

The D0337 authorization is consumed atomically at the first of:

1. first ZE0 manifest scientific-payload read;
2. first ZE1 inventory scientific-payload read;
3. first ZE2 output write.

`CONSUMPTION_EVENT=FIRST_ZE0_MANIFEST_SCIENTIFIC_PAYLOAD_READ_OR_FIRST_ZE1_INVENTORY_SCIENTIFIC_PAYLOAD_READ_OR_FIRST_ZE2_OUTPUT_WRITE_WHICHEVER_OCCURS_FIRST`

Governance metadata reads, Git-tree name reads, Git blob-OID reads, ZE1 LFS-pointer-only reads, and synthetic-only tests are non-consuming.

After consumption the remaining attempt capacity is zero. No automatic retry is authorized.

A failed, interrupted, or partial consumed attempt may not be rerun under D0337.

An abort before the consumption boundary leaves the authorization unconsumed, but the abort must be reported before another attempt.

## Exact execution scope

The future authorized attempt may read only the frozen ZE0 candidate-representation manifest and frozen ZE1 source-representation inventory required by D0336.

It may not read raw D0318 candidate records or the substantive frozen source files.

It may not expand the source universe or alter ZE0/ZE1 representation rules.

Only the deterministic exact-equality comparisons frozen by D0336 are authorized.

Fuzzy matching, semantic matching, manual alias creation, and mapping remain prohibited.

## Reserved output

- root: `evidence/representation_alignment/ZE2/deterministic_candidate_source_overlap_v1`
- overlap manifest: `evidence/representation_alignment/ZE2/deterministic_candidate_source_overlap_v1/candidate_source_representation_overlap.json`
- execution state: `evidence/representation_alignment/ZE2/deterministic_candidate_source_overlap_v1/_execution_state.json`

The output root must be absent before attempt start.

Partial output from a consumed failed attempt may not be silently deleted, overwritten, or retried.

Successful completion requires a separate ZE2 result checkpoint.

## Scientific interpretation boundary

ZE2 overlap is not semantic evidence.

ZE2 overlap is not protocol support.

ZE2 non-overlap is not semantic non-support.

ZE2 overlap is not mapping.

`C4_STATUS=UNRESOLVED`

`P8_MAPPING_AUTHORIZED=NO`

## Downstream firewall

`ZE3_EXECUTION_AUTHORIZED=NO`

`ZE4_EXECUTION_AUTHORIZED=NO`

`E2_AUTHORIZED=NO`

`E3_AUTHORIZED=NO`

`E4_AUTHORIZED=NO`

`P10_GOLD_ANNOTATION_AUTHORIZED=NO`

`P11_ANALYZER_IMPLEMENTATION_AUTHORIZED=NO`

`P11_ANALYZER_EXECUTION_AUTHORIZED=NO`

`BASELINE_EXECUTION_AUTHORIZED=NO`

`REPAIR_EXECUTION_AUTHORIZED=NO`

## D0337 authoring noninterference

`ZE0_MANIFEST_PAYLOAD_READ_PERFORMED=NO`

`ZE1_INVENTORY_PAYLOAD_READ_PERFORMED=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED=NO`

`REPRESENTATION_OVERLAP_PERFORMED=NO`

`ZE2_EXECUTION_PERFORMED=NO`

`P8_MAPPING_PERFORMED=NO`


## Corrective revision after independent pre-commit review

The first independent D0337 pre-commit review returned `REVISION_REQUIRED` with `PASS_CHECK_COUNT=109` and exactly five findings.

Reviewed author-candidate identities:

- decision SHA-256: `a53a7261bd1073a347dedfd8d0551c25b65416b3299267d32353d5f1f764755f`
- machine artifact SHA-256: `4fe424d2b2d42a528e48ae8ae0107574b21b8ec3f3f014a0cd169ab1446fffe3`

No scientific payload was read and no ZE2 execution occurred while correcting the five findings.

### D0337-PR-001 — explicit preexecution reconciliation authorization

After D0337 becomes fully effective, D0337 authorizes exactly one non-consuming post-publication preexecution reconciliation:

`SVF-D0337-ZE2-POSTPUBLICATION-PREEXECUTION-RECONCILIATION-V1`

Its authorization scope is exactly:

`ONE_NONCONSUMING_POSTPUBLICATION_PREEXECUTION_RECONCILIATION`

This reconciliation adds zero ZE2 execution-attempt capacity and does not consume the one ZE2 execution authorization.

### D0337-PR-002 — closed required-check set

The reconciliation must execute exactly these eight required checks:

1. `D0337_REMOTE_COMMIT_IDENTITY_EXACT`
2. `D0336_EFFECTIVE_BINDING_EXACT`
3. `ZE0_GIT_PATH_AND_BLOB_IDENTITY_EXACT`
4. `ZE1_GIT_PATH_AND_LFS_POINTER_IDENTITY_EXACT`
5. `ZE2_RESERVED_OUTPUT_ROOT_ABSENT`
6. `CANDIDATE_VALUE_SERIALIZER_SYNTHETIC_CONFORMANCE_PASS`
7. `EXACT_MATCHER_SYNTHETIC_CONFORMANCE_PASS`
8. `NO_SCIENTIFIC_PAYLOAD_READ_DURING_RECONCILIATION`

All eight must PASS. The required-check set is closed; runtime substitution or omission is prohibited.

### D0337-PR-003 — frozen synthetic-only conformance vectors

The machine contract freezes:

- eleven candidate-representation serializer vectors covering string, ordered sequence, nested ordered sequence, empty values, and non-ASCII UTF-8;
- twelve exact-matcher vectors covering positive and negative string, sequence, nested-sequence, ordering, length, case, substring, and empty-value cases.

The synthetic-conformance contract is:

`SVF-D0337-ZE2-PREEXECUTION-SYNTHETIC-CONFORMANCE-V1`

All vectors must PASS.

The vectors contain no frozen candidate or source scientific content.

### D0337-PR-004 — consumed execution input-verification order

After the non-consuming reconciliation PASS, the future consuming attempt must execute the frozen input-identity sequence before any overlap comparison.

The ordered sequence is:

1. read the complete ZE0 scientific manifest payload;
2. verify the exact ZE0 full-file SHA-256;
3. verify the exact ZE0 candidate canonical SHA-256;
4. read the complete ZE1 scientific inventory payload;
5. verify the exact ZE1 full-file SHA-256;
6. verify the exact ZE1 canonical JSON SHA-256;
7. only after all prior checks PASS may D0336 candidate/source comparison begin.

The first scientific payload read consumes D0337 according to the already frozen one-shot boundary.

If any payload identity check fails after consumption, the consumed attempt aborts and remaining capacity is zero.

`IDENTITY_MISMATCH_ALLOWS_RETRY=NO`

No candidate/source comparison or representation overlap may occur before all frozen input identity checks PASS.

### D0337-PR-005 — remote readback before capacity activation

Publication alone does not activate the one-attempt capacity.

After publication but before exact remote readback:

`ZE2_EXECUTION_ATTEMPT_CAPACITY=0`

Only after exact remote readback confirms the published D0337 commit does the one attempt become conditionally available:

`ZE2_EXECUTION_ATTEMPT_CAPACITY=1_CONDITIONALLY_AVAILABLE`

Even then, consuming permissions remain blocked until the separately authorized non-consuming preexecution reconciliation PASS.

### Corrective-authoring noninterference

`D0337_PR_001_RESOLVED=YES`

`D0337_PR_002_RESOLVED=YES`

`D0337_PR_003_RESOLVED=YES`

`D0337_PR_004_RESOLVED=YES`

`D0337_PR_005_RESOLVED=YES`

`ZE0_MANIFEST_PAYLOAD_READ_PERFORMED_DURING_CORRECTION=NO`

`ZE1_INVENTORY_PAYLOAD_READ_PERFORMED_DURING_CORRECTION=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED_DURING_CORRECTION=NO`

`REPRESENTATION_OVERLAP_PERFORMED_DURING_CORRECTION=NO`

`ZE2_EXECUTION_PERFORMED_DURING_CORRECTION=NO`

`P8_MAPPING_PERFORMED_DURING_CORRECTION=NO`


## Second corrective revision after fresh independent pre-commit review

The fresh independent review of the corrected D0337 author candidate returned `REVISION_REQUIRED` with `PASS_CHECK_COUNT=192` and exactly one finding: `D0337-PR-006`.

Reviewed corrected byte identities:

- decision SHA-256: `27dad3b71785f189b44df7d2d4150b8475ad09a0c1ed403b36600473da1236b1`
- machine artifact SHA-256: `bdea17599d0636f0e0e4cdc6f4053f0593100487d181c403593113f72ab022e1`

No ZE0 or ZE1 scientific payload was read and no ZE2 execution occurred while correcting this finding.

### D0337-PR-006 — one-shot lifecycle of the reconciliation authorization

The separately authorized post-publication preexecution reconciliation has its own one-shot authorization lifecycle, distinct from the ZE2 execution authorization.

The reconciliation-attempt start event is:

`FIRST_EXECUTION_OF_ANY_REQUIRED_RECONCILIATION_CHECK_OR_FIRST_SYNTHETIC_CONFORMANCE_VECTOR_WHICHEVER_OCCURS_FIRST`

At that event, the reconciliation authorization is consumed atomically.

`RECONCILIATION_AUTHORIZATION_CONSUMED_AT_ATTEMPT_START=YES`

After reconciliation-attempt start:

`REMAINING_RECONCILIATION_ATTEMPT_CAPACITY=0`

No automatic reconciliation retry is authorized after consumption.

`AUTOMATIC_RETRY_AFTER_RECONCILIATION_AUTHORIZATION_CONSUMPTION_AUTHORIZED=NO`

A failed or interrupted reconciliation attempt may not be retried under the same reconciliation authorization.

`FAILED_OR_INTERRUPTED_RECONCILIATION_ATTEMPT_MAY_RETRY=NO`

Starting, passing, failing, or interrupting the reconciliation does not consume the separate ZE2 execution authorization.

`RECONCILIATION_ATTEMPT_START_CONSUMES_ZE2_EXECUTION_AUTHORIZATION=NO`

`RECONCILIATION_PASS_CONSUMES_ZE2_EXECUTION_AUTHORIZATION=NO`

`RECONCILIATION_FAIL_CONSUMES_ZE2_EXECUTION_AUTHORIZATION=NO`

`RECONCILIATION_INTERRUPTION_CONSUMES_ZE2_EXECUTION_AUTHORIZATION=NO`

A failed or interrupted reconciliation continues to block ZE2 consuming permissions.

### Second corrective-authoring noninterference

`D0337_PR_006_RESOLVED=YES`

`ZE0_MANIFEST_PAYLOAD_READ_PERFORMED_DURING_SECOND_CORRECTION=NO`

`ZE1_INVENTORY_PAYLOAD_READ_PERFORMED_DURING_SECOND_CORRECTION=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED_DURING_SECOND_CORRECTION=NO`

`REPRESENTATION_OVERLAP_PERFORMED_DURING_SECOND_CORRECTION=NO`

`ZE2_EXECUTION_PERFORMED_DURING_SECOND_CORRECTION=NO`

`P8_MAPPING_PERFORMED_DURING_SECOND_CORRECTION=NO`

## Activation lifecycle

Authoring alone is not effective.

A local commit alone is not effective.

Required sequence:

1. independent pre-commit verification;
2. exact local D0337 two-file commit;
3. independent post-commit verification;
4. publication of that exact reviewed commit;
5. exact remote readback;
6. separate non-consuming post-publication preexecution reconciliation PASS;
7. only then may the single ZE2 attempt consume D0337.

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0337_SINGLE_ZE2_EXECUTION_AUTHORIZATION_AUTHOR_CANDIDATE`
