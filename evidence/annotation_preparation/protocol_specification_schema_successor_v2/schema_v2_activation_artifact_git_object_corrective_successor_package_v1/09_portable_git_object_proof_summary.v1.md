# Portable Raw Git-Object Corrective Evidence Summary

## Scope

This successor addresses only AF04, AF07, AF08, and AF09.

Closed PASS items AF01, AF02, AF03, AF05, AF06, and AF10 are not reopened.

## Historical proof target

Checkpoint commit:

`fa64f7810443d14cd710600cd48ae9f9fedbb04a`

Checkpoint root tree:

`9bb36f1a7d1bb303341f65ded8f0c63796d5c7cd`

Parent commit:

`6eba8a1fc69c0b1146e033b031f5948a245bd84b`

Parent root tree:

`67a80e37f8c94c2c5878f4ddde4da1943e7a5dc6`

The exported checkpoint commit object must identify the exact checkpoint root
tree and exact parent commit. The exported parent commit object must identify
the exact parent root tree.

## Original package change scope

Original activation-artifact-finalization package tree:

`f2e01db7ebe24d48736fa73d05854b0d3e3f2076`

The package path is absent in the parent.

The portable verifier independently compares the exported checkpoint and parent
Merkle trees and must reconstruct exactly 22 changed leaf paths, all underneath:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_artifact_finalization_package_v1/`

## Shared trees

Config tree:

`a86c0022a0d264a1195ed3fcd0b9424b85742c2d`

Documentation tree:

`33adb6befe244d24ddfe90680d7388c98da4de05`

Each is byte/OID-identical between checkpoint and parent.

## Required absence proofs

The exported tree set must independently prove absence at both checkpoint and
parent for:

- config/protocol_content_hash_canonicalization.v2.json
- config/protocol_specification_schema_version_dispatch.v1.json
- config/protocol_specifications/curl.json

## Raw object export

Total exported objects: 41

Commit objects: 2

Tree objects: 17

Blob objects: 22

Every object is stored as raw object-content bytes. The portable verifier
recomputes each Git SHA-1 object identifier as:

`SHA1(type + " " + decimal_length + NUL + raw_content)`

It does not require access to the research repository or to the Git executable.

## Governance boundary

This package is evidence only. It does not activate Schema V2, install either
active artifact, adopt the Decision-0019 successor, authorize positive
V4-to-V2 mapping, create curl.json, or authorize analyzer, baseline, or repair
activity.
