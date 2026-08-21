# Residual Schema-V2 Losslessness-Insufficiency Proof V1

Status: **AUTHOR CANDIDATE — INDEPENDENT HUMAN TECHNICAL REVIEW REQUIRED**

Machine-readable proof:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_residual_losslessness_insufficiency_proof_v1/01_residual_schema_v2_losslessness_insufficiency_proof.v1.json`

SHA-256:

`400f6806217f50b79d17ec77e41683d9077f64e07c63e5421c8b1922b49aaff0`

## 1. Scope

This proof evaluates whether the active Schema V2 can support an admissible,
deterministic and reverse-reconstructible projection of the exact approved
curl Technical Working Draft V4 semantics.

The claim is deliberately scoped. It is **not** a claim that arbitrary
information-theoretic encoding into strings is impossible. Opaque packing,
semantic-category repurposing and external per-rule lookup as a substitute for
canonical semantic preservation remain outside the approved losslessness
boundary.

## 2. Historical obstructions already addressed by Schema V2

The four principal structural obstructions identified against the predecessor
schema now have first-class structural carriers:

1. membership / identity-sensitive relations;
2. four machine verdicts and aggregation policy;
3. path-sensitive set-valued reasoning; and
4. structured rule preconditions, effects and bindings.

Those historical issues are therefore not reused as the residual argument.

## 3. Residual R1 — enforcement semantics

Technical Working Draft V4 contains 64 rule records and every one carries an
`enforcement` value.

There are 15 distinct enforcement classifications.

Active Schema V2 has no explicit `enforcement` carrier.

The source enforcement classification is not reconstructible from verdict
alone: three verdict groups correspond to multiple enforcement categories.

It is also not reconstructible from defect category plus verdict alone: four
such groups correspond to multiple enforcement categories.

This does not rule out every imaginable distributed encoding. It establishes
that no exact first-class carrier exists and that simple derivation from the
obvious normative outputs is non-injective. Any proposed distributed mapping
must therefore independently demonstrate semantic admissibility and exact
reverse reconstruction without opaque packing or field repurposing.

## 4. Residual R2 — exact representation-policy preservation

Three required V4 representation-policy assertions remain without explicit
Schema-V2 policy carriers:

- `normative_strength_uncertainty_must_not_be_silently_strengthened=true`;
- `resource_centered=true`; and
- `synthetic_protocol_events_invented=false`.

Existing structures provide related behavior, but related structure is not
treated as proof that the exact source assertion can be machine-checkably
reconstructed.

## 5. Supporting R3 — rule-field decomposition

Schema V2 provides a unit-level `semantic_rules` carrier for all 64 rule
records, but unit accountability is distinct from field-level losslessness.

Fields lacking a direct same-named V2 property require a separately justified
deterministic decomposition and reverse-reconstruction argument. Their mere
association through `semantic_accounting` is not sufficient.

## 6. Exit obligations and semantic accounting

All three V4 exit obligations have a unit-level Schema-V2 carrier.

Schema V2 also requires forward and reverse semantic accounting.

Neither fact by itself proves that every source field is encoded
losslessly—the accounting relation identifies carriers, while semantic
preservation still has to be established.

## 7. Author-candidate conclusion

Under the existing exact V4 losslessness and admissibility constraints, the
current evidence supports an **author-candidate residual Schema-V2
insufficiency conclusion**.

A positive V4-to-V2 mapping is therefore not authorized.

This conclusion has **not** yet received independent human technical review
and cannot itself authorize Schema V3 or any other schema successor.

## 8. Explicit non-authorizations

This proof does not authorize:

- Schema V3 or any schema successor;
- modification of active Schema V2;
- positive V4-to-V2 mapping;
- creation of `curl.json`;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## 9. Next boundary

Prepare an independent human technical review package for this exact proof V1.
