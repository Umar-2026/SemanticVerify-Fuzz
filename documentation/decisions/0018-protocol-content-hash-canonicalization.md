# Decision 0018: Protocol Content-Hash Canonicalization

Status: Accepted

## Context

The frozen protocol-specification schema requires `content_sha256` at both
the specification level and obligation-rule level. Provenance evidence also
requires a `content_sha256`.

A pre-draft audit found that the repository already uses deterministic
canonical JSON serialization in other executable integrity contracts, but
the protocol-specification artifacts did not define whether their own
`content_sha256` fields are included or excluded when calculating those
hashes.

Direct inclusion would be self-referential. No previously frozen
library-specific protocol specification exists whose historical hash
semantics must be preserved.

This decision therefore freezes an additive deterministic clarification
before the first library-specific protocol specification is authored.

## Canonical JSON byte representation

For protocol object hashing, canonical JSON bytes are:

- UTF-8 encoding;
- `ensure_ascii = false`;
- keys sorted lexicographically;
- JSON separators exactly `(",", ":")`;
- no insignificant whitespace;
- no trailing newline;
- non-finite JSON numbers are prohibited.

Equivalent Python serialization is:

`json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")`

## Provenance evidence hash

For every provenance record, `content_sha256` is:

SHA-256 of the exact bytes of the cited approved pinned source artifact
identified by `path_or_url`.

It is a source-artifact byte hash, not a hash of the provenance JSON record
and not a hash of a quoted excerpt.

Line/range descriptions may identify relevant evidence, but they do not
change the file-byte hash.

## Obligation-rule hash

For an obligation object:

1. make a shallow semantic copy of the complete obligation object;
2. remove only that object's own `content_sha256` field;
3. canonicalize the remaining obligation object using the canonical JSON
   byte representation above;
4. set `content_sha256` to SHA-256 of those canonical bytes.

All other required fields, including authorship, dates, revision,
provenance references, ownership effect, cleanup responsibility, defect
category, severity, and transition identifiers, participate in the hash.

The hash field is omitted, not replaced with null, zeroes, or an empty
string.

## Top-level specification hash

For a complete protocol specification:

1. make a shallow semantic copy of the complete specification object;
2. remove only the top-level specification `content_sha256` field;
3. retain all nested obligation `content_sha256` values and provenance
   source `content_sha256` values;
4. canonicalize the remaining specification using the canonical JSON byte
   representation above;
5. set the top-level `content_sha256` to SHA-256 of those canonical bytes.

Therefore a change to any nested obligation hash, provenance source hash,
state, event, transition, date, author, reviewer, revision, or other
included specification field changes the top-level specification hash.

## Draft versus frozen artifact

This rule does not convert a working draft into a frozen specification.

Pre-review working material may exist outside the canonical frozen
specification path. A canonical library-specific protocol specification is
hashed only after:

- source-only authoring is complete;
- required reviewer checks are complete;
- author and reviewer identities are fixed;
- creation and freeze dates are fixed;
- all obligation contents are final;
- all provenance source hashes are fixed.

Obligation hashes are then computed first, followed by the top-level
specification hash.

## Scope

This decision defines only deterministic hash semantics.

It does not:

- author a zlib protocol rule;
- inspect generated drivers;
- start gold annotation;
- release annotation packets;
- implement or execute SemanticVerify-Fuzz;
- run baselines;
- run controlled LLM review;
- implement repair.

The generated corpus remains outside the specification-authoring evidence
boundary.
