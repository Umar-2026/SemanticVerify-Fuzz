import json
from pathlib import Path

p = Path(__file__).parent / "d0287_result_freeze_manifest.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0287"
assert d["role"] == "RQ_EVALUATION_RESULT_FREEZE_MANIFEST"

assert d["source"] == "D0286_RQ_EVALUATION_EXECUTION"

assert d["results_frozen"] is True

for rq in ["RQ1","RQ2","RQ3","RQ5"]:
    assert rq in d["frozen_results"]

for k,v in d["forbidden_operations"].items():
    assert v is False

print("D0287_FREEZE_VERIFICATION=PASS")
print("RESULTS_FROZEN=YES")
print("SOURCE=D0286_RQ_EVALUATION_EXECUTION")
print("MUTATION=NO")
