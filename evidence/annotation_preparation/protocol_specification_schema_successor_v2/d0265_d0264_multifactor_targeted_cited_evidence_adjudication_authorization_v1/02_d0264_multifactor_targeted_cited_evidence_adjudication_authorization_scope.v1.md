# D0265 — Bounded D0264 Multi-Factor Targeted Cited-Evidence Adjudication Authorization

## Role

D0265 is authorization only.

It designates D0266 as the sole execution step for a bounded targeted cited-evidence adjudication concerning D0264-verified multi-factor discrepancy candidates 8 and 9.

## Frozen input

The authorization is bound to frozen D0264 commit:

`28a2eb573c88bedd8a0f2b527814cfd8ebe8406e`

and to the exact D0264 primary result identity:

`45cfc7e3105120e9ede8eb74d54b987c3a57c0e3010eb4c8e028178d1990bf09`

D0264 independently verified candidate 8 and candidate 9 as `MULTI_FACTOR_DIVERGENCE`.

## Target locator universe

Exactly five pre-existing positive-evidence locators are bound:

- candidate 8: `L50-L50`
- candidate 8: `L51-L51`
- candidate 8: `L61-L61`
- candidate 8: `L84-L84`
- candidate 9: `L195-L195`

All are `LINE_RANGE`.

Canonical targeted-locator universe SHA-256:

`0be5087f66e27dce13ad2271ea69c8cce58441ef318ceb8c624b9c4ab0d30bea`

## Snapshot identity mapping

Candidate 8 is bound to:

- root: `DISCOVERY-ROOT-03`
- snapshot: `008.EXACT_BLOB_COPY`
- SHA-256: `c74240135454c6746b0829306d60c5a818c67d06a4148116de0f21891669a940`
- byte count: `5134601`
- raw Git blob OID: `336573866fc84ab4b4379ee4f331fb448252acfb`

Candidate 9 is bound to:

- root: `DISCOVERY-ROOT-03`
- snapshot: `009.EXACT_BLOB_COPY`
- SHA-256: `80cebe2423f5e7061012a550c262e7f3ca13898ab40b76c0288c90bc9e4a5b9c`
- byte count: `11346`
- raw Git blob OID: `03c709e75cb3ff738175198ad24b8074bbe6e70d`

Canonical targeted snapshot-mapping universe SHA-256:

`37bf22a6c4367a803802b8d3f66aea50fbf6e6784661d77f1bf7d9fe1534f06f`

## Authorized D0266 content boundary

After D0265 is independently verified and frozen, D0266 may read each of the two exact bound D0251 snapshots at most once, for a successful total of exactly two snapshot reads.

Those reads are authorized only for mechanical identity verification and extraction of the exact bound target locators from retained bytes.

D0266 is not authorized to semantically rereview the full snapshot or semantically inspect non-target snapshot regions.

## Blind targeted adjudication boundary

Before all locator judgments are durably recorded, the targeted adjudicator may receive only:

- candidate index,
- exact bound locator,
- extracted target evidence-unit text,
- the locked target-evidence question.

Prior source-record identity, prior result values, evidence-purpose labels, and prior rationales remain unavailable until the source-attribution gate opens.

## Non-establishment boundary

D0265 does not execute D0266.

D0265 does not select a final sufficiency value.

D0265 does not assign positional status.

D0265 does not reclassify Class06.

D0265 does not authorize successor-result-universe materialization, C4, C5, C6, or B2.

D0266 execution remains blocked until a separate independent read-only D0265 checkpoint establishes D0265 as verified and frozen.
