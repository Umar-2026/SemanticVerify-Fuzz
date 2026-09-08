import json
from pathlib import Path

p = Path(__file__).parent / "d0292_reviewer_reproduction_checklist.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0292"
assert d["role"] == "REVIEWER_REPRODUCTION_CHECKLIST_MANIFEST"

assert d["source"] == "D0291_ARTIFACT_AVAILABILITY_STATEMENT"

assert d["checklist_generated"] is True

required = [
    "environment_setup",
    "artifact_download",
    "dataset_validation",
    "experiment_execution",
    "result_verification",
    "provenance_validation"
]

for item in required:
    assert item in d["reproduction_steps"]

for rq in ["RQ1","RQ2","RQ3","RQ5"]:
    assert rq in d["rq_mapping"]

for k,v in d["forbidden_operations"].items():
    assert v is False

print("D0292_CHECKLIST_VERIFICATION=PASS")
print("REPRODUCTION_CHECKLIST_GENERATED=YES")
print("SOURCE=D0291_ARTIFACT_AVAILABILITY_STATEMENT")
print("MUTATION=NO")
