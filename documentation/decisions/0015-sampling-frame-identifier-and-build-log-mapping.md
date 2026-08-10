# Decision 0015: Sampling-Frame Identifier and Build-Log Mapping

Status: Accepted

## Context

The frozen compilable-sampling-frame schema requires `attempt_id`,
`driver_id`, `driver_sha256`, and `build_log_sha256`. The primary generation
records predate construction of the gold sampling frame and do not serialize
fields named `attempt_id`, `driver_id`, or `build_log_sha256`.

The completed primary corpus already contains immutable identifiers and
integrity fields suitable for a deterministic additive mapping. Across all
487 COMPILED logical attempts:

- `logical_slot_id` is present, stable, and unique;
- `driver_source_sha256` is present and valid;
- `complete_log_path` and `complete_log_sha256` are present;
- every referenced compile-log file exists and its bytes hash to the recorded
  `complete_log_sha256`;
- the proposed mapping validates against the frozen sampling-frame schema for
  all 487 eligible records.

No driver source or compiler-log text was inspected to make this decision.

## Decision

For the primary human-gold compilable sampling frame, the following mapping is
frozen:

- `attempt_id = logical_slot_id`
- `driver_id = logical_slot_id`
- `driver_sha256 = driver_source_sha256`
- `build_log_sha256 = complete_log_sha256`

The equality of `attempt_id` and `driver_id` is intentional for this primary
corpus because each logical generation attempt denotes one candidate generated
driver. The immutable logical-slot identifier is used instead of inventing a
new post-hoc identifier before sampling.

The frozen sampling ranking therefore evaluates:

`SHA256("2026080603|" + driver_id)`

with `driver_id` equal to the pre-existing logical-slot identifier.

## Boundaries

This mapping is metadata-only. It does not change generation evidence,
compilation results, source bytes, log bytes, sampling strata, sample size,
seed, or selection algorithm.

This decision does not draw the 140-driver sample, create anonymization
packets, or authorize human inspection of generated source. Those operations
occur only after this mapping is committed and verified.

Analyzer and repair implementation remain prohibited at this boundary.
