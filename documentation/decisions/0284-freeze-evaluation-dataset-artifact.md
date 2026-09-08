# D0284 — Freeze Evaluation Dataset Artifact

## Decision

D0284 freezes the evaluation dataset artifact constructed by D0283.

The frozen artifact is derived only from the D0281 final evidence accounting manifest.

No evidence mutation or label mutation is performed.

## Parent Binding

D0283 execution:

`af3c73b`

D0282 authorization:

`9f4a5ea`

D0281 final evidence accounting manifest:

`2974826`

## Freeze Boundary

Included:

- dataset artifact manifest generation
- evaluation dataset hash recording
- experiment input freeze

Excluded:

- new evidence acquisition
- snapshot reread
- evidence mutation
- label mutation
- analyzer execution
- repair execution
