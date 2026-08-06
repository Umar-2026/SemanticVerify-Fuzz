# Decision 0007: Gate 1A Obligation Schema and Normalization Freeze

- Status: Accepted
- Date: 2026-08-06
- Stage: Stage A — verification
- Gate: Gate 1A

## Decision

The project freezes the proposal-defined protocol representation
`P=(S,s0,A,delta,F,Omega)` and the primary normalized evaluation unit
`O=<driver,resource,rule,program-point-or-exit,abstract-context>`.

Raw CFG paths are retained only as evidence. They are merged when the normalized
obligation identity, abstract resource identity, required condition, observed
state set, and relevant branch-predicate class agree. Raw paths are never
independent statistical samples.

Eligibility is separate from verdict. The three base outcomes are VALID,
VIOLATION, and UNKNOWN; VIOLATION is quantified as MUST or MAY, producing four
serialized labels. UNKNOWN is never VALID and is incorrect on eligible gold
instances for the primary endpoint.

The D1-D8 proposal taxonomy, provenance fields, approved evidence classes,
prohibited pre-freeze inputs, and seven explicit UNKNOWN limitation codes are
frozen in `config/protocol_obligation_contract.json`. Two Draft 2020-12 machine-readable schemas freeze
the protocol-file and normalized-obligation record shapes.

## Boundary

This decision creates no library-specific protocol rule, system prompt,
scenario binding, generated driver, analyzer implementation, held-out
inspection, or repair implementation. Gate 1 remains in progress. Primary
generation remains unauthorized, and repair remains prohibited until Gate V.
