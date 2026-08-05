#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update

apt-get install -y --no-install-recommends \
  'clang-14=1:14.0.0-1ubuntu1.1' \
  'clang-tools-14=1:14.0.0-1ubuntu1.1' \
  'llvm-14-dev=1:14.0.0-1ubuntu1.1' \
  'libclang-14-dev=1:14.0.0-1ubuntu1.1' \
  'lld-14=1:14.0.0-1ubuntu1.1' \
  'ninja-build=1.10.1-1' \
  'pkg-config=0.29.2-1ubuntu3'

printf 'GATE0B_TOOLCHAIN_INSTALL=PASS\n'
