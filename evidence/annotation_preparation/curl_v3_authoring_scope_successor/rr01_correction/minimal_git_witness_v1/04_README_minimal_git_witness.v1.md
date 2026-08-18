# curl V3 RR01 Minimal Git Object Witness V1

## Purpose

This artifact provides independently resolvable Git object evidence for the
curl V3 RR01 re-review.

It intentionally does **not** contain the full research repository or full Git
history.

## Exact contents

The witness contains exactly:

- 2 commit objects;
- 6 tree objects;
- 2 file blob objects.

The only file blobs are:

1. exact curl V3 scope blob:
   `931c24cc46c99f23ee352455d3e8c93e57e63401`

2. exact Decision 0024 blob:
   `ca72e87d5668c649eb64db8fc04f457eeebc5d0c`

Parent commit objects and unrelated file blobs are intentionally absent.

## Reviewer verification

Extract:

`02_curl_v3_rr01_minimal_git_witness.v1.tar.gz`

The extracted bare Git repository is:

`curl-v3-rr01-minimal.git`

Resolve the exact V3 author tree:

`git --git-dir=curl-v3-rr01-minimal.git rev-parse 7de6fc01797ae68cbd64406b850a3198f71cc702^{tree}`

Expected:

`c5f96b844e5803cccd04c9f64a55754dc6c77e20`

Resolve the exact V3 target blob:

`git --git-dir=curl-v3-rr01-minimal.git rev-parse 7de6fc01797ae68cbd64406b850a3198f71cc702:config/annotation/curl_v3_authoring_scope.v3.json`

Expected:

`931c24cc46c99f23ee352455d3e8c93e57e63401`

Compute its content SHA-256:

`git --git-dir=curl-v3-rr01-minimal.git cat-file blob 931c24cc46c99f23ee352455d3e8c93e57e63401 | sha256sum`

Expected:

`ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb`

The same witness also independently binds Decision 0024.

## Quarantine

This witness does not provide generated-driver, gold-label, analyzer-output,
baseline-output, LLM-review-output, or repair-output file blobs.

It is binding evidence only.

It does not authorize V3 scope freeze or any downstream implementation step.
