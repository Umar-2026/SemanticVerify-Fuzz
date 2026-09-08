import json
from pathlib import Path

p = Path(__file__).parent / "d0291_artifact_availability_manifest.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0291"
assert d["role"] == "ARTIFACT_AVAILABILITY_STATEMENT_MANIFEST"

assert d["source"] == "D0290_PUBLICATION_EVIDENCE_PACKAGE"

assert d["statement_generated"] is True

for item in [
    "source_code",
    "evaluation_dataset",
    "experiment_configuration",
    "evaluation_results",
    "provenance_records"
]:
    assert item in d["availability_scope"]

for k,v in d["forbidden_operations"].items():
    assert v is False

print("D0291_AVAILABILITY_VERIFICATION=PASS")
print("ARTIFACT_STATEMENT_GENERATED=YES")
print("SOURCE=D0290_PUBLICATION_EVIDENCE_PACKAGE")
print("MUTATION=NO")
