# Decision 0137 — Authorize Requirement-Bound Carrier Admissibility Resolution Study V1

## Status

AUTHORIZED — STUDY V1 NOT YET AUTHORED

## Decision-0136 checkpoint

Commit:

`ea07e29b61e2a9d76a852be7acfdd1d942aa367d`

Tree:

`ab39a1f9cea358cecda12de673424f33f75b6bcb`

Parent Decision-0135 commit:

`92d745dd3186ef8a528196976b283f75d7bd43b8`

Bounded Requirement-Provenance Governance Adoption V1 Git tree:

`9893bd5dc8d7472f1177c373fa89d289de9ca59f`

## Governance-adopted prerequisite

The project now has a reviewed and governance-adopted result:

`REQUIREMENT_PROVENANCE_RESOLVED`

with scope:

`REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY`

The exact requirement domain is fixed at 17 existing V4 losslessness
requirements:

- BOUND_EXACT: 17
- BOUND_COMPOSITE: 0
- UNRESOLVED: 0

## Historical carrier-analysis basis

The prior semantic-unit/carrier study remains immutable and read-only.

Bound Git tree:

`3f04237bdc58c2be56e85628de5923b87578a051`

Historical domains remain:

- semantic units: 109
- Schema-V2 paths: 171
- semantic-unit/path pairs: 18,639

Decision 0137 does not alter or reclassify any of those historical pairs.

## Authorized successor study

Decision 0137 authorizes:

`Schema-V2 Requirement-Bound Carrier Admissibility Resolution Study V1`

The study may assess each of the 17 governance-bound requirements against
existing Schema-V2 carrier support.

Allowed requirement-level classifications are:

- `ADMISSIBLE_EXACT`
- `ADMISSIBLE_COMPOSITE`
- `NO_ADMISSIBLE_CARRIER_PROVEN`
- `UNRESOLVED`

A missing discovered carrier is not sufficient for a negative conclusion.

`NO_ADMISSIBLE_CARRIER_PROVEN` requires a requirement-specific exhaustive
carrier-domain argument.

If any requirement remains unresolved, the global study outcome must remain:

`FURTHER_EVIDENCE_REQUIRED`

Only if all 17 requirement-level carrier questions are resolved may the study
report:

`REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLVED`

## Critical distinction

Requirement-level carrier admissibility is not a positive mapping witness.

Requirement-level carrier non-admissibility is not automatically a global
mapping-impossibility proof.

Even if all 17 requirements obtain admissible carriers, joint cross-requirement
coherence and whole mapping correctness remain separate questions.

## Preserved immutable evidence

The study must not modify:

- active Schema V2;
- approved curl V4;
- Mapping Contract V4;
- the adopted 17-requirement provenance result;
- the prior 109 semantic-unit inventory;
- the prior 171-path domain;
- the historical 18,639 pair state.

## Prohibited evidence

The study may not inspect or use:

- generated-driver source;
- selected-sample membership;
- raw model responses;
- compiler-log semantic contents;
- gold labels;
- analyzer output;
- baseline output;
- LLM-review output;
- repair output.

## Nonauthorizations

Decision 0137 does not authorize:

- historical pair reclassification;
- operational positive mapping;
- global negative mapping impossibility;
- whole-V4 exhaustiveness;
- active Schema-V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution;
- repair.

## Pre-study verifier lifecycle

Decision-0137 A02 is created but not executed by this decision.

Initial state:

`ACTIVE_UNCONSUMED`

It may execute exactly once immediately before Study V1 authoring.

Its execution checkpoint must be the immediate committed successor of
Decision 0136.

After that one execution, successful or failed, it must become:

`PERMANENTLY_RETIRED`

No previously retired A02 verifier may be executed.

## Next boundary

`RUN_DECISION_0137_A02_EXACTLY_ONCE_IMMEDIATELY_BEFORE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1_AUTHORING`
