# Decision 0057 — Authorize Schema V2 Activation-Governance Package Authoring

## Basis

Decision 0056 records final independent human technical approval of the exact
Schema V2 candidate.

Approved candidate:

`config/schemas/protocol_specification.v2.schema.json`

SHA-256:

`c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956`

Size:

`43030` bytes

Git blob:

`245fc02f538c21cff5de25f4a6a3c297e915e40f`

Final Schema V2 review state:

`10 PASS / 0 REVISION_REQUIRED / 0 FAIL`

This approval does not itself activate Schema V2.

## Existing canonical governance

Decision 0019 remains an immutable historical decision.

Path:

`documentation/decisions/0019-canonical-library-protocol-specification-path-convention.md`

SHA-256:

`50e273ecb6af838bc83d2499a2ed3a71607bc7c0cf8d74bd2622b56c2fefafa9`

Decision 0019 currently requires canonical artifacts under
`config/protocol_specifications/` to validate against the unmodified frozen
protocol-specification schema.

That existing frozen-schema binding was established in the V1 governance
environment and has not yet been amended or superseded for Schema V2.

Decision 0019 must not be edited in place.

Any V2 activation must therefore use a new explicit successor/amendment
decision.

## Existing V1 hash contract

The frozen V1 hash/canonicalization contract remains:

`config/protocol_content_hash_canonicalization.v1.json`

SHA-256:

`5fb33fe68520e906a6fcc325e998229eecd94d44ed7fe2bcb0012d6b18f3211f`

It explicitly depends on:

`config/schemas/protocol_specification.schema.json`

SHA-256:

`7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34`

Therefore the V1 hash contract must not be silently reused as a Schema V2
hash contract.

## Frozen V1 canonical artifacts

The following remain immutable and must not be migrated during Schema V2
activation governance:

### zlib

SHA-256:

`f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1`

Git blob:

`5e4d5744f9da0b1a2723d4ec834f9ad03b7e64ea`

### libpcap

SHA-256:

`b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73`

Git blob:

`ce4ea9b2d97c1ca570b004dc1c4869eb067f8c5d`

Schema V2 activation must support coexistence rather than rewriting these
frozen V1 artifacts.

## Authorization

This decision authorizes authoring of exactly one activation-governance
package at:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_governance_package_v1`

This is an **authoring authorization only**.

It does not activate Schema V2.

## Mandatory activation-governance requirements

The package must resolve all nine requirements:

1. **AG01 — Activation scope.** Define exact Schema V2 activation scope
   without modifying the approved candidate.

2. **AG02 — Decision 0019 successor.** Propose an explicit successor or
   amendment decision enabling version-dispatched canonical validation.
   Decision 0019 itself remains immutable.

3. **AG03 — V2 hash contract.** Define a Schema V2-specific content-hash and
   canonicalization contract. The frozen V1 contract must not be silently
   reused.

4. **AG04 — V1 non-migration.** Preserve frozen zlib and libpcap byte-for-byte
   and Git-blob-for-Git-blob.

5. **AG05 — Version dispatch.** Define coexistence such that V1 artifacts
   remain governed by the V1 schema/hash contract, while future V2 artifacts
   may use the approved V2 schema and separately approved V2 hash contract
   only after activation.

6. **AG06 — Mapping separation.** Schema V2 activation must remain separate
   from any positive V4-to-V2 semantic mapping contract.

7. **AG07 — No curl materialization.** Activation governance must not create
   `config/protocol_specifications/curl.json`.

8. **AG08 — No downstream execution authorization.** Activation governance
   must not authorize analyzer implementation/execution, baseline execution,
   or repair.

9. **AG09 — Independent review before activation.** The activation-governance
   package must undergo independent review/verification before any later
   decision marks Schema V2 active.

## Schema V2 hash-contract candidate

The eventual reserved active path is:

`config/protocol_content_hash_canonicalization.v2.json`

This decision does not create that file and does not activate a V2 hash
contract.

The activation-governance package may contain a review candidate for the V2
hash contract, but that candidate must explicitly bind the exact approved
Schema V2 SHA-256:

`c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956`

## Required package contents

The activation-governance package must contain at least:

- exact Schema V2 candidate binding;
- exact Decision 0019 binding and conflict analysis;
- frozen V1 schema/hash-contract bindings;
- frozen zlib/libpcap byte and Git-object bindings;
- proposed Decision 0019 successor/amendment text;
- proposed V1/V2 version-dispatch policy;
- proposed Schema V2 hash/canonicalization contract candidate;
- proof that the V2 hash candidate binds the exact approved Schema V2;
- proof that frozen V1 behavior/artifacts remain unchanged;
- explicit activation criteria and non-activation conditions;
- explicit separation from positive V4-to-V2 mapping;
- explicit no-curl/no-analyzer/no-baseline/no-repair boundaries;
- blank independent human-review packet;
- self-contained verifier and checksum manifest.

## Non-authorization

This decision does not authorize:

- modification of the approved Schema V2 candidate;
- modification of the V1 schema;
- modification of the V1 hash contract;
- modification of Decision 0019 in place;
- migration of zlib or libpcap;
- creation of an active V2 hash contract;
- Schema V2 activation;
- immediate supersession of Decision 0019;
- positive V4-to-V2 mapping;
- curl.json creation;
- analyzer implementation or execution;
- baseline execution;
- repair.

## Next boundary

`AUTHOR_SCHEMA_V2_ACTIVATION_GOVERNANCE_PACKAGE_V1`
