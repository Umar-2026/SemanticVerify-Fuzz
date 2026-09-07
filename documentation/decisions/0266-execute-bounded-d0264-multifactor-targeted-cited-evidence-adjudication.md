# Decision 0266 — Execute bounded D0264 multifactor targeted cited-evidence adjudication

D0266 executes the D0265-authorized targeted adjudication for candidates 8 and 9.

Part A consumed the two authorized D0251 snapshot reads exactly once and extracted only the five bound target units. Blind adjudication was performed in a fresh isolated context using only the anonymized five-unit packet.

Part B durably ingested the five returned blind judgments, normalized only transport-inserted ASCII spaces inside the returned SHA-256 fields after exact text-hash verification, hashed the complete blind judgment record, opened the source-attribution gate only after all five judgments were durable, bound frozen source provenance, and applied the locked candidate aggregation formula.

Candidate 8 targeted positive evidence: TARGETED_POSITIVE_EVIDENCE_VALIDATED.
Candidate 9 targeted positive evidence: TARGETED_POSITIVE_EVIDENCE_VALIDATED.

No final sufficiency result is selected. No positional status is assigned. Class06 is not reclassified. No downstream operational branch is authorized by this decision.

The first required successor step is an independent read-only verification of D0266 without any D0251 snapshot reread.
