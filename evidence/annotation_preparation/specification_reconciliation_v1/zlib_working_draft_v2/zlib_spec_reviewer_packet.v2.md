# zlib Source-Only Protocol Specification Successor Review Packet V2

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

Draft:

`evidence/annotation_preparation/specification_reconciliation_v1/zlib_working_draft_v2/zlib_source_only_successor_working_fsm_draft.v2.json`

Draft SHA-256:

`9f6e035fb275fb34e5f9ab34a6267f3b416b80a7aae8a7a1741c445c20457e5d`

Pinned zlib revision:

`da607da739fa6047df13e66a2af6b8bec7c2a498`

This artifact is a successor author checkpoint created in response to the completed V1 human review.

It is **not** a frozen canonical protocol specification.

The V1 checkpoint remains immutable.

V1 draft SHA-256:

`cb2738329164537bba86282668bfabf51599fac1292309f150a68a32f2571573`

V1 human-review record SHA-256:

`38db57f9a038ba1d052ccb8b33b703c0f85600b4323b818b0a2d611293dc9822`

The prior overall decision was `REVISION_REQUIRED`.

The prior reviewer accepted `ZLIB-CAND-R14`; V2 promotes it to core rule `ZLIB-R14`.

## Review quarantine

The reviewer must use only the approved source evidence listed below.

Do **not** consult generated fuzz drivers, selected-sample membership, raw model responses, generated compiler-log semantic contents, gold labels, analyzer output, baseline output, controlled LLM-review output, repair output, or failure-prompted post-hoc evidence.

## Integrity and structure

Expected V2 structure:

- States: 8
- Events: 11
- Transitions: 17
- Core obligations: 14
- Provenance evidence items: 7
- Canonical specification frozen: NO
- Human review completed for V2: NO

Working-draft `freeze_date` and `content_sha256` fields remain intentionally deferred until exact human approval and finalization.

## Approved source evidence

- `EV-ZLIB-H-001` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/zlib.h` — SHA-256 `818667d6ab6a37fe7469cb06a7f0cb2c2cb2f2c948a03e5accf1a4a74bf3020a`
- `EV-ZLIB-DEF-002` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/deflate.c` — SHA-256 `ea9ca4eb51b1a71aaf214b99f4a9fab177253d6268cae8e4c26d44d1812e52c2`
- `EV-ZLIB-INF-003` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/inflate.c` — SHA-256 `90221ea7d762e7044057f6ad5013e969086c6ba3d3051716b7aa786d7a6362ec`
- `EV-ZLIB-ZPIPE-004` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/examples/zpipe.c` — SHA-256 `e79717cefd20043fb78d730fd3b9d9cdf8f4642307fc001879dc82ddb468509f`
- `EV-ZLIB-TEST-005` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/test/example.c` — SHA-256 `be1b050aad808cdb016c01f42568d3a62ee37dd7b2b56bef0ade21be8d9fee0d`
- `EV-ZLIB-INFCOVER-006` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/test/infcover.c` — SHA-256 `37718912b22c68942a469f971cbb47500d24dc4f6258db271edd417f0eb69a5e`
- `EV-ZLIB-INFLATE-H-007` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/inflate.h` — SHA-256 `e6a43bd0e24ab2cf5fa1dca630859e9a2f6a721f033f75faf179f5c0299e4fe2`

## Reviewer-visible defect taxonomy

- **D1**: Use before successful initialization
- **D2**: Use after failed initialization or activation
- **D3**: Use after close, destroy, end, or release
- **D4**: Double close, destroy, end, or release
- **D5**: Missing cleanup on a success or failure exit
- **D6**: Invalid API call ordering or missing prerequisite call
- **D7**: Ownership misuse: freeing borrowed data, failing transferred ownership, or wrong owner
- **D8**: Conditionally invalid cleanup or cleanup under the wrong state or return condition

## Key V2 semantic clarifications

1. `DEFLATE_READY` and `DEFLATE_ACTIVE` are documented call-history abstractions, not exact private implementation statuses.
2. `INIT_FAILED` and `RELEASED` are terminal for the current logical resource instance. Later reuse begins a fresh logical FSM instance.
3. The transition relation is obligation-driven and partial. An absent transition alone does not imply validity or violation.
4. Repeated `inflate()` from `INFLATE_STREAM_END` is modeled by `T17`, returning `Z_STREAM_END` and remaining in `INFLATE_STREAM_END`.
5. `T15` is destination-side acquisition for successful `inflateCopy`; it has been removed from source-oriented `ZLIB-R02`.
6. Core z_stream lifecycle obligations apply to supported zlib, raw, and gzip-wrapper modes. gzip wrapper mode is not globally excluded.
7. Wrapper-specific or other unmodeled stateful APIs listed in the draft remain explicitly outside this scenario-bounded modeled API set.
8. Human-accepted candidate `ZLIB-CAND-R14` is promoted to core `ZLIB-R14` (`D7`).

## V1-review closure checks

For each item below, record exactly `PASS`, `REVISION_REQUIRED`, or `FAIL`.

### Closure 1

Revision implemented: Corrected EV-ZLIB-TEST-005; no reset-workflow claim.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:

### Closure 2

Revision implemented: Added pinned inflate.h evidence and T17 repeated-inflate Z_STREAM_END self-transition.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:

### Closure 3

Revision implemented: Added reviewer-visible frozen D1-D8 definitions.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:

### Closure 4

Revision implemented: Defined DEFLATE_READY/DEFLATE_ACTIVE as documented call-history abstractions rather than exact private statuses.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:

### Closure 5

Revision implemented: Defined INIT_FAILED and RELEASED as terminal for the current logical resource instance; later reuse starts a fresh logical lifecycle.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:

### Closure 6

Revision implemented: Removed T15 from source-oriented ZLIB-R02 and retained T15 only as destination acquisition semantics.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:

### Closure 7

Revision implemented: Defined the FSM as an obligation-driven partial transition relation; absence does not silently imply validity.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:

### Closure 8

Revision implemented: Explicitly listed reviewer-identified additional stateful APIs as outside this scenario-bounded modeled API set.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:

### Closure 9

Revision implemented: Reconciled gzip scope with frozen S03: core z_stream lifecycle obligations include supported gzip wrapper mode; wrapper-specific extra APIs remain separately scoped.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:

### Closure 10

Revision implemented: Promoted human-accepted ZLIB-CAND-R14 to core ZLIB-R14 with D7 ownership semantics.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:


## Mandatory review checks

Record exactly `PASS`, `REVISION_REQUIRED`, or `FAIL`.

### 1. Evidence completeness

Decision:

Notes:

### 2. Transition consistency

Decision:

Notes:

### 3. Ownership effects

Decision:

Notes:

### 4. Terminal / permitted exit states

Proposed permitted exits remain:

- `UNINITIALIZED`
- `INIT_FAILED`
- `RELEASED`

Decision:

Notes:

### 5. Unsupported conditions and scope

Decision:

Notes:

## Specific R14 review

Please verify the promoted core rule `ZLIB-R14`.

Confirm whether the following is sufficiently supported:

`inflateCopy` destination must not already own any live modeled zlib internal state before copy; successful copy acquires an independent destination state that later requires `inflateEnd`.

Decision: `PASS / REVISION_REQUIRED / FAIL`

Notes:

## Overall human-review decision

Choose exactly one:

- [ ] `APPROVE_EXACT_DRAFT_FOR_FINALIZATION`
- [ ] `REVISION_REQUIRED`
- [ ] `REJECT`

Summary:

Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

## Important immutability rule

If the decision is `REVISION_REQUIRED`, do not edit this V2 file in place. A new successor author checkpoint must be created and reviewed as a new immutable target.

If the decision is `APPROVE_EXACT_DRAFT_FOR_FINALIZATION`, no semantic change may be introduced during finalization. Only the deferred freeze dates and Decision-0018 content hashes may be added before validation and canonical freeze.
