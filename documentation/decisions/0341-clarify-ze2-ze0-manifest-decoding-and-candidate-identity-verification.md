# Decision 0341 — Record unresolved ZE2 ZE0-manifest decoding and candidate-identity verification provenance gaps

## Status

`CORRECTED_AUTHOR_CANDIDATE_NOT_EFFECTIVE`

This is the corrective D0341 author candidate after an independent pre-commit
review returned `REVISION_REQUIRED`.

The previous D0341 author candidate is not approved, is not effective, and
must not be committed.

The independent review recorded exactly two blocking findings:

- `D0341-PR-001 — UNSUPPORTED_NEW_DECODER_CONTRACT`
- `D0341-PR-002 — UNSUPPORTED_HASH_VERIFICATION_SUBSTITUTION`

This corrective candidate resolves those review findings by retracting the
unsupported assumptions. It does not claim that the underlying provenance
gaps themselves have been scientifically or operationally closed.

## D0341-PR-001 corrective resolution

The previous author candidate introduced two concrete ZE0
`representations` decoding forms even though pre-D0341 governance did not
establish those materialized JSON forms.

Those rules are withdrawn.

D0341 does not authorize or define:

- an object-key representation layout;
- an ordered-entry representation layout;
- a two-element-array representation layout;
- any guessed representation-value field name;
- any guessed representation-ID field name;
- recursive association discovery;
- position-only representation-ID inference;
- type-only representation-ID inference;
- regeneration of stored representation values from
  `schema_v2_property_path`;
- fallback decoding.

The exact materialized JSON sub-layout of
`record["representations"]` therefore remains:

`ZE0_REPRESENTATIONS_SERIALIZED_LAYOUT_STATUS=UNRESOLVED`

What remains frozen and established is only the existing D0323/D0326
contractual information:

- candidate records: `171`;
- representation forms per candidate: `7`;
- total stored representation values: `1197`;
- exact seven representation IDs;
- exact frozen representation order;
- frozen representation value types;
- every candidate record contains a `representations` member;
- all seven representation IDs are required in contract order;
- stored values must be preserved without scientific transformation.

These facts do not, by themselves, establish the concrete nested JSON
encoding used by the already-materialized ZE0 manifest.

No ZE2 implementation may guess that encoding.

`D0341_PR_001_RESOLVED=YES_BY_RETRACTION_OF_UNSUPPORTED_DECODER_RULES`

## D0341-PR-002 corrective resolution

The previous D0341 author candidate treated equality of the
manifest-carried field

`candidate_manifest_canonical_json_sha256`

with the frozen value

`c2746447215aa5aa2be0abea3bb631043eb0bb12745cc54309881d88a5a1f908`

as satisfying D0337 operation:

`VERIFY_ZE0_CANDIDATE_CANONICAL_SHA256`

That substitution is withdrawn.

Pre-D0341 governance establishes the frozen candidate canonical identity
value and establishes that D0325 independently enumerated the governed
candidate list for integrity verification.

The currently inspected governance does not establish a standalone exact
recomputation algorithm that may safely replace D0337's frozen operation
during ZE2.

Therefore:

`ZE0_CANDIDATE_CANONICAL_RECOMPUTATION_PROCEDURE_STATUS=UNRESOLVED`

The following remain true but are not sufficient to redefine D0337 step 3:

- expected candidate canonical SHA-256 is
  `c2746447215aa5aa2be0abea3bb631043eb0bb12745cc54309881d88a5a1f908`;
- candidate namespace is `SCHEMA_V2_PROPERTY_PATH`;
- candidate count is `171`;
- D0325 verified candidate ordinals exactly `1` through `171`;
- D0325 verified all property paths are strings and unique;
- the already-materialized ZE0 manifest stores the candidate canonical
  identity field.

No equality check against a manifest-carried field is declared equivalent to
the original frozen canonical-hash computation unless separately established
by governed provenance or prospectively amended by a later reviewed
checkpoint.

`D0341_PR_002_RESOLVED=YES_BY_RETRACTION_OF_UNSUPPORTED_HASH_SUBSTITUTION`

## Current ZE2 readiness consequence

The two independent-review findings against the previous D0341 candidate are
resolved at the author-candidate level because their unsupported rules have
been removed.

However, two underlying implementation provenance gaps remain:

1. `ZE0_REPRESENTATIONS_SERIALIZED_LAYOUT_STATUS=UNRESOLVED`
2. `ZE0_CANDIDATE_CANONICAL_RECOMPUTATION_PROCEDURE_STATUS=UNRESOLVED`

Therefore:

`ZE2_EXECUTION_GO=NO`

No irreversible ZE2 execution may begin while either gap remains unresolved.

## Frozen identities preserved

ZE0 full manifest SHA-256 remains:

`556096b6b6adc0708aee4903c5a4eb033231c04d7abe125d14f9dd5ad9760693`

ZE0 candidate canonical identity SHA-256 remains:

`c2746447215aa5aa2be0abea3bb631043eb0bb12745cc54309881d88a5a1f908`

D0340 remains effective and unchanged:

`candidate_index := exact stored candidate_ordinal`

No renumbering or record-position substitution is permitted.

D0336 representation compatibility, equality semantics, output schema,
serialization contract, occurrence ordering, and scientific interpretation
boundary remain unchanged.

## Authorization state

The original ZE2 authorization remains:

`SVF-D0337-ZE2-SINGLE-EXECUTION-AUTH-V1`

Current state:

`TOTAL_ZE2_EXECUTION_ATTEMPT_CAPACITY=1`

`ZE2_EXECUTION_AUTHORIZATION_CONSUMED=NO`

`REMAINING_ZE2_EXECUTION_ATTEMPT_CAPACITY=1`

D0341 adds:

`NEW_ZE2_EXECUTION_ATTEMPT_CAPACITY=0`

D0341 does not alter the D0337 one-shot consumption boundary and does not
authorize a retry after consumption.

## Scientific boundary

D0341 does not establish:

- representation overlap;
- semantic evidence;
- protocol support;
- semantic non-support;
- mapping;
- source-universe sufficiency;
- source-universe insufficiency;
- C4 satisfaction or C4 failure.

`REPRESENTATION_OVERLAP_ESTABLISHED=NO`

`MAPPING_ESTABLISHED=NO`

`C4_STATUS=UNRESOLVED`

`P8_MAPPING_AUTHORIZED=NO`

## Required next governance action

Before ZE2 may receive `GO`, a separate governance transaction must close both
remaining implementation-provenance gaps without guessing.

That future transaction must either:

1. establish exact pre-existing provenance for the missing serialized-layout
   and candidate-canonical verification procedures; or
2. explicitly design a prospective operational correction and subject it to
   full independent review before any scientific payload read.

D0341 itself does not choose between those routes.

## Corrective-authoring noninterference

During this corrective authoring:

`ZE0_SCIENTIFIC_PAYLOAD_READ_PERFORMED=NO`

`ZE1_SCIENTIFIC_PAYLOAD_READ_PERFORMED=NO`

`D0318_RAW_CANDIDATE_RECORD_READ_PERFORMED=NO`

`ZE2_RESERVED_OUTPUT_ROOT_TEST_PERFORMED=NO`

`ZE2_OUTPUT_WRITE_PERFORMED=NO`

`CANDIDATE_SOURCE_COMPARISON_PERFORMED=NO`

`REPRESENTATION_OVERLAP_PERFORMED=NO`

`ZE2_EXECUTION_PERFORMED=NO`

`ZE2_EXECUTION_AUTHORIZATION_CONSUMED=NO`

`GIT_ADD_PERFORMED=NO`

`COMMIT_PERFORMED=NO`

`PUSH_PERFORMED=NO`

## Activation

Corrective D0341 authoring alone is ineffective.

If independently approved, D0341 becomes effective only after:

1. independent pre-commit verification PASS;
2. exact local commit;
3. independent post-commit verification PASS;
4. publication of the exact reviewed commit to `origin/main`;
5. exact remote readback confirmation.

Even after D0341 becomes effective:

`ZE2_EXECUTION_GO=NO`

until both remaining provenance gaps are separately closed.

## Next action

`INDEPENDENT_PRE_COMMIT_VERIFY_CORRECTED_D0341_PROVENANCE_GAP_RECORD`
