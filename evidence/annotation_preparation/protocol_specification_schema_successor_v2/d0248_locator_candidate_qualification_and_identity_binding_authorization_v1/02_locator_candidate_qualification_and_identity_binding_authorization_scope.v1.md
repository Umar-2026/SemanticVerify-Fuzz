# D0248 Metadata-Only Locator Candidate Qualification and Identity Binding Authorization V1

Status: `AUTHORIZED — NOT EXECUTED`

D0248 authorizes D0249 to perform metadata-only identity qualification over exactly the ten lexical candidates frozen by D0247.

The only permitted comparison is between committed candidate metadata and already-governed D0246 anchor metadata.

`D0249_DESIGNATED_EXECUTION_DECISION=YES`
`D0249_QUALIFICATION_EXECUTION_AUTHORIZED=YES`
`D0249_QUALIFICATION_EXECUTED=NO`

Permitted relation values are only:

`EXACT_BOUND_ANCHOR_MEMBER_IDENTITY`

and

`NO_BOUND_ANCHOR_IDENTITY_MATCH`

An exact bound-anchor identity requires the same root ID, exact candidate locator equal to the bound anchor path, and exact candidate Git object ID equal to the bound anchor Git blob.

`D0249_EXPECTED_CANDIDATE_COUNT=10`
`D0249_EXPECTED_EXACT_BOUND_ANCHOR_MEMBER_IDENTITY_COUNT=3`
`D0249_EXPECTED_NO_BOUND_ANCHOR_IDENTITY_MATCH_COUNT=7`

This authorization does not permit candidate-content inspection.

`D0249_CANDIDATE_CONTENT_OPEN_AUTHORIZED=NO`
`D0249_CANDIDATE_BLOB_READ_AUTHORIZED=NO`
`D0249_CANDIDATE_FILE_BYTE_HASH_AUTHORIZED=NO`
`D0249_CANDIDATE_JSON_PARSE_AUTHORIZED=NO`
`D0249_CANDIDATE_MARKDOWN_READ_AUTHORIZED=NO`
`D0249_CANDIDATE_PYTHON_READ_AUTHORIZED=NO`
`D0249_CANDIDATE_MANIFEST_READ_AUTHORIZED=NO`

`D0249_SOURCE_ROOT_REENUMERATION_AUTHORIZED=NO`
`D0249_REPOSITORY_WIDE_SEARCH_AUTHORIZED=NO`
`D0249_GIT_HISTORY_SEARCH_AUTHORIZED=NO`
`D0249_EXTERNAL_NETWORK_ACCESS_AUTHORIZED=NO`

The relation `NO_BOUND_ANCHOR_IDENTITY_MATCH` is not proof that a candidate is non-authoritative, non-crosswalk, irrelevant, or otherwise semantically negative.

The relation `EXACT_BOUND_ANCHOR_MEMBER_IDENTITY` establishes only identity with an already-governed anchor. It does not establish a Class06 crosswalk source, source authority for C2, crosswalk semantics, or C2 readiness.

`C2_AUTHORIZED=NO`
`C2_EXECUTED=NO`
`C3_AUTHORIZED=NO`

`B2_READINESS_ESTABLISHED=NO`
`B2_AUTHORIZED=NO`
`B2_EXECUTED=NO`

Next required checkpoint:

`INDEPENDENT_READ_ONLY_VERIFY_D0248_BEFORE_ANY_D0249_METADATA_QUALIFICATION_EXECUTION`
