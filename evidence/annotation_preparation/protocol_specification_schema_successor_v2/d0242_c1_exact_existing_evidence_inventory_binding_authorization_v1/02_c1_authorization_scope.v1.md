# D0242 — C1 Exact Existing-Evidence Inventory/Binding Authorization

Status:

`C1_AUTHORIZED_NOT_EXECUTED`

D0242 authorizes only C1: exact existing-evidence inventory and binding.

The authorized input universe contains exactly nine already-governed repository
artifacts: four substantive evidence members and five governance-support
members.

D0242 does not execute C1.

## Authorized C1 operations

A later separately executed D0243 transaction may:

- read only the nine exact bound inputs;
- recompute their SHA-256 values and Git blob identities;
- bind their existing governance provenance;
- parse only identity/governance metadata needed for inventory;
- derive a detached existing-evidence inventory and detached hashes.

No source expansion is permitted.

## Semantic limits

`SUPPORTED_BINDING` does not imply `INCLUDED`.

`UNRESOLVED_BINDING` does not imply `EXCLUDED`.

Absence of positive evidence is not negative proof.

Human technical-support confirmation does not itself imply `INCLUDED`.

Req06/Req14 semantic-role adoption does not establish accounting satisfaction.

Governance-support contracts are not carrier-admissibility results.

C1 inventory binding does not create operational source-unit/carrier mapping.

## Explicit nonauthorization

`C2_AUTHORIZED=NO`

`C3_AUTHORIZED=NO`

`C4_AUTHORIZED=NO`

`C5_AUTHORIZED=NO`

`C6_AUTHORIZED=NO`

`NEW_EVIDENCE_ACQUISITION_AUTHORIZED=NO`

`UNLISTED_SOURCE_EXPANSION_AUTHORIZED=NO`

`CANDIDATE_ADMISSIBILITY_EVALUATION_AUTHORIZED=NO`

`CANDIDATE_DISPOSITION_CREATION_AUTHORIZED=NO`

`PAIR_RECLASSIFICATION_AUTHORIZED=NO`

`AEA01_CONSTRUCTION_AUTHORIZED=NO`

`AEA02_CONSTRUCTION_AUTHORIZED=NO`

`U_DOMAIN_CONSTRUCTION_AUTHORIZED=NO`

`C_DOMAIN_CONSTRUCTION_AUTHORIZED=NO`

`DOMAIN_FREEZE_AUTHORIZED=NO`

`CROSS_SOURCE_JOIN_AUTHORIZED=NO`

`CONCRETE_MAPPING_AUTHORIZED=NO`

`REQ06_REQ14_DETERMINATION_AUTHORIZED=NO`

`B2_READINESS_ESTABLISHED=NO`

`B2_EXECUTION_AUTHORIZED=NO`

`B3_AUTHORIZED=NO`

`B4_AUTHORIZED=NO`

`B5_AUTHORIZED=NO`

`B6_AUTHORIZED=NO`

`B7_AUTHORIZED=NO`

`ACTIVE_SCHEMA_V2_MATERIALIZATION_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

## Execution boundary

D0242 creates authorization only.

No C1 inventory artifact is created by this decision.

Before any D0243 execution, D0242 must receive an independent read-only
verification checkpoint.
