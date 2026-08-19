# curl Technical Protocol Working Draft V2 — Independent Human Review Packet

## Purpose

This is an independent human technical-specification review of the exact

immutable curl Technical Protocol Working Draft V2 successor.

Working Draft V1 received an overall independent human-review decision of

`REVISION\_REQUIRED`.

V2 is a new immutable successor and must be reviewed independently before any

separate canonicalization operation may be considered.

## Exact review target

Working draft:

`03\_curl\_technical\_protocol\_working\_draft.v2.json`

SHA-256:

`63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31`

Author checkpoint commit:

`a9042429155a161bd5c089910e7557b907808db6`

Author checkpoint tree:

`00a4fce0e91b0216e2e26efb46201e2aa9fa8f4c`

The supplied minimal Git witness must independently resolve the author

commit → tree → V2 target blob and Decision 0030 blob.

## Evidence boundary

Permitted evidence in this package:

exact Working Draft V2;

exact V2 author-resolution record;

Decision 0029 and Decision 0030;

exact completed V1 independent human technical review;

frozen V3 source-only scope;

source-evidence map;

approved source-evidence manifest;

the same 21 approved pinned curl source files;

minimal V2 author-checkpoint Git witness.

Not permitted as V2 technical-review evidence:

generated drivers;

selected-sample membership;

raw model responses;

generated-driver compiler-log semantic content;

gold labels;

analyzer output;

baseline output;

LLM-review output;

repair output.

## Decision choices

For every review item choose exactly one:

`PASS`

`REVISION\_REQUIRED`

`FAIL`

A `PASS` means the exact V2 treatment of that item is technically acceptable.

If `REVISION\_REQUIRED`, state the precise semantic change required.

Do not edit files under the immutable review-package copy. Complete only an

external editable reviewer-response copy prepared from this packet.

\---

### V2-RR01 — Exact V2 author-checkpoint identity and immutability

Decision: PASS

Notes: Exact Working Draft V2 SHA-256 confirmed:

63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31

Author checkpoint commit independently resolved:

a9042429155a161bd5c089910e7557b907808db6

The author checkpoint commit resolves to the expected tree:

00a4fce0e91b0216e2e26efb46201e2aa9fa8f4c

The V2 target path resolves to Git blob:

e9d323d5dac5ce8c28653fbb40868703daf15c4c

The resolved V2 Git blob is byte-identical to the packaged Working Draft V2.

The SHA-256 of the resolved V2 blob matches the declared V2 SHA-256.

The Decision 0030 path resolves from the same author checkpoint to Git blob:

2460750ba8ece9c5d74ff9accd122c7123fa24f2

The resolved Decision 0030 blob is byte-identical to the packaged Decision 0030 copy.

Decision 0030 records the same Working Draft V2 path and SHA-256.

The minimal Git witness contains exactly eight objects.

The witness contains one commit, five trees, and only the two expected file blobs.

The author commit records the V2 successor-authorization commit as its parent.

The parent commit object is intentionally absent from the minimal witness.

The V1 predecessor remains consistently bound to SHA-256:

80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6

The same V1 SHA-256 appears consistently in Decision 0029, Decision 0030, the successor authorization, the author-resolution record, and the completed V1 human review.

No evidence indicates that Working Draft V1 was edited in place.

The immutable V2 review package contains exactly 40 expected files.

All immutable-package file hashes match the external handoff manifest.

All 39 internal checksum-manifest entries match their target files.

The immutable reviewer template remained unchanged.

The review was completed only in the external editable reviewer-response copy.

No evidence of silent in-place modification of the V2 review target was found.



Confirm:

exact V2 SHA-256;

author checkpoint commit and tree;

V2 target Git blob;

Decision 0030 Git blob;

V1 remains immutable;

no silent in-place modification occurred.

\---

### V2-RR02 — Frozen scope and successor boundary

Decision: PASS

Notes: Working Draft V2 contains exactly twelve curl functions.

The frozen V3 scope also contains exactly twelve curl functions.

The V2 and frozen V3 function sets are identical.

The exact frozen function surface is:

curl\_global\_init

curl\_global\_cleanup

curl\_easy\_init

curl\_easy\_setopt

curl\_easy\_perform

curl\_easy\_reset

curl\_easy\_cleanup

curl\_multi\_init

curl\_multi\_add\_handle

curl\_multi\_perform

curl\_multi\_remove\_handle

curl\_multi\_cleanup

No V2 rule references a function outside this frozen surface.

The pinned curl repository revision remains:

68720b4837284335b2d63cb358f8f6ce65f5bc55

The pinned curl source tree remains:

e23d273aeb073c04aa5b073b35c9fde16979c896

The packaged frozen V3 SHA-256 is:

ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb

The V2 governance record binds to the same frozen V3 SHA-256.

The V2 author-resolution record confirms that the API surface did not change.

The pinned curl revision did not change.

The scenario-manifest boundary did not change.

The approved source-evidence class did not change.

The packaged evidence contains no generated-driver artifact.

No V2 rule requires or cites generated-driver-derived evidence.

V2 records synthetic\_protocol\_events\_invented as false.

The V2 implemented-item set is exactly TS-RR05 through TS-RR14.

This implemented-item set matches the corrections authorized by Decision 0029.

No additional protocol function, source class, or generated-driver-derived rule was introduced.

The V2 changes remain bounded to the completed V1 human-review successor corrections.



Confirm:

exactly the frozen twelve curl functions remain in scope;

pinned curl revision is unchanged;

frozen V3 source-only scope is unchanged;

no generated-driver-derived rule was introduced;

V2 changes are bounded to the human-review successor corrections.

\---

### V2-RR03 — TS-RR05/TS-RR06: return-conditioned multi cleanup

Decision: PASS

Notes: The exact V2 draft and the approved pinned `lib/multi.c` source were reviewed for this item.

Only `curl\_multi\_cleanup` returning `CURLM\_OK` establishes `MULTI\_RELEASED`.

Only successful cleanup discharges the multi-handle cleanup obligation.

Only successful cleanup establishes complete structural detachment of remaining easy handles.

The pinned implementation clears easy-to-multi associations before freeing the multi handle and returning `CURLM\_OK`.

A non-`CURLM\_OK` return does not establish that the multi handle was released.

A non-`CURLM\_OK` return leaves the multi cleanup obligation outstanding.

The implementation can return an error before cleanup begins or while processing remaining easy handles.

Therefore, after failed cleanup, complete detachment cannot safely be assumed.

Membership facts not established by the failed cleanup are represented conservatively as unresolved.

Rule M24 explicitly applies to both `MULTI\_OWNED` and `MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN`.

The same return-conditioned release, obligation, and membership rules therefore apply from the post-error multi state.

The V2 treatment is conservative and consistent with the approved pinned source evidence.

No semantic revision is required for this review item.



Review whether:

only `curl\_multi\_cleanup == CURLM\_OK` establishes `MULTI\_RELEASED`;

only successful cleanup discharges the multi cleanup obligation;

only successful cleanup establishes complete structural detachment;

non-`CURLM\_OK` cleanup does not assert release;

non-`CURLM\_OK` cleanup preserves the cleanup obligation;

unresolved membership after failed cleanup is represented conservatively;

the same rules apply from the post-error multi state.

\---

### V2-RR04 — TS-RR07: exact four-verdict contract

Decision: PASS

Notes: The exact V2 JSON was manually reviewed for every populated machine-readable verdict field.

The declared `allowed\_machine\_verdicts` list contains exactly:

`VALID`

`VIOLATION-MUST`

`VIOLATION-MAY`

`UNKNOWN`

All rule-level `verdict` fields use only values from this declared four-verdict set.

All `missing\_cleanup\_verdict` fields also use only values from this declared set.

The populated verdict fields comprise 29 `VIOLATION-MUST`, 6 `VALID`, and 1 `UNKNOWN` values.

No populated rule currently requires `VIOLATION-MAY`, but it remains a declared valid verdict.

No undeclared qualified verdict, including an `UNKNOWN\_PENDING\_\*` variant, appears in a machine-readable verdict field.

Classification details are stored separately in fields such as `classification\_note`, `enforcement`, and `condition`.

Review and provenance information is stored separately in fields such as `review\_item`, `human\_review\_item`, `resolution`, and `current\_draft\_behavior`.

Text such as `UNKNOWN pending independent review` occurs only as separate historical or explanatory information and does not create an additional machine verdict.

The `open\_independent\_review\_items` field is separate from the verdict contract and is currently empty.

The exact four-verdict machine-readable contract is preserved.

No semantic revision is required for this review item.



Confirm that machine-readable verdict fields use only:

`VALID`

`VIOLATION-MUST`

`VIOLATION-MAY`

`UNKNOWN`

Confirm that scoped, pending, explanatory, or review information is stored

separately and does not create undeclared verdict variants.

\---

### V2-RR05 — TS-RR08: D1, D2, D4 and NULL cleanup cases

Decision: REVISION\_REQUIRED

Notes: The exact V2 draft, frozen V3 defect projection, completed V1 review, and approved pinned source evidence were reviewed for this item.

Rules E14 through E16 explicitly classify `curl\_easy\_setopt`, `curl\_easy\_perform`, and `curl\_easy\_reset` before successful easy-handle acquisition as D1 `VIOLATION-MUST`.

Rules E17 through E19 explicitly classify those operations on a NULL `curl\_easy\_init` result as D2 `VIOLATION-MUST`.

Rules M16 through M18 provide D1 classifications for `curl\_multi\_add\_handle`, `curl\_multi\_perform`, and `curl\_multi\_remove\_handle` when no multi handle was successfully acquired.

Rules M19 through M21 provide corresponding D2 classifications when the multi argument is a NULL `curl\_multi\_init` result.

However, `curl\_multi\_add\_handle` and `curl\_multi\_remove\_handle` consume both a multi handle and an easy handle.

Rule M04 requires the easy handle to be live, but the draft does not assign a D1 or D2 defect and verdict when that easy-handle precondition is violated.

The pinned implementation explicitly validates the easy argument in both functions and returns `CURLM\_BAD\_EASY\_HANDLE` when it is not a valid easy handle.

The frozen V3 defect projection requires an easy-handle operation before successful easy-handle acquisition to map to D1.

The frozen V3 defect projection also requires an easy-handle operation on a NULL `curl\_easy\_init` result to map to D2.

Therefore, the existing D1/D2 rules do not completely cover the dual-resource preconditions of `curl\_multi\_add\_handle` and `curl\_multi\_remove\_handle`.

Rules E21 and M23 correctly classify repeated easy and multi cleanup of the same released non-NULL resource as D4 `VIOLATION-MUST`.

Those cleanup-specific D4 rules explicitly take precedence over the generic D3 use-after-release rules.

Rule E20 correctly preserves `curl\_easy\_cleanup(NULL)` as a valid documented no-op.

Rule M22 correctly records that `curl\_multi\_cleanup(NULL)` returns `CURLM\_BAD\_HANDLE`.

Rule M22 correctly states that NULL multi cleanup releases no resource, detaches no membership, and discharges no cleanup obligation.

Rule M24 correctly preserves the multi cleanup obligation after a non-`CURLM\_OK` cleanup result.

The multi-handle exit obligation also correctly requires `curl\_multi\_cleanup` to return `CURLM\_OK` before the D5 cleanup obligation is discharged.

Required semantic change:

Create an immutable successor containing explicit D1 `VIOLATION-MUST` rules for `curl\_multi\_add\_handle` and `curl\_multi\_remove\_handle` when their easy argument is not backed by a successful easy-handle acquisition.

Add explicit D2 `VIOLATION-MUST` rules for the same functions when their easy argument is the NULL result of a failed `curl\_easy\_init`.

Record the pinned `CURLM\_BAD\_EASY\_HANDLE` result and absence of membership change for those invalid-easy cases.

Apply these easy-argument rules independently of the existing D1/D2 rules for the multi argument.

Preserve the existing `curl\_easy\_cleanup(NULL)` exception and the existing `curl\_multi\_cleanup(NULL)` return-conditioned behavior.



Review:

explicit D1 rules before successful easy/multi acquisition;

explicit D2 rules after failed/NULL acquisition;

cleanup-specific D4 rules for repeated easy/multi cleanup after release;

precedence of cleanup-specific D4 over generic D3 use-after-release;

`curl\_easy\_cleanup(NULL)` no-op exception;

`curl\_multi\_cleanup(NULL)` returning `CURLM\_BAD\_HANDLE`;

NULL multi cleanup releasing nothing and discharging no obligation;

failed multi cleanup not discharging the D5 exit obligation.

\---

### V2-RR06 — TS-RR09: explicit global cleanup obligation at exit

Decision: REVISION\_REQUIRED

Notes: The exact V2 global-runtime rules, exit-obligation table, resource metadata, completed V1 review, and approved source evidence were reviewed.

Rule G01 establishes `EXPLICIT\_CLEANUP\_DUE` after successful explicit `curl\_global\_init` from an uninitialized runtime.

Rule G02 also establishes `EXPLICIT\_CLEANUP\_DUE` when successful explicit initialization occurs after implicit readiness.

Rule G10 classifies program exit with `EXPLICIT\_CLEANUP\_DUE` as defect D5.

Rule G10 assigns enforcement `MUST`.

Rule G10 assigns verdict `VIOLATION-MUST`.

The separate exit-obligation entry agrees with G10.

That entry records defect D5, enforcement `MUST`, and `missing\_cleanup\_verdict` equal to `VIOLATION-MUST`.

The approved documentation supports a corresponding `curl\_global\_cleanup` for each explicit `curl\_global\_init`.

The draft correctly states that the explicit obligation is established only by successful explicit `curl\_global\_init`.

The draft correctly states that implicit readiness created by successful `curl\_easy\_init` does not by itself establish `EXPLICIT\_CLEANUP\_DUE`.

However, the resource metadata still contains:

`missing\_at\_exit\_normative\_status: REVIEW\_REQUIRED\_MUST\_OR\_MAY`

That field conflicts with Rule G10, the exit-obligation table, and the recorded NR01 resolution.

NR01 is no longer pending because V1 human review resolved the classification as D5 `VIOLATION-MUST`.

The exact V2 draft therefore contains contradictory machine-readable normative status for the same exit condition.

Required semantic change:

Create an immutable successor.

Replace `resources.EXPLICIT\_GLOBAL\_CLEANUP\_OBLIGATION.missing\_at\_exit\_normative\_status` value `REVIEW\_REQUIRED\_MUST\_OR\_MAY` with the resolved status `MUST`, or remove the stale field if the resolved G10 and exit-obligation fields are authoritative.

Ensure no remaining field represents the NR01 normative strength as pending or review-required.

Preserve the D5, `MUST`, and `VIOLATION-MUST` classification.



Preserve the rule that implicit readiness alone creates no explicit global-cleanup obligation.

Confirm that exit with `EXPLICIT\_CLEANUP\_DUE`, where the obligation arose from

successful explicit `curl\_global\_init`, is classified:

defect `D5`;

enforcement `MUST`;

verdict `VIOLATION-MUST`.

Confirm implicit readiness alone does not create this explicit obligation.

\---

### V2-RR07 — TS-RR10: multi cleanup ordering recommendation

Decision: PASS

Notes:

The exact V2 draft, completed V1 review, approved documentation, and pinned `lib/multi.c` implementation were reviewed for this item.

The documentation describes the preferred sequence as:

`curl\_multi\_remove\_handle`

`curl\_easy\_cleanup`

`curl\_multi\_cleanup`



Rule M13 records this sequence as a preferred documented ordering.

Rule M13 assigns enforcement `NON\_ENFORCEABLE\_RECOMMENDATION`.

The recommendation is not represented as an unconditional D6 or other MUST violation.

Rule M13 applies only when `curl\_multi\_cleanup` returns `CURLM\_OK`.

For that successful-cleanup condition, Rule M13 assigns verdict `VALID`.

Skipping explicit removal is therefore not, solely by itself, an enforceable violation when multi cleanup succeeds.

The pinned implementation supports this treatment by structurally clearing remaining easy-to-multi associations during successful multi cleanup.

Successful multi cleanup does not free the caller-owned easy handles.

The affected easy handles remain live, detached, and caller-owned.

Rule M13 explicitly preserves each affected easy handle's individual `curl\_easy\_cleanup` obligation.

Cross-resource Rule X01 independently confirms that multi cleanup does not discharge individual easy-handle cleanup obligations.

The multi-handle cleanup obligation is discharged by successful multi cleanup, while the separate easy-handle obligations remain outstanding.

The earlier `UNKNOWN` wording is retained only as historical provenance under the previous V1 review-item record.

The operative M13 rule and resolved NR02 record consistently establish the non-enforceable recommendation treatment.

No semantic revision is required for this review item.



Review whether the documented:

`remove → easy cleanup → multi cleanup`

sequence is represented as a non-enforceable recommendation rather than an

unconditional MUST.

Confirm successful multi cleanup with attached caller-owned easy handles is not

an enforceable violation solely because explicit remove was skipped.

Confirm individual easy cleanup obligations remain.

\---

### V2-RR08 — TS-RR11: post-error multi-perform and recovery

Decision: PASS

Notes:

The exact V2 rules, multi-handle resource model, completed V1 review, and pinned `curl\_multi\_perform` documentation were reviewed.

The pinned documentation states that after `curl\_multi\_perform` returns an error, transfer states are uncertain and cannot be continued normally.

Rule M07 transitions the multi handle to `MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN` after a non-`CURLM\_OK` result.

Rule M08 classifies plain repetition of `curl\_multi\_perform` without documented recovery as defect D6.

Rule M08 assigns enforcement `MUST`.

Rule M08 assigns verdict `VIOLATION-MUST`.

Rule M08 explicitly keeps the multi handle in `MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN` after the prohibited repeat.

A prohibited repeat does not itself restore normal multi ownership.

Rule M09 permits successful removal of an attached easy handle from both `MULTI\_OWNED` and `MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN`.

Removal therefore remains available as part of recovery.

Rules M12 and M13 allow successful cleanup of a live multi handle, including the post-error state, when cleanup returns `CURLM\_OK`.

Rule M24 explicitly applies failed cleanup handling to both normal and post-error multi states.

A failed cleanup does not establish release or recovery and leaves the cleanup obligation outstanding.

Cleanup therefore remains available but all release and detachment effects remain conditioned on its return value.

Rule M25 requires every easy handle attached at the time of the error to be successfully removed first.

Rule M25 then requires a successful re-add before normal `curl\_multi\_perform` use resumes.

Only that complete remove-all followed by successful re-add sequence restores `MULTI\_OWNED`.

The multi-handle resource metadata records the same complete recovery sequence.

Rule M25 explicitly states that partial removal or premature re-addition does not clear `MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN`.

Partial recovery therefore cannot silently restore normal multi-perform validity.

The V2 treatment matches the approved source evidence and the resolved NR03 human-review finding.

No semantic revision is required for this review item.



Confirm:

plain `curl\_multi\_perform` repetition after non-`CURLM\_OK`, without complete

documented recovery, is `D6 VIOLATION-MUST`;

the multi remains in the post-error uncertain state after prohibited repeat;

removal remains available;

cleanup remains available subject to return-conditioned cleanup;

recovery requires complete removal of error-time handles followed by

successful re-add before normal multi-perform resumes;

partial recovery does not silently clear post-error uncertainty.

\---

### V2-RR09 — TS-RR12: set-valued NULL easy-init state and verdict joins

Decision: REVISION\_REQUIRED

Notes: The exact E04 rule, verdict-join policy, completed V1 review, and pinned `easy.c` implementation were reviewed.

When `curl\_easy\_init` starts from `RUNTIME\_UNINITIALIZED`, the implementation first attempts implicit global initialization.

If global initialization fails, its reference increment is reversed and the runtime remains `RUNTIME\_UNINITIALIZED`.

If global initialization succeeds but `Curl\_open` fails, `curl\_easy\_init` returns NULL while implicit runtime readiness remains established.

The second feasible post-state is therefore `RUNTIME\_READY\_IMPLICIT\_ONLY`.

Rule E04 correctly preserves exactly these two feasible runtime post-states:

`RUNTIME\_UNINITIALIZED`

`RUNTIME\_READY\_IMPLICIT\_ONLY`

A NULL result creates no easy-handle resource.

Neither feasible failure branch creates an explicit `curl\_global\_init` cleanup obligation.

The representation policy correctly states that a known finite set of states does not automatically imply `UNKNOWN`.

The feasible-state join policy correctly uses the common verdict when all feasible states produce the same verdict.

The policy correctly joins mixed `VALID` and enforceable-violation outcomes to `VIOLATION-MAY`.

The policy correctly reserves `UNKNOWN` for unresolved normative strength, insufficient evidence, or bounded-model coverage uncertainty.

Rules E17 through E19 correctly ensure that definite ordinary use of a NULL easy-init result remains D2 `VIOLATION-MUST` across both runtime alternatives.

However, operative Rule E04 still contains:

`enforcement: IMPLEMENTATION\_DERIVED\_REVIEW\_REQUIRED`

Rule E04 also still contains:

`review\_item: NR04`

These fields conflict with the draft's `implemented\_review\_items`, its resolved NR04 record, and its empty `open\_independent\_review\_items` list.

The two-state result is now confirmed by approved pinned source evidence and is not an unresolved implementation-derived review question.

Leaving E04 marked `REVIEW\_REQUIRED` can incorrectly suggest unresolved evidence or normative strength and can undermine the rule that the state set alone must not force `UNKNOWN`.

Required semantic change:

Create an immutable successor.

Change E04 enforcement from `IMPLEMENTATION\_DERIVED\_REVIEW\_REQUIRED` to a resolved source-grounded status such as `SOURCE\_GROUNDED`.

Remove `review\_item: NR04` from the operative E04 rule, or move it to clearly historical resolved-review provenance.

Ensure that no operative E04 field continues to mark NR04 as pending or review-required.

Explicitly preserve the rule that a directly applicable definite D2 violation is evaluated in every feasible runtime state and is not weakened to `VIOLATION-MAY` or `UNKNOWN` merely because the runtime post-state is set-valued.

Complete the missing D2 easy-argument coverage for `curl\_multi\_add\_handle` and `curl\_multi\_remove\_handle` identified under V2-RR05, so those definite failed-acquisition uses are not incorrectly reduced to a runtime-state join.

Preserve the exact two-state runtime post-state and the rule that neither branch creates an explicit global-cleanup obligation.



Confirm the source-grounded NULL `curl\_easy\_init` runtime post-state remains:

`RUNTIME\_UNINITIALIZED`, or

`RUNTIME\_READY\_IMPLICIT\_ONLY`.

Confirm:

the state set itself does not automatically imply `UNKNOWN`;

common verdicts across feasible states remain the common verdict;

mixed VALID/enforceable-violation outcomes join to `VIOLATION-MAY`;

unresolved normative strength or bounded-model uncertainty remains `UNKNOWN`;

neither failure branch creates an explicit global-cleanup obligation.

\---

### V2-RR10 — TS-RR13: wrong-multi removal

Decision: REVISION\_REQUIRED

Notes: The exact M09, M10, and M11 rules, completed V1 review, and pinned `curl\_multi\_remove\_handle` implementation were reviewed.

For a live easy handle attached to a different live multi than the supplied live multi, Rule M11 assigns defect D7.

Rule M11 assigns enforcement `MUST`.

Rule M11 assigns verdict `VIOLATION-MUST`.

Rule M11 records the pinned return value `CURLM\_BAD\_EASY\_HANDLE`.

Rule M11 correctly states that the rejected call does not detach the easy handle.

The actual easy-to-original-multi membership therefore remains unchanged.

Rule M10 separately treats repeated removal of an already detached easy handle as `VALID`.

The pinned implementation returns `CURLM\_OK` without changing membership when the easy handle is already detached and both supplied handles have passed validity checks.

The substantive distinction between wrong-multi removal and valid repeated removal is therefore correct.

However, Rule M10 uses only:

`condition: easy is already detached`

Rule M10 does not explicitly require the supplied multi handle to be live and valid.

The pinned implementation validates the supplied multi handle before checking whether the easy handle is already detached.

An invalid supplied multi returns `CURLM\_BAD\_HANDLE` before the repeated-remove no-op path is reached.

Therefore, the unconditional M10 statement that the pinned implementation returns `CURLM\_OK` is broader than the approved source behavior.

Rule M11 likewise does not explicitly state that the supplied multi handle has passed the live-handle validity check.

Without that precondition, M10 or M11 can overlap incorrectly with D1, D2, or D3 rules for an absent, NULL, or released supplied multi handle.

Required semantic change:

Create an immutable successor.

Constrain Rule M10 to a live valid supplied multi handle and a live already-detached easy handle.

State that only this valid repeated-remove case returns `CURLM\_OK`, changes no membership, and is `VALID`.

Constrain Rule M11 to a live valid supplied multi handle and a live easy handle attached to a different original multi handle.

Preserve M11 as D7 `VIOLATION-MUST`, returning `CURLM\_BAD\_EASY\_HANDLE` and preserving the original membership.

Specify that invalid, NULL, or released supplied-multi cases are classified by their applicable D1, D2, or D3 rules before the membership comparison.

Preserve the distinction between wrong-multi removal and valid repeated removal.



Review whether wrong-multi `curl\_multi\_remove\_handle` is correctly represented

as:

`D7`;

`VIOLATION-MUST`;

rejected with `CURLM\_BAD\_EASY\_HANDLE`;

actual easy-to-original-multi membership preserved.

Confirm this remains distinct from valid repeated removal of an already

detached easy handle.

\---

### V2-RR11 — TS-RR14: final-reference global cleanup with live resources

Decision: PASS

Notes: The exact V2 global-runtime rules, cross-resource rules, resource model, and pinned `curl\_global\_cleanup` implementation were reviewed.

Rule X02 applies only when `curl\_global\_cleanup` removes the final runtime reference while a modeled easy or multi resource remains live.

Rule X02 classifies that condition as defect D8.

Rule X02 assigns enforcement `MUST`.

Rule X02 assigns verdict `VIOLATION-MUST`.

No other V2 rule assigns D8 to `curl\_global\_cleanup`.

Rule X02 correctly preserves the real runtime effect of the cleanup call.

The final-reference cleanup transitions the runtime to `RUNTIME\_UNINITIALIZED` even though the call itself is a protocol violation.

Subsequent operations requiring runtime readiness are evaluated from that resulting uninitialized state.

Rule G06 separately models cleanup that removes an explicit reference while an implicit reference remains.

That path leaves the runtime in `RUNTIME\_READY\_IMPLICIT\_ONLY` and does not satisfy the final-reference condition of X02.

Cleanup after all modeled easy and multi resources have completed their lifecycles is also explicitly excluded from X02.

Rule G07 treats final cleanup from implicit-only readiness as state-sensitive rather than automatically assigning D4.

Rule G08 models `curl\_global\_cleanup` from zero runtime references as an implementation-level no-op.

Rule G08 explicitly states that the zero-reference no-op is not automatically a D4 double-cleanup violation.

The pinned implementation confirms that cleanup decrements an existing reference, returns without global teardown when another reference remains, and performs final teardown only when the reference count reaches zero.

The pinned implementation also returns without action when the reference count is already zero.

The classification therefore depends on runtime-reference state and the presence of live modeled resources.

It is not based solely on the numerical ordering or count of global-init and global-cleanup calls.

The V2 treatment is consistent with the resolved NR06 finding and approved pinned source evidence.

No semantic revision is required for this review item.



Confirm that `curl\_global\_cleanup` is classified as state-sensitive

`D8 VIOLATION-MUST` only when it removes the final runtime reference while a

modeled easy or multi resource remains live.

Confirm:

the actual runtime transition to uninitialized still occurs;

cleanup leaving another runtime reference ready is distinct;

cleanup after all modeled resources are finished is distinct;

a zero-reference no-op is not automatically D4;

classification is not based solely on global init/cleanup call count.

\---

### V2-RR12 — Source traceability, quarantine, and overall V2 adequacy

Decision: REVISION\_REQUIRED

Notes: The exact V2 draft, frozen V3 scope, source-evidence map, approved source manifest, completed V1 review, and packaged source files were reviewed.

The approved source-evidence manifest declares evidence class `PREAPPROVED\_SOURCE\_ONLY`.

The manifest contains exactly 21 approved pinned curl source files.

The packaged `12\_source\_evidence` directory also contains exactly 21 files.

The packaged source paths exactly match the approved manifest.

All 21 packaged source-file SHA-256 values match the approved manifest.

The pinned source commit remains:

`68720b4837284335b2d63cb358f8f6ce65f5bc55`

The pinned source tree remains:

`e23d273aeb073c04aa5b073b35c9fde16979c896`

No generated-driver evidence is present or cited as technical-specification evidence.

No selected-sample membership evidence is present or cited.

No raw model-response evidence is present or cited.

No generated-driver compiler-log semantic evidence is present or cited.

No gold-label evidence is present or cited.

No analyzer or baseline output is present or cited.

No LLM-review or repair output is present or cited.

The evidence quarantine and approved source-evidence class are therefore preserved.

The important V2 subjects can generally be traced manually to frozen V3, the completed V1 review, and the same approved pinned source files.

However, the included source-evidence map remains explicitly bound to Working Draft V1 and its V1 SHA-256.

It does not provide an exact V2-bound rule-to-source mapping for the successor corrections.

The exact V2 also contains unresolved semantic inconsistencies identified during this review.

The D1/D2 rules do not cover invalid easy-handle acquisition states when `curl\_multi\_add\_handle` or `curl\_multi\_remove\_handle` consumes the easy argument.

The explicit-global-cleanup resource metadata still says `REVIEW\_REQUIRED\_MUST\_OR\_MAY`, despite the resolved D5 `MUST` and `VIOLATION-MUST` rules.

Operative Rule E04 still says `IMPLEMENTATION\_DERIVED\_REVIEW\_REQUIRED` and still identifies NR04 as an active review item, despite NR04 being implemented and listed as resolved.

Rules M10 and M11 do not explicitly require the supplied multi handle to be live and valid before assigning the repeated-remove or wrong-multi behavior.

These omissions and contradictions prevent approval of the exact V2 for canonicalization.

The defects are bounded and correctable, so `FAIL` is not required.

Required successor corrections:

Create a new immutable successor and do not edit V2 in place.

Add D1 `VIOLATION-MUST` rules for `curl\_multi\_add\_handle` and `curl\_multi\_remove\_handle` when their easy argument is not backed by successful easy-handle acquisition.

Add corresponding D2 `VIOLATION-MUST` rules when their easy argument is a NULL `curl\_easy\_init` result.

Record `CURLM\_BAD\_EASY\_HANDLE` and no membership change for those invalid-easy cases.

Replace the stale explicit-cleanup status `REVIEW\_REQUIRED\_MUST\_OR\_MAY` with resolved `MUST` status, or remove that obsolete field.

Change E04 to a resolved source-grounded enforcement status.

Remove E04's operative pending `review\_item: NR04` marker or move it to clearly resolved historical provenance.

Preserve the two-state NULL easy-init runtime result and the specified feasible-state verdict joins.

Constrain M10 to a live valid supplied multi and a live detached easy handle.

Constrain M11 to a live valid supplied multi and a live easy handle attached to a different original multi.

Preserve M11 as D7 `VIOLATION-MUST`, returning `CURLM\_BAD\_EASY\_HANDLE` and preserving original membership.

Provide a successor-bound traceability record that maps the corrected successor rules to frozen V3 and/or the unchanged approved pinned source evidence.

Do not add any new evidence class while making these corrections.



Confirm:

all important V2 rules remain traceable to frozen V3 and/or the same approved

pinned source evidence;

exactly the approved source-evidence class is used;

no prohibited generated-driver, gold, analyzer, baseline, LLM-review, or

repair evidence is used;

V2 did not introduce a new semantic inconsistency while resolving the V1

findings;

the exact V2 is technically adequate, or identify any required successor

correction.

\---

## Overall technical review decision

Choose exactly one:

Overall decision: REVISION\_REQUIRED

Notes:

The exact immutable Working Draft V2 was reviewed item by item against the permitted evidence boundary.

V2-RR01 passed exact author-checkpoint identity and immutability review.

V2-RR02 passed frozen scope and successor-boundary review.

V2-RR03 passed return-conditioned multi-cleanup review.

V2-RR04 passed the exact four-verdict contract review.

V2-RR05 requires revision because D1/D2 coverage is incomplete for invalid easy-handle arguments supplied to `curl\_multi\_add\_handle` and `curl\_multi\_remove\_handle`.

V2-RR06 requires revision because `missing\_at\_exit\_normative\_status` still contains `REVIEW\_REQUIRED\_MUST\_OR\_MAY`, conflicting with the resolved D5 `MUST` and `VIOLATION-MUST` classification.

V2-RR07 passed the non-enforceable multi-cleanup ordering recommendation review.

V2-RR08 passed post-error multi-perform and complete-recovery review.

V2-RR09 requires revision because operative Rule E04 still contains `IMPLEMENTATION\_DERIVED\_REVIEW\_REQUIRED` and `review\_item: NR04` despite NR04 being implemented and resolved.

V2-RR10 requires revision because Rules M10 and M11 do not explicitly constrain their behavior to a live valid supplied multi handle.

V2-RR11 passed the state-sensitive final-reference global-cleanup review.

V2-RR12 requires revision because the identified semantic inconsistencies remain and the included source-evidence map is still explicitly bound to Working Draft V1 rather than the exact V2 successor.

The approved source-evidence boundary remains intact.

Exactly the same 21 approved pinned curl source files are present and their hashes match the approved manifest.

No prohibited generated-driver, selected-sample, raw-model-response, gold, analyzer, baseline, LLM-review, or repair evidence was used.

The identified defects are bounded and correctable, so `FAIL` is not warranted.

The exact Working Draft V2 is not technically adequate to proceed to canonicalization.

Working Draft V2 must remain immutable.

A new immutable successor must implement the precise corrections recorded in the revision-required review items.

This decision does not create or authorize canonical `curl.json`.

Generated-driver inspection, selected-sample inspection, gold annotation, analyzer implementation or execution, baseline execution, and repair remain unauthorized at this boundary.



Approval means only that the exact immutable V2 may proceed to a separate

canonicalization authorization/operation.

Approval does not itself create or authorize use of canonical `curl.json`.

Generated-driver inspection, selected-sample inspection, gold annotation,

analyzer implementation/execution, baseline execution, and repair remain

separately governed and unauthorized at this boundary.

## Reviewer identity

Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 19 / August / 2026

## Post-review rule

No assistant-generated or synthetic human approval is permitted.

If revision is required, exact V2 must remain immutable and a new successor

must be created rather than editing V2 in place.

