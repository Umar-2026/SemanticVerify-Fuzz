# Decision 0089 — Authorize Schema-V2 Semantic-Role Relation Formalization V1

Status: ADDITIONAL CAPABILITY EVIDENCE AUTHORING AUTHORIZED — FORMALIZATION NOT YET AUTHORED

## Human-reviewed basis

Decision 0088 immutably records the completed independent human technical
review of Capability Study V1.

CSR01 through CSR08 are PASS.

Overall human decision:

`APPROVE_SCHEMA_V2_CAPABILITY_STUDY_V1`

The bounded result:

`FURTHER_EVIDENCE_REQUIRED`

is human-approved.

The human review does not establish either a positive mapping result or a
negative impossibility result.

`POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO`

`NEGATIVE_EXISTING_V2_MAPPING_PATH_IMPOSSIBILITY_PROVEN=NO`

`ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO`

## Specific unresolved evidence gap

Capability Study V1 and its human review identify a central remaining gap:
the criterion “semantically related carriers only” has not yet been
represented as a complete machine-readable semantic-role relation sufficient
to support exhaustive admissible-composition analysis.

Decision 0089 therefore authorizes one additional evidence artifact only:

`SCHEMA_V2_SEMANTIC_ROLE_RELATION_FORMALIZATION_V1`

## Required formalization scope

The formalization must bind to:

- 10 V4 semantic containers;
- 109 V4 semantic units;
- 531 V4 leaf fields;
- 57 V4 field classes;
- 171 Schema-V2 property paths;
- 123 distinct Schema-V2 property names; and
- 59 open unconstrained Schema-V2 string carrier paths.

At minimum it must contain a machine-readable relation from V4 field classes
to Schema-V2 property paths and context refinement at V4 semantic-unit level
where field-class classification alone is insufficient.

Every evaluated relation must use one of:

- SEMANTICALLY_RELATED
- NOT_SEMANTICALLY_RELATED
- UNRESOLVED

The artifact must provide complete accounting and explicit justification for
nontrivial semantic relations.

## Admissibility constraints

The Decision-0083 admissibility constraints remain binding.

The formalization may not use:

- opaque blob packing;
- hidden semantic storage in free text;
- unrelated field repurposing;
- external lookup for reverse reconstruction;
- semantic_accounting as substitute semantic storage;
- lossy normalization; or
- silent semantic strengthening or weakening.

The four-verdict contract, UNKNOWN-first-class policy, normative-strength
uncertainty, resource-centered semantics, synthetic-event non-invention,
ownership, membership, path, return, and set-valued reasoning semantics must
remain preserved.

## Formalization is evidence, not a mapping decision

Authoring this formalization alone does not prove:

- that an admissible existing-Schema-V2 exact mapping exists;
- that no admissible existing-Schema-V2 exact mapping can exist; or
- that admissible composition enumeration is exhaustive.

The formalization itself must be treated as an author-candidate artifact and
must undergo separately authorized independent human technical review before
governance use.

## Explicit non-authorizations

Decision 0089 does not authorize:

- exhaustive composition enumeration or elimination;
- constructive positive mapping-witness authoring;
- operational V4-to-V2 mapping;
- operational V4-to-successor mapping;
- positive mapping authorization;
- active Schema-V2 modification;
- schema-successor authoring;
- Schema V3;
- successor-version preselection;
- curl.json;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## Retired verifiers

The following remain permanently retired and must not be rerun:

- Decision-0087 pre-record verifier;
- CSR01-CSR08 initial blank-state verifier;
- Decision-0085 pre-review-package verifier;
- Decision-0083 pre-study verifier.

The Decision-0089 verifier is pre-formalization-authoring only.

It may run only while the formalization artifact does not exist. It must run
its final allowed time immediately before formalization creation and must then
be permanently retired.

## Next boundary

Author Schema-V2 Semantic-Role Relation Formalization V1 only.
