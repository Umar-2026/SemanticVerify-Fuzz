from src.verifier.protocol_loader import load_protocol_spec
from src.verifier.trace import TraceEvent, ExecutionTrace
from src.verifier.fsm_executor import FSMExecutor


spec = load_protocol_spec(
    "config/protocol_specifications/zlib.json"
)


trace = ExecutionTrace(
[
    TraceEvent(
        "E06_INFLATE_INIT",
        "Z_OK"
    ),

    TraceEvent(
        "E07_INFLATE",
        None
    ),

    TraceEvent(
        "E10_INFLATE_COPY",
        "Z_OK"
    ),

    TraceEvent(
        "E07_INFLATE",
        None
    ),

    TraceEvent(
        "E08_INFLATE_END"
    ),

    TraceEvent(
        "E08_INFLATE_END"
    )
]
)


executor = FSMExecutor(spec)

result = executor.execute(trace)

print("STATUS =", result.status)
print("FINAL_STATE =", result.final_state)
print("VIOLATED_RULE =", result.violated_rule)
