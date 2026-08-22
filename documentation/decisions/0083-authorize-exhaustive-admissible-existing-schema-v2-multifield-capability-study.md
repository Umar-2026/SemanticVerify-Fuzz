# Decision 0083 — Authorize Exhaustive Admissible Existing-Schema-V2 Multi-Field Capability Study

Status: CAPABILITY-STUDY AUTHORING AUTHORIZED — NO MAPPING OR SCHEMA-SUCCESSOR AUTHORIZATION

## Human-approved basis

Decision 0082 records the completed independent human review of Corrective
Assessment V2.

CVR01-CVR08 all passed.

The human-approved bounded conclusion is:

`FURTHER_EVIDENCE_REQUIRED`

Neither of the following has been human-approved:

- `SCHEMA_SUCCESSOR_REQUIRED`
- `NO_SUCCESSOR_REQUIRED_WITH_PROVEN_ADMISSIBLE_V2_MAPPING_PATH`

## Authorized question

Decision 0083 authorizes one exhaustive capability study answering:

> Can any admissible semantically related composition of existing active
> Schema-V2 carriers preserve every required curl-V4 semantic unit exactly and
> support deterministic exact reverse reconstruction under the already
> reviewed losslessness and admissibility constraints?

## Required exhaustiveness

The study must examine the complete existing Schema-V2 semantic carrier space,
including direct and semantically related multi-field compositions.

It must not restrict analysis to same-named properties.

It must account for:

- all 17 exact V4 losslessness requirements;
- all 10 V4 semantic containers;
- all 64 rule records;
- all 3 exit obligations;
- all 10 representation-policy fields;
- all 15 enforcement classifications; and
- the complete relevant V4 rule-field inventory.

## Admissibility boundary

An admissible existing-V2 representation must use native structured Schema-V2
carriers with semantically related roles.

It must support deterministic exact forward encoding and deterministic exact
reverse reconstruction.

It must preserve the four-verdict contract, UNKNOWN as first-class,
normative-strength semantics, resource-centered semantics, ownership,
membership, path, return and set-valued reasoning.

It must not:

- use opaque blob packing;
- use free text as hidden semantic storage;
- require external lookup for reverse reconstruction;
- repurpose semantically unrelated fields;
- substitute semantic accounting for semantic storage;
- perform lossy normalization;
- silently strengthen or weaken semantics; or
- invent synthetic protocol events.

## Permitted study outcomes

The study may conclude exactly one of:

1. `PROVEN_ADMISSIBLE_EXISTING_SCHEMA_V2_MAPPING_PATH_AVAILABLE`
2. `PROVEN_NO_ADMISSIBLE_EXISTING_SCHEMA_V2_MAPPING_PATH_UNDER_REVIEWED_CONSTRAINTS`
3. `FURTHER_EVIDENCE_REQUIRED`

The study must not presuppose which outcome will result.

## Governance effect of study result

Any study result is an author candidate only and requires independent human
technical review before it can affect subsequent governance.

A positive existing-V2 capability result does not authorize an operational
positive mapping contract.

A negative existing-V2 capability result does not authorize schema-successor
authoring.

No study outcome authorizes curl.json, analyzer activity, baseline execution,
or repair.

## Permitted analysis artifacts

The study may create specification-level:

- semantic-unit inventories;
- Schema-V2 carrier inventories;
- exhaustive composition matrices;
- analysis-only candidate encoding witnesses;
- deterministic reverse-reconstruction definitions;
- collision analyses;
- semantic-noninterference analyses;
- coverage matrices;
- gap matrices; and
- machine-readable counterexamples or constructive witnesses.

It may not create an operational positive mapping contract or canonical
curl.json.

## Prohibited evidence

The study must not inspect or use:

- generated-driver source;
- selected-sample membership;
- raw model responses;
- compiler-log semantic contents;
- gold labels;
- analyzer output;
- baseline output;
- LLM-review output; or
- repair output.

## Explicit non-authorizations

Decision 0083 does not authorize:

- modification of active Schema V2;
- schema-successor authoring;
- Schema V3 authoring;
- successor-version preselection;
- operational positive V4-to-V2 mapping authoring;
- operational positive V4-to-successor mapping authoring;
- positive mapping authorization;
- curl.json creation;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## Retired verifier boundary

All previously retired authoring, package, activation, and initial blank-state
verifiers remain permanently retired.

The Decision-0083 verifier is:

`PRE_CAPABILITY_STUDY_AUTHORING_ONLY`

It may run only until Capability Study V1 is authored.

It must run its final allowed time immediately before study authoring and must
then be permanently retired.

## Next boundary

Author Exhaustive Admissible Existing-Schema-V2 Multi-Field Capability Study
V1 only.
