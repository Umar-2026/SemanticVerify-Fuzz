# Decision 0338 — Record Failed D0337 Preexecution Reconciliation and Authorize a Transport-Safe Successor

## Status

`AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_POSTCOMMIT_VERIFIED_PUBLISHED_AND_REMOTELY_CONFIRMED`

D0338 is a corrective governance-successor author candidate only.

It does not retry the consumed D0337 reconciliation, does not execute ZE2, does
not consume the existing D0337 ZE2 execution authorization, and grants no new
ZE2 execution-attempt capacity.

## Governing frozen ZE2 contract

Effective D0336 contract:

- commit: `40561ff59630f82e9fa7427632c87894ca95e08d`
- contract ID: `SVF-ZE2-DETERMINISTIC-STRUCTURAL-REPRESENTATION-OVERLAP-V1`
- decision SHA-256: `a5f94caaf7035f2179902a258eafbe9e3beac9b6b5a2724d91448af09ff10cf1`
- machine artifact SHA-256: `8381b86f29e0e1a04b1c8728e4ff47f31569c20b5906f8bcdd494cebcb42f37b`

D0338 does not modify D0336 representation compatibility, matching semantics,
serialization, output schema, scientific interpretation boundary, or reserved
ZE2 execution ID.

## Effective D0337 authorization binding

Effective D0337:

- commit: `0d9bf0db43e94a09375439a287985dc34eaed715`
- authorization ID: `SVF-D0337-ZE2-SINGLE-EXECUTION-AUTH-V1`
- reserved execution ID: `SVF-ZE2-DETERMINISTIC-REPRESENTATION-OVERLAP-RUN-001`
- decision SHA-256: `a1f49d2e2d87098d91a96e645937d71f23c335e3dd4cc1be5381ccc91913216f`
- machine artifact SHA-256: `78cd6c174fe872167d1269d7a73737b62bd477bcb25b3d30b4dbf06abd67621b`

The D0337 ZE2 execution authorization remains unconsumed.

`D0337_ZE2_EXECUTION_AUTHORIZATION_CONSUMED=NO`

`TOTAL_ZE2_EXECUTION_ATTEMPT_CAPACITY=1`

`CONSUMED_ZE2_EXECUTION_ATTEMPTS=0`

`REMAINING_ZE2_EXECUTION_ATTEMPT_CAPACITY=1`

D0338 grants:

`NEW_ZE2_EXECUTION_ATTEMPT_CAPACITY=0`

The same original single D0337 ZE2 attempt is preserved.

## Recorded failed D0337 reconciliation

D0337 separately authorized exactly one non-consuming post-publication
preexecution reconciliation:

`SVF-D0337-ZE2-POSTPUBLICATION-PREEXECUTION-RECONCILIATION-V1`

That reconciliation attempt started and therefore consumed its own independent
reconciliation authorization.

The failure occurred on the first required check:

`D0337_REMOTE_COMMIT_IDENTITY_EXACT`

The Git HTTPS remote read returned code `128` with an HTTP/2 framing-layer
transport error.

This is recorded as:

`FAILURE_CLASS=NONSCIENTIFIC_REMOTE_HTTPS_TRANSPORT_FAILURE`

The failure occurred before:

- any ZE0 scientific-manifest payload read;
- any full ZE1 scientific-inventory payload read;
- any candidate/source comparison;
- any representation-overlap comparison;
- any ZE2 output write.

Therefore:

`D0337_RECONCILIATION_AUTHORIZATION_CONSUMED=YES`

`D0337_RECONCILIATION_REMAINING_ATTEMPT_CAPACITY=0`

`D0337_RECONCILIATION_RETRY_UNDER_SAME_AUTHORIZATION=NO`

but:

`D0337_ZE2_EXECUTION_AUTHORIZATION_CONSUMED=NO`

`ZE2_EXECUTION_PERFORMED=NO`

`ZE2_OUTPUT_WRITE_PERFORMED=NO`

The D0337 reconciliation is permanently retired. D0338 does not reopen or
reinterpret it.

## Corrective-successor authorization identity

D0338 successor authorization ID:

`SVF-D0338-ZE2-PREEXECUTION-RECONCILIATION-TRANSPORT-SAFE-SUCCESSOR-AUTH-V1`

Authorized successor reconciliation ID:

`SVF-D0338-ZE2-POSTPUBLICATION-PREEXECUTION-RECONCILIATION-SUCCESSOR-V1`

Exact scope:

`ONE_TRANSPORT_SAFE_NONCONSUMING_PREEXECUTION_RECONCILIATION_SUCCESSOR`

D0338 authorizes at most one successor reconciliation attempt, and only after
D0338 completes its full activation lifecycle.

This successor adds zero ZE2 execution-attempt capacity and does not consume the
existing D0337 ZE2 execution authorization.

## Corrective transport-lifecycle change

The scientific and governance identity semantics of the retired D0337 remote
identity requirement are preserved, but its volatile live-network operation is
moved outside the successor reconciliation attempt-start boundary.

Before the successor reconciliation attempt may start, an exact transport
preflight must PASS.

The preflight is limited to:

- an authenticated read of `origin/main`;
- a per-command `HTTP/1.1` Git HTTP-version override;
- no persistent Git configuration mutation;
- no credential-helper or credential-storage configuration;
- exact confirmation that live remote `main` equals the **effective published
  D0338 commit identity already established by the completed D0338 activation
  lifecycle**.

The D0338 commit hash is intentionally not guessed or frozen during authoring.
It is resolved only after independent pre-commit review, exact commit,
independent post-commit review, publication, and exact remote readback have
established the effective D0338 commit identity.

At successor-preflight time:

`REMOTE_MAIN_MUST_EQUAL_EFFECTIVE_PUBLISHED_D0338_COMMIT=YES`

and:

`LOCAL_HEAD_MUST_EQUAL_EFFECTIVE_D0338_COMMIT=YES`

`LOCAL_HEAD_PARENT_MUST_EQUAL_D0337_COMMIT=YES`

The historical D0337 commit
`0d9bf0db43e94a09375439a287985dc34eaed715` remains the parent and historical
authorization binding only. It is **not** the required post-activation remote
`main` target.

The transport preflight is non-consuming.

`TRANSPORT_PREFLIGHT_CONSUMES_SUCCESSOR_RECONCILIATION_AUTHORIZATION=NO`

`TRANSPORT_PREFLIGHT_CONSUMES_ZE2_EXECUTION_AUTHORIZATION=NO`

If the transport preflight fails:

- the successor reconciliation attempt has not started;
- no successor reconciliation capacity is consumed;
- no automatic same-transaction preflight retry is authorized;
- the failure must be reported;
- any later preflight requires a separate read-only recovery reconciliation;
- the still-unconsumed successor authorization may then be used if governance
  state remains exact.

This correction addresses only the transport lifecycle. It does not weaken,
remove, or substitute any scientific or deterministic conformance requirement.

## Closed successor required-check set

Only after the transport preflight PASS may the successor reconciliation
attempt start.

The closed required-check set after preflight is exactly:

1. `D0336_EFFECTIVE_BINDING_EXACT`
2. `ZE0_GIT_PATH_AND_BLOB_IDENTITY_EXACT`
3. `ZE1_GIT_PATH_AND_LFS_POINTER_IDENTITY_EXACT`
4. `ZE2_RESERVED_OUTPUT_ROOT_ABSENT`
5. `CANDIDATE_VALUE_SERIALIZER_SYNTHETIC_CONFORMANCE_PASS`
6. `EXACT_MATCHER_SYNTHETIC_CONFORMANCE_PASS`
7. `NO_SCIENTIFIC_PAYLOAD_READ_DURING_RECONCILIATION`

The retired D0337 check `D0337_REMOTE_COMMIT_IDENTITY_EXACT` is not discarded;
its exact identity requirement is satisfied by the mandatory successful
non-consuming transport preflight immediately before successor attempt start.

All seven closed checks must PASS.

Runtime substitution, omission, semantic expansion, or weakening is prohibited.

## Frozen synthetic-conformance binding

D0338 reuses byte-for-byte the already published D0337 synthetic-only
conformance contract:

`SVF-D0337-ZE2-PREEXECUTION-SYNTHETIC-CONFORMANCE-V1`

Bound source machine artifact SHA-256:

`78cd6c174fe872167d1269d7a73737b62bd477bcb25b3d30b4dbf06abd67621b`

The frozen set remains:

- eleven candidate-value serializer vectors;
- twelve exact-matcher vectors.

D0338 authors no new synthetic vectors.

No scientific payload is needed by those vectors.

## Successor reconciliation one-shot lifecycle

The successor reconciliation attempt-start event is:

`FIRST_EXECUTION_OF_ANY_CLOSED_REQUIRED_CHECK_AFTER_SUCCESSFUL_TRANSPORT_PREFLIGHT_OR_FIRST_SYNTHETIC_CONFORMANCE_VECTOR_WHICHEVER_OCCURS_FIRST`

At that event the D0338 successor reconciliation authorization is consumed
atomically.

`SUCCESSOR_RECONCILIATION_AUTHORIZATION_CONSUMED_AT_ATTEMPT_START=YES`

After attempt start:

`REMAINING_SUCCESSOR_RECONCILIATION_ATTEMPT_CAPACITY=0`

No automatic reconciliation retry is authorized.

A failed or interrupted successor reconciliation may not be retried under
D0338.

Starting, passing, failing, or interrupting the successor reconciliation does
not consume the separate original D0337 ZE2 execution authorization.

A failed or interrupted successor reconciliation continues to block ZE2
consuming permissions.

## Permitted successor reconciliation operations

The successor reconciliation may only:

- verify the exact effective D0336 binding;
- verify the frozen ZE0 Git path and blob identity without reading scientific
  payload;
- verify the frozen ZE1 Git path and LFS pointer without reading the full
  scientific inventory;
- verify the reserved ZE2 output root is absent;
- execute the frozen D0337 synthetic serializer vectors;
- execute the frozen D0337 exact-matcher vectors;
- verify that no scientific payload was read during reconciliation.

It may not:

- read the ZE0 manifest scientific payload;
- read the full ZE1 scientific inventory payload;
- compare candidate/source representations;
- perform representation overlap;
- write ZE2 output;
- perform fuzzy or semantic matching;
- perform P8 mapping.

## Activation lifecycle

D0338 authoring is not effective.

A local D0338 commit alone is not effective.

The D0338 successor reconciliation authorization becomes effective only after:

1. independent pre-commit review PASS;
2. exact commit of the D0338 decision and D0338 machine artifact only;
3. independent post-commit review PASS;
4. publication of that exact reviewed commit;
5. exact remote readback of the published D0338 commit.

Before all five conditions complete:

`D0338_SUCCESSOR_RECONCILIATION_AUTHORIZED=NO`

After all five conditions complete:

`D0338_SUCCESSOR_RECONCILIATION_AUTHORIZED=YES_MAXIMUM_ONE_ATTEMPT`

Even then:

`ZE2_CONSUMING_PERMISSIONS_EXERCISABLE=NO`

until the successor reconciliation itself PASSes.

## Scientific interpretation boundary

D0338 is governance only.

It does not establish:

- semantic evidence;
- protocol support;
- semantic non-support;
- representation mapping;
- C4.

`C4_STATUS=UNRESOLVED`

`P8_MAPPING_AUTHORIZED=NO`

## Downstream firewall

D0338 authoring does not authorize:

- ZE2 execution;
- ZE3 or ZE4 execution;
- P8 mapping;
- P10 gold annotation;
- P11 analyzer implementation;
- P11 analyzer execution;
- baseline execution;
- repair.

## Corrective revision after independent pre-commit review

The first independent pre-commit review of the D0338 author candidate returned:

`REVISION_REQUIRED`

with:

`PASS_CHECK_COUNT=108`

`FAIL_CHECK_COUNT=2`

`REVIEW_FINDING_COUNT=2`

The two blocking findings were:

- `D0338-PR-001`: the machine artifact froze the D0337 parent as the expected
  remote `main` target even though the successor reconciliation can run only
  after D0338 itself is published and remotely confirmed;
- `D0338-PR-002`: the human decision repeated the same impossible
  post-activation target.

Both findings are corrected in this revision.

The post-activation transport preflight now resolves the required remote
identity as the exact **effective published D0338 commit** established by the
completed D0338 activation lifecycle.

No future D0338 commit hash is invented during authoring.

This correction changes only the transport-lifecycle binding. It does not
change:

- D0336 representation-overlap semantics;
- the frozen D0337 ZE2 execution authorization;
- the reserved ZE2 execution ID;
- ZE2 total or remaining execution-attempt capacity;
- the seven successor reconciliation checks;
- frozen synthetic vectors;
- scientific interpretation boundaries;
- downstream non-authorizations.

`D0338_PR_001_RESOLVED=YES`

`D0338_PR_002_RESOLVED=YES`

`NEW_ZE2_EXECUTION_ATTEMPT_CAPACITY_GRANTED_BY_CORRECTION=0`

`D0337_RECONCILIATION_RETRY_PERFORMED_DURING_CORRECTION=NO`

`REMOTE_ACCESS_PERFORMED_DURING_CORRECTION=NO`

`ZE0_SCIENTIFIC_PAYLOAD_READ_PERFORMED_DURING_CORRECTION=NO`

`ZE1_SCIENTIFIC_PAYLOAD_READ_PERFORMED_DURING_CORRECTION=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED_DURING_CORRECTION=NO`

`REPRESENTATION_OVERLAP_PERFORMED_DURING_CORRECTION=NO`

`ZE2_EXECUTION_PERFORMED_DURING_CORRECTION=NO`

`P8_MAPPING_PERFORMED_DURING_CORRECTION=NO`

## Authoring noninterference

During this D0338 authoring transaction:

`REMOTE_ACCESS_PERFORMED=NO`

`D0337_RECONCILIATION_RETRY_PERFORMED=NO`

`ZE0_SCIENTIFIC_PAYLOAD_READ_PERFORMED=NO`

`ZE1_SCIENTIFIC_PAYLOAD_READ_PERFORMED=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED=NO`

`REPRESENTATION_OVERLAP_PERFORMED=NO`

`ZE2_OUTPUT_WRITE_PERFORMED=NO`

`ZE2_EXECUTION_PERFORMED=NO`

`P8_MAPPING_PERFORMED=NO`

`GIT_ADD_PERFORMED=NO`

`COMMIT_PERFORMED=NO`

`PUSH_PERFORMED=NO`

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0338_CORRECTIVE_SUCCESSOR_AUTHOR_CANDIDATE`
