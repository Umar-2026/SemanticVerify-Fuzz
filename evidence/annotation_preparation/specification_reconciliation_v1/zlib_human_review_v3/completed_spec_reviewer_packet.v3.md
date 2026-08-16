# zlib Source-Only Protocol Specification Successor Review Packet V3

## Exact immutable review target

Author role: `Spec-Author-1`

Reviewer role: `Spec-Reviewer-1`

Reviewer underlying role: `Adjudicator-C`

### Repository immutable target path

`evidence/annotation\_preparation/specification\_reconciliation\_v1/zlib\_working\_draft\_v3/zlib\_source\_only\_successor\_working\_fsm\_draft.v3.json`

### Package-local immutable review target

`03\_zlib\_source\_only\_successor\_working\_fsm\_draft.v3.json`

Both locations are required to be byte-identical and are bound to this exact SHA-256:

`8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e`

Pinned zlib revision:

`da607da739fa6047df13e66a2af6b8bec7c2a498`

This V3 artifact is a new immutable successor author checkpoint.

It is **not** a frozen canonical protocol specification.

## Prior immutable V2 review

V2 draft SHA-256:

`9f6e035fb275fb34e5f9ab34a6267f3b416b80a7aae8a7a1741c445c20457e5d`

Completed V2 human-review SHA-256:

`e921490a4462d8a8774192b79b7dcebe58487333fa5fa8a812959b131f01227d`

V2 human-review record SHA-256:

`f21e7b6ad8c31acd8decc8b2d4983184028ca67528a5ac480c7fcf6ef7c149fd`

Prior overall decision:

`REVISION\_REQUIRED`

Only three remaining V2-review issues are addressed in this successor.

## Exact V3 specification delta

There is exactly one protocol-specification semantic correction:

`ZLIB-R12.source\_evidence`

Changed from:

`\["EV-ZLIB-H-001","EV-ZLIB-DEF-002","EV-ZLIB-INF-003","EV-ZLIB-TEST-005"]`

to:

`\["EV-ZLIB-H-001","EV-ZLIB-DEF-002","EV-ZLIB-INF-003"]`

`EV-ZLIB-TEST-005` was removed because the pinned `example.c` does not demonstrate `deflateReset` or `inflateReset`.

All V2 states, events, transitions, permitted exit states, protocol provenance entries, `T17`, `ZLIB-R14`, R02/T15 correction, and gzip-scope semantics are otherwise preserved.

## Review quarantine

Use only the files supplied in this review package.

Do **not** consult:

* generated fuzz drivers
* selected-sample membership
* raw model responses
* generated compiler-log semantic contents
* gold labels
* analyzer output
* baseline output
* controlled LLM-review output
* repair output
* failure-prompted post-hoc evidence

## Approved protocol evidence

* `EV-ZLIB-H-001` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/zlib.h` — SHA-256 `818667d6ab6a37fe7469cb06a7f0cb2c2cb2f2c948a03e5accf1a4a74bf3020a`
* `EV-ZLIB-DEF-002` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/deflate.c` — SHA-256 `ea9ca4eb51b1a71aaf214b99f4a9fab177253d6268cae8e4c26d44d1812e52c2`
* `EV-ZLIB-INF-003` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/inflate.c` — SHA-256 `90221ea7d762e7044057f6ad5013e969086c6ba3d3051716b7aa786d7a6362ec`
* `EV-ZLIB-ZPIPE-004` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/examples/zpipe.c` — SHA-256 `e79717cefd20043fb78d730fd3b9d9cdf8f4642307fc001879dc82ddb468509f`
* `EV-ZLIB-TEST-005` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/test/example.c` — SHA-256 `be1b050aad808cdb016c01f42568d3a62ee37dd7b2b56bef0ade21be8d9fee0d`
* `EV-ZLIB-INFCOVER-006` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/test/infcover.c` — SHA-256 `37718912b22c68942a469f971cbb47500d24dc4f6258db271edd417f0eb69a5e`
* `EV-ZLIB-INFLATE-H-007` — `/openbayes/home/svf-gate1c-source-qualification-v1/zlib/inflate.h` — SHA-256 `e6a43bd0e24ab2cf5fa1dca630859e9a2f6a721f033f75faf179f5c0299e4fe2`

## Frozen S03 review-scope governance evidence

Package-local reference:

`04\_frozen\_zlib\_S03\_scope\_reference.v1.json`

Reference SHA-256:

`3067726f23aafc256266c34c2383ce80dd3e614f10db0df3046d481e5f808c57`

Frozen source manifest repository path:

`config/generation/scenario\_bindings.80.v10.json`

Frozen source manifest SHA-256:

`a7ab361e6e2d41d9051e48bc7626f0be37c1df9ec35f788a9a019b010054a2db`

Gate-1 closure commit:

`15ff63bfc82f023f784266bacf04f43abbe82818`

Frozen zlib S03 canonical object SHA-256:

`4027fd91f65a64f47cf5c67ab824b77fd05333ca2ad4d7cac2c33d61cf34efd1`

Frozen S03 task:

`Use input bytes to select a supported zlib, gzip, or raw decoding mode and attempt streaming decompression.`

This S03 reference is governance/scope evidence for independently checking the gzip reconciliation. It is **not** protocol-obligation provenance.

## V2-RR-01 — ZLIB-R12 evidence correction

Please verify that:

1. `EV-ZLIB-TEST-005` has been removed from `ZLIB-R12.source\_evidence`.
2. `EV-ZLIB-H-001`, `EV-ZLIB-DEF-002`, and `EV-ZLIB-INF-003` remain.
3. The retained pinned sources sufficiently support the modeled `deflateReset` / `inflateReset` obligation.
4. No unrelated semantic change was introduced into `ZLIB-R12`.

Decision: PASS



Notes:



Verified the exact V2 and V3 ZLIB-R12 objects. EV-ZLIB-TEST-005

has been removed from ZLIB-R12.source\_evidence, while EV-ZLIB-H-001,

EV-ZLIB-DEF-002, and EV-ZLIB-INF-003 remain.



The retained pinned sources sufficiently support the modeled reset

obligation. zlib.h documents that deflateReset and inflateReset require

consistent stream state and reuse internal state without freeing and

reallocating it. deflate.c and inflate.c implement the corresponding

state validation and reuse behavior. example.c contains no deflateReset

or inflateReset calls, so its removal from R12 is justified.



A field-by-field comparison of the exact V2 and V3 ZLIB-R12 objects

shows that source\_evidence is the only changed field, and the only

evidence-list change is removal of EV-ZLIB-TEST-005. No unrelated

semantic change was introduced into ZLIB-R12.

## V2-RR-02 — immutable target path correction

Please verify that:

1. The repository immutable target path is explicitly identified.
2. The package-local immutable target is explicitly identified.
3. The package-local V3 JSON is byte-identical to the repository V3 target.
4. Both are bound to the same SHA-256 `8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e`.

Decision: REVISION\_REQUIRED



Notes:



The repository immutable target path is explicitly identified as:



evidence/annotation\_preparation/specification\_reconciliation\_v1/

zlib\_working\_draft\_v3/

zlib\_source\_only\_successor\_working\_fsm\_draft.v3.json



The package-local immutable target is explicitly identified and present as:



03\_zlib\_source\_only\_successor\_working\_fsm\_draft.v3.json



The independently calculated SHA-256 of the package-local V3 JSON is:



8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e



This matches the value declared in the review packet and SHA256SUMS.txt.

However, the actual repository-side V3 target was not supplied. Therefore,

the package-local file's byte identity with the repository target, and the

repository target's binding to the same SHA-256, cannot be independently

verified.



The supplied V2 JSON does not satisfy this check because RR-02 requires

comparison of the package-local V3 JSON with the repository-side V3 target.

## V2-RR-03 — frozen S03 evidence completeness

Please verify using `04\_frozen\_zlib\_S03\_scope\_reference.v1.json` that:

1. the frozen scenario manifest SHA-256 is `a7ab361e6e2d41d9051e48bc7626f0be37c1df9ec35f788a9a019b010054a2db`;
2. the reference records the Gate-1 freeze binding;
3. the exact frozen zlib S03 task includes supported zlib, gzip, and raw decoding modes;
4. the canonical S03 object SHA-256 is `4027fd91f65a64f47cf5c67ab824b77fd05333ca2ad4d7cac2c33d61cf34efd1`;
5. this artifact is treated as governance/scope evidence rather than protocol-obligation provenance;
6. the V3 gzip-scope interpretation remains aligned with frozen S03.

Decision: PASS



Notes:



Verified that the frozen scenario manifest SHA-256 is

a7ab361e6e2d41d9051e48bc7626f0be37c1df9ec35f788a9a019b010054a2db.



The reference records the Gate-1 closure commit and the freeze-package

binding to config/generation/scenario\_bindings.80.v10.json.



The exact frozen S03 task explicitly includes supported zlib, gzip, and

raw decoding modes.



The declared canonical S03 object SHA-256 is

4027fd91f65a64f47cf5c67ab824b77fd05333ca2ad4d7cac2c33d61cf34efd1.

Independent canonicalization of the supplied S03 object using the stated

canonicalization rules produces the same hash.



The reference explicitly classifies itself as governance/scope evidence

and not as protocol-obligation provenance.



The V3 format-scope interpretation remains aligned with frozen S03:

the core z\_stream lifecycle applies to supported zlib, raw, and gzip

wrapper modes, while gzip-specific metadata/header obligations and the

gzFile API family remain separately scoped.



All six checks pass.

## Evidence completeness

Considering the corrected `ZLIB-R12` evidence and the supplied frozen-S03 scope reference:

Decision: PASS



Notes:



The corrected ZLIB-R12 evidence is complete and sufficient.

EV-ZLIB-H-001, EV-ZLIB-DEF-002, and EV-ZLIB-INF-003 are defined in

the V3 provenance table, their corresponding files are present, and

their calculated SHA-256 values match the declared hashes.



The retained public header and implementation sources support the

modeled deflateReset and inflateReset obligation: reset requires a

consistent live stream, reuses internal state without releasing

ownership, and leaves the eventual matching End obligation in place.



EV-ZLIB-TEST-005 was correctly removed from ZLIB-R12 because the pinned

example.c contains no deflateReset or inflateReset workflow. Its removal

does not create an evidence gap.



The supplied frozen-S03 reference contains the required manifest hash,

Gate-1 binding, exact zlib/gzip/raw task, and canonical object hash.

Its governance/scope classification is explicit, and the V3 gzip-scope

interpretation remains aligned with it.



Evidence completeness passes.

## Carry-forward integrity

Please verify that the previously accepted V2 technical components remain unchanged:

* 8 states
* 11 events
* 17 transitions
* 14 core obligations
* 7 protocol provenance entries
* `T17` preserved
* `ZLIB-R14` preserved
* `T15` remains absent from source-oriented `ZLIB-R02`
* gzip wrapper remains included in supported core `z\_stream` lifecycle scope
* `freeze\_date` and specification/obligation `content\_sha256` remain deferred

Decision: PASS



Notes:



Compared the exact V2 and V3 candidate specification objects.



Both versions contain 8 states, 11 events, 17 transitions, 14 core

obligations, and 7 protocol provenance entries. The state, event,

transition, and provenance collections are identical.



T17 is preserved without change. ZLIB-R14 is preserved without change.

All thirteen obligations other than ZLIB-R12 are identical. The only

change within ZLIB-R12 is the separately reviewed removal of

EV-ZLIB-TEST-005 from source\_evidence.



ZLIB-R02.permitted\_transitions is \[T11, T12, T14, T17] in both versions,

so T15 remains absent from the source-oriented ZLIB-R02.



The V2 and V3 gzip format-scope objects are identical, and the supported

core z\_stream lifecycle modes continue to include the gzip wrapper.



Specification-level freeze\_date and content\_sha256 remain unassigned,

and no obligation-level freeze\_date or content\_sha256 has been assigned.



Carry-forward integrity passes.

## Overall human-review decision

Choose exactly one:

* \[ ] `APPROVE\_EXACT\_DRAFT\_FOR\_FINALIZATION`
* \[x] `REVISION\_REQUIRED`
* \[ ] `REJECT`

Summary:





The exact V2-to-V3 comparison confirms that the ZLIB-R12 correction is

limited to removal of EV-ZLIB-TEST-005 from source\_evidence. The retained

pinned sources sufficiently support the modeled deflateReset and

inflateReset obligation, and no unrelated semantic change was introduced

into ZLIB-R12.



The frozen S03 governance/scope reference is complete. Its manifest,

Gate-1 binding, canonical object hash, and zlib/gzip/raw task were

verified, and the V3 gzip-scope interpretation remains aligned with it.



Evidence completeness and carry-forward integrity pass. V3 preserves

the accepted counts, T17, ZLIB-R14, the source-side R02/T15 correction,

gzip wrapper lifecycle scope, provenance entries, and deferred freeze

dates and content hashes.



However, V2-RR-02 cannot pass because the actual repository-side V3

target was not supplied. Although the package-local V3 JSON has the

declared SHA-256

8691897759d6267fde52dd76df9199802163b41cd11bfadd3dde534df623632e,

its byte identity with the repository target and the repository target's

binding to the same hash cannot be independently verified.



Accordingly, the overall decision is REVISION\_REQUIRED rather than

REJECT. A new immutable successor review checkpoint/package should

provide an allowed, independently verifiable repository-side V3 binding.



Reviewer role ID: `Spec-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 16 / August / 2026



## Immutability rule

If the decision is `REVISION\_REQUIRED`, do not edit this V3 file in place. A new immutable successor checkpoint is required.

If the decision is `APPROVE\_EXACT\_DRAFT\_FOR\_FINALIZATION`, no semantic change may be introduced during finalization. Only the already-deferred freeze dates and Decision-0018 content hashes may be added before validation and canonical freeze.

