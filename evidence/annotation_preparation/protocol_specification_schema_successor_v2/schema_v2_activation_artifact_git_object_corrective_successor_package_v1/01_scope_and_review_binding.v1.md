# AF04/AF07/AF08/AF09 Portable Raw-Git-Object Corrective Successor Package V1

## Status

EVIDENCE-ONLY REVIEW CANDIDATE — NO ACTIVATION

## Authority

Decision 0063 authorizes this package solely to address the evidence
deficiencies recorded for AF04, AF07, AF08, and AF09.

Authorization SHA-256:

`c8725561b71ecc72fb0d5da93b968eed70c4d7948a83baa2dd28eff66d045f8e`

Decision-0063 commit:

`c24976218895e2a90d61cabefacdbb66b2f7d550`

## Closed items

AF01, AF02, AF03, AF05, AF06, and AF10 remain PASS and are not reopened.

## Corrective evidence

This package exports original raw Git commit, tree, and blob object contents
from historical checkpoint:

`fa64f7810443d14cd710600cd48ae9f9fedbb04a`

and its exact parent:

`6eba8a1fc69c0b1146e033b031f5948a245bd84b`

The package includes a repository-independent verifier that recomputes Git
object IDs, parses raw binary tree objects, verifies the commit-parent
relationship, resolves relevant paths through the exported Merkle trees,
proves required path absences, verifies core-artifact blob identity, and
reconstructs the exact 22 changed leaf paths.

## No semantic revision

This package does not revise the reviewed version-dispatch transformation or
the reviewed Decision-0019 successor transformations.

## No activation

This package does not install the V2 hash contract, install version dispatch,
activate Schema V2, adopt the Decision-0019 successor, define or authorize
positive V4-to-V2 mapping, create curl.json, authorize analyzer implementation
or execution, authorize baseline execution, or authorize repair.
