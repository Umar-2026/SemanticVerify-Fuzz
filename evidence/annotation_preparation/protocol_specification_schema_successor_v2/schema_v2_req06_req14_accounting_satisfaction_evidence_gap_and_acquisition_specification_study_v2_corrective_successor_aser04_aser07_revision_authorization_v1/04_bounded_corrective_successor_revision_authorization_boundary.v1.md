# Decision0220 Bounded ASER04/ASER07 Corrective-Successor Revision Authorization Boundary V1

## Purpose

Decision0220 authorizes authoring of one new bounded corrective-successor
revision addressing only the two fresh re-review items still recorded as
`REVISION_REQUIRED`:

- `ASER04`
- `ASER07`

## Preserved PASS items

Fresh PASS items:

- `ASER01`
- `ASER02`

Preserved predecessor PASS items:

- `ASER03`
- `ASER05`
- `ASER06`
- `ASER08`
- `ASER09`

These items may be referenced only for non-regression and consistency.
They are not reopened.

## ASER04 authorized corrective target

The future successor revision may strengthen the future AEA01-AEA05
specification so that FC04 and domain/accounting controls become independently
recomputable.

Authorized specification work includes:

- requiring `source_container` where FC04 requires it;
- requiring `source_unit_kind` where FC04 requires it;
- binding those fields to frozen source-domain metadata;
- deterministic derivation of enumeration metadata including
  `source_unit_kind` and `source_provenance_sha256`;
- uniqueness constraints for source, candidate, forward, and reverse records;
- machine binding of `record_count`, coverage, membership, and dispositions;
- zero `UNRESOLVED` candidates before C-domain freeze;
- exact equality between frozen C and candidates marked `INCLUDED`;
- eliminating SHA-256 self-reference by a formal detached-hash or
  self-field-exclusion rule;
- completing numeric and string canonicalization.

These are future-acquisition specifications only.

## ASER07 authorized corrective target

The future successor revision may strengthen lineage and freeze controls by
requiring:

- formal constrained lineage fields for AEA03 and AEA04;
- complete freeze-event metadata;
- U-domain path and SHA-256;
- C-domain path and SHA-256;
- enumeration-source SHA-256;
- carrier-candidate-source SHA-256;
- a separate formal complete-freeze-record schema;
- checksum-bound independently recomputed verifier-output evidence for
  ancestry and immutable-domain checks;
- verifier command identity;
- evaluated commit identities;
- evaluated object hashes;
- verifier results;
- zero unresolved carrier candidates before freeze;
- exact equality between frozen C and `INCLUDED` dispositions.

No actual domain, freeze, relation witness, or mapping is created by this
authorization.

## Immutable predecessor boundary

Decision0213 corrective-successor artifacts remain immutable.

Decision0219 returned human re-review record remains immutable.

Reviewer identity fields, decisions, notes, attestation, and acknowledgement
must not be edited.

All correction must be authored as new successor artifacts.

## Status after future authoring

If later authored successfully under Decision0220 A02, the new corrective
successor revision will have status:

`AUTHOR_CANDIDATE`

It will require another independent human re-review.

Decision0220 does not authorize review-package creation, handoff, returned
review recording, or governance adoption.

## Explicit nonauthorization

`ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO`

`ACTUAL_SOURCE_UNIT_DOMAIN_ACQUISITION_AUTHORIZED=NO`

`ACTUAL_SCHEMA_CARRIER_DOMAIN_ACQUISITION_AUTHORIZED=NO`

`FORWARD_WITNESS_ACQUISITION_AUTHORIZED=NO`

`REVERSE_WITNESS_ACQUISITION_AUTHORIZED=NO`

`CONCRETE_MAPPING_CREATION_AUTHORIZED=NO`

`ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO`

`ACCOUNTING_SATISFACTION_ESTABLISHED=NO`

`PAIR_RECLASSIFICATION_AUTHORIZED=NO`

`PAIR_RECLASSIFICATION_PERFORMED=NO`

`ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO`

`ACTIVE_SCHEMA_SUCCESSOR_CREATION_AUTHORIZED=NO`

`SCHEMA_V2_LOSSLESSNESS_PROVEN=NO`

`CURL_JSON_AUTHORIZED=NO`

`GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO`

`GOLD_ANNOTATION_AUTHORIZED=NO`

`ANALYZER_AUTHORIZED=NO`

`BASELINE_AUTHORIZED=NO`

`REPAIR_AUTHORIZED=NO`

Current pair state remains:

- 211 `SUPPORTED_BINDING`;
- 1642 `UNRESOLVED_BINDING`;
- 0 `NOT_SUPPORTED_BINDING`;
- 218 Req06/Req14 pairs unresolved.

## One-time verifier lifecycle

Decision0220 A02 is authored by Decision0220 but not executed by Decision0220.

Its first later execution attempt consumes it permanently whether PASS or FAIL.

After that first attempt it must never be rerun.

## Next step

`CONSUME_DECISION0220_A02_EXACTLY_ONCE_AND_AUTHOR_BOUNDED_CORRECTIVE_SUCCESSOR_REVISION_FOR_ASER04_ASER07`
