from pathlib import Path
import re
from collections import Counter


root = Path(
"evidence/primary_generation/SVF-PRIMARY-800-V1/slots"
)


counter = Counter()


for driver in root.glob("*/driver.c"):

    text = driver.read_text(
        errors="ignore"
    )


    if "inflate(" in text:
        counter["inflate"] += 1

    if "deflate(" in text:
        counter["deflate"] += 1


    if re.search(
        r'\w+\s*=\s*inflate\s*\(',
        text
    ):
        counter["inflate_saved_return"] += 1


    if re.search(
        r'\w+\s*=\s*deflate\s*\(',
        text
    ):
        counter["deflate_saved_return"] += 1


    if "inflateEnd" in text:
        counter["inflateEnd"] += 1


    if "deflateEnd" in text:
        counter["deflateEnd"] += 1



for k,v in counter.items():
    print(k,v)
