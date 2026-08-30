# Decision0187 Recording-Authorization Boundary V1

## Authorized next transaction

Exactly one subsequent transaction may execute the Decision0187 A02
authorization verifier and, if and only if that verifier returns PASS, record
the returned human technical-adjudication packet byte-exactly as new immutable
repository evidence.

External returned packet:

`/openbayes/home/50_bounded_technical_adjudication_Nadeem_packet.MANUAL_ADJUDICATION_COPY.v1.md`

Expected SHA-256:

`ad35ddfefea1d79db79e36f24ef823407f977a682efcdf23a98a1cbc5ffd7eda`

Expected size:

`316649` bytes.

The returned packet contains 211 candidate pairs and records 211
`TECHNICAL_SUPPORT_CONFIRMED_PROMOTION_CANDIDATE` technical-adjudication
states.

## This authorization does not itself perform recording

At Decision0187:

- returned packet recording completed: NO;
- A02 executed: NO;
- human evidence promoted into governed pair classifications: NO;
- pair reclassification authorized: NO;
- automatic promotion authorized: NO;
- `SUPPORTED_BINDING` creation authorized: NO;
- `NOT_SUPPORTED_BINDING` creation authorized: NO;
- operational mapping authorized: NO;
- schema change authorized: NO;
- schema successor authorized: NO;
- `curl.json` authorized: NO;
- analyzer implementation/execution authorized: NO;
- baseline execution authorized: NO;
- repair authorized: NO.

## One-time verifier lifecycle

`02_authorize_single_recording_transaction.v1.py` is authored here but MUST
NOT be executed during Decision0187.

It is authorized for exactly one execution in the immediately subsequent
recording transaction.

After that execution it is permanently retired regardless of the subsequent
recording transaction outcome.

Rerun authorization: NO.

Historical and previously retired one-time verifiers remain retired and MUST
NOT be rerun, including Decision0185 A02.
