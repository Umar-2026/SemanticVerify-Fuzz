# Decision 0248 — Authorize Metadata-Only Locator Candidate Qualification and Identity Binding

Status: `AUTHORIZATION ONLY — NOT EXECUTED`

Decision0248 authorizes Decision0249 to classify exactly the ten D0247 lexical locator candidates using only already-committed metadata.

Decision0249 may compare only root ID, full locator, and Git object ID against the single governed D0246 anchor for the same root.

No candidate content may be opened, read, parsed, or byte-hashed.

The only relation values are `EXACT_BOUND_ANCHOR_MEMBER_IDENTITY` and `NO_BOUND_ANCHOR_IDENTITY_MATCH`.

This metadata-only identity classification does not establish source authority, crosswalk semantics, evidence adequacy, Class06 source status, C2 readiness, Req06/Req14 satisfaction, or B2 readiness.

`D0249_QUALIFICATION_EXECUTION_AUTHORIZED=YES`
`D0249_QUALIFICATION_EXECUTED=NO`

`C2_AUTHORIZED=NO`
`C3_AUTHORIZED=NO`
`B2_AUTHORIZED=NO`

Next required checkpoint:

`INDEPENDENT_READ_ONLY_VERIFY_D0248_BEFORE_ANY_D0249_METADATA_QUALIFICATION_EXECUTION`
