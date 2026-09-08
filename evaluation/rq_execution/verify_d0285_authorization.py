import json
from pathlib import Path

p = Path(__file__).parent / "d0285_rq_execution_authorization.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0285"
assert d["role"] == "RQ_EVALUATION_EXECUTION_AUTHORIZATION"

assert d["source"] == "D0284_FROZEN_EVALUATION_DATASET"

assert d["authorized"] is True
assert d["execution_started"] is False

assert "RQ1" in d["research_questions"]
assert "RQ2" in d["research_questions"]
assert "RQ3" in d["research_questions"]
assert "RQ5" in d["research_questions"]

for item in [
    "new_evidence",
    "evidence_mutation",
    "dataset_mutation",
    "label_mutation",
    "repair_execution"
]:
    assert item in d["forbidden_operations"]

print("D0285_AUTHORIZATION_VERIFICATION=PASS")
print("SOURCE=D0284_FROZEN_EVALUATION_DATASET")
print("RQ_EXECUTION_AUTHORIZED=YES")
print("EXECUTION_STARTED=NO")
