# Decision 0044 — Authorize curl Mapping Contract V3 Corrective Successor

## Basis

Exact V2 human review outcome:

`8 PASS / 2 REVISION_REQUIRED / 0 FAIL`

Overall:

`REVISION_REQUIRED`

Revision-required items:

`V2-RR01`

`V2-RR08`

Exact V2 remains immutable.

## V3 corrective scope

V3 may correct only the independently identified successor requirements.

For RR08, V3 must explicitly require preservation of:

- ownership-sensitive semantics;
- return-sensitive semantics;
- complete exact V4 representation-policy semantics.

The complete exact V4 representation-policy boundary must be
machine-checkably bound and accounted for.

All previously required membership-sensitive, path-sensitive, set-valued,
UNKNOWN, four-verdict, forward-accounting, reverse-accounting, 10-container,
64-rule, and 3-exit-obligation requirements remain in force.

## RR01 review-package requirement

The future V3 independent-review handoff must contain portable Git-object
evidence sufficient for an external reviewer to verify the V3 author
checkpoint commit, tree, and exact V3 bytes at the repository path.

The V2 human RR01 decision remains REVISION_REQUIRED and is not retroactively
changed.

## Non-authorization

This decision does not authorize:

- canonical-schema successor authoring;
- canonical-schema modification;
- positive-mapping approval;
- curl.json;
- analyzer implementation or execution;
- baseline execution;
- repair.

## Next boundary

`AUTHOR_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V3`
