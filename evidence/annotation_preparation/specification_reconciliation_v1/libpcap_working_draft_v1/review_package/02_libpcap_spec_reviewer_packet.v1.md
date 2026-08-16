# libpcap Source-Only Protocol Specification Review Packet V1

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

Repository immutable target path:

`evidence/annotation_preparation/specification_reconciliation_v1/libpcap_working_draft_v1/libpcap_source_only_working_fsm_draft.v1.json`

Exact draft SHA-256:

`2a2723eba8cac78c004b846fc1fe71e786730c9aeecc6800e81ee6f2e318687a`

Author checkpoint commit:

`a2344c4905555388bbecd53834ca6627cdbe808a`

Author checkpoint tree:

`4d3bed534b74c6dd548d0ff8791d419f081da8c8`

Git blob for the exact repository target:

`de11a08a6737f5a29734d2b41f7fd5c19cca8522`

Package-local byte-identical review copy:

`evidence/annotation_preparation/specification_reconciliation_v1/libpcap_working_draft_v1/review_package/03_libpcap_source_only_working_fsm_draft.v1.json`

Package-copy SHA-256:

`2a2723eba8cac78c004b846fc1fe71e786730c9aeecc6800e81ee6f2e318687a`

This V1 artifact is an immutable author checkpoint. It is **not** a frozen
canonical protocol specification.

## Frozen authoring-scope binding

Scope contract:

`config/annotation/libpcap_v1_authoring_scope.v1.json`

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
* `EV-LIBPCAP-MAN-CREATE-005` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_create.3pcap` — SHA-256 `b9cc4a57b5ef4ffed8647c33440eec3c2365f587d7a01d2c5971918498854c55`
* `EV-LIBPCAP-MAN-ACTIVATE-006` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_activate.3pcap` — SHA-256 `ca5461684af7e4107fc817c0f599249ff8ef6827d88540a9df2a9e9826049655`
* `EV-LIBPCAP-MAN-CLOSE-007` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_close.3pcap` — SHA-256 `7cbb72168caf80000b58a1d294f5ef18db075745c302bc137d38f3d7d4a088bc`
* `EV-LIBPCAP-MAN-SNAPLEN-008` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_set_snaplen.3pcap` — SHA-256 `4cad03c340197b1bca2554716a232945651fafe950f3522e0bea37b02f19a45c`
* `EV-LIBPCAP-MAN-PROMISC-009` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_set_promisc.3pcap` — SHA-256 `1282eecdf67079ddad1ed23bb7dc5a29bbfcc880f364af53b722daef22ca6287`
* `EV-LIBPCAP-MAN-TIMEOUT-010` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_set_timeout.3pcap` — SHA-256 `ffbf8ed8e594dbff786ff5727e77c914a24ca04dc3b6ff1cb611e796e91c04cf`
* `EV-LIBPCAP-MAN-IMMEDIATE-011` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_set_immediate_mode.3pcap.in` — SHA-256 `14509e13caa40e35dcf37cf77bdbeb3c5c3b62cf0629a01adccc8b8d5e319111`
* `EV-LIBPCAP-MAN-BUFFER-012` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_set_buffer_size.3pcap` — SHA-256 `513c91d6e340a8afa58b0939914fb646403ce5f2fda0a0b874b3fd6b6f17e7d1`
* `EV-LIBPCAP-MAN-DATALINK-013` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_datalink.3pcap.in` — SHA-256 `434c12ea9f01c6badf1cc3ef5009392df2dbe32761435baff3d091a62cdb9d09`
* `EV-LIBPCAP-MAN-NEXTEX-014` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_next_ex.3pcap` — SHA-256 `becc1379a3072cedffc8bdfb76a187c6c448f52a79332d1af0dc853f2cb62efc`
* `EV-LIBPCAP-MAN-COMPILE-015` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_compile.3pcap.in` — SHA-256 `c021ead1c9f04d8601d3afcc164baae8e704d1952c85e93767c1ccd5d9624323`
* `EV-LIBPCAP-MAN-SETFILTER-016` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_setfilter.3pcap` — SHA-256 `8cfc4d0c8a76d0fb6ffb8c5f3fd5d82228e50d6ca82eb2e7995b3ac3315b9fce`
* `EV-LIBPCAP-MAN-FREECODE-017` — `/openbayes/home/svf-gate1c-source-qualification-v1/libpcap/pcap_freecode.3pcap` — SHA-256 `3d97c939069feadce4f62d576ceddf9409e68c60d97faf6084228f70255d79e6`

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
   `pcap_create()` returning non-NULL creates an owned unactivated handle.
   `pcap_activate()` return `>= 0` establishes the active state; positive
   values are warnings. A negative result leaves an owned failed-activation
   handle that still requires `pcap_close()`.

2. **Pre-activation configuration.**
   The frozen family is exactly `pcap_set_snaplen`, `pcap_set_promisc`,
   `pcap_set_timeout`, `pcap_set_immediate_mode`, and
   `pcap_set_buffer_size`. Post-activation use is modeled as D6.

3. **Active-only operations.**
   `pcap_datalink`, `pcap_next_ex`, `pcap_compile`, and `pcap_setfilter`
   require the relevant active-handle precondition.

4. **Borrowed packet/header values.**
   A successful `pcap_next_ex()` yields library-owned borrowed header/data.
   The caller must not free them. Within this frozen V1 scope, a later
   `pcap_next_ex()` invalidates reliance on the prior view unless copied.

5. **BPF ownership.**
   `pcap_compile()` return `0` creates a caller-owned compiled program.
   `pcap_setfilter()` does not transfer that ownership; eventual
   `pcap_freecode()` remains required.

6. **Repeated `pcap_freecode()`.**
   V1 does not classify a repeated call as D4 merely by count. T13 is limited
   to the same still-live `struct bpf_program` object after the pinned
   implementation has set `bf_len` to zero and `bf_insns` to NULL. This does
   not make the released program valid for later filter use.

7. **Independent resource identities.**
   Each acquired `pcap_t` and each successful `bpf_program` is independently
   tracked. Cleanup of one does not satisfy cleanup of another.

8. **Single-schema / dual-resource initial-state representation.**
   The JSON schema has one required top-level `initial_state`. The draft uses
   `NO_HANDLE` as that schema-level default because all frozen scenarios begin
   their capture lifecycle with `pcap_create`. The BPF subresource has its
   explicit local fresh state `NO_VALID_PROGRAM`, and T09/T10 are evaluated on
   that independent logical resource.

   This representation is **not pre-approved**. The reviewer must explicitly
   decide whether it is acceptable. If not, record `REVISION_REQUIRED`; the
   V1 author checkpoint must remain immutable and a successor must be created.

9. **Partial relation semantics.**
   Absence of a transition alone establishes neither validity nor violation.
   A protocol violation requires an explicit obligation.

## Mandatory review checks

For every section, record exactly `PASS`, `REVISION_REQUIRED`, or `FAIL`.

### RR-01 — Evidence completeness and provenance integrity

Decision:

Notes:

Verify all 17 evidence files are the approved pinned artifacts, all hashes
match, and every obligation references only defined evidence IDs.

### RR-02 — State / event / transition consistency

Decision:

Notes:

Verify all state/event/transition identifiers and references, activation
branches, repeated packet reads, compiled-program acquisition/release, and
pcap-handle release semantics.

### RR-03 — pcap_t ownership and activation semantics

Decision:

Notes:

Verify successful creation, configuration-before-activation, positive-warning
activation, negative activation, active-only use, release, use-after-close,
double-close, and function-exit cleanup obligations.

### RR-04 — BPF-program ownership semantics

Decision:

Notes:

Verify compile success/failure separation, setfilter prerequisites,
non-transfer of ownership, eventual freecode cleanup, post-freecode use, and
the limited repeated-freecode T13 interpretation.

### RR-05 — Borrowed packet/header ownership and lifetime

Decision:

Notes:

Verify D7 caller-free prohibition and D3 lifetime rule for successful
`pcap_next_ex()` borrowed values.

### RR-06 — Terminal and permitted exit states

Decision:

Notes:

Proposed permitted exits are:

* `NO_HANDLE`
* `CLOSED`
* `NO_VALID_PROGRAM`
* `FREED_OR_EMPTY`

Verify that no state carrying live `pcap_t` or compiled-program ownership is a
permitted exit.

### RR-07 — Resource-identity independence

Decision:

Notes:

Verify that two independent `pcap_t` handles and separately compiled
`bpf_program` instances retain distinct cleanup obligations and that the draft
does not invent same-handle identity coupling beyond the frozen scope.

### RR-08 — Dual-resource initial-state representation

Decision:

Notes:

Explicitly decide whether the schema-level `initial_state = NO_HANDLE` plus
the independently declared local BPF start state `NO_VALID_PROGRAM` is an
acceptable representation under the existing single-specification schema.

This item must not be left implicit.

### RR-09 — Unsupported conditions and frozen-scope alignment

Decision:

Notes:

Verify that excluded functions remain outside V1, `pcap_open_live` is not
silently substituted, `pcap_next` is not included due substring matching,
`pcap_snapshot` is not inferred from “snapshot-length”, and no generated
corpus evidence entered the specification.

### RR-10 — D1-D8 obligation projection

Decision:

Notes:

Verify the 20 obligations are assigned to the declared D1-D8 taxonomy without
silently classifying arbitrary non-protocol C bugs.

## Overall human-review decision

Choose exactly one:

* [ ] `APPROVE_EXACT_DRAFT_FOR_FINALIZATION`
* [ ] `REVISION_REQUIRED`
* [ ] `REJECT`

Summary:

Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

## Immutability rule

If the decision is `REVISION_REQUIRED`, do not edit this V1 file in place.
Create a new immutable successor author checkpoint and reviewer package.

If the decision is `APPROVE_EXACT_DRAFT_FOR_FINALIZATION`, no semantic change
may be introduced during finalization. Only the already-deferred freeze dates
and Decision-0018 content hashes may be added before schema validation and
canonical freeze.
