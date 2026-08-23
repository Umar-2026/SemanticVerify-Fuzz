# Decision 0106 — Authorize External Independent Review Handoff of Relation-Informed Study V1 Review Package

Status: AUTHORIZED FOR EXTERNAL HANDOFF AUTHORING ONLY — HANDOFF NOT YET AUTHORED

## Decision-0105 source checkpoint

Decision-0105 commit:

`0e76454cef50c4e8383c50561ad3a5818d2aeccd`

Decision-0105 tree:

`0c1fef773a20eb3606ce8e821f43eedff05fe553`

Review Package V1 Git tree:

`a43856c2b63941eaf379b4157669bc8590d585d1`

Blank reviewer packet SHA-256:

`a60a89c97292b62303a5a8f9c5fa0c3c2796f964a46cf544232d2d8202124166`

Review-package manifest SHA-256:

`d2dcaf72e2ebacd79efe1305672065632e11108621910b57ba319b4a9ceed9ae`

Review-package safe verifier SHA-256:

`9e0cb169350002ef42ece37e1b23d5f601fa454322a82447f818e29c9b2eefee`

Review-package checksum SHA-256:

`8bce3796572a48ef3140c34055c251b555d809f404a0a27c9e913d18aceaa606`

Decision-0105 SHA-256:

`3b39b58b1646cdac883f91db49bf003b76571f8814d91cb337b9cff71b91fd35`

## Current review state

Review Package V1 remains:

`BLANK_READY_FOR_INDEPENDENT_HUMAN_REVIEW`

RIAC01-RIAC08 decisions are blank.

Overall review decision is blank.

Reviewer identity is not prepopulated.

Required reviewer role:

`Spec-Technical-Reviewer-1`

## Retired authorization verifiers

Decision-0102 A02 remains permanently retired.

Decision-0104 A02 remains permanently retired.

Decision 0106 does not execute either retired verifier.

## Authorized handoff

Decision 0106 authorizes authoring only of:

`External Independent Human Review Handoff V1`

The handoff must contain an immutable exact Review Package V1 together with
portable source bindings, handoff manifest/checksum closure, Decision-0105,
Decision-0106 authorization evidence, Decision-0106 authorization-verifier
final output and consumption record, and a safe package-local handoff verifier.

The external delivery must include:

1. an immutable ZIP; and
2. a separate editable manual reviewer packet.

Planned immutable ZIP:

`/openbayes/home/19_relation_informed_study_v1_independent_review_handoff.v1.zip`

Planned editable reviewer packet:

`/openbayes/home/19_RIAC01_RIAC08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md`

The editable packet must initially be byte-identical to the immutable blank
review packet:

`a60a89c97292b62303a5a8f9c5fa0c3c2796f964a46cf544232d2d8202124166`

Only the independent human reviewer may populate review decisions, reviewer
notes, identity, and the overall review decision in the external editable copy.

The immutable ZIP and internal review package must not be modified.

## One-time Decision-0106 authorization verifier

The new pre-handoff authorization verifier is initially:

`ACTIVE_UNCONSUMED`

Decision 0106 does not execute it.

It may execute exactly once immediately before external handoff authoring.

Its successful output must be preserved byte-exactly.

After that run it becomes permanently retired and must never be rerun after
handoff authoring begins.

## Explicit non-authorizations

Decision 0106 does not create or synthesize a human-review decision.

It does not authorize:

- Study V1 governance adoption;
- positive existing-Schema-V2 mapping;
- negative mapping impossibility;
- whole-V4 exhaustiveness;
- operational V4-to-V2 mapping;
- operational mapping-contract authoring;
- active Schema V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution; or
- repair.

Prohibited evidence remains prohibited.

## Decision-0106 authorization artifacts

Authorization record SHA-256:

`1573946c7a891f2c63c97594a1598b09992fc7506a6d719e6d15e2a237991188`

One-time pre-handoff verifier SHA-256:

`933e0baa38f0809e71038f8626980b8469ddd6cd6e3279720ad37501e8ece4e9`

Authorization checksum SHA-256:

`1da2366d9c7df19414e915eca3155a12750b196ee99c2da25e2760de14167645`

## Next boundary

`RUN_DECISION_0106_AUTHORIZATION_VERIFIER_ONCE_THEN_AUTHOR_EXTERNAL_INDEPENDENT_REVIEW_HANDOFF_V1`
