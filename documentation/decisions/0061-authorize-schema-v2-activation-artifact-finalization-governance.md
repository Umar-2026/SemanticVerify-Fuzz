# Decision 0061 — Authorize Schema V2 Activation-Artifact Finalization Governance

## Status

Authoring authorization only.

This decision does not activate Schema V2.

## Basis

Decision 0060 records independent human approval of the exact active-form
Schema V2 hash contract.

That hash-contract active form requires no further transformation.

The remaining activation blockers are:

1. the reviewed version-dispatch policy still has internal status
   `REVIEW_CANDIDATE_NOT_ACTIVE`;
2. the reviewed Decision-0019 successor remains explicitly marked as a
   non-active review candidate.

## Version-dispatch finalization

Reviewed source SHA-256:

`5a91a9938af7029edff6b91b8b624b2f0712680d49fad3abd1be29e649944bce`

A future active dispatch artifact is reserved at:

`config/protocol_specification_schema_version_dispatch.v1.json`

The finalization package may derive an active-form dispatch review candidate
by changing exactly one JSON scalar:

`$.status`

from:

`REVIEW_CANDIDATE_NOT_ACTIVE`

to:

`ACTIVE_UPON_EXPLICIT_SCHEMA_V2_ACTIVATION_DECISION`

No other JSON key or value may change.

Expected active-form dispatch SHA-256:

`67a96c3eda8de95fa6c55342d5d33ea725e16cea8af21fcb4f3b8945b9d4eeee`

Expected size:

`1334` bytes

Expected canonical-JSON SHA-256:

`2333c2521db84ddb347b23a956acebdc6ad713c61cc890b76d7b04d0b8d2fc7f`

## Decision-0019 successor finalization

Reviewed source SHA-256:

`8665163eb5d4f7a8718ba3ed2d3973ba928fea85789c23696599a2d6ea02bbb3`

Reviewed source size:

`2158` bytes

Decision 0019 remains historically immutable.

The finalization package may derive a successor active-form review candidate
using exactly three transformations:

1. remove the `REVIEW CANDIDATE —` title prefix;
2. replace the candidate-only status line;
3. replace the exact two-line candidate-only activation paragraph with the
   explicitly activation-gated final-form paragraph.

All other successor text must remain byte-preserved.

Expected finalized successor SHA-256:

`a96f9d8b6811a9f9170a18de9ff8be6f80a3704b9e6a13c59fbb88e423bec3bb`

Expected size:

`2203` bytes

The finalized successor does not become operative merely by being authored or
reviewed. A later explicit reviewed Schema V2 activation decision must adopt
the exact finalized text by SHA-256.

## Approved V2 hash form

Human-approved active-form SHA-256:

`37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9`

It requires no further transformation and remains uninstalled.

## Required review

The finalization package must undergo independent AF01-AF10 human review.

## Authorized package

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_artifact_finalization_package_v1`

## Explicit non-authorization

This decision does not:

- create or install the active V2 hash contract;
- create or install the active version-dispatch policy;
- activate Schema V2;
- adopt the Decision-0019 successor;
- modify Decision 0019;
- modify either reviewed source candidate;
- modify the approved V2 hash-contract active form;
- define or authorize positive V4-to-V2 mapping;
- create curl.json;
- authorize analyzer implementation/execution;
- authorize baseline execution;
- authorize repair.

## Next boundary

`AUTHOR_SCHEMA_V2_ACTIVATION_ARTIFACT_FINALIZATION_PACKAGE_V1`
