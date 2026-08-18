# curl V2 Source-Only Authoring-Scope Successor Independent Review Packet

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

Repository target:

`config/annotation/curl\_v2\_authoring\_scope.v2.json`

Exact V2 scope SHA-256:

`f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df`

Author checkpoint commit:

`fae56e4f5196fd0460046723ef9d6a4e26234612`

Author checkpoint tree:

`0cb044dd10d48908895425512f5a2e7c1e8633b9`

Git blob for the exact V2 scope:

`5c88a9e00d9ad2e8e4a59aa41488dec016c58cad`

Package-local byte-identical review copy:

`evidence/annotation\_preparation/curl\_v2\_authoring\_scope\_successor/review\_package/03\_curl\_v2\_authoring\_scope.v2.json`

This V2 artifact is an immutable **author checkpoint**. It is **not** a frozen
curl authoring scope and it is **not** a canonical protocol specification.

Human review completed: `NO`

Technical curl working-draft authoring authorized: `NO`

## Exact predecessor

Immutable V1 scope:

`config/annotation/curl\_v1\_authoring\_scope.v1.json`

SHA-256:

`d8e020cc14bd6c8ea9d679ba0f736bdce6098763d9b8ac0c0f95edaf8d9fd9c7`

V1 scope freeze commit:

`9b3a33a358cd9cd0d4837b7221426d2e96d42239`

V1 scope freeze tree:

`5933e2ea78dc3e503251e47be49c16f8971cbda3`

Decision 0021:

`documentation/decisions/0021-curl-v1-source-only-authoring-scope-freeze.md`

SHA-256:

`9ef22ab551184808d3185c95d7286ab3c296bf6d9c29736c0312b84df78f18eb`

Decision 0022:

`documentation/decisions/0022-curl-v2-source-only-authoring-scope-successor.md`

SHA-256:

`f4bfbc72fcc218f56b8223bf0d36a0db24edd40e59fab21de6fbbac71406cf8b`

V1 edit in place allowed: `NO`

## Why V2 exists

Source-only reconciliation found that V1 cannot faithfully distinguish actual
libcurl global runtime readiness from the explicit `curl\_global\_init()` cleanup
obligation.

The pinned source also establishes a `curl\_multi\_perform()` post-error
condition that V1 did not represent.

V2 additionally removes the automatic call-count D4 classification for an
unmatched extra `curl\_global\_cleanup()`, records pinned repeated-remove no-op
behavior, and makes cleanup-order normative strength an explicit review item.

The API function set, pinned revision, scenario manifest and 21 approved
source-evidence files are unchanged.

## Review quarantine

Use only:

* the exact immutable V2 target;
* the package-local V2 target copy;
* the exact V1 predecessor included in this package;
* Decisions 0021 and 0022;
* the frozen scenario manifest binding;
* the approved pinned curl source evidence listed below; and
* already-approved protocol-governance material needed to interpret D1-D8.

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
* corpus prevalence or performance feedback; or
* failure-prompted post-hoc evidence outside the approved pinned source set.

## Approved pinned curl evidence

* `docs/libcurl/curl\_easy\_cleanup.md` — SHA-256 `d39b972fe61d57d72ab60c310d8fe8ea06b253cb008bceee7535fbaed36851a7`
* `docs/libcurl/curl\_easy\_init.md` — SHA-256 `59b98da718399b47958e3e1d812accaa05b9a1016c62797bf490dd215e6b1927`
* `docs/libcurl/curl\_easy\_perform.md` — SHA-256 `6fe91c0b04879dcaac1036bc1307bb3fb85be6102d47d788af7f2c620ba098c7`
* `docs/libcurl/curl\_easy\_reset.md` — SHA-256 `d2b6932349acbdf4d3e230ecda20cf13edf66520e47b3d43bffa87b2948e7cc0`
* `docs/libcurl/curl\_easy\_setopt.md` — SHA-256 `8b6f4283da3eb20a16f320cd90baaa9d8276b585750a782916451422e87cc951`
* `docs/libcurl/curl\_global\_cleanup.md` — SHA-256 `dce5ac828e85d5e1a303333163c1d71d3503816241f71809a7824370387bc1a1`
* `docs/libcurl/curl\_global\_init.md` — SHA-256 `0cb6702df283336798293eae8b5e57775852f56ea237b03384bdfabe27be7cbc`
* `docs/libcurl/curl\_multi\_add\_handle.md` — SHA-256 `8964c4ff62cd009f6fa7ca72d5a0bfcf19822e259c2352f785d9b83e1084a90a`
* `docs/libcurl/curl\_multi\_cleanup.md` — SHA-256 `ad4d80cc39186e65e3a5e10231f41e61a8e4f8a16179013e98ee90a83ac4e67d`
* `docs/libcurl/curl\_multi\_init.md` — SHA-256 `6be119495ff8b99a79e5d45e4bb1be3aeeee3046e2b54cdb0e11565fdfaaa445`
* `docs/libcurl/curl\_multi\_perform.md` — SHA-256 `5b85efb586d552e0632a25b25b1642b26e82192694c8be5dfb86cffa5e23ae2e`
* `docs/libcurl/curl\_multi\_remove\_handle.md` — SHA-256 `88809d1245dc0c66a672aedaba53a69fa7aa4dbb5d68eab3e1d8ff5946720938`
* `docs/libcurl/libcurl-easy.md` — SHA-256 `5b1e2b2c3cc94bbee837c306b9ce8afa0be1bb148f8d18fbc6374876d3d5ec94`
* `docs/libcurl/libcurl-multi.md` — SHA-256 `19b8aa18f2bd6a5c9bb4b33568cd669513a2fb7185afd3bd4a8e7bf6cb30b3c2`
* `docs/libcurl/libcurl.md` — SHA-256 `be4b4285651cc5cf1bc7cbbed79a8a1d5d2dfd72974115ec86843de3541bb81a`
* `include/curl/curl.h` — SHA-256 `f17ab2d4b216bd96df937dbe494ecae1ea167a3f0e56b8dea83cd32a58cca18a`
* `include/curl/easy.h` — SHA-256 `f101da02dd373151ea7b00082cb62c9d6e482361ab26b6d430ee96aab1b71565`
* `include/curl/multi.h` — SHA-256 `ab3278832925f69a68852e2c6b5a300884ee5f974a2291b642a7d1ef1ed49af9`
* `lib/easy.c` — SHA-256 `2c00a68e4cff5f8c69d4078f2a07316b553a9bdd0b1520f3246e3b1448bae483`
* `lib/multi.c` — SHA-256 `b5dc84f15ed14179acbd06ae6b108331c46dd6c7067395282f0d1a2c42a5cdf3`
* `lib/setopt.c` — SHA-256 `3738ff6a04a09f4941b9d9b7c79d2882a999fc20f0dcaf543ce5385eb4972dcc`

## Mandatory review decisions

For each item record exactly one of:

`PASS`

`REVISION\_REQUIRED`

`FAIL`

Do not infer an overall approval from blank fields.

### V2-RR01 — Exact predecessor and immutable-target binding

Decision: PASS

Notes: I manually verified the V2 SHA-256 as

f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df.

The review-package copy produced the same hash.



The V2 Git blob, author commit and tree identifiers were consistently recorded

as 5c88a9e00d9ad2e8e4a59aa41488dec016c58cad,

fae56e4f5196fd0460046723ef9d6a4e26234612, and

0cb044dd10d48908895425512f5a2e7c1e8633b9.



I manually verified the included V1 SHA-256 as

d8e020cc14bd6c8ea9d679ba0f736bdce6098763d9b8ac0c0f95edaf8d9fd9c7.

The exact-binding and review-package V1 copies matched. The package records V1

as immutable and disallows editing it in place.



Decision 0021 matched SHA-256

9ef22ab551184808d3185c95d7286ab3c296bf6d9c29736c0312b84df78f18eb.



Decision 0022 matched SHA-256

f4bfbc72fcc218f56b8223bf0d36a0db24edd40e59fab21de6fbbac71406cf8b.



Git identifiers were manually cross-checked across the binding manifests,

reviewer packet and branch-reference files.

### V2-RR02 — Runtime readiness versus explicit global cleanup obligation

Decision: PASS

Notes: I manually reviewed the V2 global-state model against the approved pinned curl

documentation and implementation.



V2 distinguishes RUNTIME\_UNINITIALIZED,

RUNTIME\_READY\_IMPLICIT\_ONLY, RUNTIME\_READY\_EXPLICIT\_ONLY, and

RUNTIME\_READY\_IMPLICIT\_PLUS\_EXPLICIT. These states separately represent a

genuinely uninitialized runtime, readiness established automatically by a

successful curl\_easy\_init(), readiness established by successful explicit

curl\_global\_init(), and the bounded coexistence of implicit and explicit

runtime references.



The pinned curl\_easy\_init documentation and lib/easy.c implementation confirm

the automatic-global-init exception. The global\_init implementation increments

the initialized reference count when initialization already exists, supporting

the bounded implicit-plus-explicit state. The curl\_global\_cleanup

implementation decrements this count and leaves runtime readiness present when

another reference remains.



The pinned curl\_multi\_init documentation provides no automatic-global-init

exception, and its lib/multi.c implementation creates the multi handle without

calling global\_init. Therefore curl\_multi\_init requires prior runtime

readiness.



V2 models EXPLICIT\_GLOBAL\_CLEANUP\_OBLIGATION separately from

GLOBAL\_RUNTIME\_REFERENCE\_STATE. Implicit curl\_easy\_init readiness does not

automatically establish the same explicit cleanup obligation, while successful

explicit curl\_global\_init does. Runtime readiness and explicit cleanup

responsibility are therefore not silently conflated.

### V2-RR03 — Global cleanup and D4 reconciliation

Decision: PASS

Notes: I manually reviewed the V2 global-cleanup treatment against the approved pinned

documentation and lib/easy.c implementation.



V2 does not classify an unmatched extra curl\_global\_cleanup as D4 solely by

call count. Its D4 projection contains double curl\_easy\_cleanup and double

curl\_multi\_cleanup, but no automatic global-cleanup call-count rule.



The pinned curl\_global\_cleanup implementation first checks whether the global

initialized reference count is zero. At zero it unlocks and returns without

further action, confirming that a zero-reference cleanup is an implementation

no-op.



When a reference exists, curl\_global\_cleanup decrements the reference count.

A transition from two references to one leaves runtime readiness established,

while a transition from one reference to zero performs global cleanup.

Therefore the effect of cleanup is state-sensitive.



V2 correctly records that cleanup from implicit-only readiness can remove the

remaining runtime reference. If modeled libcurl use remains live, such

premature cleanup is a MUST violation eligible for path/state-sensitive D6/D8

classification. If implicit and explicit references coexist and cleanup leaves

implicit readiness intact, the wrong timing is a MAY-level ordering defect

rather than an unconditional MUST violation.



I classify a missing matching explicit curl\_global\_cleanup as a MAY violation

and D5 cleanup-obligation defect because the dedicated pinned documentation

uses “should” wording. I classify wrongly timed cleanup as a MUST violation

only when it removes required runtime readiness while modeled libcurl use

remains live or continues without readiness being re-established. Otherwise,

wrong timing is a MAY-level ordering defect.



An unmatched cleanup is therefore not D4 by call count alone; its treatment

depends on the actual runtime reference state and the surrounding execution

path.

### V2-RR04 — `curl\_multi\_perform()` post-error protocol condition

Decision: PASS

Notes: I manually reviewed the curl\_multi\_perform post-error model against the approved

pinned curl\_multi\_perform documentation.



The documentation states that when curl\_multi\_perform returns an error, the

state of all transfers is uncertain and the transfers cannot be continued. It

also states that curl\_multi\_perform should not be called again on the same

multi handle unless all handles are first removed and handles are then added

again.



V2 uses return != CURLM\_OK as the error predicate and transitions the multi

resource into the explicit MULTI\_OWNED\_POST\_ERROR\_UNCERTAIN condition. It does

not represent an ordinary repeat curl\_multi\_perform as a valid continuation.

It permits curl\_multi\_remove\_handle in the post-error condition and records the

documented remove-all/re-add recovery relationship. It also permits

curl\_multi\_cleanup as a release path.



I classify an unrecovered plain repeat curl\_multi\_perform on the same multi

handle as a MUST violation under D6. Although one sentence uses “should not,”

the preceding source statement says that transfer state is uncertain and the

transfers cannot be continued. The documented recovery precondition must

therefore be satisfied before curl\_multi\_perform is resumed.



Removing only some attached handles does not satisfy the documented recovery

when other handles remain; all handles must be removed before the multi handle

is repopulated and curl\_multi\_perform is called again.

### V2-RR05 — Easy/multi membership and cleanup semantics

Decision: PASS

Notes: I manually reviewed the V2 easy/multi membership and cleanup model against the

approved pinned documentation and lib/multi.c implementation.



Adding an easy handle to a multi handle changes membership but does not

transfer ownership. The easy handle remains caller-owned while attached, and

curl\_multi\_cleanup does not free caller-owned easy handles. The pinned

curl\_multi\_cleanup implementation clears each external easy handle's multi

association while only closing internally owned handles. Each successfully

created caller-owned easy handle therefore still requires its own

curl\_easy\_cleanup.



The pinned curl\_multi\_add\_handle and curl\_easy\_perform documentation prohibit

curl\_easy\_perform while the easy handle remains attached. I classify such use

as a MUST violation. The curl\_multi\_remove\_handle documentation confirms that

a successful removal re-enables easy-interface use.



The pinned curl\_multi\_remove\_handle implementation returns CURLM\_OK without

state change when the easy handle is already detached. I therefore do not

classify repeated detached removal as D4 merely by call count. The pinned

curl\_multi\_add\_handle implementation rejects an already attached easy handle

with CURLM\_ADDED\_ALREADY and does not create duplicate membership.



I classify curl\_easy\_cleanup while the handle is still attached as a MUST

violation because the dedicated easy-cleanup documentation requires prior

removal. However, I do not strengthen the entire

curl\_multi\_remove\_handle -> curl\_easy\_cleanup -> curl\_multi\_cleanup sequence

into an unconditional MUST ordering rule. The broader sequence is documented

using “should” wording, and the pinned multi-cleanup implementation can clear

remaining memberships without freeing caller-owned easy handles.



I classify deviation from the broader total cleanup order as a MAY-level

ordering issue when membership is safely cleared and every caller-owned easy

handle is still eventually cleaned up. Failure to perform the required

individual easy-handle cleanup remains a MUST/D5 resource-cleanup violation.

### V2-RR06 — Frozen surface and evidence preservation

Decision: PASS

Notes: I manually compared the frozen V1 authoring scope with the exact V2 successor.



The in-scope API set remains unchanged at twelve functions:

curl\_easy\_init, curl\_easy\_setopt, curl\_easy\_perform, curl\_easy\_reset,

curl\_easy\_cleanup, curl\_multi\_init, curl\_multi\_add\_handle,

curl\_multi\_perform, curl\_multi\_remove\_handle, curl\_multi\_cleanup,

curl\_global\_init, and curl\_global\_cleanup. No function was added or removed.



The pinned curl revision remains

68720b4837284335b2d63cb358f8f6ce65f5bc55.



The scenario manifest remains

config/generation/scenario\_bindings.80.v10.json with SHA-256

a7ab361e6e2d41d9051e48bc7626f0be37c1df9ec35f788a9a019b010054a2db.

The bounded curl scenarios remain S01 through S10.



I compared the V1 and V2 source\_evidence arrays and the package-local checksum

ledger. The approved source-evidence set remains unchanged at 21 files, with

the same paths and SHA-256 values.



The source-only quarantine remains in force. Generated-driver source,

selected-sample membership, gold labels, analyzer output, baseline output,

LLM-review output, repair output, raw model responses, and compiler-log

semantic contents are not admitted as scope evidence.



V2 explicitly keeps one-hop API expansion disabled. Documentation references

to additional curl functions do not expand the twelve-function protocol

surface. I found no change to the API surface, pinned revision, scenario

manifest, approved evidence set, or source-only quarantine boundary.

### V2-RR07 — Representation and downstream authorization boundary

Decision: REVISION\_REQUIRED

Notes: I manually reviewed the representation and downstream authorization boundary.



The representation requirement is acceptable. V2 identifies the independent

GLOBAL\_RUNTIME\_REFERENCE\_STATE, EXPLICIT\_GLOBAL\_CLEANUP\_OBLIGATION,

EASY\_HANDLE, MULTI\_HANDLE, EASY\_MULTI\_MEMBERSHIP, and

MULTI\_PERFORM\_POST\_ERROR\_CONDITION components. It acknowledges the schema's

single initial\_state constraint and requires a combined/product-state or other

independently reviewable schema-approved representation. It also prohibits

inventing synthetic initialization or recovery protocol events.



The present checkpoint is correctly marked as not human-reviewed, not frozen,

not a canonical specification, and not authorized for technical working-draft

creation. The package documents also continue to prohibit generated-driver

inspection, gold annotation, analyzer implementation, baseline execution, and

repair.



However, the exact V2 JSON contains

working\_draft\_authoring\_authorized\_after\_exact\_v2\_human\_approval: true.

This conflicts with the reviewer packet, whose allowed approval is

APPROVE\_EXACT\_V2\_SCOPE\_FOR\_FREEZE and whose post-review boundary says that

human approval authorizes the next scope-freeze step. The JSON therefore

permits a downstream consumer to treat human approval as direct technical

working-draft authorization and bypass the separate freeze boundary.



This authorization conflict must be corrected in a new immutable V3 successor.

The current V2 bytes must remain unchanged. V3 should explicitly represent the

sequence from human approval, to scope-freeze authorization, to completed

scope freeze, and only then to technical working-draft authorization. It should

also retain explicit false authorization values for generated-driver

inspection, gold annotation, analyzer implementation, baseline execution, and

repair until their respective later gates are satisfied.

## Overall decision

\## Overall decision



Overall decision:

REVISION\_REQUIRED



Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad 

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 18 / August / 2026



Notes:

I completed the independent review of the exact curl V2 authoring-scope

successor.



V2-RR01 passed. The V2 and V1 hashes, recorded Git bindings, predecessor

relationship, and Decision 0021/0022 hashes were manually checked against the

supplied handoff records and package copies.



V2-RR02 passed. V2 correctly separates genuinely uninitialized runtime,

implicit readiness established by successful curl\_easy\_init(), explicit

readiness established by successful curl\_global\_init(), and the bounded

implicit-plus-explicit state. curl\_multi\_init does not receive the

curl\_easy\_init automatic-global-init exception. Runtime readiness and explicit

cleanup responsibility are represented separately.



V2-RR03 passed with the following normative decisions: an unmatched

curl\_global\_cleanup is not D4 by call count alone; zero-reference cleanup is a

pinned-implementation no-op; missing matching explicit global cleanup is a

MAY/D5 cleanup-obligation defect; and wrongly timed cleanup is a MUST D6/D8

violation when it removes required runtime readiness while modeled libcurl use

remains live. Wrong timing that leaves runtime readiness intact is a MAY-level

ordering defect.



V2-RR04 passed with the decision that an unrecovered plain repeat

curl\_multi\_perform after a non-CURLM\_OK return is a MUST/D6 violation. Recovery

requires removing all handles and adding handles again before resuming

curl\_multi\_perform on the same multi handle. Cleanup remains an allowed release

path.



V2-RR05 passed. Easy-handle ownership remains with the caller;

curl\_easy\_perform and curl\_easy\_cleanup while the easy handle is attached are

MUST violations; successful removal re-enables easy-interface use; repeated

detached removal is a CURLM\_OK no-op and not D4; repeated attached add is

rejected with CURLM\_ADDED\_ALREADY; and curl\_multi\_cleanup does not free

caller-owned easy handles. The complete remove -> easy-cleanup -> multi-cleanup

ordering is a MAY-level documented recommendation rather than an unconditional

MUST, while eventual individual cleanup of each caller-owned easy handle

remains mandatory.



V2-RR06 passed. The twelve-function API surface, pinned curl revision, scenario

manifest, ten-scenario binding, 21-file approved source-evidence set,

source-only quarantine boundary, and disabled one-hop expansion policy are

preserved.



V2-RR07 requires revision. The structural representation requirement correctly

covers the independent runtime, explicit-cleanup, easy-handle, multi-handle,

membership, and multi-perform post-error components under the single

initial\_state constraint without synthetic protocol events. The present

checkpoint is also marked unreviewed, unfrozen, and unauthorized for downstream

technical work.



However, the exact V2 JSON contains

working\_draft\_authoring\_authorized\_after\_exact\_v2\_human\_approval: true. This

conflicts with the reviewer packet, whose permitted approval value is

APPROVE\_EXACT\_V2\_SCOPE\_FOR\_FREEZE and whose post-review boundary authorizes only

the next scope-freeze step. The JSON can therefore be interpreted as allowing

technical working-draft authoring immediately after human approval, bypassing

the separate freeze boundary.



The current exact V2 scope is therefore not approved for freeze. Its bytes must

remain unchanged. A new immutable V3 successor is required to represent the

authorization sequence explicitly: human review -> scope-freeze authorization

\-> completed scope freeze -> technical working-draft authorization. Until that

successor is reviewed, canonical finalization, generated-driver inspection,

gold annotation, analyzer implementation, baseline execution, and repair remain

unauthorized.

## Post-review boundary

Only a real independent human review of these exact immutable V2 bytes may
authorize the next scope-freeze step.

The review completion must be recorded in **new review artifacts**. Do not edit
the immutable V2 target or this package copy to manufacture approval.

