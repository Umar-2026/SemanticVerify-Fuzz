# Decision 0009: Gate 1C exact source/build freeze

- Status: Accepted
- Gate: Gate 1C
- Frozen at UTC: 2026-08-08T12:32:06+00:00

## Decision

Freeze the exact source identity and qualified build recipe for all eight
experimental libraries before any primary driver generation.

The final qualified set is 8/8 PASS. Source identity is bound by upstream
remote, tag, tag type, tag object where applicable, peeled commit, Git tree,
and deterministic qualification archive SHA-256.

The final build recipes are the exact recipes that were successfully
qualified with Clang/LLVM 14. curl and lcms use the dependency-stable V3
recipes. libpcap uses pinned Flex and Bison. libvpx uses pinned NASM with
explicit `--as=nasm`.

## Qualification history

The first build pass produced 6/8 PASS. libpcap failed because Flex/Lex was
not installed. libvpx failed because `--disable-asm` is not supported by the
pinned source. Those failures are preserved rather than erased.

The corrective V2 pass qualified libpcap and libvpx. V3 then removed
environment-sensitive optional dependency AUTO behavior from curl and lcms.

## Boundaries

This decision does not create library-specific protocol rules, does not
create any scenario binding, does not authorize primary generation, does not
authorize held-out driver inspection, and does not authorize analyzer or
repair implementation.

Repair remains prohibited until Gate V.
