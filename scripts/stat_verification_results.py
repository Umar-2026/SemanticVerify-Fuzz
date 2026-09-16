import json
from collections import Counter


path="evaluation/verification_results.jsonl"


counter=Counter()


with open(path) as f:

    for line in f:

        r=json.loads(line)

        counter[
            r["status"]
        ] += 1


print(counter)

print(
    "total:",
    sum(counter.values())
)
