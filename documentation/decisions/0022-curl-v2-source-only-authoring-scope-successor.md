# Decision 0022: curl V2 Source-Only Authoring-Scope Successor

Status: Author-side successor decision; independent human review required before V2 scope freeze

Date: 2026-08-17

## Predecessor

The immutable curl V1 authoring scope is:

`config/annotation/curl_v1_authoring_scope.v1.json`

SHA-256:

`d8e020cc14bd6c8ea9d679ba0f736bdce6098763d9b8ac0c0f95edaf8d9fd9c7`

It was frozen in commit:

`9b3a33a358cd9cd0d4837b7221426d2e96d42239`

Decision 0021 is:

`documentation/decisions/0021-curl-v1-source-only-authoring-scope-freeze.md`

SHA-256:

`9ef22ab551184808d3185c95d7286ab3c296bf6d9c29736c0312b84df78f18eb`

The V1 scope is not edited in place.

## Why a V2 scope successor is required

Source-only reconciliation against pinned curl revision:

`68720b4837284335b2d63cb358f8f6ce65f5bc55`

identified protocol-state semantics that cannot be represented faithfully by
the frozen V1 scope without a semantic successor.

First, the official global-initialization documentation requires libcurl
global initialization before ordinary libcurl calls, while `curl_easy_init()`
is a documented automatic-initialization exception and `curl_multi_init()`
does not itself provide that exception. Therefore actual runtime readiness
must be distinguished from the explicit `curl_global_init()` cleanup
obligation.

Second, after `curl_multi_perform()` returns a non-`CURLM_OK` error, the
official documentation states that the state of the transfers is uncertain
and ordinary continuation must not simply repeat the same operation without
the documented remove/re-add recovery discipline.

Third, V1 treated an unmatched extra `curl_global_cleanup()` as automatic D4
by call count. The pinned implementation returns without action at zero global
reference count, while an unmatched cleanup when an implicit runtime reference
exists can instead change runtime readiness. V2 therefore requires
state-sensitive handling and removes the unconditional call-count D4 rule.

Fourth, the broad remove -> easy-cleanup -> multi-cleanup sequence is described
using normative `should` wording. The author checkpoint does not silently
strengthen that entire sequence into an unconditional MUST violation.
Independent review must resolve MUST/MAY/recommendation strength where needed.

The pinned implementation also shows that removing an already detached easy
handle returns `CURLM_OK` as a no-op. Repeated remove is therefore not
automatically D4 merely by call count.

## V2 candidate

The exact immutable V2 scope-successor author checkpoint is:

`config/annotation/curl_v2_authoring_scope.v2.json`

SHA-256:

`f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df`

The API function set remains unchanged at 12 functions.

The pinned curl revision remains unchanged.

The frozen scenario manifest remains unchanged:

`config/generation/scenario_bindings.80.v10.json`

SHA-256:

`a7ab361e6e2d41d9051e48bc7626f0be37c1df9ec35f788a9a019b010054a2db`

The approved source-evidence set remains unchanged at 21 pinned files.

## V2 semantic changes

V2 introduces author-side candidate semantics for:

1. process-wide runtime readiness;
2. separate explicit-global cleanup responsibility;
3. the `curl_multi_perform()` post-error condition;
4. state-sensitive `curl_global_cleanup()` classification;
5. repeated detached `curl_multi_remove_handle()` no-op behavior; and
6. explicit human review of cleanup-order normative strength.

No new API function is added.

No synthetic protocol event is introduced.

## Review boundary

This Decision does **not** freeze the V2 scope and does **not** authorize
technical curl working-draft authoring.

`Spec-Reviewer-1` must independently review the exact immutable V2 scope
candidate using only the approved pinned source evidence, the exact V1
predecessor, Decisions 0021 and 0022, and the frozen scenario manifest.

The reviewer must explicitly decide the normative strength of the identified
MUST/MAY-sensitive rules.

Generated fuzz-driver source, selected-sample membership, raw model responses,
generated compiler semantic contents, gold labels, analyzer output, baseline
output, controlled LLM-review output, repair output, corpus prevalence, and
performance feedback remain prohibited as specification evidence.

If the reviewer requests any semantic modification, this V2 author checkpoint
must remain immutable and a V3 successor must be created.

Only exact human approval of this V2 scope may authorize its scope freeze and
subsequent source-only technical working-draft authoring.
