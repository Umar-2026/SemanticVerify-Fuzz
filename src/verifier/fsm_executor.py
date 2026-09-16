from dataclasses import dataclass

from .predicate import (
    evaluate,
    PredicateResult
)


@dataclass
class VerificationResult:

    status: str

    final_state: str

    violated_rule: str = None



class FSMExecutor:


    def __init__(self, spec):

        self.spec = spec



    def execute(self, trace):

        state = self.spec.initial_state


        for event in trace.events:

            matched = False


            for transition in self.spec.transitions:

                if (
                    event.event_id == transition.event_id
                    and state in transition.from_states
                ):

                    result = evaluate(
                        transition.return_predicate,
                        event.return_value
                    )


                    if result == PredicateResult.FALSE:

                        continue


                    if result == PredicateResult.UNKNOWN:

                        return VerificationResult(
                            status="UNKNOWN",
                            final_state=state,
                            violated_rule=event.event_id
                        )


                    if result == PredicateResult.TRUE:

                        state = transition.to_states[0]

                        matched = True

                        break



            if not matched:

                return VerificationResult(
                    status="VIOLATION-MUST",
                    final_state=state,
                    violated_rule=event.event_id
                )


        return VerificationResult(
            status="VALID",
            final_state=state
        )
