# Decision 0039 — curl Canonical Representation Mapping Contract V1 Author Checkpoint

## Status

Exact approved curl Technical Working Draft V4 does not contain the
reference-style canonical-shaped candidate required by the proven zlib and
libpcap finalization precedent.

A positive V4-to-canonical mapping has **not** been silently invented.

This decision checkpoints the mapping-feasibility contract for independent
technical review.

## Exact contract

Path:

`config/annotation/curl_canonical_representation_mapping_contract.v1.json`

SHA-256:

`31d606f98f2c819291103ba7403214206ccde1d8e5e0e9103f0659c227622257`

Size:

`10879` bytes

After this checkpoint, exact V1 is immutable.

## Approved V4 binding

Exact approved V4 SHA-256:

`e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8`

Exact V4 size:

`41033` bytes

V4 remains immutable.

## Frozen canonical schema binding

Schema:

`config/schemas/protocol_specification.schema.json`

SHA-256:

`7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34`

The frozen schema requires a 15-field pre-freeze canonical core followed by
canonical finalization metadata.

## Corrected reference precedent

For both zlib and libpcap:

- a canonical-shaped candidate already existed before freeze;
- FSM states/events/transitions were not reconstructed during freeze;
- obligation semantics were not rewritten during freeze;
- only the field names `freeze_date` and `content_sha256` were added at
  canonical finalization, including obligation-level completion.

## curl V4 result

Exact V4 contains:

- 10 approved protocol-semantic containers;
- 12 API-surface functions;
- 5 resource components;
- 10 global-runtime rules;
- 21 easy-handle rules;
- 29 multi-handle rules;
- 4 cross-resource rules;
- 64 total frozen rule records;
- 3 exit obligations.

Exact V4 contains no reference-style 15-field canonical candidate.

It contains no canonical top-level:

- states;
- initial_state;
- events;
- transitions;
- obligations;
- permitted_exit_states;
- provenance.

Therefore construction of the current frozen canonical representation would
require additional representational decisions.

## Author conclusion

`LOSSLESS_V4_TO_FROZEN_SCHEMA_MAPPING_PROVEN=NO`

`CANONICAL_MATERIALIZATION_SAFE=NO`

`POSITIVE_MAPPING_ALGORITHM_AUTHORED=NO`

`curl.json CREATED=NO`

This is a conservative technical conclusion, not a human-review decision.

## Independent review requirement

Independent technical review must determine whether the negative feasibility
result is correct.

If the reviewer identifies a valid deterministic positive mapping, this V1
must remain immutable and a separately authorized successor mapping contract
must be created and reviewed.

If the current frozen schema cannot losslessly represent approved V4, any
canonical-schema successor requires separate authorization.

## Explicit non-authorization

This checkpoint does not authorize:

- curl.json materialization;
- generated-driver inspection;
- selected-sample membership inspection;
- gold annotation;
- analyzer implementation;
- analyzer execution;
- baseline execution;
- repair.

No assistant-generated or synthetic human approval is permitted.

## Next boundary

`BUILD_INDEPENDENT_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V1_REVIEW_PACKAGE`
