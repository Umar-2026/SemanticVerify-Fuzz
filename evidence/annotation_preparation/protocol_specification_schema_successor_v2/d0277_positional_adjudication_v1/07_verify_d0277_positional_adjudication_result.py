import json
from pathlib import Path

p = Path(__file__).parent / "06_d0277_positional_adjudication_result.json"

d = json.loads(p.read_text())

assert d["decision"] == "D0277"
assert d["role"] == "POSITIONAL_ADJUDICATION_RESULT"

assert d["input_source"] == "D0276_MATERIALIZED_UNITS_ONLY"

assert d["snapshot_reread"] is False
assert d["new_evidence"] is False
assert d["target_rejudgment"] is False
assert d["global_positional_status_assigned"] is False

assert len(d["candidate_results"]) == 3

assert [x["candidate_index"] for x in d["candidate_results"]] == [6,8,9]

for x in d["candidate_results"]:
    assert x["positional_status"] in [
        "INDETERMINATE",
        "NOT_REQUIRED",
        "REQUIRED"
    ]

print("D0277_POSITIONAL_ADJUDICATION_VERIFIER=PASS")
print("CANDIDATES=6,8,9")
print("GLOBAL_STATUS_ASSIGNED=NO")
print("SNAPSHOT_REREAD=NO")
