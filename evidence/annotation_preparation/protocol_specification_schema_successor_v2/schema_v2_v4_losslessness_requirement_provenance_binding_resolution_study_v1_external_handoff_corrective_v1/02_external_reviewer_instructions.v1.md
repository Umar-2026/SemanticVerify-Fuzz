# External Independent Human Review Handoff — RPR01–RPR08

## Review subject

V4 Losslessness Requirement Provenance and Binding Resolution Study V1

## Required reviewer role

`Spec-Technical-Reviewer-1`

## What the reviewer must do

1. Extract the immutable ZIP into a normal local directory.
2. Run:

   `python3 08_verify_corrective_external_handoff_v1.py`

3. Review the immutable evidence under:

   `review_package_v1_exact/`

4. Complete only:

   `03_RPR01_RPR08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md`

5. Give an independent decision for each of RPR01 through RPR08.
6. Select exactly one overall decision from the options already present.
7. Fill reviewer name, initials, review date, and reviewer role.
8. Return the completed manual reviewer packet.
9. Do not modify any immutable review evidence.

## Corrective-governance note

A previous pre-handoff verifier failed because it incorrectly required the
current handoff-authoring HEAD to equal the Decision-0129 checkpoint.

That failed verifier was retired permanently without handoff authoring.

The corrective authorization and its exact failure evidence are included for
auditability. The failure did not falsify Review Package V1 or Study V1.

## Interpretation boundary

`REQUIREMENT_PROVENANCE_RESOLVED` means only that the existing 17
losslessness-requirement identities and their immutable source provenance
were resolved.

It does not prove:

- a positive existing-Schema-V2 lossless mapping;
- impossibility of such a mapping;
- semantic-unit/carrier admissibility;
- whole-V4 admissible-composition exhaustiveness; or
- operational authorization.

## Author noninterference

No RPR decision, reviewer identity, reviewer note, or overall reviewer
decision has been prefilled or synthesized.

All reviewer judgments must be independent.
