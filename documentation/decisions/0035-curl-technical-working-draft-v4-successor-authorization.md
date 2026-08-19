# Decision 0035 — Authorize curl Technical Working Draft V4 Successor

## Status

Authorized for immutable V4 successor authoring preparation.

This decision does not create Working Draft V4.

## Exact immutable predecessor

Working Draft V3:

`config/annotation/curl_technical_protocol_working_draft.v3.json`

SHA-256:

`2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2`

Size:

`41330` bytes

Exact V3 must remain immutable.

## Completed V3 human review

Completed-review commit:

`0f6625753452944bbedeab66a77a4098a6e349a9`

Completed-review tree:

`a822ec4504071e0edbdc8b77c0eda8ea3974cdbc`

Completed-review SHA-256:

`9a15b13cea29bcbcbfff349c9b9bcb113a9d9a4e01afe03727d7be8dbd87c327`

Overall decision:

`REVISION_REQUIRED`

Revision-required items:

- V3-RR02
- V3-RR12

## Accepted V3 technical semantics

The independent reviewer accepted V3-RR03 through V3-RR11.

V4 therefore must preserve the accepted protocol-rule semantics.

No protocol-rule semantic change is authorized by this decision.

The ten PASS review items are to remain preserved:

- V3-RR01
- V3-RR03
- V3-RR04
- V3-RR05
- V3-RR06
- V3-RR07
- V3-RR08
- V3-RR09
- V3-RR10
- V3-RR11

## Authorized V4 draft correction scope

V4 may correct only review-required internal metadata and successor-governance
bindings, including:

1. internal purpose text;
2. `governance.working_draft_version`;
3. predecessor version/path/SHA/size and immutable-predecessor binding;
4. completed V3 human-review binding;
5. successor-authorization binding;
6. stale `v1_in_place_edit_authorized`-era operative metadata;
7. version-specific `explicit_non_claims`;
8. operative successor-resolution metadata.

V4 must bind exact immutable V3 as predecessor.

V4 must bind the completed V3 human review.

V4 must represent V3-RR02 and V3-RR12 as the reason for the successor.

## Review-package portability correction

The next V4 independent-review package must use platform-independent path
comparison.

Logical relative source paths remain unchanged.

The same approved 21 pinned source files and hashes remain unchanged.

Path separator normalization must not alter source-evidence semantics or hashes.

A fresh V4-bound traceability record, author checkpoint, package manifest,
verifier, and checksums are required before another independent review.

## Preserved boundaries

The twelve-function curl API surface remains unchanged.

Pinned curl commit:

`68720b4837284335b2d63cb358f8f6ce65f5bc55`

Pinned curl tree:

`e23d273aeb073c04aa5b073b35c9fde16979c896`

Evidence class remains:

`PREAPPROVED_SOURCE_ONLY`

Approved source-file count remains:

`21`

Machine verdicts remain exactly:

- `VALID`
- `VIOLATION-MUST`
- `VIOLATION-MAY`
- `UNKNOWN`

No synthetic protocol event may be invented.

## Prohibited evidence

V4 authoring must not use:

- generated-driver source;
- selected-sample membership;
- raw model responses;
- generated-driver compiler-log semantic content;
- gold labels;
- analyzer output;
- baseline output;
- LLM-review output;
- repair output.

## Explicit non-authorization

This decision does not authorize canonical `curl.json`.

This decision does not authorize generated-driver inspection.

This decision does not authorize selected-sample membership inspection.

This decision does not authorize gold annotation.

This decision does not authorize analyzer implementation or execution.

This decision does not authorize baseline execution.

This decision does not authorize repair.

## Required immediate next step

Before V4 is authored, inspect the exact V3 internal metadata structure
read-only so that stale V1/V2 fields can be corrected without guessing field
locations or changing accepted protocol semantics.

## Next boundary

`INSPECT_V3_METADATA_FOR_EXACT_BOUNDED_V4_AUTHORING`
