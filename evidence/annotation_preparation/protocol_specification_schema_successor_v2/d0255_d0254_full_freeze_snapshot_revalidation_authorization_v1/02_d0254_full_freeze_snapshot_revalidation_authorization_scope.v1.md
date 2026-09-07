# D0255 — D0254 Full-Freeze Snapshot Revalidation Authorization Scope

Role: authorization only.

D0255 authorizes D0256, and only D0256, to execute the committed D0254
safe verifier exactly once for structural and evidence-integrity
revalidation required before D0254 may be independently frozen.

## Corrected metadata binding

The authoritative C3 frozen-snapshot metadata universe is the complete
10-record D0251 candidate_content_snapshots array, exactly equal to the
D0253 adjudication input snapshot-record array.

Full-record universe SHA-256:
dbb16ce946761f76490f86ee7f72a8be3871a72f3ea3c3d25d28ffb67307d7b5

The D0254 candidate records intentionally carry only seven shared snapshot
binding fields. Their seven-field projection is separately bound by:

fe0ba4023b8f9dd9bfbf00b4056717229de4f420d6311053f9864e21b729206e

The full-record hash and seven-field projection hash are distinct hash
domains and must never be substituted for one another.

Recorded evidence-locator universe:
- count: 24
- LINE_RANGE: 24
- JSON_POINTER: 0
- BYTE_RANGE: 0
- SHA-256: a0e326368d63c350c1d18f0f8e8988047f9731079c330d71dcd814f7e102df97

## Authorized D0256 operation

D0256 may execute the committed D0254 safe verifier exactly once.
Snapshot bytes may be read only by that verifier during the designated
execution. No additional direct D0256 snapshot reads are authorized.

The verifier may independently check snapshot SHA-256, byte count,
raw Git blob identity, recorded evidence-locator bounds, and recorded
verdict-formula consistency.

## Not authorized

No C3 adjudication reexecution or semantic rejudgment is authorized.
No original source reopening, original candidate worktree read,
reference following, source-root reenumeration, repository search,
history search, network access, or snapshot Python execution/import is
authorized.

No C4, C5, C6, B2, active-schema materialization, analyzer, baseline,
or repair authorization is created.

D0256 remains blocked until D0255 receives a separate independent
read-only verified/frozen checkpoint.
