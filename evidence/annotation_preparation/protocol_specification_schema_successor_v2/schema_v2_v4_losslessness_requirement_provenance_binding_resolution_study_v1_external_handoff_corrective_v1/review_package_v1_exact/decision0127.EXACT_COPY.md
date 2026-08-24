# Decision 0127 — Record V4 Losslessness Requirement Provenance and Binding Resolution Study V1

Status: AUTHOR_CANDIDATE — INDEPENDENT HUMAN REVIEW REQUIRED

## Decision-0126 checkpoint

Commit:

`bb6383a1c3c2a7400ab466bde6c4e8de00e809ff`

Tree:

`0b54fd699bcecda2348c58be6f3dd1c32dca09a8`

Authorization Git tree:

`d4dc111090a7c71b9c5b899d2f1ccb13fea18eeb`

## Corrected requirement-identity basis

The existing 17 V4 losslessness requirements are identified by the exact
keys of the canonical V4 losslessness object.

Canonical losslessness-object SHA-256:

`c869079bfbd395b479e2dd8f2f1bcc31aabeababe0e24fc1542c6d35d210602e`

The independently stored 17-name lists are exact-order equal.

The canonical 17-key object is value-equal across:

1. curl canonical representation mapping contract V4;
2. Schema-V2 successor design-record snapshot; and
3. residual-losslessness proof snapshot.

The verified design-record canonical hash path is:

`$.approved_v4_basis.losslessness_contract_canonical_sha256`

The verified design-record mapping-contract path is:

`$.approved_v4_basis.mapping_contract_sha256`

## Binding accounting

- Requirement count: `17`
- BOUND_EXACT: `17`
- BOUND_COMPOSITE: `0`
- UNRESOLVED: `0`

Author-candidate outcome:

`REQUIREMENT_PROVENANCE_RESOLVED`

## Meaning and limitation

This result resolves requirement identity and immutable source provenance.

It does not prove that existing Schema V2 represents the 17 requirements
losslessly.

It does not prove a positive existing-V2 mapping.

It does not prove negative existing-V2 mapping impossibility.

It does not establish whole-V4 admissible-composition exhaustiveness.

The historical index-only unresolved requirement records remain immutable
historical evidence. No independent semantic equivalence between those
placeholder indices and canonical requirement-name order is claimed.

## Preserved state

No semantic-unit/carrier pair was reclassified.

The existing 18,639 pair state was not modified.

No carrier-admissibility conclusion was made.

No positive mapping witness or negative impossibility proof was constructed.

## Operational non-authorizations

Decision 0127 does not authorize:

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

Final successful output SHA-256:

`aa7beb98d50f322d00069fb00fa75eb0d33a581a1b07bc8a7fe3343f08459e34`

Final output size:

`864`

State:

`PERMANENTLY_RETIRED`

It must never be rerun.

## Study evidence

Binding matrix SHA-256:

`a03a1c0d5e43a83d74534ed772503f46b3118cec9351f4324ac03ebeb51ae4ac`

Source inventory SHA-256:

`96bb1dc5a0d25621dc1736b3637a34a6af4c846464e6a8c1dc5535226d1e0853`

Accounting SHA-256:

`44fad8ce51ec19d3f87349460d44a867b3349b3c4f17130b994a8b603913bc07`

Study report SHA-256:

`d86afc4b0b229b1db35c5c423565c9ef6af00992856d0b9e458333b7a153b13d`

Decision-0126 A02 exact-output SHA-256:

`aa7beb98d50f322d00069fb00fa75eb0d33a581a1b07bc8a7fe3343f08459e34`

A02 consumption-record SHA-256:

`9b922a3b4c3b0553964a1644645c0ccf6ab7468742855860524f1918aab2f5f8`

Safe verifier SHA-256:

`8e95ccffa89eba415bcf12e8c47e69b68486d181dde249dcb2c21b31223f177d`

Checksum closure SHA-256:

`a1e5f4ffad170b471f48a9cdd668bdac1582afc66bb6a635be4a1d626a7919f6`

## Next boundary

`SEPARATELY_AUTHORIZE_INDEPENDENT_HUMAN_REVIEW_OF_V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1`
