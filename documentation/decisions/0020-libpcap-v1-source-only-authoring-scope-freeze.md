# Decision 0020: libpcap V1 Source-Only Authoring Scope Freeze

Status: Accepted before libpcap V1 working-draft authoring

Date: 2026-08-16

## Context

The canonical zlib specification is frozen. Under the source-only recovery
protocol, the libpcap protocol scope must be fixed before any generated
libpcap driver source is inspected.

The frozen scenario manifest is:

`config/generation/scenario_bindings.80.v10.json`

SHA-256:

`a7ab361e6e2d41d9051e48bc7626f0be37c1df9ec35f788a9a019b010054a2db`

The pinned libpcap revision is:

`a999701dca5c873779281938baee6bc185a8d4dc`

Two preliminary scope-freeze executions stopped during source-evidence path
validation before creating any governance artifact. The first corrected the
immediate-mode manpage to `pcap_set_immediate_mode.3pcap.in`. The second
revealed that a substring-based filename audit incorrectly treated
`pcap_datalink_name_to_val.3pcap` and `pcap_datalink_val_to_name.3pcap` as
alternative pages for `pcap_datalink()`.

The primary pinned API page is exactly:

`pcap_datalink.3pcap.in`

SHA-256:

`434c12ea9f01c6badf1cc3ef5009392df2dbe32761435baff3d091a62cdb9d09`

No generated driver, gold label, analyzer output, baseline output, LLM-review
output, or repair output was used to resolve these source-only evidence paths.

## Decision

The normative machine-readable V1 authoring scope is:

`config/annotation/libpcap_v1_authoring_scope.v1.json`

SHA-256:

`52ed3d09c6031c7d256e59246aa44ff741d358a784f32516a9f503abe5110d65`

Two independently tracked protocol-resource families are modeled:

1. `pcap_t *` capture handles; and
2. successfully compiled `struct bpf_program` objects.

The capture-handle lifecycle covers `pcap_create()`, five bounded
pre-activation configuration functions, `pcap_activate()`, active operations,
activation-failure cleanup, and `pcap_close()`.

The pre-activation family is:

- `pcap_set_snaplen()`;
- `pcap_set_promisc()`;
- `pcap_set_timeout()`;
- `pcap_set_immediate_mode()`; and
- `pcap_set_buffer_size()`.

The active-use family is:

- `pcap_datalink()`;
- `pcap_next_ex()`;
- `pcap_compile()`; and
- `pcap_setfilter()`.

A successful `pcap_compile()` creates a caller-owned BPF program carrying an
eventual `pcap_freecode()` obligation. `pcap_setfilter()` does not consume that
ownership.

The header and packet-data values returned by `pcap_next_ex()` are modeled as
library-owned borrowed values; the caller must not free them and must copy them
if they must remain valid beyond their documented lifetime.

## Explicit boundaries

`pcap_open_live()` is outside V1 because all ten frozen scenarios use
`pcap_create()` plus `pcap_activate()`.

`pcap_next()` is outside V1; its earlier lexical occurrence was a substring
match inside `pcap_next_ex`.

"Snapshot-length" refers to `pcap_set_snaplen()` and does not entitle
`pcap_snapshot()`.

Offline/dead handles, dumpers, discovery, timestamp configuration, statistics,
non-blocking control, alternate loop/dispatch APIs, injection, datalink
mutation and the broader API surface remain outside V1.

Repeated `pcap_freecode()` is not automatically D4 merely by call count because
the pinned implementation resets the program length and nulls the instruction
pointer.

## Stage boundary

This freeze authorizes source-only libpcap V1 working-draft authoring from the
frozen scope and approved pinned evidence only.

Generated-driver inspection, gold annotation, analyzer implementation,
baseline execution, LLM-review execution and repair remain blocked.
