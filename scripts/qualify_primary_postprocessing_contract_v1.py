#!/usr/bin/env python3

import json
import hashlib
import subprocess
import tempfile
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "config/primary_postprocessing_contract.v1.json"
DECISION = ROOT / "documentation/decisions/0010-primary-postprocessing-precedence-and-duplicate-semantics.md"
VERIFIER = ROOT / "scripts/verify_primary_postprocessing_contract_v1.py"
REPORT = ROOT / "evidence/generation_opening/postprocessing_contract_v1/qualification.v1.json"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def run(cmd):
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace"
    )


def classify(text):
    if not isinstance(text, str):
        return "EXTRACTION_FAILURE", None

    if text.strip() == "":
        return "MISSING_CODE", text

    return "EXTRACTED_VERBATIM", text


SOURCES = {
    "zlib": r'''
#include <stddef.h>
#include <string.h>
#include <zlib.h>
int svf_probe(const unsigned char *data, size_t size)
{
    z_stream s;
    memset(&s, 0, sizeof(s));
    if (inflateInit(&s) != Z_OK) return 1;
    s.next_in = (Bytef *)data;
    s.avail_in = (uInt)size;
    (void)inflate(&s, Z_NO_FLUSH);
    inflateEnd(&s);
    return 0;
}
''',

    "libpcap": r'''
#include <pcap/pcap.h>
int svf_probe(void)
{
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *p = pcap_create("lo", errbuf);
    if (p) pcap_close(p);
    return 0;
}
''',

    "curl": r'''
#include <curl/curl.h>
int svf_probe(void)
{
    CURL *h = curl_easy_init();
    if (h) curl_easy_cleanup(h);
    return 0;
}
''',

    "cJSON": r'''
#include <cJSON.h>
int svf_probe(void)
{
    cJSON *x = cJSON_Parse("{}");
    if (x) cJSON_Delete(x);
    return 0;
}
''',

    "libtiff": r'''
#include <tiffio.h>
int svf_probe(void)
{
    TIFF *t = TIFFOpen("/nonexistent-svf-input", "r");
    if (t) TIFFClose(t);
    return 0;
}
''',

    "libvpx": r'''
#include <vpx/vpx_decoder.h>
#include <vpx/vp8dx.h>
int svf_probe(void)
{
    vpx_codec_ctx_t ctx;

    if (vpx_codec_dec_init(
            &ctx,
            vpx_codec_vp8_dx(),
            0,
            0) == VPX_CODEC_OK) {
        vpx_codec_destroy(&ctx);
    }

    return 0;
}
''',

    "c-ares": r'''
#include <stddef.h>
#include <string.h>
#include <ares.h>
int svf_probe(void)
{
    ares_channel_t *channel = NULL;
    struct ares_options opts;

    memset(&opts, 0, sizeof(opts));

    if (ares_init_options(
            &channel,
            &opts,
            0) == ARES_SUCCESS) {
        ares_destroy(channel);
    }

    return 0;
}
''',

    "lcms": r'''
#include <lcms2.h>
int svf_probe(void)
{
    cmsHPROFILE p = cmsCreate_sRGBProfile();
    if (p) cmsCloseProfile(p);
    return 0;
}
'''
}


def main():
    failures = []

    if REPORT.exists():
        print("ERROR=qualification report already exists")
        return 2

    c = json.loads(
        CONTRACT.read_text(encoding="utf-8")
    )

    compiler = c["compilation"]["compiler"]

    cp = run([compiler, "--version"])

    first = (
        cp.stdout.splitlines()[0]
        if cp.stdout.splitlines()
        else ""
    )

    print("COMPILER_VERSION=" + first)

    if cp.returncode != 0:
        failures.append("compiler_unavailable")

    if first != c["compilation"]["expected_compiler_version"]:
        failures.append("compiler_version")

    library_results = {}

    with tempfile.TemporaryDirectory(
        prefix="svf-postprocessing-qualification-"
    ) as temp_name:

        td = Path(temp_name)

        shim_c = td / "svf_weak_main.c"
        shim_o = td / "svf_weak_main.o"

        shim_c.write_text(
            c["compilation"][
                "external_weak_main_shim"
            ]["source"],
            encoding="utf-8"
        )

        shim_proc = run([
            compiler,
            "-std=gnu11",
            "-c",
            str(shim_c),
            "-o",
            str(shim_o)
        ])

        print(
            "QUALIFY|WEAK_MAIN|"
            + (
                "PASS"
                if shim_proc.returncode == 0
                else "FAIL"
            )
        )

        if shim_proc.returncode != 0:
            failures.append("weak_main")

        for name, cfg in c["libraries"].items():
            source = td / (name + ".c")
            output = td / (name + ".exe")

            source.write_text(
                SOURCES[name].lstrip("\n"),
                encoding="utf-8"
            )

            cmd = [
                compiler,
                *c["compilation"]["common_flags"]
            ]

            for inc in cfg["include_dirs"]:
                cmd.extend(["-I", inc])

            cmd.extend([
                str(source),
                str(shim_o),
                cfg["static_artifact"],
                *c["compilation"]["system_link_tail"],
                "-o",
                str(output)
            ])

            proc = run(cmd)

            warnings = sum(
                1
                for line in proc.stdout.splitlines()
                if "warning:" in line
            )

            passed = (
                proc.returncode == 0
                and output.is_file()
            )

            print(
                "QUALIFY|{}|{}|exit={}|warnings={}".format(
                    name,
                    "PASS" if passed else "FAIL",
                    proc.returncode,
                    warnings
                )
            )

            if not passed:
                failures.append("compile_" + name)

            library_results[name] = {
                "compiler_exit_code":
                    proc.returncode,

                "compiler_warning_count":
                    warnings,

                "linked_executable_created":
                    output.is_file(),

                "linked_executable_executed":
                    False,

                "static_artifact_sha256":
                    sha(cfg["static_artifact"]),

                "compiler_log":
                    proc.stdout,
            }

    extraction_cases = [
        (
            "raw_c",
            "int f(void){return 0;}\n",
            "EXTRACTED_VERBATIM"
        ),
        (
            "leading_trailing_whitespace",
            "\n int f(void){return 0;}\n\n",
            "EXTRACTED_VERBATIM"
        ),
        (
            "markdown_fence",
            "```c\nint f(void){return 0;}\n```\n",
            "EXTRACTED_VERBATIM"
        ),
        (
            "commentary",
            "Here is code:\nint f(void){return 0;}\n",
            "EXTRACTED_VERBATIM"
        ),
        (
            "empty",
            "",
            "MISSING_CODE"
        ),
        (
            "whitespace_only",
            " \n\t",
            "MISSING_CODE"
        ),
        (
            "non_string",
            None,
            "EXTRACTION_FAILURE"
        ),
    ]

    extraction_results = []

    for name, original, expected in extraction_cases:
        actual, preserved = classify(original)

        unchanged = (
            preserved == original
            if isinstance(original, str)
            else preserved is None
        )

        passed = (
            actual == expected
            and unchanged
        )

        print(
            "EXTRACTION|{}|{}|{}".format(
                name,
                "PASS" if passed else "FAIL",
                actual
            )
        )

        if not passed:
            failures.append(
                "extraction_" + name
            )

        extraction_results.append({
            "case": name,
            "expected": expected,
            "actual": actual,
            "content_unchanged": unchanged,
            "pass": passed,
        })

    pass_count = sum(
        1
        for r in library_results.values()
        if (
            r["compiler_exit_code"] == 0
            and r["linked_executable_created"]
        )
    )

    report = {
        "schema_version": "1.0.0",

        "qualification_id":
            "SVF-PRIMARY-POSTPROCESSING-QUALIFICATION-V1",

        "qualified_at_utc":
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z"),

        "contract_sha256":
            sha(CONTRACT),

        "decision_0010_sha256":
            sha(DECISION),

        "verifier_sha256":
            sha(VERIFIER),

        "qualification_runner_sha256":
            sha(Path(__file__).resolve()),

        "compiler_version":
            first,

        "library_results":
            library_results,

        "extraction_results":
            extraction_results,

        "synthetic_library_pass_count":
            pass_count,

        "linked_executables_executed":
            False,

        "live_provider_calls":
            0,

        "primary_generation_performed":
            False,

        "generated_driver_inspection":
            False,

        "analyzer_implementation":
            False,

        "repair_implementation":
            False,

        "qualification_status":
            "PASS" if not failures else "FAIL",

        "failures":
            failures,
    }

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
            ensure_ascii=False
        ) + "\n",
        encoding="utf-8"
    )

    print(
        "SYNTHETIC_LIBRARY_PASS_COUNT="
        + str(pass_count)
        + "_OF_8"
    )

    print(
        "QUALIFICATION_REPORT_SHA256="
        + sha(REPORT)
    )

    print(
        "POSTPROCESSING_QUALIFICATION="
        + report["qualification_status"]
    )

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
