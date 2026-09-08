import json
from pathlib import Path

p = Path(__file__).parent / "d0288_final_evaluation_report_manifest.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0288"
assert d["role"] == "FINAL_EVALUATION_REPORT_MANIFEST"

assert d["source"] == "D0287_RQ_EVALUATION_RESULT_FREEZE"

assert d["report_generated"] is True

for rq in ["RQ1", "RQ2", "RQ3", "RQ5"]:
    assert rq in d["research_question_mapping"]

for k, v in d["forbidden_operations"].items():
    assert v is False

print("D0288_REPORT_MANIFEST_VERIFICATION=PASS")
print("REPORT_GENERATED=YES")
print("SOURCE=D0287_RQ_EVALUATION_RESULT_FREEZE")
print("MUTATION=NO")
