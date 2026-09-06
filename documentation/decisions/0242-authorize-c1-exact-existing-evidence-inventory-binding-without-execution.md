# Decision 0242 — Authorize C1 Exact Existing-Evidence Inventory/Binding Without Execution

Status:

`C1 AUTHORIZED — NOT EXECUTED`

## Decision

Authorize C1 only: exact existing-evidence inventory and provenance/integrity
binding over the nine exact inputs bound by the D0242 authorization package.

The authorization contains:

- four exact substantive existing-evidence members;
- five exact governance-support members;
- exact path, SHA-256, and Git blob identity for every member;
- governing decision provenance for the four substantive members;
- explicit exclusions preventing semantic promotion and source expansion.

## Operational boundary

`C1_AUTHORIZED=YES`

`C1_EXECUTED=NO`

`C2_AUTHORIZED=NO`

`C3_AUTHORIZED=NO`

`C4_AUTHORIZED=NO`

`C5_AUTHORIZED=NO`

`C6_AUTHORIZED=NO`

`NEW_EVIDENCE_ACQUISITION_AUTHORIZED=NO`

`CANDIDATE_ADMISSIBILITY_EVALUATION_AUTHORIZED=NO`

`CANDIDATE_DISPOSITION_CREATION_AUTHORIZED=NO`

`PAIR_RECLASSIFICATION_AUTHORIZED=NO`

`CROSS_SOURCE_JOIN_AUTHORIZED=NO`

`CONCRETE_MAPPING_AUTHORIZED=NO`

`REQ06_REQ14_DETERMINATION_AUTHORIZED=NO`

`B2_READINESS_ESTABLISHED=NO`

`B2_AUTHORIZED=NO`

`B2_EXECUTED=NO`

`DOMAIN_FREEZE_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

C1 execution remains a separate future D0243 transaction and must not begin
until D0242 receives an independent read-only verification checkpoint.
