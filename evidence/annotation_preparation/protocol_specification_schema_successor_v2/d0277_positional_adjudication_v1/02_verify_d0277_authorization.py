import json
from pathlib import Path

p = Path(__file__).parent / "01_d0277_authorization_scope.json"

data = json.loads(p.read_text())

assert data["decision"] == "D0277"
assert data["parent"] == "D0276"
assert data["authorized"] is True
assert data["executed"] is False

assert data["snapshot_read"] is False
assert data["materialization"] is False
assert data["new_evidence"] is False
assert data["target_rejudgment"] is False

assert data["allowed_candidates"] == [6,8,9]

print("D0277_AUTHORIZATION_VERIFIER=PASS")
print("D0277_AUTHORIZED=YES")
print("D0277_EXECUTED=NO")
print("SNAPSHOT_READ=NO")
print("POSITIONAL_ADJUDICATION_PERFORMED=NO")
