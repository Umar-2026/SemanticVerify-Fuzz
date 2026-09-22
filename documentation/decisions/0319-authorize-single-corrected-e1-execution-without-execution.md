# D0319 — Authorize Single Corrected E1 Execution Without Execution

## Status

`AUTHORIZATION_AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0319 is an authorization successor candidate.

This authoring transaction does not perform source-integrity verification, does not start corrected E1 extraction, does not create the corrected output root, and does not materialize any pair records or evidence units.

## Source checkpoint

Effective D0318 design checkpoint:

`cc25d9f1e70063eb5a3a7f4da29a78c095ee5e5a`

D0319 is valid only against the exact reviewed and published D0318 contract.

## Frozen corrected-E1 execution contract

D0319 binds exactly:

- candidate universe: 171;
- candidate namespace: `SCHEMA_V2_PROPERTY_PATH`;
- substantive source universe: `C1-S01`, `C1-S02`, `C1-S03`, `C1-S04`;
- pair domain: 684;
- pair range: `E1P0001` through `E1P0684`;
- execution ID: `SVF-E1-CORRECTED-RUN-001`;
- output root: `evidence/extraction/E1/corrected_run_v1`.

Candidate-manifest canonical JSON SHA-256:

`c2746447215aa5aa2be0abea3bb631043eb0bb12745cc54309881d88a5a1f908`

Source-manifest canonical JSON SHA-256:

`b6c97642ee0a3bc8de5839209a0a8546feb61beedc198c24a8c43c44b6534b52`

Pair-manifest canonical JSON SHA-256:

`fdb49a7bca9a56ea54bd52a7fd63c07df06738cd03db95928d0f1ccf3f3de398`

The historical placeholder tree:

`evidence/extraction/E1/d0316_outputs`

remains preserved and must not be used as the corrected execution output location.

## Authorization lifecycle

D0319 is not effective merely because it has been authored.

If and only if D0319 is:

1. independently verified before commit;
2. committed with the exact reviewed bytes;
3. independently verified after commit;
4. published to the governed repository;

then D0319 authorizes at most one corrected E1 execution attempt under the exact D0318 contract.

Before publication:

`CORRECTED_E1_EXECUTION_AUTHORIZED=NO`

After valid publication, the authorization grant is limited to the single corrected E1 attempt described here.

## Preauthorization integrity verification

Before any corrected extraction attempt starts, all four frozen substantive source identities must be re-verified.

The integrity phase is limited to:

- frozen source path verification;
- SHA-256 verification;
- Git blob OID verification;
- candidate-manifest hash verification;
- source-manifest hash verification;
- pair-manifest hash verification;
- clean corrected-output-root verification.

The integrity-verification source read is explicitly not an extraction-purpose read and does not consume the one-shot authorization.

During integrity verification it is prohibited to perform:

- candidate matching;
- occurrence detection;
- evidence extraction;
- evidence-unit construction;
- pair-record writing;
- semantic adjudication;
- mapping;
- repair.

If any frozen source identity, byte hash, blob OID, manifest hash, or output-root condition fails, processing fails closed before the extraction attempt starts and before authorization is consumed.

## Attempt start and authorization consumption

After all preauthorization integrity checks pass, the one-shot authorization is consumed atomically at the first:

- extraction-purpose source-content read; or
- corrected pair-record write;

whichever occurs first.

An extraction-purpose source-content read means source access used for exact candidate matching, exact occurrence detection, or governed evidence-unit extraction.

The preauthorization integrity-verification read is excluded from this consumption event.

After authorization consumption:

- automatic retry is prohibited;
- a failed attempt may not retry under D0319;
- an incomplete attempt may not retry under D0319;
- a new separately reviewed and published successor authorization is required for any later attempt.

The historical D0308 authorization may not be reused.

## Permitted corrected-E1 actions after D0319 becomes effective

Only the following corrected-E1 actions are within scope:

- exact D0318 candidate matching;
- exact D0318 Markdown extraction;
- exact D0318 JSON extraction;
- governed zero-occurrence pair-record materialization;
- provenance-bound evidence-unit materialization;
- exactly one pair record for each D0318 pair;
- writes only under `evidence/extraction/E1/corrected_run_v1`.

## Prohibited corrected-E1 actions

The following remain prohibited:

- candidate reselection;
- candidate subsetting;
- alias expansion;
- fuzzy candidate matching;
- semantic search;
- candidate-specific query rewriting;
- source expansion;
- external or network search;
- repository-wide open-ended evidence search;
- cross-source joining;
- semantic adjudication;
- candidate disposition;
- mapping;
- repair;
- writing corrected outputs into the historical placeholder tree.

## Successful completion contract

A successful corrected E1 completion requires exactly 684 pair records.

The records must:

- use exactly `E1P0001` through `E1P0684`;
- match the D0318 frozen Cartesian pair manifest;
- preserve frozen candidate and source identities;
- use the governed zero-occurrence representation when occurrence count is zero;
- preserve required locators and evidence-unit SHA-256 values when evidence units exist;
- contain no semantic-adjudication, mapping, or repair fields.

A partial execution is not successful completion.

Fewer than 684 pair records is not successful completion.

Additional pair records are prohibited.

Successful E1 completion does not itself authorize E2.

## Downstream authorization state

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

## Protected boundary

D0319 does not authorize:

- D0251 snapshot-content reads;
- D0276 retained-evidence-content reads;
- D0301 reexecution;
- historical one-time verifier execution;
- Class06 reclassification;
- positional reassignment;
- pair reclassification;
- Req06/Req14 determination;
- carrier-admissibility disposition;
- concrete mapping;
- schema V4→V2 mapping.

## Authoring transaction state

During D0319 authoring:

- no substantive source bytes were read;
- no integrity verification was performed;
- no corrected E1 attempt started;
- no one-shot authorization was consumed;
- no corrected output root was created;
- no pair records were written;
- no evidence units were extracted;
- no E2/C4/B2/P8/analyzer/repair action occurred.

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0319_SINGLE_CORRECTED_E1_EXECUTION_AUTHORIZATION_AUTHOR_CANDIDATE`

No commit, push, integrity-verification source read, corrected E1 extraction, E2 adjudication, mapping, analyzer execution, gold annotation, baseline execution, or repair is authorized by this authoring transaction.
