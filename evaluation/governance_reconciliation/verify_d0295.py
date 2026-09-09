import json
from pathlib import Path

p = Path(
"evaluation/governance_reconciliation/d0295_governance_reconciliation.json"
)

d=json.loads(p.read_text())

assert d["decision"]=="D0295"

assert d["authoritative_activation"]=="Decision-0066"

assert d["schema_v2_status"]=="ALREADY_ACTIVE"

assert d["duplicate_activation_resolution"]=="NON_AUTHORITATIVE_RECORD"


for k,v in d["forbidden_operations"].items():
    assert v is False


print("D0295_GOVERNANCE_RECONCILIATION=PASS")
print("SCHEMA_V2_STATUS=ALREADY_ACTIVE")
print("AUTHORITY=DECISION_0066")
print("MUTATION=NO")
