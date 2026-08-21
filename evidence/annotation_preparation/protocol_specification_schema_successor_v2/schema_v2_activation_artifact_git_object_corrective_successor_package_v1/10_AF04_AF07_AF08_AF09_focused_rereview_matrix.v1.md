# Focused AF04/AF07/AF08/AF09 Corrective Rereview Matrix

This rereview is evidence-only.

AF01, AF02, AF03, AF05, AF06, and AF10 remain closed PASS items.

For each open item, the reviewer must use exactly one decision:

PASS
REVISION_REQUIRED
FAIL

## AF04 — Explicit future active dispatch path and deferred creation

Verify from exported original Git commit/tree objects that:

- the checkpoint and parent are authentic under recomputed Git object IDs;
- the exact parent relationship is reproduced;
- `config/protocol_specification_schema_version_dispatch.v1.json` is absent at
  both checkpoint and parent using tree-entry nonexistence, not copied listings.

## AF07 — Historical Decision-0019 immutability and deferred successor adoption

Verify from exported original Git objects that:

- historical Decision 0019 resolves through commit→tree→path→blob chains;
- the same exact blob OID occurs at checkpoint and parent;
- the exported raw blob reproduces its governed SHA-256;
- the corrective package does not adopt the successor.

## AF08 — Approved V2 hash-contract active-form preservation

Verify from exported original Git objects that:

- the approved V2 hash active-form path resolves to the same blob OID at
  checkpoint and parent;
- its raw blob reproduces the governed SHA-256;
- `config/protocol_content_hash_canonicalization.v2.json` is absent at both
  checkpoint and parent.

## AF09 — Core artifact and downstream non-interference

Verify from exported original Git objects that:

- core paths resolve to identical blob OIDs at checkpoint and parent;
- the raw governed blobs reproduce their known SHA-256 values;
- `curl.json` is absent at both commits;
- the checkpoint differs from its parent by exactly 22 changed leaf paths;
- every changed leaf path lies beneath the immutable original
  activation-artifact-finalization package V1 prefix;
- no repository access or Git executable is required by the portable verifier.

## Overall focused rereview

Allowed overall values:

APPROVE_AF04_AF07_AF08_AF09_CORRECTIVE_EVIDENCE
REVISION_REQUIRED
FAIL
