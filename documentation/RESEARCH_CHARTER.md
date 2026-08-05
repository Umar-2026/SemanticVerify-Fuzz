# Research Charter

## Authoritative title

SemanticVerify-Fuzz: Resource-Centered, Path-Sensitive Verification and
Constrained Repair of API-Protocol Violations in LLM-Generated Fuzz Drivers

## Mandatory research order

Stage A must complete RQ1, RQ2, RQ3, and RQ5 before Gate V. Gate V freezes:

- protocol specifications;
- generated corpus and build records;
- normalized gold obligations and labels;
- analyzer code and configuration;
- UNKNOWN policy;
- baseline mappings;
- ablation outputs;
- primary metrics and verification claims.

Only after Gate V may Stage B implement and evaluate C3/RQ4.

## Four contributions

- C1: Fuzz-driver-specific protocol-obligation representation.
- C2: Resource-centered path-sensitive protocol verification.
- C3: Evidence-guided constrained deterministic repair after Gate V.
- C4: Blindly annotated cross-library empirical evaluation.

## Five research questions

- RQ1: Natural defect prevalence.
- RQ2: Verification accuracy and uncertainty.
- RQ3: Value of resource-centered path sensitivity.
- RQ4: Constrained repair effectiveness after Gate V.
- RQ5: Analysis-engine transferability.

## Fresh-start rule

Earlier implementations, generated drivers, labels, results, thresholds,
schemas, and repair artifacts are not active inputs or evidence. If any
historical material is imported later, it must be quarantined as immutable
provenance and excluded from all decisions and claims.
