# Decision 0132 — Authorize Corrective External-Handoff Authoring Successor After Decision-0130 A02 Failure

## Status

AUTHORIZED — CORRECTIVE EXTERNAL HANDOFF NOT YET AUTHORED

## Predecessor checkpoint

Decision-0130 commit:

`acccf40b8636609e7d98fd3a7d9575529777470d`

Decision-0130 tree:

`b9e9c557cac213f5b1f66354e61db7ccc4a3e725`

Decision-0129 parent commit:

`7ddaaa2e24a065053c132700292023dfaca9c428`

Review Package V1 Git tree:

`35794b450ed9bcde337f4ea4b7de35dd8218cc03`

Failed Decision-0130 External-Handoff Authorization V1 Git tree:

`030017ebc1daaa22b4031a1a4b82533652ab7490`

## Failed Decision-0130 A02

Failed verifier SHA-256:

`ed9ce5e278f1f2b9b49f7d11715faafbbd8e0873b20c961c4173d943e04965f4`

Final output:

`FAIL|DECISION0129_CHECKPOINT`

Failed-output SHA-256:

`4635ef9374bd8edb6278b185635033ce86fa891f387a821d656f626f71dd5a56`

Consumption-sentinel SHA-256:

`a977c957e4e8fc9177147d257c64014cfaba0cc98bbbcd13ba44e1da7dd35bf0`

The verifier executed once, returned failure, and is now:

`PERMANENTLY_RETIRED`

It must never be rerun or patched in place.

## Failure classification

The failure is classified as:

`AUTHORIZATION_VERIFIER_CHECKPOINT_BINDING_DEFECT`

The failed verifier incorrectly required the current pre-handoff HEAD to equal
the Decision-0129 package-author checkpoint.

At legitimate handoff-authoring time, the repository had already advanced to
the committed Decision-0130 authorization checkpoint.

Therefore the correct execution relation is not:

`CURRENT_HEAD == DECISION_0129`

The corrective verifier instead requires:

`CURRENT_HEAD_PARENT == DECISION_0130`

That means the verifier may execute only from the immediate committed
successor authorization checkpoint created by this decision.

## Technical interpretation

The failure does not falsify:

- Review Package V1;
- Study V1;
- the 17 BOUND_EXACT provenance bindings; or
- the bounded `REQUIREMENT_PROVENANCE_RESOLVED` result.

Handoff artifact authoring never began.

No Decision-0131 artifact, handoff directory, external ZIP, or manual reviewer
packet was created by the failed attempt.

## Corrective successor authorization

Decision 0132 authorizes only:

1. a new one-time corrective pre-handoff verifier;
2. verification that the current execution checkpoint is the immediate
   successor of Decision 0130;
3. verification that Review Package V1 remains immutable and valid;
4. verification that failed Decision-0130 A02 remains permanently retired;
5. successor authoring of the external RPR01–RPR08 handoff only after the new
   verifier passes exactly once.

The new corrective verifier does not execute the failed Decision-0130 A02.

## Human-review state

Human review performed:

`NO`

Reviewer decision:

`NONE`

Required reviewer role remains:

`Spec-Technical-Reviewer-1`

Review items remain:

`RPR01–RPR08`

No reviewer decision may be synthesized.

## Retired verifier boundary

The following remain non-runnable:

- Decision-0130 A02;
- Decision-0128 A02;
- Decision-0126 A02;
- all other previously retired A02 verifiers.

## Preserved non-authorizations

Decision 0132 does not authorize:

- human-review decision recording;
- study governance adoption;
- semantic-unit/carrier pair reclassification;
- carrier-admissibility conclusions;
- positive mapping;
- negative mapping impossibility;
- whole-V4 exhaustiveness;
- operational mapping;
- active Schema-V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution;
- repair.

## Corrective verifier lifecycle

Decision-0132 A02 is not executed by this decision.

Initial state:

`ACTIVE_UNCONSUMED`

It may run exactly once immediately before corrective external handoff
authoring. After that single execution it must be permanently retired,
regardless of success or failure.

## Next boundary

`RUN_DECISION_0132_A02_EXACTLY_ONCE_IMMEDIATELY_BEFORE_CORRECTIVE_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_V1_AUTHORING`
