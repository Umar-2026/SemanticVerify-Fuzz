# Decision 0084 — Record Existing-Schema-V2 Multi-Field Capability Study V1 Author Checkpoint

Status: AUTHOR CANDIDATE RECORDED — INDEPENDENT HUMAN REVIEW REQUIRED

## Authorization

Decision 0083 authorized authoring of the exhaustive admissible
existing-Schema-V2 multi-field capability study only.

Its pre-study authorization verifier ran its final allowed time immediately
before Capability Study V1 authoring.

Final verifier file SHA-256:

`5f2cfa2a25fb70d9e804b5dfb93519fad63414c424ff408bbf491337043c1555`

Final verifier output SHA-256:

`e6eb4748bdf804153be96498a8b8309a9f07a5d415b712281bf70cfd2174abcd`

That verifier is now permanently retired and must never be rerun.

## Capability Study V1

Study JSON SHA-256:

`9bf685bcd5d8286938f4e221bffd2cc1acc8b5da961d3b0e14f1b10a6a43b78b`

Semantic-unit inventory SHA-256:

`2b39f5625658e41aeb906a1db8a4a472d9265dc3654572e60374827f0ce7fa7d`

Schema-V2 carrier inventory SHA-256:

`0f32fb87e1396da8c37e3f74c41059560338346ae54f29df0c2d38d72deb1d6d`

Candidate multi-field composition matrix SHA-256:

`c064cfa8c7143b537dc3bb54b8af353f56bafba3e415e7ccdb2c17efaff30d45`

Study Markdown SHA-256:

`7976e9d079a1df6ef20f183f37a290398a6214079a5b08674aa9ea68b25c600c`

Study checksum-manifest SHA-256:

`68d2a28fb99b3fbb4df2e93ddd7569efb97a35367e08ec823afd9e89fc5848b2`

## Complete inventory results

Capability Study V1 inventories:

- all 10 curl-V4 semantic containers;
- 109 V4 semantic units;
- the complete V4 leaf-field surface;
- all 57 V4 semantic field classes used by the capability screening;
- all 64 V4 rule records;
- all 3 V4 exit obligations;
- all 10 V4 representation-policy fields;
- all 171 active Schema-V2 recursive property paths;
- all 123 distinct Schema-V2 property names; and
- all 7 required Schema-V2 carrier families.

The study also confirms 64/64 enforcement-bearing rules and 15 distinct
enforcement classifications.

Under the explicit rule-only grouping recomputed by this study, there are
2 verdict-to-enforcement ambiguity groups and 2 defect+verdict-to-enforcement
ambiguity groups.

## Author-candidate outcome

Capability Study V1 selects:

`FURTHER_EVIDENCE_REQUIRED`

This result is not yet human-approved.

## Why a positive existing-V2 path is not proven

The study identifies multiple structured direct and multi-field candidate
carrier compositions, but no complete constructive witness yet covers every V4
semantic unit while simultaneously proving:

- deterministic exact forward encoding;
- deterministic exact reverse reconstruction;
- complete collision freedom; and
- semantic noninterference.

Therefore:

`PROVEN_ADMISSIBLE_EXISTING_SCHEMA_V2_MAPPING_PATH_AVAILABLE`

is not established.

## Why a negative existing-V2 path is not proven

The study exhaustively inventories the V4 semantic surface and Schema-V2
carrier surface, and screens every V4 field class and semantic unit.

However, the reviewed admissibility contract uses the semantic criterion
"semantically related carriers only" without a complete machine-readable
relation enumerating every admissible multi-field composition.

Schema V2 also contains open string-valued semantically typed carriers.

Consequently, the admissible composition space cannot currently be
machine-enumerated and exhaustively eliminated.

Therefore:

`PROVEN_NO_ADMISSIBLE_EXISTING_SCHEMA_V2_MAPPING_PATH_UNDER_REVIEWED_CONSTRAINTS`

is not established.

Absence of a same-named Schema-V2 property is not treated as an impossibility
proof.

## Central unresolved exactness classes

At minimum, the study retains as unresolved:

- enforcement;
- normative-strength uncertainty preservation;
- resource-centered semantics; and
- synthetic-protocol-event non-invention.

Additional rule/exit metadata exactness questions are recorded in the study
matrix.

## Governance effect

Decision 0084 records the author checkpoint only.

Capability Study V1 requires independent human technical review before its
result can affect subsequent governance.

Decision 0084 does not authorize:

- an operational positive V4-to-V2 mapping contract;
- schema-successor authoring;
- Schema V3;
- successor-version preselection;
- curl.json materialization;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## Next boundary

Separately authorize an independent human technical review package for
Capability Study V1.
