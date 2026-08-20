# zlib / libpcap Pre/Post Immutability Evidence

## zlib

Canonical file:

`config/protocol_specifications/zlib.json`

Frozen file SHA-256:

`f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1`

Frozen semantic content SHA-256:

`3461269e60f3b824bef3c62335d24e9eda5552b1a939bea4c720983e39a25049`

Canonical freeze commit:

`e12adfe2d502f6915a094c2f39a46e426ddc0522`

Git blob at canonical freeze and every later supplied checkpoint:

`5e4d5744f9da0b1a2723d4ec834f9ad03b7e64ea`

## libpcap

Canonical file:

`config/protocol_specifications/libpcap.json`

Frozen file SHA-256:

`b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73`

Frozen semantic content SHA-256:

`370da6351b59f6134ae09477d8941d8ab119adad7f4230540758e09326b47c4f`

Canonical freeze commit:

`b1635239e29ff6dd9a3188e264c4e6a816977aae`

Git blob at canonical freeze and every later supplied checkpoint:

`ce4ea9b2d97c1ca570b004dc1c4869eb067f8c5d`

## Relevant later checkpoints

- Schema V2 authoring authorization: `dc6371ceaa189d0a39ae5a93e131cb85ebe328d8`
- Schema V2 author checkpoint: `5195de4842668fdd1ef587e4dbe969e53f80dd5c`
- Review Package V1: `41753d7f7b6f26836ff6c2a4b12bb13084f069e9`
- Completed human-review record: `c2c1e28c235c158eb36759d167c3700bfd8042f4`
- Corrective Review Package V2 authorization: `bf6cf53d54c105353906f02c6fa117668b635eae`

For these later governance checkpoints, the package supplies both checkpoint
and immediate-parent Git objects and tree/file bindings so that a reviewer can
independently verify that zlib.json and libpcap.json were not rewritten by
those commits.

The machine-readable comparison manifest is:

`12_zlib_libpcap_prepost_comparison_manifest.v1.json`

The portable original Git-object proof is:

`13_zlib_libpcap_prepost_git_proof/`
