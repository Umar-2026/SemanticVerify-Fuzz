# Decision 0038 — Authorize Canonical curl Specification from Approved V4

## Status

Canonical curl specification materialization is authorized from one exact
approved source only:

`config/annotation/curl_technical_protocol_working_draft.v4.json`

Approved V4 SHA-256:

`e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8`

Approved V4 size:

`41033` bytes

V4 must remain immutable.

## Human-review authorization basis

The completed independent human review recorded at commit:

`ceeafb3600531f89a832df874ab28e81823f7f7c`

and tree:

`cdc9806d776c4222d4142f86fdf17ae86e1cfeec`

contains:

`12 PASS / 0 REVISION_REQUIRED / 0 FAIL`

Overall decision:

`APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION`

Completed human-review SHA-256:

`074814c04922f7cbc5fa41ef460cbde74dcb32529c09ef5752cf1d0f511f2aed`

## Authorized target

The only authorized canonical target is:

`config/protocol_specifications/curl.json`

The target must not already exist.

Overwrite is not authorized.

Editing V4 in place is not authorized.

## Authorized transformation boundary

Canonical metadata transformation is authorized.

Protocol-rule semantic change is not authorized.

Protocol-rule addition is not authorized.

Protocol-rule removal is not authorized.

API-surface change is not authorized.

Defect-taxonomy change is not authorized.

Machine-verdict-contract change is not authorized.

Source-evidence change is not authorized.

New evidence classes are not authorized.

Synthetic protocol events are not authorized.

All ten approved V4 protocol-semantic containers must be preserved exactly in
JSON semantics.

Easy-handle rules must remain `21`.

Multi-handle rules must remain `29`.

Frozen curl API surface must remain twelve functions.

Machine verdicts must remain exactly:

- `VALID`
- `VIOLATION-MUST`
- `VIOLATION-MAY`
- `UNKNOWN`

Pinned curl commit remains:

`68720b4837284335b2d63cb358f8f6ce65f5bc55`

Pinned curl tree remains:

`e23d273aeb073c04aa5b073b35c9fde16979c896`

Evidence class remains:

`PREAPPROVED_SOURCE_ONLY`

Approved source-file count remains:

`21`

## Required inspection before materialization

Before `curl.json` is created, the repository's existing canonical
specification conventions must be inspected read-only using:

- `config/protocol_specifications/zlib.json`
- `config/protocol_specifications/libpcap.json`

This inspection is required to determine the exact canonical metadata,
finalization, freeze-manifest, and checksum conventions.

It may not change V4 protocol semantics.

## Required canonicalization evidence

Actual materialization must separately produce and verify:

- exact V4-to-canonical protocol-semantic equality;
- canonical curl file identity;
- canonical finalization record;
- canonical freeze manifest;
- canonical checksum manifest;
- exact repository worktree/staging scope.

## Current state

Canonical curl specification authorization:

`YES`

Canonical `curl.json` created:

`NO`

Canonical `curl.json` frozen:

`NO`

This authorization does not authorize generated-driver inspection, selected
sample inspection, gold annotation, analyzer implementation or execution,
baseline execution, or repair.

## Stage-specific verifier rule

The verifier created with this decision is pre-materialization only because it
checks that `curl.json` does not yet exist.

After legitimate materialization, later stages must validate this authorization
record directly rather than reusing the pre-materialization absence assertion.

## Next boundary

`INSPECT_CANONICAL_SPECIFICATION_CONVENTIONS_BEFORE_CURL_MATERIALIZATION`
