# Decision 0185 — Authorize External Human Technical-Adjudication Handoff V1

## Decision

Authorize one separately governed successor transaction to author an external
human technical-adjudication handoff for the neutral 211-pair package created
by Decision0184.

Decision0185 is authorization only.

No external handoff is authored in Decision0185.

No human technical adjudication is performed in Decision0185.

## Bound Decision0184 package

The authorized handoff is bound to the immutable Decision0184 technical-
adjudication package containing exactly 211 candidate pairs.

The package contains:

- 211 unique candidate requirement-to-semantic-unit pairs;
- 211 governed prestates of `UNRESOLVED_BINDING`;
- zero prefilled technical-adjudication states;
- zero prefilled technical-adjudication rationales;
- zero prefilled adjudicator notes;
- no prefilled adjudicator identity.

The blank adjudication packet SHA-256 is:

`c135cd488c94be4aa94017c0684aa7a22993d9de923ff1ee3b5f389f40a7e6e0`

The required adjudicator role contract remains:

`Spec-Technical-Adjudicator-1`

## Authorized Decision0186 handoff

Decision0186 may:

1. execute Decision0185 A02 exactly once;
2. permanently retire that verifier after its single execution;
3. author an immutable internal handoff record;
4. create an immutable external ZIP containing the governed adjudication
   materials;
5. create exactly one external human-editable blank adjudication packet;
6. require that the initial editable packet be byte-identical to the internal
   blank packet;
7. include the adjudicator instructions and governed supporting evidence;
8. author checksum closure and a safe rerunnable handoff verifier;
9. author a separate Decision0186 handoff decision.

The only human-editable external surface may be the blank technical-
adjudication packet.

## Human-editable surface boundary

The author or model must not prefill:

- adjudicator name;
- adjudicator role completion;
- adjudicator signature or confirmation;
- adjudication date;
- adjudication state;
- adjudication rationale;
- adjudicator notes.

The author or model must not add, remove, rank, recommend, merge, or substitute
candidate pairs.

## Future human adjudication states

The external human adjudicator may later use only:

`TECHNICAL_SUPPORT_CONFIRMED_PROMOTION_CANDIDATE`

`TECHNICAL_SUPPORT_NOT_ESTABLISHED`

`TECHNICAL_ADJUDICATION_UNRESOLVED`

These are candidate technical-adjudication evidence states only.

They are not governed pair classifications.

A confirmed promotion candidate is not automatically `SUPPORTED_BINDING`.

A support-not-established result is not `NOT_SUPPORTED_BINDING`, is not
negative proof, and leaves the governed pair unresolved unless a later
separately governed decision establishes otherwise.

## Explicitly not authorized

Decision0185 and the authorized Decision0186 handoff transaction do not
authorize:

- performing human technical adjudication;
- recording a completed human technical-adjudication result;
- governed pair reclassification;
- automatic promotion of reviewer/adjudicator proposals;
- creation of `SUPPORTED_BINDING`;
- creation of `NOT_SUPPORTED_BINDING`;
- negative classification from lack of support;
- operational requirement-to-semantic-unit mapping;
- Schema V2 modification;
- a Schema V2 successor;
- `curl.json`;
- analyzer implementation;
- analyzer execution;
- baseline execution;
- repair implementation;
- repair execution.

## One-time verifier lifecycle

`02_verify_external_handoff_authorization_once.v1.py` is authored by
Decision0185 but must not be executed during Decision0185.

Its end-of-Decision0185 state must be:

`ACTIVE_UNCONSUMED`

Its only authorized execution transaction is Decision0186.

After the first authorized execution it becomes permanently retired and must
never be rerun.

## Next boundary

`CONSUME_DECISION0185_A02_EXACTLY_ONCE_AND_AUTHOR_EXTERNAL_HUMAN_TECHNICAL_ADJUDICATION_HANDOFF_V1`
