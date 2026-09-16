from pathlib import Path
import re


root=Path(
"evidence/primary_generation/SVF-PRIMARY-800-V1/slots"
)


counter={
"api_compare":0,
"assignment":0,
"plain_call":0
}


for f in root.glob("*/driver.c"):

    text=f.read_text(errors="ignore")


    # inflate(...) == VALUE
    pattern1=r'(inflate|deflate)\s*\([^;]*\)\s*(==|!=)\s*(Z_[A-Z_]+)'


    # if (VALUE == inflate(...))
    pattern2=r'(Z_[A-Z_]+)\s*(==|!=)\s*(inflate|deflate)\s*\('


    if re.search(pattern1,text) or re.search(pattern2,text):
        counter["api_compare"]+=1


    elif re.search(
        r'\w+\s*=\s*(inflate|deflate)\s*\(',
        text
    ):
        counter["assignment"]+=1


    elif re.search(
        r'\b(inflate|deflate)\s*\(',
        text
    ):
        counter["plain_call"]+=1



print(counter)
