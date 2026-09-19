# D0296 — Reconcile Scientific Authority After Administrative Evaluation Chain and Exploratory Prototype Artifacts

Date: 19 September 2026

Status:

`AUTHOR_CANDIDATE — CORRECTIVE SCIENTIFIC-AUTHORITY RECONCILIATION — NOT YET INDEPENDENTLY VERIFIED OR FROZEN`

## Purpose

D0296 reconciles the scientific authority of the historical D0281–D0292
administrative evaluation chain and the later exploratory Python verifier /
annotation-scaffolding commits with the still-governing Stage-A prerequisite
boundaries.

This decision does not delete, rewrite, amend in place, or conceal any
historical Git object.

## Source checkpoint

Current HEAD:

`9185a71e7932f0cab3707a1d131731c072567c2f`

Current origin/main:

`9185a71e7932f0cab3707a1d131731c072567c2f`

The reconciliation artifact authored with this decision is:

`evaluation/governance_reconciliation/d0296_scientific_authority_reconciliation.json`

SHA-256:

`cb0f4bf4583981df67e385abe55415dbd2cd617bca618eb26f13170e596b251c`

## Preserved upstream scientific boundary

The authoritative historical Schema-V2 activation remains D0066.

The later B2/accounting chain did not establish B2 readiness or operational
Schema-V2 materialization before the administrative D0281–D0292 chain.

In particular, the governed pre-evaluation boundary retained:

- B2 readiness not established;
- B2 not authorized;
- concrete operational mapping not authorized;
- active Schema-V2 materialization not authorized;
- analyzer authorization not established;
- baseline authorization not established;
- repair authorization not established.

D0296 does not change those upstream scientific facts.

## Administrative D0281–D0292 classification

D0281 through D0292 remain immutable historical records.

For scientific-result authority, D0296 classifies that chain as:

`HISTORICAL_ADMINISTRATIVE_DECLARATIVE_CHAIN_NOT_EMPIRICAL_STAGE_A_RESULT_EVIDENCE`

The chain contains declarations such as downstream-evaluation authorization,
RQ execution, result freezing, paper traceability, publication packaging, and
reviewer reproduction metadata.

Those declarations do not by themselves establish that the proposal-defined
Stage-A empirical experiment occurred.

The D0285–D0288 evaluation areas contain no concrete:

- precision result;
- recall result;
- F1 result;
- confusion-matrix result;
- bootstrap interval;
- per-driver gold-versus-prediction result; or
- proposal-level Clang LibTooling / Clang CFG analyzer execution evidence.

Therefore D0281–D0292 must not be cited as proof of completed RQ1, RQ2, RQ3,
or RQ5 empirical results, completed analyzer evaluation, final Stage-A
evaluation, or Gate-V scientific freeze.

This is a scientific-authority correction, not a historical deletion.

## Exploratory prototype classification

Commit:

`2b634265534de398e450771452d0bef54a46e89c`

subject:

`implement FSM verifier and initial zlib verification pipeline`

is retained as a historical exploratory implementation checkpoint.

Its scientific classification is:

`PRE_P11_EXPLORATORY_PYTHON_REGEX_FSM_PROTOTYPE_NONAUTHORITATIVE_FOR_PAPER_RESULTS`

It is not the proposal-defined Clang LibTooling + Clang CFG +
bounded resource-state/path-sensitive analyzer.

The existing exploratory result artifact:

`evaluation/verification_results.jsonl`

has SHA-256:

`15e48e0b256fb1bfca315d4434bd9621f8206437e99f968b00124b3a517ccb1e`

and currently contains:

- 487 rows;
- 414 VALID;
- 61 UNKNOWN;
- 12 VIOLATION-MUST;
- 414 zero-trace rows;
- 73 nonzero-trace rows.

These values are preserved only as exploratory diagnostic output.

They are not gold-backed detection metrics and must not be reported as
SemanticVerify-Fuzz paper results.

## Annotation-scaffolding classification

Commit:

`f29e9894343a29027ad856277626c75a92cf277d`

created zero-byte zlib annotation placeholders.

Commit:

`9185a71e7932f0cab3707a1d131731c072567c2f`

added a draft zlib annotation protocol.

The current annotation protocol SHA-256 is:

`ec6ca966be182082d64b65419d2e5fadcc60d2c069360ecd7687340adb35cfdc`

The current:

`annotation/zlib/gold_labels.json`

is empty.

These artifacts are therefore classified as:

`DRAFT_SCAFFOLDING_NOT_GOVERNED_P10_GOLD_ANNOTATION`

They do not establish that P10 started, and they do not authorize annotation
of the exploratory 12 VIOLATION-MUST outputs.

## Current scientific stage state

D0296 records the current Stage-A scientific state as:

- P8 — BLOCKED / NOT COMPLETED;
- P9 — NOT COMPLETED;
- P10 — NOT STARTED;
- P11 — NOT STARTED;
- P12 — NOT STARTED;
- P13 — BLOCKED and outside the current Paper-1 Stage-A verification work.

The absence of:

`config/protocol_specifications/curl.json`

is preserved.

No positive operational V4-to-V2 mapping is established by D0296.

## No-backflow rule

Neither:

- D0281–D0292 administrative declarations;
- exploratory verifier outputs;
- the 414 / 61 / 12 diagnostic counts;
- the draft annotation protocol; nor
- the empty gold-label file

may be used to retroactively satisfy, bypass, or infer completion of an
earlier protocol-specification, gold-annotation, analyzer, baseline, or
evaluation prerequisite.

## Explicit nonauthorization

D0296 does not authorize:

- positive V4-to-V2 mapping execution;
- curl.json materialization;
- P10 gold annotation;
- annotation of the 12 exploratory VIOLATION-MUST outputs;
- analyzer implementation;
- analyzer execution;
- baseline execution;
- RQ evaluation execution;
- repair implementation;
- repair execution;
- mutation of historical D0281–D0292 artifacts;
- mutation of exploratory verification results; or
- history rewriting.

## Author-candidate boundary

D0296 is only an author-candidate at this checkpoint.

It is not independently verified or frozen by its own authoring transaction.

No commit and no push are authorized by this authoring action.

## Next required checkpoint

`INDEPENDENT_READ_ONLY_VERIFY_REVISED_D0296_AUTHOR_CANDIDATE_BEFORE_COMMIT_OR_PUSH`


## Revision 2 after independent review

The first independent static review of this uncommitted D0296
author-candidate returned:

`REVISION_REQUIRED_BEFORE_COMMIT`

with four findings:

1. D0281–D0292 exact SHA-256 identities were not durably embedded in D0296.
2. D0285 does not explicitly list `analyzer_execution` while D0286 later
   records `analyzer_execution`.
3. D0240 was not explicitly provenance-bound.
4. D0241 was not explicitly provenance-bound.

Revision 2 addresses exactly those findings.

No new decision number is created.

No historical decision, result, evidence artifact, gold label, protocol
specification, analyzer output, or Git history object is modified by this
revision.

The superseded uncommitted Revision-1 identities were:

- D0296 decision SHA-256:
  `1cd70c2f66472872df0249f3d58e1298a9271f41a10479138d4cf1fa7dde8e6c`
- D0296 machine artifact SHA-256:
  `d21262084589f4690bfa0634939d85867ae4be0509e7e56804431bc032feca7f`

Those hashes identify only an uncommitted author-candidate revision.

## Exact upstream governance bindings

The following tracked objects are bound at source checkpoint
`9185a71e7932f0cab3707a1d131731c072567c2f`.

| Object | Path | SHA-256 | Git blob OID |
|---|---|---|---|
| D0066 decision | `documentation/decisions/0066-activate-schema-v2-and-adopt-decision-0019-successor.md` | `6bd97e92f97f77d7e7e36bbc9a334ad115f1ebe8f8a2e9f3d0d2b2c361da65d2` | `8ba3c6590102267d694edf958456e2b855e821a6` |
| D0240 decision | `documentation/decisions/0240-govern-b2-authoritative-input-bindings-without-b2-authorization.md` | `03e34ea61a69741e3267b768e5dad0b0bd9704b48c78b17c1f74b7b16be79359` | `0d42f205aaa3d040b0ec88b9e60d980a9590f0fc` |
| D0240 machine governance artifact | `evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0240_b2_authoritative_input_binding_governance_v1/01_b2_authoritative_input_binding_governance.v1.json` | `41bc880c8a028301242a03440b899ed4d1aa6638a7be98813308a5a578533da8` | `88ca3d1b06048de1025e5aafe10cc8c48faff14f` |
| D0241 decision | `documentation/decisions/0241-design-carrier-admissibility-evidence-closure-before-b2-without-execution-authorization.md` | `64ca946cc05f8b0295c7e9e6c73600f406a26885ce2d9abc12d1e2a08ea83e7c` | `1792e5e854b0eeada667c055fba2aa2a2fcca57f` |


The D0240 machine governance artifact explicitly records:

- `B2_readiness = false`;
- `B2_execution = false`;
- `B5_concrete_source_unit_carrier_mapping = false`;
- `B6_req06_req14_accounting_satisfaction_determination = false`;
- `active_schema_v2_materialization = false`;
- `analyzer = false`;
- `baseline = false`; and
- `repair = false`

inside its `explicit_nonauthorization` /
`substantive_results_established` structures.

Therefore D0240 is a binding-only governance checkpoint, not an operational
B2, mapping, Schema-V2 materialization, analyzer, baseline, or repair
authorization.

D0241 separately records:

- `B2_READINESS_ESTABLISHED=NO`;
- `B2_AUTHORIZED=NO`;
- `CONCRETE_MAPPING_AUTHORIZED=NO`;
- `ACTIVE_SCHEMA_V2_MATERIALIZATION_AUTHORIZED=NO`;
- `ANALYZER_AUTHORIZED=NO`;
- `BASELINE_AUTHORIZED=NO`; and
- `REPAIR_AUTHORIZED=NO`.

These bindings make the upstream scientific boundary explicit.

## Exact D0281–D0292 historical bindings

The administrative/declarative chain classified by D0296 is bound to the
following exact tracked objects.

| Decision | Path | SHA-256 | Git blob OID |
|---|---|---|---|
| D0281 | `documentation/decisions/0281-freeze-final-evidence-accounting-manifest.md` | `8edf04f012bcc9e74d2ec894526d4f4fd8278d77ca760ee8d68407b7313028be` | `efbc9e2d91083249e9eeada9c0157af1349d98fe` |
| D0282 | `documentation/decisions/0282-authorize-evaluation-dataset-construction-from-frozen-evidence-accounting-manifest.md` | `f5bb22f96097e6c4fd6e86ef51eea57d130fa605743eb300446a5dfc5fae969e` | `f441e0cefb9d38f242f55c742effea6abebd2c3d` |
| D0283 | `documentation/decisions/0283-execute-evaluation-dataset-construction-from-frozen-accounting-manifest.md` | `c8ed088371a61e6706ef234578c9afd0a199051558ed2fc49e9a764a565277cb` | `cb45267fbc428c3a0a17703167c51e753d6c3fda` |
| D0284 | `documentation/decisions/0284-freeze-evaluation-dataset-artifact.md` | `7ec815a677673068e87d6c166714856897df73bb2e24ec02f9c47a043df1be14` | `ebef2da492115d7aed0bd64b6aee875ad673cff6` |
| D0285 | `documentation/decisions/0285-authorize-rq-evaluation-execution-from-frozen-dataset.md` | `6501732a1f6c620945d526957bda3bc184b97d7608aa6e7969c9e5676c526f0b` | `4f8379d92e345a7d0d5e82a4f0763d42bf46662a` |
| D0286 | `documentation/decisions/0286-execute-rq-evaluation-from-frozen-dataset.md` | `93db22e3aa812e18ccf1cb86e2c93b381beb5566182954938bcd05dcd6046451` | `adfe935f1b4d0426598fbbe163d4bab376ef4ab1` |
| D0287 | `documentation/decisions/0287-freeze-rq-evaluation-results.md` | `c4a2d4ca8933cf667516c59a0d5c933c31920c8e14d6cc9607275ce611442f9d` | `cb533557248416e3cbcc366be9b3f497e9fcc796` |
| D0288 | `documentation/decisions/0288-generate-final-evaluation-report-manifest.md` | `1e933ed4fecd19e1ef6cf91199cfa9aec7c1015aa478a3153b406c8b01614e92` | `2ba135cfc31d9d654bcd23dc71915b2355e67172` |
| D0289 | `documentation/decisions/0289-generate-paper-results-traceability-manifest.md` | `0ab0c86f6b3a9b12aa81d500c7dfefe56cd94920eb489386e9ecdfd6c0cf947c` | `b20a9287404158728ccbe6dcb1c50802475e3225` |
| D0290 | `documentation/decisions/0290-freeze-publication-evidence-package.md` | `ca0f4a41611fc31006c8c76c308c32b3edf4b81d8c4de0cbecb5eb7c169f54e2` | `ab5d31cd996b113ed2132588382ad7b5d3805cf5` |
| D0291 | `documentation/decisions/0291-generate-artifact-availability-statement.md` | `460b3e502b9ba940c5a6b058e4e0d3f7dab6b9462c6b43a34d65d086bf0f549c` | `49695ed08ed269062bd9c25e777456bfd7266ae8` |
| D0292 | `documentation/decisions/0292-generate-reviewer-reproduction-checklist.md` | `23b68bf0aeff9078fa8049c037ee23cfd57c8ce43a06e9ca6d3306a7983341b5` | `ea6825edf30df6f5628ab15c87b600dff3b82974` |


These bindings prevent the D0296 classification from floating over an
unidentified or subsequently changed historical decision set.

## D0285-to-D0286 authorization-specificity finding

The exact D0285 machine authorization lists:

- `experiment_execution`;
- `metric_computation`;
- `result_recording`; and
- `evaluation_report_generation`

as allowed operations.

It does not explicitly list:

`analyzer_execution`

The exact D0286 machine result later records:

`analyzer_execution`

as an executed operation.

Revision 2 therefore records the bounded finding:

`D0286_ANALYZER_EXECUTION_CLAIM_LACKS_EXPLICIT_D0285_ANALYZER_EXECUTION_AUTHORIZATION`

D0296 does not retrospectively interpret the generic phrase
`experiment_execution` as an explicit analyzer-execution authorization.

Separately, the earlier static audit found no concrete precision, recall, F1,
confusion-matrix, bootstrap, per-driver gold-comparison, or proposal-level
Clang LibTooling / Clang CFG execution evidence in the D0285–D0288
evaluation areas.

Consequently D0286 must not be treated as either:

- the explicit authorization basis for the proposal-defined analyzer; or
- standalone empirical proof that the proposal-defined analyzer actually
  executed and produced the claimed RQ evaluations.

## Revision-2 status

This remains an uncommitted:

`AUTHOR_CANDIDATE — NOT INDEPENDENTLY VERIFIED OR FROZEN`

Revision 2 does not self-close the four findings.

A fresh independent read-only review is required.

No positive V4-to-V2 mapping, `curl.json` materialization, P10 annotation,
P11 analyzer implementation/execution, P12 evaluation, baseline, or repair
operation is authorized by Revision 2.

## Revision-2 next required checkpoint

`INDEPENDENT_READ_ONLY_VERIFY_REVISED_D0296_AUTHOR_CANDIDATE_BEFORE_COMMIT_OR_PUSH`
