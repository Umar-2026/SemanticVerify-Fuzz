import re

from src.verifier.trace import (
    TraceEvent,
    ExecutionTrace
)


API_MAP = {
    "inflateInit2": "E06_INFLATE_INIT",
    "inflateInit": "E06_INFLATE_INIT",
    "inflate": "E07_INFLATE",
    "inflateEnd": "E08_INFLATE_END",
    "inflateReset": "E09_INFLATE_RESET",
    "inflateCopy": "E10_INFLATE_COPY",

    "deflateInit2": "E01_DEFLATE_INIT",
    "deflateInit": "E01_DEFLATE_INIT",
    "deflate": "E02_DEFLATE",
    "deflateEnd": "E03_DEFLATE_END",
    "deflateReset": "E04_DEFLATE_RESET",
    "deflateSetDictionary": "E05_DEFLATE_SET_DICTIONARY",
}


RETURNS = [
    "Z_STREAM_END",
    "Z_OK",
    "Z_BUF_ERROR",
    "Z_DATA_ERROR",
    "Z_MEM_ERROR",
    "Z_STREAM_ERROR"
]


def extract_return(line):

    for r in RETURNS:
        if r in line:
            return r

    return None



def extract_resource(line, api):

    m = re.search(
        rf"{api}\s*\(\s*&(\w+)",
        line
    )

    if m:
        return m.group(1)

    return None



def extract_trace(source):

    events=[]


    for line_no,line in enumerate(
        source.splitlines(),
        1
    ):

        for api,event_id in API_MAP.items():

            if re.search(
                r"\b"+api+r"\s*\(",
                line
            ):

                events.append(

                    TraceEvent(

                        event_id=event_id,

                        resource_id=extract_resource(
                            line,
                            api
                        ),

                        return_value=extract_return(
                            line
                        ),

                        location=f"line:{line_no}"

                    )
                )


    return ExecutionTrace(events)



def extract_file(path):

    with open(
        path,
        errors="ignore"
    ) as f:

        source=f.read()


    return extract_trace(source)

