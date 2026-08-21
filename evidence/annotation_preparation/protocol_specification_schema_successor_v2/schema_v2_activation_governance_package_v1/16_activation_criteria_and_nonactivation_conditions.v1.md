# Schema V2 Activation Criteria and Non-Activation Conditions

## Required before activation

Schema V2 may be marked active only after all of the following are true:

1. the exact approved Schema V2 candidate remains byte-identical;
2. AG01 through AG09 receive independent human PASS decisions;
3. the proposed Decision 0019 successor/version-dispatch semantics are
   independently approved;
4. the proposed V2 hash/canonicalization contract is independently approved;
5. a later explicit activation decision installs or binds the exact approved
   V2 hash contract;
6. a later explicit activation decision adopts the reviewed version-dispatch
   rule;
7. frozen zlib and libpcap remain unchanged;
8. activation and positive V4-to-V2 mapping remain separate decisions.

## Mandatory non-activation conditions

Do not activate if any AG01-AG09 item is REVISION_REQUIRED or FAIL.

Do not activate if the Schema V2 bytes change.

Do not activate if Decision 0019 would need silent reinterpretation rather
than an explicit successor decision.

Do not activate if the V2 hash contract remains ambiguous or unreviewed.

Do not activate if activation would require rewriting zlib or libpcap.

Do not activate if the process implicitly assumes a positive curl V4-to-V2
mapping.

## Explicit downstream boundary

Even successful Schema V2 activation would only make V2 an eligible canonical
representation schema.

It would not itself:

- define or approve curl technical-V4 → Schema-V2 semantic mapping;
- create curl.json;
- authorize analyzer implementation or execution;
- authorize baseline execution;
- authorize repair.
