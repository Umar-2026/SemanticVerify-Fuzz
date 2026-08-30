# Decision 0193 — Author Req06/Req14 Accounting Semantic-Role Resolution Study V1

Date: 30 August 2026

Status: AUTHOR-CANDIDATE ROLE STUDY CREATED — INDEPENDENT HUMAN REVIEW REQUIRED

## Authorization predecessor

Decision0192 commit:

`d8fb51e465b91c3e2d37dcdf2a1bdd1c3b6f5506`

Decision0192 tree:

`9a303fea709154a96adcd38e8ed872c6fc2517be`

Decision0192 authorized exactly one authoring transaction for the bounded
Req06/Req14 Accounting Semantic-Role Resolution Study V1.

## Decision0192 A02 consumption

A02 SHA-256:

`318989e9cf4c70bc2145f7e3c2718250abd429b4f7ea64ad473ce32510216a94`

Execution count:

`1`

Execution result:

`PASS`

Execution output SHA-256:

`06ba902d90727fb202024743d4eecc89c7df02bddb8e01e9658c82298370be86`

Pre-execution sentinel SHA-256:

`297f7d36a32712080a305c18dc533d1483f30f3981891617891f1b3e32df43c1`

Lifecycle:

`PERMANENTLY_RETIRED`

`DECISION0192_A02_RERUN_AUTHORIZED=NO`

Decision0192 A02 must never be executed again.

## Study result

The bounded author-candidate study classifies:

Req06 `forward_accounting_required`:

`CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT`

Req14 `reverse_accounting_required`:

`CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT`

The classification is based on the explicitly bound structural evidence:

- Schema V2 defines forward accounting as source-unit-to-schema-carrier
  accounting records;
- Schema V2 requires `forward_complete=true`;
- Schema V2 defines reverse accounting as schema-carrier-to-source-unit
  accounting records;
- Schema V2 requires `reverse_complete=true`;
- the design record assigns dedicated
  `/semantic_accounting/forward_accounting` and
  `/semantic_accounting/reverse_accounting` carriers;
- residual evidence explicitly states both accounting directions are
  schema-supported;
- residual evidence also explicitly states accounting alone does not prove
  semantic encoding.

These requirements therefore operate as cross-cutting accounting/completeness
constraints rather than ordinary semantic properties of one selected semantic
unit.

This is an author-candidate study conclusion, not a governance-adopted human
judgment.

## Accounting satisfaction

For both Req06 and Req14:

`FURTHER_ACCOUNTING_SATISFACTION_EVIDENCE_REQUIRED`

Schema capability and semantic-role classification do not prove that a concrete
accounting instance is completely and correctly populated.

`ACCOUNTING_SATISFACTION_ESTABLISHED=NO`

## Pair-state boundary

The D0191 pair successor is unchanged:

- `SUPPORTED_BINDING`: 211;
- `UNRESOLVED_BINDING`: 1642;
- `NOT_SUPPORTED_BINDING`: 0.

All 109 Req06 pair records remain `UNRESOLVED_BINDING`.

All 109 Req14 pair records remain `UNRESOLVED_BINDING`.

`TARGET_PAIR_RECORDS_RECLASSIFIED=0`

`PAIR_RECLASSIFICATION_PERFORMED=NO`

`SUPPORTED_BINDING_CREATED=NO`

`NOT_SUPPORTED_BINDING_CREATED=NO`

No 218-pair promotion is implied or authorized.

## Technical nonclaims

Role classification does not establish a populated operational mapping.

Accounting completeness, if later established, would not by itself prove exact
lossless semantic preservation and reconstruction.

`OPERATIONAL_MAPPING_CREATED=NO`

`OPERATIONAL_MAPPING_AUTHORIZED=NO`

`SCHEMA_V2_LOSSLESSNESS_PROVEN=NO`

`SCHEMA_MAPPING_INFERRED=NO`

`SCHEMA_V2_MODIFIED=NO`

`SCHEMA_SUCCESSOR_AUTHORIZED=NO`

`CURL_JSON_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

## Review status

`STUDY_STATUS=AUTHOR_CANDIDATE`

`INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES`

`GOVERNANCE_ADOPTED=NO`

The study result may not be promoted into governed Req06/Req14 role resolution
before a separately authorized independent human review and subsequent
recording/adoption chain.

## Retired-verifier boundary

Decision0190 P03 remains permanently retired and was not rerun.

Decision0187 A02 remains permanently retired and was not rerun.

Decision0188 CRLF-safe successor remains permanently retired and was not rerun.

Decision0192 A02 is now permanently retired and must never be rerun.

## Next boundary

`SEPARATELY_AUTHORIZE_INDEPENDENT_HUMAN_REVIEW_PACKAGE_FOR_REQ06_REQ14_ACCOUNTING_SEMANTIC_ROLE_RESOLUTION_STUDY_V1`
