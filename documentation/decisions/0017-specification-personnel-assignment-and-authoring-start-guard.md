# Decision 0017: Specification Personnel Assignment and Authoring Start Guard

Status: Accepted

## Personnel assignment

The project assigns the following two distinct real-human roles for the
source-only specification reconciliation established by Decision 0016:

- `Spec-Author-1`: specification author and current project researcher.
- `Spec-Reviewer-1`: specification reviewer, mapped to the already secured
  human role `Adjudicator-C`.

The specification author and specification reviewer are distinct people.

`Annotator-A` and `Annotator-B` are not reused as specification personnel.

The reuse of `Adjudicator-C` as `Spec-Reviewer-1` is explicit and recorded.
It is not a silent role substitution. The reviewer remains distinct from the
specification author.

## Why the adjudicator/reviewer overlap is permitted

The frozen recovery protocol requires a specification author and a distinct
second reviewer. It does not require the second reviewer to be distinct from
the later third adjudicator.

All human annotation roles will ultimately receive the same frozen approved
protocol specification as annotation evidence. Therefore prior participation
in specification review does not provide the reviewer/adjudicator with
machine-output information unavailable to the annotation process.

This overlap does not permit the reviewer to inspect generated drivers before
the separate annotation packet-release gate.

## Source-only restriction

Specification authoring and review may use only the source classes permitted
by Decision 0016 and the frozen Gate-1A provenance contract:

1. pinned official API documentation;
2. public headers at the pinned revision;
3. pinned implementation source;
4. pinned upstream tests;
5. predeclared upstream usage examples.

Generated experimental drivers, raw model responses, gold labels, analyzer
output, baseline or QuartetFuzz output, controlled LLM-review output, repair
output, defect-triggering mutations, and outcome-prompted issue searches remain
prohibited as specification evidence.

## Start authorization

After this decision and the associated personnel start guard are committed,
library-specific specification authoring is authorized under the source-only
reconciliation protocol.

This authorization is additive. It does not modify the previously frozen
recovery contract or its historical pre-guard `author_library_specifications =
false` state.

The authorization covers specification authoring and independent review only.

It does not authorize:

- generated-driver human inspection;
- gold annotation;
- annotation packet release;
- analyzer implementation;
- baseline execution;
- controlled LLM review;
- repair implementation.

## Final specification-freeze condition

All eight library specifications must:

- use the frozen pinned library revisions;
- satisfy the frozen protocol-specification schema;
- contain complete rule-level provenance;
- contain content hashes;
- be authored by `Spec-Author-1`;
- be independently reviewed by `Spec-Reviewer-1`;
- record the required five reviewer checks;
- freeze before any selected generated-driver source is released to humans.

This personnel assignment is a start guard only. It is not final reviewer
signoff on specifications that do not yet exist.
