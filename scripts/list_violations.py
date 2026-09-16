import json


path="evaluation/verification_results.jsonl"


with open(path) as f:

    for line in f:

        r=json.loads(line)

        if r["status"]=="VIOLATION-MUST":

            print("="*60)

            print(
                r
            )
