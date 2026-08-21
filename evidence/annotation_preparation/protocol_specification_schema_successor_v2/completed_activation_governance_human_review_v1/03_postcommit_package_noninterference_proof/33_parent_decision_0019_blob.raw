# Decision 0019: Canonical Library Protocol-Specification Path Convention

Status: Accepted before creation of the first canonical library-specific protocol specification

Date: 2026-08-16

## Context

Decision 0018 defines deterministic content-hash semantics and distinguishes
working drafts from canonical frozen protocol specifications, but the repository
did not previously declare the authoritative canonical output path for each
library-specific specification.

The zlib source-only semantic review is complete. The exact immutable approved
technical source is `zlib.z-stream.lifecycle.v3` with SHA-256
`8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e`. Canonical finalization has not yet occurred.

A canonical path convention must therefore be fixed before the first final
library-specific specification is created.

## Decision

The authoritative canonical specification root is:

`config/protocol_specifications/`

Exactly one primary canonical path is assigned to each study library:

- zlib: `config/protocol_specifications/zlib.json`
- libpcap: `config/protocol_specifications/libpcap.json`
- curl: `config/protocol_specifications/curl.json`
- cJSON: `config/protocol_specifications/cjson.json`
- libtiff: `config/protocol_specifications/libtiff.json`
- libvpx: `config/protocol_specifications/libvpx.json`
- c-ares: `config/protocol_specifications/c-ares.json`
- lcms: `config/protocol_specifications/lcms.json`

The machine-readable authority for this mapping is:

`config/annotation/canonical_protocol_specification_paths.v1.json`

with SHA-256:

`4c6471d51627997f58b6c6bca833d364edc4c51e5aa7b80d0c34be8d63d19aaa`

## Canonical-artifact rules

A file under the canonical root:

1. is created only after the corresponding source-only specification has
   completed the required independent human review;
2. must validate against the unmodified frozen protocol-specification schema;
3. must use Decision-0018 content-hash semantics;
4. contains the canonical protocol-specification object itself, not an author
   working wrapper, review packet, or review record;
5. is immutable after its canonical freeze;
6. must not be overwritten by a later correction; corrections require a
   separately governed artifact and do not silently alter the frozen primary
   specification.

Working drafts, reviewer packets, binding evidence, and human-review records
remain outside `config/protocol_specifications/`.

## zlib first-finalization binding

For zlib, the canonical path is:

`config/protocol_specifications/zlib.json`

The approved source remains byte-exact SHA-256:

`8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e`

The locked freeze date is:

`2026-08-16`

The prospective Decision-0018 top-level canonical content hash established by
the read-only finalization preflight is:

`3461269e60f3b824bef3c62335d24e9eda5552b1a939bea4c720983e39a25049`

No protocol-semantic change is permitted during canonical finalization. The only
permitted additions to the approved V3 specification object are the already
deferred `freeze_date` and `content_sha256` fields.

This decision does **not** create or freeze the zlib canonical specification.

## Stage boundary

This path decision does not authorize generated-driver source inspection, gold
annotation, analyzer implementation, baseline execution, controlled LLM review,
or repair implementation.

Those stages remain blocked until the governing specification and packet-release
conditions are satisfied.
