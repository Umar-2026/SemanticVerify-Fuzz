import json
from pathlib import Path

p = Path(__file__).parent / "d0289_paper_results_traceability_manifest.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0289"
assert d["role"] == "PAPER_RESULTS_TRACEABILITY_MANIFEST"

assert d["source"] == "D0288_FINAL_EVALUATION_REPORT_MANIFEST"

assert d["traceability_generated"] is True

for rq in ["RQ1","RQ2","RQ3","RQ5"]:
    assert rq in d["mapping"]

for k,v in d["forbidden_operations"].items():
    assert v is False

print("D0289_TRACEABILITY_VERIFICATION=PASS")
print("PAPER_MAPPING_GENERATED=YES")
print("SOURCE=D0288_FINAL_EVALUATION_REPORT_MANIFEST")
print("MUTATION=NO")
