# Decision 0008: Gate 1B Sampling, Blind Annotation, and Quarantine Freeze

- Status: Accepted
- Date: 2026-08-06
- Stage: Stage A — verification
- Gate: Gate 1B

## Sampling decision

The gold frame contains only newly generated drivers that compile under the
future pinned build procedure. If at most 140 compile, the study uses a census.
Otherwise it draws exactly 140 without replacement using library-by-model
strata, a minimum-one capped proportional largest-remainder allocation, and the
preregistered SHA-256 ranking seed `2026080603`.

Every eligible driver has positive conditional inclusion probability. Each
selected driver records `N_h`, `n_h`, `pi_h=n_h/N_h`, and `w_h=N_h/n_h`.
Scenario and compiler-warning coverage are diagnostics, not zero-probability
quotas. No reroll, replacement, desired-yield generation, or post-hoc expansion
is allowed. The Gate 0 power-planning value of 18 held-out drivers per library
is explicitly not a sampling quota.

## Annotation decision

Two non-author annotators independently inspect each whole anonymized driver,
discover resources and obligations before verdict assignment, label the blinded
union independently, and submit records before third-party adjudication. The
main analyzer/repair developer cannot serve as a primary annotator.

Eligible human gold records use VALID, VIOLATION-MUST, or VIOLATION-MAY;
UNKNOWN remains an analyzer abstention and is not a human gold label.
OUT_OF_SCOPE records receive no validity verdict. Violations require a D1-D8
category, while VALID records carry no defect category. Every verdict-phase
record must declare IN_SCOPE or OUT_OF_SCOPE and retain an evidence citation.

A per-person per-driver exposure registry disqualifies anyone who has viewed
SemanticVerify-Fuzz, QuartetFuzz, controlled-LLM, baseline, or repair output for
that driver. Gold labels freeze before machine output is revealed. Missing two
independent annotators or a third adjudicator downgrades affected results to
exploratory; developer labels cannot substitute.

## Boundary

No sample is drawn, no driver is opened, and no model is called by this freeze.
Gate 1 remains in progress. Analyzer implementation is not authorized by Gate
1B, primary generation remains blocked, and repair remains prohibited until
Gate V.
