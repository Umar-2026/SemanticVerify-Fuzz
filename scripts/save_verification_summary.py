import json
from collections import Counter


src="evaluation/verification_results.jsonl"

out="evaluation/verification_summary.json"


counter=Counter()


total=0


with open(src) as f:

    for line in f:

        r=json.loads(line)

        counter[r["status"]] += 1
        total += 1



summary={

    "population":
        total,

    "outcomes":
        dict(counter),

    "percentages":
        {
            k:
            round(v/total*100,2)
            for k,v in counter.items()
        }

}


with open(out,"w") as f:

    json.dump(
        summary,
        f,
        indent=2
    )


print(json.dumps(summary,indent=2))
