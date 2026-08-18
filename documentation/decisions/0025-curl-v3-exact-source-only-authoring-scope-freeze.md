# Decision 0025: curl V3 Exact Source-Only Authoring-Scope Freeze

## Status

Completed separate source-only authoring-scope freeze for the exact,
independently approved curl V3 scope.

This decision records the freeze operation only.

It does **not** itself authorize technical protocol working-draft authoring.

## Exact frozen scope

Path:

`config/annotation/curl_v3_authoring_scope.v3.json`

SHA-256:

`ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`

Original immutable author checkpoint commit:

`7de6fc01797ae68cbd64406b850a3198f71cc702`

Original immutable author checkpoint tree:

`c5f96b844e5803cccd04c9f64a55754dc6c77e20`

Git blob:

`931c24cc46c99f23ee352455d3e8c93e57e63401`

The scope bytes are unchanged from the exact V3 object reviewed and approved
by the independent human reviewer.

## Human authorization binding

The completed RR01 independent human re-review is recorded at repository
commit:

`15a1c5ce6e5f9ee32456ca55550b8e5879d9b66a`

with tree:

`dd06610552e979a8472aceed763227421c490670`

The exact completed human-review file has SHA-256:

`ed5707f6b54a89123f0c59b136a15feb5e62cec3e0e645df08737051bfab169b`

The human decisions were:

- RR01-R1: `PASS`
- RR01-R2: `PASS`
- RR01-R3: `PASS`
- RR01-R4: `PASS`
- Overall: `APPROVE_EXACT_V3_SCOPE_FOR_FREEZE`

That approval authorized this separate freeze operation.

## Freeze semantics

This freeze establishes that the following exact object is the frozen curl V3
source-only authoring scope:

`7de6fc01797ae68cbd64406b850a3198f71cc702`

→ tree

`c5f96b844e5803cccd04c9f64a55754dc6c77e20`

→ path

`config/annotation/curl_v3_authoring_scope.v3.json`

→ blob

`931c24cc46c99f23ee352455d3e8c93e57e63401`

→ SHA-256

`ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`

No V3 bytes are modified by this freeze.

Any future change to the frozen scope requires a new immutable successor. The
V3 scope MUST NOT be edited in place.

## Current authorization boundary

After completion of this freeze:

- V3 scope-freeze authorized: YES;
- V3 scope frozen: YES;
- technical working-draft authoring authorized: NO;
- canonical curl protocol specification authorized: NO;
- generated-driver inspection authorized: NO;
- gold annotation authorized: NO;
- analyzer implementation/execution authorized: NO;
- baseline execution authorized: NO;
- repair authorized: NO.

The completed freeze satisfies the prerequisite that must exist before
technical curl working-draft authoring **may subsequently be authorized**.

It does not automatically grant that downstream authorization.

## Quarantine

The existing source-only quarantine remains in force. No generated-driver
source, selected-sample membership, raw model response, compiler-log semantic
content, gold labels, analyzer output, baseline output, controlled LLM-review
output, or repair output is authorized or introduced by this freeze.

## Next boundary

Evaluate and record the separate post-freeze authorization for technical curl
protocol working-draft authoring.

Until that separate authorization is recorded, technical working-draft
authoring remains prohibited.
