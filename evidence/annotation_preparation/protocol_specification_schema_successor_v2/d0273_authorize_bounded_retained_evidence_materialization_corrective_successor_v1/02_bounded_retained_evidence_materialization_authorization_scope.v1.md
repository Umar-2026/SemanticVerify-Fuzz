# D0273 Bounded Retained-Evidence Materialization Authorization Scope

## Role

D0273 is an authorization-only corrective successor.

D0272 remains historically unchanged. D0272 originally designated D0273
as the separate branch-local positional adjudication execution.

Read-only readiness and auxiliary-artifact discovery subsequently
established that candidates 6, 8, and 9 do not have direct retained
semantic-unit text available in the frozen records permitted for that
adjudication.

D0273 therefore performs no positional adjudication and performs no
snapshot-content read.

It authorizes a separate D0274 transaction to materialize only the exact
already-frozen evidence units identified by the prebound locator universe.

## Exact candidate scope

- Candidate 6: 5 exact D0260 independently revalidated line-range locators.
- Candidate 8: 4 exact D0266 target locator records.
- Candidate 9: 1 exact D0266 target locator record.
- Total: 10 line-range locators.

No filtering, reselection, or new locator discovery is authorized.

## D0274 materialization boundary

D0274 may, only after D0273 independently passes its checkpoint:

1. Verify the exact frozen snapshot identity for candidates 6, 8, and 9.
2. Read each authorized frozen snapshot at most once.
3. Extract text only at the ten prebound line-range locators.
4. Record the exact extracted UTF-8 text and its SHA-256.
5. Verify candidate 8 and candidate 9 extracted-unit hashes against their
   already frozen D0266 extracted-unit hashes.

Candidate 6 has no previously retained extracted-unit hash; D0274 may
compute that hash during materialization.

D0274 is materialization only.

## Explicit prohibitions

D0274 does not authorize:

- full-snapshot semantic rereview;
- locator filtering;
- locator reselection;
- new locator discovery;
- reference following;
- original source-blob reopening;
- repository search;
- Git-history search;
- network access;
- execution of snapshot content;
- target-evidence rejudgment;
- positional adjudication;
- positional-status assignment;
- Class06 reclassification;
- sufficiency reselection or mutation;
- branch migration or cross-branch backflow;
- B2;
- analyzer;
- baseline;
- repair.

## D0275

D0275 is only a prospective later positional-adjudication checkpoint.

D0273 does not authorize D0275.

D0275 may not be authorized before D0274 executes, and may not execute
before D0274 has passed an independent verification/freeze checkpoint.
