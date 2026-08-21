# Decision 0063 — Authorize AF04/AF07/AF08/AF09 Git-Object Corrective Successor

Status: AUTHORIZED FOR EVIDENCE-PACKAGE AUTHORING ONLY — NO ACTIVATION

## Basis

Decision 0062 recorded the independent human review of the Schema V2
activation-artifact finalization package.

The result was:

- 6 PASS
- 4 REVISION_REQUIRED
- 0 FAIL

Open review items are exactly:

`AF04, AF07, AF08, AF09`

The reviewer did not request changes to the reviewed dispatch or
Decision-0019-successor transformations. The deficiency is portable provenance
evidence only.

## Authorization

This decision authorizes authoring one evidence-only corrective successor
package containing original raw Git objects and a repository-independent
verifier sufficient to address AF04, AF07, AF08, and AF09.

The package must satisfy GE01 through GE10 in:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_artifact_git_object_corrective_successor_authorization/01_git_object_corrective_successor_authorization.v1.json`

The proof target is historical package checkpoint:

`fa64f7810443d14cd710600cd48ae9f9fedbb04a`

with exact parent:

`6eba8a1fc69c0b1146e033b031f5948a245bd84b`

and checkpoint root tree:

`9bb36f1a7d1bb303341f65ded8f0c63796d5c7cd`

The corrective package must provide portable cryptographic proof of:

- original checkpoint and parent commit object IDs;
- checkpoint-parent relationship;
- root-tree bindings;
- nested Merkle tree path bindings;
- exact 22-path package-only change scope;
- historical Decision-0019 immutability;
- approved V2 hash active-form preservation;
- reserved active V2 hash path absence;
- reserved active version-dispatch path absence;
- curl.json absence;
- unchanged core-artifact blob bindings.

## Closed review items

AF01, AF02, AF03, AF05, AF06, and AF10 remain PASS and are not reopened.

## Non-authorization

This decision does not authorize:

- modification of the original activation-artifact finalization package;
- modification of the completed human review;
- changes to either reviewed artifact transformation;
- installation of the active V2 hash contract;
- installation of the active version-dispatch policy;
- Schema V2 activation;
- adoption of the Decision-0019 successor;
- modification of Decision 0019;
- positive V4-to-V2 mapping;
- creation of curl.json;
- analyzer implementation or execution;
- baseline execution; or
- repair.

The corrective successor requires independent focused human rereview before
any later activation decision.

## Next boundary

`AUTHOR_AF04_AF07_AF08_AF09_PORTABLE_RAW_GIT_OBJECT_CORRECTIVE_SUCCESSOR_PACKAGE_V1`
