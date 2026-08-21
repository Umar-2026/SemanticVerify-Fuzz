\# AF04/AF07/AF08/AF09 — Focused Independent Human Rereview

Enter exactly one decision for each item:

PASS

REVISION\_REQUIRED

FAIL

\---



\## AF04 — Explicit future active dispatch path and deferred creation

Decision: PASS

Notes: The packaged raw Git objects independently reproduce checkpoint commit `fa64f7810443d14cd710600cd48ae9f9fedbb04a`, its sole immediate parent `6eba8a1fc69c0b1146e033b031f5948a245bd84b`, and root trees `9bb36f1a7d1bb303341f65ded8f0c63796d5c7cd` and `67a80e37f8c94c2c5878f4ddde4da1943e7a5dc6`. Raw tree-entry inspection confirms that `config/protocol\_specification\_schema\_version\_dispatch.v1.json` is absent at both revisions. The future active dispatch path was therefore not created or installed by the reviewed commit.

\## AF07 — Historical Decision-0019 immutability and deferred successor adoption

Decision: PASS

Notes: Commit-to-tree-to-path-to-blob resolution binds historical Decision 0019 at `documentation/decisions/0019-canonical-library-protocol-specification-path-convention.md` to the identical Git blob `2b4f46282ab05ff41e2610facb3fb26aa697983b` at the checkpoint and parent. The exported raw blob reproduces SHA-256 `50e273ecb6af838bc83d2499a2ed3a71607bc7c0cf8d74bd2622b56c2fefafa9`. The documentation subtree is identical at both revisions, and the evidence records no Decision-0019 successor adoption.



\## AF08 — Approved V2 hash-contract active-form preservation

Decision: PASS

Notes: The approved V2 hash-contract active form at `evidence/annotation\_preparation/protocol\_specification\_schema\_successor\_v2/schema\_v2\_hash\_contract\_finalization\_package\_v1/02\_active\_form\_v2\_hash\_contract.REVIEW\_CANDIDATE.json` resolves to the identical Git blob `fd9648f4e0eee7e4516927dc1e370a0d69920ea2` at checkpoint and parent. Its raw blob reproduces SHA-256 `37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9`. The active path `config/protocol\_content\_hash\_canonicalization.v2.json` is absent at both revisions, so the approved artifact was preserved without active-path installation.



\## AF09 — Core artifact and downstream non-interference

Decision: PASS

Notes: Raw Git-object resolution verifies identical checkpoint and parent blobs, with reproduced governed SHA-256 values, for Decision 0019, the approved V2 hash-contract active form, its human-approval record, the reviewed successor source, the reviewed version-dispatch source, Schema V2, the V1 hash contract, frozen `zlib.json`, and frozen `libpcap.json`. The checkpoint and parent use the identical config tree `a86c0022a0d264a1195ed3fcd0b9424b85742c2d` and documentation tree `33adb6befe244d24ddfe90680d7388c98da4de05`. `config/protocol\_specifications/curl.json` is absent at both revisions. Recursive comparison produces exactly 22 changed leaf paths, all under `evidence/annotation\_preparation/protocol\_specification\_schema\_successor\_v2/schema\_v2\_activation\_artifact\_finalization\_package\_v1/`, with zero missing, additional, or out-of-scope paths.

\---



\## Overall focused corrective evidence decision

Enter exactly one:

APPROVE\_AF04\_AF07\_AF08\_AF09\_CORRECTIVE\_EVIDENCE

REVISION\_REQUIRED

FAIL



Overall decision: APPROVE\_AF04\_AF07\_AF08\_AF09\_CORRECTIVE\_EVIDENCE

Overall notes: All four focused corrective items PASS. The ZIP SHA-256 is `e165dab32a743bc94dbd93c31861387327c881c937cc16229326677aad1e9762`. All 6 outer and 54 package checksum entries reproduce with zero mismatches. All 41 supplied raw Git objects reproduce their expected object IDs, the exact checkpoint-parent relationship is verified, all governed path/blob and SHA-256 bindings pass, all required active paths are absent, and all 22 changes are confined to the original activation-artifact-finalization package. Together with the six closed prior PASS items, the aggregate state is `10 PASS / 0 REVISION\_REQUIRED / 0 FAIL`. This approval is evidence-only and does not activate Schema V2, install an active V2 hash contract or version-dispatch artifact, adopt the Decision-0019 successor, create `curl.json`, define or authorize a positive mapping, or authorize analyzer, baseline, or repair execution.



Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 21 / August / 2026



