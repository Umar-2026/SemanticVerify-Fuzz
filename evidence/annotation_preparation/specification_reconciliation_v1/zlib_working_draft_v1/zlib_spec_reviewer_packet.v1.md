# zlib Source-Only Protocol Specification Review Packet V1

## Exact immutable review target

Author role: `Spec-Author-1`
Reviewer role: `Spec-Reviewer-1`
Reviewer underlying role: `Adjudicator-C`

Draft:

`evidence/annotation_preparation/specification_reconciliation_v1/zlib_working_draft_v1/zlib_source_only_working_fsm_draft.v1.json`

Draft SHA-256:

`cb2738329164537bba86282668bfabf51599fac1292309f150a68a32f2571573`

Pinned zlib revision:

`da607da739fa6047df13e66a2af6b8bec7c2a498`

This artifact is an author checkpoint only.
It is **not** a frozen protocol specification.

The reviewer must not consult generated fuzz drivers, selected-sample
membership, raw model responses, generated compiler-log semantic contents,
gold labels, analyzer output, baseline output, controlled LLM-review output,
repair output, or failure-prompted post-hoc evidence.

## Mandatory review checks

Record exactly `PASS`, `REVISION_REQUIRED`, or `FAIL`.

### 1. Evidence completeness

Decision: ____________________

Notes: _______________________

### 2. Transition consistency

Decision: ____________________

Notes: _______________________

### 3. Ownership effects

Decision: ____________________

Notes: _______________________

### 4. Terminal / permitted exit states

Proposed permitted exits:

- UNINITIALIZED
- INIT_FAILED
- RELEASED

Decision: ____________________

Notes: _______________________

### 5. Unsupported conditions and scope

Decision: ____________________

Notes: _______________________

## Candidate rule ZLIB-CAND-R14

Proposition:

`inflateCopy` destination should not already own a live inflate state before
copy because the pinned implementation allocates and assigns a new
destination state without releasing a prior destination state.

This candidate is intentionally outside the 13 core obligations pending
human review.

Choose exactly one:

- [ ] ACCEPT
- [ ] REJECT
- [ ] REVISION_REQUIRED

Reason:

____________________________________________________________

## Overall human-review decision

Choose exactly one:

- [ ] APPROVE_EXACT_DRAFT_FOR_FINALIZATION
- [ ] REVISION_REQUIRED
- [ ] REJECT

Reviewer role ID: `Spec-Reviewer-1`

Review date: ____________________

Signature / recorded human confirmation:

____________________________________________________________
