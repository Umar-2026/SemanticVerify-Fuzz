import json
from pathlib import Path

p = Path(__file__).parent / "d0282_evaluation_dataset_authorization.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0282"
assert d["role"] == "EVALUATION_DATASET_CONSTRUCTION_AUTHORIZATION"

assert d["source"] == "D0281_FINAL_EVIDENCE_ACCOUNTING_MANIFEST"

assert d["source_frozen"] is True
assert d["authorized"] is True

assert "new_evidence" in d["forbidden"]
assert "snapshot_reread" in d["forbidden"]
assert "evidence_mutation" in d["forbidden"]
assert "label_mutation" in d["forbidden"]

print("D0282_AUTHORIZATION_VERIFICATION=PASS")
print("SOURCE=D0281_FINAL_EVIDENCE_ACCOUNTING_MANIFEST")
print("SOURCE_FROZEN=YES")
print("DATASET_CONSTRUCTION_AUTHORIZED=YES")
