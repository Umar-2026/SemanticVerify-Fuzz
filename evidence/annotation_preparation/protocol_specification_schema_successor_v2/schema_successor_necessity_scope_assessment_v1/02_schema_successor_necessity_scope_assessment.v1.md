# Schema-Successor Necessity/Scope Assessment V1

Status: AUTHOR ASSESSMENT CANDIDATE — INDEPENDENT HUMAN TECHNICAL REVIEW NOT YET COMPLETED

## 1. Assessment boundary

This assessment addresses one bounded question:

> Under the already reviewed exact curl V4 losslessness and admissibility
> constraints, can the existing active Schema V2 support an admissible,
> deterministic, exactly reverse-reconstructible representation, or is a
> schema successor required?

This assessment does not claim that Schema V2 is generally unusable and does
not claim abstract information-theoretic impossibility.

The exact reviewed inputs are:

- curl Technical Working Draft V4 SHA-256:
  `e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8`
- active Schema V2 SHA-256:
  `c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956`
- residual Schema-V2 insufficiency Proof V1 SHA-256:
  `400f6806217f50b79d17ec77e41683d9077f64e07c63e5421c8b1922b49aaff0`

The residual-insufficiency human-review chain is complete. RI01 was originally
REVISION_REQUIRED because of activation/provenance evidence, then passed the
focused corrective RI01-C rereview. RI02-RI08 remain PASS_CLOSED. The
historical first-round overall REVISION_REQUIRED decision remains unchanged.

## 2. Existing-V2 alternatives assessed

### A. Direct use of existing Schema-V2 carriers

Not sufficient.

The reviewed residual evidence establishes:

- 64 of 64 V4 rule records carry an `enforcement` field;
- those rules use 15 distinct enforcement classifications;
- Schema V2 has no explicit enforcement carrier;
- three exact representation-policy assertions lack explicit
  machine-checkable Schema-V2 carriers; and
- additional rule and exit-obligation field-level mappings remain without a
  reviewed exact reconstruction proof.

### B. Derive enforcement from verdict or defect-plus-verdict

Not admissible as exact reconstruction.

The reviewed evidence contains:

- 3 verdict-to-enforcement ambiguous groups; and
- 4 defect-plus-verdict-to-enforcement ambiguous groups.

Therefore those fields do not determine the original enforcement
classification.

### C. Repurpose unrelated Schema-V2 fields

Rejected under the existing admissibility constraints.

Semantic-field repurposing would not itself establish a semantically
admissible, deterministic inverse representation.

### D. Opaque packing or external per-rule lookup

Rejected under the existing reviewed contract.

Opaque packing and external lookup substitution are not accepted substitutes
for machine-checkable semantic representation.

### E. Semantic accounting alone

Not sufficient.

Semantic accounting can bind source units to destination carriers, but the
accounting relation does not itself encode missing source semantics. Unit
accountability is therefore not equivalent to field-level losslessness.

## 3. Minimum semantic scope of a successor

This assessment specifies capability requirements only. It does not design or
name a successor schema.

A successor must provide an admissible machine-checkable representation that:

1. preserves all 15 observed V4 enforcement classifications across all 64 rule
   records without silent strengthening or weakening;
2. preserves and exactly reconstructs
   `normative_strength_uncertainty_must_not_be_silently_strengthened=true`;
3. preserves and exactly reconstructs `resource_centered=true`;
4. preserves and exactly reconstructs
   `synthetic_protocol_events_invented=false`;
5. provides a reviewed deterministic mapping/decomposition and inverse
   reconstruction for every remaining V4 rule field;
6. provides the same for all fields of all three V4 exit obligations; and
7. retains semantic accounting as traceability rather than treating it as
   storage for otherwise unrepresented semantics.

The successor scope must therefore not be narrowed artificially to only the
enforcement field and three policy assertions.

## 4. Remaining rule-field scope

The V4 rule-field inventory includes the direct fields
`rule_id`, `defect`, and `verdict`, together with fields whose exact
field-level preservation or semantic decomposition remains to be demonstrated,
including:

- argument_scope
- classification_note
- cleanup_obligation_effect
- condition
- dependent_reasoning_policy
- effect
- enforcement
- excludes
- fact
- function
- precedence
- precondition
- reason
- recommendation
- return
- return_behavior
- return_note
- runtime_post_state
- structural_effect

Direct carriers for some individual fields do not establish losslessness of
the complete source rule record.

## 5. Exit-obligation scope

There are three V4 exit obligations.

Their source-field scope includes:

- classification_note
- condition
- defect
- discharge_condition
- enforcement
- failed_cleanup_effect
- missing_cleanup_verdict
- required_discharge
- resource

Each field must either have a direct semantic carrier or a reviewed
deterministic decomposition with exact inverse reconstruction.

## 6. Backward compatibility

A future successor must not rewrite or silently reinterpret the already frozen
zlib/libpcap Schema-V1 specifications.

Historical Schema V1 and active Schema V2 governance artifacts remain
immutable.

No mandatory migration of the existing frozen zlib/libpcap specifications is
justified merely because curl requires a richer representation.

A future successor must use separately reviewed version dispatch and explicit
schema-version binding.

Schema V2 remains active until a separately reviewed and separately authorized
successor activation occurs.

## 7. Minimum governance sequence

If this assessment is independently approved, the next stages must remain
separate:

1. separately authorize successor-schema authoring;
2. author a successor candidate;
3. machine-check its semantic-carrier and exact roundtrip requirements;
4. independently review the successor candidate;
5. separately finalize successor hash/canonicalization and dispatch governance;
6. separately authorize and execute successor activation;
7. only after activation, separately authorize a positive curl
   V4-to-successor mapping contract;
8. independently verify and review complete forward preservation and exact
   reverse reconstruction;
9. only then separately authorize `curl.json` canonical materialization.

Analyzer implementation/execution, baseline execution, and repair remain
outside this assessment.

## 8. Author-candidate conclusion

**SCHEMA_SUCCESSOR_REQUIRED**

This conclusion is bounded:

A schema successor is required **if the project continues to require exact
lossless canonical representation of curl V4 under the existing reviewed
admissibility constraints**.

`NO_SUCCESSOR_REQUIRED_WITH_PROVEN_ADMISSIBLE_V2_MAPPING_PATH` is not
selected because no such mapping path has been proven and the reviewed
residual-insufficiency chain is complete.

`FURTHER_EVIDENCE_REQUIRED` is not selected because the identified
Schema-V2 residual-insufficiency evidence has already completed independent
technical review and corrective provenance rereview. The remaining limitation
is representational capability rather than an unresolved evidence-provenance
question.

This author assessment does **not** authorize successor-schema authoring,
select a successor version number, create Schema V3, authorize a positive
mapping, create `curl.json`, or authorize analyzer/baseline/repair work.

Independent human technical review of this assessment is required before any
successor authoring authorization may be considered.
