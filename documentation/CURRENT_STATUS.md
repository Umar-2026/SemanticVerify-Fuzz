# Current Status

- Repository logical path: `/openbayes/home/semanticverify-fuzz-research`
- Repository physical path: `/output/semanticverify-fuzz-research`
- Current stage: Stage A — verification
- Current milestone: Gate 0F — generation-window and transport-retry protocol complete
- Gate 0 overall: IN PROGRESS
- Gate 0A repository bootstrap: PASS
- Gate 0B environment qualification: PASS
- Gate 0C proposal provenance: PASS
- Gate 0D1 official model documentation: PASS
- Gate 0D2 live endpoint/capability qualification: PASS
- Gate 0E statistical analysis and power registration: PASS
- Gate 0F generation-window and transport-retry protocol: PASS
- Gate 1: NOT STARTED
- Gate 2: NOT STARTED
- Gate 3: NOT STARTED
- Gate 4: NOT STARTED
- Gate 5: NOT STARTED
- Gate V: NOT STARTED
- Gate 6: BLOCKED BY GATE V
- Primary generation: NOT AUTHORIZED
- Repair implementation: PROHIBITED

## Frozen live model observations

- DeepSeek requested and returned model: `deepseek-v4-flash`
- DeepSeek documented served version: `DeepSeek-V4-Flash-0731`
- DeepSeek mode: non-thinking
- Gemini requested and returned version: `gemini-3.1-flash-lite`
- Gemini mode: minimum thinking
- Live qualification report SHA-256:
  `f0b22b51684605677d4bfbfa4b187227c67093fc4c79792412797e28cb30f5c4`
- Total experimental design: 2 × 8 × 10 × 5 = 800 attempts

## Frozen statistical analysis

- Primary endpoint: held-out library-macro obligation-level F1.
- Primary paired comparison: full versus path-insensitive verifier.
- UNKNOWN is scored incorrect; raw CFG paths are not independent samples.
- Driver-cluster bootstrap within library strata: 2,000 replicates.
- Precision guard: 0.80; decision-coverage guard: 0.75.
- Power grid: 144 scenarios; 61 reached conditional and claimable 80% MDI.
- Sparse settings do not trigger post-hoc expansion; claims are withheld.
- Power report SHA-256:
  `bb746da67ccdae2eeda232aba36c53ba53ec3d7830fdd726bb4f450aa2ab9b58`

## Credential handling

Keys were supplied through hidden, ephemeral environment input. They were not
stored, printed, hashed, committed, or retained after qualification.

At least one pre-success DeepSeek call failed with HTTP 402 because the account
balance was insufficient. It created no qualification report and no
experimental output. The exact failed-attempt count was not machine-captured,
so no unsupported count is claimed.

## Remaining before Gate 0 closes

1. Create and verify the final Gate 0 manifest.

No primary generation, driver inspection, or repair implementation is
authorized.
