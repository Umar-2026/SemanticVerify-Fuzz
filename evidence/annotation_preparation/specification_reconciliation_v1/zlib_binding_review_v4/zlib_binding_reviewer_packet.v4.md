# zlib V4 Binding-Only Successor Review Packet

## Important scope

This is **not** a new zlib protocol specification version.

No `zlib.z-stream.lifecycle.v4` specification has been created.

The exact technical review target remains the immutable V3 specification:

Repository path:

`evidence/annotation_preparation/specification_reconciliation_v1/zlib_working_draft_v3/zlib_source_only_successor_working_fsm_draft.v3.json`

V3 content SHA-256:

`8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e`

V3 author checkpoint commit:

`b06e52bf66b0d93efd34a27fc5515ca5f70d6e5e`

V3 Git blob object:

`4898445e63de1b4b2fdbe7ca072a1d05258ab0b0`

Reviewer role:

`Spec-Reviewer-1`

Reviewer underlying role:

`Adjudicator-C`

## Prior V3 human review

Completed V3 review SHA-256:

`f4e8e2c74584e6adf7bfb5225f4463631ddc6bdc20173f2528127d3def355606`

V3 review-record SHA-256:

`1848093b51f037e3b48ae3290fcab44e8eccbea702fac1c16f89c67bc6339ba7`

Prior overall decision:

`REVISION_REQUIRED`

Prior V3 decisions:

- V2-RR-01: PASS
- V2-RR-02: REVISION_REQUIRED
- V2-RR-03: PASS
- Evidence completeness: PASS
- Carry-forward integrity: PASS

The only remaining issue was independent verification of the repository-side V3 target binding.

No protocol semantic change was requested.

## V4 binding proof

Proof file:

`04_v3_repository_binding_proof.v1.json`

Proof SHA-256:

`7f93a493e428ebd87d05cf0f854820582d2fcc5c8052141b99b420249982ee41`

Offline verifier:

`05_verify_v3_repository_binding.py`

Verifier SHA-256:

`da74b963d019d9adbd7e90be8d1ad14357abb7946c64325113babd823f790e6b`

The proof contains exactly:

- 1 raw Git commit object
- 5 raw Git tree objects along the V3 repository path
- 1 raw Git blob object, which is the exact V3 JSON target

No unrelated repository blob content is included.

### Raw Git objects

- `commit` `b06e52bf66b0d93efd34a27fc5515ca5f70d6e5e` — `objects/01_commit_b06e52bf66b0d93efd34a27fc5515ca5f70d6e5e.raw` — raw SHA-256 `4afd05f1ef23f6d90e4d1c9d179b02f1b271bfd1ee57a80a27e0e3434518ecb3`
- `tree` `616d5f83f55b08687186580d8f77c5a75d4b6f7b` — `objects/02_tree_616d5f83f55b08687186580d8f77c5a75d4b6f7b.raw` — raw SHA-256 `175dd35134871437abdf190dd992d628bc434a911182a4d89978e72939de29e7`
- `tree` `d1cd86376d7f585d89044027f84f4126eca1f6cf` — `objects/03_tree_d1cd86376d7f585d89044027f84f4126eca1f6cf.raw` — raw SHA-256 `90df1435be4258b9a154c7802f6b02c87126259234f951092f3e76e8162f21db`
- `tree` `9e002955c1c03f5db0afdd046bd484d547315f7f` — `objects/04_tree_9e002955c1c03f5db0afdd046bd484d547315f7f.raw` — raw SHA-256 `695b0675f94e6d73e88397f9ddb1ac410ad6bb99eec4cd1143e7ab7a51c4fdd3`
- `tree` `6f9e3a7b58fdd47dc631ade25f59ba2e9e710ea1` — `objects/05_tree_6f9e3a7b58fdd47dc631ade25f59ba2e9e710ea1.raw` — raw SHA-256 `d8c681d3534340d2daec4c8fd81bf9dcf37a7e40c74cd7b08f10f161815b7c7c`
- `tree` `37c522e8b06526ab40c931b0de4ec88ecb8bd0c8` — `objects/06_tree_37c522e8b06526ab40c931b0de4ec88ecb8bd0c8.raw` — raw SHA-256 `e5a39eb46f79e9b66ebbb31237523d61c6450c9265fc05842a56bcb65fbc21c5`
- `blob` `4898445e63de1b4b2fdbe7ca072a1d05258ab0b0` — `objects/07_blob_4898445e63de1b4b2fdbe7ca072a1d05258ab0b0.raw` — raw SHA-256 `8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e`

## Required independent verification

Before editing this review packet, run from the package root:

`python3 05_verify_v3_repository_binding.py`

The verification must end with:

`BINDING_PROOF_VERIFICATION=PASS`

The verifier independently checks:

1. every supplied raw Git object self-hashes to its declared Git SHA-1 object ID;
2. commit `b06e52bf66b0d93efd34a27fc5515ca5f70d6e5e` names root tree `616d5f83f55b08687186580d8f77c5a75d4b6f7b`;
3. the supplied Git tree chain resolves the exact repository path `evidence/annotation_preparation/specification_reconciliation_v1/zlib_working_draft_v3/zlib_source_only_successor_working_fsm_draft.v3.json`;
4. that path resolves to Git blob `4898445e63de1b4b2fdbe7ca072a1d05258ab0b0`;
5. the raw blob content SHA-256 is `8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e`;
6. package-local `03_zlib_source_only_successor_working_fsm_draft.v3.json` is byte-identical to that repository-bound Git blob.

## V3-RR-01 — repository binding closure

Please record exactly `PASS`, `REVISION_REQUIRED`, or `FAIL`.

Decision:

Notes:

Please confirm whether the supplied minimal Git-object proof allows you to independently establish all of the following without access to the research repository:

- the supplied V3 author commit object self-verifies as `b06e52bf66b0d93efd34a27fc5515ca5f70d6e5e`;
- that commit binds to the supplied root tree;
- the tree-object chain binds the exact repository path to the V3 blob;
- the V3 blob self-verifies as Git object `4898445e63de1b4b2fdbe7ca072a1d05258ab0b0`;
- the V3 blob content SHA-256 is `8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e`;
- the package-local V3 JSON is byte-identical to that repository-bound blob.

## Overall human-review decision

This overall decision applies to the **exact immutable V3 specification** with SHA-256:

`8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e`

Choose exactly one:

- [ ] `APPROVE_EXACT_DRAFT_FOR_FINALIZATION`
- [ ] `REVISION_REQUIRED`
- [ ] `REJECT`

Summary:

Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

## Finalization immutability rule

If the decision is `APPROVE_EXACT_DRAFT_FOR_FINALIZATION`, no protocol semantic change may be introduced.

Canonical finalization must preserve the exact approved V3 semantics. Only the already-deferred `freeze_date` fields and Decision-0018 `content_sha256` fields may be added before canonical validation and freeze.

If the decision is `REVISION_REQUIRED`, the immutable V3 technical target must not be edited in place.
