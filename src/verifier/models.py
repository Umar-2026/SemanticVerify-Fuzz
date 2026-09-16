from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Obligation:

    rule_id: str

    defect_category: str

    resource_kind: str

    trigger: str

    precondition: str

    return_predicate: Optional[str]

    ownership_effect: str

    permitted_transitions: List[str]

    cleanup_responsibility: str

    source_evidence: List[str]


@dataclass
class Transition:

    transition_id: str

    event_id: str

    from_states: List[str]

    to_states: List[str]

    return_predicate: str

    ownership_effect: str


@dataclass
class ProtocolSpec:

    library: str

    resource_kind: str

    schema_version: str

    initial_state: str

    states: List[str]

    events: List[Dict]

    transitions: List[Transition]

    obligations: List[Obligation]

    permitted_exit_states: List[str]
