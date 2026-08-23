# Decision 0096 — Authorize Post-Final-Authorization-Run Recovery for Corrective Successor Package V2

Status: NARROW RECOVERY AUTHORIZED — RECOVERY NOT YET EXECUTED

## Trigger

Decision 0095 authorized Corrective Successor Package V2 authoring.

The Decision-0095 authorization verifier completed its final allowed run with
PASS before package authoring began.

Verifier SHA-256:

`4c4a1feca0496055035e57389f0c581542e97ac72a46d10137f657208743093b`

Final allowed verifier-output SHA-256:

`07c8cbaf7ac1c7adf393c340d77c316c9663c4c61e3216489b19ff021e317ce5`

Final allowed verifier-output size:

`980`

The Decision-0095 authorization verifier is therefore permanently retired and
must never be rerun.

## Partial package state

Corrective Successor Package V2 authoring began immediately after that final
PASS.

Before an author checkpoint could be completed, the newly authored package-local
safe verifier failed with:

`FAIL|SAFE_VERIFIER_CONTAINS_OPENBAYES_ABSOLUTE_PATH`

The current partial package contains exactly 47 files.

Its byte-exact pre-recovery inventory is recorded by:

`01_partial_successor_package_pre_recovery_inventory.v1.SHA256SUMS`

Inventory SHA-256:

`7696e37f1f19b0fe5731eaea55e48d762467d7c1397ab234e76c7610315ba2c7`

Inventory size:

`6977`

## Diagnosed validator defect

The partial safe verifier has SHA-256:

`20324afe760f80ed7405b6987788bb6e9d969d7addfa8b4f7dd4c03bb6271ba0`

and size:

`25681`

Read-only diagnosis established exactly one literal occurrence of
`/openbayes/` in the safe verifier.

That occurrence is the validator's own check:

`if "/openbayes/" in script_text:`

No absolute OpenBayes path dependency was identified elsewhere in the safe
verifier.

The failure is therefore classified as:

`VALIDATOR_SELF_REFERENCE_FALSE_POSITIVE`

No research-evidence defect, relation-row defect, or SRR04 erratum defect was
identified by this failure.

## Authorized recovery mutation 1

Exactly one textual site in:

`05_verify_corrective_successor_package_v2.py`

may be changed.

Old condition:

`if "/openbayes/" in script_text:`

Authorized replacement:

`absolute_path_prefix = "/" + "openbayes" + "/"`

followed by:

`if absolute_path_prefix in script_text:`

This preserves the intended absolute-path prohibition while preventing the
validator from matching its own literal.

No other safe-verifier semantic change is authorized.

## Authorized recovery mutation 2

Because the safe verifier bytes will change, exactly one dependent artifact may
be regenerated:

`07_corrective_successor_package_v2.SHA256SUMS`

The regenerated manifest must bind the corrected safe verifier and all other
package files.

## Byte-exact preservation requirement

All other 45 partial-package files must remain byte-exact against the
pre-recovery 47-file snapshot.

In particular, recovery does not authorize modification of:

- the package manifest;
- either SRR04 erratum artifact;
- the blank focused rereview packet;
- the Decision-0095 consumption record;
- any source evidence;
- any Formalization V1 exact copy;
- any Review Package V1 exact copy;
- any completed human-review exact copy;
- any Decision-0095 authorization evidence; or
- any copied governance decision.

## Recovery-verifier lifecycle

The Decision-0096 recovery-authorization verifier may run before recovery
mutation begins.

It must run for its final allowed time immediately before the authorized
safe-verifier correction.

Once that correction begins, the Decision-0096 recovery-authorization verifier
is permanently retired and must never be rerun.

The already retired Decision-0095 authorization verifier must not be executed
during recovery under any circumstances.

## Explicit non-authorizations

Decision 0096 does not establish or authorize:

- Formalization V1 approval;
- focused human-review completion;
- focused human approval;
- operational V4-to-V2 mapping;
- schema-successor authoring;
- successor-schema version preselection;
- Schema V3;
- curl.json;
- analyzer implementation or execution;
- baseline execution; or
- repair.

## Next boundary

Run the Decision-0096 recovery-authorization verifier for its final allowed
time.

If it passes, immediately apply only the authorized one-site safe-verifier
self-reference correction and regenerate the dependent package checksum
manifest.

The Decision-0095 authorization verifier must never be rerun.
