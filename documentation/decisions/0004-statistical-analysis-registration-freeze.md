# Decision 0004: Statistical Analysis Registration Freeze

- Status: Accepted
- Date: 2026-08-06
- Stage: Gate 0E

## Frozen confirmatory analysis

- Primary endpoint: held-out library-macro obligation-level F1.
- Positive class: VIOLATION, pooling MUST and MAY for the primary endpoint.
- UNKNOWN is forced to the wrong binary label and cannot improve F1.
- Primary comparison: full verifier minus path-insensitive verifier.
- Resampling: 2,000 driver-cluster bootstrap replicates within library strata.
- Inference: two-sided alpha 0.05, percentile 95% confidence interval, effect sizes.
- Planned ablations use Holm family-wise multiplicity adjustment.
- Precision must be at least 0.80 and decision coverage at least 0.75.

## Frozen sparse-outcome rules

- Fewer than 30 positive obligations or five positive libraries withholds
  confirmatory sensitivity and superiority claims.
- Categories with fewer than 10 positives receive counts and exact intervals only.
- No post-hoc sample expansion and no generation to obtain desired defects.

## Frozen power evidence

- 144 scenarios cover prevalence 5-20%, combined ICC 0.01-0.10, detector
  discordance 5-20%, and 4/8/12 eligible obligations per driver.
- 61 scenarios reached both conditional and claimable 80% MDI.
- In the central 12-obligation scenario, a 0.10 positive-sensitivity gain produced
  median macro-F1 difference 0.069727 and claimable power 0.8865.
- Non-reached scenarios are informative and narrow claims; they do not change the
  fixed generation or annotation budgets.

## Provenance

- Pre-simulation registration SHA-256: `8a26244a7be384ce58d1a11f7365054998fd92d4c5b496e07d7b3dfa3d2a7144`
- Active frozen registration SHA-256: `c7537ce5d082de904cc7aef4d617c9ff6612b30fdb4740b0667c9eb84ca5b2d4`
- Power report SHA-256: `bb746da67ccdae2eeda232aba36c53ba53ec3d7830fdd726bb4f450aa2ab9b58`
- Simulation script SHA-256: `15dd19839d8bea03a7e5e9a755ea4fa862b937f399a0f1d43548f886be8555b1`
- Read-only verifier SHA-256: `5d661f1351d188c0f027a3cd98566fa34f6f15d344444378be0c777dd1323f76`
- Freeze-preparation script SHA-256: `7180ff2ac119e4e8c41bfbc173c9e5fefaa0039d85918a0ded8ea77978d67442`

Primary generation remains unauthorized. Driver inspection remains unauthorized.
Repair implementation remains prohibited until Gate V.
