# curl Technical Protocol Working Draft V3 — Independent Human Review Packet

## Purpose

This packet is for an independent human technical-specification review of the
exact immutable curl Technical Protocol Working Draft V3 author checkpoint.

Working Draft V2 received an overall independent human-review decision of
`REVISION\_REQUIRED`.

V3 is a new immutable successor implementing only the bounded corrections
authorized from V2-RR05, V2-RR06, V2-RR09, V2-RR10, and V2-RR12.

No canonicalization may occur unless this exact V3 later receives the required
human approval and a separate canonicalization authorization.

## Exact review target

Working draft:

`03\_curl\_technical\_protocol\_working\_draft.v3.json`

SHA-256:

`2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2`

Size:

`41330` bytes

Author checkpoint commit:

`d4c41e682882f6053fd6657a7f0f82a402697354`

Author checkpoint tree:

`d6878d64e639566a5cedaa95891947c23815b989`

The supplied minimal Git witness must independently resolve the author
checkpoint commit → tree → exact V3 target blob and Decision 0033 blob.

## Evidence boundary

Permitted technical-review evidence in this package:

* exact Working Draft V3;
* exact immutable Working Draft V2 predecessor;
* completed V2 independent human technical review;
* V3 successor authorization;
* Decision 0031, Decision 0032, and Decision 0033;
* exact V3 author-resolution record;
* exact V3 author-checkpoint record;
* exact V3 successor-bound rule-to-source traceability record;
* frozen V3 source-only scope;
* exactly the same 21 approved pinned curl source files;
* minimal V3 author-checkpoint Git witness.

Not permitted as V3 technical-review evidence:

* generated drivers;
* selected-sample membership;
* raw model responses;
* generated-driver compiler-log semantic content;
* gold labels;
* analyzer output;
* baseline output;
* LLM-review output;
* repair output.

## Decision choices

For every review item choose exactly one:

`PASS`

`REVISION\_REQUIRED`

`FAIL`

A `PASS` means the exact V3 treatment of that item is technically acceptable.

If `REVISION\_REQUIRED`, state the precise semantic change required.

Do not edit the immutable review-package copy. Complete only an external
editable reviewer-response copy prepared from this packet.

\---

### V3-RR01 — Exact V3 author-checkpoint identity and immutability

Decision: PASS

Notes: The exact V3 SHA-256 was independently recalculated as:

2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2

The exact V3 size is 41330 bytes.

The author-checkpoint commit resolves to:

d4c41e682882f6053fd6657a7f0f82a402697354

The commit resolves to tree:

d6878d64e639566a5cedaa95891947c23815b989

The V3 target path resolves to Git blob:

086adbf28333b27683441da0475c275087409e57

Decision 0033 resolves to Git blob:

af99db5023a6e1b9c1ce2eaf05eb4b5a9e365db7

The raw V3 witness blob is byte-identical to the packaged V3 target.

The raw Decision 0033 witness blob is byte-identical to the packaged Decision 0033 file.

The immutable V2 predecessor SHA-256 is:

63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31

The packaged V2 predecessor is byte-identical to the earlier immutable V2 review target.

No silent V2 in-place modification was identified.

The exact packaged V3 target is the author-checkpoint artifact.



Confirm:

* exact V3 SHA-256 and size;
* author-checkpoint commit and tree;
* V3 target Git blob;
* Decision 0033 Git blob;
* immutable V2 predecessor binding;
* V2 was not edited in place;
* exact V3 package target is the author-checkpoint artifact.

\---

### V3-RR02 — Frozen scope and bounded-successor boundary

Decision: REVISION\_REQUIRED

Notes: The exact V3 function surface contains the frozen twelve curl functions.

No additional protocol function or event was introduced.

The pinned curl commit remains:

68720b4837284335b2d63cb358f8f6ce65f5bc55

The pinned curl tree remains:

e23d273aeb073c04aa5b073b35c9fde16979c896

The frozen V3 scope SHA-256 remains:

ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb

The V2-to-V3 protocol-rule changes are limited to V3-C01 through V3-C08.

No generated-driver-derived rule was identified.

No new evidence class was introduced.

However, the exact V3 draft contains stale V1/V2 successor-governance metadata.

Its purpose still describes V2 as the successor to V1.

governance.working\_draft\_version is still V2.

The predecessor version, path, and SHA-256 still identify V1 rather than V2.

The completed-review SHA-256 still identifies the V1 review rather than the completed V2 review.

The successor-authorization commit still contains the earlier V2 authorization value.

The v1\_in\_place\_edit\_authorized field is stale for the V3 successor boundary.

Required semantic change:

Keep exact V3 immutable and create a new immutable successor.

Correct the internal purpose, version, predecessor, completed-review, authorization, and immutable-predecessor metadata.

Preserve the verified twelve-function scope and bounded protocol-rule changes.



Confirm:

* exactly the frozen twelve curl functions remain in scope;
* pinned curl revision and tree are unchanged;
* frozen V3 source-only scope is unchanged;
* V3 semantic changes are limited to the authorized V2 revision-required items;
* no generated-driver-derived rule was introduced;
* no new evidence class was introduced.

\---

### V3-RR03 — Preserved return-conditioned multi cleanup semantics

Decision: PASS

Notes: Rules M12, M13, M14, and M24 are unchanged from V2.

Only curl\_multi\_cleanup returning CURLM\_OK establishes MULTI\_RELEASED.

Only successful cleanup discharges the multi cleanup obligation.

Only successful cleanup establishes complete structural detachment.

A non-CURLM\_OK result does not establish release.

A non-CURLM\_OK result leaves the cleanup obligation outstanding.

Membership facts not established by failed cleanup remain conservatively unresolved.

Rule M24 covers both MULTI\_OWNED and MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN.

The same return-conditioned treatment therefore applies from the post-error state.



Review whether V3 preserves the accepted V2 treatment that:

* only `curl\_multi\_cleanup == CURLM\_OK` establishes `MULTI\_RELEASED`;
* only successful cleanup discharges the multi cleanup obligation;
* only successful cleanup establishes complete structural detachment;
* non-`CURLM\_OK` cleanup does not assert release;
* non-`CURLM\_OK` cleanup preserves the cleanup obligation;
* unresolved membership after failed cleanup remains conservative;
* the same treatment applies from the post-error multi state.

\---

### V3-RR04 — Exact four-verdict machine contract

Decision: PASS

Notes: The declared machine-verdict set contains exactly:

VALID

VIOLATION-MUST

VIOLATION-MAY

UNKNOWN

All populated rule-level verdict fields use only these values.

All missing\_cleanup\_verdict fields use only these values.

No UNKNOWN\_PENDING\_\* or other undeclared qualified verdict appears in a machine-verdict field.

Review state, provenance, classifications, qualifiers, and explanations remain in separate fields.

Historical explanatory UNKNOWN text does not create another machine verdict.

The exact four-verdict machine contract is preserved.



Confirm that all machine-readable verdict fields use only:

`VALID`

`VIOLATION-MUST`

`VIOLATION-MAY`

`UNKNOWN`

Confirm that review state, provenance, qualifiers, and explanatory information
remain separate and do not create undeclared machine verdict variants.

\---

### V3-RR05 — D1/D2 dual-resource coverage and cleanup-specific cases

Decision: PASS

Notes: M26 classifies the pre-acquisition easy argument to curl\_multi\_add\_handle as D1 VIOLATION-MUST.

M27 applies the same D1 classification to curl\_multi\_remove\_handle.

M28 classifies a NULL failed-curl\_easy\_init result supplied to curl\_multi\_add\_handle as D2 VIOLATION-MUST.

M29 applies the same D2 classification to curl\_multi\_remove\_handle.

When the supplied multi passes its live-valid check, the pinned invalid-easy return is CURLM\_BAD\_EASY\_HANDLE.

These invalid-easy branches create, detach, or change no membership.

Easy-argument D1/D2 classification remains independent of supplied-multi D1/D2/D3 classification.

The pinned implementation validates the supplied multi first.

An invalid supplied multi may therefore determine the earlier CURLM\_BAD\_HANDLE return.

The definite D2 result is preserved across both feasible failed-easy runtime states.

Cleanup-specific D4 precedence remains intact.

curl\_easy\_cleanup(NULL) remains a VALID documented no-op.

curl\_multi\_cleanup(NULL) returns CURLM\_BAD\_HANDLE.

NULL multi cleanup releases nothing, detaches nothing, and discharges no obligation.

Review the V3 treatment of `curl\_multi\_add\_handle` and
`curl\_multi\_remove\_handle`.



Confirm that:

* M26 and M27 explicitly classify the easy argument used before successful
`curl\_easy\_init` acquisition as D1 `VIOLATION-MUST`;
* M28 and M29 explicitly classify a NULL failed-`curl\_easy\_init` result as
D2 `VIOLATION-MUST`;
* when the supplied multi has passed its live-valid check, the pinned invalid
easy result is `CURLM\_BAD\_EASY\_HANDLE`;
* these invalid-easy cases create/detach/change no membership;
* easy-argument D1/D2 classification is independent of supplied-multi
D1/D2/D3 classification;
* invalid supplied-multi cases may determine the earlier pinned return;
* definite D2 failed-easy use is not weakened merely because the failed
`curl\_easy\_init` runtime post-state is set-valued;
* cleanup-specific D4 precedence remains intact;
* `curl\_easy\_cleanup(NULL)` remains the documented no-op exception;
* `curl\_multi\_cleanup(NULL)` retains its return-conditioned no-release behavior.

\---

### V3-RR06 — Explicit global cleanup obligation at exit

Decision: PASS

Notes: Successful explicit curl\_global\_init establishes EXPLICIT\_CLEANUP\_DUE.

Implicit readiness created by curl\_easy\_init does not establish that explicit obligation.

Failed explicit curl\_global\_init does not establish the obligation.

Exit with EXPLICIT\_CLEANUP\_DUE is defect D5.

Its enforcement is MUST.

Its verdict is VIOLATION-MUST.

The exit-obligation table contains the same D5, MUST, and VIOLATION-MUST classification.

The stale REVIEW\_REQUIRED\_MUST\_OR\_MAY value does not occur in exact V3.

The operative missing\_at\_exit\_normative\_status is MUST.

The resource metadata is consistent with the resolved D5 classification.



Confirm that:

* successful explicit `curl\_global\_init` establishes
`EXPLICIT\_CLEANUP\_DUE`;
* implicit readiness alone does not establish that explicit obligation;
* exit with an outstanding explicit cleanup obligation is D5;
* enforcement is `MUST`;
* verdict is `VIOLATION-MUST`;
* the V3 resource metadata no longer contains the stale
`REVIEW\_REQUIRED\_MUST\_OR\_MAY` normative status;
* the operative missing-at-exit normative status is consistent with the
resolved D5 `MUST` classification.

\---

### V3-RR07 — Preserved multi-cleanup ordering recommendation

Decision: PASS

Notes: The documentation describes the preferred order as:

curl\_multi\_remove\_handle

curl\_easy\_cleanup

curl\_multi\_cleanup

Rule M13 records this as NON\_ENFORCEABLE\_RECOMMENDATION.

It is not represented as an unconditional MUST violation.

When cleanup returns CURLM\_OK with caller-owned easy handles attached, M13 assigns verdict VALID.

Skipping explicit removal is not, solely by itself, an enforceable violation.

Successful cleanup structurally clears the remaining easy-to-multi associations.

The caller-owned easy handles are not freed.

They remain live, detached, and caller-owned.

Their individual curl\_easy\_cleanup obligations remain outstanding.



Review whether V3 preserves the accepted treatment that:

* `remove → easy cleanup → multi cleanup` is a documented recommendation;
* it is not an unconditional MUST violation;
* successful multi cleanup with caller-owned easy handles still attached is
not a violation solely because explicit remove was skipped;
* successful multi cleanup structurally detaches remaining easy handles;
* individual easy cleanup obligations remain outstanding.

\---

### V3-RR08 — Preserved post-error multi-perform and recovery semantics

Decision: PASS

Notes: A non-CURLM\_OK curl\_multi\_perform result establishes MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN.

Plain repetition without complete recovery is D6 VIOLATION-MUST.

The prohibited repeat does not restore normal MULTI\_OWNED state.

The multi remains in the post-error uncertain state.

Successful removal remains available from the post-error state.

Cleanup remains available subject to its return value.

Failed cleanup does not establish release or recovery.

Recovery requires successful removal of every easy handle attached at the error.

At least one successful re-add must then occur before normal curl\_multi\_perform resumes.

Only the complete remove-all followed by successful re-add sequence restores MULTI\_OWNED.

Partial removal or premature re-addition does not clear post-error uncertainty.



Confirm that:

* plain `curl\_multi\_perform` repetition after non-`CURLM\_OK` without complete
recovery remains D6 `VIOLATION-MUST`;
* the multi remains in the post-error uncertain state after prohibited repeat;
* removal remains available;
* cleanup remains available subject to return-conditioned cleanup;
* recovery requires complete removal of error-time handles followed by
successful re-add before normal multi-perform resumes;
* partial recovery does not silently clear post-error uncertainty.

\---

### V3-RR09 — Resolved E04 set-valued NULL easy-init semantics

Decision: PASS

Notes: Operative E04 now uses SOURCE\_GROUNDED enforcement.

IMPLEMENTATION\_DERIVED\_REVIEW\_REQUIRED does not occur in exact V3.

Operative E04 no longer contains review\_item: NR04.

E04 preserves exactly:

RUNTIME\_UNINITIALIZED

RUNTIME\_READY\_IMPLICIT\_ONLY

A NULL result creates no easy resource.

Neither branch creates an explicit global-cleanup obligation.

The existence of two feasible states does not itself force UNKNOWN.

When every feasible state agrees, the common verdict is used.

Mixed VALID and enforceable-violation outcomes join to VIOLATION-MAY.

UNKNOWN is reserved for normative, evidence, or bounded-model uncertainty.

Definite D2 use of the failed easy result remains VIOLATION-MUST across both states.

NR04 remains only in historical and resolved-review provenance outside operative E04.



Confirm that operative E04 now:

* uses resolved source-grounded enforcement rather than
`IMPLEMENTATION\_DERIVED\_REVIEW\_REQUIRED`;
* no longer carries an operative pending `review\_item: NR04`;
* preserves exactly the feasible post-states:
`RUNTIME\_UNINITIALIZED` and `RUNTIME\_READY\_IMPLICIT\_ONLY`;
* creates no easy resource on NULL;
* creates no explicit global-cleanup obligation on either failure branch;
* does not force `UNKNOWN` merely because the runtime state is set-valued;
* uses the common verdict when every feasible state agrees;
* joins mixed VALID/enforceable-violation outcomes to `VIOLATION-MAY`;
* reserves `UNKNOWN` for normative/evidence/model uncertainty;
* preserves definite D2 failed-easy use across both feasible runtime states.

Historical resolved NR04 provenance may remain outside the operative E04 rule.

\---

### V3-RR10 — Valid repeated removal and wrong-multi removal

Decision: PASS

Notes: M10 requires a live valid supplied multi and a live already-detached easy handle.

Only that valid repeated-remove branch returns CURLM\_OK.

That branch changes no membership and is VALID.

M11 requires a live valid supplied multi and a live easy handle attached to a different original multi.

M11 remains defect D7.

M11 enforcement remains MUST.

M11 verdict remains VIOLATION-MUST.

The pinned wrong-multi return is CURLM\_BAD\_EASY\_HANDLE.

The rejected call performs no successful detachment.

The easy handle remains attached to its actual original multi.

Absent supplied-multi acquisition is covered by D1.

A NULL curl\_multi\_init result is covered by D2.

Use of a released supplied multi is covered by D3.

Those classifications apply before membership comparison.

Valid repeated removal and wrong-multi removal remain explicitly distinct.



Confirm that:

* M10 applies only with a live valid supplied multi and a live already-detached
easy handle;
* only that valid repeated-remove case returns `CURLM\_OK`, changes no
membership, and is `VALID`;
* M11 applies only with a live valid supplied multi and a live easy handle
attached to a different original multi;
* M11 remains D7 `VIOLATION-MUST`;
* M11 returns `CURLM\_BAD\_EASY\_HANDLE`;
* rejected wrong-multi removal preserves the actual original membership;
* absent, NULL, or released supplied-multi cases are classified by applicable
D1/D2/D3 rules before membership comparison;
* valid repeated removal remains distinct from wrong-multi removal.

\---

### V3-RR11 — Preserved final-reference global cleanup with live resources

Decision: PASS

Notes: X02 applies when curl\_global\_cleanup removes the final runtime reference while a modeled easy or multi resource remains live.

That condition is D8 VIOLATION-MUST.

The actual transition to RUNTIME\_UNINITIALIZED still occurs.

Later readiness-dependent operations are evaluated from the resulting uninitialized state.

Cleanup leaving another runtime reference ready is distinct.

Cleanup after all modeled resources complete their lifecycles is distinct.

A zero-reference curl\_global\_cleanup is an implementation-level no-op.

The zero-reference no-op is not automatically D4.

The classification depends on runtime-reference and live-resource state.

It is not determined solely by counting global init and cleanup calls.



Confirm that V3 preserves the accepted state-sensitive treatment:

* final-reference `curl\_global\_cleanup` with a live modeled easy or multi
resource is D8 `VIOLATION-MUST`;
* the actual runtime transition to uninitialized still occurs;
* cleanup leaving another runtime reference ready is distinct;
* cleanup after modeled resources have completed is distinct;
* a zero-reference no-op is not automatically D4;
* classification is state/reference-sensitive rather than based only on
global init/cleanup call counts.

\---

### V3-RR12 — V3-bound traceability, quarantine, and overall adequacy

Decision: REVISION\_REQUIRED

Notes: The successor traceability record binds exact V3 SHA-256:

2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2

The corrected subjects are mapped to frozen V3 and approved pinned source evidence.

Every traced source path belongs to the approved source manifest.

Every traced source hash matches the approved manifest.

The evidence class is exactly PREAPPROVED\_SOURCE\_ONLY.

Exactly 21 approved pinned source files are supplied.

The V2 and V3 source sets have identical paths and hashes.

No generated-driver, selected-sample, raw-model-response, compiler-log semantic, gold, analyzer, baseline, LLM-review, or repair evidence was identified.

The V2-to-V3 protocol-rule diff is limited to the authorized corrections.

No unauthorized protocol-rule semantic change was found.

The seven V2 PASS-review subjects remain preserved.

However, exact V3 contains contradictory internal successor metadata described under V3-RR02.

Version-specific explicit\_non\_claims also refer to Working Draft V2 instead of Working Draft V3.

The internal successor-resolution metadata remains bound to the earlier V1 review instead of the completed V2 review and V3 corrections.

The supplied verifier also fails on Windows with FAIL|SOURCE\_PATH\_SET.

This verifier failure is caused by backslash-versus-forward-slash path comparison.

Manual normalized comparison confirms that all 21 source paths and hashes are correct.

Required successor correction:

Keep exact V3 immutable.

Create a new immutable successor with corrected internal successor and governance metadata.

Update version-specific non-claims and review-resolution metadata.

Preserve all verified protocol semantics and evidence boundaries.

Make the verifier path comparison platform-independent.

Regenerate the package manifest and checksums.

Create a new author checkpoint and exact successor-bound traceability record before another review.

The exact V3 is therefore not technically adequate for canonicalization authorization.



Confirm:

* the exact V3 SHA is bound by the successor traceability record;
* corrected V3 subjects are mapped to frozen V3 and/or unchanged approved
pinned source evidence;
* exactly the approved `PREAPPROVED\_SOURCE\_ONLY` evidence class is used;
* exactly the same 21 approved pinned curl source files are supplied;
* no generated-driver, selected-sample, raw-model-response, compiler-log
semantic, gold, analyzer, baseline, LLM-review, or repair evidence is used;
* V3 contains no semantic change outside the authorized bounded corrections;
* the seven V2 PASS-review subjects remain preserved;
* the exact V3 is technically adequate for a later separate canonicalization
authorization, or identify any required successor correction.

\---

## Overall technical review decision

Choose exactly one:

`APPROVE\_EXACT\_WORKING\_DRAFT\_V3\_FOR\_CANONICALIZATION`

`REVISION\_REQUIRED`

`FAIL`

Overall decision: REVISION\_REQUIRED

Notes: The exact immutable Working Draft V3 was reviewed against the permitted evidence boundary.

V3-RR01 and V3-RR03 through V3-RR11 pass.

V3-RR02 and V3-RR12 require revision.

The technical protocol-rule corrections are bounded, source-grounded, and acceptable.

The exact V3 nevertheless contains contradictory internal V1/V2 successor metadata.

The supplied review-package verifier also requires a platform-independent path correction.

These defects are precise and recoverable.

FAIL is therefore not warranted.

The exact V3 must remain immutable.

A new immutable successor must be created and independently reviewed.

The exact V3 is not approved to proceed to canonicalization.

This decision does not create or authorize canonical curl.json.

Generated-driver inspection, selected-sample inspection, gold annotation, analyzer implementation or execution, baseline execution, and repair remain unauthorized at this boundary.

## Reviewer identity

Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 19 / August / 2026

## Post-review rule

No assistant-generated or synthetic human approval is permitted.

If revision is required, exact V3 must remain immutable and a new successor
must be created rather than editing V3 in place.

If approval is granted, exact V3 must remain immutable and canonicalization
still requires a separate explicit authorization and operation.

