import json
from pathlib import Path

p = Path(__file__).parent / "d0286_rq_execution_result.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0286"
assert d["role"] == "RQ_EVALUATION_EXECUTION_RESULT"

assert d["source"] == "D0284_FROZEN_EVALUATION_DATASET"

assert d["execution_completed"] is True

for rq in ["RQ1","RQ2","RQ3","RQ5"]:
    assert d["research_questions"][rq] == "executed"

assert d["forbidden_operations"]["new_evidence"] is False
assert d["forbidden_operations"]["evidence_mutation"] is False
assert d["forbidden_operations"]["dataset_mutation"] is False
assert d["forbidden_operations"]["label_mutation"] is False
assert d["forbidden_operations"]["repair_execution"] is False

print("D0286_EXECUTION_VERIFICATION=PASS")
print("RQ_EVALUATION_EXECUTED=YES")
print("SOURCE=D0284_FROZEN_DATASET")
print("MUTATION=NO")
