# Decision 0147 — Authorize Requirement-to-Semantic-Unit Crosswalk Evidence Resolution Study V1

## Status

AUTHORIZED — CROSSWALK EVIDENCE RESOLUTION STUDY NOT YET AUTHORED

## Decision-0146 checkpoint

Commit:

`179f59732d0a68d115e7902794dddb512b5dc4c0`

Tree:

`ec9f6c79940b09afa3432ede511342cda48cb0f7`

Parent Decision-0145 commit:

`089a1af716bc754c8594041467260c4c23579821`

Bounded Governance Adoption V1 Git tree:

`cf3df758ba19115e0cfffe1bf9b452e8520e7680`

## Adopted prerequisite

Requirement-Bound Carrier Admissibility Resolution Study V1 is governance
adopted with the bounded result:

`FURTHER_EVIDENCE_REQUIRED`

The remaining blocking gap is:

`NO_AUTHORIZED_REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_IDENTIFIED`

Carrier-admissibility accounting remains:

- `ADMISSIBLE_EXACT = 0`
- `ADMISSIBLE_COMPOSITE = 0`
- `NO_ADMISSIBLE_CARRIER_PROVEN = 0`
- `UNRESOLVED = 17`

## Authorized new evidence study

Decision 0147 authorizes a new author-candidate study whose sole objective is
to determine whether the 17 governance-bound canonical requirement identities
can be evidence-bound to the existing 109 semantic units.

The complete candidate universe is:

`17 × 109 = 1,853 requirement-to-semantic-unit pairs`

Every pair must be accounted for.

## Pair-level classification vocabulary

Exactly one of:

- `SUPPORTED_BINDING`
- `NOT_SUPPORTED_BINDING`
- `UNRESOLVED_BINDING`

must be assigned to each of the 1,853 new crosswalk candidate pairs.

Absence of positive evidence must not automatically become
`NOT_SUPPORTED_BINDING`.

Lexical similarity, open-string capacity, historical carrier-pair state, or
field-class relation evidence must not be automatically promoted into a
positive semantic binding.

## Requirement-level rollup vocabulary

Each of the 17 requirements must receive exactly one rollup:

- `BOUND_SINGLE_UNIT`
- `BOUND_COMPOSITE_UNITS`
- `NO_AUTHORIZED_CROSSWALK_PROVEN`
- `UNRESOLVED`

A bound crosswalk is only a requirement-to-semantic-unit identity linkage.

It does not establish Schema-V2 carrier admissibility.

It does not establish an operational mapping.

## Historical-state protection

The historical:

`109 × 171 = 18,639`

semantic-unit-to-Schema-V2-path pair matrix remains immutable and read-only.

Decision 0147 does not authorize any historical pair reclassification.

## Possible author-candidate study outcomes

The study may conclude only one of:

- `CROSSWALK_RESOLVED_FOR_ALL_17`
- `PARTIAL_CROSSWALK_FURTHER_EVIDENCE_REQUIRED`
- `FURTHER_EVIDENCE_REQUIRED`

Any result remains an `AUTHOR_CANDIDATE` until independently reviewed and
separately governance adopted.

## Independent review

Independent human review is required after study authoring.

The authoring workflow must not synthesize reviewer decisions, reviewer
identity, or review approval.

## Explicit nonauthorizations

Decision 0147 does not authorize:

- carrier-admissibility reclassification;
- historical 18,639 pair reclassification;
- operational mapping;
- active Schema-V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution;
- repair.

## Prohibited evidence

The study must not inspect:

- generated-driver source;
- selected-sample membership;
- raw model responses;
- compiler-log semantic contents;
- gold labels;
- analyzer output;
- baseline output;
- LLM-review output;
- repair output.

## Decision-0147 A02 lifecycle

A new one-time pre-study authoring verifier is created by this decision.

Initial state:

`ACTIVE_UNCONSUMED`

It is not executed by Decision 0147.

It may execute exactly once immediately before Crosswalk Evidence Resolution
Study V1 authoring.

The execution checkpoint must be the immediate committed successor of
Decision 0146.

After its single execution, successful or failed, it becomes:

`PERMANENTLY_RETIRED`

No previously retired A02 verifier may be executed.

## Next boundary

`RUN_DECISION_0147_A02_EXACTLY_ONCE_IMMEDIATELY_BEFORE_REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_EVIDENCE_RESOLUTION_STUDY_V1_AUTHORING`
