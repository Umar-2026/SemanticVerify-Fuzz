# curl Mapping Contract V4 — Independent Human Technical Review

## Exact target

V4 SHA-256:

`9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070`

Size:

`26601`

Author checkpoint commit:

`390acaac338c1259dc67632d42db137707366e36`

Author checkpoint tree:

`f426da2294cda67aa89d5e062245d64ce2eb3a48`

Internal review target:

`Exact immutable V4 corrective schema-insufficiency proof.`

Author outcome:

`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`

This remains an author conclusion pending independent review.

For every item use exactly:

`PASS`

`REVISION_REQUIRED`

`FAIL`

### V4-RR01 — Portable original Git-object binding

Decision:

Notes:

Run:

`17_git_object_proof/07_verify_git_object_proof.v1.py`

Independently verify the checkpoint commit object ID, root-tree binding,
`config/annotation` path, exact V4 blob object ID, V4 SHA-256, and V4 size.

Confirm the evidence is independently portable without requiring unrelated
repository blob contents.

### V4-RR02 — Correct successor and predecessor immutability

Decision:

Notes:

Confirm exact V3 remains immutable with overall human decision
REVISION_REQUIRED and only V3-RR10 requiring correction.

Confirm exact V4 is a separately authorized corrective successor rather than
an in-place rewrite of V3.

### V4-RR03 — Exact V3-RR10 review-target correction

Decision:

Notes:

Confirm exact V3 contained the stale value:

`Exact immutable V2 schema-insufficiency proof.`

Confirm exact V4 contains at:

`$.independent_review_requirement.review_target`

exactly:

`Exact immutable V4 corrective schema-insufficiency proof.`

Confirm the current artifact therefore unambiguously identifies itself as the
independent review target.

### V4-RR04 — Preservation of V3 substantive proof semantics

Decision:

Notes:

Confirm V4 preserves the substantive V3 frozen-schema insufficiency proof
without semantic weakening or strengthening.

Confirm structural proof content outside authorized successor/governance
metadata remains unchanged.

### V4-RR05 — Complete V4 representation-policy correction retained

Decision:

Notes:

Confirm the complete exact approved 10-field curl V4 representation-policy
binding remains preserved.

Confirm ownership-sensitive and return-sensitive preservation remain explicit.

### V4-RR06 — Complete retained losslessness boundary

Decision:

Notes:

Confirm membership sensitivity, ownership sensitivity, return sensitivity,
path sensitivity, set-valued reasoning, first-class UNKNOWN, four-verdict
semantics, forward accounting, reverse accounting, all 10 semantic
containers, 64 rule records, and 3 exit obligations remain required.

Confirm no required semantic class is silently dropped.

### V4-RR07 — Structural obstruction and admissibility preservation

Decision:

Notes:

Confirm all four retained structural obstruction witnesses, frozen inventory,
frozen-schema structural facts, admissibility constraints, candidate carrier
classifications, and scoped proof conclusion remain preserved.

### V4-RR08 — Corrected frozen-schema insufficiency conclusion

Decision:

Notes:

Under the exact corrected V4 governance and complete losslessness boundary,
determine whether the scoped conclusion remains supported:

`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`

This is not a claim that every theoretically imaginable arbitrary encoding is
mathematically impossible.

### V4-RR09 — No unauthorized semantic, schema, or materialization action

Decision:

Notes:

Confirm V4 does not add/remove/change protocol rules, invent semantic protocol
events, use opaque payload packing, modify the frozen canonical schema,
approve a positive mapping, or create `curl.json`.

### V4-RR10 — Governance consequence and next boundary

Decision:

Notes:

Confirm approval of exact V4 would establish only the independently reviewed
technical need for a separately governed canonical-schema-successor process.

Confirm V4 itself does not authorize schema-successor authoring, schema
modification, `curl.json`, analyzer implementation/execution, baseline
execution, or repair.

Confirm exact V4 must remain immutable after review.

## Overall technical review decision

Choose exactly one:

`APPROVE_V4_RR10_CORRECTED_SCHEMA_INSUFFICIENCY_PROOF`

`REVISION_REQUIRED`

`FAIL`

Overall decision:

Notes:

## Reviewer identity

Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

## Evidence quarantine

Do not use generated-driver source, selected-sample membership, raw model
responses, generated-driver compiler-log semantic content, gold labels,
analyzer output, baseline output, LLM-review output, or repair output.

## Post-review rule

No synthetic or assistant-generated human approval is permitted.

Exact V4 remains immutable after its author checkpoint.

Approval of this proof does not authorize a canonical-schema successor or
`curl.json`.
