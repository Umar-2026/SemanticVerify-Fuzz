# Decision 0014: Blind Annotation Packet Contract and Role-Roster Start Guard

Status: Accepted

## Context

The primary 800-attempt corpus is complete, closed, frozen, and committed
before human inspection of generated driver source. The frozen gold-sampling
protocol makes only drivers with compilation_status COMPILED eligible for the
human-gold sampling frame. The completed corpus contains 487 eligible drivers,
so the preregistered gold draw is exactly 140.

The historical Gate-1 summary records
`role_roster_secured_claimed=false`. That historical evidence remains
immutable. The separately frozen role roster records researcher-attested
pseudonymous assignments for ANNOTATOR_A, ANNOTATOR_B, and ADJUDICATOR_C,
with all three marked real-human secured and eligible under the protocol.

This decision preserves both records rather than rewriting either one.

## Decision

1. The annotation sampling population is exactly the 487 frozen COMPILED
   logical attempts.
2. The gold sample size is exactly 140.
3. Primary strata remain library by model label; all sixteen strata are
   nonempty.
4. Allocation uses the frozen minimum-one capped proportional
   largest-remainder algorithm.
5. Within-stratum selection remains SHA-256 keyed ranking without replacement
   using master seed 2026080603.
6. Primary annotators must not receive provider/model identity,
   attempt/replicate identity, scenario/prompt information, analyzer output,
   baseline output, LLM-review output, or repair output.
7. Primary annotators may receive only complete anonymized selected driver
   source, library identity, and frozen approved protocol specifications and
   cited evidence.
8. The anonymization mapping remains separate from annotation packets.
9. Per-person per-driver exposure quarantine is mandatory.
10. Two independent primary annotations precede blinded union construction;
    both annotators independently label every union obligation before third
    adjudication.
11. Eligible in-scope human labels are VALID, VIOLATION-MUST, and
    VIOLATION-MAY. UNKNOWN is not a human-gold label.
12. This decision authorizes preparation and freezing of the sampling frame,
    deterministic draw, anonymization mapping, exposure registry, and packet
    generation.
13. This decision does not authorize human opening of generated driver source.
    A separate packet-release gate is required after all preparation artifacts
    are generated, verified, frozen, and committed.
14. Analyzer, baseline, LLM-review, and repair output remain quarantined until
    the gold freeze.

## No-backflow boundary

The 800-attempt generation corpus cannot be reopened or expanded. Failed
attempts are not replaced. Analyzer and repair implementation remain outside
this decision.
