# curl V3 Source-Only Authoring-Scope Successor Independent Review Packet

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

Repository target:

`config/annotation/curl_v3_authoring_scope.v3.json`

Exact V3 scope SHA-256:

`ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`

Author checkpoint commit:

`7de6fc01797ae68cbd64406b850a3198f71cc702`

Author checkpoint tree:

`c5f96b844e5803cccd04c9f64a55754dc6c77e20`

Git blob:

`931c24cc46c99f23ee352455d3e8c93e57e63401`

This V3 artifact is an immutable author checkpoint.

It is NOT a frozen curl authoring scope.

It is NOT a technical protocol working draft.

It is NOT a canonical curl protocol specification.

Human review completed: `NO`

Scope freeze authorized: `NO`

Technical working-draft authoring authorized: `NO`

## Why V3 exists

The completed independent V2 review recorded:

- V2-RR01 through V2-RR06: `PASS`
- V2-RR07: `REVISION_REQUIRED`
- overall: `REVISION_REQUIRED`

V2-RR07 identified a downstream authorization-boundary defect.

V2 could be interpreted as authorizing technical working-draft authoring
immediately after human approval, bypassing the separately required completed
scope-freeze boundary.

V2 remains immutable and was not edited in place.

V3 is a minimal successor intended to correct that authorization boundary only.

## Required V3 sequence

The required sequence is:

1. independent human review of the exact immutable V3 scope;
2. approval may authorize the separate scope-freeze step only;
3. the exact approved V3 scope must complete scope freeze;
4. only after completed scope freeze may technical working-draft authoring
   become authorized.

Human approval alone MUST NOT directly authorize technical working-draft
authoring.

## Frozen semantic surface that must remain unchanged

Verify that V3 preserves from V2:

- all twelve in-scope curl functions;
- pinned curl revision
  `68720b4837284335b2d63cb358f8f6ce65f5bc55`;
- scenario manifest and S01-S10 bindings;
- all 21 approved source-evidence entries and hashes;
- global runtime-reference semantics;
- explicit global-cleanup-obligation semantics;
- `curl_multi_perform()` post-error semantics;
- global-cleanup/D4 reconciliation;
- easy/multi membership and ownership semantics;
- repeated remove/add semantics;
- cleanup-order normative-strength treatment;
- source-only quarantine;
- disabled one-hop API expansion.

No protocol-semantic change is authorized by this V3 successor.

## Review quarantine

Do not consult:

- generated fuzz-driver source;
- selected-sample membership;
- raw model responses;
- compiler-log semantic contents;
- gold labels;
- analyzer output;
- baseline output;
- controlled LLM-review output;
- repair output;
- corpus prevalence/performance feedback.

## Mandatory review decisions

For each item choose exactly one:

`PASS`

`REVISION_REQUIRED`

`FAIL`

### V3-RR01 — Exact immutable target and predecessor binding

Decision:

Notes:

Confirm:

- V3 SHA-256, Git blob, author commit and tree are exact;
- exact V2 predecessor is preserved;
- V2 remains immutable;
- completed V2 review and Decision 0023 are correctly bound.

### V3-RR02 — RR07 authorization-boundary correction

Decision:

Notes:

Confirm that V3 explicitly represents:

human review
→ scope-freeze authorization
→ completed V3 scope freeze
→ technical working-draft authorization.

Confirm that human approval alone does NOT directly authorize technical
working-draft authoring.

### V3-RR03 — Preservation of V2-RR01 through V2-RR06 semantics

Decision:

Notes:

Confirm that the twelve-function API surface, pinned revision, scenario
manifest, 21-source evidence set, resource-state semantics, membership,
ownership, cleanup semantics, post-error handling, and normative-strength
decisions remain unchanged.

### V3-RR04 — Current downstream authorization and quarantine state

Decision:

Notes:

Confirm that at this checkpoint:

- human review is incomplete;
- scope freeze is unauthorized;
- scope is unfrozen;
- technical working-draft authoring is unauthorized;
- canonical curl specification is unauthorized;
- generated-driver inspection is unauthorized;
- gold annotation is unauthorized;
- analyzer implementation/execution is unauthorized;
- baseline execution is unauthorized;
- repair is unauthorized.

## Overall decision

Choose exactly one:

`APPROVE_EXACT_V3_SCOPE_FOR_FREEZE`

`REVISION_REQUIRED`

`FAIL`

Overall decision:


Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

Notes:


## Post-review boundary

If and only if a real independent human reviewer chooses
`APPROVE_EXACT_V3_SCOPE_FOR_FREEZE`, the next repository operation may prepare
the separate exact-V3 scope-freeze step.

That approval does NOT itself authorize technical working-draft authoring.

Technical working-draft authoring remains prohibited until the approved exact
V3 scope subsequently completes its separate freeze boundary.

Review completion must be recorded in new artifacts.

Do not edit the immutable V3 author checkpoint or immutable package copy.
