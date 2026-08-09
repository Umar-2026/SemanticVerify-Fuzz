# Decision 0010: Primary postprocessing precedence and duplicate semantics

- Status: Accepted
- Gate: Post-Gate1 generation-opening control
- Prepared at UTC: 2026-08-09T07:22:20+00:00
- Frozen at UTC: 2026-08-09T07:36:50Z

## Context

The frozen Gate1 generation protocol defines exactly one terminal status for
each logical slot and fixes the allowed terminal-status vocabulary, but it
does not define a postprocessing precedence among extraction, duplicate
detection, and compilation.

This decision closes that ambiguity additively. It does not modify or
reinterpret the closed Gate1 freeze package.

## Decision

Primary postprocessing shall use the following deterministic order.

1. Apply the already-frozen transport and provider-response rules first.
   If the frozen protocol resolves the logical slot as `REFUSAL`, `TIMEOUT`,
   `API_ERROR`, `TRUNCATED_OUTPUT`, or `TRANSPORT_FAILURE`, that terminal
   status is final for the slot. Extraction, duplicate detection, and
   compilation are not performed.

2. For a complete response that is not already terminal under step 1,
   preserve the raw response before extraction.

3. Apply the provider-specific response parser. If a complete response
   cannot yield the required logical model-text string, assign
   `EXTRACTION_FAILURE`. Compilation is not performed.

4. Preserve successfully obtained model text verbatim. No Markdown-fence
   stripping, commentary stripping, whitespace trimming, source
   reformatting, include insertion, entrypoint insertion, or source repair
   is allowed.

5. If the logical model-text string is empty or contains only Unicode
   whitespace, assign `MISSING_CODE`. Compilation is not performed.

6. For non-empty successfully extracted source, compute and retain its
   source SHA-256 and byte length.

7. Perform deterministic duplicate detection only within the same frozen
   experimental task group:

       requested model ID + library + scenario ID

   Thus duplicate comparison is among the five replicate logical attempts
   belonging to that same model/library/scenario task.

8. The earliest successfully extracted occurrence in canonical logical-slot
   order is the canonical occurrence. A later source in the same task group
   is `DUPLICATE_OUTPUT` only when its preserved extracted source is exactly
   byte-identical to that earlier occurrence. SHA-256 and byte length may be
   used as the lookup key, with retained source bytes providing the
   byte-identity authority.

9. A `DUPLICATE_OUTPUT` slot is preserved, is not replaced, remains part of
   the fixed 800-slot denominator, records the canonical
   `duplicate_of_logical_slot_id`, and is not compiled.

10. Identical source observed across different models, libraries, or
    scenario IDs is not assigned the `DUPLICATE_OUTPUT` terminal status by
    this rule. Such cross-task identity may be recorded descriptively but
    does not alter the primary terminal status.

11. Only a unique, non-empty source with successful verbatim extraction and
    no upstream terminal status is eligible for primary compilation.

12. Primary compilation uses the separately frozen postprocessing
    compilation contract. A non-zero compiler/linker exit code yields
    terminal status `NON_COMPILATION` and compilation status
    `NON_COMPILATION`.

13. A zero compiler/linker exit code yields terminal status
    `RESPONSE_RECEIVED` and compilation status `COMPILED`. Compiler warnings
    are counted separately and do not change that terminal status.

## Terminal-status precedence

For postprocessing purposes the precedence is therefore:

    frozen upstream transport/provider terminal
        >
    EXTRACTION_FAILURE
        >
    MISSING_CODE
        >
    DUPLICATE_OUTPUT
        >
    NON_COMPILATION
        >
    RESPONSE_RECEIVED

This is a decision order, not a reordering or renaming of the frozen Gate1
terminal-status vocabulary.

## Compilation-status mapping

- Upstream terminal status: `NOT_ATTEMPTED`
- `EXTRACTION_FAILURE`: `NOT_ATTEMPTED`
- `MISSING_CODE`: `NOT_ATTEMPTED`
- `DUPLICATE_OUTPUT`: `NOT_ATTEMPTED`
- Compiler/linker non-zero: `NON_COMPILATION`
- Compiler/linker zero: `COMPILED`

The compilation denominator remains all 800 logical slots, as frozen in the
generation protocol. No failed, duplicate, missing, or non-compiling slot is
replaced.

## Boundaries

This decision does not authorize primary generation and does not open the
generation window.

It does not alter provider retry semantics, model targets, prompts, scenario
bindings, source revisions, or the closed Gate1 package.

It does not authorize execution of linked primary drivers, sanitizers,
libFuzzer, analyzer implementation or execution, held-out driver inspection,
or repair.

Repair remains prohibited until Gate V.
