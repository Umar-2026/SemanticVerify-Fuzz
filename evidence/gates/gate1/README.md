# Gate 1 Evidence

Gate 1 establishes the specification foundation required by the authoritative
proposal. It does not authorize primary generation, held-out driver inspection,
analyzer implementation, or repair implementation.

Completed:

- Gate 1A: protocol-obligation schema, verdict contract, D1-D8 taxonomy,
  UNKNOWN limitation codes, provenance fields, and equivalent-path
  normalization contract.

- Gate 1B: positive-probability gold sampling, whole-driver blind annotation,
  third-party adjudication, agreement reporting, and per-driver exposure
  quarantine protocol.

- Gate 1C: exact source/build locks for all eight libraries.

- Gate 1 final freeze: system prompt, all 80 exact library-specific scenario bindings,
  deterministic user-message template, provider price snapshots, and independent-
  annotation role roster frozen; final Gate 1 manifest closed.

Library-specific protocol rules begin with zlib at Gate 2. The six held-out
protocol files must be frozen before their corresponding generated drivers are
opened or annotated; their scenario bindings are already frozen in the Gate 1
scenario manifest.


## Gate 1C exact source/build freeze

Status: **PASS**

All eight libraries have exact source identities and qualified reproducible
build recipes frozen in `config/library_source_build_lock.json`. Final qualification is 8/8 PASS.
Qualification logs and build metadata are persisted under
`evidence/gates/gate1/gate1c_source_build/`.

This gate does not authorize primary generation, held-out driver inspection,
analyzer implementation, or repair.
