# Decision 0117 — Authorize SUCR01 Corrective Portable Source Evidence Successor Package V2

Status: CORRECTIVE SUCCESSOR PACKAGE V2 AUTHORING AUTHORIZED — PACKAGE NOT YET AUTHORED

## Source checkpoint

Decision-0116 commit:

`5a55c0afe194a8bfb016f856ce9d1b97df5e5d87`

Decision-0116 tree:

`6e2632bdeb8e5b73f09a2d108177509f8624750b`

Completed Human Review V1 Git tree:

`e8178b937ab376faca698d35cc57d6e3785fbbb5`

Original Review Package V1 Git tree:

`e3d3c93a723b9d4c085a81ec0d0be11df852601a`

Current Semantic-Unit Carrier Study V1 Git tree:

`3f04237bdc58c2be56e85628de5923b87578a051`

## Original independent review state

SUCR01:

`REVISION_REQUIRED`

SUCR02-SUCR08:

`PASS`

Original overall review:

`REVISION_REQUIRED`

The original review remains immutable.

Decision 0117 does not rewrite the original overall result as approval.

Review-chain closure remains:

`NO`

## Authorized corrective scope

Decision 0117 authorizes only:

`SUCR01 — SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY`

No SUCR02-SUCR08 technical revision is authorized or required by this decision.

Their original PASS findings are carried forward as historical independent
review findings.

## Required portable source evidence

Corrective Successor Package V2 must contain independently portable and
resolvable byte-exact or Git-tree-exact evidence for:

1. active Schema V2;
2. Semantic-Role Relation artifact;
3. Semantic-Role Traceability artifact;
4. prior Relation-Informed Exhaustive Admissible Composition Study V1;
5. governance-adoption evidence for that prior Study V1; and
6. Decision-0109 governance-adoption decision.

Resolved Relation artifact:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_semantic_role_relation_formalization_v1/02_v4_field_class_to_schema_v2_property_path_relation.v1.json`

SHA-256:

`239e6492faca3bb6da0c79abdb980470e2ea76690fc1f081562ccdbf7f303a32`

Resolved Traceability artifact:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_semantic_role_relation_formalization_v1/03_v4_semantic_unit_context_and_leaf_traceability.v1.json`

SHA-256:

`6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4`

Active Schema V2 SHA-256:

`c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956`

Prior Study V1 Git tree:

`bb55744db442f718daa56f8f38733e3ef4819b1a`

Governance-Adoption V1 Git tree:

`b5e2ccf604fc874cfa64e4831b66c22f669ade78`

Decision-0109 SHA-256:

`1728f262195cd0f72bc744e566150a94c3fa28f1a6410150c5788bd24a8b5237`

## Corrective-package invariants

Corrective Successor Package V2 must:

- preserve original Review Package V1 byte-exactly;
- preserve the completed original human review byte-exactly;
- bind Decision-0116 completed-review evidence;
- include the required missing source evidence without semantic modification;
- include a portable source-binding manifest;
- include a portable-resolvability manifest;
- provide a safe post-authoring verifier;
- provide checksum closure;
- preserve original overall REVISION_REQUIRED;
- preserve SUCR02-SUCR08 original PASS findings;
- avoid any author-synthesized focused rereview; and
- remain an author-candidate corrective package until independent focused
  SUCR01 rereview occurs.

Expected post-authoring package state:

`AUTHOR_CANDIDATE_AWAITING_FOCUSED_SUCR01_REREVIEW`

## Decision-0117 A02 lifecycle

Decision-0117 A02 begins as:

`ACTIVE_UNCONSUMED`

Decision 0117 does not execute it.

It may execute exactly once immediately before Corrective Successor Package
V2 authoring.

Its successful final output must be preserved byte-exactly.

After that final run it becomes:

`PERMANENTLY_RETIRED`

It must never be rerun.

## Focused rereview boundary

Decision 0117 does not authorize the focused SUCR01 rereview itself.

That requires a separate later authorization after Corrective Successor
Package V2 has been authored, verified, committed, and frozen.

## Technical state

Study V1 remains:

`AUTHOR_CANDIDATE`

Bounded technical outcome remains:

`FURTHER_EVIDENCE_REQUIRED`

Study governance adoption remains:

`NO`

No positive existing-Schema-V2 mapping witness is proven.

No negative existing-Schema-V2 mapping impossibility is proven.

Whole-V4 admissible-composition exhaustiveness remains unproven.

## Explicit non-authorizations

Decision 0117 does not authorize:

- operational V4-to-V2 mapping;
- operational mapping-contract authoring;
- active Schema-V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation;
- analyzer execution;
- baseline execution;
- repair;
- focused SUCR01 human rereview;
- review-chain closure; or
- governance adoption.

## Retired verifier state

The following remain permanently retired:

- Decision-0102 A02
- Decision-0104 A02
- Decision-0106 A02
- Decision-0110 A02
- Decision-0112 A02
- Decision-0114 A02

They must not be executed.

## Authorization evidence

Authorization record SHA-256:

`9a2131455bef7a8029492265e08db460c9725ab86022f9345bba21d4c3d3b6c5`

One-time pre-package authorization verifier SHA-256:

`b0116a3e10c38819d9bb6415a41aaa29a7d39a90363e40e2cbe2ed4b61acd646`

Authorization checksum SHA-256:

`dbde06d9f13d97db5d8f38ab9e84c1ca5ee4edd6db2bc0759408ec84624ff301`

## Next boundary

`RUN_DECISION_0117_A02_EXACTLY_ONCE_IMMEDIATELY_BEFORE_SUCR01_CORRECTIVE_SUCCESSOR_PACKAGE_V2_AUTHORING`
