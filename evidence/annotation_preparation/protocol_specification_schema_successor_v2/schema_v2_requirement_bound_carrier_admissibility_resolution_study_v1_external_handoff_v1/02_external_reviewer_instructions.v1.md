# External Independent Human Review Instructions — RBCA01-RBCA08

## Review target

`Schema-V2 Requirement-Bound Carrier Admissibility Resolution Study V1`

Author-candidate outcome:

`FURTHER_EVIDENCE_REQUIRED`

Required reviewer role:

`Spec-Technical-Reviewer-1`

## Files supplied

The external handoff consists of:

1. one immutable ZIP containing this handoff and the complete Review Package V1;
2. one separate editable manual reviewer packet initially byte-exact to the
   package-local blank RBCA01-RBCA08 packet.

## Reviewer procedure

1. Keep the supplied ZIP immutable.
2. Extract the ZIP to a new directory.
3. Run only:

   `python3 08_verify_external_RBCA01_RBCA08_handoff.v1.py`

4. Do **not** execute any file whose name contains a historical/pre-authoring
   `02_verify_*authoring_authorization*.py` A02 verifier.
5. Inspect `review_package_v1_exact/`, including its study artifacts and
   portable source evidence.
6. Independently assess RBCA01 through RBCA08.
7. In the separate editable manual reviewer packet, replace each decision
   placeholder with exactly one of:

   - `PASS`
   - `REVISION_REQUIRED`
   - `FAIL`

8. Choose exactly one overall decision:

   - `APPROVE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1`
   - `REVISION_REQUIRED`
   - `FAIL`

9. Add reviewer notes where appropriate.
10. Complete:

    - Human reviewer name
    - Human reviewer signature / recorded confirmation
    - Human reviewer date
    - Reviewer role (`Spec-Technical-Reviewer-1`)

11. Return only the completed editable reviewer packet for repository
    verification and later recording.

## Important boundaries

The author-candidate result under review is:

`FURTHER_EVIDENCE_REQUIRED`

The review does not automatically establish Schema-V2 losslessness, carrier
admissibility, positive mapping, negative mapping impossibility, or whole-V4
exhaustiveness.

The reviewer must not modify the immutable ZIP or repository-package blank
reviewer packet.
