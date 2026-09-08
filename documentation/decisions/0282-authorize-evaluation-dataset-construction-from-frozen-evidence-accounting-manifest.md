# D0282 — Authorize Evaluation Dataset Construction From Frozen Evidence Accounting Manifest

## Decision

D0282 authorizes construction of the evaluation dataset from the frozen
D0281 final evidence accounting manifest.

The evaluation dataset is a derived evaluation artifact and does not modify
the frozen evidence chain.

## Parent Binding

D0281 final evidence accounting manifest:

`2974826`

D0280 evidence accounting integration:

`4e9784cc10fff5e991fefc9c231eec695a13d5df`

D0279 chain closure:

`7482da6f8634a5ac2c861ef98673186ee977d8ff`

## Construction Source

Input:

`D0281_FINAL_EVIDENCE_ACCOUNTING_MANIFEST`

The dataset construction must use only frozen accounting records.

## Authorized Operations

Allowed:

- create evaluation dataset indexes;
- create evaluation metadata records;
- map evidence units to experiment records;
- prepare RQ1/RQ2/RQ3/RQ5 evaluation inputs.

## Forbidden Operations

Not allowed:

- new evidence acquisition;
- snapshot reread;
- evidence extraction;
- evidence mutation;
- label mutation;
- analyzer execution;
- repair execution.

## Status

EVALUATION_DATASET_CONSTRUCTION_AUTHORIZED=YES

SOURCE_EVIDENCE_FROZEN=YES

EVIDENCE_MUTATION=NO
