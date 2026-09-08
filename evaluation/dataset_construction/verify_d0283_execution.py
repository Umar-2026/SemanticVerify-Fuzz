import json
from pathlib import Path

p = Path(__file__).parent / "d0283_execution_result.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0283"
assert d["role"] == "EVALUATION_DATASET_CONSTRUCTION_EXECUTION"

assert d["source"] == "D0281_FINAL_EVIDENCE_ACCOUNTING_MANIFEST"

assert d["dataset_constructed"] is True

assert d["forbidden_executions"]["new_evidence"] is False
assert d["forbidden_executions"]["snapshot_reread"] is False
assert d["forbidden_executions"]["evidence_mutation"] is False
assert d["forbidden_executions"]["label_mutation"] is False
assert d["forbidden_executions"]["analyzer_execution"] is False
assert d["forbidden_executions"]["repair_execution"] is False

print("D0283_EXECUTION_VERIFICATION=PASS")
print("SOURCE=D0281_FINAL_EVIDENCE_ACCOUNTING_MANIFEST")
print("DATASET_CONSTRUCTED=YES")
print("EVIDENCE_MUTATION=NO")
print("ANALYZER_EXECUTION=NO")
print("REPAIR_EXECUTION=NO")
