# curl Technical Protocol Working Draft V1 — Independent Human Review Packet

## Purpose

This is an independent human technical-specification review of the exact
immutable curl Technical Protocol Working Draft V1.

This review is separate from the earlier V3 source-only authoring-scope review.

The reviewer must decide whether the exact working draft is technically
adequate to proceed to a **separate canonicalization operation**, or whether
an immutable successor/revision is required.

## Exact review target

Working draft:

`03\_curl\_technical\_protocol\_working\_draft.v1.json`

SHA-256:

`80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6`

Author checkpoint commit:

`06a626c90bd18b6645a66117c5562c200734ccc1`

Author checkpoint tree:

`f86c25370a7b74b493cf22491e925b420ae3d303`

The package includes a minimal Git witness allowing independent resolution of
the author commit → tree → target path → blob → SHA-256 relationship.

## Evidence boundary

Permitted review evidence in this package:

* exact Working Draft V1;
* exact frozen V3 source-only scope;
* Decision 0026 and Decision 0027;
* source-evidence map and author notes;
* the 21 previously approved pinned curl source files;
* minimal Git object witness.

Not permitted as technical-specification evidence:

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

A `PASS` means the exact current draft treatment is acceptable.

If `REVISION\_REQUIRED`, describe the precise required semantic change.

Do not edit the immutable review-package copies.

\---

### TS-RR01 — Exact author-checkpoint identity and immutability

Decision: PASS

Notes: Exact Working Draft V1 SHA-256 confirmed:

80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6



Author commit independently resolved:

06a626c90bd18b6645a66117c5562c200734ccc1



Author commit resolves to the expected tree:

f86c25370a7b74b493cf22491e925b420ae3d303



The target draft path resolves to blob:

4e4b87319aa2f09b5618d2a0b8e0a076788a2e10



The resolved draft blob is byte-identical to the packaged Working Draft V1.



Decision 0027 resolves from the same author commit to blob:

4d2f9eced54e406d8f9212464351a749f9af88e1



The resolved Decision 0027 blob is byte-identical to the packaged copy.



Decision 0027 records the same Working Draft V1 SHA-256.



The immutable reviewer packet and manual-review copy are byte-identical.



No evidence of silent in-place modification was found.



Confirm that:

* exact Working Draft V1 SHA-256 is correct;
* author commit and tree are independently resolvable using the supplied
minimal Git witness;
* the target path resolves to the exact draft blob;
* Decision 0027 is bound to the same author checkpoint;
* the review target has not been silently edited in place.

\---

### TS-RR02 — Frozen V3 scope compliance and twelve-function surface

Decision: PASS

Notes: The Working Draft V1 contains exactly twelve API functions.

The frozen V3 scope also contains exactly twelve API functions.

The two twelve-function sets are identical.

The exact function surface is:

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

All function references in the draft rules remain within this frozen surface.

No additional API function or synthetic protocol event was introduced.

All required V3 resource and state components are represented.

Runtime readiness remains separate from the explicit global-cleanup obligation.

Implicit readiness from curl\_easy\_init does not create the same explicit cleanup obligation.

curl\_multi\_init continues to require prior runtime readiness.

An unmatched curl\_global\_cleanup is not automatically classified as D4.

Easy-handle cleanup continues to require prior detachment from a multi handle.

Easy-handle ownership remains with the caller after attachment to a multi handle.

curl\_multi\_cleanup does not discharge individual easy-handle cleanup obligations.

A non-CURLM\_OK curl\_multi\_perform result creates an explicit post-error uncertain state.

The broader multi-cleanup sequence has not been silently strengthened to an unconditional MUST.

The draft preserves the frozen V3 semantic guardrails without expanding the frozen protocol surface.



Review whether the working draft remains within the frozen twelve-function
surface and preserves the frozen V3 semantic guardrails without inventing
additional protocol events.

\---

### TS-RR03 — Global runtime readiness versus explicit cleanup obligation

Decision: PASS

Notes: Actual global runtime readiness is modeled separately from the explicit global-cleanup obligation.

The runtime state and cleanup-obligation state are represented as independent resource dimensions.

A successful explicit curl\_global\_init from an uninitialized runtime creates RUNTIME\_READY\_EXPLICIT\_ONLY.

The same successful explicit initialization creates EXPLICIT\_CLEANUP\_DUE.

A successful curl\_easy\_init from an uninitialized runtime creates RUNTIME\_READY\_IMPLICIT\_ONLY.

Implicit readiness established by curl\_easy\_init does not create EXPLICIT\_CLEANUP\_DUE.

A successful explicit curl\_global\_init after implicit readiness creates RUNTIME\_READY\_IMPLICIT\_PLUS\_EXPLICIT.

Its matching curl\_global\_cleanup removes only the explicit obligation and returns the runtime to RUNTIME\_READY\_IMPLICIT\_ONLY.

A failed explicit curl\_global\_init does not establish runtime readiness.

A failed explicit curl\_global\_init does not create an explicit cleanup obligation.

Ordinary libcurl use after failed explicit initialization is classified as D2 VIOLATION-MUST.

curl\_global\_cleanup from RUNTIME\_READY\_EXPLICIT\_ONLY removes the explicit obligation and makes the runtime uninitialized.

curl\_global\_cleanup from RUNTIME\_READY\_IMPLICIT\_PLUS\_EXPLICIT removes the explicit obligation while preserving implicit readiness.

curl\_global\_cleanup from RUNTIME\_READY\_IMPLICIT\_ONLY can remove the remaining runtime reference without inventing an explicit cleanup obligation.

curl\_global\_cleanup from an already uninitialized runtime is represented as an implementation-level no-op and is not automatically classified as D4.

The cleanup transitions correctly reflect the pinned implementation’s reference-sensitive initialization counter.

Implicit runtime readiness is not silently treated as the same obligation created by an explicit curl\_global\_init.



Review the separation between:

* actual runtime readiness;
* explicit `curl\_global\_init` cleanup obligation;
* implicit readiness established by successful `curl\_easy\_init`;
* failed explicit initialization;
* reference-sensitive `curl\_global\_cleanup`.

Confirm that implicit readiness is not silently treated as the same explicit
cleanup obligation.

\---

### TS-RR04 — Easy-handle lifecycle

Decision: PASS

Notes: A non-NULL curl\_easy\_init result creates a caller-owned easy-handle resource.

The newly created easy handle enters the EASY\_OWNED\_DETACHED state.

A non-NULL curl\_easy\_init result creates an individual curl\_easy\_cleanup obligation.

A NULL curl\_easy\_init result does not create an easy-handle resource.

curl\_easy\_setopt requires a live easy handle.

curl\_easy\_setopt leaves the easy-handle lifetime and membership state unchanged.

A curl\_easy\_setopt failure does not release the easy handle.

The complete CURLOPT-specific pointer and memory-lifetime surface remains outside the frozen scope.

curl\_easy\_perform is permitted when the easy handle is live and detached.

The easy handle remains live and detached after curl\_easy\_perform returns.

A transfer failure does not release the easy handle or discharge its cleanup obligation.

Repeated curl\_easy\_perform calls on the same live detached handle are correctly classified as VALID.

curl\_easy\_perform while the handle is attached to a multi handle is correctly classified as D6 VIOLATION-MUST.

curl\_easy\_reset resets options without releasing the easy handle.

curl\_easy\_reset preserves ownership and the existing cleanup obligation.

curl\_easy\_cleanup on a live detached handle transitions it to EASY\_RELEASED.

curl\_easy\_cleanup while the handle remains attached to a multi handle is correctly classified as D6 VIOLATION-MUST.

Ordinary use of an easy handle after cleanup is correctly classified as D3 VIOLATION-MUST.

Exiting with a live detached or attached easy handle is correctly classified as a missing-cleanup D5 VIOLATION-MUST.

The reviewed easy-handle lifecycle is consistent with the frozen V3 scope and approved pinned source evidence.



Review:

* non-NULL `curl\_easy\_init` resource creation;
* `curl\_easy\_setopt`;
* detached `curl\_easy\_perform`;
* repeated easy-perform use;
* `curl\_easy\_reset`;
* detached cleanup;
* use-after-cleanup;
* exit cleanup obligation.

\---

### TS-RR05 — Multi-handle membership and ownership

Decision: REVISION\_REQUIRED

Notes: curl\_multi\_init correctly requires prior global runtime readiness.

A non-NULL curl\_multi\_init result correctly creates a caller-owned MULTI\_OWNED resource.

A NULL curl\_multi\_init result correctly creates no multi-handle resource.

A successful curl\_multi\_add\_handle correctly attaches a live detached easy handle to the specified live multi handle.

Easy-handle ownership correctly remains with the caller after attachment.

A duplicate add returning CURLM\_ADDED\_ALREADY correctly leaves membership unchanged.

The duplicate-add error is correctly not treated by itself as a protocol violation.

A successful curl\_multi\_remove\_handle correctly detaches the easy handle from the same multi handle.

A repeated remove of an already detached easy handle correctly returns CURLM\_OK and leaves membership unchanged.

curl\_easy\_perform while the easy handle remains attached is correctly classified as D6 VIOLATION-MUST.

curl\_easy\_cleanup while the easy handle remains attached is correctly classified as D6 VIOLATION-MUST.

Successful multi cleanup does not free caller-owned easy handles.

Successful multi cleanup does not discharge the individual cleanup obligations of those easy handles.

The draft correctly preserves the fact that affected easy handles remain caller-owned and still require curl\_easy\_cleanup.

Revision is required because M12 and M13 do not condition their cleanup effects on the return value of curl\_multi\_cleanup.

The pinned implementation can return CURLM\_RECURSIVE\_API\_CALL or CURLM\_BAD\_HANDLE before completing multi-handle release.

The draft’s return-condition policy does not currently include curl\_multi\_cleanup

A successor must specify that only curl\_multi\_cleanup returning CURLM\_OK transitions the multi handle to MULTI\_RELEASED.

Only a successful curl\_multi\_cleanup may discharge the multi-handle cleanup obligation.

The implementation-derived detachment of remaining easy handles must apply only to the successful cleanup path.

If curl\_multi\_cleanup returns non-CURLM\_OK, the draft must not assert successful multi release or complete easy-handle detachment.

After a non-CURLM\_OK cleanup result, the multi cleanup obligation must remain outstanding and any unresolved membership state must be represented conservatively.



Review:

* `curl\_multi\_init`;
* add/remove membership;
* duplicate add;
* repeated remove;
* easy ownership remaining with caller;
* prohibition on easy-perform while attached;
* easy cleanup requiring detachment;
* multi cleanup not discharging easy cleanup obligations.

\---

### TS-RR06 — `curl\_multi\_perform` return-conditioned state

Decision: REVISION\_REQUIRED

Notes: A curl\_multi\_perform return of CURLM\_OK correctly preserves the MULTI\_OWNED state.

CURLM\_OK correctly does not imply that every individual transfer succeeded.

A non-CURLM\_OK return correctly transitions the multi handle to MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN.

The post-error state preserves caller ownership of the multi handle.

The post-error state does not silently assume that transfers can continue normally.

Successful removal of an attached easy handle is permitted from both MULTI\_OWNED and MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN.

The documented recovery sequence of removing all handles and adding new ones is recognized.

Plain curl\_multi\_perform repetition after an error is classified as UNKNOWN rather than silently declared VALID.

The final enforceable classification of that plain repetition is reviewed separately under TS-RR11.

Exiting with a multi handle in MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN correctly leaves the cleanup obligation active.

Revision is required because post-error cleanup behavior is not fully return-conditioned.

Rules M12 and M13 can assert MULTI\_RELEASED or complete easy-handle detachment without requiring curl\_multi\_cleanup to return CURLM\_OK.

The pinned implementation can return a cleanup error before completing release or detachment.

This can cause a failed cleanup attempt on a post-error multi handle to be treated as successful recovery or release.

A successor must specify that only curl\_multi\_cleanup returning CURLM\_OK transitions the multi handle to MULTI\_RELEASED.

A non-CURLM\_OK cleanup result must preserve the cleanup obligation.

A non-CURLM\_OK cleanup result must not assert complete easy-handle detachment.

Any membership or ownership state not established after a failed cleanup must remain conservatively represented.



Review whether:

* `CURLM\_OK` preserves normal multi ownership;
* non-`CURLM\_OK` establishes
`MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN`;
* recovery/removal/cleanup behavior is represented conservatively;
* plain repetition after error is not silently declared valid.

\---

### TS-RR07 — Verdict semantics and uncertainty discipline

Decision: REVISION\_REQUIRED

Notes: The conceptual definition of VALID is correct.

VALID requires all modeled source-backed preconditions and obligations to be satisfied.

VALID correctly excludes paths controlled by unresolved normative-strength or model-coverage uncertainty.

The conceptual definition of VIOLATION-MUST is correct.

VIOLATION-MUST is limited to a definite violation of an enforceable source-backed rule.

The conceptual definition of VIOLATION-MAY is correct.

VIOLATION-MAY is expressly limited to multiple feasible path or state alternatives where at least one alternative violates an enforceable rule and at least one does not.

VIOLATION-MAY is expressly not used for uncertainty about normative strength.

No current protocol rule incorrectly uses VIOLATION-MAY as a substitute for normative uncertainty.

The conceptual definition of UNKNOWN is correct.

UNKNOWN is first-class and covers insufficient evidence, bounded-model uncertainty, and unresolved normative strength.

The representation policy expressly prohibits converting UNKNOWN to VALID.

The explicit non-claims also confirm that unresolved review items are not silently converted to VALID.

Revision is required because verdict-valued fields do not consistently use only the four declared verdict values.

The draft uses the additional undefined verdict string:

UNKNOWN\_PENDING\_NR01

The draft uses the additional undefined verdict string:

UNKNOWN\_UNTIL\_SPECIFIC\_SUBSEQUENT\_EVENT\_OR\_REVIEW\_RULE\_APPLIES

The draft uses the additional undefined verdict string:

VALID\_WITH\_RESPECT\_TO\_D4\_ONLY

The draft uses the additional undefined verdict string:

VALID\_WITH\_RESPECT\_TO\_REPEAT\_ADD\_PROTOCOL\_RULE

The draft uses the additional undefined verdict string:

VALID\_WITH\_RESPECT\_TO\_REPEAT\_REMOVE

These qualified strings create undeclared fifth-category variants in machine-readable verdict fields.



A successor must restrict every verdict-valued field to exactly:

VALID

VIOLATION-MUST

VIOLATION-MAY

UNKNOWN



Pending or conditional explanations must be stored in separate fields such as review\_item, verdict\_scope, unknown\_reason, or classification\_note.

UNKNOWN\_PENDING\_NR01 must become the base verdict UNKNOWN with NR01 recorded separately.

UNKNOWN\_UNTIL\_SPECIFIC\_SUBSEQUENT\_EVENT\_OR\_REVIEW\_RULE\_APPLIES must become the base verdict UNKNOWN with its condition recorded separately.

D4-only, duplicate-add, and repeated-remove conclusions should be represented as scoped rule facts or separate classification fields rather than new VALID verdict variants.

This revision preserves the correct uncertainty discipline while making the four-verdict contract unambiguous.



Review the meanings and separation of:

* `VALID`;
* `VIOLATION-MUST`;
* `VIOLATION-MAY`;
* `UNKNOWN`.

Confirm that `VIOLATION-MAY` is used for feasible path/state uncertainty and
is not used as a substitute for unresolved normative strength.

Confirm that `UNKNOWN` is first-class and is never silently converted to
`VALID`.

\---

### TS-RR08 — Exit obligations and defect-taxonomy mapping

Decision: REVISION\_REQUIRED

Notes: The draft defines all eight defect classes D1 through D8.

The existing D1 mapping for curl\_multi\_init without runtime readiness is justified by the frozen V3 rule.

The draft does not explicitly map ordinary easy-handle operations before successful easy-handle acquisition to D1.

The draft does not explicitly map ordinary multi-handle operations before successful multi-handle acquisition to D1.

The existing D2 mapping for ordinary libcurl use after failed explicit global initialization is justified.

The draft does not explicitly map ordinary easy-handle operations on a NULL curl\_easy\_init result to D2.

The draft does not explicitly map ordinary multi-handle operations on a NULL curl\_multi\_init result to D2.

The existing D3 mappings for easy-handle and multi-handle use after release are justified by documentation declaring post-cleanup use illegal.

The draft contains no explicit D4 rule.

Frozen V3 expressly maps a second curl\_easy\_cleanup of the same released easy handle to D4.

Frozen V3 expressly maps a second curl\_multi\_cleanup of the same released multi handle to D4.

Generic D3 use-after-release rules do not provide an unambiguous cleanup-specific D4 classification.

The easy-handle exit obligation is justified.

A successful non-NULL curl\_easy\_init expressly requires a corresponding curl\_easy\_cleanup.

Exiting with a live easy handle is correctly classified as D5 VIOLATION-MUST.

The multi-handle exit obligation is justified.

A successful non-NULL curl\_multi\_init expressly MUST have a corresponding curl\_multi\_cleanup.

Exiting with a live normal or post-error multi handle is correctly classified as D5 VIOLATION-MUST.

A multi-handle cleanup obligation must be discharged only when curl\_multi\_cleanup returns CURLM\_OK.

The explicit global-cleanup exit obligation is correctly kept separate from runtime readiness.

The current UNKNOWN status for missing explicit global cleanup does not impose an unjustified MUST.

Its final normative classification is reviewed separately under TS-RR09.

The existing D6 mappings for curl\_easy\_perform while attached and curl\_easy\_cleanup before detachment are justified.

No existing D7 enforceable rule is present.

The wrong-multi removal association case remains UNKNOWN and is reviewed separately under TS-RR13.

No existing D8 enforceable rule is present.

Premature global cleanup and cleanup under the wrong state or return condition therefore remain incompletely mapped.

The premature-global-cleanup classification is reviewed separately under TS-RR14.

No existing VIOLATION-MUST rule was found to have an unjustified MUST status.

Revision is required because the taxonomy coverage is incomplete rather than because the existing MUST rules are too strong.

A successor must add explicit D1 rules for ordinary operations before successful resource acquisition.

A successor must add explicit D2 rules for ordinary operations that rely on failed or NULL acquisition results.

A successor must add cleanup-specific D4 VIOLATION-MUST rules for repeated easy and multi cleanup after release.

A successor must ensure that a failed curl\_multi\_cleanup does not discharge the multi-handle D5 exit obligation.

A successor must explicitly preserve the documented curl\_easy\_cleanup(NULL) no-op exception.

A successor must explicitly model curl\_multi\_cleanup(NULL) as returning CURLM\_BAD\_HANDLE, releasing nothing, and not discharging any obligation.

D7 and D8 mappings must be completed consistently with the separate TS-RR13 and TS-RR14 decisions.



Review D1-D8 mappings and the exit obligations for:

* easy handles;
* multi handles;
* explicit global cleanup.

Identify any rule whose defect class or MUST-status is not justified.

\---

### TS-RR09 — NR01: explicit global cleanup at exit

Decision: REVISION\_REQUIRED

Notes: A successful explicit curl\_global\_init acquires process-wide resources.

The approved documentation identifies curl\_global\_cleanup as the companion function that releases those resources.

The documentation states that curl\_global\_cleanup should be called once for each curl\_global\_init.

The approved libcurl overview requires the number of global initialization and cleanup calls to be the same.

The overview also places curl\_global\_cleanup after the final use of libcurl.

Frozen V3 expressly projects a missing matching curl\_global\_cleanup after successful explicit curl\_global\_init to defect class D5.

The bounded model tracks this responsibility as EXPLICIT\_CLEANUP\_DUE.

When the program exits with EXPLICIT\_CLEANUP\_DUE, the required matching cleanup has definitely not occurred.

There is no remaining path or state uncertainty about whether that explicit obligation is outstanding.

The current UNKNOWN\_PENDING\_NR01 treatment is therefore too weak for the bounded explicit-initialization scenario.

A successor must classify exit with EXPLICIT\_CLEANUP\_DUE as D5 VIOLATION-MUST.

Rule G10 must use enforcement MUST.

Rule G10 must use verdict VIOLATION-MUST.

The explicit-global exit obligation must use missing\_cleanup\_verdict VIOLATION-MUST.

The obligation must be discharged only by a matching curl\_global\_cleanup.

This enforceable rule must apply only after a successful explicit curl\_global\_init.

Implicit readiness established by curl\_easy\_init must not create this explicit cleanup obligation.

A failed explicit curl\_global\_init must not create this cleanup obligation.

Repeated explicit initialization beyond the bounded reviewed model may remain UNKNOWN rather than inventing unbounded reference-count semantics.



Review the current treatment:

`UNKNOWN\_PENDING\_NR01`

for an outstanding explicit global-cleanup obligation at exit.

State whether the exact current treatment is acceptable or whether it should
be changed to a specific enforceable classification.

\---

### TS-RR10 — NR02: multi cleanup with attached easy handles

Decision: REVISION\_REQUIRED

Notes: The approved documentation describes the preferred cleanup order as:

curl\_multi\_remove\_handle

curl\_easy\_cleanup

curl\_multi\_cleanup

The curl\_multi\_cleanup documentation uses the word should for this ordering.

The curl\_multi\_add\_handle documentation also says the easy handle should be removed before terminating the easy and multi handles.

Frozen V3 expressly prohibits silently strengthening the complete sequence to an unconditional MUST.

The pinned implementation permits curl\_multi\_cleanup to process a multi handle that still contains caller-owned easy handles.

On a successful curl\_multi\_cleanup, the implementation clears the easy-to-multi associations.

The successful cleanup does not free the caller-owned easy handles.

The affected easy handles remain live and caller-owned.

Each affected easy handle retains its independent curl\_easy\_cleanup obligation.

Failure to perform the later individual easy cleanup remains D5 VIOLATION-MUST.

Calling curl\_easy\_cleanup while an easy handle is still attached remains D6 VIOLATION-MUST.

Successful multi cleanup first removes the attachment structurally, so later easy cleanup is not an attached-handle cleanup.

The source evidence supports a cleanup-order recommendation rather than an unconditional MUST violation.

VIOLATION-MAY must not be used because there is no feasible-path uncertainty controlling the normative strength.

The current UNKNOWN treatment should therefore not remain after this independent review.

A successor must classify remove → easy-cleanup → multi-cleanup as the recommended ordering.

A successful curl\_multi\_cleanup with attached easy handles must not be classified as an enforceable violation solely because explicit curl\_multi\_remove\_handle was skipped.

The recommendation must not discharge or weaken the separate MUST cleanup obligation for every easy handle.

The structural detachment effect must apply only when curl\_multi\_cleanup returns CURLM\_OK.

If curl\_multi\_cleanup returns non-CURLM\_OK, the draft must not assume complete detachment or release.

The successor should record the ordering as a non-enforceable recommendation in a separate classification field rather than using UNKNOWN, VIOLATION-MAY, or an invented qualified verdict.



Review the current treatment where the pinned implementation structurally
detaches remaining caller-owned easy handles but documentation describes an
ordered remove → easy-cleanup → multi-cleanup sequence.

State whether current `UNKNOWN` treatment is acceptable or requires a precise
MUST/MAY/recommendation classification.

\---

### TS-RR11 — NR03: plain multi-perform repetition after error

Decision: REVISION\_REQUIRED

Notes: A non-CURLM\_OK curl\_multi\_perform result correctly establishes MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN.

The approved documentation states that the state of all transfers is uncertain after such an error.

The documentation further states that those transfers cannot be continued.

The same multi handle should not receive another curl\_multi\_perform call unless all handles are first removed and handles are added again.

The reviewed case is a plain repetition without that documented recovery sequence.

There is no path uncertainty about whether the prior curl\_multi\_perform returned non-CURLM\_OK.

There is no path uncertainty about whether the same multi handle is being used again.

There is no path uncertainty about whether the required remove-and-re-add recovery was skipped.

VIOLATION-MAY is therefore not appropriate.

The source wording that transfers cannot be continued supports an enforceable ordering rule.

Frozen V3 projects this plain continuation case to defect class D6.

The current UNKNOWN treatment is too weak.

A successor must classify plain curl\_multi\_perform repetition after a non-CURLM\_OK result, without documented recovery, as D6 VIOLATION-MUST.

Rule M08 must use enforcement MUST.

Rule M08 must use verdict VIOLATION-MUST.

The multi handle must remain in MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN after the prohibited repetition unless another evidenced transition applies.

curl\_multi\_remove\_handle must remain available in the post-error state.

curl\_multi\_cleanup must remain available as a release path, subject to its own return-conditioned cleanup rules.

The successor must also add an explicit recovery transition.

The recovery transition must require removal of all handles from the post-error multi handle.

The recovery transition must then require successful addition of handles again before curl\_multi\_perform can resume normally.

After the complete documented recovery sequence, the multi handle may return to the normal MULTI\_OWNED state.

Partial removal or re-addition before all prior handles are removed must not silently clear the post-error uncertainty.



Review the current `UNKNOWN` treatment after a non-`CURLM\_OK`
`curl\_multi\_perform` when the program plainly repeats `curl\_multi\_perform`
without documented recovery.

State whether the current treatment is acceptable or should become a specific
enforceable violation class.

\---

### TS-RR12 — NR04: `curl\_easy\_init(NULL-result)` runtime post-state

Decision: REVISION\_REQUIRED

Notes: The set-valued runtime post-state is source-grounded.

When curl\_easy\_init is called from RUNTIME\_UNINITIALIZED, implicit global initialization is attempted first.

If implicit global initialization fails, the implementation reverses the reference-count increment.

That failure path leaves the runtime in RUNTIME\_UNINITIALIZED.

If implicit global initialization succeeds, Curl\_open is then attempted.

If Curl\_open fails, curl\_easy\_init returns NULL without reversing the successful implicit initialization.

That failure path leaves the runtime in RUNTIME\_READY\_IMPLICIT\_ONLY.

A NULL result creates no easy-handle resource.

The correct runtime post-state set is therefore:

RUNTIME\_UNINITIALIZED

RUNTIME\_READY\_IMPLICIT\_ONLY

The draft correctly avoids selecting either runtime state without supporting path evidence.

Revision is required because dependent reasoning must not automatically become UNKNOWN in every case.

The draft defines VIOLATION-MAY specifically for multiple feasible path or state alternatives where at least one alternative violates an enforceable rule and at least one does not.

The two E04 runtime alternatives are feasible path or state alternatives.

If a later event is valid in one runtime alternative and violates an enforceable rule in the other, the correct joined verdict is VIOLATION-MAY.

For example, runtime readiness for a later non-exempt operation can differ between the two alternatives.

If all feasible alternatives produce the same verdict, that common verdict must be used.

UNKNOWN should be used only when the available evidence or bounded model cannot determine the applicable rule or normative strength.

The mere existence of a known finite set of feasible runtime states is not by itself sufficient to force UNKNOWN.

The approved documentation also states that other curl functions cannot be used after curl\_easy\_init returns NULL.

A definite ordinary continuation prohibited by that failed acquisition must be handled by the applicable D2 rule and must not be weakened solely because the internal runtime state is set-valued.

A successor must retain the two-state E04 runtime post-state.

A successor must remove the blanket verdict\_if\_future\_reasoning\_depends\_on\_exact\_runtime\_state value of UNKNOWN.

A successor must evaluate dependent events across both feasible runtime alternatives.

A mixed valid and enforceable-violation result must produce VIOLATION-MAY.

A result controlled by unresolved normative or model-coverage evidence may remain UNKNOWN.

No explicit global-cleanup obligation may be created by either E04 failure path.



Review the set-valued runtime post-state when `curl\_easy\_init` is invoked from
an uninitialized runtime and returns `NULL`.

The implementation permits failure before successful implicit global init or
after successful implicit initialization during `Curl\_open`.

Confirm whether dependent reasoning should remain `UNKNOWN` when the exact
post-state cannot be established.

\---

### TS-RR13 — NR05: removing an easy handle through the wrong multi

Decision: REVISION\_REQUIRED

Notes: The membership model associates each attached easy handle with one specific multi handle.

A successful curl\_multi\_remove\_handle is defined only when the easy handle is attached to the supplied multi handle.

Removing an already detached easy handle is a separate case.

The pinned implementation returns CURLM\_OK for repeated removal of an already detached easy handle.

That repeated-remove case is not a protocol violation by itself.

The wrong-multi case occurs when the easy handle is live and attached, but it is attached to a different multi handle.

The pinned implementation explicitly detects this mismatched association.

The wrong-multi call returns CURLM\_BAD\_EASY\_HANDLE.

The call does not detach the easy handle from its actual multi handle.

The easy handle remains attached to its original multi handle.

There is no path uncertainty about which multi handle owns the membership relation.

There is no normative-strength uncertainty about the rejected association.

The current UNKNOWN classification is therefore too weak.

D7 is the more precise defect class.

D7 covers ownership or resource-association misuse.

D6 is less precise because the primary defect is not call timing or ordering.

The primary defect is supplying a multi handle that does not own the easy-handle membership relation.

A successor must classify wrong-multi curl\_multi\_remove\_handle as D7 VIOLATION-MUST.

Rule M11 must use enforcement MUST.

Rule M11 must use verdict VIOLATION-MUST.

Rule M11 must preserve the actual easy-to-multi association after the rejected call.

The CURLM\_BAD\_EASY\_HANDLE return must not be treated as a successful detachment.

This classification must remain distinct from the valid repeated-remove case for an already detached easy handle.



Review whether the current `UNKNOWN` protocol classification for a
wrong-multi `curl\_multi\_remove\_handle` should remain conservative or should
be mapped to a specific D6/D7 enforceable violation.

\---

### TS-RR14 — NR06: global cleanup while live resources remain

Decision: REVISION\_REQUIRED

Notes: The draft correctly avoids classifying curl\_global\_cleanup solely by cleanup call count.

The pinned implementation uses a global initialization reference count.

curl\_global\_cleanup with a zero reference count is an implementation-level no-op.

A zero-reference cleanup is therefore not automatically a D4 double-cleanup violation.

curl\_global\_cleanup that decrements the count while another reference remains does not remove runtime readiness.

That case must remain distinct from cleanup that removes the final runtime reference.

The reviewed NR06 condition occurs only when curl\_global\_cleanup transitions the runtime to RUNTIME\_UNINITIALIZED while a modeled easy or multi resource remains live.

The approved documentation places curl\_global\_cleanup after the application is done using libcurl.

The approved overview places global cleanup after the final use of libcurl.

A live easy or multi resource means the modeled resource lifecycle has not been completed.

Frozen V3 expressly maps premature removal of required global readiness while modeled resources remain live to D8.

The draft correctly records the real transition to RUNTIME\_UNINITIALIZED.

The draft does not, however, classify the premature cleanup event itself as an enforceable violation.

Rule X02 currently uses UNKNOWN and addresses only possible subsequent operations.

This is too weak because the cleanup call has already removed required runtime readiness under the wrong live-resource state.

A successor must classify the cleanup event as D8 VIOLATION-MUST when it removes the final runtime reference while any modeled easy or multi resource remains live.

The actual runtime transition to RUNTIME\_UNINITIALIZED must still be applied even though the cleanup event is a violation.

Any later operation that requires runtime readiness must be evaluated from the resulting uninitialized state.

A cleanup that leaves another runtime reference ready must not be classified under this specific NR06 rule.

A cleanup performed after all modeled libcurl resources have completed their lifecycles must not be classified under this specific NR06 rule.

A zero-reference no-op must remain non-D4 unless some separate source-backed rule applies.

The successor must preserve the distinction between runtime readiness and the explicit global-cleanup obligation.

The final rule must remain state-sensitive and must not be reduced to counting curl\_global\_init and curl\_global\_cleanup calls.



Review the state-sensitive treatment of `curl\_global\_cleanup` that removes
runtime readiness while live libcurl resources remain.

Confirm whether the draft appropriately avoids classifying this solely by
cleanup call count.

\---

### TS-RR15 — Source traceability and quarantine

Decision: PASS

Notes: The approved source-evidence manifest contains exactly 21 files.

The frozen V3 scope also identifies exactly 21 approved source-evidence files.

The manifest and frozen V3 evidence path sets are identical.

The manifest and frozen V3 SHA-256 values are identical for every approved source file.

All 21 packaged source-evidence files are present.

All 21 packaged source-evidence file hashes match their recorded SHA-256 values.

The source-evidence directory contains no additional file outside the approved 21-file set.

The approved evidence consists only of pinned curl documentation, public headers, and implementation source files.

The source-evidence map contains twelve explicit technical assertions.

Each source-evidence-map assertion identifies its supporting approved file, line range, and SHA-256 value.

The important global-runtime rules are traceable to the frozen V3 scope and approved lib/easy.c evidence.

The important easy-handle lifecycle rules are traceable to the frozen V3 scope and approved easy-interface documentation or implementation evidence.

The important multi membership, ownership, perform, removal, and cleanup rules are traceable to the frozen V3 scope and approved multi-interface documentation or implementation evidence.

Rules derived directly from frozen semantic guardrails are identified as frozen-V3 rules.

Implementation-derived structural facts are distinguished from documentation-derived normative rules.

The source-evidence map records prohibited\_evidence\_used as false.

No generated-driver artifact is present in the approved source-evidence tree.

No selected-sample membership artifact is present in the approved source-evidence tree.

No raw model-response artifact is present in the approved source-evidence tree.

No compiler-log semantic artifact is present in the approved source-evidence tree.

No gold-label artifact is present in the approved source-evidence tree.

No analyzer-output artifact is present in the approved source-evidence tree.

No baseline-output artifact is present in the approved source-evidence tree.

No LLM-review artifact is present in or cited by the immutable review package as technical-specification evidence.

No repair artifact is present in the approved source-evidence tree.

The draft explicitly exposes NR01 through NR06 as independent-review items.

The draft uses UNKNOWN for unresolved normative or bounded-model questions rather than silently declaring them VALID.

The draft explicitly states that unresolved SHOULD or MAY wording is not silently upgraded to MUST.

The semantic revisions identified by this review do not indicate a source-quarantine breach.

The package satisfies the required source-traceability and evidence-quarantine boundary.



Confirm that:

* all important technical rules are traceable to the frozen V3 scope and/or
approved pinned source evidence;
* the package contains exactly the approved source-evidence class;
* no prohibited generated-driver, gold, analyzer, baseline, LLM-review, or
repair evidence is used;
* unresolved normative issues are exposed rather than hidden.

\---

## Overall technical review decision

Choose exactly one:

Overall decision: REVISION\_REQUIRED

Notes:

The exact Working Draft V1 identity, SHA-256, author commit, author tree, target blob, and Decision 0027 binding were independently verified.

The draft remains within the frozen twelve-function API surface.

The separation between runtime readiness and the explicit global-cleanup obligation is technically sound.

The core easy-handle lifecycle is technically sound.

The approved 21-file source-evidence set is complete and hash-consistent.

No prohibited evidence class is present in or cited by the immutable review package.

The exact Working Draft V1 is not technically adequate to proceed to canonicalization without revision.

curl\_multi\_cleanup transitions must be conditioned on a CURLM\_OK return.

A failed curl\_multi\_cleanup must not release the multi handle, discharge its cleanup obligation, or assert complete easy-handle detachment.

The four-verdict contract must use only VALID, VIOLATION-MUST, VIOLATION-MAY, and UNKNOWN in verdict-valued fields.

Qualified or pending verdict information must be represented in separate scope, reason, or review-item fields.

The D1-D8 mapping requires explicit completion, including cleanup-specific D4 rules.

Exit with an outstanding explicit cleanup obligation from successful curl\_global\_init must be classified as D5 VIOLATION-MUST.

Multi cleanup with attached easy handles must be recorded as a non-enforceable ordering recommendation rather than remaining UNKNOWN or being strengthened to an unconditional MUST.

Plain curl\_multi\_perform repetition after a non-CURLM\_OK result without complete remove-and-re-add recovery must be classified as D6 VIOLATION-MUST.

The multi-perform post-error model must include an explicit transition back to normal ownership after the complete documented recovery sequence.

The set-valued runtime post-state after a NULL curl\_easy\_init result must be preserved.

Downstream conclusions over that state set must follow the verdict join rules rather than automatically becoming UNKNOWN.

Wrong-multi curl\_multi\_remove\_handle must be classified as D7 VIOLATION-MUST and must leave the actual membership unchanged.

curl\_global\_cleanup that removes the final runtime reference while modeled easy or multi resources remain live must be classified as D8 VIOLATION-MUST.

Global cleanup must remain reference-sensitive and must not be classified solely by cleanup call count.

The required corrections are bounded and source-grounded, so FAIL is not warranted.

Working Draft V1 must remain immutable.

The required semantic corrections must be made in a new immutable successor or revision.

This decision does not authorize creation or use of canonical curl.json.

Generated-driver inspection remains unauthorized.

Gold annotation remains unauthorized.

Analyzer implementation or execution remains unauthorized.

Baseline execution remains unauthorized.

Repair implementation or repair-output inspection remains unauthorized.



An approval here authorizes only a **subsequent separate canonicalization
operation** for the exact approved Working Draft V1.

It does not itself create or authorize use of canonical `curl.json`.

Generated-driver inspection, gold annotation, analyzer implementation,
baseline execution, and repair remain separately governed and unauthorized
at this boundary.

## Reviewer identity

Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 19 / August / 2026



## Post-review rule

No assistant-generated or synthetic human approval is permitted.

If revision is required, the exact V1 author checkpoint must remain immutable;
create an immutable successor rather than editing V1 in place.

