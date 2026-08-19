# Decision 0041 — Authorize curl Canonical Representation Mapping Contract V2 Successor

## Status

Mapping Contract V1 has completed real independent human technical review.

Review result:

`10 PASS / 0 REVISION_REQUIRED / 0 FAIL`

Overall decision:

`APPROVE_MAPPING_BLOCKER_CONTRACT`

V1 correctly establishes that a lossless transformation from approved curl V4
to the frozen canonical schema is not yet proven.

This decision authorizes a separately versioned V2 mapping-contract successor.

## Exact predecessor

V1 SHA-256:

`31d606f98f2c819291103ba7403214206ccde1d8e5e0e9103f0659c227622257`

Completed V1 human review SHA-256:

`a19d4a6132be417798b027794045227949ea40265e11714543e85ef1c325ad73`

Completed V1 review-record SHA-256:

`b7a8572b3893d83e411c4d79a56682c9b3a47345ed25396df5dcc4556d8a161d`

Completed-review recording commit:

`f9cbcdc75129cc715267885ca1d21197192bdd25`

V1 remains immutable.

## Exact protocol and schema bindings

Approved curl V4 SHA-256:

`e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8`

Frozen canonical schema SHA-256:

`7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34`

Neither may be modified by this authorization.

## Authorized V2 target

`config/annotation/curl_canonical_representation_mapping_contract.v2.json`

V2 authoring may propose a deterministic representation mapping for:

- composite/product states;
- canonical initial state;
- canonical state inventory;
- representational event IDs derived from existing V4 semantics;
- API call, return-condition, branch, and function-exit projections;
- transition IDs and state transitions;
- ownership and membership effects;
- return predicates and path conditions;
- all 64 V4 rules;
- all 3 exit obligations;
- permitted exit states;
- approved provenance;
- forward and reverse semantic accounting.

These are candidate representation decisions only.

They are not approved merely because they are authored.

## Semantic boundary

V2 must not introduce:

- new protocol semantics;
- new API functions;
- new defect categories;
- new machine verdicts;
- semantic protocol events not already grounded in V4;
- new source evidence;
- new evidence classes;
- rule additions or removals;
- rule strengthening or weakening;
- opaque semantic payload packing.

The four verdicts remain exactly:

`VALID / VIOLATION-MUST / VIOLATION-MAY / UNKNOWN`

## Independent review requirement

Any positive V2 mapping must be independently technically reviewed after the
V2 author checkpoint.

No V2 mapping may be used to materialize canonical `curl.json` before that
review is completed and separately recorded.

If V2 demonstrates that the frozen schema is insufficient, schema-successor
work requires separate governance authorization.

## Explicit non-authorization

This decision does not authorize:

- curl.json materialization;
- canonical-schema modification;
- canonical-schema successor creation;
- positive-mapping approval;
- generated-driver inspection;
- selected-sample membership inspection;
- gold annotation;
- analyzer implementation;
- analyzer execution;
- baseline execution;
- repair.

## Next boundary

`AUTHOR_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V2`
