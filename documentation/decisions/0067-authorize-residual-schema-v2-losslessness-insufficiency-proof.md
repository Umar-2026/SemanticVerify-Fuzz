# Decision 0067 — Authorize Residual Schema-V2 Losslessness-Insufficiency Proof

Status: AUTHORIZED FOR PROOF AUTHORING ONLY — NO SCHEMA SUCCESSOR AUTHORIZED

## Basis

Schema V2 is active under Decision 0066.

Read-only post-activation audits against exact curl Technical Working Draft V4
and the active Schema V2 identified residual losslessness questions that block
a positive V4-to-V2 mapping authorization.

The mechanically recomputed pre-authoring facts include:

- 64 V4 rule records;
- 15 distinct V4 `enforcement` values;
- no explicit Schema-V2 `enforcement` carrier;
- 3 verdict-to-enforcement ambiguous groups;
- 4 defect-plus-verdict-to-enforcement ambiguous groups; and
- 3 unresolved exact representation-policy fields:
  - `normative_strength_uncertainty_must_not_be_silently_strengthened`;
  - `resource_centered`;
  - `synthetic_protocol_events_invented`.

These observations are not themselves an independently reviewed final
insufficiency conclusion.

## Authorization

This decision authorizes authoring a residual Schema-V2 losslessness-
insufficiency proof bound to:

- `config/annotation/curl_technical_protocol_working_draft.v4.json`
  SHA-256 `e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8`;
- `config/annotation/curl_canonical_representation_mapping_contract.v4.json`
  SHA-256 `9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070`;
- `config/schemas/protocol_specification.v2.schema.json`
  SHA-256 `c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956`;
- the active V2 hash contract; and
- the active schema-version dispatch.

The proof must distinguish historical obstructions already resolved by Schema
V2 from residual gaps that may remain under the strict V4 losslessness
contract.

Independent technical human review is required before any residual
insufficiency conclusion may authorize a schema successor.

## Explicitly not authorized

Decision 0067 does not authorize:

- Schema V3 or any other schema-successor authoring;
- modification of active Schema V2;
- positive V4-to-V2 mapping authoring or approval;
- creation of `curl.json`;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## Next boundary

Author the residual Schema-V2 losslessness-insufficiency proof V1 and prepare
it for independent technical review.
