#!/usr/bin/env python3
"""Publish Vardheim workspace crates in validated crates.io dependency order."""

from __future__ import annotations

import argparse
import builtins
import json
import re
import subprocess
import sys
import time
from pathlib import Path

from release_validation import ValidationError, validate_readiness

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - release-host guard.
    print("Python 3.11+ is required because this script uses tomllib.", file=sys.stderr)
    raise


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "release-crates.toml"
CHANGE_KINDS = ("code", "dependency", "metadata", "unchanged")
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?$")

PUBLISH_ORDER = (
    "vardheim-core",
    "vardheim-challenge-http",
    "vardheim-challenge-dns",
    "vardheim-challenge-tls",
    "vardheim",
)


def run(command: list[str], *, dry_run: bool) -> None:
    print(f"+ {' '.join(command)}", flush=True)
    if not dry_run:
        subprocess.run(command, cwd=ROOT, check=True)


def capture(command: list[str]) -> str:
    return subprocess.check_output(command, cwd=ROOT, text=True).strip()


def try_capture(command: list[str]) -> str | None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def parse_version(version: str) -> tuple[int, int, int]:
    if SEMVER.fullmatch(version) is None:
        raise RuntimeError(f"version must be SemVer MAJOR.MINOR.PATCH: {version}")
    core = version.split("-", maxsplit=1)[0]
    major, minor, patch = (int(part) for part in core.split("."))
    return (major, minor, patch)


def cargo_metadata() -> dict:
    raw = capture(["cargo", "metadata", "--format-version", "1", "--no-deps"])
    return json.loads(raw)


def workspace_packages(metadata: dict) -> dict[str, dict]:
    workspace_ids = set(metadata["workspace_members"])
    return {
        package["name"]: package
        for package in metadata["packages"]
        if package["id"] in workspace_ids
    }


def validate_plan_entry(package_name: str, entry: dict, release: str) -> None:
    previous = entry.get("previous_version")
    version = entry.get("version")
    change = entry.get("change")
    publish = entry.get("publish")
    reason = entry.get("reason")
    strings = (previous, version, change, reason)
    if not all(isinstance(value, str) and value for value in strings):
        raise RuntimeError(f"{package_name} has incomplete release plan metadata")
    if change not in CHANGE_KINDS:
        raise RuntimeError(f"{package_name} has invalid change kind {change!r}")
    if not isinstance(publish, bool):
        raise RuntimeError(f"{package_name} publish must be true or false")

    previous_parts = parse_version(previous)
    planned_parts = parse_version(version)
    parse_version(release)

    if package_name == "vardheim":
        if version != release:
            raise RuntimeError(
                f"vardheim must always match the release/tag version {release}"
            )
        if not publish:
            raise RuntimeError("vardheim must be published for every release tag")

    if change == "code":
        if package_name == "vardheim":
            pass
        else:
            expected = (previous_parts[0], previous_parts[1] + 1, 0)
            if planned_parts != expected or "-" in version:
                dotted = ".".join(str(part) for part in expected)
                raise RuntimeError(
                    f"{package_name} has code changes, so independent support-crate "
                    f"version must be {dotted}"
                )
        if not publish:
            raise RuntimeError(f"{package_name} has code changes but publish is false")
    elif change == "metadata":
        if version != release or not publish:
            raise RuntimeError(
                f"{package_name} metadata changes must use {release} and publish"
            )
    elif change == "dependency":
        same_line = planned_parts[:2] == previous_parts[:2]
        patch_bump = planned_parts[2] > previous_parts[2]
        if not same_line or not patch_bump or "-" in version:
            raise RuntimeError(
                f"{package_name} dependency-only changes require a patch bump"
            )
        if not publish:
            raise RuntimeError(
                f"{package_name} has dependency-only changes but publish is false"
            )
    else:
        if version != previous:
            raise RuntimeError(
                f"{package_name} is unchanged but version differs from previous_version"
            )
        if publish:
            raise RuntimeError(f"{package_name} is unchanged but publish is true")


def release_plan(plan_path: Path) -> dict:
    plan = load_toml(plan_path)
    release = plan.get("release", {})
    crates = plan.get("crates", {})
    version = release.get("version")
    if not isinstance(version, str):
        raise RuntimeError("release-crates.toml is missing [release].version")
    parse_version(version)
    if set(crates) != set(PUBLISH_ORDER):
        raise RuntimeError(
            "release-crates.toml crates differ from PUBLISH_ORDER: "
            f"expected {tuple(sorted(PUBLISH_ORDER))}, actual {tuple(sorted(crates))}"
        )
    for package_name, entry in crates.items():
        validate_plan_entry(package_name, entry, version)
    return {"version": version, "crates": crates}


def verify_publish_order(packages: dict[str, dict], plan: dict) -> None:
    if set(packages) != set(PUBLISH_ORDER):
        raise RuntimeError(
            "PUBLISH_ORDER differs from workspace packages: "
            f"expected {tuple(sorted(PUBLISH_ORDER))}, "
            f"actual {tuple(sorted(packages))}"
        )

    seen: set[str] = set()
    for package_name in PUBLISH_ORDER:
        package = packages[package_name]
        planned_version = plan["crates"][package_name]["version"]
        if package["version"] != planned_version:
            raise RuntimeError(
                f"{package_name} is {package['version']}, expected {planned_version}"
            )
        for dependency in package["dependencies"]:
            dependency_name = dependency["name"]
            if dependency_name in packages and dependency_name not in seen:
                raise RuntimeError(
                    f"{package_name} depends on {dependency_name}, but "
                    f"{dependency_name} appears later in PUBLISH_ORDER"
                )
        seen.add(package_name)


def publish_plan(plan: dict) -> tuple[str, ...]:
    return tuple(
        package for package in PUBLISH_ORDER if plan["crates"][package]["publish"]
    )


def selected_steps(start_at: str | None, steps: tuple[str, ...]) -> tuple[str, ...]:
    if start_at is None:
        return steps
    try:
        return steps[steps.index(start_at) :]
    except ValueError as exc:
        raise RuntimeError(
            f"--start-at package is not selected for this release: {start_at}"
        ) from exc


def require_clean_tagged_tree(version: str) -> None:
    status = capture(["git", "status", "--porcelain"])
    if status:
        raise RuntimeError("refusing to publish from a dirty worktree")
    head = capture(["git", "rev-parse", "HEAD"])
    tag = f"v{version}"
    tagged_commit = try_capture(["git", "rev-list", "-n", "1", tag])
    if tagged_commit != head:
        raise RuntimeError(f"refusing to publish: {tag} does not point at HEAD")
    try:
        validate_readiness(tag, require_tag_absent=False)
    except ValidationError as error:
        raise RuntimeError(f"refusing to publish: {error}") from error


def run_preflight(*, dry_run: bool) -> None:
    run(["scripts/checks.sh"], dry_run=dry_run)
    run(["cargo", "deny", "check"], dry_run=dry_run)
    run(["cargo", "audit"], dry_run=dry_run)


def publish(package: str, *, dry_run: bool) -> None:
    run(["cargo", "publish", "-p", package], dry_run=dry_run)


def require_interactive_multi_publish(
    steps: tuple[str, ...],
    *,
    dry_run: bool,
    stdin=None,
) -> None:
    stream = sys.stdin if stdin is None else stdin
    if not dry_run and len(steps) > 1 and not stream.isatty():
        raise RuntimeError(
            "refusing unattended multi-package publish: stdin is not a TTY"
        )


def read_confirmation(prompt: str) -> str:
    try:
        return builtins.input(prompt).strip()
    except EOFError as error:
        raise RuntimeError("stdin closed; refusing to continue publishing") from error


def wait_for_index(package: str, version: str, *, dry_run: bool) -> None:
    print(f"Published {package} {version}.")
    print(f"Confirm https://crates.io/crates/{package}/{version} before continuing.")
    if dry_run:
        print("[dry-run] skipping registry wait")
        return
    read_confirmation("Press Enter after crates.io resolves this version: ")
    time.sleep(5)


def publish_steps(steps: tuple[str, ...], plan: dict, args: argparse.Namespace) -> None:
    for index, package in enumerate(steps):
        if not args.dry_run:
            require_clean_tagged_tree(args.version)
        publish(package, dry_run=args.dry_run)
        if index != len(steps) - 1:
            wait_for_index(
                package,
                plan["crates"][package]["version"],
                dry_run=args.dry_run,
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Publish Vardheim workspace crates in dependency order."
    )
    parser.add_argument("--plan", default=str(DEFAULT_PLAN))
    parser.add_argument("--version", default=None)
    parser.add_argument("--start-at", choices=PUBLISH_ORDER)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()

    raw_plan_path = Path(args.plan)
    plan_path = raw_plan_path if raw_plan_path.is_absolute() else ROOT / raw_plan_path
    plan = release_plan(plan_path.resolve())
    if args.version is not None and args.version != plan["version"]:
        print(
            f"Refusing: --version {args.version} differs from plan {plan['version']}.",
            file=sys.stderr,
        )
        return 1
    args.version = plan["version"]

    verify_publish_order(workspace_packages(cargo_metadata()), plan)
    if args.check:
        print("release_crates.py publish order and versions are valid.")
        print(f"release_crates.py release plan is {args.version}.")
        return 0

    if not args.dry_run:
        require_clean_tagged_tree(args.version)

    steps = selected_steps(args.start_at, publish_plan(plan))
    require_interactive_multi_publish(steps, dry_run=args.dry_run)
    print(f"Release version: {args.version}")
    print("Publish sequence:")
    for package in steps:
        print(f"  - {package} {plan['crates'][package]['version']}")

    if not args.yes:
        answer = read_confirmation("Type the release version to continue: ")
        if answer != args.version:
            print("Version confirmation did not match; aborting.", file=sys.stderr)
            return 1

    run_preflight(dry_run=args.dry_run)
    publish_steps(steps, plan, args)

    print("Release publish sequence completed.")
    print(f"Verify with: cargo info vardheim@{args.version}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"Release refused: {error}", file=sys.stderr)
        raise SystemExit(1) from None
