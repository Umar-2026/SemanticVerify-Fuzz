#!/usr/bin/env python3

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
