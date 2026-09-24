# D0328 — Authorize One Non-Consuming ZE1 Preauthorization-Integrity Verification

## Status

`AUTHORIZATION_AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0328 is an authorization checkpoint only.

D0328 does not execute the integrity verification.

D0328 does not authorize or execute ZE1.

D0328 does not authorize substantive source-content reads.

## Governing checkpoint

D0327 is published and effective at:

`47c9135987178ce51179949d7b333b5bd2aa7492`

D0327 froze the candidate-blind ZE1 source-representation inventory contract.

Its source universe remains exactly:

`C1-S01`

`C1-S02`

`C1-S03`

`C1-S04`

The frozen source-manifest canonical SHA-256 remains:

`b6c97642ee0a3bc8de5839209a0a8546feb61beedc198c24a8c43c44b6534b52`

## Authorization

Authorization ID:

`SVF-D0328-ZE1-PREAUTH-INTEGRITY-ONE-SHOT-AUTH-V1`

Reserved integrity execution ID:

`SVF-ZE1-PREAUTH-INTEGRITY-RUN-001`

After D0328 becomes independently verified, committed, post-commit verified, and published, it authorizes at most one bounded ZE1 preauthorization-integrity verification attempt under the exact D0327 contract.

This integrity transaction is non-consuming with respect to any future ZE1 execution capacity.

It does not start ZE1.

## Authorized integrity scope

The future integrity transaction may verify only the following classes of facts:

1. exact local and remote D0327 publication identity;
2. exact D0327 decision and machine-artifact byte identities;
3. exact frozen source-manifest identity, source IDs, source order, paths, formats, and recorded SHA-256 metadata;
4. exact Git blob OIDs using Git tree metadata only;
5. absence of the reserved ZE1 output root;
6. conformance of an implementation of the exact D0327 grammar against the five D0327-frozen synthetic-only vectors;
7. runtime Unicode database version used for the synthetic-only grammar implementation.

No governed source bytes or governed candidate values are needed for those checks.

## Non-consuming preflight

Before the authorized integrity attempt starts, a future transaction may perform bounded non-consuming preflight checks for:

- clean repository state;
- exact published D0327 local identity;
- exact published D0327 remote identity;
- exact D0327 byte identities;
- absence of the ZE1 output root;
- absence of the reserved integrity-result path.

Those checks do not consume future ZE1 execution capacity and do not start ZE1.

## D0328 authorization-consumption boundary

D0328 itself authorizes one integrity attempt.

The integrity attempt starts, and D0328's one-shot integrity authorization is consumed, at the first of:

`FIRST_SYNTHETIC_CONFORMANCE_VECTOR_EVALUATION`

or

`FIRST_INTEGRITY_RESULT_ARTIFACT_WRITE`

No automatic retry is authorized after that boundary.

A failed or incomplete started integrity attempt requires separate successor governance.

## Synthetic-only conformance

The future integrity transaction may execute exactly the five synthetic vectors already frozen by D0327:

`ZE1-TV01`

`ZE1-TV02`

`ZE1-TV03`

`ZE1-TV04`

`ZE1-TV05`

These vectors contain no governed substantive source content and no governed candidate content.

Their execution is an implementation-conformance check only.

It is not a source inventory.

It is not candidate/source matching.

It is not ZE1 execution.

## Strict prohibitions

During the authorized integrity verification, the transaction may not:

- open or read any substantive bytes of `C1-S01` through `C1-S04`;
- use `git show` or an equivalent operation to extract substantive frozen source-file contents;
- read the ZE0 candidate-representation manifest;
- traverse D0318 candidate records;
- read a governed Schema V2 candidate property-path value;
- read a governed candidate representation value;
- construct candidate-specific source queries;
- construct a source-representation inventory;
- compare candidate and source representations;
- perform representation-overlap matching;
- perform fuzzy, semantic, embedding, or LLM-based matching;
- perform semantic adjudication;
- execute E2, E3, or E4;
- determine C4;
- perform positive V4-to-V2 mapping;
- materialize `curl.json`;
- start P10 gold annotation;
- implement or execute P11;
- execute a baseline;
- execute repair.

## Authorized write boundary

The future integrity transaction may write exactly one integrity-result artifact at:

`evaluation/governance_reconciliation/ze1_preauthorization_integrity_v1/d0328_preauthorization_integrity_execution_result.json`

It may not write any other repository file.

It may not create or write:

`evidence/representation_alignment/ZE1/source_representation_inventory_v1`

The future result must record the integrity execution identity, authorization identity, attempt/consumption state, PASS/FAIL accounting, findings, immutable D0327 anchors, source identity checks, output-root absence, five synthetic-vector results, runtime Unicode database version, and all negative side-effect boundaries.

## Integrity success criterion

A successful integrity result requires all authorized check groups to pass.

It requires:

`FAIL_CHECK_COUNT=0`

and no findings.

All five synthetic vectors must pass.

The ZE1 output root must remain absent.

The result must record:

`SUBSTANTIVE_SOURCE_CONTENT_READ=NO`

`ZE0_MANIFEST_READ=NO`

`CANDIDATE_VALUE_READ=NO`

`MATCHING_PERFORMED=NO`

`ZE1_EXECUTION_PERFORMED=NO`

## Result publication requirement

Even a passing integrity result does not authorize ZE1.

A passing result must first be recorded, independently verified, committed, post-commit verified, and published by a separate successor checkpoint.

The expected successor is:

`D0329_RECORD_ZE1_PREAUTH_INTEGRITY_RESULT_WITHOUT_ZE1_START`

Only after that separate result checkpoint may a further successor consider ZE1 execution authorization.

## Current authorization state

`PREAUTH_INTEGRITY_EXECUTION_AUTHORIZED_BY_EFFECTIVE_D0328=NO`

The above remains `NO` until D0328 itself is independently verified, committed, post-commit verified, and published.

`ZE1_EXECUTION_AUTHORIZED=NO`

`SUBSTANTIVE_SOURCE_CONTENT_READ_AUTHORIZED=NO`

`SOURCE_REPRESENTATION_INVENTORY_AUTHORIZED=NO`

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

`P8_MAPPING_AUTHORIZED=NO`

`P10_GOLD_ANNOTATION_AUTHORIZED=NO`

`P11_ANALYZER_IMPLEMENTATION_AUTHORIZED=NO`

`P11_ANALYZER_EXECUTION_AUTHORIZED=NO`

`BASELINE_EXECUTION_AUTHORIZED=NO`

`REPAIR_EXECUTION_AUTHORIZED=NO`

## D0328 authoring transaction

During D0328 authoring:

`INTEGRITY_EXECUTION_PERFORMED=NO`

`SYNTHETIC_VECTOR_EXECUTION_PERFORMED=NO`

`INTEGRITY_RESULT_WRITTEN=NO`

`SUBSTANTIVE_SOURCE_CONTENT_READ_PERFORMED=NO`

`ZE0_MANIFEST_READ_PERFORMED=NO`

`CANDIDATE_LIST_TRAVERSED=NO`

`CANDIDATE_VALUE_READ_PERFORMED=NO`

`CANDIDATE_REPRESENTATION_VALUE_READ_PERFORMED=NO`

`SOURCE_REPRESENTATION_INVENTORY_PERFORMED=NO`

`MATCHING_PERFORMED=NO`

`ZE1_EXECUTION_PERFORMED=NO`

`E2_EXECUTION_PERFORMED=NO`

`MAPPING_PERFORMED=NO`

`ANALYZER_EXECUTION_PERFORMED=NO`

`REPAIR_EXECUTION_PERFORMED=NO`

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0328_AUTHORIZATION_AUTHOR_CANDIDATE`
