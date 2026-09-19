# D0304 — Authorize one bounded E0-freeze execution without E1 extraction

## Status

`AUTHOR_CANDIDATE_EXECUTION_AUTHORIZATION_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0304 is an execution-authorization candidate only. At authoring time it is not effective and does not itself execute E0.

## Source checkpoint

- Published and effective D0303 commit: `551d68bba5cca8f50d5753dd229795da484fb277`
- D0304 machine authorization artifact: `evaluation/governance_reconciliation/d0304_single_bounded_e0_freeze_execution_authorization.json`
- D0304 artifact SHA-256: `b30eb49890ea53f49a3207cd67528fff57ba2bf63a3ba21fd2dedcdbdaff2be9`

## Authorized operation after D0304 becomes effective

D0304 may authorize exactly **one successful bounded E0-freeze execution transaction**.

The execution is reserved as:

`SVF-D0305-E0-FREEZE-EXECUTION-V1`

with output root:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0305_e0_freeze_execution_v1`

and exactly four required outputs:

1. `01_frozen_candidate_universe_manifest.v1.json`
2. `02_frozen_evidence_source_universe_manifest.v1.json`
3. `03_frozen_relation_target_and_protocol_manifest.v1.json`
4. `04_e0_freeze_execution_report.v1.json`

The successful authorization is consumed only after all four outputs are validated and atomically materialized.

A failed or partial execution must not consume the successful-execution allowance and must not leave a published D0305 output root.

## E0 execution boundary

The future D0305 transaction may mechanically:

- bind the exact 171 D0301 candidate identifiers;
- bind the exact 9 D0243 inventory members;
- preserve the 4 substantive / 5 governance-support classification;
- verify existing source SHA-256 and Git blob identities;
- bind the D0303 C4 relation target;
- bind the future E1 extraction protocol;
- bind the evidence-unit locator/hash scheme;
- bind the future independent E2 adjudication protocol;
- materialize the four E0-freeze outputs.

Existing source bytes may be accessed only for mechanical identity verification.

## Explicit prohibition on E1 activity

D0304 does **not** authorize future D0305 to:

- search substantive source content for candidate identifiers;
- perform exact-identifier occurrence discovery;
- extract Markdown paragraphs;
- extract JSON objects or array elements;
- create 684 candidate-source pair results;
- create zero-occurrence E1 records;
- materialize evidence units;
- perform cross-source joins;
- perform semantic or fuzzy matching.

Therefore the future E1 domain of 684 candidate-source pairs remains a frozen design fact only, not an executable workload under D0304.

## Explicit prohibition on E2 and later stages

D0304 does not authorize:

- evidence-unit adjudication;
- support / non-support / ambiguity judgments;
- candidate-level closure aggregation;
- carrier-admissibility dispositions;
- E3 accounting;
- E4 readiness reassessment;
- C4 authorization;
- B2 authorization;
- V4→V2 mapping;
- curl.json creation;
- gold annotation;
- analyzer implementation/execution;
- baseline execution;
- repair.

## One-shot rule

`MAXIMUM_SUCCESSFUL_E0_EXECUTION_TRANSACTIONS=1`

Before publication of D0304:

`E0_EXECUTION_AUTHORIZED_NOW=NO`

After independent verification, exact commit, post-commit verification, and exact publication, the authorization may become effective for one successful D0305 transaction only.

After a successful D0305 transaction:

`D0304_REMAINING_SUCCESSFUL_E0_EXECUTION_TRANSACTIONS=0`

D0305 must never be reexecuted under this authorization after success.

## Fail-closed execution rule

Any mismatch in:

- D0303 identity;
- candidate universe;
- D0243 inventory membership;
- source class;
- source SHA-256;
- Git blob OID;
- relation-target contract;
- protocol contract;
- required output set;
- output validation

must abort the future E0 execution before publication of the D0305 output root.

## Current state at D0304 authoring

`D0304_AUTHORIZATION_EFFECTIVE=NO`

`D0304_SUCCESSFUL_EXECUTION_TRANSACTION_COUNT=0`

`D0304_MAXIMUM_SUCCESSFUL_EXECUTION_TRANSACTION_COUNT=1`

`D0304_REMAINING_SUCCESSFUL_EXECUTION_TRANSACTIONS=1`

`E0_EXECUTED=NO`

`E1_EXTRACTION_AUTHORIZED=NO`

`E1_EXTRACTION_EXECUTED=NO`

`E2_ADJUDICATION_AUTHORIZED=NO`

`E2_ADJUDICATION_EXECUTED=NO`

`E3_ACCOUNTING_AUTHORIZED=NO`

`E4_READINESS_REASSESSMENT_AUTHORIZED=NO`

`NEW_EVIDENCE_ACQUISITION_AUTHORIZED=NO`

`NETWORK_EVIDENCE_ACQUISITION_AUTHORIZED=NO`

`SUBSTANTIVE_EVIDENCE_CONTENT_SEARCH_AUTHORIZED=NO`

`SUBSTANTIVE_EVIDENCE_EXTRACTION_AUTHORIZED=NO`

`SEMANTIC_ADJUDICATION_AUTHORIZED=NO`

`C4_ZERO_UNRESOLVED_CLOSURE_ESTABLISHED=NO`

`C4_ENTRY_READINESS_ESTABLISHED=NO`

`C4_AUTHORIZED=NO`

`C4_EXECUTED=NO`

`B2_READINESS_ESTABLISHED=NO`

`B2_AUTHORIZED=NO`

`B2_EXECUTED=NO`

`POSITIVE_V4_TO_V2_MAPPING_AUTHORIZED=NO`

`CURL_JSON_MATERIALIZATION_AUTHORIZED=NO`

`P10_GOLD_ANNOTATION_AUTHORIZED=NO`

`P11_ANALYZER_IMPLEMENTATION_AUTHORIZED=NO`

`P11_ANALYZER_EXECUTION_AUTHORIZED=NO`

`BASELINE_EXECUTION_AUTHORIZED=NO`

`REPAIR_EXECUTION_AUTHORIZED=NO`

## Protected boundaries

D0304 does not authorize D0251 snapshot-content reads, D0276 retained-evidence-content reads, historical one-time verifier execution, D0301 reexecution, new/network evidence acquisition, substantive evidence searching or extraction, candidate-identifier occurrence searches, semantic adjudication, result reselection, candidate subsetting, Class06 reclassification, positional reassignment, pair reclassification, Req06/Req14 determination, carrier-admissibility disposition, concrete mapping, or schema V4→V2 mapping.

## Next checkpoint

`INDEPENDENT_READ_ONLY_VERIFY_D0304_EXECUTION_AUTHORIZATION_AUTHOR_CANDIDATE_BEFORE_COMMIT_OR_PUSH`

No E0 execution, commit, push, E1 extraction, or E2 adjudication occurs in this authoring transaction.
