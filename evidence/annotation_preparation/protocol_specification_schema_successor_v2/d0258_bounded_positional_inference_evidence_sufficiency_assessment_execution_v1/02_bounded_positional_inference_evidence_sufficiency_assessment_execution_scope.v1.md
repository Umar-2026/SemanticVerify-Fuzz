# D0258 bounded positional-inference evidence-sufficiency assessment execution

## Scope
This decision executes only the D0257-authorized evidence-sufficiency
assessment for frozen D0254 candidates 1,2,3,5,6,7,8,9,10.

Each exact frozen D0251 snapshot is read once for its primary D0258
assessment. Identity checks, decoding and bounded review use the same
in-memory bytes.

## Assessment boundary
The assessment answers only whether the current frozen snapshot contains
sufficient explicit information to support a later separately-authorized
positional-inference determination.

D0258 does not assign POSITIONAL_REQUIRED or POSITIONAL_NOT_REQUIRED.
It does not rejudge frozen D0254 requirement identity, semantic-unit
identity, explicit crosswalk, version/checksum, authority-basis, or
Class06 verdict fields.

## Conservative assessment rule
Pure SHA256SUMS snapshot content is insufficient when complete bounded
review confirms that the snapshot consists only of checksum/path reference
records, because reference following is prohibited.

For non-checksum artifacts, SUFFICIENT requires explicit within-snapshot
position/pairing/mapping or requirement-to-semantic-unit relation mechanism
evidence. In the absence of such strong explicit evidence, complex content
remains INDETERMINATE rather than being promoted to bounded negative proof.

## Prohibitions
No original source blob reopen.
No original candidate worktree content read.
No reference following.
No repository-wide source search.
No Git-history source search.
No network access.
No Python snapshot execution or import.
No cross-candidate content join.

## Governance
D0258 does not authorize C4, C5, C6 or B2.
D0258 results do not automatically authorize any post-assessment branch.
Independent D0258 verification is required next.
