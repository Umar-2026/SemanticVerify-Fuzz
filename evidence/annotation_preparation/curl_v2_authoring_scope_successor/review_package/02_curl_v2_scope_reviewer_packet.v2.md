# curl V2 Source-Only Authoring-Scope Successor Independent Review Packet

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

Repository target:

`config/annotation/curl_v2_authoring_scope.v2.json`

Exact V2 scope SHA-256:

`f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df`

Author checkpoint commit:

`fae56e4f5196fd0460046723ef9d6a4e26234612`

Author checkpoint tree:

`0cb044dd10d48908895425512f5a2e7c1e8633b9`

Git blob for the exact V2 scope:

`5c88a9e00d9ad2e8e4a59aa41488dec016c58cad`

Package-local byte-identical review copy:

`evidence/annotation_preparation/curl_v2_authoring_scope_successor/review_package/03_curl_v2_authoring_scope.v2.json`

This V2 artifact is an immutable **author checkpoint**. It is **not** a frozen
curl authoring scope and it is **not** a canonical protocol specification.

Human review completed: `NO`

Technical curl working-draft authoring authorized: `NO`

## Exact predecessor

Immutable V1 scope:

`config/annotation/curl_v1_authoring_scope.v1.json`

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
libcurl global runtime readiness from the explicit `curl_global_init()` cleanup
obligation.

The pinned source also establishes a `curl_multi_perform()` post-error
condition that V1 did not represent.

V2 additionally removes the automatic call-count D4 classification for an
unmatched extra `curl_global_cleanup()`, records pinned repeated-remove no-op
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

* `docs/libcurl/curl_easy_cleanup.md` — SHA-256 `d39b972fe61d57d72ab60c310d8fe8ea06b253cb008bceee7535fbaed36851a7`
* `docs/libcurl/curl_easy_init.md` — SHA-256 `59b98da718399b47958e3e1d812accaa05b9a1016c62797bf490dd215e6b1927`
* `docs/libcurl/curl_easy_perform.md` — SHA-256 `6fe91c0b04879dcaac1036bc1307bb3fb85be6102d47d788af7f2c620ba098c7`
* `docs/libcurl/curl_easy_reset.md` — SHA-256 `d2b6932349acbdf4d3e230ecda20cf13edf66520e47b3d43bffa87b2948e7cc0`
* `docs/libcurl/curl_easy_setopt.md` — SHA-256 `8b6f4283da3eb20a16f320cd90baaa9d8276b585750a782916451422e87cc951`
* `docs/libcurl/curl_global_cleanup.md` — SHA-256 `dce5ac828e85d5e1a303333163c1d71d3503816241f71809a7824370387bc1a1`
* `docs/libcurl/curl_global_init.md` — SHA-256 `0cb6702df283336798293eae8b5e57775852f56ea237b03384bdfabe27be7cbc`
* `docs/libcurl/curl_multi_add_handle.md` — SHA-256 `8964c4ff62cd009f6fa7ca72d5a0bfcf19822e259c2352f785d9b83e1084a90a`
* `docs/libcurl/curl_multi_cleanup.md` — SHA-256 `ad4d80cc39186e65e3a5e10231f41e61a8e4f8a16179013e98ee90a83ac4e67d`
* `docs/libcurl/curl_multi_init.md` — SHA-256 `6be119495ff8b99a79e5d45e4bb1be3aeeee3046e2b54cdb0e11565fdfaaa445`
* `docs/libcurl/curl_multi_perform.md` — SHA-256 `5b85efb586d552e0632a25b25b1642b26e82192694c8be5dfb86cffa5e23ae2e`
* `docs/libcurl/curl_multi_remove_handle.md` — SHA-256 `88809d1245dc0c66a672aedaba53a69fa7aa4dbb5d68eab3e1d8ff5946720938`
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

`REVISION_REQUIRED`

`FAIL`

Do not infer an overall approval from blank fields.

### V2-RR01 — Exact predecessor and immutable-target binding

Decision:

Notes:

Verify the exact V2 SHA-256, Git blob, author commit and tree.

Verify that the included V1 scope is exactly SHA-256
`d8e020cc14bd6c8ea9d679ba0f736bdce6098763d9b8ac0c0f95edaf8d9fd9c7` and that V1 remains immutable.

Verify Decisions 0021 and 0022 against their exact hashes.

### V2-RR02 — Runtime readiness versus explicit global cleanup obligation

Decision:

Notes:

Verify that V2 correctly distinguishes:

* genuinely uninitialized runtime;
* readiness established implicitly by successful `curl_easy_init()`;
* readiness established by explicit `curl_global_init()`; and
* the bounded case in which implicit and explicit references coexist.

Verify that `curl_multi_init()` does not receive the
`curl_easy_init()` automatic-global-init exception.

Verify that runtime readiness and explicit cleanup responsibility are not
silently conflated.

### V2-RR03 — Global cleanup and D4 reconciliation

Decision:

Notes:

Verify that an unmatched extra `curl_global_cleanup()` is **not** classified
as D4 solely by call count.

Verify the pinned implementation fact that zero reference count causes a
no-op return.

Also verify that cleanup can be state-sensitive when implicit readiness exists,
so premature cleanup remains eligible for path/state-sensitive D6/D8 treatment
where source-supported.

Explicitly decide the MUST/MAY strength of missing or wrongly timed explicit
global cleanup.

### V2-RR04 — `curl_multi_perform()` post-error protocol condition

Decision:

Notes:

Verify that a non-`CURLM_OK` return establishes the documented post-error
condition in which transfer state is uncertain.

Verify that V2 does not permit an ordinary repeat `curl_multi_perform()` as if
nothing happened.

Verify the documented remove/re-add recovery relationship.

Explicitly decide whether an unrecovered plain repeat is a MUST violation,
MAY violation, or another reviewer-approved protocol classification.

### V2-RR05 — Easy/multi membership and cleanup semantics

Decision:

Notes:

Verify:

* easy ownership is not transferred to the multi handle;
* `curl_easy_perform()` is prohibited while the easy handle is attached;
* successful remove re-enables easy-interface use;
* repeated remove of an already detached easy handle is not D4 merely by call
  count and is a pinned-implementation `CURLM_OK` no-op;
* repeated add while already attached is rejected by the pinned implementation;
* `curl_multi_cleanup()` does not free caller-owned easy handles; and
* the entire remove -> easy-cleanup -> multi-cleanup sequence is not silently
  strengthened from documented `should` wording into unconditional MUST.

Explicitly decide the normative strength of the broader cleanup sequence.

### V2-RR06 — Frozen surface and evidence preservation

Decision:

Notes:

Verify that V2 changes **no**:

* in-scope API function;
* pinned curl revision;
* scenario manifest;
* approved source-evidence set; or
* source-only quarantine boundary.

Verify that one-hop API expansion remains disabled.

### V2-RR07 — Representation and downstream authorization boundary

Decision:

Notes:

Verify that an eventual technical working draft must structurally represent
all independent modeled components under the single-schema `initial_state`
constraint without inventing synthetic protocol events.

Verify that this V2 scope checkpoint itself does **not** authorize:

* curl technical working-draft creation;
* canonical protocol finalization;
* generated-driver inspection;
* gold annotation;
* analyzer implementation;
* baseline execution; or
* repair.

Any requested semantic modification requires a new immutable V3 successor.
The reviewed V2 bytes must not be edited in place.

## Overall decision

Overall decision:

Reviewer name:

Reviewer role:

Review date:

Notes:

Allowed overall values:

`APPROVE_EXACT_V2_SCOPE_FOR_FREEZE`

`REVISION_REQUIRED`

`FAIL`

A blank overall decision means the review is incomplete.

## Post-review boundary

Only a real independent human review of these exact immutable V2 bytes may
authorize the next scope-freeze step.

The review completion must be recorded in **new review artifacts**. Do not edit
the immutable V2 target or this package copy to manufacture approval.
