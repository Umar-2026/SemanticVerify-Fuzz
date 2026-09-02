# Decision 0221 — Supersede Unexecuted Defective Decision0220 A02 and Author Tree-Binding-Safe Corrective-Revision Authorization Successor

Date: 02 September 2026

Status: D0220 A02 SUPERSEDED UNEXECUTED — TREE-BINDING-SAFE SUCCESSOR AUTHORED UNCONSUMED

## Source checkpoint

Decision0220 commit:

`57d84382ccdbe8784f06f33e9d99505192426c3a`

Decision0220 tree:

`dc9affb71e0b23c89f591e93997b842ffc90a528`

Decision0219 commit:

`f480347f329d89765db6a7d13d30ae6ebf929bb2`

Decision0219 tree:

`64ac36956e46d8307441ccef58b41f5ff4419303`

Returned re-review record tree:

`3e20186e0a4b674c326b0dbab3e380a16a256020`

Returned re-review SHA-256:

`8613f25eb8c971d6d38774ea7cd0ac97e8171f1e116854a843e3d346432b7618`

## Defective Decision0220 A02

SHA-256:

`d38ed4efd7db411d9feb303f60b1f467dc4d057c99df5d47b9488295f940abca`

The defect was identified before execution.

`EXECUTION_ATTEMPT_COUNT=0`

`EXECUTED=NO`

`CONSUMED=NO`

`SENTINEL_EXISTS=NO`

The verifier's parent-tree computation used `HEAD^{tree}`, which resolves to
the Decision0220 tree rather than the Decision0219 parent tree expected by the
check.

Decision0220 A02 is therefore:

`SUPERSEDED_UNEXECUTED`

and must never be executed.

## Fresh successor verifier

Decision0221 authors a fresh tree-binding-safe one-time verifier.

SHA-256:

`04200a09526bffec25d77702f877b9d21b4ed7da407976c9e4510284e7ee6d08`

Execution by Decision0221:

`NO`

Authorized future execution count:

`1`

First execution consumes the authorization permanently, PASS or FAIL.

Rerun is not authorized.

## Corrective scope

`ASER04,ASER07`

Preserved fresh PASS:

`ASER01,ASER02`

Preserved predecessor PASS:

`ASER03,ASER05,ASER06,ASER08,ASER09`

## Result boundary

`CORRECTIVE_SUCCESSOR_REVISION_AUTHORED=NO`

A later successfully authored revision remains `AUTHOR_CANDIDATE` and requires
independent human re-review.

## Explicit nonauthorization

No actual accounting evidence acquisition, U/C-domain acquisition,
forward/reverse witness acquisition, concrete mapping, accounting-satisfaction
determination, pair reclassification, active Schema-V2 modification, analyzer,
baseline, or repair work is authorized.

## Next step

`READ_ONLY_VERIFY_D0221_THEN_CONSUME_R03_EXACTLY_ONCE_IN_SEPARATE_D0222_AUTHORING_TRANSACTION`
