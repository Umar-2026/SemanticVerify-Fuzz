# D0263 authorization scope

This decision authorizes D0264 only.

Authorized candidate set:
- candidate 8
- candidate 9

Authorized evidence domain:
- frozen D0258 result records for candidates 8 and 9
- frozen D0260 result records for candidates 8 and 9
- frozen D0262 result records for candidates 8 and 9

Authorized activity:
- compare the three recorded sufficiency result values
- compare recorded evidence-reference selections and locator profiles
- compare recorded bounded rationales
- characterize the recorded basis of the three-way discrepancy
- identify the exact follow-on resolution question

Not authorized:
- D0251 snapshot-content reads
- original source-blob reopening
- original worktree candidate reads
- reference following
- repository-wide search
- Git-history search
- network access
- fourth tie-breaker review
- new sufficiency adjudication
- final sufficiency result selection
- positional REQUIRED / NOT_REQUIRED assignment
- Class06 reclassification
- mutation of D0258, D0260, or D0262
- successor result-universe materialization
- C4, C5, C6, or B2 authorization or execution

D0264 execution remains blocked until D0263 receives a separate independent read-only authorization checkpoint.
