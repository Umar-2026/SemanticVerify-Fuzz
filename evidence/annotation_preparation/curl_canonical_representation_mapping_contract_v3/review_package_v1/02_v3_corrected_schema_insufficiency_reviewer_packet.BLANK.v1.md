# curl Mapping Contract V3 — Independent Human Technical Review

## Exact target

V3 SHA-256:

`ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97`

Size:

`24750`

Author checkpoint commit:

`eeffef65a0ab2c9982e0cb708376635b096fec07`

Author checkpoint tree:

`de149c84681855ca1b00f306df4f04cc6debe4d3`

Author outcome:

`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`

This remains an author conclusion pending independent review.

For every item use exactly:

`PASS`

`REVISION_REQUIRED`

`FAIL`

### V3-RR01 — Portable original Git-object binding

Decision:

Notes:

Run `17_git_object_proof/07_verify_git_object_proof.v1.py`.

Independently confirm the original checkpoint commit object ID, its declared
root tree, the tree path `config/annotation`, the exact V3 blob object ID,
V3 SHA-256, and V3 size.

Confirm the evidence is sufficient to resolve the predecessor RR01 portability
problem without requiring access to unrelated repository blob contents.

### V3-RR02 — Correct successor and predecessor immutability

Decision:

Notes:

Confirm exact V2 remains immutable, its human decision remains
REVISION_REQUIRED, and V3 is a separately authorized corrective successor.

Confirm the V2 RR01 human decision has not been retroactively rewritten.

### V3-RR03 — Complete exact V4 representation-policy binding

Decision:

Notes:

Confirm V3 binds the complete exact 10-field V4 `representation_policy`.

Confirm canonical semantic SHA-256:

`dd645ad929e40bcfa2af2353817d55ad76596f464991f2417c4ac1b57c0be408`

Confirm every field has exact-value accounting and preservation_required=true.

### V3-RR04 — Ownership-sensitive preservation

Decision:

Notes:

Confirm `ownership_sensitive_semantics_preserved=true` is explicitly inside
the formal required losslessness contract.

Confirm this closes the ownership-related V2-RR08 omission.

### V3-RR05 — Return-sensitive preservation

Decision:

Notes:

Confirm `return_sensitive_semantics_preserved=true` is explicitly inside the
formal required losslessness contract.

Confirm this closes the return-related V2-RR08 omission.

### V3-RR06 — Complete retained semantic-accounting boundary

Decision:

Notes:

Confirm V3 also retains membership sensitivity, path sensitivity,
set-valued-state reasoning, first-class UNKNOWN, four-verdict semantics,
forward accounting, reverse accounting, all 10 V4 semantic containers,
64 rule records, and 3 exit obligations.

Confirm no required semantic class is silently dropped.

### V3-RR07 — Preservation of valid V2 proof evidence

Decision:

Notes:

Confirm V3 preserves the V2 frozen inventory, frozen-schema structural facts,
four structural obstruction witnesses, admissibility constraints, considered
carrier classes, and scoped proof conclusion without semantic weakening or
strengthening.

### V3-RR08 — Corrected frozen-schema insufficiency conclusion

Decision:

Notes:

Under the corrected complete losslessness boundary, determine whether the
scoped conclusion remains supported:

`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`

Do not interpret this as a claim that every theoretically imaginable arbitrary
encoding is mathematically impossible.

### V3-RR09 — No unauthorized semantic or schema action

Decision:

Notes:

Confirm V3 does not add/remove/change protocol rules, invent semantic protocol
events, use opaque payload packing, modify the frozen schema, define an
approved positive mapping, or create `curl.json`.

### V3-RR10 — Governance consequence

Decision:

Notes:

Confirm approval of V3 would establish only an independently reviewed
technical need for a separately governed canonical-schema-successor process.

Confirm V3 itself does not authorize schema-successor authoring, analyzer
implementation/execution, baseline execution, or repair.

Confirm exact V3 must remain immutable after review.

## Overall technical review decision

Choose exactly one:

`APPROVE_V3_CORRECTED_SCHEMA_INSUFFICIENCY_PROOF`

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
responses, compiler-log semantic contents, gold labels, analyzer output,
baseline output, LLM-review output, or repair output.

## Post-review rule

No synthetic or assistant-generated human approval is permitted.

Exact V3 remains immutable.

Approval does not authorize a schema successor or `curl.json`.
