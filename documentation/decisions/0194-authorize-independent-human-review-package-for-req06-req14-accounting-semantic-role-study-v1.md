# Decision 0194 — Authorize Independent Human Review Package for Req06/Req14 Accounting Semantic-Role Study V1

Date: 30 August 2026

Status: INDEPENDENT HUMAN REVIEW PACKAGE AUTHORING AUTHORIZED — PACKAGE NOT YET AUTHORED

## Immutable predecessor

Decision0193 commit:

`bfa56e86ae24bf330a33b89cd70cb00fc5d9df4e`

Decision0193 tree:

`593f7d7938cf89acaaa98ab462603e7cbaa811ca`

The Req06/Req14 Accounting Semantic-Role Resolution Study V1 remains:

`STUDY_STATUS=AUTHOR_CANDIDATE`

Its author-candidate role classifications are:

- Req06 `forward_accounting_required`:
  `CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT`
- Req14 `reverse_accounting_required`:
  `CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT`

For both requirements:

`FURTHER_ACCOUNTING_SATISFACTION_EVIDENCE_REQUIRED`

## Authorization

`INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORIZED=YES`

Decision0194 authorizes one immediately subsequent transaction to author an
independent human review package for this exact immutable study and its exact
evidence-anchor matrix.

The future review package must contain six review items:

- ASRR01 — immutable evidence/study binding;
- ASRR02 — Req06 semantic-role support;
- ASRR03 — Req14 semantic-role support;
- ASRR04 — role-resolution versus pair-promotion distinction;
- ASRR05 — accounting-satisfaction evidence-gap conclusion;
- ASRR06 — technical and downstream nonclaims.

Review-item decision vocabulary:

- `PASS`
- `REVISION_REQUIRED`

Overall review vocabulary:

- `APPROVE_BOUNDED_ROLE_STUDY`
- `REVISION_REQUIRED`

## Human-field boundary

The future package must not synthesize or prefill:

- reviewer identity;
- reviewer role;
- reviewer decisions;
- reviewer notes or rationale;
- reviewer signature or confirmation;
- review date;
- reviewer attestation.

All such fields must remain blank pending actual independent human review.

`HUMAN_REVIEW_PACKAGE_AUTHORED=NO`

`HUMAN_REVIEW_PERFORMED=NO`

`HUMAN_REVIEW_RECORDED=NO`

## Governance boundary

Authoring a blank review package is not review completion.

A later completed human review is not itself governance adoption.

`ROLE_GOVERNANCE_ADOPTED=NO`

`PAIR_RECLASSIFICATION_PERFORMED=NO`

`SUPPORTED_BINDING_CREATED=NO`

`NOT_SUPPORTED_BINDING_CREATED=NO`

`ACCOUNTING_SATISFACTION_ESTABLISHED=NO`

The D0191 pair-state distribution remains unchanged:

- 211 `SUPPORTED_BINDING`;
- 1642 `UNRESOLVED_BINDING`;
- 0 `NOT_SUPPORTED_BINDING`.

All 218 Req06/Req14 pair records remain unresolved.

## Downstream nonauthorization

`OPERATIONAL_MAPPING_CREATED=NO`

`OPERATIONAL_MAPPING_AUTHORIZED=NO`

`SCHEMA_V2_MODIFIED=NO`

`SCHEMA_SUCCESSOR_AUTHORIZED=NO`

`CURL_JSON_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

## One-time review-package authorization verifier

Decision0194 authors:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_semantic_role_resolution_study_v1_independent_human_review_package_authorization_v1/02_authorize_independent_human_review_package_once.v1.py`

Execution in Decision0194:

`NO`

Authorized future execution count:

`1`

Authorized consuming transaction:

`IMMEDIATELY_SUBSEQUENT_REVIEW_PACKAGE_AUTHORING_TRANSACTION_ONLY`

After first execution:

`PERMANENTLY_RETIRED`

Rerun authorization:

`NO`

## Retired verifier boundary

Decision0192 A02 remains permanently retired and must not be rerun.

Decision0190 P03 remains permanently retired and must not be rerun.

Decision0187 A02 remains permanently retired and must not be rerun.

Decision0188 CRLF-safe successor remains permanently retired and must not be
rerun.

## Next boundary

`EXECUTE_DECISION0194_A02_EXACTLY_ONCE_AND_IF_PASS_AUTHOR_BLANK_INDEPENDENT_HUMAN_REVIEW_PACKAGE`

No human review is performed by Decision0194.
