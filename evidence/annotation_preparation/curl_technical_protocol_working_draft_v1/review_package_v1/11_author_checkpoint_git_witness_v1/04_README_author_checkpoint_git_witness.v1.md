# curl Technical Working Draft V1 — Minimal Git Witness

This witness permits independent verification of the exact immutable author
checkpoint without exposing unrelated repository file blobs.

It contains exactly:

- 1 commit object;
- 5 tree objects;
- 2 file blobs.

The only file blobs are:

1. the exact curl Technical Protocol Working Draft V1;
2. Decision 0027.

The parent commit object and unrelated file blobs are intentionally absent.

Run:

`python3 03_verify_author_checkpoint_git_witness.v1.py`

Expected final marker:

`CURL_TECHNICAL_V1_AUTHOR_GIT_WITNESS_VERIFICATION=PASS`
