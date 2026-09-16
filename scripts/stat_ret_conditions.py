from pathlib import Path
import re


root=Path(
"evidence/primary_generation/SVF-PRIMARY-800-V1/slots"
)


counter={
    "ret_compare":0,
    "ret_return":0,
    "ret_unused":0
}


for f in root.glob("*/driver.c"):

    text=f.read_text(errors="ignore")


    if re.search(
        r'\bret\s*=\s*(inflate|deflate)\s*\(',
        text
    ):

        if re.search(
            r'\bret\s*(==|!=)\s*Z_[A-Z_]+',
            text
        ):
            counter["ret_compare"]+=1

        elif re.search(
            r'\breturn\s+ret',
            text
        ):
            counter["ret_return"]+=1

        else:
            counter["ret_unused"]+=1



print(counter)
