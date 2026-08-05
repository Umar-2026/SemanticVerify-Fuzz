#!/usr/bin/env python3

import datetime
import hashlib
import json
import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "config" / "toolchain_lock.json"
SMOKE_SOURCE = ROOT / "tests" / "toolchain_smoke"
REPORT_PATH = (
    ROOT
    / "evidence"
    / "gates"
    / "gate0"
    / "environment_qualification.json"
)

def run(command, cwd=None):
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    if result.returncode != 0:
        rendered = " ".join(str(part) for part in command)
        raise RuntimeError(
            f"command failed ({result.returncode}): {rendered}\n"
            f"{result.stdout}"
        )

    return result.stdout.strip()

def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

try:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))

    required_commands = [
        "clang-14",
        "clang++-14",
        "llvm-config-14",
        "cmake",
        "ninja",
        "git",
        "python3",
    ]

    command_paths = {}

    for command in required_commands:
        resolved = shutil.which(command)
        require(resolved is not None, f"missing command: {command}")
        command_paths[command] = resolved

    package_versions = {}

    for package, expected_version in lock["apt_packages"].items():
        actual_version = run([
            "dpkg-query",
            "-W",
            "-f=${Version}",
            package,
        ])

        require(
            actual_version == expected_version,
            f"{package}: expected {expected_version}, got {actual_version}",
        )

        package_versions[package] = actual_version

    llvm_include = Path(run(["llvm-config-14", "--includedir"]))
    llvm_libdir = run(["llvm-config-14", "--libdir"])
    llvm_cmakedir = run(["llvm-config-14", "--cmakedir"])

    require(
        (llvm_include / "clang" / "Tooling" / "Tooling.h").is_file(),
        "Clang LibTooling header missing",
    )
    require(
        (llvm_include / "clang" / "Analysis" / "CFG.h").is_file(),
        "Clang CFG header missing",
    )

    with tempfile.TemporaryDirectory(
        prefix="svf-gate0b-",
        dir="/tmp",
    ) as temporary:
        temporary_path = Path(temporary)

        sanitizer_source = temporary_path / "sanitizer_smoke.c"
        sanitizer_binary = temporary_path / "sanitizer_smoke"

        sanitizer_source.write_text(
            "int main(void) { return 0; }\n",
            encoding="utf-8",
        )

        run([
            "clang-14",
            "-std=c11",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-fsanitize=address,undefined",
            str(sanitizer_source),
            "-o",
            str(sanitizer_binary),
        ])

        run([str(sanitizer_binary)])

        build_path = temporary_path / "libtooling-build"

        cmake_output = run([
            "cmake",
            "-S",
            str(SMOKE_SOURCE),
            "-B",
            str(build_path),
            "-G",
            "Ninja",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_C_COMPILER=clang-14",
            "-DCMAKE_CXX_COMPILER=clang++-14",
            f"-DLLVM_DIR={llvm_cmakedir}",
            "-DClang_DIR=/usr/lib/llvm-14/lib/cmake/clang",
        ])

        build_output = run([
            "cmake",
            "--build",
            str(build_path),
        ])

        run([str(build_path / "svf_clang_smoke")])

    report = {
        "schema_version": "1.0.0",
        "gate": "Gate 0B",
        "status": "PASS",
        "qualified_at_utc": (
            datetime.datetime.now(datetime.timezone.utc)
            .replace(microsecond=0)
            .isoformat()
        ),
        "repository": {
            "logical_path": (
                "/openbayes/home/semanticverify-fuzz-research"
            ),
            "physical_path": str(ROOT),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "cpu_count": os.cpu_count(),
        },
        "commands": command_paths,
        "versions": {
            "python": platform.python_version(),
            "git": run(["git", "--version"]),
            "cmake": run(["cmake", "--version"]).splitlines()[0],
            "ninja": run(["ninja", "--version"]),
            "clang": run(["clang-14", "--version"]).splitlines()[0],
            "llvm": run(["llvm-config-14", "--version"]),
        },
        "llvm": {
            "include_directory": str(llvm_include),
            "library_directory": llvm_libdir,
            "cmake_directory": llvm_cmakedir,
            "libtooling_header": "PASS",
            "cfg_header": "PASS",
        },
        "package_versions": package_versions,
        "tests": {
            "asan_ubsan_compile": "PASS",
            "asan_ubsan_run": "PASS",
            "clang_libtooling_configure": "PASS",
            "clang_libtooling_build": "PASS",
            "clang_cfg_runtime": "PASS",
        },
        "artifact_digests": {
            "toolchain_lock_sha256": sha256(LOCK_PATH),
            "cmake_smoke_sha256": sha256(
                SMOKE_SOURCE / "CMakeLists.txt"
            ),
            "cpp_smoke_sha256": sha256(
                SMOKE_SOURCE / "main.cpp"
            ),
        },
        "cmake_configure_tail": cmake_output.splitlines()[-12:],
        "cmake_build_tail": build_output.splitlines()[-12:],
        "repair_implementation_allowed": False,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("GATE0B_ENVIRONMENT_QUALIFICATION=PASS")
    print("SANITIZER_SMOKE=PASS")
    print("CLANG_LIBTOOLING_CONFIGURE=PASS")
    print("CLANG_LIBTOOLING_BUILD=PASS")
    print("CLANG_CFG_RUNTIME=PASS")
    print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
    print(f"REPORT={REPORT_PATH}")
    print(f"REPORT_SHA256={sha256(REPORT_PATH)}")

except Exception as error:
    print("GATE0B_ENVIRONMENT_QUALIFICATION=FAIL")
    print(f"REASON={error}")
    raise SystemExit(1)
