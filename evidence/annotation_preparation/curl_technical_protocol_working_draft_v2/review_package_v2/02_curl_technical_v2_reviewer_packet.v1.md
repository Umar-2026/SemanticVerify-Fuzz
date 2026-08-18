# curl Technical Protocol Working Draft V2 — Independent Human Review Packet

## Purpose

This is an independent human technical-specification review of the exact
immutable curl Technical Protocol Working Draft V2 successor.

Working Draft V1 received an overall independent human-review decision of
`REVISION_REQUIRED`.

V2 is a new immutable successor and must be reviewed independently before any
separate canonicalization operation may be considered.

## Exact review target

Working draft:

`03_curl_technical_protocol_working_draft.v2.json`

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

- exact Working Draft V2;
- exact V2 author-resolution record;
- Decision 0029 and Decision 0030;
- exact completed V1 independent human technical review;
- frozen V3 source-only scope;
- source-evidence map;
- approved source-evidence manifest;
- the same 21 approved pinned curl source files;
- minimal V2 author-checkpoint Git witness.

Not permitted as V2 technical-review evidence:

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

A `PASS` means the exact V2 treatment of that item is technically acceptable.

If `REVISION_REQUIRED`, state the precise semantic change required.

Do not edit files under the immutable review-package copy. Complete only an
external editable reviewer-response copy prepared from this packet.

---

### V2-RR01 — Exact V2 author-checkpoint identity and immutability

Decision:

Notes:

Confirm:

- exact V2 SHA-256;
- author checkpoint commit and tree;
- V2 target Git blob;
- Decision 0030 Git blob;
- V1 remains immutable;
- no silent in-place modification occurred.

---

### V2-RR02 — Frozen scope and successor boundary

Decision:

Notes:

Confirm:

- exactly the frozen twelve curl functions remain in scope;
- pinned curl revision is unchanged;
- frozen V3 source-only scope is unchanged;
- no generated-driver-derived rule was introduced;
- V2 changes are bounded to the human-review successor corrections.

---

### V2-RR03 — TS-RR05/TS-RR06: return-conditioned multi cleanup

Decision:

Notes:

Review whether:

- only `curl_multi_cleanup == CURLM_OK` establishes `MULTI_RELEASED`;
- only successful cleanup discharges the multi cleanup obligation;
- only successful cleanup establishes complete structural detachment;
- non-`CURLM_OK` cleanup does not assert release;
- non-`CURLM_OK` cleanup preserves the cleanup obligation;
- unresolved membership after failed cleanup is represented conservatively;
- the same rules apply from the post-error multi state.

---

### V2-RR04 — TS-RR07: exact four-verdict contract

Decision:

Notes:

Confirm that machine-readable verdict fields use only:

- `VALID`
- `VIOLATION-MUST`
- `VIOLATION-MAY`
- `UNKNOWN`

Confirm that scoped, pending, explanatory, or review information is stored
separately and does not create undeclared verdict variants.

---

### V2-RR05 — TS-RR08: D1, D2, D4 and NULL cleanup cases

Decision:

Notes:

Review:

- explicit D1 rules before successful easy/multi acquisition;
- explicit D2 rules after failed/NULL acquisition;
- cleanup-specific D4 rules for repeated easy/multi cleanup after release;
- precedence of cleanup-specific D4 over generic D3 use-after-release;
- `curl_easy_cleanup(NULL)` no-op exception;
- `curl_multi_cleanup(NULL)` returning `CURLM_BAD_HANDLE`;
- NULL multi cleanup releasing nothing and discharging no obligation;
- failed multi cleanup not discharging the D5 exit obligation.

---

### V2-RR06 — TS-RR09: explicit global cleanup obligation at exit

Decision:

Notes:

Confirm that exit with `EXPLICIT_CLEANUP_DUE`, where the obligation arose from
successful explicit `curl_global_init`, is classified:

- defect `D5`;
- enforcement `MUST`;
- verdict `VIOLATION-MUST`.

Confirm implicit readiness alone does not create this explicit obligation.

---

### V2-RR07 — TS-RR10: multi cleanup ordering recommendation

Decision:

Notes:

Review whether the documented:

`remove → easy cleanup → multi cleanup`

sequence is represented as a non-enforceable recommendation rather than an
unconditional MUST.

Confirm successful multi cleanup with attached caller-owned easy handles is not
an enforceable violation solely because explicit remove was skipped.

Confirm individual easy cleanup obligations remain.

---

### V2-RR08 — TS-RR11: post-error multi-perform and recovery

Decision:

Notes:

Confirm:

- plain `curl_multi_perform` repetition after non-`CURLM_OK`, without complete
  documented recovery, is `D6 VIOLATION-MUST`;
- the multi remains in the post-error uncertain state after prohibited repeat;
- removal remains available;
- cleanup remains available subject to return-conditioned cleanup;
- recovery requires complete removal of error-time handles followed by
  successful re-add before normal multi-perform resumes;
- partial recovery does not silently clear post-error uncertainty.

---

### V2-RR09 — TS-RR12: set-valued NULL easy-init state and verdict joins

Decision:

Notes:

Confirm the source-grounded NULL `curl_easy_init` runtime post-state remains:

- `RUNTIME_UNINITIALIZED`, or
- `RUNTIME_READY_IMPLICIT_ONLY`.

Confirm:

- the state set itself does not automatically imply `UNKNOWN`;
- common verdicts across feasible states remain the common verdict;
- mixed VALID/enforceable-violation outcomes join to `VIOLATION-MAY`;
- unresolved normative strength or bounded-model uncertainty remains `UNKNOWN`;
- neither failure branch creates an explicit global-cleanup obligation.

---

### V2-RR10 — TS-RR13: wrong-multi removal

Decision:

Notes:

Review whether wrong-multi `curl_multi_remove_handle` is correctly represented
as:

- `D7`;
- `VIOLATION-MUST`;
- rejected with `CURLM_BAD_EASY_HANDLE`;
- actual easy-to-original-multi membership preserved.

Confirm this remains distinct from valid repeated removal of an already
detached easy handle.

---

### V2-RR11 — TS-RR14: final-reference global cleanup with live resources

Decision:

Notes:

Confirm that `curl_global_cleanup` is classified as state-sensitive
`D8 VIOLATION-MUST` only when it removes the final runtime reference while a
modeled easy or multi resource remains live.

Confirm:

- the actual runtime transition to uninitialized still occurs;
- cleanup leaving another runtime reference ready is distinct;
- cleanup after all modeled resources are finished is distinct;
- a zero-reference no-op is not automatically D4;
- classification is not based solely on global init/cleanup call count.

---

### V2-RR12 — Source traceability, quarantine, and overall V2 adequacy

Decision:

Notes:

Confirm:

- all important V2 rules remain traceable to frozen V3 and/or the same approved
  pinned source evidence;
- exactly the approved source-evidence class is used;
- no prohibited generated-driver, gold, analyzer, baseline, LLM-review, or
  repair evidence is used;
- V2 did not introduce a new semantic inconsistency while resolving the V1
  findings;
- the exact V2 is technically adequate, or identify any required successor
  correction.

---

## Overall technical review decision

Choose exactly one:

Overall decision:

Allowed values:

`APPROVE_EXACT_WORKING_DRAFT_V2_FOR_CANONICALIZATION`

`REVISION_REQUIRED`

`FAIL`

Notes:

Approval means only that the exact immutable V2 may proceed to a **separate
canonicalization authorization/operation**.

Approval does not itself create or authorize use of canonical `curl.json`.

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

If revision is required, exact V2 must remain immutable and a new successor
must be created rather than editing V2 in place.
