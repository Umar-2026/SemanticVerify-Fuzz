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

`03_curl_technical_protocol_working_draft.v1.json`

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

- exact Working Draft V1;
- exact frozen V3 source-only scope;
- Decision 0026 and Decision 0027;
- source-evidence map and author notes;
- the 21 previously approved pinned curl source files;
- minimal Git object witness.

Not permitted as technical-specification evidence:

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

A `PASS` means the exact current draft treatment is acceptable.

If `REVISION_REQUIRED`, describe the precise required semantic change.

Do not edit the immutable review-package copies.

---

### TS-RR01 — Exact author-checkpoint identity and immutability

Decision:

Notes:

Confirm that:

- exact Working Draft V1 SHA-256 is correct;
- author commit and tree are independently resolvable using the supplied
  minimal Git witness;
- the target path resolves to the exact draft blob;
- Decision 0027 is bound to the same author checkpoint;
- the review target has not been silently edited in place.

---

### TS-RR02 — Frozen V3 scope compliance and twelve-function surface

Decision:

Notes:

Review whether the working draft remains within the frozen twelve-function
surface and preserves the frozen V3 semantic guardrails without inventing
additional protocol events.

---

### TS-RR03 — Global runtime readiness versus explicit cleanup obligation

Decision:

Notes:

Review the separation between:

- actual runtime readiness;
- explicit `curl_global_init` cleanup obligation;
- implicit readiness established by successful `curl_easy_init`;
- failed explicit initialization;
- reference-sensitive `curl_global_cleanup`.

Confirm that implicit readiness is not silently treated as the same explicit
cleanup obligation.

---

### TS-RR04 — Easy-handle lifecycle

Decision:

Notes:

Review:

- non-NULL `curl_easy_init` resource creation;
- `curl_easy_setopt`;
- detached `curl_easy_perform`;
- repeated easy-perform use;
- `curl_easy_reset`;
- detached cleanup;
- use-after-cleanup;
- exit cleanup obligation.

---

### TS-RR05 — Multi-handle membership and ownership

Decision:

Notes:

Review:

- `curl_multi_init`;
- add/remove membership;
- duplicate add;
- repeated remove;
- easy ownership remaining with caller;
- prohibition on easy-perform while attached;
- easy cleanup requiring detachment;
- multi cleanup not discharging easy cleanup obligations.

---

### TS-RR06 — `curl_multi_perform` return-conditioned state

Decision:

Notes:

Review whether:

- `CURLM_OK` preserves normal multi ownership;
- non-`CURLM_OK` establishes
  `MULTI_OWNED_POST_ERROR_UNCERTAIN`;
- recovery/removal/cleanup behavior is represented conservatively;
- plain repetition after error is not silently declared valid.

---

### TS-RR07 — Verdict semantics and uncertainty discipline

Decision:

Notes:

Review the meanings and separation of:

- `VALID`;
- `VIOLATION-MUST`;
- `VIOLATION-MAY`;
- `UNKNOWN`.

Confirm that `VIOLATION-MAY` is used for feasible path/state uncertainty and
is not used as a substitute for unresolved normative strength.

Confirm that `UNKNOWN` is first-class and is never silently converted to
`VALID`.

---

### TS-RR08 — Exit obligations and defect-taxonomy mapping

Decision:

Notes:

Review D1-D8 mappings and the exit obligations for:

- easy handles;
- multi handles;
- explicit global cleanup.

Identify any rule whose defect class or MUST-status is not justified.

---

### TS-RR09 — NR01: explicit global cleanup at exit

Decision:

Notes:

Review the current treatment:

`UNKNOWN_PENDING_NR01`

for an outstanding explicit global-cleanup obligation at exit.

State whether the exact current treatment is acceptable or whether it should
be changed to a specific enforceable classification.

---

### TS-RR10 — NR02: multi cleanup with attached easy handles

Decision:

Notes:

Review the current treatment where the pinned implementation structurally
detaches remaining caller-owned easy handles but documentation describes an
ordered remove → easy-cleanup → multi-cleanup sequence.

State whether current `UNKNOWN` treatment is acceptable or requires a precise
MUST/MAY/recommendation classification.

---

### TS-RR11 — NR03: plain multi-perform repetition after error

Decision:

Notes:

Review the current `UNKNOWN` treatment after a non-`CURLM_OK`
`curl_multi_perform` when the program plainly repeats `curl_multi_perform`
without documented recovery.

State whether the current treatment is acceptable or should become a specific
enforceable violation class.

---

### TS-RR12 — NR04: `curl_easy_init(NULL-result)` runtime post-state

Decision:

Notes:

Review the set-valued runtime post-state when `curl_easy_init` is invoked from
an uninitialized runtime and returns `NULL`.

The implementation permits failure before successful implicit global init or
after successful implicit initialization during `Curl_open`.

Confirm whether dependent reasoning should remain `UNKNOWN` when the exact
post-state cannot be established.

---

### TS-RR13 — NR05: removing an easy handle through the wrong multi

Decision:

Notes:

Review whether the current `UNKNOWN` protocol classification for a
wrong-multi `curl_multi_remove_handle` should remain conservative or should
be mapped to a specific D6/D7 enforceable violation.

---

### TS-RR14 — NR06: global cleanup while live resources remain

Decision:

Notes:

Review the state-sensitive treatment of `curl_global_cleanup` that removes
runtime readiness while live libcurl resources remain.

Confirm whether the draft appropriately avoids classifying this solely by
cleanup call count.

---

### TS-RR15 — Source traceability and quarantine

Decision:

Notes:

Confirm that:

- all important technical rules are traceable to the frozen V3 scope and/or
  approved pinned source evidence;
- the package contains exactly the approved source-evidence class;
- no prohibited generated-driver, gold, analyzer, baseline, LLM-review, or
  repair evidence is used;
- unresolved normative issues are exposed rather than hidden.

---

## Overall technical review decision

Choose exactly one:

`APPROVE_EXACT_WORKING_DRAFT_V1_FOR_CANONICALIZATION`

`REVISION_REQUIRED`

`FAIL`

Overall decision:

Notes:

An approval here authorizes only a **subsequent separate canonicalization
operation** for the exact approved Working Draft V1.

It does not itself create or authorize use of canonical `curl.json`.

Generated-driver inspection, gold annotation, analyzer implementation,
baseline execution, and repair remain separately governed and unauthorized
at this boundary.

## Reviewer identity

Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

## Post-review rule

No assistant-generated or synthetic human approval is permitted.

If revision is required, the exact V1 author checkpoint must remain immutable;
create an immutable successor rather than editing V1 in place.
