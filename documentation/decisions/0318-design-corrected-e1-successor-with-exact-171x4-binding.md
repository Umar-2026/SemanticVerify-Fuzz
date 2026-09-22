# D0318 — Design Corrected E1 Successor with Exact 171×4 Binding

## Status

`DESIGN_ONLY_AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0318 is design-only.

D0318 does not authorize E1 execution, corrected E1 execution, E2 adjudication, C4, B2, P8 mapping, gold annotation, analyzer implementation/execution, baseline execution, or repair.

## Source checkpoint

Effective corrective checkpoint:

`be53d66dcd619bf6c2d38dc078617399971c31e2`

D0317 established that Batch 001–044 are historical placeholder scaffolding and credit zero valid governed E1 pair completions.

The historical placeholder output tree remains preserved and is not rewritten by D0318.

## Corrected candidate universe

The corrected E1 successor binds exactly the 171 frozen D0303 candidates.

Namespace:

`SCHEMA_V2_PROPERTY_PATH`

Ordering:

`LEXICOGRAPHIC_ASCENDING`

Candidate count:

`171`

D0318 candidate-manifest canonical JSON SHA-256:

`c2746447215aa5aa2be0abea3bb631043eb0bb12745cc54309881d88a5a1f908`

No candidate reselection, subsetting, alias expansion, fuzzy matching, semantic search, or candidate-specific query rewriting is allowed.

## Corrected substantive source universe

Exactly four frozen substantive sources are permitted:

- `C1-S01`
- `C1-S02`
- `C1-S03`
- `C1-S04`

Each source is bound by the frozen D0303 identity fields:

- `member_id`
- `class`
- `role`
- `path`
- `sha256`
- `git_blob_oid`

D0318 source-manifest canonical JSON SHA-256:

`b6c97642ee0a3bc8de5839209a0a8546feb61beedc198c24a8c43c44b6534b52`

No source expansion, repository-wide search, network search, or external evidence acquisition is allowed.

Any source identity/hash/blob mismatch must fail closed before extraction.

## Exact corrected E1 pair domain

The future corrected E1 pair domain is exactly:

`171 × 4 = 684 candidate-source pairs`

Ordering is deterministic:

1. candidate ordinal ascending;
2. source ordinal ascending in `C1-S01`, `C1-S02`, `C1-S03`, `C1-S04` order.

Pair ordinal formula:

`(candidate_ordinal - 1) * 4 + source_ordinal`

Pair IDs are:

`E1P0001` through `E1P0684`.

D0318 pair-manifest canonical JSON SHA-256:

`fdb49a7bca9a56ea54bd52a7fd63c07df06738cd03db95928d0f1ccf3f3de398`

The full 684-pair manifest is embedded in the D0318 machine artifact.

## Exact extraction protocol

Candidate matching uses the exact frozen `schema_v2_property_path` string only.

Markdown sources:

- locate exact identifier occurrences;
- extract the blank-line-delimited paragraph containing each occurrence;
- record the 1-based frozen-blob line range;
- hash exact extracted paragraph UTF-8 bytes.

JSON sources:

- parse JSON;
- match only exact string keys or exact string scalar values equal to the candidate identifier;
- extract the smallest enclosing JSON object or array element containing the match;
- record the RFC6901 match/enclosing-unit locator;
- hash canonical JSON using sorted keys, compact separators, and `ensure_ascii=false`.

Every distinct unit is materialized in source order.

Deduplication is permitted only for byte-identical or canonical-JSON-identical units within the same candidate-source pair while retaining all relevant locators.

Cross-source joining is prohibited during E1.

Semantic judgment is prohibited during E1.

## Zero-occurrence accounting

Every one of the 684 candidate-source pairs requires a pair record.

If a pair has zero exact candidate identifier occurrences:

- `exact_identifier_occurrence_count = 0`;
- `evidence_units = []`.

This records only absence of an exact occurrence within that frozen source for that candidate.

It is not:

- negative evidence;
- candidate exclusion;
- carrier inadmissibility;
- mapping failure;
- semantic adjudication.

## Future corrected pair-record contract

Future execution ID is frozen as:

`SVF-E1-CORRECTED-RUN-001`

Future clean output root is frozen as:

`evidence/extraction/E1/corrected_run_v1`

This path is distinct from the historical placeholder tree:

`evidence/extraction/E1/d0316_outputs`

Each future pair record binds:

- execution ID;
- deterministic pair ID and ordinal;
- candidate ordinal;
- exact `schema_v2_property_path`;
- source ordinal and member ID;
- source path;
- source SHA-256;
- source Git blob OID;
- relation target ID;
- extraction-rule ID;
- exact occurrence count;
- zero or more provenance-bound evidence units.

Each evidence unit must contain:

- unit ordinal;
- locator kind;
- locator value;
- extracted unit content;
- extracted evidence-unit SHA-256.

Semantic-judgment, candidate-disposition, mapping, and repair fields are prohibited in E1 pair records.

## Replacement one-shot semantics

D0318 does not authorize execution.

Any future authorization must authorize at most one corrected E1 execution attempt.

Before an authorized corrected-E1 execution attempt begins, frozen-source identity and byte integrity must be re-verified against the bound source path, SHA-256, and Git blob OID.

This preauthorization integrity-verification read is explicitly non-consuming and is limited to source identity and byte-integrity verification. It must not perform candidate matching, extraction, evidence-unit construction, pair-record materialization, semantic adjudication, or output writing.

If source identity or integrity verification fails, processing fails closed before the corrected-E1 execution attempt starts and before authorization is consumed.

After integrity verification succeeds, the one-shot authorization is consumed atomically at the first extraction-purpose source-content read or first pair-record write, whichever occurs first.

An extraction-purpose source-content read means source access used for exact candidate matching, occurrence detection, or evidence-unit extraction. It is distinct from the preauthorization integrity-verification read.

Once an authorized extraction attempt begins:

- automatic retry is prohibited;
- reuse of D0308 authorization is prohibited;
- failure or incomplete execution requires a new separately governed successor authorization.

This removes both the historical D0314 consumption ambiguity and any ambiguity between preauthorization source-integrity verification and an extraction-purpose source read.

## Preconditions before any corrected E1 execution

Before any corrected E1 run, a separate successor must independently verify and authorize:

1. exact 171-candidate binding;
2. exact four-source binding;
3. source path/SHA-256/Git-blob identity;
4. candidate-manifest hash;
5. source-manifest hash;
6. 684-pair manifest hash;
7. Markdown extraction rule;
8. JSON extraction rule;
9. zero-occurrence record representation;
10. locator formats;
11. evidence-unit hash rules;
12. future output schema;
13. execution ID;
14. clean output root;
15. one-shot attempt-consumption semantics.

D0318 itself performs none of these future execution actions.

## Authorization state

`E1_EXECUTION_AUTHORIZED=NO`

`CORRECTED_E1_EXECUTION_AUTHORIZED=NO`

`E2_AUTHORIZED=NO`

`E3_AUTHORIZED=NO`

`E4_AUTHORIZED=NO`

`C4_AUTHORIZED=NO`

`B2_AUTHORIZED=NO`

`P8_MAPPING_AUTHORIZED=NO`

`POSITIVE_V4_TO_V2_MAPPING_AUTHORIZED=NO`

`CURL_JSON_MATERIALIZATION_AUTHORIZED=NO`

`P10_GOLD_ANNOTATION_AUTHORIZED=NO`

`P11_ANALYZER_IMPLEMENTATION_AUTHORIZED=NO`

`P11_ANALYZER_EXECUTION_AUTHORIZED=NO`

`BASELINE_EXECUTION_AUTHORIZED=NO`

`REPAIR_EXECUTION_AUTHORIZED=NO`

## Protected boundary

D0318 does not authorize:

- D0251 snapshot-content reads;
- D0276 retained-evidence-content reads;
- D0301 reexecution;
- historical one-time verifier reexecution;
- candidate reselection/subsetting;
- source expansion;
- semantic adjudication;
- Class06 reclassification;
- positional reassignment;
- pair reclassification;
- Req06/Req14 determination;
- carrier-admissibility disposition;
- concrete mapping;
- schema V4→V2 mapping.

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_D0318_CORRECTED_E1_SUCCESSOR_DESIGN_AUTHOR_CANDIDATE`

No commit, push, E1 extraction, substantive extraction-source read, E2 adjudication, mapping, analyzer execution, gold annotation, baseline execution, or repair is authorized by this authoring transaction.
