from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TraceEvent:

    event_id: str

    resource_id: Optional[str] = None

    return_value: Optional[str] = None

    location: Optional[str] = None



@dataclass
class ExecutionTrace:

    events: List[TraceEvent]
