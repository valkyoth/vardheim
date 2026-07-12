#!/usr/bin/env sh
set -eu

chmod a-w registry/iana-*.xml registry/SHA256SUMS
scripts/registry_baseline.py
