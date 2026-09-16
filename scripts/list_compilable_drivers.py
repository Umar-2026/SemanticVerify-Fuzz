from pathlib import Path
import json


root = Path(
"evidence/primary_generation/SVF-PRIMARY-800-V1/slots"
)


out=[]


for slot in root.iterdir():

    pp = slot / "postprocessing.json"

    if not pp.exists():
        continue


    data=json.loads(
        pp.read_text()
    )


    if (
        data.get("compiler_exit_code")
        == 0
        and (slot/"driver.c").exists()
    ):
        out.append(
            str(slot/"driver.c")
        )


print("compile_success drivers:",
      len(out))


Path(
"evaluation/compile_success_drivers.txt"
).write_text(
    "\n".join(out)
)
