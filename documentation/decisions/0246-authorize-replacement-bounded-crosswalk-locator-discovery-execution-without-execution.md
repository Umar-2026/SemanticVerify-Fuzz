# Decision 0246 — Authorize Replacement Bounded Crosswalk Locator Discovery Execution Without Execution

Status: `AUTHORIZATION ONLY — NOT EXECUTED`

Decision0246 assigns Decision0247 as the replacement execution decision for the bounded locator-discovery operation originally authorized by Decision0244.

The original Decision0245 execution designation was never executed and was superseded unexecuted when Decision0245 was consumed by the D0244 verifier-binding corrective successor.

Decision0246 inherits all three complete D0244 root records exactly, including their governed anchor-member metadata. No root metadata is dropped or reconstructed through a reduced projection.

Decision0247 is authorized only for the exact metadata-only discovery contract preserved from Decision0244: three exact Git tree roots, recursion depth one, immediate tracked child metadata only, and the fixed ten-token lexical filename filter.

Decision0246 does not itself enumerate root children or read candidate content.

`D0247_EXECUTION_AUTHORIZED=YES`
`D0247_EXECUTION_PERFORMED=NO`
`LOCATOR_DISCOVERY_EXECUTED=NO`

`C2_AUTHORIZED=NO`
`C3_AUTHORIZED=NO`
`B2_AUTHORIZED=NO`

Next required checkpoint:

`INDEPENDENT_READ_ONLY_VERIFY_D0246_BEFORE_ANY_D0247_LOCATOR_DISCOVERY_EXECUTION`
