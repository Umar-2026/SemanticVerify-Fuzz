# SemanticVerify-Fuzz

**Resource-Centered, Path-Sensitive Verification and Constrained Repair
of API-Protocol Violations in LLM-Generated Fuzz Drivers**

This repository is a complete research restart dated 5 August 2026.

The implementation order is mandatory:

1. Stage A: verification.
2. Gate V: irreversible verification freeze.
3. Stage B: constrained repair.

No repair implementation or repair output may influence Stage A.

## Locked experimental design

- Two target low-cost API models, pending live qualification.
- Eight libraries.
- Ten scenarios per library.
- Five attempts per scenario/model.
- Total: 800 newly generated attempts.
- Development: zlib.
- Validation: libpcap.
- Held out: curl, cJSON, libtiff, libvpx, c-ares, and lcms.
- Blind dual-annotation sample: up to 140 compilable drivers.
- Repair: minimum 20 eligible natural defects for confirmation; cap 40.

## Current milestone

Gate 0A repository bootstrap. See `documentation/CURRENT_STATUS.md`.

The project does not claim complete verification of arbitrary C/C++ code,
general symbolic path feasibility, or globally minimal program repair.
