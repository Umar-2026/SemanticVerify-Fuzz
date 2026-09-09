import json
from pathlib import Path


p = Path(__file__).parent / "d0294_schema_v2_activation_manifest.json"

d = json.loads(p.read_text())


assert d["decision"] == "D0294"

assert d["role"] == "SCHEMA_V2_ACTIVATION_MANIFEST"

assert d["schema_version"] == "V2"

assert d["activation"] is True

assert d["canonical_representation"] is True


for lib in [
    "zlib",
    "libpcap"
]:
    assert lib in d["supported_libraries"]


for item in [
    "obligation_representation",
    "resource_model",
    "protocol_state_model",
    "defect_mapping"
]:
    assert item in d["activation_scope"]


for k,v in d["forbidden_operations"].items():
    assert v is False


print("D0294_SCHEMA_V2_ACTIVATION_VERIFICATION=PASS")
print("SCHEMA_V2_ACTIVATED=YES")
print("CANONICAL_PROTOCOL_SCHEMA=V2")
print("ANALYZER_EXECUTION=NO")
print("REPAIR_EXECUTION=NO")
print("MUTATION=NO")
