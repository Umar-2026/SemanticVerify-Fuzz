# D0250 C2 Bounded Candidate Content Acquisition Authorization V1

Status: `AUTHORIZED — NOT EXECUTED`

D0250 authorizes only D0241 C2 bounded additional evidence acquisition over the exact ten immutable Git blob identities bound by frozen D0249.

Designated execution decision: `D0251`.

`C2_AUTHORIZED=YES`
`C2_EXECUTED=NO`

D0251 may read exactly ten bound Git blob objects, each exactly once, and materialize exactly ten byte-for-byte detached snapshots.

No D0251 source blob is read by D0250.

`D0251_SOURCE_BLOB_READ_EXECUTED=NO`
`D0251_C2_ACQUISITION_EXECUTED=NO`

D0251 acquisition may compute snapshot SHA-256 and byte counts and must preserve exact Git blob identity.

D0251 does not authorize semantic interpretation or adjudication.

`C3_AUTHORIZED=NO`
`SOURCE_AUTHORITY_ADJUDICATION_AUTHORIZED=NO`
`CROSSWALK_SEMANTIC_ADJUDICATION_AUTHORIZED=NO`
`CANDIDATE_ADMISSIBILITY_ADJUDICATION_AUTHORIZED=NO`

`B2_READINESS_ESTABLISHED=NO`
`B2_AUTHORIZED=NO`
`B2_EXECUTED=NO`

No root re-enumeration, repository-wide search, Git-history search, or network access is authorized.

Next required checkpoint:

`INDEPENDENT_READ_ONLY_VERIFY_D0250_BEFORE_ANY_D0251_SOURCE_BLOB_READ`
