# V1 / Proposed V2 Hash-Canonicalization Contract Comparison

## V1 contract

Path:

`config/protocol_content_hash_canonicalization.v1.json`

SHA-256:

`5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f`

The V1 contract explicitly depends on the V1 protocol specification schema.

It remains frozen and unchanged.

## Proposed V2 contract

Review-candidate package path:

`07_proposed_v2_hash_contract.REVIEW_CANDIDATE.json`

The proposed contract:

- has a distinct V2 contract ID;
- explicitly binds the exact approved Schema V2 SHA-256;
- retains deterministic UTF-8 canonical JSON rules;
- retains top-level self-field exclusion for specification
  `content_sha256`;
- preserves exact-source-byte provenance hashing when the V2 schema exposes
  provenance `content_sha256` carriers;
- does not inherit V1 obligation hashing merely because V1 had obligation
  objects;
- enumerates the actual Schema V2 `content_sha256` carriers from the
  approved schema;
- is a review candidate only and is not installed at the active path.

The active reserved V2 contract path remains absent:

`config/protocol_content_hash_canonicalization.v2.json`

The reviewer must determine whether this explicit V2 contract is sufficiently
complete and unambiguous for future V2 canonical freezes.
