# Decision 0003: Live Model Qualification Freeze

- Status: Accepted
- Date: 2026-08-05
- Stage: Gate 0D2

## Qualified targets

- DeepSeek request ID: `deepseek-v4-flash`
- DeepSeek returned model: `deepseek-v4-flash`
- DeepSeek documented served version: `DeepSeek-V4-Flash-0731`
- DeepSeek control: non-thinking
- Gemini request ID: `gemini-3.1-flash-lite`
- Gemini returned model version: `gemini-3.1-flash-lite`
- Gemini control: minimum thinking

Both model-list checks and both exact low-token probes passed. The immutable
live report SHA-256 is
`f0b22b51684605677d4bfbfa4b187227c67093fc4c79792412797e28cb30f5c4`.

## Configuration binding

The exact prequalification target lock is preserved at
`evidence/gates/gate0/model_targets_prequalification.json` with SHA-256
`d8d048bba349e45a3c2267567c37a3d771011d50ceac885fb8a953149a5cc401`.

The active target configuration records the PASS transition, but does not
authorize primary generation.

## Environmental incident

Before the successful qualification, at least one DeepSeek request returned
HTTP 402 because the account balance was insufficient. No report or
experimental output was created. The exact number and timestamps of failed
setup attempts were not machine-captured and are therefore not asserted.

## Authorization boundary

Gate 0 remains IN PROGRESS. Statistical registration, the generation-window
protocol, and the final Gate 0 manifest remain pending. Primary generation is
not authorized. Repair remains prohibited until Gate V.
