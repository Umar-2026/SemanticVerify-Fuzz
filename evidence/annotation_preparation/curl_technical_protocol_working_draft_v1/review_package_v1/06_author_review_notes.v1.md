# curl Technical Protocol Working Draft V1 — Author Review Notes

## Status

This is an author-side technical working draft.

It is not the canonical `curl.json` protocol specification.

Independent human technical-specification review is required before any
canonicalization.

## Core representation

The draft separates four protocol dimensions:

1. global runtime readiness;
2. explicit global-cleanup obligation;
3. easy-handle lifetime plus multi membership;
4. multi-handle lifetime plus post-error uncertainty.

This separation is intentional.

In particular, implicit global readiness established by `curl_easy_init` is
not treated as identical to the explicit cleanup obligation established by a
successful explicit `curl_global_init`.

## Important source-grounded rules

- successful non-NULL `curl_easy_init` creates a caller-owned easy resource;
- `curl_easy_perform` is prohibited while that easy is attached to a multi;
- a failed `curl_easy_perform` does not release the easy resource;
- successful add attaches an easy to a multi without transferring ownership;
- successful remove detaches it and re-enables easy-interface use;
- transfer completion alone does not detach the easy;
- non-`CURLM_OK` `curl_multi_perform` establishes a post-error uncertain
  condition;
- `curl_multi_cleanup` does not discharge individual easy cleanup obligations.

## Conservative treatment of unresolved normative questions

The draft deliberately does not force unresolved source wording into an
enforceable `MUST`.

Six items are therefore explicitly review-required:

- NR01 — outstanding explicit global cleanup obligation at exit;
- NR02 — multi cleanup while easy handles remain attached;
- NR03 — plain multi-perform repetition after a multi error;
- NR04 — runtime state after uninitialized `curl_easy_init` returns NULL;
- NR05 — wrong-multi remove classification;
- NR06 — premature global cleanup while live resources remain.

Where one of these controls the result, the draft uses `UNKNOWN`.

## Verdict discipline

`VIOLATION-MAY` represents feasible path/state uncertainty.

It must not be used as a substitute for unresolved normative strength.

Normative-strength uncertainty is represented as `UNKNOWN` until independent
technical review resolves it.

`UNKNOWN` must never be converted to `VALID`.

## Quarantine

No generated-driver source, selected-sample membership, raw model response,
compiler-log semantic content, gold label, analyzer output, baseline output,
LLM-review output, or repair output was used to author this draft.

## Next boundary

Package this exact immutable author checkpoint for independent human
technical-specification review.

Do not canonicalize `curl.json` before that review.
