# Independent Human-Review Packet — CWXR01–CWXR08
Study under review:
**Requirement-to-Semantic-Unit Crosswalk Evidence Resolution Study V1**
Required reviewer role:
**Spec-Technical-Reviewer-1**
Allowed per-item decisions:
**PASS / REVISION_REQUIRED / FAIL**
Allowed overall decisions:
**APPROVE_REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_EVIDENCE_RESOLUTION_STUDY_V1 / REVISION_REQUIRED / FAIL**
---
## CWXR01 — Study identity and artifact integrity
Verify Study V1 identity, Decision-0148 binding, complete artifact integrity, checksum closure, and repeat-safe verifier result.
CWXR01 decision: `PASS`
CWXR01 reviewer notes: Study V1’s identity and Decision-0148 artifact bindings are internally consistent. All 37 external-handoff, 28 review-package, and 10 Study V1 checksum entries matched, with complete coverage of every non-checksum file. All seven portable-source hashes and declared Study V1 artifact hashes also matched. The repeat-safe verifier’s read-only assertions were independently reproduced without executing the bundled scripts. No artifact alteration was identified.
---
## CWXR02 — Exact 17 × 109 pair universe
Verify exactly 17 canonical requirements, exactly 109 semantic units, and complete Cartesian accounting of exactly 1,853 requirement-to-semantic-unit pairs.
CWXR02 decision: `PASS`
CWXR02 reviewer notes: Independent recounting confirmed exactly 17 unique canonical requirements and 109 unique semantic units. The pair matrix contains exactly 1,853 unique `(requirement_id, semantic_unit_id)` records, equal to `17 × 109`. Every Cartesian combination appears exactly once, with no missing or duplicate pairs. Requirement and semantic-unit ordinals and source anchors are consistent with their respective inventories.
---
## CWXR03 — Pair-classification conservatism
Verify all 1,853 pair records are `UNRESOLVED_BINDING` and that no pair was promoted without authorized evidence to `SUPPORTED_BINDING` or `NOT_SUPPORTED_BINDING`.
CWXR03 decision: `PASS`
CWXR03 reviewer notes: All 1,853 pair records are classified as `UNRESOLVED_BINDING`; none is classified as `SUPPORTED_BINDING` or `NOT_SUPPORTED_BINDING`. No record promotes lexical similarity, field-class relations, historical carrier state, open-string capacity, human semantic judgment, or absence of positive evidence into a binding conclusion. All checked positive-binding, negative-exclusion, reclassification, schema-mapping, carrier-admissibility, and operational-authority flags are false.
---
## CWXR04 — Requirement-level rollups
Verify all 17 requirement rollups are `UNRESOLVED` and conform to the authorized rollup rules.
CWXR04 decision: `PASS`
CWXR04 reviewer notes: All 17 canonical requirements have exactly one rollup classified as `UNRESOLVED`. Each rollup accounts for all 109 semantic-unit pairs: zero `SUPPORTED_BINDING`, zero `NOT_SUPPORTED_BINDING`, and 109 `UNRESOLVED_BINDING`. This conforms to the authorized rule that any unresolved pair requires the corresponding requirement rollup to remain unresolved. No positive crosswalk or exhaustive negative proof is claimed.
---
## CWXR05 — Provenance and bounded semantic-unit-domain authority
Verify exact requirement provenance, semantic-unit source identity, and bounded 109-unit-domain authority without overstating global approval or requirement-to-unit pair evidence.
CWXR05 decision: `PASS`
CWXR05 reviewer notes: The canonical requirement inventory is byte-exact to its portable provenance source and contains 17 `BOUND_EXACT` records. The Study V1 semantic-unit inventory is byte-exact to its portable source and contains 109 unique units; the traceability artifact contains the same 109-unit identity set. Pair and provenance records bind the corresponding source hashes correctly. Decision 0109 limits authority to the 109-unit domain used by the reviewed relation-informed study and does not grant global semantic-role-formalization approval or establish requirement-to-unit pair bindings.
---
## CWXR06 — Historical-state and technical-boundary preservation
Verify the historical 18,639 semantic-unit-to-Schema-V2-path matrix remains read-only and that no carrier-admissibility, operational-mapping, Schema-V2-losslessness, negative-mapping-impossibility, or whole-V4-exhaustiveness conclusion is improperly inferred.
CWXR06 decision: `PASS`
CWXR06 reviewer notes: The supplied historical matrix matches its declared SHA-256 and retains 18,639 records across 109 semantic units and 171 Schema-V2 property paths. Every historical record remains `UNRESOLVED`, and Study V1 identifies the matrix as read-only with no reclassification performed. The artifacts consistently avoid inferring carrier admissibility, operational mapping, Schema-V2 losslessness, negative mapping impossibility, or whole-V4 exhaustiveness. All corresponding nonclaim and nonauthorization boundaries are preserved.
---
## CWXR07 — Decision-0147 A02 lifecycle
Verify Decision-0147 A02 was consumed exactly once, its PASS output is preserved byte-exactly in Study V1, its lifecycle is `PERMANENTLY_RETIRED`, and no rerun occurred.
CWXR07 decision: `REVISION_REQUIRED`
CWXR07 reviewer notes: The preserved A02 output’s SHA-256 and byte size match the consumption record. The output contains the recorded PASS marker, and the record consistently states return code 0, execution count 1, `PERMANENTLY_RETIRED`, and `rerun_authorized = false`.
However, the ZIP does not include the original Decision-0147 A02 script, sealed repository history, or an independent tamper-evident execution audit. It therefore verifies preservation and internal consistency of the lifecycle record but cannot independently establish that A02 was executed exactly once or that no rerun occurred. Supply independently reviewable lifecycle evidence or narrow this criterion to verification of the preserved record.
---
## CWXR08 — Global result and governance boundaries
Verify the global author-candidate result `FURTHER_EVIDENCE_REQUIRED`, the requirement for independent human review, and all operational non-authorizations.
CWXR08 decision: `PASS`
CWXR08 reviewer notes: The study manifest, pair matrix, requirement rollups, accounting summary, Decision-0148 copy, and review-package manifest consistently report 1,853 `UNRESOLVED_BINDING` pairs, 17 `UNRESOLVED` requirement rollups, and the global author-candidate result `FURTHER_EVIDENCE_REQUIRED`. Independent human review remains required, and Study V1 is not governance-adopted. All stated non-authorizations—including pair or historical reclassification, operational mapping, Schema-V2 modification, schema-successor authoring, Schema V3, `curl.json`, analyzer or baseline execution, and repair—are preserved.
---
# Overall independent human-review decision
Overall decision: `REVISION_REQUIRED`

Reviewer name: Abdul Raheem Shahzad
Reviewer role: Spec-Technical-Reviewer-1
Reviewer confirmation/signature: ARS
Review date:25 / August / 2026

Overall reviewer notes:
CWXR01–CWXR06 and CWXR08 pass. The supplied evidence supports the study’s conservative `FURTHER_EVIDENCE_REQUIRED` result, complete 17 × 109 pair accounting, unresolved classifications and rollups, source bindings, historical-state preservation, and governance boundaries.
CWXR07 requires revision because the ZIP verifies a consistent, byte-preserved A02 lifecycle record but lacks independent evidence sufficient to establish the stronger claim that Decision-0147 A02 executed exactly once and was never rerun. Provide sealed repository history or equivalent tamper-evident execution evidence, or narrow CWXR07 to verification of the preserved lifecycle record.