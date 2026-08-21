# Decision 0059 — Authorize Active-Form Schema V2 Hash-Contract Finalization Governance

## Status

Authoring authorization only.

This decision does not install an active V2 hash contract and does not activate
Schema V2.

## Basis

The exact activation-governance package has received independent human
approval and that approval is recorded by Decision 0058.

The exact reviewed Schema V2 hash-contract candidate is:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_governance_package_v1/07_proposed_v2_hash_contract.REVIEW_CANDIDATE.json`

SHA-256:

`8fa63b0faea168e7dcc7701d94704d408dbd8d22e5d17d6c83cc3ab90095aab0`

Size:

`3126` bytes

Its internal status is:

`REVIEW_CANDIDATE_NOT_ACTIVE`

and its candidate-only draft-boundary fields remain true.

Therefore direct byte-identical installation at:

`config/protocol_content_hash_canonicalization.v2.json`

would produce an internally contradictory active artifact.

## Finalization rule

This decision authorizes authoring of a separate review package containing one
deterministically derived active-form candidate.

Exactly three scalar values may differ from the human-reviewed source
candidate:

1. `$.status`

   from:

   `REVIEW_CANDIDATE_NOT_ACTIVE`

   to:

   `FROZEN_BEFORE_FIRST_SCHEMA_V2_CANONICAL_SPECIFICATION`

2. `$.draft_boundary.review_candidate_is_not_active_contract`

   from `true` to `false`;

3. `$.draft_boundary.active_path_must_not_be_created_until_later_reviewed_activation_decision`

   from `true` to `false`.

No top-level key may be added or removed.

No other value may change.

## Target status rationale

The V1 historical value
`FROZEN_BEFORE_FIRST_LIBRARY_SPECIFICATION_DRAFT` is not copied literally,
because library protocol drafting has already occurred.

The proposed active-form status instead describes the relevant V2 boundary:

`FROZEN_BEFORE_FIRST_SCHEMA_V2_CANONICAL_SPECIFICATION`

No Schema-V2 canonical protocol specification currently exists.

The status itself must receive independent review before any installation.

## Deterministic expected active-form bytes

Expected review-candidate file SHA-256:

`37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9`

Expected file size:

`3154` bytes

Expected canonical-JSON SHA-256:

`8f90f681c8942471ee05afc8d1fbb12d8208858163bc7f59695c26a82d48c4f6`

These values are derived in memory from the exact reviewed source candidate
using only the three authorized scalar changes.

## Mandatory preservation boundary

The finalization candidate must preserve exactly:

- contract ID;
- schema version;
- reason;
- all dependencies;
- canonical JSON rules;
- all Schema V2 content_sha256 carrier accounting;
- specification content-hash semantics;
- provenance content-hash semantics;
- computation order;
- prohibited effects;
- the remaining non-candidate-specific draft-boundary semantics.

## Human review requirements

The finalization package must independently review HF01 through HF08:

- HF01 exact source binding;
- HF02 exact three-scalar delta;
- HF03 target-status semantic accuracy;
- HF04 unchanged hash/canonicalization semantics;
- HF05 unchanged approved Schema V2 dependency;
- HF06 unchanged V1 contract and frozen V1 artifacts;
- HF07 active-path installation remains deferred;
- HF08 no mapping/curl/analyzer/baseline/repair side effect.

## Authorized package

The authorized authoring target is:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_hash_contract_finalization_package_v1`

The package must include:

- exact source reviewed contract;
- exact deterministically derived active-form review candidate;
- machine-readable semantic-diff proof;
- exact expected file/canonical hashes;
- required immutable dependency bindings;
- blank independent human-review packet;
- self-contained verifier;
- checksum manifest.

## Explicit non-authorization

This decision does not authorize:

- creation of `config/protocol_content_hash_canonicalization.v2.json`;
- installation of the active-form candidate;
- Schema V2 activation;
- adoption of the Decision-0019 successor;
- activation of version dispatch;
- modification of the source reviewed V2 hash candidate;
- modification of Schema V2;
- modification of the V1 hash contract;
- modification or migration of zlib/libpcap;
- positive V4-to-V2 mapping;
- curl.json creation;
- analyzer implementation or execution;
- baseline execution;
- repair.

## Next boundary

`AUTHOR_ACTIVE_SCHEMA_V2_HASH_CONTRACT_FINALIZATION_PACKAGE_V1`
