# D0273 — Authorize Exact Bounded Retained-Evidence Materialization in D0274 and Defer Positional Adjudication to D0275 Without Execution

## Decision

D0273 is an authorization-only corrective successor.

D0272 remains historically unchanged. D0272 had designated D0273 as the
separate positional-adjudication execution checkpoint.

Subsequent read-only audits established that candidates 6, 8, and 9 do not
have direct retained semantic-unit text in the frozen record universe
available for that execution.

The exact corrective locator universe has now been bound:

- locator-universe SHA256: 057f93353c5055da5a13e6af04b0c8413dd9bddb9b6afe1624b2c55a929945ec
- snapshot-metadata universe SHA256: d389c7df9ac5936f6ef1c0bbed80051edb386c9872d3b11494cd2f5ed0550ec9
- candidate 6 locator-list SHA256: 2f98d935ffb35c7bb9cb6befdbd3b51f604217eb008ad41925aafaab98a8307e
- candidate 8 locator-list SHA256: 65760e94b75ed5748d2ecfd624f1c7148028cef720cffbd3341b008152f1c4cf
- candidate 9 locator-list SHA256: 0b9fcaf16df5da5afb45fbe2c6b5a5a85405620a8317c9c7d465b68bb548ffa8

Candidate 6 uses exactly five D0260 independently revalidated evidence
references in recorded order.

Candidate 8 uses exactly four D0266 target locator records in recorded
order.

Candidate 9 uses exactly one D0266 target locator record in recorded order.

No filtering, locator reselection, or new locator discovery occurred.

## D0274 authorization

D0273 authorizes D0274 to perform bounded retained-evidence materialization
only after D0273 independently passes its verification/freeze checkpoint.

D0274 may verify each exact frozen snapshot identity, read each of the
three authorized frozen snapshots at most once, and extract only the ten
prebound line-range evidence units.

D0274 may record exact extracted text and SHA-256 values.

For candidates 8 and 9, D0274 must verify the extracted-unit hashes against
the already frozen D0266 hashes.

For candidate 6, D0274 computes the extracted-unit hashes because those
exact unit hashes were not previously retained.

## Prohibitions

D0273 itself performs no snapshot-content read and no materialization.

Neither D0273 nor D0274 authorizes positional adjudication, positional
status assignment, Class06 reclassification, sufficiency mutation, branch
migration, B2, analyzer, baseline, or repair.

## D0275

D0275 is only the prospective later positional-adjudication checkpoint.

D0273 does not authorize D0275.

D0275 may not be authorized before D0274 executes and may not execute
before D0274 has passed an independent verification/freeze checkpoint.
