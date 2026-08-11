#!/usr/bin/env python3

import argparse
import copy
import hashlib
import json
from pathlib import Path


def canonical_json_bytes(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(
        Path(path).read_bytes()
    )


def hash_object_without_own_content_sha256(value):
    if not isinstance(value, dict):
        raise TypeError("hash target must be a JSON object")

    working = copy.deepcopy(value)
    working.pop("content_sha256", None)

    return sha256_bytes(
        canonical_json_bytes(working)
    )


def obligation_content_sha256(obligation):
    return hash_object_without_own_content_sha256(
        obligation
    )


def specification_content_sha256(specification):
    return hash_object_without_own_content_sha256(
        specification
    )


def verify_obligation(obligation):
    expected = obligation.get(
        "content_sha256"
    )

    if not isinstance(expected, str):
        return False

    return expected == obligation_content_sha256(
        obligation
    )


def verify_specification(specification):
    expected = specification.get(
        "content_sha256"
    )

    if not isinstance(expected, str):
        return False

    return expected == specification_content_sha256(
        specification
    )


def self_test():
    # Key-order invariance.
    a = {
        "b": 2,
        "a": 1,
    }

    b = {
        "a": 1,
        "b": 2,
    }

    assert canonical_json_bytes(a) == canonical_json_bytes(b)

    # Own content_sha256 does not participate in an object's hash.
    o1 = {
        "rule_id": "R1",
        "resource_kind": "demo",
        "content_sha256": "0" * 64,
    }

    o2 = {
        "content_sha256": "f" * 64,
        "resource_kind": "demo",
        "rule_id": "R1",
    }

    assert (
        obligation_content_sha256(o1)
        ==
        obligation_content_sha256(o2)
    )

    # Semantic mutation must change hash.
    o3 = dict(o2)
    o3["resource_kind"] = "changed"

    assert (
        obligation_content_sha256(o1)
        !=
        obligation_content_sha256(o3)
    )

    # Top-level specification retains nested obligation hash values.
    s1 = {
        "specification_id": "demo",
        "obligations": [
            {
                "rule_id": "R1",
                "content_sha256": "1" * 64,
            }
        ],
        "content_sha256": "0" * 64,
    }

    s2 = copy.deepcopy(s1)
    s2["content_sha256"] = "f" * 64

    assert (
        specification_content_sha256(s1)
        ==
        specification_content_sha256(s2)
    )

    s3 = copy.deepcopy(s1)
    s3["obligations"][0]["content_sha256"] = "2" * 64

    assert (
        specification_content_sha256(s1)
        !=
        specification_content_sha256(s3)
    )

    print("PROTOCOL_CONTENT_HASH_SELF_TEST=PASS")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--self-test",
        action="store_true",
    )

    parser.add_argument(
        "--hash-source-file",
    )

    parser.add_argument(
        "--hash-obligation-json",
    )

    parser.add_argument(
        "--hash-specification-json",
    )

    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    if args.hash_source_file:
        print(
            sha256_file(
                args.hash_source_file
            )
        )
        return

    if args.hash_obligation_json:
        value = json.loads(
            Path(
                args.hash_obligation_json
            ).read_text(
                encoding="utf-8"
            )
        )

        print(
            obligation_content_sha256(
                value
            )
        )
        return

    if args.hash_specification_json:
        value = json.loads(
            Path(
                args.hash_specification_json
            ).read_text(
                encoding="utf-8"
            )
        )

        print(
            specification_content_sha256(
                value
            )
        )
        return

    parser.error(
        "select one operation"
    )


if __name__ == "__main__":
    main()
