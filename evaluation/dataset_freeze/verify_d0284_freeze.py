import json
from pathlib import Path

p = Path(__file__).parent / "d0284_dataset_freeze_manifest.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0284"
assert d["role"] == "EVALUATION_DATASET_FREEZE_MANIFEST"

assert d["source"] == "D0283_EVALUATION_DATASET_CONSTRUCTION"

assert d["dataset_frozen"] is True

for k,v in d["forbidden_operations"].items():
    assert v is False

print("D0284_FREEZE_VERIFICATION=PASS")
print("DATASET_FROZEN=YES")
print("SOURCE=D0283_EVALUATION_DATASET_CONSTRUCTION")
print("MUTATION=NO")
