from pathlib import Path
import re

root=Path(
"evidence/primary_generation/SVF-PRIMARY-800-V1/slots"
)

counter={
"compare":0,
"assignment":0,
"plain":0
}


for f in root.glob("*/driver.c"):

    text=f.read_text(errors="ignore")


    if re.search(
        r'(==|!=).*(inflate|deflate)\s*\(',
        text
    ):
        counter["compare"]+=1


    elif re.search(
        r'\w+\s*=\s*(inflate|deflate)\s*\(',
        text
    ):
        counter["assignment"]+=1


    elif re.search(
        r'\b(inflate|deflate)\s*\(',
        text
    ):
        counter["plain"]+=1


print(counter)
