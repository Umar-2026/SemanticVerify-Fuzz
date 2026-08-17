# libpcap Source-Only Protocol Specification Review Packet V1

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

Repository immutable target path:

`evidence/annotation\_preparation/specification\_reconciliation\_v1/libpcap\_working\_draft\_v1/libpcap\_source\_only\_working\_fsm\_draft.v1.json`

Exact draft SHA-256:

`2a2723eba8cac78c004b846fc1fe71e786730c9aeecc6800e81ee6f2e318687a`

Author checkpoint commit:

`a2344c4905555388bbecd53834ca6627cdbe808a`

Author checkpoint tree:

`4d3bed534b74c6dd548d0ff8791d419f081da8c8`

Git blob for the exact repository target:

`de11a08a6737f5a29734d2b41f7fd5c19cca8522`

Package-local byte-identical review copy:

`evidence/annotation\_preparation/specification\_reconciliation\_v1/libpcap\_working\_draft\_v1/review\_package/03\_libpcap\_source\_only\_working\_fsm\_draft.v1.json`

Package-copy SHA-256:

`2a2723eba8cac78c004b846fc1fe71e786730c9aeecc6800e81ee6f2e318687a`

This V1 artifact is an immutable author checkpoint. It is **not** a frozen
canonical protocol specification.

## Frozen authoring-scope binding

Scope contract:

`config/annotation/libpcap\_v1\_authoring\_scope.v1.json`

SHA-256:

`52ed3d09c6031c7d256e59246aa44ff741d358a784f32516a9f503abe5110d65`

Decision 0020:

`documentation/decisions/0020-libpcap-v1-source-only-authoring-scope-freeze.md`

SHA-256:

`f2bed5a076cfc434bb2fbfb4e0fdb7ad7fff77bbeea0f34c57b1c96a37a69a6e`

Pinned libpcap revision:

`a999701dca5c873779281938baee6bc185a8d4dc`

## Review quarantine

Use only the frozen scope materials and approved pinned source evidence listed
in this packet.

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

## Approved protocol evidence

* `EV-LIBPCAP-H-001` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap/pcap.h` — SHA-256 `a18377a304f254e93e7d5059eec87d28c46b44cdad6fb174cff315440cae87b0`
* `EV-LIBPCAP-C-002` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap.c` — SHA-256 `0cef77dc8385eefa5902df7c7abd42d8dd43ee68a72afa0c80f701e4efc202c9`
* `EV-LIBPCAP-GENCODE-003` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/gencode.c` — SHA-256 `8326daaddd56a9eab15a8c4c09666873e5e056922c2f1cc0a5918958f8953113`
* `EV-LIBPCAP-MAN-PCAP-004` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap.3pcap.in` — SHA-256 `ba3ef9b9fc1874cf0372ba757fb2494827abca69d4a23333ab758c435a7643b4`
* `EV-LIBPCAP-MAN-CREATE-005` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_create.3pcap` — SHA-256 `b9cc4a57b5ef4ffed8647c33440eec3c2365f587d7a01d2c5971918498854c55`
* `EV-LIBPCAP-MAN-ACTIVATE-006` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_activate.3pcap` — SHA-256 `ca5461684af7e4107fc817c0f599249ff8ef6827d88540a9df2a9e9826049655`
* `EV-LIBPCAP-MAN-CLOSE-007` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_close.3pcap` — SHA-256 `7cbb72168caf80000b58a1d294f5ef18db075745c302bc137d38f3d7d4a088bc`
* `EV-LIBPCAP-MAN-SNAPLEN-008` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_set\_snaplen.3pcap` — SHA-256 `4cad03c340197b1bca2554716a232945651fafe950f3522e0bea37b02f19a45c`
* `EV-LIBPCAP-MAN-PROMISC-009` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_set\_promisc.3pcap` — SHA-256 `1282eecdf67079ddad1ed23bb7dc5a29bbfcc880f364af53b722daef22ca6287`
* `EV-LIBPCAP-MAN-TIMEOUT-010` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_set\_timeout.3pcap` — SHA-256 `ffbf8ed8e594dbff786ff5727e77c914a24ca04dc3b6ff1cb611e796e91c04cf`
* `EV-LIBPCAP-MAN-IMMEDIATE-011` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_set\_immediate\_mode.3pcap.in` — SHA-256 `14509e13caa40e35dcf37cf77bdbeb3c5c3b62cf0629a01adccc8b8d5e319111`
* `EV-LIBPCAP-MAN-BUFFER-012` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_set\_buffer\_size.3pcap` — SHA-256 `513c91d6e340a8afa58b0939914fb646403ce5f2fda0a0b874b3fd6b6f17e7d1`
* `EV-LIBPCAP-MAN-DATALINK-013` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_datalink.3pcap.in` — SHA-256 `434c12ea9f01c6badf1cc3ef5009392df2dbe32761435baff3d091a62cdb9d09`
* `EV-LIBPCAP-MAN-NEXTEX-014` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_next\_ex.3pcap` — SHA-256 `becc1379a3072cedffc8bdfb76a187c6c448f52a79332d1af0dc853f2cb62efc`
* `EV-LIBPCAP-MAN-COMPILE-015` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_compile.3pcap.in` — SHA-256 `c021ead1c9f04d8601d3afcc164baae8e704d1952c85e93767c1ccd5d9624323`
* `EV-LIBPCAP-MAN-SETFILTER-016` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_setfilter.3pcap` — SHA-256 `8cfc4d0c8a76d0fb6ffb8c5f3fd5d82228e50d6ca82eb2e7995b3ac3315b9fce`
* `EV-LIBPCAP-MAN-FREECODE-017` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap\_freecode.3pcap` — SHA-256 `3d97c939069feadce4f62d576ceddf9409e68c60d97faf6084228f70255d79e6`

## Expected V1 structure

* States: `8`
* Events: `10`
* Transitions: `14`
* Core obligations: `20`
* Provenance items: `17`
* Canonical specification frozen: `NO`
* Human review completed: `NO`
* Obligation freeze dates/content hashes: `DEFERRED`
* Top-level freeze date/content hash: `DEFERRED`

## Reviewer-visible defect taxonomy

* **D1** — Use before successful initialization
* **D2** — Use after failed initialization or activation
* **D3** — Use after close, destroy, end, or release
* **D4** — Double close, destroy, end, or release
* **D5** — Missing cleanup on a success or failure exit
* **D6** — Invalid API call ordering or missing prerequisite call
* **D7** — Ownership misuse: freeing borrowed data, failing transferred ownership, or wrong owner
* **D8** — Conditionally invalid cleanup or cleanup under the wrong state or return condition

## Critical semantics requiring explicit review

1. **Handle acquisition and activation.**
`pcap\_create()` returning non-NULL creates an owned unactivated handle.
`pcap\_activate()` return `>= 0` establishes the active state; positive
values are warnings. A negative result leaves an owned failed-activation
handle that still requires `pcap\_close()`.
2. **Pre-activation configuration.**
The frozen family is exactly `pcap\_set\_snaplen`, `pcap\_set\_promisc`,
`pcap\_set\_timeout`, `pcap\_set\_immediate\_mode`, and
`pcap\_set\_buffer\_size`. Post-activation use is modeled as D6.
3. **Active-only operations.**
`pcap\_datalink`, `pcap\_next\_ex`, `pcap\_compile`, and `pcap\_setfilter`
require the relevant active-handle precondition.
4. **Borrowed packet/header values.**
A successful `pcap\_next\_ex()` yields library-owned borrowed header/data.
The caller must not free them. Within this frozen V1 scope, a later
`pcap\_next\_ex()` invalidates reliance on the prior view unless copied.
5. **BPF ownership.**
`pcap\_compile()` return `0` creates a caller-owned compiled program.
`pcap\_setfilter()` does not transfer that ownership; eventual
`pcap\_freecode()` remains required.
6. **Repeated `pcap\_freecode()`.**
V1 does not classify a repeated call as D4 merely by count. T13 is limited
to the same still-live `struct bpf\_program` object after the pinned
implementation has set `bf\_len` to zero and `bf\_insns` to NULL. This does
not make the released program valid for later filter use.
7. **Independent resource identities.**
Each acquired `pcap\_t` and each successful `bpf\_program` is independently
tracked. Cleanup of one does not satisfy cleanup of another.
8. **Single-schema / dual-resource initial-state representation.**
The JSON schema has one required top-level `initial\_state`. The draft uses
`NO\_HANDLE` as that schema-level default because all frozen scenarios begin
their capture lifecycle with `pcap\_create`. The BPF subresource has its
explicit local fresh state `NO\_VALID\_PROGRAM`, and T09/T10 are evaluated on
that independent logical resource.

   This representation is **not pre-approved**. The reviewer must explicitly
decide whether it is acceptable. If not, record `REVISION\_REQUIRED`; the
V1 author checkpoint must remain immutable and a successor must be created.

9. **Partial relation semantics.**
Absence of a transition alone establishes neither validity nor violation.
A protocol violation requires an explicit obligation.

## Mandatory review checks

For every section, record exactly `PASS`, `REVISION\_REQUIRED`, or `FAIL`.

### RR-01 — Evidence completeness and provenance integrity

Decision: `PASS`



Notes:



All 17 approved evidence files are present in the handoff and their computed

SHA-256 values match the values declared by the packet, the frozen scope

contract, the candidate provenance records, and the handoff manifest.  The 17

evidence IDs are unique.  Every `source\_evidence` reference made by the 20

obligations resolves to one of those defined evidence IDs; there are no

undefined or out-of-quarantine evidence references.  The exact draft SHA-256,

scope-contract SHA-256, Decision-0020 SHA-256, and locally computed Git blob

for the draft also match their declared values.



Verify all 17 evidence files are the approved pinned artifacts, all hashes

match, and every obligation references only defined evidence IDs.

### RR-02 — State / event / transition consistency

Decision: `PASS`



Notes:



The candidate contains 8 unique states, 10 unique events, 14 unique

transitions, and 20 uniquely identified obligations.  All transition event

references, state references, and obligation transition references resolve.

T01/T02 separate successful and failed creation; T04/T05 separate

non-negative and negative activation; T07/T08 separate packet-producing and

non-packet-producing `pcap\_next\_ex` returns; T09/T10 separate successful and

failed compilation; T12/T13 distinguish first release from the narrowly

defined normalized repeated-freecode case; and T14 releases every declared

owned handle state.  The adequacy of using one schema-level initial state for

the two local resource lifecycles is not silently accepted here; it is

adjudicated separately under RR-08.



Verify all state/event/transition identifiers and references, activation

branches, repeated packet reads, compiled-program acquisition/release, and

pcap-handle release semantics.

### RR-03 — pcap\_t ownership and activation semantics

Decision: `PASS`



Notes:



The pinned documentation and implementation support the modeled handle

lifecycle.  A non-NULL `pcap\_create` result establishes a handle requiring

eventual `pcap\_close`, while a NULL result establishes no handle.  The five

frozen setters operate before successful activation and return

`PCAP\_ERROR\_ACTIVATED` on an activated handle.  `pcap\_activate` returns zero

for success, positive values for success with warnings, and negative values

for errors; on activation failure the handle is not freed and should be

closed.  `pcap\_datalink`, `pcap\_next\_ex`, `pcap\_compile`, and `pcap\_setfilter`

have the modeled active-handle prerequisite.  `pcap\_close` invokes handle

cleanup and frees the `pcap\_t`, supporting the use-after-close and

double-close prohibitions.  LIBPCAP-R01 through R11, together with T01-T08

and T14, cover acquisition, ordering, failed activation, active use,

conditional cleanup, missing exit cleanup, use after close, and double close.



Verify successful creation, configuration-before-activation, positive-warning

activation, negative activation, active-only use, release, use-after-close,

double-close, and function-exit cleanup obligations.

### RR-04 — BPF-program ownership semantics

Decision: `PASS`



Notes:



The pinned implementation rejects `pcap\_compile` on a not-yet-activated

handle, returns 0 only after populating `bf\_insns` and `bf\_len`, and returns an

error on compilation failure.  Thus T09 acquires a compiled program only on

return 0 and T10 creates no new valid program on failure.  `pcap\_setfilter`

requires an activated handle and a compiled-program argument; its use does

not remove the caller's later `pcap\_freecode` responsibility, as confirmed by

the freecode documentation.  `pcap\_freecode` sets `bf\_len` to zero, frees a

non-NULL `bf\_insns`, and then sets `bf\_insns` to NULL.  T13 is therefore

acceptable only for the same still-live `struct bpf\_program` object in that

normalized state; it does not restore `COMPILED\_OWNED` or permit later filter

use.  LIBPCAP-R14 through R19 correctly cover success/failure, prerequisites,

non-transfer, cleanup, and post-release use.



Verify compile success/failure separation, setfilter prerequisites,

non-transfer of ownership, eventual freecode cleanup, post-freecode use, and

the limited repeated-freecode T13 interpretation.

### RR-05 — Borrowed packet/header ownership and lifetime

Decision: `PASS`



Notes:



The pinned `pcap\_next\_ex` documentation states that, on return 1, the packet

header and packet data are library-owned values that the caller must not free.

It also states that they are not guaranteed to remain valid after the next

packet-reading call and must be copied if longer lifetime is required.

LIBPCAP-R12 assigns caller deallocation to D7 and LIBPCAP-R13 assigns reliance

on an uncopied prior view after a later in-scope `pcap\_next\_ex` to D3.  Those

rules accurately reflect the frozen V1 lifetime boundary.



Verify D7 caller-free prohibition and D3 lifetime rule for successful

`pcap\_next\_ex()` borrowed values.

### RR-06 — Terminal and permitted exit states

Decision: `PASS`



Notes:



The declared permitted exits are exactly `NO\_HANDLE`, `CLOSED`,

`NO\_VALID\_PROGRAM`, and `FREED\_OR\_EMPTY`.  None carries a live caller-owned

`pcap\_t` or successfully compiled BPF program.  The live ownership states

`UNACTIVATED\_OWNED`, `ACTIVE\_OWNED`, `ACTIVATION\_FAILED\_OWNED`, and

`COMPILED\_OWNED` are correctly excluded.  For a scenario containing both

resource families, the handle and program cleanup obligations must each be

satisfied independently; one permitted local exit does not discharge the

other resource's obligation.



Proposed permitted exits are:



\* `NO\_HANDLE`

\* `CLOSED`

\* `NO\_VALID\_PROGRAM`

\* `FREED\_OR\_EMPTY`



Verify that no state carrying live `pcap\_t` or compiled-program ownership is a

permitted exit.



### RR-07 — Resource-identity independence

Decision: `PASS`



Notes:



LIBPCAP-R20 explicitly conditions cleanup on each corresponding resource's

own successful acquisition and states that cleanup of one resource does not

discharge another.  The source APIs operate on the particular `pcap\_t \*` or

`struct bpf\_program \*` supplied by the caller, so two acquired handles and two

successfully compiled program objects retain separate cleanup duties.  The

draft also does not require the handle passed to `pcap\_setfilter` to be the

same handle used for `pcap\_compile`; no such identity coupling is established

by the frozen approved evidence.  Resource independence is therefore stated

without inventing an unsupported same-handle rule.



Verify that two independent `pcap\_t` handles and separately compiled

`bpf\_program` instances retain distinct cleanup obligations and that the draft

does not invent same-handle identity coupling beyond the frozen scope.



### RR-08 — Dual-resource initial-state representation

Decision: `REVISION\_REQUIRED`



Notes:



The proposed representation is not acceptable for canonical finalization

under the existing single-specification schema.  The candidate's only

structured `initial\_state` is `NO\_HANDLE`.  The schema has no per-resource

initial-state field and transitions have no structured resource-family

discriminator.  `NO\_VALID\_PROGRAM` is described as the fresh BPF local start

in reviewer-visible prose and in obligation text, but it is not encoded as a

second machine-readable initial state in the candidate specification fields.

Starting from the schema-level `NO\_HANDLE` and following the declared

transition relation reaches only the handle states; `NO\_VALID\_PROGRAM`,

`COMPILED\_OWNED`, and `FREED\_OR\_EMPTY`, and therefore T09, T10, T12, and T13,

are not reachable through that single state relation.  The partial-relation

rule prevents treating a missing transition as a violation, but it does not

establish the missing initial condition for a second resource machine.



A V2 successor should encode resource-local initial states and resource scope

structurally (or use another unambiguous schema-approved multi-resource

representation).  The immutable V1 author checkpoint must not be edited.



Explicitly decide whether the schema-level `initial\_state = NO\_HANDLE` plus

the independently declared local BPF start state `NO\_VALID\_PROGRAM` is an

acceptable representation under the existing single-specification schema.



This item must not be left implicit.

### RR-09 — Unsupported conditions and frozen-scope alignment

Decision: `PASS`



Notes:



The modeled events and obligations stay within the frozen function set.

`pcap\_open\_live` is not substituted for the `pcap\_create` plus

`pcap\_activate` lifecycle.  `pcap\_next` and `pcap\_snapshot` are absent as

modeled events and obligations; the draft uses `pcap\_next\_ex` and

`pcap\_set\_snaplen` as required.  The broader offline/dead, loop/dispatch,

timestamp, statistics, non-blocking, injection, dumper, discovery, and

datalink-mutation APIs remain explicitly unsupported or out of scope.  The

candidate declares `generated\_corpus\_used\_as\_specification\_evidence: false`,

and its provenance and all obligation evidence references contain only the 17

approved pinned source artifacts.



Verify that excluded functions remain outside V1, `pcap\_open\_live` is not

silently substituted, `pcap\_next` is not included due substring matching,

`pcap\_snapshot` is not inferred from “snapshot-length”, and no generated

corpus evidence entered the specification.

### RR-10 — D1-D8 obligation projection

Decision: `PASS`



Notes:



All 20 obligations use only D1-D8 and every declared category is represented:

D1=4, D2=2, D3=3, D4=1, D5=2, D6=3, D7=2, and D8=3.  The assignments match

the packet taxonomy: pre-initialization/active-state prerequisites map to D1;

use after failed creation or activation to D2; post-release use to D3;

double close to D4; missing handle/program cleanup to D5; invalid ordering or

missing prerequisites to D6; borrowed/non-transferred ownership misuse to D7;

and wrongly conditioned cleanup/use to D8.  The explicit unsupported

conditions exclude general packet-processing errors, buffer bugs, network

behavior, and arbitrary non-protocol C defects, and no obligation silently

imports those categories.



Verify the 20 obligations are assigned to the declared D1-D8 taxonomy without

silently classifying arbitrary non-protocol C bugs.



## Overall human-review decision

Choose exactly one:

* \[ ] `APPROVE\_EXACT\_DRAFT\_FOR\_FINALIZATION`
* \[x] `REVISION\_REQUIRED`
* \[ ] `REJECT`

Summary: RR-01 through RR-07 and RR-09 through RR-10 pass against the frozen scope and

approved pinned evidence.  RR-08 requires revision because the existing

single-initial-state schema does not structurally encode the independently

asserted BPF local start state; under the single declared transition relation

the BPF lifecycle is not reachable from `NO\_HANDLE`.  This is a correctable

representation defect rather than evidence of a fundamentally invalid

libpcap lifecycle, so the appropriate overall decision is

`REVISION\_REQUIRED`, not `REJECT`.  Per the immutability rule, the V1 target

must remain unchanged and any correction must be issued as a V2 successor

author checkpoint and reviewer package.



Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS



I confirm that I personally reviewed the exact immutable V1 target against

the frozen scope and approved evidence set, and I record the overall decision

REVISION\_REQUIRED.

Human reviewer date:17 / August / 2026

## Immutability rule

If the decision is `REVISION\_REQUIRED`, do not edit this V1 file in place.
Create a new immutable successor author checkpoint and reviewer package.

If the decision is `APPROVE\_EXACT\_DRAFT\_FOR\_FINALIZATION`, no semantic change
may be introduced during finalization. Only the already-deferred freeze dates
and Decision-0018 content hashes may be added before schema validation and
canonical freeze.

