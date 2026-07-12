#!/usr/bin/env python3
"""Command wrapper for Vardheim release readiness validation."""

import sys

from release_validation import readiness_main


if __name__ == "__main__":
    raise SystemExit(readiness_main(sys.argv[1:]))
