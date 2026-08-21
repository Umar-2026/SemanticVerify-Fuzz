# Decision 0058 — Record Human Approval of Schema V2 Activation-Governance Package

## Reviewed package

The exact reviewed activation-governance package is:

`evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_governance_package_v1`

Commit:

`30840f40d2b76d50ad543f43621641eb43016ad2`

Tree:

`b36673ffb10c440ca5e6da77a9ef28cdb5b8cf9c`

Immediate parent:

`f48fe86761ed5687d7a6e311b5b617363b141b4c`

Package manifest SHA-256:

`5338a5347ce73dbf6420e4c7eb5c1c87c0fbcee41598888d84c531034eedd71c`

Package checksum-manifest SHA-256:

`ef528e002fed0db3cb1faa99642898f3053cd3e4d326763d2cc8e26d028b82a7`

## Completed independent human review

Exact completed review SHA-256:

`2b5421a0466bdec575e87f035fb303c8ed1b610bc242c14a977870b4b87d2109`

Size:

`7345` bytes

Reviewer role:

`Spec-Technical-Reviewer-1`

Reviewer:

`Abdul Raheem Shahzad`

Recorded confirmation:

`ARS`

Review date:

`21 / August / 2026`

All nine activation-governance review items are PASS:

`9 PASS / 0 REVISION_REQUIRED / 0 FAIL`

Overall decision:

`APPROVE_SCHEMA_V2_ACTIVATION_GOVERNANCE_PACKAGE`

## Approved review candidates

The approved package contains the following exact review candidates.

### Schema V2 hash/canonicalization contract

SHA-256:

`8fa63b0faea168e7dcc7701d94704d408dbd8d22e5d17d6c83cc3ab90095aab0`

Size:

`3126` bytes

### V1/V2 version-dispatch policy

SHA-256:

`5a91a9938af7029edff6b91b8b624b2f0712680d49fad3abd1be29e649944bce`

### Decision 0019 successor

SHA-256:

`8665163eb5d4f7a8718ba3ed2d3973ba928fea85789c23696599a2d6ea02bbb3`

These are approved as components of the activation-governance package.

They are not made active by this decision.

## Decision

The exact immutable Schema V2 activation-governance package is now recorded as
having received independent human approval.

No revision of AG01 through AG09 is required.

## Critical distinction: package approval is not Schema V2 activation

This decision records the completed human review only.

It does **not**:

- activate Schema V2;
- create or install
  `config/protocol_content_hash_canonicalization.v2.json`;
- modify Decision 0019 in place;
- supersede Decision 0019;
- adopt the proposed Decision-0019 successor;
- activate the proposed version-dispatch policy;
- define or authorize positive V4-to-V2 mapping;
- create `config/protocol_specifications/curl.json`;
- authorize analyzer implementation or execution;
- authorize baseline execution;
- authorize repair.

## Required next boundary

Before any Schema V2 activation, a separate read-only repository-bound
activation preflight must establish that:

1. the exact approved Schema V2 candidate remains unchanged;
2. this exact completed activation-governance human approval remains bound;
3. the exact reviewed V2 hash-contract candidate remains unchanged;
4. the exact reviewed version-dispatch policy remains unchanged;
5. the exact reviewed Decision-0019 successor remains unchanged;
6. frozen zlib/libpcap remain unchanged;
7. the active V2 hash path remains absent before activation;
8. curl.json remains absent;
9. activation can be performed atomically without implying positive V4-to-V2
   mapping or downstream analyzer/baseline/repair authorization.

## Next boundary

`PREFLIGHT_SCHEMA_V2_ACTIVATION_DECISION`
