# Decision 0126 — Authorize V4 Losslessness Requirement Provenance and Binding Resolution Study V1

Status: BOUNDED TECHNICAL EVIDENCE STUDY AUTHORIZED — NOT YET AUTHORED

## Source checkpoint

Decision-0125 commit:

`8c363e4216493d402cedab8e2f73d1b2bd23245a`

Decision-0125 tree:

`28243d46da8a13f5019cbdefaffb01f249a70773`

Governance Adoption V1 Git tree:

`28a768d8dedc6f8614f7f0c23c19674df481a3ac`

Governed Semantic-Unit Carrier / Requirement-Binding Study V1 Git tree:

`3f04237bdc58c2be56e85628de5923b87578a051`

Review-Chain Closure Assessment V1 Git tree:

`18d6b1b77994d6827b878a498e1556487921fda7`

## Governance state

Governance status:

`APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME`

Adopted bounded technical outcome:

`FURTHER_EVIDENCE_REQUIRED`

Review chain:

`PASS_CLOSED`

Study governance adopted:

`YES`

## Why this bounded evidence step is next

The governed Study V1 does not establish sufficient source provenance for
the existing 17 losslessness requirements.

Before carrier admissibility, constructive mapping, impossibility, or schema
successor reasoning can proceed, the existing losslessness requirements must
first be bound to explicit immutable V4 evidence where possible.

## Authorized study

Title:

`V4 Losslessness Requirement Provenance and Binding Resolution Study V1`

The study is limited to the existing 17 losslessness requirements.

Allowed per-requirement classifications:

- `BOUND_EXACT`
- `BOUND_COMPOSITE`
- `UNRESOLVED`

The study must preserve existing requirement IDs and must not invent new
losslessness requirements.

## Allowed study outcomes

`REQUIREMENT_PROVENANCE_RESOLVED`

only if all 17 requirements are BOUND_EXACT or BOUND_COMPOSITE.

Otherwise:

`FURTHER_EVIDENCE_REQUIRED`

## Critical boundary

This study does not authorize reclassification of the existing 18,639
semantic-unit/carrier pairs.

It does not authorize carrier-admissibility conclusions.

It does not authorize construction of a positive mapping witness.

It does not authorize construction of a negative mapping-impossibility proof.

It does not establish whole-V4 admissible-composition exhaustiveness.

## Prohibited evidence

The study must not inspect:

- generated-driver source;
- selected-sample membership;
- raw model responses;
- compiler-log semantic contents;
- gold labels;
- analyzer output;
- baseline output;
- LLM-review output; or
- repair output.

Only already-approved immutable protocol-specification, provenance, schema,
study, governance, and decision evidence may be used.

## Operational non-authorizations

Decision 0126 does not authorize:

- operational mapping;
- active Schema-V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation;
- analyzer execution;
- baseline execution; or
- repair.

## Decision-0126 A02 lifecycle

Decision-0126 A02 begins as:

`ACTIVE_UNCONSUMED`

Decision 0126 does not execute it.

It may execute exactly once immediately before Study V1 authoring.

Its successful final output must be preserved byte-exactly.

After its final successful run it becomes:

`PERMANENTLY_RETIRED`

and must never be rerun.

## Authorization evidence

Authorization record SHA-256:

`db80d52e45c870cba04e402378af6d5b7d3ad8f591e9c70581326fd30e08baec`

One-time pre-study verifier SHA-256:

`007793e7682e26b1405ca0d3fbf19ae7e0b868b8ab003137ef3ff016bbb9964b`

Authorization checksum SHA-256:

`e67e7f13d38e0bc7a6861a650d577fb72ed87ddb6eac8cc2f4f5aea21e22e2d8`

Governed Study V1 requirement-binding assessment SHA-256:

`c8c6fd120f7046ac7e747124821796d1a3686be3dcf6ea40e712b96cdd851ee5`

## Next boundary

`RUN_DECISION_0126_A02_EXACTLY_ONCE_IMMEDIATELY_BEFORE_V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1_AUTHORING`
