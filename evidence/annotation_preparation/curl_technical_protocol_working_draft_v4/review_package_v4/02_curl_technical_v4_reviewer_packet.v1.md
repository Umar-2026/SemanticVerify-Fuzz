# curl Technical Protocol Working Draft V4 — Independent Human Review Packet

## Purpose

This packet is for independent human technical review of exact immutable
curl Technical Protocol Working Draft V4.

Working Draft V3 received overall decision `REVISION_REQUIRED`.

V4 is a metadata-only immutable successor addressing V3-RR02 and V3-RR12.
Accepted V3 protocol-rule semantics must remain unchanged.

No canonicalization may occur unless exact V4 receives the required independent
human approval and a later separate canonicalization authorization.

## Exact review target

Working draft:

`03_curl_technical_protocol_working_draft.v4.json`

SHA-256:

`e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8`

Size:

`41033` bytes

Author checkpoint commit:

`b98d76536376b21fc6f2e85a060e960e1681453c`

Author checkpoint tree:

`e7243cda2f8afd9b6cceff793ab0cfa723fabbe5`

## Evidence boundary

Permitted evidence:

* exact V4;
* exact immutable V3 predecessor;
* completed V3 independent human review;
* Decisions 0034, 0035, and 0036;
* V4 successor authorization;
* V4 author-resolution record;
* V4 metadata-successor traceability;
* V4 author-checkpoint record;
* frozen source-only scope;
* exactly 21 approved pinned curl source files;
* minimal V4 author-checkpoint Git witness;
* the self-contained V4 package verifier.

Not permitted:

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

For every V4-RR item enter exactly one:

`PASS`

`REVISION_REQUIRED`

`FAIL`

If revision is required, state the precise required change.

---

### V4-RR01 — Exact V4 identity, author checkpoint, and immutable V3 predecessor

Decision:

Notes:

Confirm exact V4 SHA-256, size, author-checkpoint commit/tree, V4 Git blob,
Decision 0036 Git blob, exact V3 predecessor SHA, and that V3 was not edited
in place.

---

### V4-RR02 — Correct V4 purpose and working-draft version metadata

Decision:

Notes:

Confirm V4 identifies itself as Working Draft V4, describes exact V3 as its
immediate immutable predecessor, identifies the metadata-only successor
boundary, and no longer describes V2 as the operative successor.

---

### V4-RR03 — Exact V3 predecessor and completed-V3-review bindings

Decision:

Notes:

Confirm governance and successor-resolution metadata bind exact V3 path,
SHA-256, size, completed V3 human-review SHA/commit/tree, and overall
`REVISION_REQUIRED` decision.

---

### V4-RR04 — Removal of stale operative V1/V2 successor metadata

Decision:

Notes:

Confirm operative V4 purpose, governance, successor-resolution metadata, and
version-specific non-claims contain no stale V1/V2 successor binding,
including the former V1 predecessor path/review SHA/authorization commit and
`v1_in_place_edit_authorized` field.

Historical provenance outside the operative successor metadata may remain.

---

### V4-RR05 — Preservation of accepted V3 protocol semantics

Decision:

Notes:

Confirm all ten protocol-semantic containers are identical in JSON semantics
between packaged V3 and V4:

* api_surface;
* resources;
* return_condition_policy;
* verdict_semantics;
* defect_taxonomy;
* global_runtime_rules;
* easy_handle_rules;
* multi_handle_rules;
* cross_resource_rules;
* exit_obligations.

No protocol-semantic correction is authorized in V4.

---

### V4-RR06 — Rule counts, API surface, and four-verdict contract

Decision:

Notes:

Confirm easy-handle rule count remains 21, multi-handle rule count remains 29,
no protocol rule was added or removed, the frozen twelve-function curl surface
is preserved, and machine verdicts remain exactly:

`VALID`

`VIOLATION-MUST`

`VIOLATION-MAY`

`UNKNOWN`

---

### V4-RR07 — Frozen scope and approved source evidence

Decision:

Notes:

Confirm frozen V3 source-only scope remains unchanged, pinned curl revision and
tree remain unchanged, evidence class remains `PREAPPROVED_SOURCE_ONLY`, and
exactly the same 21 approved source files and hashes are supplied.

---

### V4-RR08 — V4 author-resolution, traceability, and checkpoint consistency

Decision:

Notes:

Confirm V4-C01 through V4-C06 are correctly represented and bound to
V3-RR02/V3-RR12, V3 PASS subjects are preserved, exact V4 SHA is bound by
traceability/checkpoint records, and no unauthorized protocol change appears.

---

### V4-RR09 — Platform-independent review-package path verification

Decision:

Notes:

Review `18_verify_review_package.v4.py`.

Confirm source-path comparison canonicalizes logical relative paths to
forward-slash POSIX form before comparison, accepts equivalent Windows
backslash representations after normalization, joins logical path components
to the local filesystem safely, and does not alter source hashes or evidence
semantics.

This item addresses V4-P01.

---

### V4-RR10 — Evidence quarantine and prohibited evidence

Decision:

Notes:

Confirm no generated-driver source, selected-sample membership, raw model
response, generated-driver compiler-log semantic content, gold label, analyzer
output, baseline output, LLM-review output, or repair output is present or used
as V4 review evidence.

---

### V4-RR11 — V4-specific non-claims and non-authorizations

Decision:

Notes:

Confirm V4-specific non-claims correctly state that V4 is not canonical and
has not yet received independent approval. Confirm canonical curl.json,
generated-driver inspection, selected-sample inspection, gold annotation,
analyzer implementation/execution, baseline execution, and repair remain
unauthorized.

---

### V4-RR12 — Overall technical adequacy for later canonicalization authorization

Decision:

Notes:

Considering the exact V4 metadata corrections, complete preservation of accepted
V3 protocol semantics, source-only evidence boundary, successor-bound
traceability, and platform-independent package verification, determine whether
exact V4 is technically adequate to proceed to a later separate
canonicalization authorization.

If not, identify the precise required successor correction.

---

## Overall technical review decision

Choose exactly one:

`APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION`

`REVISION_REQUIRED`

`FAIL`

Overall decision:

Notes:

## Reviewer identity

Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

## Post-review rule

No assistant-generated or synthetic human approval is permitted.

If revision is required, exact V4 must remain immutable and a new successor
must be created rather than editing V4 in place.

If approval is granted, exact V4 must remain immutable and canonicalization
still requires a separate explicit authorization and operation.
