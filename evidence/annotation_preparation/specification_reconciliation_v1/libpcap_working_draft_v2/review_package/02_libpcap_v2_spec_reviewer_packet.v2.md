# libpcap V2 RR-08 Successor Independent Review Packet

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

Repository target:

`evidence/annotation_preparation/specification_reconciliation_v1/libpcap_working_draft_v2/libpcap_source_only_working_fsm_draft.v2.json`

Exact V2 draft SHA-256:

`3ee8459dd2cff6dc8f5dd538a0f8d54a9ceda740d5ea7d977a0a9d34093c3221`

Author checkpoint commit:

`342ea862912e53b1ebec70f2e53e57db10d7846c`

Author checkpoint tree:

`1e8253e52be0a0d41fbe436c738d0011a02e33fa`

Git blob for exact V2 target:

`2f5782b744edc3e7684b459241cf079a77da1ab7`

Package-local byte-identical copy:

`evidence/annotation_preparation/specification_reconciliation_v1/libpcap_working_draft_v2/review_package/03_libpcap_source_only_working_fsm_draft.v2.json`

This V2 artifact is an immutable author checkpoint. It is **not** a
canonical frozen libpcap protocol specification.

## Why V2 exists

The V1 human review recorded `REVISION_REQUIRED` only for `RR-08`.

The blocking representation problem was that V1 used one schema-level
`initial_state = NO_HANDLE`, while the independently modeled BPF resource
used local fresh state `NO_VALID_PROGRAM`. Under the single declared
transition relation, the BPF lifecycle was not structurally reachable.

V2 addresses that representation defect by using the existing schema's
string-state representation as a direct product:

`PCAP_STATE__BPF__BPF_STATE`

The V2 schema-level initial state is:

`NO_HANDLE__BPF__NO_VALID_PROGRAM`

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
* Initial state: `NO_HANDLE__BPF__NO_VALID_PROGRAM`
* Schema changed from V1: `NO`
* Synthetic protocol events added: `NO`
* Canonical specification frozen: `NO`
* Human review completed: `NO`
* Freeze dates/content hashes: `DEFERRED`

## Mandatory V2 review checks

For every section, record exactly one of:

`PASS`

`REVISION_REQUIRED`

`FAIL`

### V2-RR01 — Exact predecessor and immutable-target binding

Decision:

Notes:

Verify that the reviewed bytes are exactly the V2 author checkpoint identified
by SHA-256 `3ee8459dd2cff6dc8f5dd538a0f8d54a9ceda740d5ea7d977a0a9d34093c3221`, Git blob
`2f5782b744edc3e7684b459241cf079a77da1ab7`, and author commit `342ea862912e53b1ebec70f2e53e57db10d7846c`.

Also verify that V2 is a successor to the exact V1 reviewed target and that the
recorded V1 outcome was `REVISION_REQUIRED` with blocking item `RR-08`.

### V2-RR02 — Product-state representation closes RR-08

Decision:

Notes:

Verify that the 15 V2 states represent the Cartesian product of the five
`pcap_t` local states and three BPF-program local states.

Verify that the single schema-level initial state
`NO_HANDLE__BPF__NO_VALID_PROGRAM` structurally initializes both resource
components and removes the V1 reachability defect.

### V2-RR03 — PCAP transition lifting

Decision:

Notes:

Verify that each V1 `pcap_t` transition is lifted across all three BPF states.

For every lifted transition, verify that only the PCAP component changes and
the BPF component is held fixed.

Verify that event ID, return predicate, and ownership effect remain equivalent
to the V1 transition being lifted.

### V2-RR04 — BPF transition lifting

Decision:

Notes:

Verify that each V1 BPF transition is lifted across all five PCAP states.

For every lifted transition, verify that only the BPF component changes and
the PCAP component is held fixed.

Verify that event ID, return predicate, and ownership effect remain equivalent
to the V1 transition being lifted.

### V2-RR05 — Obligation preservation and transition-reference expansion

Decision:

Notes:

Verify that all 20 V1 obligations remain present with the same substantive
protocol meaning, source evidence, library revision, ownership semantics, and
D1-D8 classification.

Where a V1 obligation structurally referenced a local transition ID, verify
that V2 expands that reference to the corresponding lifted transition variants
without changing the obligation's substantive meaning.

### V2-RR06 — Permitted exit states

Decision:

Notes:

Verify that the four permitted V2 exits are exactly the combinations of:

PCAP component: `NO_HANDLE` or `CLOSED`

and

BPF component: `NO_VALID_PROGRAM` or `FREED_OR_EMPTY`.

Verify that no state containing live caller-owned `pcap_t` or
`COMPILED_OWNED` BPF ownership is a permitted exit.

### V2-RR07 — Preservation of previously approved semantics

Decision:

Notes:

Verify that V2 does not change:

* library revision;
* frozen API scope;
* event set;
* return-value semantics;
* ownership semantics;
* source provenance;
* borrowed `pcap_next_ex()` lifetime semantics;
* `pcap_setfilter()` non-transfer semantics;
* limited repeated-`pcap_freecode()` interpretation;
* independent logical resource identity;
* D1-D8 taxonomy projection.

Verify that no synthetic initialization event was introduced.

### V2-RR08 — Source-only quarantine and RR-08 closure

Decision:

Notes:

Verify that no generated-corpus evidence, analyzer result, baseline result,
LLM-review result, gold label, repair output, or corpus-performance feedback
entered the V2 specification.

Explicitly decide whether V2 adequately resolves the original V1 `RR-08`
representation defect and is suitable for finalization without additional
semantic revision.

## Overall human-review decision

Choose exactly one:

* [ ] `APPROVE_EXACT_V2_DRAFT_FOR_FINALIZATION`
* [ ] `REVISION_REQUIRED`
* [ ] `REJECT`

Summary:

Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

## Immutability rule

If the decision is `REVISION_REQUIRED`, do not edit this V2 author checkpoint
in place. Create a new immutable successor.

If the decision is `APPROVE_EXACT_V2_DRAFT_FOR_FINALIZATION`, no semantic
change may be introduced during finalization. Only already-deferred freeze
metadata and Decision-0018 content hashes may be added before schema
validation and canonical freeze.
