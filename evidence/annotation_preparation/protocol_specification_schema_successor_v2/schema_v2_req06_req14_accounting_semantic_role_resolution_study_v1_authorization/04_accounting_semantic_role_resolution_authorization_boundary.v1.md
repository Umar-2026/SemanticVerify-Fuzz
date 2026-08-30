# Decision0192 Req06/Req14 Accounting Semantic-Role Resolution Study Authorization Boundary

Decision0192 authorizes only a bounded author-candidate semantic-role
resolution study for:

- Requirement 06: `forward_accounting_required`
- Requirement 14: `reverse_accounting_required`

The current D0191 pair-classification successor remains unchanged:

- `SUPPORTED_BINDING`: 211
- `UNRESOLVED_BINDING`: 1642
- `NOT_SUPPORTED_BINDING`: 0

For Req06 and Req14 specifically, all 218 requirement-to-semantic-unit pairs
remain `UNRESOLVED_BINDING`.

The authorization exists because the currently bound evidence now distinguishes
accounting structure from ordinary semantic-unit pair binding:

- Schema V2 contains dedicated forward and reverse accounting structures;
- Schema V2 requires explicit forward and reverse completeness flags;
- the Schema-V2 design record identifies dedicated accounting carrier paths;
- residual evidence states that forward and reverse accounting are supported by
  the schema;
- residual evidence also states that accounting alone does not prove semantic
  encoding;
- historical carrier/admissibility evidence remains bounded and unresolved and
  must not be retroactively upgraded.

The future study may determine only one of the following author-candidate role
states for each target requirement:

1. `CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT`
2. `UNIT_BINDABLE_SUBSTANTIVE_REQUIREMENT`
3. `ROLE_UNRESOLVED`

The future study must separately state whether accounting satisfaction requires
further evidence.

Role resolution does not itself create a requirement-to-semantic-unit
`SUPPORTED_BINDING`.

Role resolution does not itself establish accounting completion.

Accounting completion would not by itself establish lossless semantic
preservation or reverse reconstruction.

Decision0192 performs no semantic-role classification.

Decision0192 performs no pair reclassification.

Decision0192 creates no `SUPPORTED_BINDING`.

Decision0192 creates no `NOT_SUPPORTED_BINDING`.

Decision0192 does not establish or authorize operational mapping.

Decision0192 does not authorize Schema-V2 modification, a schema successor,
`curl.json`, analyzer implementation/execution, baseline execution, or repair.

The one-time authorization verifier authored by Decision0192 is not executed
in Decision0192. It may be executed exactly once in the immediately subsequent
study-authoring transaction and is permanently retired after that first
execution regardless of result.
