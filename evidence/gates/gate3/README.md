# Gate 3 — libpcap Candidate and Human-Gold Freeze

## Formal status

- Final human-gold freeze: ESTABLISHED
- Candidate freeze: ESTABLISHED
- Gate 3: COMPLETE
- Ready for Gate 4: YES
- Analyzer executed on libpcap validation sample: NO
- libpcap validation executed: NO
- Paper effectiveness result established: NO

## Human-gold frame

- Total logical driver-rule records: 420
- PRESENT / IN_SCOPE: 268
- ABSENT / OUT_OF_SCOPE: 152
- VALID human verdicts: 268
- Human-confirmed violations: 0
- Null verdicts: 152

Construction:

- A/B agreed records: 392
- Adjudicated records: 28
- Final records: 420

## Frozen identities

FINAL_HUMAN_GOLD_RECORDS.jsonl
SHA-256:
200bc55afc7267be4c166ae7b51d4c9fb6b9aafb733bd8f55b70aa4a1483e3a7

FINAL_HUMAN_GOLD_SUMMARY.json
SHA-256:
2562e698e4f03b588a1b6d47199de82b01cebcb6c81e430db25336ba7d8a205a

FINAL_HUMAN_GOLD_FREEZE_MANIFEST.json
SHA-256:
844d61deddcadf0d457cdb312f7f2d44c19483d8a908d6af7eeb2a3ecac0fcb0

GATE3_CANDIDATE_FREEZE_CLOSEOUT.json
SHA-256:
20e145838f17d7777191237b5be50510cdc01120fa70731c6b875f6a67180389

## Scientific boundary

The frozen libpcap human gold contains no human-confirmed
protocol violations among the 268 eligible obligations.

Therefore, this validation sample can evaluate false-positive
behaviour, preservation of VALID obligations, UNKNOWN behaviour,
decision coverage, and mismatch causes, but it cannot independently
estimate violation-class recall or violation-class F1.

## Repository exclusion boundary

This checkpoint intentionally excludes:

- PRIVATE_DISAGREEMENT_CASES.json
- raw Annotator-A archive
- raw Annotator-B archive
- adjudicator receipt containing human identity
- private mappings
- analyzer outputs
- Gate-4 validation results

No Gate-4 analyzer execution occurred while creating this checkpoint.
