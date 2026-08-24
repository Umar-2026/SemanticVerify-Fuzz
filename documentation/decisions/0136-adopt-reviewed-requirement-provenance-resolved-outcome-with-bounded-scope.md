# Decision 0136 — Adopt Reviewed REQUIREMENT_PROVENANCE_RESOLVED Outcome with Bounded Scope

## Status

BOUNDED GOVERNANCE ADOPTION COMPLETED

## Authorization checkpoint

Decision-0135 commit:

`92d745dd3186ef8a528196976b283f75d7bd43b8`

Decision-0135 tree:

`f1448fee627388b1cbf6857af4e891c320c4d6c8`

Decision-0134 parent:

`f36cd77ead4ee4f154b4bc7cfa2b88ce963a05d9`

Study V1 Git tree:

`ee85980dcff85b5be3f21995f578b3b78cf39aa2`

Completed Human Review V1 Git tree:

`d873ef00dceb359a2dc8dc25293ab8ec57518dd2`

Governance-Adoption Authorization V1 Git tree:

`8c62c8ec31bc4f6c4a3c0a6940d05f6e80349d79`

## Independent-review basis

The completed RPR01–RPR08 independent human review records:

- RPR01: `PASS`
- RPR02: `PASS`
- RPR03: `PASS`
- RPR04: `PASS`
- RPR05: `PASS`
- RPR06: `PASS`
- RPR07: `PASS`
- RPR08: `PASS`

Overall decision:

`APPROVE_V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1`

No reviewer decision is synthesized by this adoption step.

## Adopted governance result

The project governance now adopts:

`REQUIREMENT_PROVENANCE_RESOLVED`

strictly within:

`REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY`

The governed result is:

- existing V4 losslessness requirements: `17`;
- `BOUND_EXACT = 17`;
- `BOUND_COMPOSITE = 0`;
- `UNRESOLVED = 0`.

The identities and immutable source provenance of the existing 17 V4
losslessness requirements are therefore now a reviewed and governance-adopted
basis for subsequent bounded technical work.

## Study artifact immutability

Study V1 itself remains immutable.

This decision does not rewrite Study V1's historical author-candidate bytes.
Governance adoption is represented by this new successor adoption record.

## Decision-0135 A02 lifecycle

Final result:

`PASS`

Final-output SHA-256:

`fcc9533c9372ab597b2f159cffd82bc81b513fcdaa810b98056988a1389b6160`

Final-output size:

`1026`

State after its one permitted run:

`PERMANENTLY_RETIRED`

It must never be rerun.

No previously retired A02 verifier was executed.

## Technical nonclaims preserved

This governance adoption does **not** establish:

- Schema-V2 losslessness;
- semantic-unit/carrier admissibility;
- a positive existing-Schema-V2 mapping;
- negative existing-Schema-V2 mapping impossibility;
- whole-V4 admissible-composition exhaustiveness.

## Operational nonauthorizations preserved

This decision does not authorize:

- semantic-unit/carrier pair reclassification;
- modification of the existing 18,639-pair state;
- carrier-admissibility conclusions;
- positive mapping;
- negative mapping impossibility;
- whole-V4 exhaustiveness;
- operational mapping;
- active Schema-V2 modification;
- schema-successor authoring;
- schema-version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution;
- repair.

## Next technical boundary

The requirement-identity/source-provenance blocker is now governance-resolved.

Any further work must be separately authorized.

The next eligible technical step is a bounded successor study that uses the
reviewed 17 requirement identities and their immutable provenance to resolve
the still-open semantic-unit/carrier admissibility question without silently
changing prior pair classifications or asserting a mapping conclusion.

## Next boundary

`SEPARATELY_AUTHORIZE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_SUCCESSOR_STUDY`
