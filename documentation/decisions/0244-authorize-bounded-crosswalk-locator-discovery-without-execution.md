# Decision 0244 — Authorize Bounded Crosswalk Locator Discovery Without Execution

Status: `AUTHORIZATION ONLY — NOT EXECUTED`

Decision0244 authorizes exactly one later bounded locator-discovery phase, designated D0245.

The authorized universe is limited to three exact Git tree objects bound to the verified D0243 checkpoint. The later execution may enumerate only immediate tracked child metadata and apply the fixed lexical filename filter defined in the D0244 machine record.

Decision0244 does not authorize reading candidate file contents, evidence acquisition, semantic interpretation, carrier-admissibility adjudication, candidate disposition creation, pair reclassification, operational mapping, Req06/Req14 satisfaction determination, C2 acquisition, C3, or B2.

A future locator candidate is only a locator candidate. Its authority, identity, crosswalk semantics, and suitability must be resolved separately before any C2 acquisition authorization.

`LOCATOR_DISCOVERY_AUTHORIZED=YES`
`LOCATOR_DISCOVERY_EXECUTED=NO`
`C2_AUTHORIZED=NO`
`C2_EXECUTED=NO`
`B2_READINESS_ESTABLISHED=NO`
`B2_AUTHORIZED=NO`
`B2_EXECUTED=NO`

Next required checkpoint:

`INDEPENDENT_READ_ONLY_VERIFY_D0244_BEFORE_ANY_D0245_LOCATOR_DISCOVERY_EXECUTION`
