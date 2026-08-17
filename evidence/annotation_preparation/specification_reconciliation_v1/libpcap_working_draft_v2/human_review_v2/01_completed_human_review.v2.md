# libpcap V2 RR-08 Successor Independent Review Packet

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

Repository target:

`evidence/annotation\_preparation/specification\_reconciliation\_v1/libpcap\_working\_draft\_v2/libpcap\_source\_only\_working\_fsm\_draft.v2.json`

Exact V2 draft SHA-256:

`3ee8459dd2cff6dc8f5dd538a0f8d54a9ceda740d5ea7d977a0a9d34093c3221`

Author checkpoint commit:

`342ea862912e53b1ebec70f2e53e57db10d7846c`

Author checkpoint tree:

`1e8253e52be0a0d41fbe436c738d0011a02e33fa`

Git blob for exact V2 target:

`2f5782b744edc3e7684b459241cf079a77da1ab7`

Package-local byte-identical copy:

`evidence/annotation\_preparation/specification\_reconciliation\_v1/libpcap\_working\_draft\_v2/review\_package/03\_libpcap\_source\_only\_working\_fsm\_draft.v2.json`

This V2 artifact is an immutable author checkpoint. It is **not** a
canonical frozen libpcap protocol specification.

## Why V2 exists

The V1 human review recorded `REVISION\_REQUIRED` only for `RR-08`.

The blocking representation problem was that V1 used one schema-level
`initial\_state = NO\_HANDLE`, while the independently modeled BPF resource
used local fresh state `NO\_VALID\_PROGRAM`. Under the single declared
transition relation, the BPF lifecycle was not structurally reachable.

V2 addresses that representation defect by using the existing schema's
string-state representation as a direct product:

`PCAP\_STATE\_\_BPF\_\_BPF\_STATE`

The V2 schema-level initial state is:

`NO\_HANDLE\_\_BPF\_\_NO\_VALID\_PROGRAM`

There are 15 product states and 50 lifted transitions.

## Review quarantine

Use only:

* the exact immutable V2 target;
* the V1 completed human review and V1 decision record included in this package;
* the frozen libpcap authoring scope;
* the approved pinned source evidence referenced by V2 provenance;
* the protocol specification schema;
* Decision 0020 and already-frozen protocol governance materials.

Do **not** consult:

* generated fuzz-driver source;
* selected-sample membership;
* raw model responses;
* generated compiler-log semantic contents;
* gold labels;
* analyzer output;
* baseline output;
* controlled LLM-review output;
* repair output;
* corpus prevalence or performance feedback;
* failure-prompted post-hoc evidence outside the approved pinned source set.

## V2 structural facts

* Specification ID: `libpcap.live-capture.lifecycle.v2`
* States: `15`
* Events: `10`
* Transitions: `50`
* Core obligations: `20`
* Provenance items: `17`
* Initial state: `NO\_HANDLE\_\_BPF\_\_NO\_VALID\_PROGRAM`
* Schema changed from V1: `NO`
* Synthetic protocol events added: `NO`
* Canonical specification frozen: `NO`
* Human review completed: `NO`
* Freeze dates/content hashes: `DEFERRED`

## Mandatory V2 review checks

For every section, record exactly one of:

`PASS`

`REVISION\_REQUIRED`

`FAIL`

### V2-RR01 — Exact predecessor and immutable-target binding

\### V2-RR01 — Exact predecessor and immutable-target binding

Decision: `REVISION\_REQUIRED`

Notes:

The supplied V2 draft computes to SHA-256

`3ee8459dd2cff6dc8f5dd538a0f8d54a9ceda740d5ea7d977a0a9d34093c3221`

and Git blob

`2f5782b744edc3e7684b459241cf079a77da1ab7`. Both values exactly match the

review packet and included manifests.

The included V1 completed review and decision record match their declared

hashes. They consistently identify the exact V1 target SHA-256

`2a2723eba8cac78c004b846fc1fe71e786730c9aeecc6800e81ee6f2e318687a`,

record the overall V1 decision as `REVISION\_REQUIRED`, and identify `RR-08`

as the blocking item. The V2 records consistently declare V2 as the authorized

RR-08-only successor.

However, the ZIP contains neither the original Git repository nor a Git

bundle containing author commit

`342ea862912e53b1ebec70f2e53e57db10d7846c` and its tree. The bundled verifier

fails with `fatal: not a git repository`. Therefore the author commit/tree

cannot be independently resolved, and it cannot be independently demonstrated

from the ZIP that the declared commit contains the reviewed blob.

The repository-target V2 file and exact V1 predecessor draft bytes are also not

separately included, so repository/package byte identity and the exact

predecessor-byte relationship cannot be independently reproduced.

The supplied hashes and binding records are internally consistent, but the

mandatory commit and exact-predecessor bindings are not fully verifiable from

the ZIP alone. A Git bundle/original repository and exact V1 predecessor bytes

are required before this item can be changed to `PASS`.

Verify that the reviewed bytes are exactly the V2 author checkpoint identified
by SHA-256 `3ee8459dd2cff6dc8f5dd538a0f8d54a9ceda740d5ea7d977a0a9d34093c3221`, Git blob
`2f5782b744edc3e7684b459241cf079a77da1ab7`, and author commit `342ea862912e53b1ebec70f2e53e57db10d7846c`.

Also verify that V2 is a successor to the exact V1 reviewed target and that the
recorded V1 outcome was `REVISION\_REQUIRED` with blocking item `RR-08`.

### V2-RR02 — Product-state representation closes RR-08

\### V2-RR02 — Product-state representation closes RR-08

Decision: `PASS`

Notes:

The V2 state list contains exactly the Cartesian product of the five PCAP

local states:



\* `NO\_HANDLE`

\* `UNACTIVATED\_OWNED`

\* `ACTIVE\_OWNED`

\* `ACTIVATION\_FAILED\_OWNED`

\* `CLOSED`



and the three BPF local states:



\* `NO\_VALID\_PROGRAM`

\* `COMPILED\_OWNED`

\* `FREED\_OR\_EMPTY`



This produces exactly `5 × 3 = 15` product states. All 15 expected

`PCAP\_STATE\_\_BPF\_\_BPF\_STATE` combinations are present exactly once. No product

state is missing, duplicated, or outside the declared Cartesian product.



The single schema-level initial state is exactly:



`NO\_HANDLE\_\_BPF\_\_NO\_VALID\_PROGRAM`



Unlike V1, this state structurally initializes both resource components. The

PCAP component begins in `NO\_HANDLE`, while the BPF component simultaneously

begins in `NO\_VALID\_PROGRAM`; the BPF initial condition no longer depends on

reviewer-visible prose outside the structured state relation.



The BPF lifecycle is now structurally reachable from the initial product state.

For example:



1\. `T01\_\_BPF\_\_NO\_VALID\_PROGRAM` moves successful handle creation to

&#x20;  `UNACTIVATED\_OWNED\_\_BPF\_\_NO\_VALID\_PROGRAM`.

2\. `T04\_\_BPF\_\_NO\_VALID\_PROGRAM` moves successful activation to

&#x20;  `ACTIVE\_OWNED\_\_BPF\_\_NO\_VALID\_PROGRAM`.

3\. `T09\_\_PCAP\_\_ACTIVE\_OWNED` moves successful compilation to

&#x20;  `ACTIVE\_OWNED\_\_BPF\_\_COMPILED\_OWNED`.

4\. `T12\_\_PCAP\_\_ACTIVE\_OWNED` moves program release to

&#x20;  `ACTIVE\_OWNED\_\_BPF\_\_FREED\_OR\_EMPTY`.



Thus `NO\_VALID\_PROGRAM`, `COMPILED\_OWNED`, and `FREED\_OR\_EMPTY` participate in

the same machine-readable state relation that begins at the top-level initial

state. This removes the V1 defect in which the BPF lifecycle had no

schema-level reachable starting condition.

The correction uses the unchanged string-state schema and introduces no

synthetic initialization event. Cross-resource validity conditions remain

enforced by the existing return predicates and obligations; transition

presence alone is not treated as a validity verdict.

Therefore the 15-state direct-product representation adequately closes the

original V1 RR-08 structural reachability defect.

Verify that the 15 V2 states represent the Cartesian product of the five
`pcap\_t` local states and three BPF-program local states.

Verify that the single schema-level initial state
`NO\_HANDLE\_\_BPF\_\_NO\_VALID\_PROGRAM` structurally initializes both resource
components and removes the V1 reachability defect.

### V2-RR03 — PCAP transition lifting

\### V2-RR03 — PCAP transition lifting

Decision: `PASS`

Notes:

The V1 PCAP-side transition family consists of ten base transitions:



\* T01 — successful `pcap\_create`

\* T02 — failed `pcap\_create`

\* T03 — successful pre-activation configuration

\* T04 — successful/warning `pcap\_activate`

\* T05 — failed `pcap\_activate`

\* T06 — `pcap\_datalink`

\* T07 — successful packet-producing `pcap\_next\_ex`

\* T08 — non-packet-producing `pcap\_next\_ex`

\* T11 — `pcap\_setfilter`

\* T14 — `pcap\_close`



Each of these ten base transitions is represented by exactly three V2 lifted

variants, one for each BPF state:



\* `NO\_VALID\_PROGRAM`

\* `COMPILED\_OWNED`

\* `FREED\_OR\_EMPTY`



This produces exactly `10 × 3 = 30` PCAP-side lifted transitions. No expected

variant is missing, duplicated, or assigned to an incorrect base transition.

The transition IDs exactly match the expansion map recorded in the V2 author

checkpoint manifest.

For every lifted PCAP transition, the BPF component appearing in each

`from\_states` entry is identical to the BPF component in the corresponding

`to\_states` entry. Only the PCAP component follows the local transition.



For example:



\* `T01\_\_BPF\_\_COMPILED\_OWNED` changes

&#x20; `NO\_HANDLE\_\_BPF\_\_COMPILED\_OWNED` to

&#x20; `UNACTIVATED\_OWNED\_\_BPF\_\_COMPILED\_OWNED`.

\* `T04\_\_BPF\_\_FREED\_OR\_EMPTY` changes

&#x20; `UNACTIVATED\_OWNED\_\_BPF\_\_FREED\_OR\_EMPTY` to

&#x20; `ACTIVE\_OWNED\_\_BPF\_\_FREED\_OR\_EMPTY`.

\* `T14\_\_BPF\_\_NO\_VALID\_PROGRAM` changes each live owned PCAP state to

&#x20; `CLOSED\_\_BPF\_\_NO\_VALID\_PROGRAM` without changing the BPF component.



Within each three-variant transition group, the event ID, return predicate,

ownership effect, and projected PCAP from/to states are identical:



\* T01 retains `E01\_PCAP\_CREATE`, non-NULL return, and `ACQUIRE`.

\* T02 retains `E01\_PCAP\_CREATE`, NULL return, and `NONE`.

\* T03 retains `E02\_PRE\_ACTIVATION\_CONFIG`, successful configuration, and

&#x20; `NONE`.

\* T04 retains `E03\_PCAP\_ACTIVATE`, return >= 0, and `NONE`.

\* T05 retains `E03\_PCAP\_ACTIVATE`, return < 0, and `NONE`.

\* T06 retains `E04\_PCAP\_DATALINK` and `NONE`.

\* T07 retains `E05\_PCAP\_NEXT\_EX`, return 1, and `BORROW`.

\* T08 retains `E05\_PCAP\_NEXT\_EX`, return != 1, and `NONE`.

\* T11 retains `E07\_PCAP\_SETFILTER` and `NONE`.

\* T14 retains `E09\_PCAP\_CLOSE` and `RELEASE`.



These projected semantics agree with the included completed V1 review and the

approved pinned source evidence. Lifting does not alter creation, activation,

packet-borrow, filter-installation, or close semantics.

Cross-resource prerequisites remain governed by the unchanged obligations and

return predicates. The existence of a lifted variant does not by itself make

a call valid in every product state.

Therefore the PCAP transition family is completely and consistently lifted

across all three BPF states while preserving the untouched BPF component and

the approved substantive transition semantics.

Exact Git/predecessor byte binding remains the separate V2-RR01 issue and does

not change this transition-lifting result.Decision:

Notes:



Verify that each V1 `pcap\_t` transition is lifted across all three BPF states.

For every lifted transition, verify that only the PCAP component changes and
the BPF component is held fixed.

Verify that event ID, return predicate, and ownership effect remain equivalent
to the V1 transition being lifted.

### V2-RR04 — BPF transition lifting

Decision: PASS

Notes:

Manual inspection confirms that all four V1 BPF base transitions—T09, T10, T12, and T13—are each lifted across all five PCAP states: NO\_HANDLE, UNACTIVATED\_OWNED, ACTIVE\_OWNED, ACTIVATION\_FAILED\_OWNED, and CLOSED. This produces the expected 20 BPF-lifted transitions.

For every lifted variant, the PCAP component remains unchanged while only the BPF component follows the corresponding base transition:

T09: NO\_VALID\_PROGRAM → COMPILED\_OWNED

T10: NO\_VALID\_PROGRAM → NO\_VALID\_PROGRAM

T12: COMPILED\_OWNED → FREED\_OR\_EMPTY

T13: FREED\_OR\_EMPTY → FREED\_OR\_EMPTY

Within each five-transition group, the event ID, return predicate, and ownership effect remain consistent with the V1 semantics:

T09 uses the compile event, requires successful compilation (return == 0), and acquires ownership.

T10 uses the compile event, represents compilation failure (return != 0), and acquires no program.

T12 uses the freecode event and releases the caller-owned compiled program.

T13 uses the freecode event on the same still-live, normalized struct bpf\_program; it has no additional ownership effect and does not make the released program valid again.

The lifted transition identifiers also agree with the expansion map. Some product-state variants remain subject to cross-resource prerequisites—particularly the active-handle requirement for compilation. Their structural presence does not independently declare the operation valid; validity and violations remain governed by the explicit predicates and obligations.



Verify that each V1 BPF transition is lifted across all five PCAP states.

For every lifted transition, verify that only the BPF component changes and
the PCAP component is held fixed.

Verify that event ID, return predicate, and ownership effect remain equivalent
to the V1 transition being lifted.

### V2-RR05 — Obligation preservation and transition-reference expansion

Decision: PASS

Notes:

Manual comparison confirms that all 20 V1 obligations remain present in V2 with the same obligation IDs and substantive protocol meanings. Their approved source-evidence references, pinned libpcap revision a999701dca5c873779281938baee6bc185a8d4dc, ownership semantics, conditions, required behaviors, and D1–D8 classifications remain unchanged.

Where a V1 obligation referenced a local transition, V2 expands that reference to every corresponding product-state variant:

PCAP transitions are expanded across all three BPF states.

BPF transitions are expanded across all five PCAP states.

Obligations involving multiple base transitions include the complete lifted set for each referenced transition.

Obligations that did not reference a transition remain without invented transition references.

All expanded transition IDs resolve to defined V2 transitions. No required lifted variant is missing, no unrelated variant has been added, and no obligation’s meaning has been broadened or narrowed by the expansion.

The D1–D8 distribution is also preserved: D1=4, D2=2, D3=3, D4=1, D5=2, D6=3, D7=2, and D8=3. No arbitrary non-protocol C defect has been introduced into the obligation set.

Verify that all 20 V1 obligations remain present with the same substantive
protocol meaning, source evidence, library revision, ownership semantics, and
D1-D8 classification.

Where a V1 obligation structurally referenced a local transition ID, verify
that V2 expands that reference to the corresponding lifted transition variants
without changing the obligation's substantive meaning.

### V2-RR06 — Permitted exit states

Decision: PASS

Notes:

Manual inspection confirms that the permitted V2 exits are exactly these four product states:

NO\_HANDLE\_\_BPF\_\_NO\_VALID\_PROGRAM

NO\_HANDLE\_\_BPF\_\_FREED\_OR\_EMPTY

CLOSED\_\_BPF\_\_NO\_VALID\_PROGRAM

CLOSED\_\_BPF\_\_FREED\_OR\_EMPTY

These are precisely the Cartesian combinations of the two non-owning PCAP states (NO\_HANDLE and CLOSED) and the two non-owning BPF states (NO\_VALID\_PROGRAM and FREED\_OR\_EMPTY).

No state containing the live caller-owned PCAP component UNACTIVATED\_OWNED, ACTIVE\_OWNED, or ACTIVATION\_FAILED\_OWNED is permitted as an exit. Likewise, no state containing the BPF component COMPILED\_OWNED is permitted as an exit.

Therefore, an exit is permitted only when neither resource component carries an outstanding caller-owned resource. Cleanup of one component does not discharge the independent cleanup obligation of the other component.



Verify that the four permitted V2 exits are exactly the combinations of:

PCAP component: `NO\_HANDLE` or `CLOSED`

and

BPF component: `NO\_VALID\_PROGRAM` or `FREED\_OR\_EMPTY`.

Verify that no state containing live caller-owned `pcap\_t` or
`COMPILED\_OWNED` BPF ownership is a permitted exit.

### V2-RR07 — Preservation of previously approved semantics

Decision: PASS

Notes:

Manual comparison confirms that V2 makes a structural product-state correction without changing the previously approved protocol semantics. The following remain unchanged:

Pinned libpcap revision: a999701dca5c873779281938baee6bc185a8d4dc

Frozen API scope and the same 10-event set

API return-value predicates and success/failure branches

Handle, BPF-program, and borrowed-value ownership semantics

The same 17 approved source-provenance items

pcap\_next\_ex() borrowed header/data semantics, including the prohibition on caller deallocation and the later-read invalidation boundary unless copied

pcap\_setfilter() non-transfer semantics and the caller’s continuing pcap\_freecode() duty

The limited repeated-pcap\_freecode() interpretation for the same still-live, normalized struct bpf\_program

Independent identity and cleanup tracking for each pcap\_t and BPF-program resource

The 20-obligation D1–D8 taxonomy projection and category distribution

No synthetic initialization event was introduced. V2 continues to use the original event set and instead structurally initializes both logical resources through the single product initial state NO\_HANDLE\_\_BPF\_\_NO\_VALID\_PROGRAM.

Accordingly, V2 changes state representation and transition lifting only; it does not introduce a substantive protocol-semantic change. Exact repository commit binding remains the separate V2-RR01 issue and does not alter this semantic-preservation finding.



Verify that V2 does not change:

* library revision;
* frozen API scope;
* event set;
* return-value semantics;
* ownership semantics;
* source provenance;
* borrowed `pcap\_next\_ex()` lifetime semantics;
* `pcap\_setfilter()` non-transfer semantics;
* limited repeated-`pcap\_freecode()` interpretation;
* independent logical resource identity;
* D1-D8 taxonomy projection.

Verify that no synthetic initialization event was introduced.

### V2-RR08 — Source-only quarantine and RR-08 closure

Decision: PASS

Notes:

Manual inspection confirms that V2 uses only the 17 approved pinned source-evidence artifacts. Its provenance records and obligation evidence references contain no generated-corpus evidence, analyzer or baseline results, controlled LLM-review output, gold labels, repair output, compiler-log semantic content, or corpus-performance feedback. The candidate also explicitly records generated\_corpus\_used\_as\_specification\_evidence: false.

V2 adequately resolves the original V1 RR-08 representation defect. Its 15 states structurally encode the Cartesian product of the five PCAP states and three BPF states, and the single schema-level initial state NO\_HANDLE\_\_BPF\_\_NO\_VALID\_PROGRAM initializes both resource components. Both lifecycles are consequently reachable within one machine-readable transition system, without relying on reviewer prose or introducing a synthetic initialization event.

The correction preserves the previously approved API, return-value, ownership, lifetime, evidence, and D1–D8 semantics. No additional semantic revision is required for the original RR-08 defect.

V2 is therefore substantively suitable for finalization with respect to source quarantine and RR-08 closure. However, finalization of the exact checkpoint as a whole should remain withheld until the separate V2-RR01 immutable commit/target-binding deficiency is resolved.



Verify that no generated-corpus evidence, analyzer result, baseline result,
LLM-review result, gold label, repair output, or corpus-performance feedback
entered the V2 specification.

Explicitly decide whether V2 adequately resolves the original V1 `RR-08`
representation defect and is suitable for finalization without additional
semantic revision.

## Overall human-review decision

Choose exactly one:

* \[ ] `APPROVE\_EXACT\_V2\_DRAFT\_FOR\_FINALIZATION`
* \[x] `REVISION\_REQUIRED`
* \[ ] `REJECT`

Summary: V2-RR02 through V2-RR08 pass. The V2 product-state construction correctly resolves the original V1 RR-08 defect: both resource components are structurally initialized, PCAP and BPF transitions are completely lifted, all 20 obligations and their approved semantics are preserved, permitted exits carry no live ownership, and the source-only quarantine remains intact. No additional semantic revision is required for the protocol model itself.

V2-RR01 remains REVISION\_REQUIRED. The archive’s V2 JSON bytes independently match the declared SHA-256 3ee8459dd2cff6dc8f5dd538a0f8d54a9ceda740d5ea7d977a0a9d34093c3221 and Git blob 2f5782b744edc3e7684b459241cf079a77da1ab7. Its records also consistently identify the V1 outcome as REVISION\_REQUIRED with blocking item RR-08. However, the handoff does not include repository metadata or a Git bundle capable of independently resolving author commit 342ea862912e53b1ebec70f2e53e57db10d7846c and its tree, and it does not include the exact V1 predecessor bytes for direct predecessor verification.

Therefore, the exact V2 draft cannot yet be approved for finalization under a strict independent-review standard. This is a correctable provenance and immutable-binding deficiency, not a substantive protocol failure, so REVISION\_REQUIRED is appropriate rather than REJECT. The V2 specification should not be semantically altered; a corrected immutable review handoff should provide independently verifiable Git history/object binding and exact predecessor material.

Archive SHA-256: 07ee89d70881aba38b9696a8f2a043554e765efa261db16e8afc36e76ab8fb54

V2 draft SHA-256: exact match

Computed Git blob: 2f5782b744edc3e7684b459241cf079a77da1ab7 — exact match

14 immutable materials ke hashes: all match

17 approved evidence files ke hashes: all match

Exact V1 draft SHA-256, previously supplied V1 archive se: match

V1 decision: REVISION\_REQUIRED, blocking item RR-08 — confirmed

States: 15 unique, exact 5×3 Cartesian product

Events: 10 unique

Transitions: 50 unique

PCAP lifts: 30/30 correct

BPF lifts: 20/20 correct

Obligations: 20/20 preserved

Provenance records: 17/17

All state/event/transition/evidence references resolve

Permitted exits: exact four non-owning states

No synthetic initialization event

D1–D8 distribution preserved

Prohibited/generated evidence detected: none

Final reverified decisions:

Review item	Decision

V2-RR01	REVISION\_REQUIRED

V2-RR02	PASS

V2-RR03	PASS

V2-RR04	PASS

V2-RR05	PASS

V2-RR06	PASS

V2-RR07	PASS

V2-RR08	PASS

Overall	REVISION\_REQUIRED



Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS

Human reviewer date:17 / August / 2026

## Immutability rule

If the decision is `REVISION\_REQUIRED`, do not edit this V2 author checkpoint
in place. Create a new immutable successor.

If the decision is `APPROVE\_EXACT\_V2\_DRAFT\_FOR\_FINALIZATION`, no semantic
change may be introduced during finalization. Only already-deferred freeze
metadata and Decision-0018 content hashes may be added before schema
validation and canonical freeze.

