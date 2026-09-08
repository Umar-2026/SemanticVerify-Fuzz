import json
from pathlib import Path

p = Path(__file__).parent / "final_evidence_accounting_manifest.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0281"
assert d["role"] == "FINAL_EVIDENCE_ACCOUNTING_MANIFEST"

assert d["evidence_source"] == "D0276_MATERIALIZED_UNITS_ONLY"

assert d["snapshot_reread"] is False
assert d["new_evidence"] is False
assert d["evidence_mutation"] is False
assert d["label_mutation"] is False

assert d["downstream_evaluation_authorized"] is True

print("D0281_MANIFEST_VERIFICATION=PASS")
print("SOURCE=D0276_MATERIALIZED_UNITS_ONLY")
print("SNAPSHOT_REREAD=NO")
print("EVALUATION_AUTHORIZED=YES")
