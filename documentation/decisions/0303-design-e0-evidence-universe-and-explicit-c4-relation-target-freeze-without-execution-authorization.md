# D0303 — Design E0 evidence-universe and explicit-C4-relation-target freeze without execution authorization

## Status

`DESIGN_ONLY_AUTHOR_CANDIDATE_NOT_EFFECTIVE_UNTIL_INDEPENDENTLY_VERIFIED_COMMITTED_AND_PUBLISHED`

D0303 is design-only. It does not execute E0 and does not authorize E1 extraction, E2 adjudication, C4, B2, positive V4→V2 mapping, curl.json materialization, gold annotation, analyzer execution, baseline execution, or repair.

## Source checkpoint

- Published and effective D0302 commit: `e034b3f6b9b71bbfd2447368dbd72794c395bf8d`
- Machine design artifact: `evaluation/governance_reconciliation/d0303_e0_evidence_universe_and_explicit_c4_relation_target_freeze_design.json`
- Machine artifact SHA-256: `2308fc76e2bcf5dd05c2658b30fd7375c26e248783795b0b91f8f508a46ec7e1`

## E0 candidate-universe freeze design

The future E0 freeze uses exactly the 171 lexicographically ordered `SCHEMA_V2_PROPERTY_PATH` identifiers already frozen by D0301.

No candidate reselection, subsetting, candidate-specific ad-hoc query rewriting, or alternate candidate namespace is permitted.

## Explicit C4 relation target

Relation target:

`SVF-C4-EXPLICIT-CARRIER-CLOSURE-RELATION-TARGET-V1`

For each exact D0301 candidate, future evidence processing may test only whether a frozen provenance-bound evidence unit explicitly establishes that candidate's relation to the governed C4 closure criterion.

Support must not require:

- cross-source joins;
- schema V4→V2 mapping;
- carrier inference;
- promotion of D0191 supported binding;
- promotion of positional or sufficiency status;
- absence-as-negative-proof reasoning;
- Req06/Req14 satisfaction inference;
- concrete mapping.

An evidence unit with no explicit support is not negative proof and is not an exclusion or carrier-inadmissibility decision.

## Evidence-source universe

D0303 freezes a future E0 source universe to the exact nine D0243 inventory members.

Exactly four members are `SUBSTANTIVE_EXISTING_EVIDENCE`:

- `C1-S01`
- `C1-S02`
- `C1-S03`
- `C1-S04`

Exactly five members are `GOVERNANCE_SUPPORT`:

- `C1-G01`
- `C1-G02`
- `C1-G03`
- `C1-G04`
- `C1-G05`

Only the four substantive members may later yield adjudicable evidence units. Governance-support members may constrain processing but may not themselves count as substantive evidence for the C4 relation target.

No repository-wide open-ended search, network search, external source, or source expansion is permitted by D0303.

Any future source expansion requires a separate governance successor and a new E0 freeze before E1 extraction.

## Uniform future E1 protocol

D0303 does not authorize E1. If E1 is later separately authorized, the frozen pair domain is exactly:

`171 candidates × 4 substantive sources = 684 candidate-source pairs`.

Every pair receives the same protocol.

Candidate matching uses only the exact `schema_v2_property_path` string. No fuzzy matching, semantic search, alias expansion, candidate-specific query rewriting, or cross-source join is allowed.

Markdown sources use exact-identifier occurrence followed by blank-line-delimited paragraph extraction.

JSON sources use exact string-key or exact string-value equality followed by extraction of the smallest enclosing JSON object or array element.

Zero exact occurrences are recorded as zero occurrences only. They are not negative evidence.

## Immutable source identities

Each source is bound by:

- D0243 member ID;
- class;
- role;
- path;
- SHA-256;
- Git blob OID.

Any byte or blob-identity change invalidates that source for this E0 version and requires separate governance.

## Evidence-unit locators and hashes

Markdown evidence units use 1-based line ranges in the frozen Git blob.

JSON evidence units use RFC 6901 JSON Pointer information for the exact match and enclosing unit.

Every later evidence unit must bind its candidate, source identity, locator, relation-target ID, extraction-rule ID, and extracted-unit SHA-256.

## Future independent E2 adjudication protocol

D0303 does not authorize E2.

If separately authorized later, adjudication is one provenance-bound evidence unit at a time and may return only:

- `EXPLICIT_C4_CLOSURE_RELATION_SUPPORT_ESTABLISHED`
- `EXPLICIT_C4_CLOSURE_RELATION_SUPPORT_NOT_ESTABLISHED`
- `EVIDENCE_UNIT_REMAINS_AMBIGUOUS`

The adjudicator must be independent of the E1 extraction actor and must not use analyzer, baseline, repair, or D0301 candidate-closure outcomes to form the unit judgment.

No candidate-level aggregation or disposition is permitted during E2.

## Escalation rule

There is no source-expansion escalation inside this D0303 design.

If the four frozen substantive sources are insufficient, processing must fail closed and a separate governance successor must define a new E0 source-universe version.

## Current authorization state

`D0303_DESIGN_EFFECTIVE=NO`

`E0_EXECUTION_AUTHORIZED=NO`

`E1_EXECUTION_AUTHORIZED=NO`

`E2_EXECUTION_AUTHORIZED=NO`

`E3_EXECUTION_AUTHORIZED=NO`

`E4_EXECUTION_AUTHORIZED=NO`

`NEW_EVIDENCE_ACQUISITION_AUTHORIZED=NO`

`NETWORK_EVIDENCE_ACQUISITION_AUTHORIZED=NO`

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

D0303 does not authorize D0251 snapshot-content reads, D0276 retained-evidence-content reads, historical one-time verifier execution, D0301 reexecution, new/network evidence acquisition, E1 extraction, E2 adjudication, result reselection, candidate subsetting, Class06 reclassification, positional reassignment, pair reclassification, Req06/Req14 determination, carrier-admissibility disposition, concrete mapping, or schema V4→V2 mapping.

## Next checkpoint

`INDEPENDENT_READ_ONLY_VERIFY_D0303_E0_FREEZE_DESIGN_AUTHOR_CANDIDATE_BEFORE_COMMIT_OR_PUSH`

No commit, push, E0 execution, E1 extraction, or E2 adjudication is authorized by this authoring transaction.
