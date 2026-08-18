# Decision 0027: curl Technical Protocol Working Draft V1 Author Checkpoint

## Status

Created the first source-grounded curl technical protocol working draft after
completion of the exact V3 source-only authoring-scope freeze and the separate
post-freeze working-draft authorization.

This is an immutable **author checkpoint**, not a canonical protocol
specification.

## Working draft

Path:

`config/annotation/curl_technical_protocol_working_draft.v1.json`

SHA-256:

`80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6`

## Governing frozen scope

V3 scope SHA-256:

`ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`

V3 original author commit:

`7de6fc01797ae68cbd64406b850a3198f71cc702`

V3 original author tree:

`c5f96b844e5803cccd04c9f64a55754dc6c77e20`

V3 Git blob:

`931c24cc46c99f23ee352455d3e8c93e57e63401`

Separate V3 scope-freeze commit:

`0992b2ae03702e29471d59f192daf43a8924314d`

Separate post-freeze working-draft authorization commit:

`cb864ac93023ee288343b8bcdc0267b07dc28114`

## Source basis

Pinned curl revision:

`68720b4837284335b2d63cb358f8f6ce65f5bc55`

Pinned curl source tree:

`e23d273aeb073c04aa5b073b35c9fde16979c896`

All 21 previously approved source-evidence hashes were verified before
authoring.

## Technical structure

The working draft models:

- global runtime readiness;
- explicit global-cleanup obligation;
- easy-handle lifetime;
- multi-handle lifetime;
- easy-to-multi membership;
- return-conditioned transitions;
- post-`curl_multi_perform` error uncertainty;
- exit cleanup obligations;
- four verdicts: VALID, VIOLATION-MUST, VIOLATION-MAY, UNKNOWN.

## Conservative review boundary

The working draft explicitly retains unresolved normative-strength questions
as review items rather than silently strengthening them.

In particular, the draft does not pre-decide:

- MUST-vs-MAY strength of missing explicit global cleanup;
- unconditional MUST status for the complete multi-cleanup ordering sequence;
- MUST-vs-MAY classification of plain multi-perform repetition after error;
- certain additional implementation-derived state/classification questions
  listed as NR04 through NR06.

## Canonicalization state

- technical working draft created: YES;
- technical working draft canonical: NO;
- independent technical-specification review completed: NO;
- canonical curl specification authorized: NO;
- generated-driver inspection authorized: NO;
- gold annotation authorized: NO;
- analyzer implementation authorized: NO;
- baseline execution authorized: NO;
- repair authorized: NO.

## Immutability

This V1 working-draft author checkpoint must not be edited in place after it
is handed to independent technical review.

If technical review requires semantic revision, create an immutable successor.

## Next boundary

Build an independent human technical-specification review package bound to
the exact working-draft V1 bytes and resulting author-checkpoint commit/tree.
