from pathlib import Path
import json

from src.extractor.api_extractor import extract_file
from src.verifier.protocol_loader import load_protocol_spec
from src.verifier.fsm_executor import FSMExecutor


spec = load_protocol_spec(
    "config/protocol_specifications/zlib.json"
)

executor = FSMExecutor(spec)


input_file = Path(
    "evaluation/compile_success_drivers.txt"
)


output_file = Path(
    "evaluation/verification_results.jsonl"
)


results=[]


for idx, line in enumerate(
    input_file.read_text().splitlines(),
    start=1
):

    driver = Path(line.strip())

    try:

        trace = extract_file(driver)

        result = executor.execute(trace)


        record = {

            "driver":
                str(driver),

            "trace_length":
                len(trace.events),

            "trace":
                [
                    {
                        "event_id": e.event_id,
                        "location": e.location,
                        "return_value": e.return_value
                    }
                    for e in trace.events
                ],

            "status":
                result.status,

            "final_state":
                result.final_state,

            "violated_rule":
                result.violated_rule
        }


    except Exception as e:

        record = {

            "driver":
                str(driver),

            "status":
                "EXTRACT_ERROR",

            "error":
                str(e)
        }


    results.append(record)


with output_file.open(
    "w"
) as f:

    for r in results:
        f.write(
            json.dumps(r)
            + "\n"
        )


print(
    "processed:",
    len(results)
)

print(
    "saved:",
    output_file
)
