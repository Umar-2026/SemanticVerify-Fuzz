import re

from src.verifier.trace import (
    TraceEvent,
    ExecutionTrace
)


API_MAP = {

    "inflateInit": "E06_INFLATE_INIT",
    "inflateInit2": "E06_INFLATE_INIT",

    "inflate": "E07_INFLATE",

    "inflateEnd": "E08_INFLATE_END",

    "inflateReset": "E09_INFLATE_RESET",

    "inflateCopy": "E10_INFLATE_COPY",


    "deflateInit": "E01_DEFLATE_INIT",
    "deflateInit2": "E01_DEFLATE_INIT",

    "deflate": "E02_DEFLATE",

    "deflateEnd": "E03_DEFLATE_END",

    "deflateReset": "E04_DEFLATE_RESET",

    "deflateSetDictionary":
        "E05_DEFLATE_SET_DICTIONARY",
}



def extract_trace(source):

    events = []


    for line_no, line in enumerate(
        source.splitlines(),
        start=1
    ):

        for api, event_id in API_MAP.items():

            pattern = r"\b" + api + r"\s*\("


            if re.search(pattern, line):

                events.append(
                    TraceEvent(
                        event_id=event_id,
                        return_value=None,
                        location=f"line:{line_no}"
                    )
                )


    return ExecutionTrace(events)



def extract_file(path):

    with open(
        path,
        "r",
        errors="ignore"
    ) as f:

        source=f.read()


    return extract_trace(source)
