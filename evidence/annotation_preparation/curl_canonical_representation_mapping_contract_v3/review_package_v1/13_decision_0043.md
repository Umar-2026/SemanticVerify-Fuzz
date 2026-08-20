# Decision 0043 — Record curl Mapping Contract V2 Human Review as REVISION_REQUIRED

## Exact human review

SHA-256:

`d688196db67da6cf9e359046ab612e78117fc54c9166122a9523729270df50d5`

Size:

`25643` bytes

Reviewer:

`Abdul Raheem Shahzad`

Confirmation:

`ARS`

Date:

`20 / August / 2026`

## Exact result

`8 PASS / 2 REVISION_REQUIRED / 0 FAIL`

Revision-required items:

`V2-RR01`

`V2-RR08`

Overall decision:

`REVISION_REQUIRED`

The human decision is preserved exactly and is not modified by this record.

## V2 binding

Exact V2 SHA-256:

`f2badbc07895e8baff078a0ce617ceb6ff02d39c7634a9e38b3b8a46a18d811c`

Author checkpoint commit:

`9bc2d448cf2c08a728174090c3d819bbdb9e28f1`

Author checkpoint tree:

`9cb9b34bbeb45cc5916543a04e0f0dad8f54af50`

Exact V2 remains immutable.

## RR01 follow-up fact

The source repository now independently verifies the declared checkpoint
commit, tree, reachability, and exact V2 object bytes.

This supplementary local verification does not retroactively change the
human reviewer's RR01 decision.

A future successor review package must include independently portable Git
object evidence, such as a Git bundle containing the checkpoint and reachable
objects.

## RR08 required correction

A separately authorized successor must explicitly preserve:

- ownership-sensitive semantics;
- return-sensitive semantics;
- the complete approved V4 representation-policy boundary.

Exact V2 must not be edited in place.

## Governance boundary

The reviewer did not reject the scoped frozen-schema insufficiency conclusion,
but exact V2 was not approved.

This decision does not authorize:

- schema-successor authoring;
- schema modification;
- a positive mapping;
- curl.json;
- analyzer implementation or execution;
- baseline execution;
- repair.

## Next boundary

`AUTHORIZE_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V3_SUCCESSOR`
