# Decision 0045 — curl Mapping Contract V3 Corrective Author Checkpoint

## Status

Exact V3 corrective successor has been authored from immutable V2.

V3 SHA-256:

`ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97`

V3 size:

`24750` bytes

## Reviewer-required correction

V3 explicitly repairs V2-RR08 by placing the following inside the formal
required losslessness contract:

- ownership-sensitive semantic preservation;
- return-sensitive semantic preservation;
- complete exact approved V4 representation-policy preservation;
- machine-checkable binding of the complete representation-policy object.

The remaining valid V2 proof structure and obstruction witnesses are
preserved.

## RR01

The V2 human RR01 decision remains REVISION_REQUIRED.

The future V3 independent-review handoff must contain portable sealed Git
object evidence sufficient for an external reviewer to independently verify:

- the V3 author checkpoint commit;
- its tree;
- exact V3 bytes at the repository path.

## Author outcome

`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`

This remains an author conclusion pending independent technical review.

## Governance boundary

Exact V2 remains immutable.

Exact V3 becomes immutable at this checkpoint.

This checkpoint does not authorize:

- schema-successor authoring;
- schema modification;
- positive mapping approval;
- curl.json;
- analyzer implementation or execution;
- baseline execution;
- repair.

## Next boundary

`CREATE_INDEPENDENT_REVIEW_PACKAGE_FOR_CURL_MAPPING_CONTRACT_V3_CORRECTED_SCHEMA_INSUFFICIENCY_PROOF`
