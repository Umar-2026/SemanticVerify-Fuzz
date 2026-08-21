# Package V2 Checkpoint/Parent Non-Interference Evidence

## Checkpoint

Review Package V2 commit:

`75dd1d9c5a3d01d72b76f9d76e8abb56113187e5`

Root tree:

`d2bc2301cea0ef87aeae7b37278ba1d5440aae57`

Immediate parent:

`bf6cf53d54c105353906f02c6fa117668b635eae`

Parent root tree:

`1c120d2385a58630ba617f0b51a676eb38b63dd4`

## Schema V2

Expected SHA-256:

`c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956`

Git blob at checkpoint and parent:

`245fc02f538c21cff5de25f4a6a3c297e915e40f`

The checkpoint and parent `config` and `config/schemas` trees are
identical. Therefore Review Package V2 authoring did not modify Schema V2.

## zlib

Expected SHA-256:

`f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1`

Git blob at checkpoint and parent:

`5e4d5744f9da0b1a2723d4ec834f9ad03b7e64ea`

## libpcap

Expected SHA-256:

`b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73`

Git blob at checkpoint and parent:

`ce4ea9b2d97c1ca570b004dc1c4869eb067f8c5d`

The checkpoint and parent `config/protocol_specifications` trees are
identical. Therefore Review Package V2 authoring did not modify zlib.json or
libpcap.json.

## Changed-path scope

The portable tree-chain evidence establishes that the Package V2 commit
changes only the newly added:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/review_package_v2/`

subtree.

All sibling entries outside that subtree remain identical through the
checkpoint/parent tree chain.

## Portable verification

Run:

`python3 14_package_v2_checkpoint_parent_git_proof/99_verify_package_v2_checkpoint_parent_proof.v1.py`

This verifier uses only the raw original Git commit/tree/blob objects included
inside this package.

## Package V3 post-commit boundary

This report proves non-interference for Review Package V2.

Review Package V3's own future Git commit is necessarily unknown while the V3
package bytes are being authored.

After V3 is committed, a separate external read-only post-commit proof must be
created and supplied to the reviewer. That external proof must not modify this
immutable Package V3.
