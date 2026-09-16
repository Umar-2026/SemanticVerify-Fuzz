from enum import Enum


class PredicateResult(Enum):

    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"



def evaluate(predicate, return_value):

    if predicate is None:
        return PredicateResult.TRUE


    if return_value is None:
        return PredicateResult.UNKNOWN


    predicate = predicate.strip()


    # handle conjunction
    if " and " in predicate:

        parts = predicate.split(" and ")

        results = [
            evaluate(
                p,
                return_value
            )
            for p in parts
            if "return" in p
        ]

        if any(
            r == PredicateResult.FALSE
            for r in results
        ):
            return PredicateResult.FALSE


        if all(
            r == PredicateResult.TRUE
            for r in results
        ):
            return PredicateResult.TRUE


        return PredicateResult.UNKNOWN



    if "return ==" in predicate:

        expected = (
            predicate
            .split("return ==")[1]
            .strip()
        )

        return (
            PredicateResult.TRUE
            if return_value == expected
            else PredicateResult.FALSE
        )


    if "return !=" in predicate:

        expected = (
            predicate
            .split("return !=")[1]
            .strip()
        )

        return (
            PredicateResult.TRUE
            if return_value != expected
            else PredicateResult.FALSE
        )


    return PredicateResult.UNKNOWN
