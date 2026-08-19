# curl Technical Protocol Working Draft V4 — Independent Human Review Packet

## Purpose

This packet is for independent human technical review of exact immutable
curl Technical Protocol Working Draft V4.

Working Draft V3 received overall decision `REVISION\_REQUIRED`.

V4 is a metadata-only immutable successor addressing V3-RR02 and V3-RR12.
Accepted V3 protocol-rule semantics must remain unchanged.

No canonicalization may occur unless exact V4 receives the required independent
human approval and a later separate canonicalization authorization.

## Exact review target

Working draft:

`03\_curl\_technical\_protocol\_working\_draft.v4.json`

SHA-256:

`e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8`

Size:

`41033` bytes

Author checkpoint commit:

`b98d76536376b21fc6f2e85a060e960e1681453c`

Author checkpoint tree:

`e7243cda2f8afd9b6cceff793ab0cfa723fabbe5`

## Evidence boundary

Permitted evidence:

* exact V4;
* exact immutable V3 predecessor;
* completed V3 independent human review;
* Decisions 0034, 0035, and 0036;
* V4 successor authorization;
* V4 author-resolution record;
* V4 metadata-successor traceability;
* V4 author-checkpoint record;
* frozen source-only scope;
* exactly 21 approved pinned curl source files;
* minimal V4 author-checkpoint Git witness;
* the self-contained V4 package verifier.

Not permitted:

* generated drivers;
* selected-sample membership;
* raw model responses;
* generated-driver compiler-log semantic content;
* gold labels;
* analyzer output;
* baseline output;
* LLM-review output;
* repair output.

## Decision choices

For every V4-RR item enter exactly one:

`PASS`

`REVISION\_REQUIRED`

`FAIL`

If revision is required, state the precise required change.

\---

### V4-RR01 — Exact V4 identity, author checkpoint, and immutable V3 predecessor

Decision: PASS

Notes: Exact V4 file size is 41033 bytes.

Exact V4 SHA-256 is:

e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8

The supplied author commit independently hashes to:

b98d76536376b21fc6f2e85a060e960e1681453c

The author commit declares tree:

e7243cda2f8afd9b6cceff793ab0cfa723fabbe5

The reconstructed root tree independently hashes to the same declared tree.

The root → config → annotation path resolves to V4 Git blob:

c7bafecdf8d35395f183f8551e1318ebb13db92f

The supplied V4 blob is byte-for-byte identical to the packaged V4 review target.

The root → documentation → decisions path resolves Decision 0036 to Git blob:

7a5e40c290200e7dea91a9910f4e414990e3b309

The supplied Decision 0036 blob is byte-for-byte identical to the packaged Decision 0036 file.

The packaged immutable V3 predecessor has size 41330 bytes.

The packaged V3 predecessor SHA-256 is:

2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2

This matches the exact previously reviewed V3 identity.

V4 exists as a separate successor file.

No in-place modification of the packaged V3 predecessor was found.

The exact packaged V4 target is therefore bound to the supplied author checkpoint.



Confirm exact V4 SHA-256, size, author-checkpoint commit/tree, V4 Git blob,
Decision 0036 Git blob, exact V3 predecessor SHA, and that V3 was not edited
in place.

\---

### V4-RR02 — Correct V4 purpose and working-draft version metadata

Decision: PASS

Notes: The schema identifier is:

curl.technical-protocol-working-draft.v4

The status identifies the artifact as:

SOURCE\_ONLY\_TECHNICAL\_WORKING\_DRAFT\_V4\_AUTHOR\_CHECKPOINT

The governance working-draft version is:

V4

The purpose text explicitly identifies Working Draft V4.

The purpose text describes V4 as an immutable metadata-only successor.

The immediate predecessor is explicitly identified as exact Working Draft V3.

The predecessor working-draft version is recorded as:

V3

The purpose states that V4 addresses V3-RR02 and V3-RR12.

The purpose states that all accepted V3 protocol-rule semantics are preserved unchanged.

No operative V4 purpose, version, or successor metadata describes V2 as the current successor.

No V1-specific or V2-specific version reference was found anywhere in the exact V4 JSON.

The V4 purpose and working-draft version metadata are internally consistent.



Confirm V4 identifies itself as Working Draft V4, describes exact V3 as its
immediate immutable predecessor, identifies the metadata-only successor
boundary, and no longer describes V2 as the operative successor.

\---

### V4-RR03 — Exact V3 predecessor and completed-V3-review bindings

Decision: PASS

Notes: The governance predecessor path is:

config/annotation/curl\_technical\_protocol\_working\_draft.v3.json

The governance predecessor version is:

V3

The governance predecessor SHA-256 is:

2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2

The governance predecessor size is:

41330 bytes

These values match the packaged immutable V3 file.

The completed V3 human-review SHA-256 is:

9a15b13cea29bcbcbfff349c9b9bcb113a9d9a4e01afe03727d7be8dbd87c327

The completed V3 human-review commit is:

0f6625753452944bbedeab66a77a4098a6e349a9

The completed V3 human-review tree is:

a822ec4504071e0edbdc8b77c0eda8ea3974cdbc

The completed V3 human-review size is:

22983 bytes

The completed V3 review file in the package matches the recorded SHA-256 and size.

The recorded completed V3 review decision is:

REVISION\_REQUIRED

The completed review identifies V3-RR02 and V3-RR12 as revision-required items.

The governance metadata contains the exact V3 predecessor and completed-review bindings.

The successor-resolution metadata independently repeats the same V3 path, SHA-256, size, review SHA, commit, tree, and overall decision.

No inconsistency was found between the governance record, successor-resolution record, completed V3 review, and packaged V3 predecessor.



Confirm governance and successor-resolution metadata bind exact V3 path,
SHA-256, size, completed V3 human-review SHA/commit/tree, and overall
`REVISION\_REQUIRED` decision.

\---

### V4-RR04 — Removal of stale operative V1/V2 successor metadata

Decision: PASS

Notes: The operative purpose identifies V4 as the current working draft.

The operative purpose identifies exact V3 as the immediate immutable predecessor.

The former V1 predecessor path is no longer present in V4 governance metadata

The former V1 predecessor SHA-256 is no longer present in V4 governance metadata.

The former completed-review SHA binding has been replaced with the exact completed V3 review SHA-256.

The former successor-authorization commit has been replaced with the V4 successor-authorization commit:

cee5299cf80b633019ea6c98efc065b46aade1dd

The corresponding successor-authorization tree is:

37528cfdc0379b2e999eb8f8d83c7b036b1bb04e

The field `v1\_in\_place\_edit\_authorized` has been removed.

It has been replaced by the predecessor-generic field:

`predecessor\_in\_place\_edit\_authorized`

The value of `predecessor\_in\_place\_edit\_authorized` is false.

The successor-resolution metadata binds completed V3 review items V3-RR02 and V3-RR12 to V4 corrections.

The version-specific non-claims consistently refer to Working Draft V4.

The version-specific non-claims no longer refer to Working Draft V2.

A direct search of the exact V4 JSON found no V1-specific or V2-specific operative reference.

No stale V1/V2 successor binding was found in the V4 purpose, governance, successor-resolution metadata, or version-specific non-claims.

Historical provenance remains permitted outside operative successor metadata, but no historical V1/V2 reference affects the operative V4 boundary.



Confirm operative V4 purpose, governance, successor-resolution metadata, and
version-specific non-claims contain no stale V1/V2 successor binding,
including the former V1 predecessor path/review SHA/authorization commit and
`v1\_in\_place\_edit\_authorized` field.

Historical provenance outside the operative successor metadata may remain.

\---

### V4-RR05 — Preservation of accepted V3 protocol semantics

Decision: PASS

Notes: The packaged V3 and V4 JSON files were compared container by container.

`api\_surface` is identical in JSON semantics.

`resources` is identical in JSON semantics.

`return\_condition\_policy` is identical in JSON semantics.

`verdict\_semantics` is identical in JSON semantics.

`defect\_taxonomy` is identical in JSON semantics.

`global\_runtime\_rules` is identical in JSON semantics.

`easy\_handle\_rules` is identical in JSON semantics.

`multi\_handle\_rules` is identical in JSON semantics.

`cross\_resource\_rules` is identical in JSON semantics.

`exit\_obligations` is identical in JSON semantics.

The independently calculated canonical hash of every protocol-semantic container matches its V4 traceability-record hash.

No protocol rule was added.

No protocol rule was removed.

No protocol-rule content or classification was changed.

The V3-to-V4 differences are confined to schema, status, purpose, governance, successor-resolution, version-specific non-claims, and next-boundary metadata.

No unauthorized protocol-semantic correction was found in V4.

The accepted V3 protocol semantics are therefore preserved unchanged.:



Confirm all ten protocol-semantic containers are identical in JSON semantics
between packaged V3 and V4:

* api\_surface;
* resources;
* return\_condition\_policy;
* verdict\_semantics;
* defect\_taxonomy;
* global\_runtime\_rules;
* easy\_handle\_rules;
* multi\_handle\_rules;
* cross\_resource\_rules;
* exit\_obligations.

No protocol-semantic correction is authorized in V4.

\---

### V4-RR06 — Rule counts, API surface, and four-verdict contract

Decision: PASS

Notes: The easy-handle rule count is 21.

The easy-handle rule identifiers remain E01 through E21.

The multi-handle rule count is 29.

The multi-handle rule identifiers remain M01 through M29.

Comparison with packaged V3 found zero added protocol rules.

Comparison with packaged V3 found zero removed protocol rules.

The frozen API surface contains exactly twelve functions.

The twelve functions are:

curl\_global\_init

curl\_global\_cleanup

curl\_easy\_init

curl\_easy\_setopt

curl\_easy\_perform

curl\_easy\_reset

curl\_easy\_cleanup

curl\_multi\_init

curl\_multi\_add\_handle

curl\_multi\_perform

curl\_multi\_remove\_handle

curl\_multi\_cleanup

No additional curl function was introduced.

No frozen function was removed.

The declared machine-verdict contract contains exactly:

VALID

VIOLATION-MUST

VIOLATION-MAY

UNKNOWN

No undeclared machine-verdict variant was found.

Review state, explanatory text, provenance, and join-policy information remain separate from machine-verdict values.

The V3 rule counts, twelve-function API surface, and four-verdict contract are preserved unchanged.



Confirm easy-handle rule count remains 21, multi-handle rule count remains 29,
no protocol rule was added or removed, the frozen twelve-function curl surface
is preserved, and machine verdicts remain exactly:

`VALID`

`VIOLATION-MUST`

`VIOLATION-MAY`

`UNKNOWN`

\---

### V4-RR07 — Frozen scope and approved source evidence

Decision: PASS

Notes:The packaged frozen V3 source-only scope SHA-256 is:

ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb

The frozen scope file size is:

27947 bytes

The frozen twelve-function scope remains unchanged.

The pinned curl revision remains:

68720b4837284335b2d63cb358f8f6ce65f5bc55

The pinned curl tree remains:

e23d273aeb073c04aa5b073b35c9fde16979c896

The pinned revision and tree agree across V3, V4, the successor authorization, and the V4 source-evidence manifest.

The approved evidence class remains:

PREAPPROVED\_SOURCE\_ONLY

The source-evidence manifest declares exactly 21 approved files.

The frozen scope contains exactly the same 21 source-evidence entries.

The package physically contains exactly 21 files under the approved source-evidence directory.

No approved source file is missing.

No additional source-evidence file is present.

Each supplied source file independently matches its recorded SHA-256.

All 21 manifest paths and hashes match the corresponding frozen-scope source-evidence entries.

No pinned source revision, source path, source hash, or evidence-class change was found.



Confirm frozen V3 source-only scope remains unchanged, pinned curl revision and
tree remain unchanged, evidence class remains `PREAPPROVED\_SOURCE\_ONLY`, and
exactly the same 21 approved source files and hashes are supplied.

\---

### V4-RR08 — V4 author-resolution, traceability, and checkpoint consistency

Decision: PASS

Notes: V4-C01 corrects the purpose text and identifies exact V3 as the immediate predecessor.

V4-C01 is bound to V3-RR02.

V4-C02 corrects `governance.working\_draft\_version` to V4.

V4-C02 is bound to V3-RR02.

V4-C03 binds the predecessor version, path, SHA-256, and size to exact V3.

V4-C03 is bound to V3-RR02.

V4-C04 binds the completed human-review metadata to the exact completed V3 review.

V4-C04 is bound to V3-RR02.

V4-C05 updates the V4 successor-authorization binding.

V4-C05 removes the stale `v1\_in\_place\_edit\_authorized` field.

V4-C05 introduces the predecessor-generic `predecessor\_in\_place\_edit\_authorized` field with value false.

V4-C05 is bound to V3-RR02.

V4-C06 corrects the operative successor-resolution metadata and V4-specific non-claims.

V4-C06 is bound to V3-RR12.

The author-resolution, traceability, and checkpoint records consistently list V4-C01 through V4-C06.

The preserved V3 PASS subjects are:

V3-RR01

V3-RR03

V3-RR04

V3-RR05

V3-RR06

V3-RR07

V3-RR08

V3-RR09

V3-RR10

V3-RR11

The exact V4 SHA-256 bound by the author-resolution record is:

e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8

The traceability record binds the same exact V4 SHA-256.

The author-checkpoint record binds the same exact V4 SHA-256 and size of 41033 bytes.

The author checkpoint identifies the status as:

SOURCE\_ONLY\_TECHNICAL\_WORKING\_DRAFT\_V4\_AUTHOR\_CHECKPOINT

The author-checkpoint record correctly binds the author-resolution and metadata-traceability file hashes.

All ten protocol-semantic containers remain identical between packaged V3 and V4.

No protocol rule was added or removed.

No unauthorized protocol-semantic change was found.

The author-resolution, traceability, checkpoint, and exact V4 artifact are internally consistent.



Confirm V4-C01 through V4-C06 are correctly represented and bound to
V3-RR02/V3-RR12, V3 PASS subjects are preserved, exact V4 SHA is bound by
traceability/checkpoint records, and no unauthorized protocol change appears.

\---

### V4-RR09 — Platform-independent review-package path verification

Decision: PASS

Notes: The verifier imports and uses `PurePosixPath` for logical-path handling.

The `logical\_path` function first replaces backslashes with forward slashes.

The normalized value is converted to canonical POSIX form with:

`PurePosixPath(s).as\_posix()`

Manifest source paths are normalized before path-set comparison.

Actual filesystem paths are converted to relative logical paths and normalized before comparison.

The verifier includes an explicit Windows-path simulation.

The simulation converts approved forward-slash paths to backslash form.

It then normalizes those simulated Windows paths back to POSIX form.

The normalized Windows representations match the approved logical source paths.

All approved manifest paths are relative paths.

No absolute, drive-qualified, or parent-traversal source path exists in the reviewed manifest.

The `physical\_from\_logical` function separates the canonical logical path into components.

It joins those components to the supplied package or source root using `root.joinpath`.

This correctly maps the reviewed logical paths to local filesystem paths on Windows and POSIX platforms.

The verifier compares the actual source-path set with the expected normalized path set.

The verifier calculates SHA-256 from each physical source file after path resolution.

It compares each calculated hash with the original manifest hash.

Path normalization does not modify file content.

Path normalization does not modify recorded hashes.

All 21 source files retain their approved hashes.

No source-evidence path, evidence classification, or semantic content is changed.

The Windows normalization self-test and the complete V4 package verification both pass.

V4-P01 is therefore correctly implemented for the reviewed package.

Review `18\_verify\_review\_package.v4.py`.



Confirm source-path comparison canonicalizes logical relative paths to
forward-slash POSIX form before comparison, accepts equivalent Windows
backslash representations after normalization, joins logical path components
to the local filesystem safely, and does not alter source hashes or evidence
semantics.

This item addresses V4-P01.

\---

### V4-RR10 — Evidence quarantine and prohibited evidence

Decision: PASS

Notes: The immutable review package contains exactly 47 files.

The package contains the exact V4 and immutable V3 predecessor.

The package contains the completed V3 human review and authorized decision records.

The package contains V4 authorization, resolution, traceability, and checkpoint records.

The package contains the frozen source-only scope.

The package contains exactly 21 approved pinned curl source files.

The package contains the minimal Git witness, package manifest, checksum manifest, and verifier.

No generated-driver source is present.

No selected-sample membership data is present.

No raw model response is present.

No generated-driver compiler-log semantic content is present.

No gold label or gold-annotation file is present.

No analyzer output is present.

No baseline output is present.

No LLM-review output is present.

No repair output is present.

References to prohibited evidence categories occur only in boundary, exclusion, and non-authorization statements.

Those references do not supply or use the prohibited material as technical evidence.

The V4 draft, authorization, traceability, source manifest, and review-package records consistently state that prohibited evidence was not used.

The supplied technical evidence remains within the approved `PREAPPROVED\_SOURCE\_ONLY` boundary.

No evidence-quarantine violation was found.



Confirm no generated-driver source, selected-sample membership, raw model
response, generated-driver compiler-log semantic content, gold label, analyzer
output, baseline output, LLM-review output, or repair output is present or used
as V4 review evidence.

\---

### V4-RR11 — V4-specific non-claims and non-authorizations

Decision: PASS

Notes: The V4 non-claims state:

This file is not canonical curl.json.

The V4 non-claims state:

Working Draft V4 has not yet received independent human technical approval.

The V4 non-claims state:

Working Draft V4 is not a canonical curl specification.

The non-claims consistently refer to Working Draft V4.

Canonical `curl.json` remains unauthorized.

Canonical curl-specification status remains false.

Generated-driver inspection remains unauthorized.

Selected-sample membership inspection remains unauthorized.

Gold annotation remains unauthorized.

Analyzer implementation remains unauthorized.

Analyzer execution remains unauthorized.

Baseline execution remains unauthorized.

Repair remains unauthorized

These non-authorizations are consistently recorded in the V4 governance, successor authorization, author-resolution, author-checkpoint, and Decision 0036 records.

No statement in the package grants canonical status or any prohibited downstream authorization.



Independent approval and any later canonicalization authorization remain separate boundaries.

Confirm V4-specific non-claims correctly state that V4 is not canonical and
has not yet received independent approval. Confirm canonical curl.json,
generated-driver inspection, selected-sample inspection, gold annotation,
analyzer implementation/execution, baseline execution, and repair remain
unauthorized.

\---

### V4-RR12 — Overall technical adequacy for later canonicalization authorization

Decision: PASS

Notes: The exact V4 SHA-256 and size are independently verified.

The author commit, tree, V4 blob, and Decision 0036 blob are independently resolved by the supplied Git witness.

V4 is a separate immutable successor to exact V3.

V4-C01 through V4-C06 correctly resolve the metadata issues identified by V3-RR02 and V3-RR12.

The operative purpose, governance, predecessor binding, completed-review binding, successor-resolution metadata, and non-claims consistently identify V4 and exact V3.

No stale operative V1 or V2 successor metadata remains.

All ten accepted V3 protocol-semantic containers are identical in JSON semantics between packaged V3 and V4.

No protocol rule was added.

No protocol rule was removed.

The 21 easy-handle rules and 29 multi-handle rules remain unchanged.

The frozen twelve-function curl API surface remains unchanged.

The exact four-machine-verdict contract remains unchanged.

The frozen source-only scope and pinned curl revision and tree remain unchanged.

The evidence class remains `PREAPPROVED\_SOURCE\_ONLY`.

Exactly the same 21 approved source files and hashes are supplied.

No prohibited evidence class is present or used.

The author-resolution, traceability, checkpoint, package manifest, checksums, and exact V4 artifact are mutually consistent.

The package verifier normalizes POSIX and Windows path representations before comparison.

The verifier preserves the original source paths, hashes, and evidence semantics.

All package checksum entries pass.

No new semantic inconsistency or required successor correction was identified.

The exact immutable V4 is technically adequate to proceed to a later separate canonicalization authorization.

This PASS does not itself authorize canonicalization or create canonical `curl.json`.



Considering the exact V4 metadata corrections, complete preservation of accepted
V3 protocol semantics, source-only evidence boundary, successor-bound
traceability, and platform-independent package verification, determine whether
exact V4 is technically adequate to proceed to a later separate
canonicalization authorization.

If not, identify the precise required successor correction.

\---

## Overall technical review decision

Choose exactly one:

`APPROVE\_EXACT\_WORKING\_DRAFT\_V4\_FOR\_CANONICALIZATION`

`REVISION\_REQUIRED`

`FAIL`

Overall decision: APPROVE\_EXACT\_WORKING\_DRAFT\_V4\_FOR\_CANONICALIZATION

Notes: All V4-RR01 through V4-RR12 review items are PASS.

The exact V4 identity, size, author checkpoint, Git witness, and immutable V3 predecessor binding are verified.

V4-C01 through V4-C06 correctly resolve the authorized V3 metadata and review-package portability findings.

All ten accepted V3 protocol-semantic containers are preserved unchanged.

No protocol rule was added, removed, or semantically modified.

The frozen twelve-function API surface and exact four-verdict contract are preserved.

The frozen scope, pinned curl revision and tree, and all 21 approved source files and hashes are unchanged.

The evidence boundary remains PREAPPROVED\_SOURCE\_ONLY.

No prohibited evidence was present or used.

The V4 author-resolution, traceability, checkpoint, manifest, checksums, and Git witness are mutually consistent.

Platform-independent source-path verification is correctly implemented.

No remaining technical inconsistency or required successor correction was identified.

The exact immutable Working Draft V4 is technically adequate to proceed to a later separate canonicalization authorization.

This approval applies only to the exact V4 SHA-256:

e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8

This approval does not itself create or authorize canonical curl.json.

Canonicalization still requires a separate explicit authorization and operation.



Generated-driver inspection, selected-sample inspection, gold annotation, analyzer implementation or execution, baseline execution, and repair remain unauthorized.Reviewer identity

Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 19 / August / 2026

## Post-review rule

No assistant-generated or synthetic human approval is permitted.

If revision is required, exact V4 must remain immutable and a new successor
must be created rather than editing V4 in place.

If approval is granted, exact V4 must remain immutable and canonicalization
still requires a separate explicit authorization and operation.

