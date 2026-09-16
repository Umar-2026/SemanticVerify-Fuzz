# Zlib Annotation Protocol

## Objective

Validate whether automatically detected API protocol violations
are supported by extracted execution traces.

## Annotation Unit

One generated fuzz driver corresponds to one annotation unit.

## Labels

### CONFIRMED_VIOLATION

The execution trace clearly violates the API protocol.

### FALSE_POSITIVE

The verifier reports a violation, but the trace does not violate
the protocol.

### UNCERTAIN

Available evidence is insufficient for a reliable decision.

## Annotation Evidence

Annotators inspect:

1. API call sequence
2. Resource lifecycle
3. FSM transition
4. Violated rule
5. Source code location

## Adjudication

Disagreements are resolved through discussion and final review.
