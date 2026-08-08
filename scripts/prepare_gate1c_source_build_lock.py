#!/usr/bin/env python3

import datetime
import hashlib
import json
import os
import shutil
import stat
import subprocess
from pathlib import Path


ROOT = Path("/openbayes/home/semanticverify-fuzz-research").resolve()
EXPECTED_HEAD = "7bd21639abcd39f2917767f01cc0e30855807661"

SELF_REL = "scripts/prepare_gate1c_source_build_lock.py"
LOCK_REL = "config/library_source_build_lock.json"
REPORT_REL = "evidence/gates/gate1/gate1c_source_build_lock.json"
EVIDENCE_DIR_REL = "evidence/gates/gate1/gate1c_source_build"
VERIFIER_REL = "scripts/verify_gate1c_source_build_lock.py"
DECISION_REL = (
    "documentation/decisions/"
    "0009-gate1c-eight-library-source-build-freeze.md"
)
RESEARCH_LOCK_REL = "config/research_lock.json"
STATUS_REL = "documentation/CURRENT_STATUS.md"
README_REL = "evidence/gates/gate1/README.md"

PROPOSAL_REL = (
    "provenance/proposal/"
    "SemanticVerify-Fuzz_Verification-First_Staged-Repair_Proposal.docx"
)

EXPECTED_PROPOSAL_SHA256 = (
    "3abc92ee7ac0100a6b9ac148a2ad2a4ca"
    "71d187677cb84abf1545de29afb4a21"
)

SOURCE_ROOT = Path(
    "/openbayes/home/svf-gate1c-source-qualification-v1"
)

V1 = Path(
    "/openbayes/home/svf-gate1c-build-qualification-v1"
)

V2 = Path(
    "/openbayes/home/svf-gate1c-build-qualification-v2"
)

V3 = Path(
    "/openbayes/home/svf-gate1c-build-qualification-v3"
)


def fail(reason):
    print("GATE1C_SOURCE_BUILD_PREPARATION=FAIL")
    print(f"REASON={reason}")
    raise SystemExit(1)


def require(condition, reason):
    if not condition:
        fail(reason)


def capture(command, cwd=ROOT):
    result = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    require(
        result.returncode == 0,
        "command failed: " + " ".join(command)
        + " :: " + result.stderr.strip()[:300],
    )
    return result.stdout.strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_new(relative, text, executable=False):
    path = ROOT / relative
    require(not path.exists(), f"refusing to overwrite {relative}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if executable:
        path.chmod(
            path.stat().st_mode
            | stat.S_IXUSR
            | stat.S_IXGRP
            | stat.S_IXOTH
        )


def package_version(name):
    return capture(
        ["dpkg-query", "-W", "-f=${Version}", name]
    )


require(ROOT.is_dir(), "repository missing")
require(
    capture(["git", "rev-parse", "HEAD"]) == EXPECTED_HEAD,
    "unexpected HEAD",
)

status_before = capture(
    ["git", "status", "--porcelain", "--untracked-files=all"]
)

actual_before = set(
    status_before.splitlines()
) if status_before else set()

require(
    actual_before <= {f"?? {SELF_REL}"},
    f"unexpected worktree changes: {sorted(actual_before)}",
)

require(
    not os.environ.get("DEEPSEEK_API_KEY")
    and not os.environ.get("GEMINI_API_KEY"),
    "LLM API keys must not be loaded during Gate 1C freeze",
)

require(
    digest(ROOT / PROPOSAL_REL)
    == EXPECTED_PROPOSAL_SHA256,
    "proposal SHA",
)

# Required previous gates.
for script in [
    "scripts/verify_gate0_final_manifest.py",
    "scripts/verify_gate1a_obligation_contract.py",
    "scripts/verify_gate1b_sampling_annotation_protocol.py",
]:
    result = subprocess.run(
        ["python3", script],
        cwd=ROOT,
        check=False,
    )
    require(
        result.returncode == 0,
        f"required verifier failed: {script}",
    )

# Exact package prerequisites established during corrective qualification.
expected_packages = {
    "flex": "2.6.4-8build2",
    "bison": "2:3.8.2+dfsg-1build1",
    "nasm": "2.15.05-1",
}

for package, expected in expected_packages.items():
    observed = package_version(package)
    require(
        observed == expected,
        f"{package} version: {observed} != {expected}",
    )

make_package_version = package_version("make")

libraries = [
    {
        "name": "zlib",
        "role": "development",
        "remote": "https://github.com/madler/zlib.git",
        "tag": "v1.3.2",
        "tag_type": "annotated",
        "tag_object":
            "216c70c020aa53f0c40920d155f808b6b59c9acb",
        "commit":
            "da607da739fa6047df13e66a2af6b8bec7c2a498",
        "tree":
            "79b5a06f88838dd54f90f821e8650254abfedb7e",
        "archive_sha256":
            "febf9d99c459f379f53467ec0ada70d8da99b3f49ba9dbc7c84b21592f6ce17e",
        "workspace": "V1",
        "artifact_rel": "build/zlib/libz.a",
        "artifact_sha256":
            "35a0f48b95d3ba921e64dfddcf17ea00a54795963956b8b1d07deb68422b2e6a",
        "configure_log_rel": "logs/zlib.configure.log",
        "configure_log_sha256":
            "c1a31fe03efd0ceac3b97cf32301db1154ac6e6c4bc0487d24bfc8a02546835f",
        "build_log_rel": "logs/zlib.build.log",
        "build_log_sha256":
            "300a70bd2246dc75902553efd08ee974e8a3f68750d524bfcb542b12a3fc4301",
        "metadata_rel": "build/zlib/CMakeCache.txt",
        "build_system": "CMake+Ninja",
        "configure_command": [
            "cmake", "-S", "<SOURCE>", "-B", "<BUILD>", "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_C_COMPILER=/usr/bin/clang-14",
            "-DCMAKE_CXX_COMPILER=/usr/bin/clang++-14",
            "-DCMAKE_AR=/usr/bin/llvm-ar-14",
            "-DCMAKE_RANLIB=/usr/bin/llvm-ranlib-14",
            "-DZLIB_BUILD_SHARED=OFF",
            "-DZLIB_BUILD_STATIC=ON",
            "-DZLIB_BUILD_TESTING=OFF",
            "-DZLIB_INSTALL=OFF",
        ],
        "build_command": [
            "cmake", "--build", "<BUILD>", "--parallel", "2"
        ],
        "dependency_policy": "No optional external dependency required.",
    },
    {
        "name": "libpcap",
        "role": "validation",
        "remote":
            "https://github.com/the-tcpdump-group/libpcap.git",
        "tag": "libpcap-1.10.6",
        "tag_type": "annotated",
        "tag_object":
            "56b49bd36ca00c2844927581219f84272f614a5c",
        "commit":
            "a999701dca5c873779281938baee6bc185a8d4dc",
        "tree":
            "6e91ac97f337382c213e1c6481b63813674bcad4",
        "archive_sha256":
            "1fbdf1855ddeeb7cb8dd5274c067522bd75f0d9a8dfcbe7639a50c5ecb52c45a",
        "workspace": "V2",
        "artifact_rel": "build/libpcap/libpcap.a",
        "artifact_sha256":
            "06db8932a5d0b23e50a01902a3a320d9183c6d638468149f4861f7969dcc68bd",
        "configure_log_rel": "logs/libpcap.configure.log",
        "configure_log_sha256":
            "e98f65c4cb9e2b3d1e36c9bad757fbdd42223c7a4ca635a403fb1913f8db2e6f",
        "build_log_rel": "logs/libpcap.build.log",
        "build_log_sha256":
            "47a0c831ff8c20a358467079f6a426b5b6b152a0521506f8a84e37b462bf6931",
        "metadata_rel": "build/libpcap/CMakeCache.txt",
        "build_system": "CMake+Ninja",
        "configure_command": [
            "cmake", "-S", "<SOURCE>", "-B", "<BUILD>", "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_C_COMPILER=/usr/bin/clang-14",
            "-DCMAKE_CXX_COMPILER=/usr/bin/clang++-14",
            "-DCMAKE_AR=/usr/bin/llvm-ar-14",
            "-DCMAKE_RANLIB=/usr/bin/llvm-ranlib-14",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DBUILD_WITH_LIBNL=OFF",
            "-DDISABLE_BLUETOOTH=ON",
            "-DDISABLE_DBUS=ON",
            "-DDISABLE_LINUX_USBMON=ON",
            "-DDISABLE_RDMA=ON",
        ],
        "build_command": [
            "cmake", "--build", "<BUILD>", "--parallel", "2"
        ],
        "dependency_policy":
            "Flex and Bison pinned; optional capture backends disabled.",
    },
    {
        "name": "curl",
        "role": "held-out",
        "remote": "https://github.com/curl/curl.git",
        "tag": "curl-8_21_0",
        "tag_type": "annotated",
        "tag_object":
            "3f00a2f6fa97f7721b65606954aac979dcb6caac",
        "commit":
            "68720b4837284335b2d63cb358f8f6ce65f5bc55",
        "tree":
            "e23d273aeb073c04aa5b073b35c9fde16979c896",
        "archive_sha256":
            "d69307e6f6207ed87c5c42905fa83fc8186c44279a3f34cf892c6a8157271723",
        "workspace": "V3",
        "artifact_rel": "build/curl/lib/libcurl.a",
        "artifact_sha256":
            "126b13dbe516d5686c6d4ef054ed4aa37cb9a504aaea9dfff32cdbc44d429116",
        "configure_log_rel": "logs/curl.configure.log",
        "configure_log_sha256":
            "de98745b677f75dbde53627634174d1b9432c751af46eb2be57b0f62e3d1d4ce",
        "build_log_rel": "logs/curl.build.log",
        "build_log_sha256":
            "015913c7d6c8952f2156a90127f23128f58c49844c813fdaab80d639eead4e5a",
        "metadata_rel": "build/curl/CMakeCache.txt",
        "build_system": "CMake+Ninja",
        "configure_command": [
            "cmake", "-S", "<SOURCE>", "-B", "<BUILD>", "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_C_COMPILER=/usr/bin/clang-14",
            "-DCMAKE_AR=/usr/bin/llvm-ar-14",
            "-DCMAKE_RANLIB=/usr/bin/llvm-ranlib-14",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DBUILD_STATIC_LIBS=ON",
            "-DBUILD_CURL_EXE=OFF",
            "-DBUILD_EXAMPLES=OFF",
            "-DBUILD_LIBCURL_DOCS=OFF",
            "-DBUILD_MISC_DOCS=OFF",
            "-DBUILD_TESTING=OFF",
            "-DCURL_ENABLE_SSL=OFF",
            "-DCURL_USE_LIBPSL=OFF",
            "-DCURL_USE_LIBSSH2=OFF",
            "-DUSE_NGHTTP2=OFF",
            "-DCURL_ZLIB=OFF",
            "-DCURL_ZSTD=OFF",
            "-DCURL_BROTLI=OFF",
        ],
        "build_command": [
            "cmake", "--build", "<BUILD>", "--parallel", "2"
        ],
        "dependency_policy":
            "Final V3 dependency-stable build disables TLS, PSL, SSH2, "
            "NGHTTP2, zlib, zstd, and brotli optional integrations.",
    },
    {
        "name": "cJSON",
        "role": "held-out",
        "remote": "https://github.com/DaveGamble/cJSON.git",
        "tag": "v1.7.19",
        "tag_type": "lightweight",
        "tag_object":
            "c859b25da02955fef659d658b8f324b5cde87be3",
        "commit":
            "c859b25da02955fef659d658b8f324b5cde87be3",
        "tree":
            "9c7b88a72ea9f3658c7f08c26b5cb09470f51761",
        "archive_sha256":
            "9d30fc24ed6290447f2f852152c324deb0044f59479afed005357f3d5ea0f03a",
        "workspace": "V1",
        "artifact_rel": "build/cJSON/libcjson.a",
        "artifact_sha256":
            "875e7d573bb4abe736b5ce7a3a95b7422891ce279e835d75bcfef3a675618470",
        "configure_log_rel": "logs/cJSON.configure.log",
        "configure_log_sha256":
            "c96c4d54fc6dd3bf6d78c4fb118bda7a711c1b0c61220d1e0ec379dff31195c6",
        "build_log_rel": "logs/cJSON.build.log",
        "build_log_sha256":
            "2eb63e4a8ebd67d113dfc7136603adea36ab5ea38780d3b1df3690a76e00b495",
        "metadata_rel": "build/cJSON/CMakeCache.txt",
        "build_system": "CMake+Ninja",
        "configure_command": [
            "cmake", "-S", "<SOURCE>", "-B", "<BUILD>", "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_C_COMPILER=/usr/bin/clang-14",
            "-DCMAKE_CXX_COMPILER=/usr/bin/clang++-14",
            "-DCMAKE_AR=/usr/bin/llvm-ar-14",
            "-DCMAKE_RANLIB=/usr/bin/llvm-ranlib-14",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DENABLE_CJSON_TEST=OFF",
            "-DENABLE_SANITIZERS=OFF",
        ],
        "build_command": [
            "cmake", "--build", "<BUILD>", "--parallel", "2"
        ],
        "dependency_policy": "Static core-library qualification.",
    },
    {
        "name": "libtiff",
        "role": "held-out",
        "remote": "https://gitlab.com/libtiff/libtiff.git",
        "tag": "v4.7.2",
        "tag_type": "annotated",
        "tag_object":
            "f1cabd542a228e0e8a8ea1f92e825b0063de86fe",
        "commit":
            "d01a94be176f5f6a87f7ee1c0b32e65416aa2b4d",
        "tree":
            "383ac4e604330018281e552e169d91a5f3ed25a1",
        "archive_sha256":
            "c040cf975f30f74fa586700ce3b5191bc6543b696ed2c99f62c53399960a4ea2",
        "workspace": "V1",
        "artifact_rel": "build/libtiff/libtiff/libtiff.a",
        "artifact_sha256":
            "c5a4841f14d72041fe67e22b98e0179d1a52173e3bd03e183bdf0d7e526ba4ef",
        "configure_log_rel": "logs/libtiff.configure.log",
        "configure_log_sha256":
            "903f436e7a18869daf95a81a8a193d6c581199b1653ad764812b0e843ea5ccbb",
        "build_log_rel": "logs/libtiff.build.log",
        "build_log_sha256":
            "94c1363f0b616d91117dba077c0235da7f5ea96e3ca4a354935a9e357a26151a",
        "metadata_rel": "build/libtiff/CMakeCache.txt",
        "build_system": "CMake+Ninja",
        "configure_command": [
            "cmake", "-S", "<SOURCE>", "-B", "<BUILD>", "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_C_COMPILER=/usr/bin/clang-14",
            "-DCMAKE_CXX_COMPILER=/usr/bin/clang++-14",
            "-DCMAKE_AR=/usr/bin/llvm-ar-14",
            "-DCMAKE_RANLIB=/usr/bin/llvm-ranlib-14",
            "-DBUILD_SHARED_LIBS=OFF",
            "-Dtiff-tools=OFF",
            "-Dtiff-tests=OFF",
            "-Dtiff-docs=OFF",
            "-Djbig=OFF",
            "-Djpeg=OFF",
            "-Dlerc=OFF",
            "-Dlibdeflate=OFF",
            "-Dlzma=OFF",
            "-Dwebp=OFF",
            "-Dzlib=OFF",
            "-Dzstd=OFF",
        ],
        "build_command": [
            "cmake", "--build", "<BUILD>", "--parallel", "2"
        ],
        "dependency_policy":
            "Optional codecs and external compression integrations disabled.",
    },
    {
        "name": "libvpx",
        "role": "held-out",
        "remote": "https://github.com/webmproject/libvpx.git",
        "tag": "v1.16.0",
        "tag_type": "annotated",
        "tag_object":
            "04def0a07f8bfa95785e30e6db95036cda17f9b2",
        "commit":
            "1024874c5919305883187e2953de8fcb4c3d7fa6",
        "tree":
            "5e48c010122b13fe684e4419d45feee3157d7387",
        "archive_sha256":
            "703d3d4a2b2a70b82e3e4a44107f21e621435e61f5f25999b5d392273abac27c",
        "workspace": "V2",
        "artifact_rel": "build/libvpx/libvpx.a",
        "artifact_sha256":
            "dcc6014ef56ccbfb7c371e02460ac9b046c542e215a6274d8aebdc4b3ec7ac8a",
        "configure_log_rel": "logs/libvpx.configure.log",
        "configure_log_sha256":
            "8e9c60d07ec28666c96f89c8980136ef9463e15bb40f2dc80a05a9d16e6bb681",
        "build_log_rel": "logs/libvpx.build.log",
        "build_log_sha256":
            "9bd88d60d0f0dfbd75d37358cfc3ae7fc69d7dd81186f233dfbdb8fcf9f8a7d3",
        "metadata_rel": "build/libvpx/config.log",
        "build_system": "libvpx configure+GNU Make",
        "configure_environment": {
            "CC": "/usr/bin/clang-14",
            "CXX": "/usr/bin/clang++-14",
            "AR": "/usr/bin/llvm-ar-14",
            "RANLIB": "/usr/bin/llvm-ranlib-14",
        },
        "configure_command": [
            "<SOURCE>/configure",
            "--target=x86_64-linux-gcc",
            "--as=nasm",
            "--disable-examples",
            "--disable-tools",
            "--disable-docs",
            "--disable-unit-tests",
        ],
        "build_command": [
            "make", "-C", "<BUILD>", "-j2"
        ],
        "dependency_policy":
            "NASM explicitly pinned; assembler auto-selection prohibited.",
    },
    {
        "name": "c-ares",
        "role": "held-out",
        "remote": "https://github.com/c-ares/c-ares.git",
        "tag": "v1.34.8",
        "tag_type": "annotated",
        "tag_object":
            "63a4c4c71b86e448bcc1c55287c35aa4aa0f4246",
        "commit":
            "c7a3138dcfe3bb0eaaf10c0c24c36dc66dc790ab",
        "tree":
            "14315b31d0b2cf5cfde9f0b1544176221393295b",
        "archive_sha256":
            "5d61068d46246a6c9d3ae7c0eee580fde06fe30298df6a5b4cdcfbb978e15e31",
        "workspace": "V1",
        "artifact_rel": "build/c-ares/lib/libcares.a",
        "artifact_sha256":
            "cf2557f712a041dbd0983e2ccd80b266aede978a6fc6f078a9e57089f42262b7",
        "configure_log_rel": "logs/c-ares.configure.log",
        "configure_log_sha256":
            "cb1e7d063e335c777cd9aec3f8c2be251cc3db3f861a48e1992296db2f63ee4f",
        "build_log_rel": "logs/c-ares.build.log",
        "build_log_sha256":
            "65623496c5173ea16ad0086b24600f2f9adb8a162dae4795c115b140dafefb36",
        "metadata_rel": "build/c-ares/CMakeCache.txt",
        "build_system": "CMake+Ninja",
        "configure_command": [
            "cmake", "-S", "<SOURCE>", "-B", "<BUILD>", "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_C_COMPILER=/usr/bin/clang-14",
            "-DCMAKE_CXX_COMPILER=/usr/bin/clang++-14",
            "-DCMAKE_AR=/usr/bin/llvm-ar-14",
            "-DCMAKE_RANLIB=/usr/bin/llvm-ranlib-14",
            "-DCARES_SHARED=OFF",
            "-DCARES_STATIC=ON",
            "-DCARES_BUILD_TESTS=OFF",
            "-DCARES_BUILD_TOOLS=OFF",
            "-DCARES_BUILD_CONTAINER_TESTS=OFF",
        ],
        "build_command": [
            "cmake", "--build", "<BUILD>", "--parallel", "2"
        ],
        "dependency_policy": "Static core-library qualification.",
    },
    {
        "name": "lcms",
        "role": "held-out",
        "remote": "https://github.com/mm2/Little-CMS.git",
        "tag": "lcms2.19.1",
        "tag_type": "lightweight",
        "tag_object":
            "21c582a594fe5279f90c0b93437c398f93bf62b0",
        "commit":
            "21c582a594fe5279f90c0b93437c398f93bf62b0",
        "tree":
            "11fed2281a421dba849b595357f92466363f1190",
        "archive_sha256":
            "a1f057b15c11cbcacf473ae7a30ebd7d81bccfa8e1f1a88fa7cde893e73fc651",
        "workspace": "V3",
        "artifact_rel": "build/lcms/liblcms2.a",
        "artifact_sha256":
            "1f9b60abf3abe289fd169aa891db8149c98eb4c213dd7c9a7aef08d9b2ba9e3e",
        "configure_log_rel": "logs/lcms.configure.log",
        "configure_log_sha256":
            "69c38a0953dc08c4bc7883b61bb69be73720bf38a3fece70fefa17cb74cd8126",
        "build_log_rel": "logs/lcms.build.log",
        "build_log_sha256":
            "2240440ce69ad1553b1f40ddd6a89090dcb127ce62c33d7dcc5e114ebc16aed7",
        "metadata_rel": "build/lcms/CMakeCache.txt",
        "build_system": "CMake+Ninja",
        "configure_command": [
            "cmake", "-S", "<SOURCE>", "-B", "<BUILD>", "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_C_COMPILER=/usr/bin/clang-14",
            "-DCMAKE_AR=/usr/bin/llvm-ar-14",
            "-DCMAKE_RANLIB=/usr/bin/llvm-ranlib-14",
            "-DLCMS2_BUILD_SHARED=OFF",
            "-DLCMS2_BUILD_STATIC=ON",
            "-DLCMS2_BUILD_TESTS=OFF",
            "-DLCMS2_BUILD_TOOLS=OFF",
            "-DLCMS2_BUILD_JPGICC=OFF",
            "-DLCMS2_BUILD_TIFICC=OFF",
            "-DLCMS2_BUILD_TIFDIFF=OFF",
            "-DLCMS2_WITH_JPEG=OFF",
            "-DLCMS2_WITH_ZLIB=OFF",
            "-DLCMS2_WITH_TIFF=OFF",
        ],
        "build_command": [
            "cmake", "--build", "<BUILD>", "--parallel", "2"
        ],
        "dependency_policy":
            "Final V3 dependency-stable build disables JPEG, TIFF and zlib.",
    },
]

workspaces = {
    "V1": V1,
    "V2": V2,
    "V3": V3,
}

# Validate exact source identity and final build evidence before writing anything.
for item in libraries:
    source_repo = SOURCE_ROOT / item["name"]
    require(source_repo.is_dir(), f"source missing: {item['name']}")

    observed_commit = capture(
        ["git", "rev-parse", "HEAD"],
        cwd=source_repo,
    )
    observed_tree = capture(
        ["git", "rev-parse", "HEAD^{tree}"],
        cwd=source_repo,
    )
    observed_status = capture(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=source_repo,
    )

    require(
        observed_commit == item["commit"],
        f"{item['name']} commit mismatch",
    )
    require(
        observed_tree == item["tree"],
        f"{item['name']} tree mismatch",
    )
    require(
        observed_status == "",
        f"{item['name']} source worktree dirty",
    )

    ws = workspaces[item["workspace"]]

    artifact = ws / item["artifact_rel"]
    configure_log = ws / item["configure_log_rel"]
    build_log = ws / item["build_log_rel"]
    metadata = ws / item["metadata_rel"]

    require(artifact.is_file(), f"{item['name']} artifact missing")
    require(
        digest(artifact) == item["artifact_sha256"],
        f"{item['name']} artifact SHA",
    )
    require(
        digest(configure_log) == item["configure_log_sha256"],
        f"{item['name']} configure log SHA",
    )
    require(
        digest(build_log) == item["build_log_sha256"],
        f"{item['name']} build log SHA",
    )
    require(
        metadata.is_file(),
        f"{item['name']} build metadata missing",
    )

# Transparent failed-attempt provenance.
v1_libpcap_failed = V1 / "logs/libpcap.configure.log"
v1_libvpx_failed = V1 / "logs/libvpx.configure.log"

require(v1_libpcap_failed.is_file(), "V1 libpcap failed log missing")
require(v1_libvpx_failed.is_file(), "V1 libvpx failed log missing")

require(
    b"Neither flex nor win_flex nor lex was found"
    in v1_libpcap_failed.read_bytes(),
    "libpcap V1 failure reason",
)

require(
    b'Unknown option "--disable-asm"'
    in v1_libvpx_failed.read_bytes(),
    "libvpx V1 failure reason",
)

timestamp = (
    datetime.datetime.now(datetime.timezone.utc)
    .replace(microsecond=0)
    .isoformat()
)

evidence_dir = ROOT / EVIDENCE_DIR_REL
require(not evidence_dir.exists(), "Gate 1C evidence directory already exists")
evidence_dir.mkdir(parents=True)

# Persist final build logs and build metadata inside the research repository.
for item in libraries:
    ws = workspaces[item["workspace"]]

    final_configure = evidence_dir / f"{item['name']}.configure.log"
    final_build = evidence_dir / f"{item['name']}.build.log"

    metadata_name = (
        f"{item['name']}.config.log"
        if item["name"] == "libvpx"
        else f"{item['name']}.CMakeCache.txt"
    )
    final_metadata = evidence_dir / metadata_name

    shutil.copy2(ws / item["configure_log_rel"], final_configure)
    shutil.copy2(ws / item["build_log_rel"], final_build)
    shutil.copy2(ws / item["metadata_rel"], final_metadata)

    item["persistent_evidence"] = {
        "configure_log_path":
            final_configure.relative_to(ROOT).as_posix(),
        "configure_log_sha256": digest(final_configure),
        "build_log_path":
            final_build.relative_to(ROOT).as_posix(),
        "build_log_sha256": digest(final_build),
        "build_metadata_path":
            final_metadata.relative_to(ROOT).as_posix(),
        "build_metadata_sha256": digest(final_metadata),
    }

# Persist failed V1 diagnostic evidence.
failed_libpcap_dest = evidence_dir / "libpcap.v1_failed.configure.log"
failed_libvpx_dest = evidence_dir / "libvpx.v1_failed.configure.log"

shutil.copy2(v1_libpcap_failed, failed_libpcap_dest)
shutil.copy2(v1_libvpx_failed, failed_libvpx_dest)

toolchain_lock_path = ROOT / "config/toolchain_lock.json"

lock_value = {
    "schema_version": "1.0.0",
    "gate": "Gate 1C",
    "status": "PASS_FROZEN",
    "title": "Eight-Library Exact Source and Build Qualification Lock",
    "frozen_at_utc": timestamp,
    "authority": {
        "proposal_path": PROPOSAL_REL,
        "proposal_sha256": EXPECTED_PROPOSAL_SHA256,
        "gate1a_contract_sha256":
            digest(ROOT / "config/protocol_obligation_contract.json"),
        "gate1b_protocol_sha256":
            digest(ROOT / "config/gold_sampling_annotation_protocol.json"),
        "toolchain_lock_path": "config/toolchain_lock.json",
        "toolchain_lock_sha256": digest(toolchain_lock_path),
    },
    "scope": {
        "library_count": 8,
        "build_qualified_count": 8,
        "source_identity_verified_count": 8,
        "source_submodules_required": False,
        "generated_driver_content_inspected": False,
        "primary_generation_performed": False,
        "analyzer_implementation_performed": False,
        "repair_implementation_performed": False,
    },
    "source_snapshot_hash_definition": {
        "field": "commit_archive_sha256",
        "method":
            "SHA-256 of deterministic git archive of the pinned commit "
            "using the qualification prefix <library>-<commit>/",
        "official_release_tarball_hash": False,
    },
    "build_environment": {
        "operating_system": "Ubuntu 22.04.5 LTS",
        "architecture": "x86_64",
        "clang": "14.0.0",
        "cmake": "3.19.3",
        "ninja": "1.10.1",
        "make_package_version": make_package_version,
        "additional_exact_packages": expected_packages,
        "parallel_build_jobs": 2,
        "static_library_qualification": True,
    },
    "qualification_history": {
        "initial_v1": {
            "result": "6_OF_8_PASS",
            "libpcap_failure":
                "Missing required Flex/Lex generator.",
            "libvpx_failure":
                "Unqualified --disable-asm option rejected by pinned source.",
        },
        "corrective_v2": {
            "result": "LIBPCAP_AND_LIBVPX_PASS",
            "changes": [
                "Install and pin flex 2.6.4-8build2.",
                "Install and pin bison 2:3.8.2+dfsg-1build1.",
                "Install and pin nasm 2.15.05-1.",
                "Use libvpx --as=nasm instead of unsupported --disable-asm.",
            ],
        },
        "dependency_stable_v3": {
            "result": "CURL_AND_LCMS_PASS",
            "changes": [
                "curl optional compression/network dependency AUTO settings "
                "replaced by explicit OFF values.",
                "lcms optional TIFF/JPEG/zlib integrations explicitly disabled.",
            ],
        },
        "final_result": "8_OF_8_PASS",
        "failed_attempts_preserved": {
            "libpcap_v1_path":
                failed_libpcap_dest.relative_to(ROOT).as_posix(),
            "libpcap_v1_sha256": digest(failed_libpcap_dest),
            "libvpx_v1_path":
                failed_libvpx_dest.relative_to(ROOT).as_posix(),
            "libvpx_v1_sha256": digest(failed_libvpx_dest),
        },
    },
    "libraries": [],
    "stage_boundaries": {
        "current_stage": "Stage A - verification",
        "library_specific_protocol_rules_created": False,
        "scenario_bindings_created": 0,
        "primary_generation_authorized": False,
        "held_out_driver_inspection_allowed": False,
        "analyzer_implementation_authorized_by_gate1c": False,
        "repair_implementation_allowed": False,
        "repair_activation_gate": "Gate V",
    },
}

for item in libraries:
    lock_value["libraries"].append({
        "name": item["name"],
        "role": item["role"],
        "source": {
            "remote": item["remote"],
            "tag": item["tag"],
            "tag_type": item["tag_type"],
            "tag_object": item["tag_object"],
            "peeled_commit": item["commit"],
            "tree": item["tree"],
            "commit_archive_sha256": item["archive_sha256"],
        },
        "build": {
            "qualification_workspace": item["workspace"],
            "build_system": item["build_system"],
            "configure_environment":
                item.get("configure_environment", {}),
            "configure_command": item["configure_command"],
            "build_command": item["build_command"],
            "dependency_policy": item["dependency_policy"],
            "artifact_sha256": item["artifact_sha256"],
            "persistent_evidence": item["persistent_evidence"],
            "status": "PASS",
        },
    })

lock_path = ROOT / LOCK_REL
require(not lock_path.exists(), f"refusing to overwrite {LOCK_REL}")
write_json(lock_path, lock_value)

lock_sha = digest(lock_path)

report_value = {
    "schema_version": "1.0.0",
    "gate": "Gate 1C",
    "status": "PASS",
    "frozen_at_utc": timestamp,
    "lock_path": LOCK_REL,
    "lock_sha256": lock_sha,
    "library_count": 8,
    "source_identity_pass": 8,
    "build_qualification_pass": 8,
    "build_qualification_fail": 0,
    "final_build_set": "READY_TO_FREEZE",
    "persistent_final_configure_logs": 8,
    "persistent_final_build_logs": 8,
    "persistent_build_metadata_files": 8,
    "preserved_failed_configure_logs": 2,
    "additional_exact_build_packages": expected_packages,
    "library_specific_protocol_rules_created": False,
    "scenario_bindings_created": 0,
    "primary_generation_authorized": False,
    "held_out_driver_inspection_allowed": False,
    "analyzer_implementation_authorized": False,
    "repair_implementation_allowed": False,
}

report_path = ROOT / REPORT_REL
require(not report_path.exists(), f"refusing to overwrite {REPORT_REL}")
write_json(report_path, report_value)

report_sha = digest(report_path)

research_lock_path = ROOT / RESEARCH_LOCK_REL
research_lock = read_json(research_lock_path)

gate1 = research_lock["gate1_foundation"]

require(gate1["status"] == "IN_PROGRESS", "Gate 1 status")
require(
    gate1["primary_generation_authorized"] is False,
    "generation authorization changed unexpectedly",
)
require(
    gate1["held_out_driver_inspection_allowed"] is False,
    "held-out inspection changed unexpectedly",
)
require(
    gate1["analyzer_implementation_authorized"] is False,
    "analyzer authorization changed unexpectedly",
)
require(
    gate1["repair_implementation_allowed"] is False,
    "repair authorization changed unexpectedly",
)

gate1["gate1c_source_build_lock"] = {
    "status": "PASS",
    "lock_path": LOCK_REL,
    "lock_sha256": lock_sha,
    "report_path": REPORT_REL,
    "report_sha256": report_sha,
    "library_count": 8,
    "source_identity_pass": 8,
    "build_qualification_pass": 8,
    "additional_exact_build_packages": expected_packages,
}

research_lock["current_status"][
    "gate_1c_source_build_lock"
] = "PASS"

write_json(research_lock_path, research_lock)

# Persistent decision record.
decision = f"""# Decision 0009: Gate 1C exact source/build freeze

- Status: Accepted
- Gate: Gate 1C
- Frozen at UTC: {timestamp}

## Decision

Freeze the exact source identity and qualified build recipe for all eight
experimental libraries before any primary driver generation.

The final qualified set is 8/8 PASS. Source identity is bound by upstream
remote, tag, tag type, tag object where applicable, peeled commit, Git tree,
and deterministic qualification archive SHA-256.

The final build recipes are the exact recipes that were successfully
qualified with Clang/LLVM 14. curl and lcms use the dependency-stable V3
recipes. libpcap uses pinned Flex and Bison. libvpx uses pinned NASM with
explicit `--as=nasm`.

## Qualification history

The first build pass produced 6/8 PASS. libpcap failed because Flex/Lex was
not installed. libvpx failed because `--disable-asm` is not supported by the
pinned source. Those failures are preserved rather than erased.

The corrective V2 pass qualified libpcap and libvpx. V3 then removed
environment-sensitive optional dependency AUTO behavior from curl and lcms.

## Boundaries

This decision does not create library-specific protocol rules, does not
create any scenario binding, does not authorize primary generation, does not
authorize held-out driver inspection, and does not authorize analyzer or
repair implementation.

Repair remains prohibited until Gate V.
"""

write_new(DECISION_REL, decision)

# Append Gate 1 README.
readme_path = ROOT / README_REL
require(readme_path.is_file(), "Gate 1 README missing")

readme_text = readme_path.read_text(encoding="utf-8")

require(
    "Gate 1C exact source/build freeze" not in readme_text,
    "Gate 1C README section already exists",
)

readme_text += f"""

## Gate 1C exact source/build freeze

Status: **PASS**

All eight libraries have exact source identities and qualified reproducible
build recipes frozen in `{LOCK_REL}`. Final qualification is 8/8 PASS.
Qualification logs and build metadata are persisted under
`{EVIDENCE_DIR_REL}/`.

This gate does not authorize primary generation, held-out driver inspection,
analyzer implementation, or repair.
"""

readme_path.write_text(readme_text, encoding="utf-8")

# Update only the completed source/build item in CURRENT_STATUS.
status_path = ROOT / STATUS_REL
require(status_path.is_file(), "CURRENT_STATUS missing")

status_text = status_path.read_text(encoding="utf-8")

old_next = (
    "2. Freeze eight library source/build locks and provider price-sheet snapshots."
)
new_next = (
    "2. Freeze provider price-sheet snapshots."
)

require(
    old_next in status_text,
    "expected CURRENT_STATUS next-work line not found",
)

status_text = status_text.replace(old_next, new_next, 1)

status_text += f"""

## Gate 1C source/build status

Gate 1C source/build freeze: **PASS**.

Eight of eight pinned libraries have verified source identity and a
successful frozen build recipe. Final curl and lcms qualification uses the
dependency-stable V3 recipes. Primary generation remains unauthorized.
Analyzer implementation remains unauthorized. Repair remains prohibited
until Gate V.
"""

status_path.write_text(status_text, encoding="utf-8")

verifier = r'''#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOCK = ROOT / "config/library_source_build_lock.json"
REPORT = ROOT / "evidence/gates/gate1/gate1c_source_build_lock.json"
RESEARCH_LOCK = ROOT / "config/research_lock.json"

EXPECTED = {
    "zlib": {
        "role": "development",
        "commit": "da607da739fa6047df13e66a2af6b8bec7c2a498",
        "tree": "79b5a06f88838dd54f90f821e8650254abfedb7e",
        "artifact": "35a0f48b95d3ba921e64dfddcf17ea00a54795963956b8b1d07deb68422b2e6a",
    },
    "libpcap": {
        "role": "validation",
        "commit": "a999701dca5c873779281938baee6bc185a8d4dc",
        "tree": "6e91ac97f337382c213e1c6481b63813674bcad4",
        "artifact": "06db8932a5d0b23e50a01902a3a320d9183c6d638468149f4861f7969dcc68bd",
    },
    "curl": {
        "role": "held-out",
        "commit": "68720b4837284335b2d63cb358f8f6ce65f5bc55",
        "tree": "e23d273aeb073c04aa5b073b35c9fde16979c896",
        "artifact": "126b13dbe516d5686c6d4ef054ed4aa37cb9a504aaea9dfff32cdbc44d429116",
    },
    "cJSON": {
        "role": "held-out",
        "commit": "c859b25da02955fef659d658b8f324b5cde87be3",
        "tree": "9c7b88a72ea9f3658c7f08c26b5cb09470f51761",
        "artifact": "875e7d573bb4abe736b5ce7a3a95b7422891ce279e835d75bcfef3a675618470",
    },
    "libtiff": {
        "role": "held-out",
        "commit": "d01a94be176f5f6a87f7ee1c0b32e65416aa2b4d",
        "tree": "383ac4e604330018281e552e169d91a5f3ed25a1",
        "artifact": "c5a4841f14d72041fe67e22b98e0179d1a52173e3bd03e183bdf0d7e526ba4ef",
    },
    "libvpx": {
        "role": "held-out",
        "commit": "1024874c5919305883187e2953de8fcb4c3d7fa6",
        "tree": "5e48c010122b13fe684e4419d45feee3157d7387",
        "artifact": "dcc6014ef56ccbfb7c371e02460ac9b046c542e215a6274d8aebdc4b3ec7ac8a",
    },
    "c-ares": {
        "role": "held-out",
        "commit": "c7a3138dcfe3bb0eaaf10c0c24c36dc66dc790ab",
        "tree": "14315b31d0b2cf5cfde9f0b1544176221393295b",
        "artifact": "cf2557f712a041dbd0983e2ccd80b266aede978a6fc6f078a9e57089f42262b7",
    },
    "lcms": {
        "role": "held-out",
        "commit": "21c582a594fe5279f90c0b93437c398f93bf62b0",
        "tree": "11fed2281a421dba849b595357f92466363f1190",
        "artifact": "1f9b60abf3abe289fd169aa891db8149c98eb4c213dd7c9a7aef08d9b2ba9e3e",
    },
}


def fail(reason):
    print("GATE1C_SOURCE_BUILD_LOCK=FAIL")
    print(f"REASON={reason}")
    raise SystemExit(1)


def require(condition, reason):
    if not condition:
        fail(reason)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for path in [LOCK, REPORT, RESEARCH_LOCK]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")

lock = json.loads(LOCK.read_text(encoding="utf-8"))
report = json.loads(REPORT.read_text(encoding="utf-8"))
research = json.loads(RESEARCH_LOCK.read_text(encoding="utf-8"))

require(lock["gate"] == "Gate 1C", "gate")
require(lock["status"] == "PASS_FROZEN", "lock status")
require(lock["scope"]["library_count"] == 8, "library count")
require(lock["scope"]["source_identity_verified_count"] == 8, "source count")
require(lock["scope"]["build_qualified_count"] == 8, "build count")
require(lock["qualification_history"]["final_result"] == "8_OF_8_PASS", "final result")

libraries = lock["libraries"]
require(len(libraries) == 8, "library records")

observed_names = [item["name"] for item in libraries]
require(observed_names == list(EXPECTED), "library order/names")

for item in libraries:
    name = item["name"]
    expected = EXPECTED[name]

    require(item["role"] == expected["role"], f"{name} role")
    require(
        item["source"]["peeled_commit"] == expected["commit"],
        f"{name} commit",
    )
    require(
        item["source"]["tree"] == expected["tree"],
        f"{name} tree",
    )
    require(
        item["build"]["artifact_sha256"] == expected["artifact"],
        f"{name} artifact",
    )
    require(item["build"]["status"] == "PASS", f"{name} build status")

    evidence = item["build"]["persistent_evidence"]

    for path_key, sha_key in [
        ("configure_log_path", "configure_log_sha256"),
        ("build_log_path", "build_log_sha256"),
        ("build_metadata_path", "build_metadata_sha256"),
    ]:
        path = ROOT / evidence[path_key]
        require(path.is_file(), f"{name} evidence missing: {path_key}")
        require(
            digest(path) == evidence[sha_key],
            f"{name} evidence SHA: {path_key}",
        )

stage = lock["stage_boundaries"]
require(stage["library_specific_protocol_rules_created"] is False, "rules")
require(stage["scenario_bindings_created"] == 0, "scenario bindings")
require(stage["primary_generation_authorized"] is False, "generation")
require(stage["held_out_driver_inspection_allowed"] is False, "inspection")
require(stage["analyzer_implementation_authorized_by_gate1c"] is False, "analyzer")
require(stage["repair_implementation_allowed"] is False, "repair")
require(stage["repair_activation_gate"] == "Gate V", "repair gate")

lock_sha = digest(LOCK)
report_sha = digest(REPORT)

require(report["status"] == "PASS", "report status")
require(report["lock_sha256"] == lock_sha, "report lock SHA")
require(report["library_count"] == 8, "report library count")
require(report["source_identity_pass"] == 8, "report source count")
require(report["build_qualification_pass"] == 8, "report build pass")
require(report["build_qualification_fail"] == 0, "report build fail")

gate1 = research["gate1_foundation"]
gate1c = gate1["gate1c_source_build_lock"]

require(gate1["status"] == "IN_PROGRESS", "Gate 1 status")
require(gate1c["status"] == "PASS", "Gate 1C status")
require(gate1c["lock_sha256"] == lock_sha, "research lock SHA")
require(gate1c["report_sha256"] == report_sha, "research report SHA")
require(gate1c["build_qualification_pass"] == 8, "research build pass")

require(gate1["primary_generation_authorized"] is False, "research generation")
require(gate1["held_out_driver_inspection_allowed"] is False, "research inspection")
require(gate1["analyzer_implementation_authorized"] is False, "research analyzer")
require(gate1["repair_implementation_allowed"] is False, "research repair")

require(
    research["current_status"]["gate_1c_source_build_lock"] == "PASS",
    "current status",
)

print("GATE1C_SOURCE_BUILD_LOCK=PASS")
print("SOURCE_IDENTITIES=8_OF_8_PASS")
print("BUILD_QUALIFICATION=8_OF_8_PASS")
print("FINAL_CURL_RECIPE=V3_DEPENDENCY_STABLE")
print("FINAL_LCMS_RECIPE=V3_DEPENDENCY_STABLE")
print("LIBPCAP_FLEX_BISON_PINNED=YES")
print("LIBVPX_NASM_PINNED=YES")
print("PRIMARY_GENERATION_AUTHORIZED=NO")
print("HELD_OUT_DRIVER_INSPECTION_ALLOWED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"LOCK_SHA256={lock_sha}")
print(f"REPORT_SHA256={report_sha}")
'''

write_new(VERIFIER_REL, verifier, executable=True)

print("GATE1C_SOURCE_BUILD_PREPARATION=PASS")
print("SOURCE_IDENTITIES=8")
print("BUILD_QUALIFIED=8")
print("FINAL_BUILD_SET=8_OF_8_PASS")
print("PERSISTENT_FINAL_LOG_PAIRS=8")
print("FAILED_V1_LOGS_PRESERVED=2")
print("PRIMARY_GENERATION_AUTHORIZED=NO")
print("HELD_OUT_DRIVER_INSPECTION_ALLOWED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"LOCK_SHA256={lock_sha}")
print(f"REPORT_SHA256={report_sha}")
