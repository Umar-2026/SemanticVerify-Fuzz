
from src.verifier.protocol_loader import load_protocol_spec


spec = load_protocol_spec(
    "config/protocol_specifications/zlib.json"
)


assert spec.library=="zlib"

assert spec.initial_state=="UNINITIALIZED"

assert len(spec.states)==8

assert len(spec.transitions)==17

assert len(spec.obligations)==14


print(
"PROTOCOL_LOADER_TEST=PASS"
)

print(
"LIBRARY=",
spec.library
)

print(
"STATES=",
len(spec.states)
)

print(
"TRANSITIONS=",
len(spec.transitions)
)

print(
"OBLIGATIONS=",
len(spec.obligations)
)


for o in spec.obligations:

    print(
        o.rule_id,
        o.defect_category
    )

