#!/usr/bin/env python3
"""Create an isolated, project-local Fab Agon emulator profile."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EMULATOR_SOURCE = Path.home() / "Agon" / "fab-agon-emulator"
DEFAULT_PROFILE = PROJECT_ROOT / ".emulator"

AUTOEXEC_BYTES = (
    b"SET KEYBOARD 1\r\n"
    b"cd mystuff/AgonWolf3D/tgt\r\n"
    b"load wolf3d.bin\r\n"
)


def replace_symlink(link: Path, target: Path) -> None:
    """Create a relative symlink, replacing only an existing link."""
    if link.is_symlink():
        link.unlink()
    elif link.exists():
        raise SystemExit(f"Refusing to replace non-symlink path: {link}")

    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(os.path.relpath(target, link.parent))


def replace_target_tree(source: Path, destination: Path) -> None:
    """Replace the profile's project target with a copy of the current target."""
    if destination.is_symlink():
        raise SystemExit(f"Refusing to replace symlinked target directory: {destination}")
    if destination.exists():
        if not destination.is_dir():
            raise SystemExit(f"Target destination is not a directory: {destination}")
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)


def setup_emulator(emulator_source: Path, profile: Path) -> None:
    emulator_source = emulator_source.resolve()
    profile = profile.resolve()

    executable = emulator_source / "fab-agon-emulator"
    firmware = emulator_source / "firmware"
    shared_sdcard = emulator_source / "sdcard"
    project_target = PROJECT_ROOT / "tgt"

    required_paths = (
        executable,
        firmware,
        shared_sdcard / "bin",
        shared_sdcard / "mos",
        shared_sdcard / "firmware.bin",
        shared_sdcard / "MOS.bin",
        project_target,
    )
    missing = [path for path in required_paths if not path.exists()]
    if missing:
        formatted = "\n".join(f"  {path}" for path in missing)
        raise SystemExit(f"Required emulator/project paths are missing:\n{formatted}")

    profile.mkdir(parents=True, exist_ok=True)
    sdcard = profile / "sdcard"
    sdcard.mkdir(parents=True, exist_ok=True)

    # Remove the previous shared-autoexec arrangement, if present. The isolated
    # profile owns only sdcard/autoexec.txt.
    legacy_autoexec = profile / "autoexec.txt"
    if legacy_autoexec.is_symlink():
        legacy_autoexec.unlink()
    elif legacy_autoexec.exists():
        raise SystemExit(f"Refusing to replace legacy non-symlink: {legacy_autoexec}")

    replace_symlink(profile / "fab-agon-emulator", executable)
    replace_symlink(profile / "firmware", firmware)
    replace_symlink(sdcard / "bin", shared_sdcard / "bin")
    replace_symlink(sdcard / "mos", shared_sdcard / "mos")
    replace_symlink(sdcard / "firmware.bin", shared_sdcard / "firmware.bin")
    replace_symlink(sdcard / "MOS.bin", shared_sdcard / "MOS.bin")

    autoexec_path = sdcard / "autoexec.txt"
    autoexec_path.write_bytes(AUTOEXEC_BYTES)

    emulator_target = sdcard / "mystuff" / "AgonWolf3D" / "tgt"
    replace_target_tree(project_target, emulator_target)

    print(f"Emulator profile: {profile}")
    print(f"Target copy:      {emulator_target}")
    print(f"Autoexec:         {autoexec_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Create an isolated Fab Agon emulator profile and copy this "
            "project's tgt directory into its local SD card."
        )
    )
    parser.add_argument(
        "--emulator-source",
        type=Path,
        default=DEFAULT_EMULATOR_SOURCE,
        help=f"shared Fab Agon emulator checkout (default: {DEFAULT_EMULATOR_SOURCE})",
    )
    parser.add_argument(
        "--profile",
        type=Path,
        default=DEFAULT_PROFILE,
        help=f"project-local emulator profile (default: {DEFAULT_PROFILE})",
    )
    args = parser.parse_args()
    setup_emulator(args.emulator_source, args.profile)


if __name__ == "__main__":
    main()
