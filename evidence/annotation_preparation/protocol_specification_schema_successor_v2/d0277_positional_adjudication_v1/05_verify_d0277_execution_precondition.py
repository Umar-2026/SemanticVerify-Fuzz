import json
from pathlib import Path

p = Path(__file__).parent / "04_d0277_execution_scope.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0277"
assert d["role"] == "POSITIONAL_ADJUDICATION_EXECUTION"
assert d["input_source"] == "D0276_MATERIALIZED_UNITS_ONLY"

assert d["snapshot_reread"] is False
assert d["new_evidence"] is False
assert d["target_rejudgment"] is False

assert d["candidates"] == [6,8,9]

print("D0277_EXECUTION_PRECONDITION=PASS")
print("INPUT=D0276_MATERIALIZED_UNITS_ONLY")
print("SNAPSHOT_REREAD=NO")
print("NEW_EVIDENCE=NO")
print("READY_FOR_ADJUDICATION=YES")
