# D0272 Positional Assignment Semantics Corrective Successor Scope

## Role

D0272 is a contract-only corrective successor.

D0271 historically designated D0272 as the execution decision for the
S1 sufficient positional branch. Subsequent read-only recovery established
that the authoritative status enum existed, but a general explicit
assignment rule for REQUIRED / NOT_REQUIRED / INDETERMINATE had not been
frozen.

D0272 therefore does not execute positional adjudication.

D0272 prospectively redesignates the actual positional adjudication
execution decision to D0273, subject to an independent read-only
verification and freeze of D0272.

## Candidate scope

Only candidates 6, 8, and 9.

No branch membership change is authorized.

## Frozen status vocabulary

- REQUIRED
- NOT_REQUIRED
- INDETERMINATE

## Assignment semantics

NOT_REQUIRED requires frozen admissible evidence that explicitly
establishes the requirement-to-semantic-unit relation without reliance on
position, ordinal, index, order, pairing, or equivalent positional
inference.

REQUIRED requires frozen admissible evidence that explicitly establishes
that the requirement-to-semantic-unit relation under adjudication is
realized through or depends on position, ordinal, index, order, pairing,
or equivalent positional inference.

INDETERMINATE applies when the frozen admissible evidence does not
explicitly establish either of the above, or supports conflicting
interpretations.

Mere presence of positional terminology is not sufficient for REQUIRED.

Failure to establish a non-positional crosswalk is not proof that
positional inference is REQUIRED.

## D0272 prohibitions

D0272 does not:

- adjudicate candidates 6, 8, or 9;
- read D0251 snapshot content;
- acquire new evidence;
- reopen source blobs;
- follow references;
- rejudge frozen D0254 required criteria;
- mutate historical D0254 positional statuses;
- reselect or mutate sufficiency results;
- assign global positional status;
- reclassify Class06;
- touch candidates 1, 2, 3, 5, 7, or 10;
- authorize B2, analyzer, baseline, or repair;
- execute D0273.

## Next checkpoint

Independent read-only verification and freeze of D0272 is required before
any D0273 positional adjudication execution.
