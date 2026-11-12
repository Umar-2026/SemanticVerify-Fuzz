# Gate 5 libvpx specification adoption

This checkpoint adopts the independently reviewed bounded libvpx decoder-context
specification. The supported scope is initialization, decode D1/D3, destroy D4,
and function-exit cleanup D5. D2 after failed initialization, `get_frame`
enforcement, held-out effectiveness, and broader lifecycle claims remain excluded.

Severity is registered as `UNSPECIFIED`. No private review documents, held-out
data, analyzer output, or baseline output are stored in this directory.
