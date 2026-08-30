# Decision 0192 — Authorize Req06/Req14 Accounting Semantic-Role Resolution Study V1

Date: 30 August 2026

Status: BOUNDED STUDY AUTHORIZED — ROLE NOT YET CLASSIFIED

## Predecessor

Decision0191 commit:

`119df8756fdb483d969b5a1b6b8ab2c7bba2d165`

Decision0191 established a bounded requirement-to-semantic-unit successor with:

- 211 `SUPPORTED_BINDING`;
- 1642 `UNRESOLVED_BINDING`;
- 0 `NOT_SUPPORTED_BINDING`.

Fifteen of seventeen canonical requirements have at least one supported
requirement-to-semantic-unit binding.

The two requirements with no supported pair binding are:

- Req06 `forward_accounting_required`;
- Req14 `reverse_accounting_required`.

Each currently has 109 unresolved pair records.

## New bounded evidence

Current bound evidence establishes that Schema V2 contains a distinct
`semantic_accounting` structure with:

- source-unit-to-schema-carrier forward accounting;
- schema-carrier-to-source-unit reverse accounting;
- mandatory `forward_complete=true`;
- mandatory `reverse_complete=true`;
- source inventory counts.

The Schema-V2 design record explicitly identifies:

`/semantic_accounting/forward_accounting`

and

`/semantic_accounting/reverse_accounting`

as dedicated sensitive-semantics carriers.

Residual evidence states that forward and reverse accounting are supported by
the schema, while explicitly preserving the distinction that accounting alone
does not prove that each source semantic is preserved and exactly
reconstructable.

Historical requirement-bound carrier evidence remains valid only within its
original bounded result. It remains `FURTHER_EVIDENCE_REQUIRED` and is not
retroactively upgraded.

## Decision

`ROLE_RESOLUTION_STUDY_AUTHORIZED=YES`

Decision0192 authorizes one subsequent bounded authoring transaction for
Req06/Req14 Accounting Semantic-Role Resolution Study V1.

The study must classify each target requirement using only:

- `CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT`;
- `UNIT_BINDABLE_SUBSTANTIVE_REQUIREMENT`; or
- `ROLE_UNRESOLVED`.

Any resulting role classification is an author-candidate study result and
requires independent human review before governance adoption.

## Critical distinction

Role resolution is not requirement-to-semantic-unit pair promotion.

Role resolution is not proof that forward or reverse accounting has been
satisfied by an operational mapping.

Schema support for accounting carriers is not equivalent to populated,
complete accounting evidence.

Even complete accounting would not by itself prove exact lossless semantic
encoding and reverse reconstruction.

## Decision0192 non-actions

`ROLE_CLASSIFICATION_PERFORMED=NO`

`PAIR_RECLASSIFICATION_PERFORMED=NO`

`SUPPORTED_BINDING_CREATED=NO`

`NOT_SUPPORTED_BINDING_CREATED=NO`

`ACCOUNTING_SATISFACTION_ESTABLISHED=NO`

`OPERATIONAL_MAPPING_CREATED=NO`

`OPERATIONAL_MAPPING_AUTHORIZED=NO`

`SCHEMA_V2_MODIFIED=NO`

`SCHEMA_SUCCESSOR_AUTHORIZED=NO`

`CURL_JSON_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

The existing 211 supported pairs remain unchanged.

The existing 1642 unresolved pair records remain unchanged.

The 218 Req06/Req14 pair records remain unresolved.

## One-time authorization verifier

Decision0192 authors:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_req06_req14_accounting_semantic_role_resolution_study_v1_authorization/02_authorize_accounting_semantic_role_resolution_study_once.v1.py`

Execution in Decision0192:

`NO`

Authorized future execution count:

`1`

After first execution:

`PERMANENTLY_RETIRED`

Rerun authorization:

`NO`

## Next boundary

`EXECUTE_DECISION0192_A02_EXACTLY_ONCE_AND_IF_PASS_AUTHOR_REQ06_REQ14_ACCOUNTING_SEMANTIC_ROLE_RESOLUTION_STUDY_V1`

No role classification is governance-adopted by Decision0192.
