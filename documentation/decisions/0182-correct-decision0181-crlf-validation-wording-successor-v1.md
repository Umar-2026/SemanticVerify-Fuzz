# Decision 0182 — Correct Decision0181 CRLF Validation Wording Successor V1

## Decision

Record a documentation-only successor correction for one malformed explanatory
passage in Decision0181.

Decision0181 itself remains immutable and is not edited.

## Predecessor binding

This successor applies only to:

`documentation/decisions/0181-record-completed-human-positive-binding-evidence-packet-v1.md`

at Decision0181 commit:

`831c6cf7dd51745a67e07a724d1a35b76f9eb6fd`

with Decision0181 file SHA-256:

`dabebaa4898ba3e07c289e585e4e98ea95a3c4006d04d70c472d1d577570fa47`

and size:

`4424` bytes.

## Documentation defect

During authoring of the Decision0181 CRLF-preservation explanation, shell
command substitution consumed two Markdown inline-code literals from an
unquoted heredoc.

The committed Decision0181 passage therefore states:

> only, staged whitespace validation uses the non-persistent command-local Git
> interpretation . All other Decision0181 artifacts
> remain subject to the ordinary  validation.

This is a documentation-generation defect only.

It does not alter the commands that were actually executed, the recorded
evidence bytes, the checksum closure, the safe verifier result, or the
Decision0180 A02 lifecycle.

## Corrected authoritative wording

For interpretation of Decision0181, the malformed passage above is superseded
only by the following wording:

> For this exact-copy artifact only, staged whitespace validation uses the
> non-persistent command-local Git interpretation
> `core.whitespace=cr-at-eol`. All other Decision0181 artifacts remain subject
> to the ordinary `git diff --check` validation.

The actual CRLF-aware staged validation performed during Decision0181 was:

`git -c core.whitespace=cr-at-eol --no-pager diff --cached --check -- <exact-copy-R02-path>`

and it returned PASS.

No persistent Git configuration was modified.

## Recorded-evidence integrity preserved

The recorded exact-copy human evidence packet remains:

SHA-256:

`effd2848702219741e3814d2dc283284c92ab07f49980cd799fde351ecb8b685`

Size:

`20425` bytes.

Its line endings remain the authorized CRLF bytes.

No normalization, rewriting, or reviewer-evidence modification is authorized
or performed by this successor.

## Decision0180 A02 lifecycle preserved

Decision0180 A02 was executed exactly once in Decision0181.

Its state remains:

`PERMANENTLY_RETIRED`

Its rerun authorization remains:

`NO`

Decision0182 does not execute or authorize execution of that verifier.

## Semantic and governance effect

This successor changes documentation interpretation only.

It does not:

- reclassify any requirement-to-semantic-unit pair;
- adjudicate any reviewer proposal;
- create `NOT_SUPPORTED_BINDING`;
- convert an unresolved proposal into negative proof;
- create an operational mapping;
- modify Schema V2;
- authorize a Schema V2 successor;
- authorize `curl.json`;
- authorize analyzer implementation or execution;
- authorize baseline execution;
- authorize repair implementation or execution.

The Decision0181 evidence-recording result remains valid and unchanged.

## Successor relationship

For the CRLF-validation explanatory wording only:

`Decision0182` supersedes the malformed Decision0181 passage.

For all other Decision0181 content and semantics:

`Decision0181` remains authoritative and unchanged.

## Next boundary

`SEPARATELY_ASSESS_TECHNICAL_ADJUDICATION_OF_RECORDED_CANDIDATE_POSITIVE_BINDING_EVIDENCE`
