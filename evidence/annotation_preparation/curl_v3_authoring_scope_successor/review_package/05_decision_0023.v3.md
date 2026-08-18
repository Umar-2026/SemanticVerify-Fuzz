# Decision 0023: curl V3 RR07 Authorization-Boundary Scope Successor

## Status

Author checkpoint decision.

This decision does **not** freeze the curl V3 authoring scope and does **not**
authorize technical protocol working-draft authoring.

## Predecessor

The exact immutable curl V2 source-only authoring-scope successor remains:

- Path: `config/annotation/curl_v2_authoring_scope.v2.json`
- SHA-256: `$ `config/annotation/curl_v2_authoring_scope.v2.json`
- SHA-256: `f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df`
- Author checkpoint commit: `fae56e4f5196fd0460046723ef9d6a4e26234612`
- Author checkpoint tree: `0cb044dd10d48908895425512f5a2e7c1e8633b9`

V2 remains immutable and may not be edited in place.

Its completed independent human review is recorded at repository commit:

`f01c66ca65e08a20114525739a5ed777cb428742`

with tree:

`f04080ca5cf1854209b932c00241904c70e762ab`.

The completed review decision was:

- V2-RR01 through V2-RR06: `PASS`
- V2-RR07: `REVISION_REQUIRED`
- Overall: `REVISION_REQUIRED`

## Reason for V3

The V2 protocol-semantic core was accepted under V2-RR01 through V2-RR06.

V2-RR07 identified one downstream authorization-boundary defect: V2 contained
a conditional field that could be interpreted as allowing technical
working-draft authoring immediately after exact V2 human approval, bypassing
the separately required scope-freeze boundary.

V3 is therefore a minimal immutable successor for this authorization-boundary
correction only.

## V3 change boundary

V3 MUST preserve unchanged:

- the twelve-function curl API surface;
- pinned curl revision
  `68720b4837284335b2d63cb358f8f6ce65f5bc55`;
- frozen scenario manifest and S01-S10 bindings;
- all 21 approved source-evidence files and hashes;
- RR01-RR06-reviewed runtime, cleanup, membership, ownership, and
  multi-perform post-error semantics;
- source-only quarantine and one-hop-expansion prohibition.

V3 changes only governance/provenance metadata required to represent the
reviewer-required authorization sequence.

## Required authorization sequence

The sequence is:

1. independent human review of the exact immutable V3 scope;
2. approval may authorize the separate scope-freeze step only;
3. the exact approved V3 scope must then complete scope freeze;
4. only after completed scope freeze may technical curl working-draft
   authoring be authorized.

Therefore, at this author checkpoint:

- human review completed: NO;
- scope freeze authorized: NO;
- scope frozen: NO;
- technical working-draft authoring authorized: NO;
- canonical curl protocol specification authorized: NO.

## Quarantine

The following remain prohibited:

- generated-driver source inspection;
- selected-sample membership use as protocol evidence;
- raw model response use;
- generated compiler-log semantic inspection;
- gold-label inspection/annotation;
- analyzer implementation/execution;
- baseline execution;
- controlled LLM-review output use;
- repair implementation/output use.

## Exact V3 target

Path:

`config/annotation/curl_v3_authoring_scope.v3.json`

SHA-256:

`ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`

This exact V3 target is an immutable **author checkpoint**, not an approved
scope and not a canonical protocol specification.

## Next boundary

Prepare a new independent-human-review package for the exact immutable V3
scope successor. Human approval must not be synthesized.
