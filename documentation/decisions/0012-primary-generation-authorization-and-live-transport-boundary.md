# Decision 0012: Primary-generation authorization record and additive live-transport boundary

- Status: Accepted
- Prepared at UTC: 2026-08-09T09:03:06+00:00
- Base commit: `53f1099bcc2c1fb24c18ba388684900a79e23947`
- Base tree: `eb25cdeab6b2bf30d424dbd96149ee14679f127f`

## Context

Gate 1 is closed and the provider-free primary-controller preauthorization
package is frozen at commit `53f1099bcc2c1fb24c18ba388684900a79e23947`. That package intentionally contains
no live network transport and does not authorize primary generation.

The frozen generation protocol already requires an explicit committed
authorization record before `SVF-PRIMARY-800-V1` may open, but the repository
contains no pre-existing authorization-record schema or authorization-named
artifact.

This decision defines that missing additive boundary. It does not modify the
closed Gate 1 artifacts, the frozen request plan, the frozen controller
interface, the frozen provider-free controller core, or the frozen generation
protocol.

## 1. Frozen preauthorization package remains immutable

The following frozen artifacts remain authoritative inputs:

- request plan SHA-256:
  `f6712fb4baa7b895f6de82f111f373bf987f0da9166b944232556b99b6ec0440`
- controller-interface SHA-256:
  `ffc143952f0b7963cb4f8ec5853a0cc3855775cc7a3292e6ca7d1a660fbc1d56`
- provider-free controller-core SHA-256:
  `6a7f4e47086c1062f041ad461dfd0769833cefe4a49cb8fae1a7fc7644a140c2`
- interface-verifier SHA-256:
  `cc0980181996b861df38d841339819e34b0cc0cd226e0fcb97e28c330ac2fe58`
- final provider-free dry-run SHA-256:
  `0f5f17497f6d798ad81af56a3f4aede4962ce777c5904684600344caf80fa2ca`
- preauthorization freeze-manifest SHA-256:
  `1325f366b554b5fde90fde8153850f588ce228d54e80a8be4ad7dd987972e7e4`

No later authorization or transport implementation may rewrite these frozen
files.

## 2. Additive authorization record

The sole operational authorization artifact for the first primary window is
fixed at:

`evidence/generation_opening/primary_generation_authorization.v1.json`

Its machine-readable schema is:

`config/schemas/primary_generation_authorization_record.schema.json`

Creating the schema does not authorize generation.

A future authorization record is effective only when all of the following hold:

1. the record validates against the frozen schema;
2. its status is exactly `AUTHORIZED_FOR_PRIMARY_WINDOW_OPEN`;
3. its window ID is exactly `SVF-PRIMARY-800-V1`;
4. it binds the exact frozen preauthorization package and request plan;
5. a fresh provider-capability requalification has PASS status and matches both
   frozen model targets, endpoints, and thinking controls;
6. the authorization record itself is tracked and present in the current
   committed `HEAD`;
7. the repository is clean immediately before the window opens;
8. the execution layer independently verifies the authorization record before
   reading either API secret;
9. the actual `window/open.json` record is created immediately before logical
   slot 0001.

The authorization record does not itself contain `opened_at_utc`; the actual
opening timestamp belongs to the append-only execution evidence.

## 3. Frozen protocol false value is not rewritten

The historical field
`config/generation_execution_protocol.json.authorization.primary_generation_authorized`
remains `false` because that frozen file captures the pre-opening
preregistration state.

Operational authorization is additive and can arise only from the separately
committed authorization record defined above. The frozen protocol itself is not
edited to toggle authorization.

## 4. Additive live-transport contract

The live transport contract is fixed at:

`config/primary_live_transport_contract.v1.json`

The contract is initially `CANDIDATE_UNCOMMITTED` and
`execution_enabled = false`.

A future live execution implementation must remain separate from the frozen
provider-free controller core and must refuse network access unless the
authorization record passes all frozen checks.

## 5. Request-byte boundary

The live layer may transmit only the exact canonical provider request body
represented by each frozen request-plan record.

Before every invocation it must:

1. canonicalize the frozen `request_body` using the already-frozen JSON byte
   contract;
2. recompute its SHA-256;
3. require equality with that slot's frozen `request_body_sha256`;
4. add credentials only in the provider-specific HTTP header;
5. never place an API secret in the retained request body, metadata, log,
   digest input, or cost calculation.

Transport retries must reuse byte-identical request-body bytes.

## 6. Provider endpoints and thinking controls

DeepSeek uses exactly:

`https://api.deepseek.com/chat/completions`

with:

`thinking.type = disabled`

Gemini uses exactly:

`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent`

with:

`generationConfig.thinkingConfig.thinkingLevel = MINIMAL`

No endpoint, model, or thinking-control substitution is permitted.

## 7. Response preservation precedes classification

For every complete HTTP response, the execution layer must preserve the raw
response bytes and redacted response headers before provider parsing,
terminal-status classification, extraction, or compilation.

Any complete HTTP response is non-retryable as a transport failure.

## 8. Cost accounting

The frozen pricing snapshot is:

`evidence/gates/gate1/provider_pricing/pricing_snapshot.v2.json`

SHA-256:

`a52e4751a1c1095cbf37183c1c658c52a26190c01a302c55710a47f168a187b6`

Raw provider usage metadata must always be preserved.

DeepSeek cost is estimated from reported cache-hit input tokens,
cache-miss input tokens, and completion tokens using the frozen snapshot.

Gemini cost is estimated from reported prompt tokens plus reported candidate
and thinking tokens using the frozen Standard-paid rates. No cached-content
discount is applied because the frozen request plan does not request explicit
cached content. An unexpected cached-content usage field or insufficient
usage metadata triggers pause rather than an invented estimate.

Cost values are evidence estimates from the frozen price snapshot, not claims
about the provider's final invoice.

## 9. Pause-before-next-call rule

The triggering invocation is preserved and no subsequent primary call may be
sent after any frozen pause condition, including model/version drift,
thinking-control rejection, authentication/balance/permission/rate-limit
responses, materially changed endpoint behavior, repeated service errors,
request-byte drift, preservation failure, or cost-accounting metadata that
cannot satisfy this frozen contract.

## 10. Driver-source storage and byte identity

The append-only retained driver-source path for every successfully parsed,
non-empty logical model-text string is fixed at:

`slots/{logical_slot_id}/driver.c`

This path is relative to the already-frozen primary-generation evidence root
`evidence/primary_generation/SVF-PRIMARY-800-V1`.

The stored driver-source bytes are exactly the UTF-8 encoding, without BOM, of
the provider parser's logical model-text Unicode string. No newline is added or
removed and no trimming, Markdown-fence stripping, commentary stripping,
reformatting, source repair, include insertion, entrypoint insertion, API-call
insertion, or compiler-feedback transformation is permitted.

For a successfully parsed non-empty model-text string, `driver.c` is written
with append-only create-new semantics before duplicate classification and before
compilation. `driver_source_sha256` and `driver_source_byte_length` are computed
from exactly those retained bytes.

For `MISSING_CODE`, `EXTRACTION_FAILURE`, or an upstream transport/provider
terminal status, no `driver.c` is created because no compile-eligible extracted
source exists.

A later exact duplicate still retains its own `driver.c`. Duplicate identity is
then determined from exact retained driver-source bytes within the frozen
`requested_model_id + library + scenario_id` task group. The earliest
successfully extracted non-empty occurrence remains canonical; a later exact
duplicate receives `DUPLICATE_OUTPUT`, records
`duplicate_of_logical_slot_id`, and is not compiled.

This additive storage rule does not alter the frozen extraction semantics,
duplicate semantics, terminal-status precedence, or compilation contract.

## 11. Invocation evidence and operational pause semantics

Every operational transport invocation record, including a transport-failure
invocation, contains all frozen per-invocation fields plus the additive fields
declared by `config/primary_live_transport_contract.v1.json`.

For an authorized primary execution,
`authorization_record_path`, `authorization_record_sha256`, and
`execution_head_commit` are non-null and bind the exact committed
authorization context. Provider-free synthetic qualification may retain these
three fields as null, but the fields themselves remain present.

`request_body_sha256_verified` is true only after the canonical outbound body
has been recomputed and matched against the frozen per-slot body hash.
`request_body_byte_length` records the transmitted secret-free body length.
`cost_estimate_status` records the deterministic result of the frozen cost
accounting policy, or `NOT_AVAILABLE` when no complete HTTP response exists.

The frozen pause condition "endpoint behavior materially changes" is
operationalized as either:

1. any complete HTTP redirect response in the 300--399 range; or
2. any complete successful 2xx response whose body is not a JSON object or
   lacks the frozen provider-specific response envelope. For DeepSeek, the
   envelope requires `choices` or `error`; for Gemini it requires
   `candidates` or `promptFeedback`.

The frozen condition "provider outage or repeated service HTTP errors" is
operationalized deterministically per provider. A complete HTTP 502, 503, or
504 response is treated as an outage indicator and pauses immediately after
preservation. Other complete 5xx responses increment a provider-specific
consecutive-service-error counter. Two consecutive complete 5xx responses
from that same provider trigger pause. A complete non-5xx response from that
provider resets its counter. Responses from the other provider do not alter
the first provider's counter.

The triggering complete response and its invocation evidence are preserved
before pause. No subsequent primary provider call is permitted after pause
until the governed resolution process is completed.

## 12. Separation

This decision does not:

- create an authorization record;
- open `SVF-PRIMARY-800-V1`;
- read API credentials;
- perform provider calls;
- perform primary generation;
- inspect generated driver content;
- execute linked generated drivers;
- implement or run the analyzer;
- implement or run repair.

Repair remains prohibited until Gate V.
