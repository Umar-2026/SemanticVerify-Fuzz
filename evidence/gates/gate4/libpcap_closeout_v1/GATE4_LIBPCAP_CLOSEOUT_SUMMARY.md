# Gate 4 libpcap Validation Closeout

## Status

Gate 4 libpcap validation is closed with a negative validation result.

## Frozen evaluation frame

- Human-gold records: 420
- Eligible obligations: 268
- Out-of-scope exclusions: 152
- Gold positives: 0
- Gold negatives: 268

## Verifier result

- Scorable decided obligations: 0
- UNKNOWN obligations: 268
- Decision coverage: 0.000000
- UNKNOWN rate: 1.000000
- Policy-scored accuracy: 0.000000
- Policy-scored precision: 0.000000
- Sensitivity: not estimable because the gold set contains zero positive obligations
- libpcap F1: 0.000000

The result must not be interpreted as 268 conventional negative-class
misclassifications. The verifier produced no scorable decisions on the
eligible obligation set. The principal validation failure is therefore
zero decision coverage / complete abstention under the frozen policy.

## Limitation evidence

- U01_UNSUPPORTED_SEMANTICS: 175
- U02_UNRESOLVED_ALIAS: 1
- U05_MISSING_EVIDENCE: 40

## Claim discipline

- Confirmatory sensitivity claim: WITHHELD
- Superiority claim: WITHHELD
- Negative and UNKNOWN outcomes are preserved.
- No post-validation analyzer tuning is incorporated into this result.
- Baseline results were not accessed.
- Six-library held-out data were not accessed.

## Gate decision

GATE4_LIBPCAP_CLOSEOUT=COMPLETE
LIBPCAP_EFFECTIVENESS_RESULT=NEGATIVE_ESTABLISHED
