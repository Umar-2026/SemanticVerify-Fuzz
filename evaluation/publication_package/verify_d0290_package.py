import json
from pathlib import Path

p = Path(__file__).parent / "d0290_publication_evidence_package_manifest.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0290"
assert d["role"] == "PUBLICATION_EVIDENCE_PACKAGE_MANIFEST"

assert d["source"] == "D0289_PAPER_RESULTS_TRACEABILITY_MANIFEST"

assert d["package_frozen"] is True

required = [
    "D0284_FROZEN_EVALUATION_DATASET",
    "D0287_RQ_EVALUATION_RESULTS",
    "D0288_FINAL_EVALUATION_REPORT_MANIFEST",
    "D0289_PAPER_RESULTS_TRACEABILITY_MANIFEST"
]

for item in required:
    assert item in d["included_artifacts"]

for k,v in d["forbidden_operations"].items():
    assert v is False

print("D0290_PACKAGE_VERIFICATION=PASS")
print("PUBLICATION_PACKAGE_FROZEN=YES")
print("SOURCE=D0289_PAPER_RESULTS_TRACEABILITY_MANIFEST")
print("MUTATION=NO")
