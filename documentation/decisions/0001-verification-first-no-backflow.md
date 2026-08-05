# Decision 0001: Verification First and No Backflow

- Status: Accepted
- Date: 2026-08-05

## Decision

SemanticVerify-Fuzz is implemented in two strictly separated stages.

Stage A develops and evaluates verification. Repair code, prompts, patches,
execution results, and reviewer decisions are unavailable to Stage A.

Gate V irreversibly freezes the verification corpus, gold labels, analyzer,
configuration, metrics, baseline mappings, results, and claims.

Stage B begins only after Gate V. Repair findings may not revise the primary
Stage A analysis. Later discoveries are reported only as explicitly labelled
secondary sensitivity analyses.

## Rationale

The separation prevents repair evidence from tuning the verifier or changing
gold decisions, preserves the independence of verification claims, and keeps
RQ4 secondary to the primary verification contribution.
