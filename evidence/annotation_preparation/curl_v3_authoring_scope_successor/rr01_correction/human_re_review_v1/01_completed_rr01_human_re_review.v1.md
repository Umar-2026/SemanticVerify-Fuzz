# curl V3 RR01 Corrected Evidence Independent Re-Review Packet

## Purpose

This is a narrowly scoped independent human re-review of the previously
blocking `V3-RR01`.

The prior completed V3 review recorded:

* V3-RR01: `REVISION\_REQUIRED`
* V3-RR02: `PASS`
* V3-RR03: `PASS`
* V3-RR04: `PASS`
* overall: `REVISION\_REQUIRED`

This re-review does not silently overwrite those historical decisions.

Its purpose is to determine whether the two V3-RR01 blockers have now been
resolved by immutable correction evidence.

## Exact V3 target

Path:

`config/annotation/curl\_v3\_authoring\_scope.v3.json`

SHA-256:

`ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`

Author checkpoint commit:

`7de6fc01797ae68cbd64406b850a3198f71cc702`

Author checkpoint tree:

`c5f96b844e5803cccd04c9f64a55754dc6c77e20`

Git blob:

`931c24cc46c99f23ee352455d3e8c93e57e63401`

The V3 scope itself has not been edited after the prior review.

## Exact V2 predecessor

Path:

`config/annotation/curl\_v2\_authoring\_scope.v2.json`

SHA-256:

`f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df`

## Historical Decision 0023

Immutable SHA-256:

`c774bb667930ef9ceaedc5ca5d25e88d57da3ffefa10de639ef6a20f7d2271d1`

The prior reviewer identified a malformed predecessor-SHA presentation line in
Decision 0023.

Decision 0023 has not been edited in place.

## Corrective Decision 0024

SHA-256:

`df22dc70c572407c1968859f6fd86a20d847062b2130a08484670c06a340915b`

Commit:

`36400fa2028df6ccaf176780ba8ff21017a68262`

Tree:

`d7afbc0a4c159530f5687c93dca2bad823e55f77`

Git blob:

`ca72e87d5668c649eb64db8fc04f457eeebc5d0c`

Decision 0024 preserves Decision 0023 as immutable historical evidence and
records the corrected predecessor binding without modifying the V3 scope
semantics.

## Independently resolvable Git witness

The package contains:

`10\_minimal\_git\_witness\_v1/02\_curl\_v3\_rr01\_minimal\_git\_witness.v1.tar.gz`

SHA-256:

`3710cd5b49fa3e80610724756bae7376fc196c23de36f2f110ab6074d256e181`

The witness is intended to contain exactly:

* 2 commit objects;
* 6 tree objects;
* 2 file blobs.

The only file blobs are the exact V3 scope and Decision 0024.

Parent commit objects and unrelated file blobs are intentionally excluded.

Run:

`python3 10\_minimal\_git\_witness\_v1/03\_verify\_minimal\_git\_witness.v1.py`

Expected final result:

`QUARANTINE\_SAFE\_MINIMAL\_GIT\_WITNESS\_VERIFICATION=PASS`

## Mandatory decisions

For each corrected RR01 item choose exactly one:

`PASS`

`REVISION\_REQUIRED`

`FAIL`

### RR01-R1 — Exact immutable V3 target and V2 predecessor

Decision: PASS

Notes: Independently verified the actual files in the corrected re-review

handoff. The exact V3 scope has SHA-256

ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb

and Git blob

931c24cc46c99f23ee352455d3e8c93e57e63401.



The exact V2 predecessor has SHA-256

f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df.



The current V3 SHA-256 is identical to the value recorded in the prior

completed V3 review. V2 is likewise preserved at its previously recorded

hash. Decision 0024 is a separate correction record and does not alter

either scope artifact. No in-place modification of V3 or V2 was found.



Confirm:

* exact V3 SHA-256 is correct;
* exact V3 Git blob is correct;
* exact V2 predecessor SHA-256 is correct;
* V3 and V2 remain immutable;
* V3 has not been edited in place after the prior review.

### RR01-R2 — Independently resolvable V3 commit/tree/blob evidence

Decision: PASS

Notes: Using only the supplied minimal Git witness, independently confirmed

that 7de6fc01797ae68cbd64406b850a3198f71cc702 exists as a commit

object. Its root tree resolves to

c5f96b844e5803cccd04c9f64a55754dc6c77e20.



Within that tree, path

config/annotation/curl\_v3\_authoring\_scope.v3.json resolves to blob

931c24cc46c99f23ee352455d3e8c93e57e63401. The extracted blob

content has SHA-256

ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb.



The complete commit → tree → path → blob → content-SHA relationship

was independently resolved without relying on the original research

repository.



Using only the supplied minimal Git witness, independently confirm:

* commit
`7de6fc01797ae68cbd64406b850a3198f71cc702`
exists as a commit object;
* its root tree resolves to
`c5f96b844e5803cccd04c9f64a55754dc6c77e20`;
* path
`config/annotation/curl\_v3\_authoring\_scope.v3.json`
resolves to blob
`931c24cc46c99f23ee352455d3e8c93e57e63401`;
* that blob has SHA-256
`ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`.

### RR01-R3 — Decision 0023 immutable correction

Decision: PASS

Notes: Independently confirmed that historical Decision 0023 remains

byte-preserved at SHA-256

c774bb667930ef9ceaedc5ca5d25e88d57da3ffefa10de639ef6a20f7d2271d1.



Decision 0024 is provided as a separate immutable correction record,

with SHA-256

df22dc70c572407c1968859f6fd86a20d847062b2130a08484670c06a340915b.

It correctly records the exact V2 predecessor SHA-256 as

f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df.



Decision 0023 was not edited in place. Decision 0024 corrects only the

historical predecessor-SHA presentation and does not modify the V3

scope artifact. The exact V3 SHA-256 remains unchanged, so no change

to its protocol-semantic surface was found.



Confirm:

* historical Decision 0023 remains byte-preserved at SHA-256
`c774bb667930ef9ceaedc5ca5d25e88d57da3ffefa10de639ef6a20f7d2271d1`;
* Decision 0024 is a separate immutable correction record;
* Decision 0024 correctly records the V2 predecessor SHA-256 as
`f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df`;
* Decision 0024 does not modify the exact V3 protocol-semantic surface.

### RR01-R4 — Witness quarantine and minimality

Decision: PASS

Notes: Independently inspected the complete object inventory of the supplied

minimal Git witness. It contains exactly 10 Git objects: 2 commit

objects, 6 tree objects, and 2 file blobs.



The only blob objects are:

931c24cc46c99f23ee352455d3e8c93e57e63401 — exact V3 scope;

ca72e87d5668c649eb64db8fc04f457eeebc5d0c — Decision 0024.



The referenced parent-history commit objects are absent. No additional

file blobs are present; therefore, no generated-driver, gold-label,

analyzer-output, baseline-output, LLM-review-output, repair-output, or

other unrelated file content is exposed by the witness. The witness

satisfies the stated quarantine and minimality requirements.



Confirm that the supplied witness contains exactly:

* 2 commit objects;
* 6 tree objects;
* 2 file blobs;

and that:

* the only file blobs are the exact V3 scope and Decision 0024;
* parent-history commit objects are absent;
* unrelated generated-driver, gold-label, analyzer-output, baseline-output,
LLM-review-output, and repair-output blobs are not exposed.

## Overall re-review decision

Choose exactly one:

Overall decision: APPROVE\_EXACT\_V3\_SCOPE\_FOR\_FREEZE



Notes: 

Independent re-review confirmed resolution of the previously blocking V3-RR01 issues. The supplied minimal Git witness independently resolves the exact V3 author commit → tree → path → blob → SHA-256 chain, and Decision 0024 separately corrects the Decision 0023 predecessor-SHA presentation while preserving Decision 0023 and the exact V3 scope unchanged. No new blocking issue was identified within this RR01 re-review boundary. This decision authorizes only the subsequent separate V3 scope-freeze operation; technical working-draft authoring and all downstream activities remain unauthorized until that freeze is completed.



Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 18 / August / 2026



## Decision interpretation

`APPROVE\_EXACT\_V3\_SCOPE\_FOR\_FREEZE` may be chosen only if the reviewer is
satisfied that the previously blocking RR01 evidence defects are resolved and
finds no new blocking issue.

That decision authorizes only the subsequent **separate V3 scope-freeze
operation**.

It does NOT directly authorize technical working-draft authoring.

Technical working-draft authoring remains prohibited until the exact approved
V3 scope subsequently completes its separate freeze boundary.

No assistant-generated or synthetic human approval is permitted.

