# zlib Source-Only Protocol Specification Successor Review Packet V2

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

Draft:

`evidence/annotation\\\_preparation/specification\\\_reconciliation\\\_v1/zlib\\\_working\\\_draft\\\_v2/zlib\\\_source\\\_only\\\_successor\\\_working\\\_fsm\\\_draft.v2.json`

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

The prior overall decision was `REVISION\\\_REQUIRED`.

The prior reviewer accepted `ZLIB-CAND-R14`; V2 promotes it to core rule `ZLIB-R14`.

## Review quarantine

The reviewer must use only the approved source evidence listed below.

Do **not** consult generated fuzz drivers, selected-sample membership, raw model responses, generated compiler-log semantic contents, gold labels, analyzer output, baseline output, controlled LLM-review output, repair output, or failure-prompted post-hoc evidence.

## Integrity and structure

Expected V2 structure:

* States: 8
* Events: 11
* Transitions: 17
* Core obligations: 14
* Provenance evidence items: 7
* Canonical specification frozen: NO
* Human review completed for V2: NO

Working-draft `freeze\\\_date` and `content\\\_sha256` fields remain intentionally deferred until exact human approval and finalization.

## Approved source evidence

* `EV-ZLIB-H-001` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/zlib.h` — SHA-256 `818667d6ab6a37fe7469cb06a7f0cb2c2cb2f2c948a03e5accf1a4a74bf3020a`
* `EV-ZLIB-DEF-002` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/deflate.c` — SHA-256 `ea9ca4eb51b1a71aaf214b99f4a9fab177253d6268cae8e4c26d44d1812e52c2`
* `EV-ZLIB-INF-003` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/inflate.c` — SHA-256 `90221ea7d762e7044057f6ad5013e969086c6ba3d3051716b7aa786d7a6362ec`
* `EV-ZLIB-ZPIPE-004` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/examples/zpipe.c` — SHA-256 `e79717cefd20043fb78d730fd3b9d9cdf8f4642307fc001879dc82ddb468509f`
* `EV-ZLIB-TEST-005` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/test/example.c` — SHA-256 `be1b050aad808cdb016c01f42568d3a62ee37dd7b2b56bef0ade21be8d9fee0d`
* `EV-ZLIB-INFCOVER-006` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/test/infcover.c` — SHA-256 `37718912b22c68942a469f971cbb47500d24dc4f6258db271edd417f0eb69a5e`
* `EV-ZLIB-INFLATE-H-007` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/inflate.h` — SHA-256 `e6a43bd0e24ab2cf5fa1dca630859e9a2f6a721f033f75faf179f5c0299e4fe2`

## Reviewer-visible defect taxonomy

* **D1**: Use before successful initialization
* **D2**: Use after failed initialization or activation
* **D3**: Use after close, destroy, end, or release
* **D4**: Double close, destroy, end, or release
* **D5**: Missing cleanup on a success or failure exit
* **D6**: Invalid API call ordering or missing prerequisite call
* **D7**: Ownership misuse: freeing borrowed data, failing transferred ownership, or wrong owner
* **D8**: Conditionally invalid cleanup or cleanup under the wrong state or return condition

## Key V2 semantic clarifications

1. `DEFLATE\\\_READY` and `DEFLATE\\\_ACTIVE` are documented call-history abstractions, not exact private implementation statuses.
2. `INIT\\\_FAILED` and `RELEASED` are terminal for the current logical resource instance. Later reuse begins a fresh logical FSM instance.
3. The transition relation is obligation-driven and partial. An absent transition alone does not imply validity or violation.
4. Repeated `inflate()` from `INFLATE\\\_STREAM\\\_END` is modeled by `T17`, returning `Z\\\_STREAM\\\_END` and remaining in `INFLATE\\\_STREAM\\\_END`.
5. `T15` is destination-side acquisition for successful `inflateCopy`; it has been removed from source-oriented `ZLIB-R02`.
6. Core z\_stream lifecycle obligations apply to supported zlib, raw, and gzip-wrapper modes. gzip wrapper mode is not globally excluded.
7. Wrapper-specific or other unmodeled stateful APIs listed in the draft remain explicitly outside this scenario-bounded modeled API set.
8. Human-accepted candidate `ZLIB-CAND-R14` is promoted to core `ZLIB-R14` (`D7`).

## V1-review closure checks

For each item below, record exactly `PASS`, `REVISION\\\_REQUIRED`, or `FAIL`.

### Closure 1

Revision implemented: Corrected EV-ZLIB-TEST-005; no reset-workflow claim.



Decision: `REVISION\_REQUIRED`



Notes: EV-ZLIB-TEST-005's provenance rationale was corrected to state that `example.c` does not demonstrate `deflateReset` or `inflateReset` workflows, and the packaged `example.c` contains no such calls. However, `ZLIB-R12` is specifically a `deflateReset`/`inflateReset` obligation and still lists `EV-ZLIB-TEST-005` in its `source\_evidence`. The reset-workflow evidence attribution has therefore not been removed consistently. `EV-ZLIB-TEST-005` should be removed from `ZLIB-R12` in a new successor checkpoint while the applicable header and implementation evidence is retained.



### Closure 2

Revision implemented: Added pinned inflate.h evidence and T17 repeated-inflate Z\_STREAM\_END self-transition.



Decision: `PASS`



Notes: Verified that `EV-ZLIB-INFLATE-H-007` is present with the expected SHA-256. `T17` models `INFLATE\_STREAM\_END` as an `inflate`/`Z\_STREAM\_END` self-transition. `inflate.h` defines `DONE` as remaining until reset, `inflate.c` returns `Z\_STREAM\_END` from `DONE`, and `T17` is included in `ZLIB-R02`.

### Closure 3

Revision implemented: Added reviewer-visible frozen D1-D8 definitions.



Decision: `PASS`



Notes: Verified that the reviewer-visible D1-D8 taxonomy is present in the V2 JSON and matches the review-packet definitions. All core obligations use only defined D1-D8 categories, and every category is represented by at least one core obligation.

### Closure 4

Revision implemented: Defined DEFLATE\_READY/DEFLATE\_ACTIVE as documented call-history abstractions rather than exact private statuses.



Decision: `PASS`



Notes: Verified that `DEFLATE\_READY` and `DEFLATE\_ACTIVE` are explicitly defined as documented call-history abstractions. The draft sets `private\_implementation\_status\_equivalence` to `false`. `T01`, `T03`, `T04`, `T06`, `T07`, and `T08` use these abstractions consistently, and no contradictory claim equating them with exact private implementation statuses was found.

### Closure 5

Revision implemented: Defined INIT\_FAILED and RELEASED as terminal for the current logical resource instance; later reuse starts a fresh logical lifecycle.



Decision: `PASS`



Notes: Verified that `INIT\_FAILED` and `RELEASED` are explicitly terminal for their current logical resource instances. The draft states that later initialization or copy begins a fresh FSM instance. No transition has `INIT\_FAILED` or `RELEASED` as a from-state. `ZLIB-R03` through `ZLIB-R06` are consistent with these semantics, and the permitted exits are limited to `UNINITIALIZED`, `INIT\_FAILED`, and `RELEASED`.



### Closure 6

Revision implemented: Removed T15 from source-oriented ZLIB-R02 and retained T15 only as destination acquisition semantics.



Decision: `PASS`



Notes: Verified that `T15` is absent from source-oriented `ZLIB-R02`, whose permitted transitions are `T11`, `T12`, `T14`, and `T17`. `T15` is explicitly modeled as the successful destination-side `ACQUIRE` transition for `inflateCopy`. The event description, source/destination clarification, `ZLIB-R09`, and `ZLIB-R14` consistently distinguish source validity from destination acquisition and cleanup.

### Closure 7

Revision implemented: Defined the FSM as an obligation-driven partial transition relation; absence does not silently imply validity.



Decision: `PASS`



Notes: Verified that the FSM is explicitly defined as an obligation-driven partial transition relation and not a closed-world model of all zlib behavior. The draft states that an absent transition alone establishes neither validity nor violation, and that a protocol violation requires an explicit obligation. The unsupported-conditions section repeats this interpretation, with no contradictory blanket rule found.

### Closure 8

Revision implemented: Explicitly listed reviewer-identified additional stateful APIs as outside this scenario-bounded modeled API set.



Decision: `PASS`



Notes: Verified that the nine reviewer-identified stateful APIs are explicitly listed as outside the scenario-bounded modeled API set in both the reviewer-visible semantics and unsupported-conditions sections. Unmodeled interactions are not treated as silently valid, the excluded APIs do not appear as modeled events or transitions, and the `gzFile` and `inflateBack` families are separately identified as out of scope.



### Closure 9

Revision implemented: Reconciled gzip scope with frozen S03: core z\_stream lifecycle obligations include supported gzip wrapper mode; wrapper-specific extra APIs remain separately scoped.



Decision: `REVISION\_REQUIRED`



Notes: The V2 gzip-wrapper clarification is internally consistent and supported by `zlib.h` and `inflate.h`. Core lifecycle modes include zlib, raw deflate, and supported gzip-wrapper operation; build availability is appropriately qualified; and wrapper-specific APIs remain separately scoped. However, the package contains only the S03 identifier and task slug, not the frozen S03 artifact or pinned content. The claimed exact reconciliation with frozen S03 cannot therefore be independently verified from the approved review package. A pinned frozen-S03 artifact or approved reference should be supplied in a successor review package.

### Closure 10



Revision implemented: Promoted human-accepted ZLIB-CAND-R14 to core ZLIB-R14 with D7 ownership semantics.



Decision: `PASS`



Notes: Verified that accepted candidate `ZLIB-CAND-R14` has been promoted to core obligation `ZLIB-R14`. The pending-candidate list is empty, historical metadata identifies `ZLIB-CAND-R14` as the accepted candidate, and the active rule is classified as D7 with destination-side `ACQUIRE` semantics. Its precondition, cleanup responsibility, and `T15` linkage consistently describe fresh-destination ownership and subsequent `inflateEnd` cleanup.Mandatory review checks

Record exactly `PASS`, `REVISION\\\_REQUIRED`, or `FAIL`.

### 1\. Evidence completeness

Decision: `REVISION\_REQUIRED`



Notes: All seven approved evidence files are present, readable, and hash-valid. The JSON contains seven provenance entries, all obligation evidence IDs are defined, `T17` is linked to the appropriate `inflate.c` and `inflate.h` evidence, and no generated corpus is declared as specification evidence. However, `ZLIB-R12` still cites `EV-ZLIB-TEST-005` for reset behavior even though its rationale and `example.c` explicitly provide no reset workflow. The review packet's stated nested JSON path also does not match the packaged root location, although the SHA-256 unambiguously identifies the target. In addition, no separate pinned frozen-S03 artifact is supplied for independently checking the claimed exact S03 reconciliation. These repairable evidence and packaging issues require correction or clarification in a successor review package.

### 2\. Transition consistency

Decision: `PASS`



Notes: Verified all 8 states, 11 events, and 17 uniquely numbered transitions. All transition state and event references are defined. Initialization, deflate, inflate, reset, End, stream-end, and `inflateCopy` transitions are internally consistent, with mutually exclusive success/failure predicates. Ownership effects consistently use `ACQUIRE` for `T01`, `T09`, and `T15`, `RELEASE` for `T05` and `T13`, and `NONE` otherwise. All obligation transition references exist and match their modeled roles. Function exit is coherently governed by explicit cleanup obligations and permitted-exit states within the documented partial-transition model.

### 3\. Ownership effects

Decision: `PASS`



Notes: Verified that successful deflate initialization, inflate initialization, and `inflateCopy` destination creation are modeled as `ACQUIRE`; `deflateEnd` and `inflateEnd` are modeled as `RELEASE`; and reset retains ownership. Failed acquisitions create no normal successful-init cleanup obligation. The exit-cleanup and exactly-one-release rules are consistent with the transition model and source implementations. `inflateCopy` allocates an independent destination state without releasing source ownership, while overwriting a previously live destination would lose its existing state; this supports the fresh-destination ownership restriction. Permitted terminal states carry no outstanding live ownership.

### 4\. Terminal / permitted exit states

Proposed permitted exits remain:

* `UNINITIALIZED`
* `INIT\\\_FAILED`
* `RELEASED`



Decision: `PASS`



Notes: Verified that permitted exits are exactly `UNINITIALIZED`, `INIT\_FAILED`, and `RELEASED`. These states carry no outstanding successfully acquired live ownership. All deflate and inflate live or stream-end states remain excluded from permitted exits and are covered by function-exit cleanup obligations. Stream end is correctly distinguished from resource release. `INIT\_FAILED` and `RELEASED` terminate only the current logical FSM instance, with later reuse beginning a fresh instance. `T05` also correctly models actual release by `deflateEnd` even when its final return can be `Z\_DATA\_ERROR`.



### 5\. Unsupported conditions and scope

Decision: `PASS`



Notes: Verified that the scenario-bounded scope explicitly excludes the `gzFile` and `inflateBack` families and the nine identified additional stateful APIs. Supported zlib, raw-deflate, and gzip-wrapper modes remain covered by the core `z\_stream` lifecycle, while wrapper-specific APIs are separately scoped. The draft consistently treats the transition relation as partial, models repeated `inflate` after stream end through `T17`, limits the raw-deflate dictionary exception, excludes unrelated correctness and memory-safety defects, and defines the scenario boundary as S01 through S10 without included/excluded API contradictions.

## Specific R14 review

Please verify the promoted core rule `ZLIB-R14`.

Confirm whether the following is sufficiently supported:

`inflateCopy` destination must not already own any live modeled zlib internal state before copy; successful copy acquires an independent destination state that later requires `inflateEnd`.



Decision: `PASS`



Notes: `ZLIB-R14` is sufficiently supported by the approved source evidence. `inflateCopy` validates the source and requires a non-null destination, then allocates an independent inflate state and, when needed, an independent window for the destination. The successful path overwrites the destination without checking or releasing any pre-existing destination state. A destination that already owns live internal state could therefore lose that ownership reference, supporting the fresh/uninitialized destination precondition. Successful copy requires a later `inflateEnd`, as confirmed by `inflateEnd` and the successful `inflateCopy`/`inflateEnd` workflow in `infcover.c`. Failed copy does not establish destination ownership. The public header does not state the fresh-destination requirement as an explicit sentence, but the approved implementation evidence sufficiently establishes the ownership constraint for this source-only specification.

## Overall human-review decision

Choose exactly one:

* \[ ] `APPROVE\\\_EXACT\\\_DRAFT\\\_FOR\\\_FINALIZATION`
* \[x] REVISION\_REQUIRED
* \[ ] `REJECT`



Summary

Closure 1:  REVISION\_REQUIRED

Closure 2:  PASS

Closure 3:  PASS

Closure 4:  PASS

Closure 5:  PASS

Closure 6:  PASS

Closure 7:  PASS

Closure 8:  PASS

Closure 9:  REVISION\_REQUIRED

Closure 10: PASS



Evidence completeness:              REVISION\_REQUIRED

Transition consistency:             PASS

Ownership effects:                  PASS

Terminal / permitted exit states:   PASS

Unsupported conditions and scope:   PASS

Specific R14 review:                PASS

Summary: The V2 draft substantially resolves the prior review concerns. Closures 2 through 8 and Closure 10 pass, and the transition model, ownership effects, permitted exit states, unsupported-condition scope, and promoted `ZLIB-R14` are internally consistent and supported by the approved source evidence.



Revision remains required because Closure 1 was not implemented consistently: `EV-ZLIB-TEST-005` correctly states that `example.c` does not demonstrate `deflateReset` or `inflateReset` workflows, but `ZLIB-R12` still cites that evidence for its reset obligation. `EV-ZLIB-TEST-005` should be removed from `ZLIB-R12`'s `source\_evidence`.



The review package also names a nested location for the immutable JSON that does not match its packaged root location. Additionally, the package contains only the S03 identifier and task slug, not a pinned frozen-S03 artifact, so the claimed exact reconciliation with frozen S03 cannot be independently reproduced from the approved package. The target remains identifiable by its matching SHA-256, but these evidence and packaging issues should be corrected or explicitly resolved in a new immutable successor review package.



Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation:

I confirm that I independently reviewed the exact V2 draft using only the

approved packaged source evidence and recorded the decision above.

Human reviewer date: 16 / August / 2026

## Important immutability rule

If the decision is `REVISION\\\_REQUIRED`, do not edit this V2 file in place. A new successor author checkpoint must be created and reviewed as a new immutable target.

If the decision is `APPROVE\\\_EXACT\\\_DRAFT\\\_FOR\\\_FINALIZATION`, no semantic change may be introduced during finalization. Only the deferred freeze dates and Decision-0018 content hashes may be added before validation and canonical freeze.

