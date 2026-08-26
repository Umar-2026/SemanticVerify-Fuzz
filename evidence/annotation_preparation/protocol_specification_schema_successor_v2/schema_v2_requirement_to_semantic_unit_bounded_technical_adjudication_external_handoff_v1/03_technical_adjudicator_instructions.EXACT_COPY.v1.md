# Technical Adjudicator Instructions V1

## Role

The required role contract is:

`Spec-Technical-Adjudicator-1`

The actual adjudicator identity must be entered only by the human adjudicator.

## Scope

Adjudicate exactly the 211 candidate requirement-to-semantic-unit pairs
enumerated in the packet.

Do not add, remove, rank, merge, or substitute candidate pairs.

Each candidate pair currently remains `UNRESOLVED_BINDING`.

The recorded reviewer rationale and notes are source evidence only. They are
not an adjudication outcome and must not be accepted automatically.

## Allowed adjudication states

For each pair, select exactly one of:

`TECHNICAL_SUPPORT_CONFIRMED_PROMOTION_CANDIDATE`

Use only when the supplied governed evidence technically supports the proposed
requirement-to-semantic-unit binding strongly enough to become a candidate for
a later separately governed promotion decision.

This does not itself create `SUPPORTED_BINDING`.

`TECHNICAL_SUPPORT_NOT_ESTABLISHED`

Use when the supplied evidence is insufficient to establish the proposed
technical support.

The governed pair remains `UNRESOLVED_BINDING`. This state is not
`NOT_SUPPORTED_BINDING`, is not negative proof, and does not establish mapping
impossibility.

`TECHNICAL_ADJUDICATION_UNRESOLVED`

Use when the evidence cannot support a confident adjudication.

The governed pair remains `UNRESOLVED_BINDING`.

## Required per-pair completion

For every one of the 211 candidate pairs, complete:

- Technical adjudication state;
- Technical adjudication rationale;
- Technical adjudicator notes, if needed.

A confirmed-promotion-candidate state requires a substantive technical
rationale grounded in the supplied governed evidence.

## Human completion

After all 211 pairs are reviewed, complete the human technical-adjudicator
identity, role, confirmation/signature, date, and attestation fields.

## Governance boundary

This packet is a technical-adjudication evidence-acquisition surface only.

Completing it does not directly:

- reclassify a governed pair;
- create `SUPPORTED_BINDING`;
- create `NOT_SUPPORTED_BINDING`;
- create an operational mapping;
- modify Schema V2;
- authorize analyzer, baseline, or repair execution.

Any later promotion remains separately governed.
