# Decision 0011: Generation-input provenance and controller boundary

- Status: Accepted
- Gate: Post-Gate1 generation-opening control
- Prepared at UTC: 2026-08-09T07:58:04Z
- Frozen at UTC: 2026-08-09T08:19:05Z

## Context

Gate1 froze the scenario manifest, system prompt, user-message template,
generation protocol, and their recorded hashes before primary generation.

A post-freeze reconstruction audit established two different provenance
results.

First, the recorded model-visible bundle SHA-256

`14b6d91841b63fed6776f312bfec5c5c4b523661bee4f0c00da79c563fdd8df2`

is exactly reproducible from the frozen 80 bindings as compact,
key-sorted UTF-8 JSON with no trailing line feed, where every array item is:

`library + scenario_id + model_visible`

and `model_visible` contains only `task` and
`required_feature_symbols`.

Second, the recorded historical assembled-80-request-bundle SHA-256

`5dc64268d13a7770937a52763f509894888e97dc1d1d737d1e97c91390b3f976`

was not reproduced by the tested deterministic reconstruction candidates.
The original byte serialization is therefore not sufficiently specified to
serve as an executable primary-controller byte contract.

This decision resolves those ambiguities without modifying the closed
Gate1 package.

## Decision

### 1. Frozen scenario-manifest authority

The complete frozen scenario manifest remains authoritative by its
Gate1-bound SHA-256:

`a7ab361e6e2d41d9051e48bc7626f0be37c1df9ec35f788a9a019b010054a2db`.

Its root status `FROZEN_GATE1`, its 80 frozen bindings, frozen library order,
frozen scenario order, and model-visible contents are execution inputs.

The row-level value `DRAFT_REVIEW_REQUIRED` is treated as historical
pre-freeze workflow metadata rather than a post-freeze execution blocker.

This interpretation is additive only. The frozen scenario file must not be
edited merely to rename or normalize that row-level status.

### 2. Model-visible boundary

Only the frozen `model_visible` fields may enter model prompts.

`hidden_research_metadata`, `binding_status`, `task_slug`, protocol rules,
defect examples, verifier output, manual labels, and repair feedback must
not be exposed to the generation models unless independently authorized by
a later preregistered amendment.

The reproduced model-visible bundle hash above is retained as an executable
integrity check.

### 3. Historical assembled-request hash

The historical assembled-request hash `5dc642...` remains preserved as
Gate1 provenance evidence.

Because its original byte serialization was not recovered, the controller
must not claim that newly assembled provider requests are byte-identical to
that historical bundle merely because they derive from the same frozen
semantic inputs.

The historical hash must not be overwritten, silently replaced, or
retroactively redefined.

### 4. New executable serialization contract

Before primary generation is authorized, a separate additive
machine-readable Primary Controller Interface contract must freeze:

- deterministic construction of all 80 user messages;
- deterministic construction and identifiers of all 800 logical slots;
- canonical slot order;
- provider-neutral request descriptors;
- exact provider-adapter request bodies;
- exact provider endpoints;
- exact response parsers;
- exact truncation/refusal/API-error mapping;
- retry-invocation records;
- append-only artifact paths and ledger records;
- payload hashes and source hashes;
- pause behavior;
- extraction and compilation handoff.

That new serialization receives its own versioned SHA-256 and does not
replace either historical Gate1 bundle hash.

### 5. Provider endpoint authority

The `base_url` strings stored in `config/model_targets.json` are frozen
provider base-URL configuration/provenance values. They do not by
themselves define the complete executable generation endpoint, so the
primary controller must not derive an operational endpoint by undocumented
or ad hoc concatenation.

The controller interface contract must instead freeze explicit operational
endpoint strings matching the successfully qualified transports.

For DeepSeek, the qualified generation endpoint is:

`https://api.deepseek.com/chat/completions`

For Gemini, the qualified generation endpoint is:

`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent`

No endpoint substitution is allowed during the primary window.

### 6. Thinking-control authority

The provider adapters must preserve the qualified thinking controls.

DeepSeek uses the qualified non-thinking request control:

`thinking.type = disabled`

Gemini uses the qualified minimum-thinking request control:

`generationConfig.thinkingConfig.thinkingLevel = MINIMAL`

The controller must not silently drop, rename, normalize, or substitute
these controls. Provider rejection or material behavior change triggers the
already-frozen pause rule.

### 7. Prompt byte preservation

The system prompt and user-message template are read from their frozen UTF-8
files without trimming their final line feeds.

User-message construction must preserve the frozen template text and may
substitute only:

- `library`;
- `scenario_id`;
- `task`;
- comma-and-space joined `required_feature_symbols`.

No hidden scenario field may participate in prompt construction.

### 8. Authorization boundary

This decision does not authorize primary generation.

It does not open `SVF-PRIMARY-800-V1`.

It does not authorize a provider call, generated-driver inspection,
analyzer implementation or execution, or repair.

A provider-free synthetic controller dry run must pass before a separate
committed generation-opening authorization is considered.

Repair remains prohibited until Gate V.
