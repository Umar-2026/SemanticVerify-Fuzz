# curl V3 Source-Only Authoring-Scope Successor Independent Review Packet

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

Repository target:

`config/annotation/curl\\\_v3\\\_authoring\\\_scope.v3.json`

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

* V2-RR01 through V2-RR06: `PASS`
* V2-RR07: `REVISION\\\_REQUIRED`
* overall: `REVISION\\\_REQUIRED`

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

* all twelve in-scope curl functions;
* pinned curl revision
`68720b4837284335b2d63cb358f8f6ce65f5bc55`;
* scenario manifest and S01-S10 bindings;
* all 21 approved source-evidence entries and hashes;
* global runtime-reference semantics;
* explicit global-cleanup-obligation semantics;
* `curl\\\_multi\\\_perform()` post-error semantics;
* global-cleanup/D4 reconciliation;
* easy/multi membership and ownership semantics;
* repeated remove/add semantics;
* cleanup-order normative-strength treatment;
* source-only quarantine;
* disabled one-hop API expansion.

No protocol-semantic change is authorized by this V3 successor.

## Review quarantine

Do not consult:

* generated fuzz-driver source;
* selected-sample membership;
* raw model responses;
* compiler-log semantic contents;
* gold labels;
* analyzer output;
* baseline output;
* controlled LLM-review output;
* repair output;
* corpus prevalence/performance feedback.

## Mandatory review decisions

For each item choose exactly one:

`PASS`

`REVISION\\\_REQUIRED`

`FAIL`

### V3-RR01 — Exact immutable target and predecessor binding

Decision: REVISION\_REQUIRED



Notes: I manually reviewed the exact V3 target and predecessor evidence supplied in

the external handoff.



The package-local V3 copies are byte-identical and produce SHA-256

ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb.

The supplied V3 bytes correspond to the recorded Git blob

931c24cc46c99f23ee352455d3e8c93e57e63401.



The exact V2 predecessor copies remain preserved at SHA-256

f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df.

V2 is consistently recorded as immutable and not editable in place.



The completed V2 review is preserved at SHA-256

cbd09e4596d95943ce30295cf3fef5369905049397336ea818fa57f8ec593f4f.

Its decision record is preserved at SHA-256

6a063e01d67588934d6eb03da8461a3e708c88f993379d0bd980ea69c1d0e54a,

and its checksum manifest matches

f0cb4a7b3e44675b886d0da137d75655b08d81605bf5f66c49efe99051300273.



Decision 0023 matches its recorded SHA-256

c774bb667930ef9ceaedc5ca5d25e88d57da3ffefa10de639ef6a20f7d2271d1.

However, Decision 0023 contains a malformed duplicate predecessor SHA line.



The external handoff does not include Git commit/tree objects, repository

metadata, or a Git bundle from which author commit

7de6fc01797ae68cbd64406b850a3198f71cc702 can be independently resolved to

tree c5f96b844e5803cccd04c9f64a55754dc6c77e20 and the exact V3 target blob.

The external verifier also does not perform this Git commit/tree check.



The exact V3 SHA-256 and Git blob were independently confirmed. The

exact V2 predecessor bytes, completed V2 review, and Decision 0023 hash

binding were also confirmed. However, the handoff contains no Git

repository, Git bundle, or commit/tree objects from which the claimed

V3 author commit and tree can be independently resolved. Their values

are internally consistent across the included manifests but are not

independently verifiable from the ZIP. Therefore, the mandatory

commit/tree confirmation remains incomplete.

Confirm:

V3-RR01 therefore cannot pass from the supplied handoff alone. A corrected

immutable handoff must include independently resolvable Git commit/tree

evidence and a corrected Decision 0023.

* V3 SHA-256, Git blob, author commit and tree are exact;
* exact V2 predecessor is preserved;
* V2 remains immutable;
* completed V2 review and Decision 0023 are correctly bound.

### V3-RR02 — RR07 authorization-boundary correction

Decision: PASS

Notes: Manually inspected the exact V3 scope artifact. V3 explicitly represents the required sequence: independent human review → scope-freeze authorization → completed exact-V3 scope freeze → technical working-draft authorization. Human approval authorizes only the separate scope-freeze step. Technical working-draft authoring is explicitly not authorized immediately after human approval and becomes eligible only after the approved exact V3 scope completes its separate freeze boundary. No contradictory direct-authorization path was found.



Confirm that V3 explicitly represents:

human review
→ scope-freeze authorization
→ completed V3 scope freeze
→ technical working-draft authorization.

Confirm that human approval alone does NOT directly authorize technical
working-draft authoring.



### V3-RR03 — Preservation of V2-RR01 through V2-RR06 semantics

Decision: PASS

Notes: Independently compared the actual included V2 and V3 scope artifacts.

The twelve-function API surface and pinned curl revision

68720b4837284335b2d63cb358f8f6ce65f5bc55 are identical. The

S01-S10 scenario manifest and bindings, all 21 source-evidence

entries and hashes, resource-state semantics, easy/multi membership

and ownership rules, cleanup semantics, curl\_multi\_perform()

post-error handling, and normative-strength decisions remain

unchanged. The observed changes are limited to V3 successor metadata,

predecessor binding, and the RR07 authorization-boundary correction.

No protocol-semantic change was found.



Confirm that the twelve-function API surface, pinned revision, scenario
manifest, 21-source evidence set, resource-state semantics, membership,
ownership, cleanup semantics, post-error handling, and normative-strength
decisions remain unchanged.

### V3-RR04 — Current downstream authorization and quarantine state

V3-RR04 — Current downstream authorization and quarantine state

Decision: PASS

Notes: Independently inspected the actual V3 scope artifact and its bound

authorization records. At this checkpoint, human review is incomplete,

scope freeze is unauthorized, and the scope remains unfrozen. Technical

working-draft authoring and canonical curl specification finalization

are unauthorized. Generated-driver inspection, gold annotation,

analyzer implementation/execution, baseline execution, and repair

remain unauthorized and quarantined. No conflicting downstream

authorization was found.



Confirm that at this checkpoint:

* human review is incomplete;
* scope freeze is unauthorized;
* scope is unfrozen;
* technical working-draft authoring is unauthorized;
* canonical curl specification is unauthorized;
* generated-driver inspection is unauthorized;
* gold annotation is unauthorized;
* analyzer implementation/execution is unauthorized;
* baseline execution is unauthorized;
* repair is unauthorized.



## Overall decision

Choose exactly one:

Overall decision: REVISION\_REQUIRED



Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad 

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 18 / August / 2026



Notes: V3-RR01 is REVISION\_REQUIRED. The exact V3 SHA-256 and independently

computed Git blob were confirmed, and the exact immutable V2

predecessor and completed V2 review records are correctly hash-bound.

However, the handoff does not contain independently resolvable Git

objects, repository metadata, or a Git bundle sufficient to verify the

claimed V3 author commit and tree. Decision 0023 also contains a

malformed duplicate predecessor SHA-256 line.



V3-RR02, V3-RR03, and V3-RR04 are PASS. The RR07 authorization-boundary

correction is correctly represented, the V2-RR01 through V2-RR06

semantic surface is preserved, and all downstream activities remain

unauthorized and quarantined.



The exact V3 scope is therefore not approved for freeze. The immutable

V3 author checkpoint must not be edited in place. A corrected immutable

successor/handoff with independently verifiable commit/tree evidence

and a corrected Decision 0023 record is required.

## Post-review boundary

If and only if a real independent human reviewer chooses
`APPROVE\\\_EXACT\\\_V3\\\_SCOPE\\\_FOR\\\_FREEZE`, the next repository operation may prepare
the separate exact-V3 scope-freeze step.

That approval does NOT itself authorize technical working-draft authoring.

Technical working-draft authoring remains prohibited until the approved exact
V3 scope subsequently completes its separate freeze boundary.

Review completion must be recorded in new artifacts.

Do not edit the immutable V3 author checkpoint or immutable package copy.

