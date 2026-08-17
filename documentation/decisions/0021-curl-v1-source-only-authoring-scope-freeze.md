# Decision 0021: curl V1 Source-Only Authoring Scope Freeze

Status: Accepted before curl V1 working-draft authoring

Date: 2026-08-17

## Context

The canonical zlib and libpcap protocol specifications are frozen. Under the
source-only recovery protocol, the curl protocol scope must be fixed before any
generated curl driver source is inspected.

The frozen scenario manifest is:

`config/generation/scenario_bindings.80.v10.json`

SHA-256:

`a7ab361e6e2d41d9051e48bc7626f0be37c1df9ec35f788a9a019b010054a2db`

The pinned curl revision is:

`68720b4837284335b2d63cb358f8f6ce65f5bc55`

No generated driver, selected-sample membership, gold label, analyzer output,
baseline output, LLM-review output, or repair output was used to define this
scope.

## Scenario-derived API boundary

The strict union of model-visible required feature symbols across curl
scenarios S01-S10 contains exactly eight functions:

- `curl_easy_init()`;
- `curl_easy_setopt()`;
- `curl_easy_perform()`;
- `curl_easy_reset()`;
- `curl_global_init()`;
- `curl_multi_init()`;
- `curl_multi_add_handle()`; and
- `curl_multi_perform()`.

Four additional functions are included only as bounded lifecycle/cleanup
closure:

- `curl_easy_cleanup()`;
- `curl_global_cleanup()`;
- `curl_multi_remove_handle()`; and
- `curl_multi_cleanup()`.

Therefore curl V1 freezes exactly twelve protocol-bearing functions.

One-hop manpage references do not expand the frozen scope.

## Normative scope

The normative machine-readable curl V1 authoring scope is:

`config/annotation/curl_v1_authoring_scope.v1.json`

SHA-256:

`d8e020cc14bd6c8ea9d679ba0f736bdce6098763d9b8ac0c0f95edaf8d9fd9c7`

Three principal resource components are modeled:

1. caller-owned `CURL *` easy handles;
2. caller-owned `CURLM *` multi handles; and
3. bounded explicit global initialization state for scenario S10.

Easy-to-multi membership is modeled separately from ownership.

## Easy-handle lifecycle

A non-null `curl_easy_init()` result creates a caller-owned easy handle and
requires eventual `curl_easy_cleanup()`.

`curl_easy_setopt()` is an in-scope live-handle operation, but curl V1 does not
expand into the complete CURLOPT-specific pointer-lifetime surface.

`curl_easy_perform()` may be used repeatedly on an appropriate live easy
handle. A transfer failure does not itself release the handle or automatically
constitute a protocol violation.

`curl_easy_reset()` resets options toward their post-init defaults but does not
release the easy handle.

Use of an easy handle after `curl_easy_cleanup()` is illegal.

## Multi/easy composition

A non-null `curl_multi_init()` creates a caller-owned multi handle and carries
an eventual `curl_multi_cleanup()` obligation.

Adding an easy handle to a multi handle does not transfer ownership of the easy
handle.

While an easy handle remains attached to a multi handle,
`curl_easy_perform()` must not be used on that easy handle.

After the easy handle is removed from the multi handle, direct easy-interface
use is again permitted.

`curl_multi_cleanup()` does not free individual easy handles. For attached
handles being torn down, the bounded cleanup discipline preserves the
source-documented order:

`curl_multi_remove_handle()` -> `curl_easy_cleanup()` -> `curl_multi_cleanup()`.

## Global initialization boundary

Pinned documentation states that global initialization precedes ordinary
libcurl use, while `curl_easy_init()` also documents automatic global
initialization if the application has not explicitly called
`curl_global_init()`.

Therefore absence of an explicit `curl_global_init()` is not automatically a
curl V1 violation for ordinary easy-interface scenarios.

The explicit global-state obligation is bounded to frozen scenario S10:
successful explicit `curl_global_init()` carries a matching
`curl_global_cleanup()` obligation after libcurl use is complete.

Broader repeated-global-init/reference-count behavior is outside curl V1.

## Explicit boundaries

Duplicate-handle, getinfo, option-introspection, alternate global-init,
multi polling/waiting/socket APIs and the broader libcurl API surface remain
outside V1.

The full CURLOPT-specific ownership/pointer-lifetime surface is not
automatically included.

Application-owned output buffers are not modeled as libcurl-owned resources.

`curl_off_t` is a type and is not an additional protocol function.

Arbitrary non-protocol bugs remain outside the D1-D8 protocol taxonomy.

## Multi-resource representation requirement

curl V1 contains independent global, easy and multi resource components plus
easy-to-multi membership.

Because the canonical protocol schema provides a single `initial_state`, the
working draft must use a schema-valid combined/product-state representation, or
another independently reviewable schema-approved representation, so that all
modeled local initial conditions are structurally represented and reachable.

No synthetic API event may be invented merely to connect independent resource
components.

## Stage boundary

This freeze authorizes source-only curl V1 working-draft authoring from the
frozen scope and approved pinned evidence only.

Generated-driver inspection, selected-sample use as protocol evidence, gold
annotation, analyzer implementation, baseline execution, LLM-review execution
and repair remain blocked.
