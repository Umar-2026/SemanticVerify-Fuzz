from src.verifier.protocol_loader import load_protocol_spec

from src.verifier.trace import (
    TraceEvent,
    ExecutionTrace
)

from src.verifier.fsm_executor import FSMExecutor



spec = load_protocol_spec(
    "config/protocol_specifications/zlib.json"
)


executor = FSMExecutor(spec)



trace = ExecutionTrace(
[
    TraceEvent(
        "E01_DEFLATE_INIT",
        "Z_OK"
    ),

    TraceEvent(
        "E02_DEFLATE",
        "Z_STREAM_END"
    ),

    TraceEvent(
        "E03_DEFLATE_END"
    )
]
)



result = executor.execute(trace)


print("STATUS=", result.status)

print("FINAL_STATE=", result.final_state)
