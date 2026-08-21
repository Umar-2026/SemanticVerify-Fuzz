# Decision 0019 / Schema V2 Activation Conflict Analysis

Decision 0019 SHA-256:

`50e273ecb6af838bc83d2499a2ed3a71607bc7c0cf8d74bd2622b56c2fefafa9`

Decision 0019 fixes the canonical root as:

`config/protocol_specifications/`

and requires a canonical artifact to validate against the **unmodified frozen
protocol-specification schema**.

The currently frozen V1 schema is:

`config/schemas/protocol_specification.schema.json`

SHA-256:

`7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34`

The independently approved Schema V2 candidate is:

`config/schemas/protocol_specification.v2.schema.json`

SHA-256:

`c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956`

Therefore simply calling V2 "active" while leaving Decision 0019 unchanged
would create an ambiguous or contradictory governance state.

The proposed resolution is not to edit Decision 0019 in place.

Instead, a later new decision must explicitly preserve Decision 0019 as
historical V1 governance and introduce deterministic schema-version dispatch:

- `schema_version = 1.0.0` → V1 schema + V1 hash contract;
- `schema_version = 2.0.0` → exact approved V2 schema + separately approved
  V2 hash contract;
- any unsupported or absent version → reject rather than guess.

This package only proposes that resolution for review. It does not enact it.
