#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def git_oid(kind, raw):
    return hashlib.sha1(
        f"{kind} {len(raw)}\0".encode() + raw
    ).hexdigest()

def parse_tree(raw):
    result = {}
    i = 0

    while i < len(raw):
        sp = raw.index(b" ", i)
        mode = raw[i:sp].decode()

        nul = raw.index(b"\0", sp + 1)
        name = raw[sp + 1:nul].decode()

        oid = raw[nul + 1:nul + 21].hex()

        result[name] = {
            "mode": mode,
            "oid": oid,
        }

        i = nul + 21

    return result

here = Path(__file__).resolve().parent
index = json.loads(
    (here / "00_git_proof_index.v1.json")
    .read_text(encoding="utf-8")
)

z_expected_sha = index["zlib_expected_sha256"]
z_expected_blob = index["zlib_expected_blob"]

p_expected_sha = index["libpcap_expected_sha256"]
p_expected_blob = index["libpcap_expected_blob"]

z_seen = []
p_seen = []

for entry in index["checkpoints"]:
    d = here / entry["directory"]

    m = json.loads(
        (d / "13_checkpoint_object_manifest.v1.json")
        .read_text(encoding="utf-8")
    )

    commit_raw = (d / "01_checkpoint_commit.raw").read_bytes()

    if git_oid("commit", commit_raw) != m["commit"]:
        fail("CHECKPOINT_COMMIT_OID|" + m["label"])

    first_line = commit_raw.decode(
        "utf-8",
        errors="strict"
    ).splitlines()[0]

    if first_line != "tree " + m["root_tree"]:
        fail("CHECKPOINT_COMMIT_TREE|" + m["label"])

    parent_lines = [
        line.split(" ", 1)[1]
        for line in commit_raw.decode(
            "utf-8",
            errors="strict"
        ).splitlines()
        if line.startswith("parent ")
    ]

    if parent_lines != [m["parent"]]:
        fail("CHECKPOINT_PARENT|" + m["label"])

    root_raw = (d / "02_checkpoint_root_tree.raw").read_bytes()
    config_raw = (d / "03_checkpoint_config_tree.raw").read_bytes()
    protocol_raw = (
        d / "04_checkpoint_protocol_specifications_tree.raw"
    ).read_bytes()

    if git_oid("tree", root_raw) != m["root_tree"]:
        fail("CHECKPOINT_ROOT_TREE_OID|" + m["label"])

    if git_oid("tree", config_raw) != m["config_tree"]:
        fail("CHECKPOINT_CONFIG_TREE_OID|" + m["label"])

    if git_oid("tree", protocol_raw) != \
       m["protocol_specifications_tree"]:
        fail("CHECKPOINT_PROTOCOL_TREE_OID|" + m["label"])

    root = parse_tree(root_raw)
    config = parse_tree(config_raw)
    protocol = parse_tree(protocol_raw)

    if root.get("config", {}).get("oid") != m["config_tree"]:
        fail("ROOT_CONFIG_BINDING|" + m["label"])

    if config.get(
        "protocol_specifications",
        {}
    ).get("oid") != m["protocol_specifications_tree"]:
        fail("CONFIG_PROTOCOL_BINDING|" + m["label"])

    if m["zlib"] is not None:
        raw = (d / "05_checkpoint_zlib_blob.raw").read_bytes()

        if git_oid("blob", raw) != m["zlib"]["blob"]:
            fail("CHECKPOINT_ZLIB_BLOB_OID|" + m["label"])

        if protocol.get("zlib.json", {}).get("oid") != \
           m["zlib"]["blob"]:
            fail("CHECKPOINT_ZLIB_TREE_BINDING|" + m["label"])

        if hashlib.sha256(raw).hexdigest() != \
           m["zlib"]["sha256"]:
            fail("CHECKPOINT_ZLIB_SHA|" + m["label"])

        if m["zlib"]["sha256"] == z_expected_sha:
            z_seen.append(m["zlib"]["blob"])

    if m["libpcap"] is not None:
        raw = (d / "06_checkpoint_libpcap_blob.raw").read_bytes()

        if git_oid("blob", raw) != m["libpcap"]["blob"]:
            fail("CHECKPOINT_LIBPCAP_BLOB_OID|" + m["label"])

        if protocol.get("libpcap.json", {}).get("oid") != \
           m["libpcap"]["blob"]:
            fail("CHECKPOINT_LIBPCAP_TREE_BINDING|" + m["label"])

        if hashlib.sha256(raw).hexdigest() != \
           m["libpcap"]["sha256"]:
            fail("CHECKPOINT_LIBPCAP_SHA|" + m["label"])

        if m["libpcap"]["sha256"] == p_expected_sha:
            p_seen.append(m["libpcap"]["blob"])

    parent_raw = (d / "07_parent_commit.raw").read_bytes()

    if git_oid("commit", parent_raw) != m["parent"]:
        fail("PARENT_COMMIT_OID|" + m["label"])

    parent_first = parent_raw.decode(
        "utf-8",
        errors="strict"
    ).splitlines()[0]

    if parent_first != "tree " + m["parent_root_tree"]:
        fail("PARENT_COMMIT_TREE|" + m["label"])

    parent_root_raw = (
        d / "08_parent_root_tree.raw"
    ).read_bytes()

    if git_oid("tree", parent_root_raw) != m["parent_root_tree"]:
        fail("PARENT_ROOT_OID|" + m["label"])

    parent_root = parse_tree(parent_root_raw)

    if m["parent_config_tree"] is not None:
        pcfg_raw = (
            d / "09_parent_config_tree.raw"
        ).read_bytes()

        if git_oid("tree", pcfg_raw) != m["parent_config_tree"]:
            fail("PARENT_CONFIG_OID|" + m["label"])

        if parent_root.get("config", {}).get("oid") != \
           m["parent_config_tree"]:
            fail("PARENT_ROOT_CONFIG_BINDING|" + m["label"])

        pcfg = parse_tree(pcfg_raw)

        if m["parent_protocol_specifications_tree"] is not None:
            pproto_raw = (
                d / "10_parent_protocol_specifications_tree.raw"
            ).read_bytes()

            if git_oid("tree", pproto_raw) != \
               m["parent_protocol_specifications_tree"]:
                fail("PARENT_PROTOCOL_OID|" + m["label"])

            if pcfg.get(
                "protocol_specifications",
                {}
            ).get("oid") != \
               m["parent_protocol_specifications_tree"]:
                fail("PARENT_CONFIG_PROTOCOL_BINDING|" + m["label"])

            pproto = parse_tree(pproto_raw)

            if m["parent_zlib"] is not None:
                raw = (
                    d / "11_parent_zlib_blob.raw"
                ).read_bytes()

                if git_oid("blob", raw) != \
                   m["parent_zlib"]["blob"]:
                    fail("PARENT_ZLIB_OID|" + m["label"])

                if pproto.get("zlib.json", {}).get("oid") != \
                   m["parent_zlib"]["blob"]:
                    fail("PARENT_ZLIB_TREE_BINDING|" + m["label"])

                if hashlib.sha256(raw).hexdigest() != \
                   m["parent_zlib"]["sha256"]:
                    fail("PARENT_ZLIB_SHA|" + m["label"])

            if m["parent_libpcap"] is not None:
                raw = (
                    d / "12_parent_libpcap_blob.raw"
                ).read_bytes()

                if git_oid("blob", raw) != \
                   m["parent_libpcap"]["blob"]:
                    fail("PARENT_LIBPCAP_OID|" + m["label"])

                if pproto.get("libpcap.json", {}).get("oid") != \
                   m["parent_libpcap"]["blob"]:
                    fail("PARENT_LIBPCAP_TREE_BINDING|" + m["label"])

                if hashlib.sha256(raw).hexdigest() != \
                   m["parent_libpcap"]["sha256"]:
                    fail("PARENT_LIBPCAP_SHA|" + m["label"])

if not z_seen:
    fail("NO_ZLIB_FROZEN_CHECKPOINTS")

if set(z_seen) != {z_expected_blob}:
    fail("ZLIB_BLOB_IDENTITY")

if not p_seen:
    fail("NO_LIBPCAP_FROZEN_CHECKPOINTS")

if set(p_seen) != {p_expected_blob}:
    fail("LIBPCAP_BLOB_IDENTITY")

print("PORTABLE_CHECKPOINT_COMMIT_OBJECTS=PASS")
print("PORTABLE_PARENT_COMMIT_OBJECTS=PASS")
print("PORTABLE_ROOT_CONFIG_PROTOCOL_TREE_BINDINGS=PASS")
print("PORTABLE_ZLIB_TREE_TO_BLOB_BINDINGS=PASS")
print("PORTABLE_LIBPCAP_TREE_TO_BLOB_BINDINGS=PASS")
print("ZLIB_BASELINE_TO_LATER_GIT_BLOB_IDENTITY=PASS")
print("LIBPCAP_BASELINE_TO_LATER_GIT_BLOB_IDENTITY=PASS")
print("PARENT_CHECKPOINT_IMMUTABILITY_EVIDENCE=PASS")
print("PORTABLE_ZLIB_LIBPCAP_PREPOST_GIT_PROOF=PASS")
