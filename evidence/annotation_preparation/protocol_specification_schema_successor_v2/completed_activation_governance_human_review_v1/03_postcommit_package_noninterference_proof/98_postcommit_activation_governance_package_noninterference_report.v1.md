# Activation Governance Package V1 Post-Commit Non-Interference Evidence

## Purpose

The immutable activation-governance package could not contain proof of its own
future Git commit while it was being authored.

This external proof binds the final package commit without modifying the
package.

## Package checkpoint

Commit:

`30840f40d2b76d50ad543f43621641eb43016ad2`

Tree:

`b36673ffb10c440ca5e6da77a9ef28cdb5b8cf9c`

Immediate parent:

`f48fe86761ed5687d7a6e311b5b617363b141b4c`

Parent root tree:

`2569598aa5f5c1d462deecea3e499cbe7625f67b`

## Non-interference result

Package authoring changed exactly 37 repository paths.

Every changed path is under:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_governance_package_v1/`

The checkpoint and parent `config` trees are identical.

Therefore package authoring did not modify:

- Schema V1;
- the approved Schema V2 candidate;
- the frozen V1 hash contract;
- zlib.json;
- libpcap.json.

The checkpoint and parent `documentation` trees are also identical.

Therefore Decision 0019 was not modified.

The active path:

`config/protocol_content_hash_canonicalization.v2.json`

is absent at both checkpoint and parent.

The canonical curl path:

`config/protocol_specifications/curl.json`

is absent at both checkpoint and parent.

## Review consequence

The package contains only review candidates.

It did not activate Schema V2, install the V2 hash contract, supersede Decision
0019, create curl.json, or authorize analyzer/baseline/repair work.
