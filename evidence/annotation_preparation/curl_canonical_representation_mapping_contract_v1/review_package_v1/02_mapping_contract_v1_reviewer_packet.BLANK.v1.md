# curl Canonical Representation Mapping Contract V1 — Independent Human Review Packet

## Purpose

This packet is for independent human technical review of exact immutable:

`curl_canonical_representation_mapping_contract.v1.json`

The contract does **not** contain a positive V4-to-canonical mapping.

Its author conclusion is deliberately conservative:

`LOSSLESS_V4_TO_FROZEN_SCHEMA_MAPPING_PROVEN=NO`

`CANONICAL_MATERIALIZATION_SAFE=NO`

The reviewer must independently determine whether that conclusion is technically
correct.

Approval of this blocker contract does **not** authorize `curl.json`,
does **not** authorize a new canonical schema, and does **not** approve any
positive mapping algorithm.

## Exact review target

Package file:

`03_exact_mapping_contract.v1.json`

SHA-256:

`31d606f98f2c819291103ba7403214206ccde1d8e5e0e9103f0659c227622257`

Size:

`10879` bytes

Author checkpoint commit:

`afc2bb285f3b9adef8129f106c1c941b14d6f10c`

Author checkpoint tree:

`ace5a3cd3b2797c7a312403656391aa6da4908bb`

## Exact technical bindings

Approved curl V4 SHA-256:

`e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8`

Frozen canonical schema SHA-256:

`7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34`

## Decision choices

For every CMR-RR item enter exactly one:

`PASS`

`REVISION_REQUIRED`

`FAIL`

If revision is required, state the precise required successor correction.

---

### CMR-RR01 — Exact contract, approved V4, schema, and authorization bindings

Decision:

Notes:

Confirm the exact mapping-contract SHA/size, author checkpoint commit/tree,
approved V4 SHA/size, frozen schema SHA, and canonicalization-authorization
binding.

---

### CMR-RR02 — Corrected zlib/libpcap pre-freeze candidate precedent

Decision:

Notes:

Using the packaged zlib and libpcap source/finalization/canonical artifacts,
confirm that each reference library already had a canonical-shaped candidate
before freeze.

Confirm finalization did not reconstruct states/events/transitions and did not
semantically rewrite obligations.

Confirm canonical completion added only the field names `freeze_date` and
`content_sha256` at the required top-level and obligation-level locations.

---

### CMR-RR03 — Absence of a reference-style canonical candidate in exact curl V4

Decision:

Notes:

Confirm exact V4 contains no 15-field reference-style pre-freeze canonical
candidate and no `candidate_specification_fields` object equivalent to the
zlib/libpcap precedent.

---

### CMR-RR04 — Accounting for all ten approved V4 semantic containers

Decision:

Notes:

Confirm the contract binds all ten approved V4 protocol-semantic containers:

- api_surface
- resources
- return_condition_policy
- verdict_semantics
- defect_taxonomy
- global_runtime_rules
- easy_handle_rules
- multi_handle_rules
- cross_resource_rules
- exit_obligations

Confirm their contract hashes agree with exact approved V4.

---

### CMR-RR05 — Frozen rule and exit-obligation inventory

Decision:

Notes:

Confirm exact V4 contains:

- 10 global-runtime rules;
- 21 easy-handle rules;
- 29 multi-handle rules;
- 4 cross-resource rules;
- 64 total rule records;
- 3 exit obligations.

Confirm the blocker contract does not add, remove, or semantically modify any
of those rules.

---

### CMR-RR06 — Canonical FSM/provenance records are not already present

Decision:

Notes:

Confirm exact V4 contains no canonical event records, transition records,
pre-freeze canonical obligation records, or canonical provenance records.

Confirm canonical top-level `states`, `initial_state`, `events`,
`transitions`, `obligations`, `permitted_exit_states`, and `provenance`
arrays/fields are absent.

---

### CMR-RR07 — Existing authorization does not permit unreviewed reconstruction

Decision:

Notes:

Confirm the current authorization permits canonical metadata transformation
but does not authorize:

- protocol-rule semantic change;
- protocol-rule addition;
- protocol-rule removal;
- API-surface change;
- defect-taxonomy change;
- machine-verdict-contract change;
- source-evidence change;
- new evidence classes;
- synthetic protocol events.

Determine whether constructing a new state/event/transition/obligation
projection without a reviewed mapping would exceed that boundary.

---

### CMR-RR08 — Current lossless mapping classification

Decision:

Notes:

Determine whether the current evidence supports:

`LOSSLESS_V4_TO_FROZEN_SCHEMA_MAPPING_PROVEN=NO`

and:

`CANONICAL_MATERIALIZATION_SAFE=NO`

If not, identify the exact deterministic mapping already supported by the
reviewed evidence and explain why it introduces no new representational
decision.

---

### CMR-RR09 — curl.json materialization boundary

Decision:

Notes:

Confirm `curl.json` must remain uncreated while no reviewed positive mapping
or separately authorized schema successor exists.

Confirm approval of this blocker contract alone would not authorize
materialization.

---

### CMR-RR10 — Required successor direction

Decision:

Notes:

Determine which technical successor is required.

If a deterministic lossless mapping to the existing frozen schema is
demonstrably possible, identify the precise mapping that must be placed in a
separately authorized successor mapping contract and independently reviewed.

If the frozen schema cannot losslessly represent approved V4, state whether a
separately governed canonical-schema successor is required.

Do not modify or reinterpret V1 in place.

---

## Overall technical review decision

Choose exactly one:

`APPROVE_MAPPING_BLOCKER_CONTRACT`

`REVISION_REQUIRED`

`FAIL`

Overall decision:

Notes:

`APPROVE_MAPPING_BLOCKER_CONTRACT` means only that the V1 negative-feasibility
contract accurately describes the current mapping boundary.

It does not approve a positive mapping, does not authorize schema modification,
and does not authorize `curl.json`.

## Reviewer identity

Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name:

Human reviewer signature / recorded confirmation:

Human reviewer date:

## Evidence quarantine

The reviewer must not use:

- generated-driver source;
- selected-sample membership;
- raw model responses;
- generated-driver compiler-log semantic content;
- gold labels;
- analyzer output;
- baseline output;
- LLM-review output;
- repair output.

## Post-review rule

No assistant-generated or synthetic human approval is permitted.

After this package is committed, exact mapping-contract V1 remains immutable.

If revision is required, create a separately authorized successor rather than
editing V1 in place.

If the reviewer identifies a valid positive mapping, that mapping must be
placed in a separately authorized successor mapping contract and independently
reviewed before any canonical materialization.

If a canonical-schema successor is required, schema supersession requires its
own explicit governance authorization.

`curl.json` must not be created by this review.
