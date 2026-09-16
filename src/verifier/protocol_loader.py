import json

from pathlib import Path

from .models import (
    Obligation,
    Transition,
    ProtocolSpec
)


def load_protocol_spec(path):

    data=json.loads(
        Path(path).read_text()
    )


    obligations=[]

    for item in data["obligations"]:

        obligations.append(

            Obligation(

                rule_id=item["rule_id"],

                defect_category=item["defect_category"],

                resource_kind=item["resource_kind"],

                trigger=item[
                    "triggering_event_or_function_exit"
                ],

                precondition=item[
                    "required_pre_state_or_exit_condition"
                ],

                return_predicate=item[
                    "return_predicate"
                ],

                ownership_effect=item[
                    "ownership_effect"
                ],

                permitted_transitions=item[
                    "permitted_transitions"
                ],

                cleanup_responsibility=item[
                    "cleanup_responsibility"
                ],

                source_evidence=item[
                    "source_evidence"
                ]
            )
        )


    transitions=[]


    for item in data["transitions"]:

        transitions.append(

            Transition(

                transition_id=item["transition_id"],

                event_id=item["event_id"],

                from_states=item["from_states"],

                to_states=item["to_states"],

                return_predicate=item[
                    "return_predicate"
                ],

                ownership_effect=item[
                    "ownership_effect"
                ]
            )
        )


    return ProtocolSpec(

        library=data["library"],

        resource_kind=data["resource_kind"],

        schema_version=data["schema_version"],

        initial_state=data["initial_state"],

        states=data["states"],

        events=data["events"],

        transitions=transitions,

        obligations=obligations,

        permitted_exit_states=data[
            "permitted_exit_states"
        ]

    )
