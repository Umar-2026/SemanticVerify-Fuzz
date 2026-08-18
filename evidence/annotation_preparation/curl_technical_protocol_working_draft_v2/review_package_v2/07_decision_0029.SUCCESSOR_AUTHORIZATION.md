# Decision 0029 — curl Technical Working Draft V2 Successor Authorization

## Status

Authorized.

## Basis

The exact curl Technical Protocol Working Draft V1 received an independent
human technical-specification review with overall decision:

`REVISION_REQUIRED`

The completed human-review evidence is bound to SHA-256:

`e253340d540a06cd24af501c569154869ac0324d677995b7266349ba097973cc`

The completed-review record is committed at:

`d8fce56e46a5c8e203aeb12c0fc6abb3945e749b`

with tree:

`d58bdcebb92ed359a1586919f987ea76a5d0a05f`

The exact V1 working draft remains bound to SHA-256:

`80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6`

V1 must remain immutable.

## Authorization

A new source-only curl Technical Protocol Working Draft V2 successor may now
be authored at:

`config/annotation/curl_technical_protocol_working_draft.v2.json`

This authorization permits implementation of only the bounded,
source-grounded corrections required by TS-RR05 through TS-RR14 of the
completed independent human review.

## Frozen boundaries

The frozen twelve-function API surface remains unchanged.

The pinned curl revision remains unchanged.

The frozen V3 source-only authoring scope remains unchanged.

The authoritative scenario manifest remains unchanged.

The approved source-evidence class remains unchanged.

No generated-driver evidence may be used while authoring V2.

Working Draft V1 may not be edited in place.

## Required successor corrections

The V2 successor must:

1. condition `curl_multi_cleanup` release, cleanup-obligation discharge, and
   structural easy-handle detachment on `CURLM_OK`;

2. preserve the multi cleanup obligation and conservative membership state
   after non-`CURLM_OK` cleanup;

3. use exactly four verdict values:
   `VALID`, `VIOLATION-MUST`, `VIOLATION-MAY`, and `UNKNOWN`;

4. move pending, scoped, or explanatory verdict qualifiers to separate
   metadata fields;

5. complete explicit D1, D2, and cleanup-specific D4 mappings, including the
   reviewed NULL-cleanup cases;

6. classify exit with `EXPLICIT_CLEANUP_DUE` after successful explicit
   `curl_global_init` as D5 `VIOLATION-MUST`;

7. represent the documented multi cleanup ordering as a non-enforceable
   recommendation rather than an unconditional MUST violation;

8. classify plain `curl_multi_perform` repetition after a non-`CURLM_OK`
   result without complete documented recovery as D6 `VIOLATION-MUST`;

9. model the complete documented remove-and-re-add recovery sequence;

10. preserve the set-valued runtime post-state after NULL `curl_easy_init`
    and apply verdict joins across feasible states instead of blanket UNKNOWN;

11. classify wrong-multi `curl_multi_remove_handle` as D7
    `VIOLATION-MUST` while preserving the actual membership relation;

12. classify final-reference `curl_global_cleanup` while modeled easy or
    multi resources remain live as state-sensitive D8 `VIOLATION-MUST`.

## Explicit non-authorization

This decision does not authorize canonical `curl.json`.

It does not authorize generated-driver inspection.

It does not authorize selected-sample membership inspection.

It does not authorize gold annotation.

It does not authorize analyzer implementation or execution.

It does not authorize baseline execution.

It does not authorize repair implementation or repair-output inspection.

## Required next review

The exact V2 successor must receive a new independent human technical review.

V2 authoring and its author checkpoint do not themselves authorize
canonicalization.

## Next boundary

`CREATE_CURL_TECHNICAL_WORKING_DRAFT_V2_SUCCESSOR_AUTHOR_CHECKPOINT`
