# Decision 0130 — Authorize External Independent Human Review Handoff for RPR01–RPR08

## Status

AUTHORIZED — EXTERNAL HANDOFF NOT YET AUTHORED

## Bound Decision-0129 checkpoint

Commit:

`7ddaaa2e24a065053c132700292023dfaca9c428`

Tree:

`2335405893a975a264352a6ece5dc318fe9ae670`

Independent Human Review Package V1 Git tree:

`35794b450ed9bcde337f4ea4b7de35dd8218cc03`

Decision-0129 SHA-256:

`c2390666adaa7c2a92f514516f62aed3db044432041696e63988772657f273a1`

## Sealed repository-bundle checkpoint

The immutable Git bundle contained in Review Package V1 was intentionally
created during Decision 0129 authoring from the Decision-0128 repository
checkpoint.

Its checkpoint commit is:

`7f13e5569c5d25c9c104a9b1dd68516471b6017a`

Its role is:

`DECISION_0128_PRE_REVIEW_PACKAGE_CHECKPOINT`

This bundle checkpoint is intentionally distinct from the Decision-0129
package-author checkpoint.

The distinction is expected and does not represent a package-integrity
failure.

## Review subject

The external handoff is limited to independent review of the immutable:

`V4 Losslessness Requirement Provenance and Binding Resolution Study V1`

through Review Package V1 criteria:

`RPR01–RPR08`

Required reviewer role:

`Spec-Technical-Reviewer-1`

The bounded author-candidate result under review remains:

- requirement count: 17;
- BOUND_EXACT: 17;
- BOUND_COMPOSITE: 0;
- UNRESOLVED: 0;
- outcome: `REQUIREMENT_PROVENANCE_RESOLVED`;
- scope: requirement identity and immutable source provenance only.

## Required handoff form

The successor external handoff must include:

1. an immutable ZIP containing the exact Review Package V1;
2. its sealed repository checkpoint Git bundle;
3. all portable source-evidence copies;
4. the blank RPR01–RPR08 reviewer packet;
5. the safe package verifier and checksum closure; and
6. an editable manual reviewer-packet copy that initially matches the blank
   packet byte-for-byte.

No reviewer decision, reviewer identity, reviewer notes, or overall approval
may be prefilled or synthesized by the author.

## Human-review state

Human review has not yet been performed.

Reviewer decision:

`NONE`

The external reviewer must independently complete and return the reviewer
packet.

## Retired verifier boundary

Decision-0128 A02 is permanently retired.

Decision-0126 A02 is permanently retired.

Neither may ever be rerun.

Decision-0130 A02 is a new one-time pre-handoff-authoring verifier.

It is not executed by Decision 0130.

Current state:

`ACTIVE_UNCONSUMED`

It may run exactly once immediately before External Handoff V1 authoring and
must then be permanently retired.

## Preserved non-authorizations

Decision 0130 does not authorize:

- recording a human-review decision;
- study governance adoption;
- semantic-unit/carrier pair reclassification;
- carrier-admissibility conclusions;
- positive mapping witness authoring;
- negative mapping-impossibility proof authoring;
- whole-V4 exhaustiveness claims;
- operational mapping;
- active Schema-V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution;
- repair.

## Next boundary

`RUN_DECISION_0130_A02_EXACTLY_ONCE_IMMEDIATELY_BEFORE_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_V1_AUTHORING`
