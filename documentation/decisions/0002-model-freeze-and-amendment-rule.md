# Decision 0002: Model Freeze and Amendment Rule

- Status: Accepted
- Date: 2026-08-05
- Stage: Gate 0D

## Frozen targets

- Model A: `deepseek-v4-flash`
- Documented served version: `DeepSeek-V4-Flash-0731`
- Mode: provider-native non-thinking

- Model B: `gemini-3.1-flash-lite`
- Stability: stable identifier
- Mode: provider-native minimum thinking

## Fixed generation parameters

- Temperature: 0.2
- Top-p: 1.0 where supported
- Maximum output: 8,192 tokens
- Ten scenarios per library
- Five attempts per scenario/model
- Eight libraries
- Total new attempts: 800

## Stop rule

Generation cannot start until both accounts pass live model-list and
minimal-generation qualification. During primary generation, any model alias,
served-version, request-control, or material endpoint change pauses all further
calls for that provider.

A preregistration amendment must be created before generation resumes. Outputs
already collected remain preserved and are never silently replaced.

A price change is archived and reflected in cost estimates, but it cannot alter
sampling, retention, or inclusion rules.

## Secret handling

API keys are supplied only through OpenBayes Secret/environment configuration.
They are never written to the repository, evidence reports, shell scripts,
command history, logs, or chat.
