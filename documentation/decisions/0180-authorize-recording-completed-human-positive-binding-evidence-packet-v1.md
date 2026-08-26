# Decision 0180 — Authorize Recording of Completed Human Positive-Binding Evidence Packet V1

## Decision

Authorize one narrowly bounded next transaction to record the exact returned
human positive-binding evidence packet as an immutable repository evidence
record.

This is an authorization decision only. No returned packet is recorded by
Decision0180.

## Authorized returned packet

External path:

`/openbayes/home/50_positive_binding_evidence_manually_packet.MANUAL_REVIEW_COPY.v1.md`

Exact SHA-256:

`effd2848702219741e3814d2dc283284c92ab07f49980cd799fde351ecb8b685`

Exact size:

`20425` bytes.

The immediately preceding read-only validation established:

- 17 requirement sections;
- 109 governed semantic units in the validation domain;
- 15 requirements recording `POSITIVE_BINDING_PROPOSED`;
- 2 requirements recording `UNRESOLVED_NO_POSITIVE_BINDING_PROPOSED`;
- 211 proposed requirement-to-semantic-unit references;
- zero unknown semantic-unit IDs;
- zero positive proposals lacking rationale;
- zero invalid evidence states;
- zero unresolved sections containing unit proposals;
- exact static-prefix preservation;
- completed human reviewer fields and attestation.

These are properties of the returned candidate evidence packet. They are not
governed pair reclassifications.

## Authorized next transaction

A separately governed successor transaction may:

1. execute the Decision0180 A02 verifier exactly once;
2. permanently retire that verifier after its single execution;
3. record the exact returned packet bytes as an immutable repository artifact;
4. bind the immutable record to the returned packet SHA-256 and size;
5. author recording metadata, checksum closure, and a safe verifier;
6. author a separate recording decision.

No semantic judgment may be added, deleted, rewritten, normalized, inferred,
or substituted while recording the returned packet.

## Interpretation boundary

The returned packet is candidate human evidence only.

`POSITIVE_BINDING_PROPOSED` entries do not themselves reclassify governed
requirement-to-semantic-unit pairs.

`UNRESOLVED_NO_POSITIVE_BINDING_PROPOSED` is not negative proof and does not
establish `NOT_SUPPORTED_BINDING`, mapping impossibility, or carrier
impossibility.

Recording the packet does not constitute technical adjudication or governance
promotion of any proposed pair.

## Explicitly not authorized

Decision0180 does not authorize:

- governed pair reclassification;
- `NOT_SUPPORTED_BINDING`;
- technical adjudication of the reviewer proposals;
- operational requirement-to-semantic-unit mapping;
- Schema V2 modification;
- a Schema V2 successor;
- `curl.json`;
- analyzer implementation;
- analyzer execution;
- baseline execution;
- repair implementation;
- repair execution.

## One-time verifier lifecycle

`02_verify_recording_authorization_once.v1.py` is authored in this decision but
must not be executed during Decision0180.

Its state at the end of Decision0180 must be:

`ACTIVE_UNCONSUMED`

Its only authorized execution transaction is Decision0181.

After the first authorized execution it is permanently retired and must never
be rerun.

## Next boundary

`CONSUME_DECISION0180_A02_EXACTLY_ONCE_AND_RECORD_EXACT_RETURNED_HUMAN_POSITIVE_BINDING_EVIDENCE_PACKET_V1`
