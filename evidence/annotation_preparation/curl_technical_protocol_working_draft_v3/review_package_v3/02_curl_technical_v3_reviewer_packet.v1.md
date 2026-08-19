# curl Technical Protocol Working Draft V3 — Independent Human Review Packet

## Purpose

This packet is for an independent human technical-specification review of the
exact immutable curl Technical Protocol Working Draft V3 author checkpoint.

Working Draft V2 received an overall independent human-review decision of
`REVISION_REQUIRED`.

V3 is a new immutable successor implementing only the bounded corrections
authorized from V2-RR05, V2-RR06, V2-RR09, V2-RR10, and V2-RR12.

No canonicalization may occur unless this exact V3 later receives the required
human approval and a separate canonicalization authorization.

## Exact review target

Working draft:

`03_curl_technical_protocol_working_draft.v3.json`

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

- exact Working Draft V3;
- exact immutable Working Draft V2 predecessor;
- completed V2 independent human technical review;
- V3 successor authorization;
- Decision 0031, Decision 0032, and Decision 0033;
- exact V3 author-resolution record;
- exact V3 author-checkpoint record;
- exact V3 successor-bound rule-to-source traceability record;
- frozen V3 source-only scope;
- exactly the same 21 approved pinned curl source files;
- minimal V3 author-checkpoint Git witness.

Not permitted as V3 technical-review evidence:

- generated drivers;
- selected-sample membership;
- raw model responses;
- generated-driver compiler-log semantic content;
- gold labels;
- analyzer output;
- baseline output;
- LLM-review output;
- repair output.

## Decision choices

For every review item choose exactly one:

`PASS`

`REVISION_REQUIRED`

`FAIL`

A `PASS` means the exact V3 treatment of that item is technically acceptable.

If `REVISION_REQUIRED`, state the precise semantic change required.

Do not edit the immutable review-package copy. Complete only an external
editable reviewer-response copy prepared from this packet.

---

### V3-RR01 — Exact V3 author-checkpoint identity and immutability

Decision:

Notes:

Confirm:

- exact V3 SHA-256 and size;
- author-checkpoint commit and tree;
- V3 target Git blob;
- Decision 0033 Git blob;
- immutable V2 predecessor binding;
- V2 was not edited in place;
- exact V3 package target is the author-checkpoint artifact.

---

### V3-RR02 — Frozen scope and bounded-successor boundary

Decision:

Notes:

Confirm:

- exactly the frozen twelve curl functions remain in scope;
- pinned curl revision and tree are unchanged;
- frozen V3 source-only scope is unchanged;
- V3 semantic changes are limited to the authorized V2 revision-required items;
- no generated-driver-derived rule was introduced;
- no new evidence class was introduced.

---

### V3-RR03 — Preserved return-conditioned multi cleanup semantics

Decision:

Notes:

Review whether V3 preserves the accepted V2 treatment that:

- only `curl_multi_cleanup == CURLM_OK` establishes `MULTI_RELEASED`;
- only successful cleanup discharges the multi cleanup obligation;
- only successful cleanup establishes complete structural detachment;
- non-`CURLM_OK` cleanup does not assert release;
- non-`CURLM_OK` cleanup preserves the cleanup obligation;
- unresolved membership after failed cleanup remains conservative;
- the same treatment applies from the post-error multi state.

---

### V3-RR04 — Exact four-verdict machine contract

Decision:

Notes:

Confirm that all machine-readable verdict fields use only:

`VALID`

`VIOLATION-MUST`

`VIOLATION-MAY`

`UNKNOWN`

Confirm that review state, provenance, qualifiers, and explanatory information
remain separate and do not create undeclared machine verdict variants.

---

### V3-RR05 — D1/D2 dual-resource coverage and cleanup-specific cases

Decision:

Notes:

Review the V3 treatment of `curl_multi_add_handle` and
`curl_multi_remove_handle`.

Confirm that:

- M26 and M27 explicitly classify the easy argument used before successful
  `curl_easy_init` acquisition as D1 `VIOLATION-MUST`;
- M28 and M29 explicitly classify a NULL failed-`curl_easy_init` result as
  D2 `VIOLATION-MUST`;
- when the supplied multi has passed its live-valid check, the pinned invalid
  easy result is `CURLM_BAD_EASY_HANDLE`;
- these invalid-easy cases create/detach/change no membership;
- easy-argument D1/D2 classification is independent of supplied-multi
  D1/D2/D3 classification;
- invalid supplied-multi cases may determine the earlier pinned return;
- definite D2 failed-easy use is not weakened merely because the failed
  `curl_easy_init` runtime post-state is set-valued;
- cleanup-specific D4 precedence remains intact;
- `curl_easy_cleanup(NULL)` remains the documented no-op exception;
- `curl_multi_cleanup(NULL)` retains its return-conditioned no-release behavior.

---

### V3-RR06 — Explicit global cleanup obligation at exit

Decision:

Notes:

Confirm that:

- successful explicit `curl_global_init` establishes
  `EXPLICIT_CLEANUP_DUE`;
- implicit readiness alone does not establish that explicit obligation;
- exit with an outstanding explicit cleanup obligation is D5;
- enforcement is `MUST`;
- verdict is `VIOLATION-MUST`;
- the V3 resource metadata no longer contains the stale
  `REVIEW_REQUIRED_MUST_OR_MAY` normative status;
- the operative missing-at-exit normative status is consistent with the
  resolved D5 `MUST` classification.

---

### V3-RR07 — Preserved multi-cleanup ordering recommendation

Decision:

Notes:

Review whether V3 preserves the accepted treatment that:

- `remove → easy cleanup → multi cleanup` is a documented recommendation;
- it is not an unconditional MUST violation;
- successful multi cleanup with caller-owned easy handles still attached is
  not a violation solely because explicit remove was skipped;
- successful multi cleanup structurally detaches remaining easy handles;
- individual easy cleanup obligations remain outstanding.

---

### V3-RR08 — Preserved post-error multi-perform and recovery semantics

Decision:

Notes:

Confirm that:

- plain `curl_multi_perform` repetition after non-`CURLM_OK` without complete
  recovery remains D6 `VIOLATION-MUST`;
- the multi remains in the post-error uncertain state after prohibited repeat;
- removal remains available;
- cleanup remains available subject to return-conditioned cleanup;
- recovery requires complete removal of error-time handles followed by
  successful re-add before normal multi-perform resumes;
- partial recovery does not silently clear post-error uncertainty.

---

### V3-RR09 — Resolved E04 set-valued NULL easy-init semantics

Decision:

Notes:

Confirm that operative E04 now:

- uses resolved source-grounded enforcement rather than
  `IMPLEMENTATION_DERIVED_REVIEW_REQUIRED`;
- no longer carries an operative pending `review_item: NR04`;
- preserves exactly the feasible post-states:
  `RUNTIME_UNINITIALIZED` and `RUNTIME_READY_IMPLICIT_ONLY`;
- creates no easy resource on NULL;
- creates no explicit global-cleanup obligation on either failure branch;
- does not force `UNKNOWN` merely because the runtime state is set-valued;
- uses the common verdict when every feasible state agrees;
- joins mixed VALID/enforceable-violation outcomes to `VIOLATION-MAY`;
- reserves `UNKNOWN` for normative/evidence/model uncertainty;
- preserves definite D2 failed-easy use across both feasible runtime states.

Historical resolved NR04 provenance may remain outside the operative E04 rule.

---

### V3-RR10 — Valid repeated removal and wrong-multi removal

Decision:

Notes:

Confirm that:

- M10 applies only with a live valid supplied multi and a live already-detached
  easy handle;
- only that valid repeated-remove case returns `CURLM_OK`, changes no
  membership, and is `VALID`;
- M11 applies only with a live valid supplied multi and a live easy handle
  attached to a different original multi;
- M11 remains D7 `VIOLATION-MUST`;
- M11 returns `CURLM_BAD_EASY_HANDLE`;
- rejected wrong-multi removal preserves the actual original membership;
- absent, NULL, or released supplied-multi cases are classified by applicable
  D1/D2/D3 rules before membership comparison;
- valid repeated removal remains distinct from wrong-multi removal.

---

### V3-RR11 — Preserved final-reference global cleanup with live resources

Decision:

Notes:

Confirm that V3 preserves the accepted state-sensitive treatment:

- final-reference `curl_global_cleanup` with a live modeled easy or multi
  resource is D8 `VIOLATION-MUST`;
- the actual runtime transition to uninitialized still occurs;
- cleanup leaving another runtime reference ready is distinct;
- cleanup after modeled resources have completed is distinct;
- a zero-reference no-op is not automatically D4;
- classification is state/reference-sensitive rather than based only on
  global init/cleanup call counts.

---

### V3-RR12 — V3-bound traceability, quarantine, and overall adequacy

Decision:

Notes:

Confirm:

- the exact V3 SHA is bound by the successor traceability record;
- corrected V3 subjects are mapped to frozen V3 and/or unchanged approved
  pinned source evidence;
- exactly the approved `PREAPPROVED_SOURCE_ONLY` evidence class is used;
- exactly the same 21 approved pinned curl source files are supplied;
- no generated-driver, selected-sample, raw-model-response, compiler-log
  semantic, gold, analyzer, baseline, LLM-review, or repair evidence is used;
- V3 contains no semantic change outside the authorized bounded corrections;
- the seven V2 PASS-review subjects remain preserved;
- the exact V3 is technically adequate for a later separate canonicalization
  authorization, or identify any required successor correction.

---

## Overall technical review decision

Choose exactly one:

`APPROVE_EXACT_WORKING_DRAFT_V3_FOR_CANONICALIZATION`

`REVISION_REQUIRED`

`FAIL`

Overall decision:

Notes:

Approval means only that the exact immutable V3 may proceed to a separate
canonicalization authorization/operation.

Approval does not itself create or authorize canonical `curl.json`.

Generated-driver inspection, selected-sample inspection, gold annotation,
analyzer implementation/execution, baseline execution, and repair remain
separately governed and unauthorized at this boundary.

## Reviewer identity

Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

## Post-review rule

No assistant-generated or synthetic human approval is permitted.

If revision is required, exact V3 must remain immutable and a new successor
must be created rather than editing V3 in place.

If approval is granted, exact V3 must remain immutable and canonicalization
still requires a separate explicit authorization and operation.
