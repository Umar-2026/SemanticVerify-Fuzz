# zlib Source-Only Protocol Specification Review Packet V1

## Exact immutable review target

Author role: `Spec-Author-1`
Reviewer role: `Spec-Reviewer-1`
Reviewer underlying role: `Adjudicator-C`

Draft:

`evidence/annotation\_preparation/specification\_reconciliation\_v1/zlib\_working\_draft\_v1/zlib\_source\_only\_working\_fsm\_draft.v1.json`

Draft SHA-256:

`cb2738329164537bba86282668bfabf51599fac1292309f150a68a32f2571573`

Pinned zlib revision:

`da607da739fa6047df13e66a2af6b8bec7c2a498`

This artifact is an author checkpoint only.
It is **not** a frozen protocol specification.

The reviewer must not consult generated fuzz drivers, selected-sample
membership, raw model responses, generated compiler-log semantic contents,
gold labels, analyzer output, baseline output, controlled LLM-review output,
repair output, or failure-prompted post-hoc evidence.

Integrity verification

Draft SHA-256: MATCH

SHA256SUMS.txt pristine-package verification: 9/9 OK

Declared evidence content hashes: 6/6 MATCH

Unresolved cited evidence IDs: 0

Declared but uncited evidence IDs: 0

Obligation count: 13

Transition count: 16

JSON well-formedness: PASS

The 9/9 result applies to the pristine ZIP before the review form is edited.

Editing 02\_zlib\_spec\_reviewer\_packet.v1.md changes its hash. If that is the

only changed package file, re-running the original manifest check in the

working directory will naturally report 8/9 OK, with only that review-form

entry failing. This post-edit 8/9 result does not alter the immutable draft or

the six evidence files and must not be misreported as the pristine ZIP result.

Hash binding proves that the packaged evidence bytes match the hashes

declared by the draft. The ZIP alone does not independently authenticate

that those bytes originated from Git commit

da607da739fa6047df13e66a2af6b8bec7c2a498.

## Mandatory review checks

Record exactly `PASS`, `REVISION\_REQUIRED`, or `FAIL`.

### 1. Evidence completeness

Decision: REVISION\_REQUIRED

Notes: All six declared evidence files exist, their hashes match, all cited IDs

resolve, and no declared evidence item is uncited.

Five provenance rationales are supported by their cited files. However,

EV-ZLIB-TEST-005 inaccurately states that example.c demonstrates reset

workflows. example.c demonstrates init-use-end ordering and calls

deflateSetDictionary after successful initialization, but contains no

deflateReset or inflateReset call.

The approved evidence is insufficient to determine exact repeated inflate

behavior after Z\_STREAM\_END. inflate.c sets mode to DONE and returns

Z\_STREAM\_END. inflateStateCheck accepts only modes in the HEAD-to-SYNC range,

but inflate.h is absent and the DONE-to-SYNC enum ordering is not defined in

any approved evidence file.

No generic requirement to add deflate.h is asserted. deflate.h should be

required only if a specific reviewed conclusion actually depends on a private

deflate status, enum membership, macro definition, or ordering that the

approved evidence does not otherwise establish.

The draft uses all defect-category labels D1 through D8, including D7 for

ZLIB-CAND-R14, but neither the immutable draft nor the package instructions

define any of them. Category correctness therefore cannot be independently

reviewed from the supplied package.

These are correctable rationale and evidence-sufficiency deficiencies, so

REVISION\_REQUIRED rather than FAIL is appropriate.

### 2. Transition consistency

Decision: REVISION\_REQUIRED

Notes: The transition graph is structurally consistent. State, event, and

transition identifiers are unique; every reference resolves; and all eight

states are graph-reachable from UNINITIALIZED. E11\_FUNCTION\_EXIT is the only

event without a state transition and serves as an exit-obligation trigger.

The initialization, stream-end, reset, End, dictionary, inflate, and

inflateCopy outcome transitions are generally supported. Three semantic

ambiguities require revision.

First, T03 sends every live non-Z\_STREAM\_END deflate result from

DEFLATE\_READY to DEFLATE\_ACTIVE. A direct invalid-flush return occurs before

the implementation changes INIT\_STATE to BUSY\_STATE, so an

implementation-status interpretation can leave the dictionary guard

satisfied. However, zlib.h requires a zlib-format dictionary before any call

of deflate and treats a prior deflate call as documented inconsistent state.

T03 is therefore defensible as a documented call-history transition but not

as an exact internal-status transition. The draft must define which

abstraction DEFLATE\_READY and DEFLATE\_ACTIVE represent. A post-error

dictionary call must not be described as documented-valid.

Second, INIT\_FAILED and RELEASED have no outgoing transitions. They are

permitted exit states, but the draft does not state whether they are terminal

for the current FSM instance or whether retry/reinitialization starts a fresh

lifecycle at UNINITIALIZED. The successor must model retry where intended or

define the terminal/fresh-resource lifecycle semantics.

Third, the table has no inflate transition from INFLATE\_STREAM\_END even

though the draft asserts no general post-Z\_STREAM\_END inflate prohibition.

Exact repeated-call behavior depends on enum ordering missing from the

approved evidence. The successor must add sufficient evidence and model the

behavior, or explicitly exclude it under defined transition-table semantics.

### 3. Ownership effects

Decision: REVISION\_REQUIRED

Notes: The individual transition ownership effects are supported at the aggregate

z\_stream-resource level. Successful initialization/copy acquires a live

state, failed acquisition does not leave a live state, reset retains

ownership, and End frees the corresponding state and nulls the state pointer.

A cross-resource association requires revision. ZLIB-R02 is source-oriented:

its resource\_kind is zlib.z\_stream.inflate, its trigger includes

inflateCopy(source), and its ownership\_effect is NONE. Its permitted

transitions nevertheless include T15. E10 explicitly states that inflateCopy

transitions are tracked for the destination, and T15 moves that destination

from UNINITIALIZED to INFLATE\_LIVE with ACQUIRE. T15 is correctly associated

with destination-oriented ZLIB-R09 but must not serve as the source-side

transition for ZLIB-R02.

The successor should remove T15 from ZLIB-R02 and represent source validity

as a non-transitioning precondition or a separate ownership-neutral

source-side transition. Accepting ZLIB-CAND-R14 does not repair this separate

source-versus-destination mismatch.

### 4. Terminal / permitted exit states

Proposed permitted exits:

- UNINITIALIZED
- INIT\_FAILED
- RELEASED

Decision: PASS

Notes: UNINITIALIZED has no successfully acquired live state. INIT\_FAILED follows an

unsuccessful acquisition; early failures occur before acquisition, partial

deflate initialization invokes cleanup, and failed inflate initialization

frees and nulls its state. RELEASED follows the corresponding End operation,

which frees and nulls the internal state.

No modeled live state is listed as a permitted exit. ZLIB-R07 through

ZLIB-R09 require successfully initialized or copied resources to reach

RELEASED on relevant function exits. The permitted exit set therefore does

not authorize exit while a modeled live resource remains owned.

### 5. Unsupported conditions and scope

Decision: REVISION\_REQUIRED

Notes: The draft does not define open-world or closed-world transition semantics and

does not explain whether absence from the table means invalid behavior or

behavior outside scope.

This ambiguity affects post-Z\_STREAM\_END inflate behavior: the scope text

asserts no general prohibition, while no E07\_INFLATE transition exists from

INFLATE\_STREAM\_END. If the behavior is to be classified or modeled,

sufficient enum evidence must be supplied. Alternatively, it may be placed

explicitly outside scope if the meaning of table absence is defined.

The API boundary is incomplete. E01-E10 are API-call events and E11 is a

function-exit event; S01-S10 are scenarios, not an event set. The draft gives

no treatment for several stateful APIs, including deflateCopy,

deflateParams, deflateResetKeep, deflateSetHeader, inflateSetDictionary,

inflateReset2, inflatePrime, inflateSync, and inflateGetHeader. A general

rule or explicit relevant exclusions are required.

Excluding gzFile APIs does not exclude gzip-wrapper stream mode. The modeled

deflateInit2 and inflateInit2 APIs can select optional gzip mode. The source

conditionally supports these paths under GZIP and GUNZIP, while no pinned

build configuration is supplied. The successor must include or exclude

gzip-wrapper mode explicitly and state whether its claims are conditional on

source configuration or tied to a pinned build configuration.

## Candidate rule ZLIB-CAND-R14

Proposition:

`inflateCopy` destination should not already own a live inflate state before
copy because the pinned implementation allocates and assigns a new
destination state without releasing a prior destination state.

This candidate is intentionally outside the 13 core obligations pending
human review.

Choose exactly one:

- \[x] ACCEPT
- \[ ] REJECT
- \[ ] REVISION\_REQUIRED

Reason:

inflateCopy validates the source state and checks only that the destination

pointer is non-null. It allocates the copied state and optional window, then

copies the complete source z\_stream over the destination and installs the new

destination state. It does not inspect, end, or free any state already owned

by the destination. A destination already owning a live state would therefore

have its prior state pointer and allocator metadata overwritten without

release, making the prior allocation unreachable.

The public header describes copy semantics and return values but does not

state a destination pre-state requirement. The pinned implementation directly

supports this source-only ownership rule.

When promoted, the obligation should cite EV-ZLIB-INF-003. If its rationale

relies on public-header silence, it should also cite EV-ZLIB-H-001 as

contextual evidence. It should either cover any prior live modeled

zlib.z\_stream.internal\_state or explain why it intentionally covers only a

prior live inflate state.

## Overall human-review decision

Choose exactly one:

- \[ ] APPROVE\_EXACT\_DRAFT\_FOR\_FINALIZATION
- \[x] REVISION\_REQUIRED
- \[ ] REJECT

Summary:

1\. Evidence completeness: REVISION\_REQUIRED

2\. Transition consistency: REVISION\_REQUIRED

3\. Ownership effects: REVISION\_REQUIRED

4\. Terminal / permitted exit states: PASS

5\. Unsupported conditions and scope: REVISION\_REQUIRED

ZLIB-CAND-R14: ACCEPT

The checkpoint is not rejected. Its integrity, evidence hash binding,

identifier resolution, graph reachability, basic ownership lifecycle, and

permitted exits are sound. The correctable rationale, evidence, abstraction,

resource-association, and scope issues above require a successor author

revision.

The current checkpoint

cb2738329164537bba86282668bfabf51599fac1292309f150a68a32f2571573

must remain immutable and must not be edited in place. The successor must be

reviewed as a new immutable target.

Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 15 / August / 2026
