# D0272 — Establish Positional Assignment Semantics and Redesignate Execution to D0273 Without Execution

## Decision

D0272 is a contract-only corrective successor.

D0271 remains historically unchanged. It authorized separate branch-local
positional inference adjudication for candidates 6, 8, and 9 and originally
designated D0272 as its execution decision.

Post-D0271 read-only recovery established that the frozen D0254 governance
contains the positional enum REQUIRED / NOT_REQUIRED / INDETERMINATE and
the Class06 verdict formula, but did not contain a general explicit rule
mapping frozen positional evidence to those three positional statuses.

Applying a newly authored assignment rule in the same transaction in which
it is first defined would lack an independently frozen semantic checkpoint.

Therefore D0272 establishes the missing bounded positional assignment
semantics without executing any candidate adjudication and prospectively
redesignates actual execution to D0273.

## Frozen semantic bindings

- D0254 positional enum SHA256: 5ca1d1cde7d044bf0588533afd1a254496625f70023afd608a90b7589d5ad807
- D0254 adjudication rubric SHA256: 97955b6553722b9562a0d71f33246de7dd7da231792638e77018692f1939f43c
- D0254 logic SHA256: e12fa090ce097613d06a4b396270fe60c82358b7f7f98893d35511a42639e14c
- D0254 positional AST bundle SHA256: c34e9554c367791b2ded02642db6d6ab3376943b4ba5133d63e57438a805046d
- D0254 status/verdict static bundle SHA256: 0a6bda85de87287a4f85572cfc5a73f326c5d26738f2c6c6b8b2e764370b5263
- D0253/D0254 positional rule-node bundle SHA256: 608e04171d3159fc2a905cf715cf98765c8fd811dd932e984256901648ed9691
- Prior positional contract discovery SHA256: 40d0a210457f589041d3be93c5470d0225573ced8685a9ad608bdb1fd1413e37
- Positional assignment static recovery SHA256: bd9a19b3a7a856c9db158966c2046371a8e04fff4ec76c7c0720be825d12e117

## Assignment semantics

NOT_REQUIRED requires explicit frozen admissible evidence establishing the
requirement-to-semantic-unit relation without reliance on positional,
ordinal, index, order, pairing, or equivalent positional inference.

REQUIRED requires explicit frozen admissible evidence establishing that the
relation under adjudication is realized through or depends on positional,
ordinal, index, order, pairing, or equivalent positional inference.

INDETERMINATE applies when neither status is explicitly established under
the frozen evidence, or the evidence supports conflicting interpretations.

The absence of an established non-positional crosswalk is not proof that
positional inference is required.

The mere presence of positional terminology is not sufficient to establish
REQUIRED.

## Execution boundary

D0272 performs no positional adjudication and assigns no positional status.

D0273 is the designated execution successor, but may not execute before
D0272 has passed an independent read-only verification/freeze checkpoint.

No D0251 snapshot content read, new evidence acquisition, Class06
reclassification, global positional materialization, B2, analyzer,
baseline, or repair authorization occurs here.
