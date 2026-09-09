# D0294 — Activate Schema V2 as Canonical Protocol Representation

## Decision

D0294 activates Schema V2 as the canonical
protocol obligation representation for
SemanticVerify-Fuzz verification.

Schema V2 becomes the authoritative representation
for subsequent protocol verification stages.

No new evidence generation,
dataset modification,
result modification,
label modification,
or repair execution is performed.

## Parent Binding

D0293 structural protocol specification repair:

`<D0293_COMMIT>`

D0292 reviewer reproduction checklist:

`34612fb`

D0291 artifact availability statement:

`ef42d50`

D0290 publication evidence package:

`902b1b0`

## Activation Scope

Schema V2 activation applies to:

- obligation representation
- resource modeling
- protocol state representation
- defect type mapping
- verification input specification

Supported protocol specifications:

- zlib
- libpcap


## Forbidden Operations

The activation does not authorize:

- new evidence acquisition
- dataset mutation
- label modification
- result modification
- analyzer execution
- repair execution


## Activation Decision

SCHEMA_V2_ACTIVATED = YES

ACTIVE_VERIFICATION_USE = AUTHORIZED

MUTATION = NO
