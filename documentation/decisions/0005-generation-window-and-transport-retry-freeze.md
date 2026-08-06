# Decision 0005: Generation Window and Transport-Retry Freeze

- Status: Accepted
- Date: 2026-08-06
- Stage: Gate 0F

## Proposal authority

Section 7.5 fixes 800 logical attempts, complete raw-output preservation,
distinct failure statuses, and retries only for transport failure. The
pre-experiment checklist requires one archived generation window and a frozen
retry policy. This decision supplies only the operational constants that the
proposal leaves unspecified.

## Frozen execution contract

- One campaign: `SVF-PRIMARY-800-V1`.
- Exactly 800 logical slots: 2 models x 8 libraries x 10 scenarios x 5 runs.
- Sequential canonical model-paired order; one request in flight globally.
- No failed slot is replaced and generation never expands to obtain a desired
  compilation or defect yield.
- Temperature 0.2, top-p 1.0 where supported, maximum output 8,192 tokens,
  streaming disabled, and provider seed/default behavior recorded.

## Retry boundary

Only failures before a complete HTTP response may be retried. A logical slot
has at most two retries after its first invocation, with deterministic waits of
5 and 20 seconds. Every invocation is retained. Any complete HTTP response,
including 4xx or 5xx, is an experimental API outcome and is never retried.

## Stop and preservation rules

Returned-model/version drift, rejection of thinking controls, material endpoint
change, authentication/balance/rate-limit failure, preservation failure, or
payload drift pauses further calls immediately. The triggering record is kept.
No silent model substitution, parameter change, slot replacement, or output
discard is allowed.

## Authorization

This freeze does not open the window. Primary generation remains unauthorized
until the final Gate 0 manifest, Gate 1 specification freeze, exact prompts and
80 scenario bindings, source locks, price snapshots, and a committed execution
authorization all pass. Repair remains prohibited until Gate V.
