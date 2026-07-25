#!/usr/bin/env python3
"""Create one project-local Fab Agon emulator profile for MapMaker."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


MAPMAKER_ROOT = Path(__file__).resolve().parent
DEFAULT_EMULATOR_SOURCE = Path.home() / "Agon" / "fab-agon-emulator"
# Keep the profile outside MAPMAKER_ROOT so its SD-card link can safely expose
# the complete working directory without recursively exposing the profile.
DEFAULT_PROFILE = MAPMAKER_ROOT.parent / ".emulator" / "mapmaker"


def replace_symlink(link: Path, target: Path) -> None:
    """Create a relative symlink, replacing only an existing symlink."""
    if link.is_symlink():
        link.unlink()
    elif link.exists():
        raise SystemExit(f"Refusing to replace non-symlink path: {link}")

    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(os.path.relpath(target, link.parent))


def setup_emulator(emulator_source: Path, profile: Path) -> None:
    emulator_source = emulator_source.resolve()
    profile = profile.resolve()
    if profile.is_relative_to(MAPMAKER_ROOT):
        raise SystemExit(
            "The emulator profile must remain outside src/mapmaker to avoid "
            "a recursive SD-card link"
        )

    executable = emulator_source / "fab-agon-emulator"
    firmware = emulator_source / "firmware"
    shared_sdcard = emulator_source / "sdcard"
    required_paths = (
        executable,
        firmware,
        shared_sdcard / "bin",
        shared_sdcard / "mos",
        shared_sdcard / "firmware.bin",
        shared_sdcard / "MOS.bin",
        shared_sdcard / "bin" / "bbcbasic.bin",
        MAPMAKER_ROOT / "mapmaker.bas",
    )
    missing = [path for path in required_paths if not path.exists()]
    if missing:
        formatted = "\n".join(f"  {path}" for path in missing)
        raise SystemExit(f"Required emulator or MapMaker paths are missing:\n{formatted}")

    sdcard = profile / "sdcard"
    sdcard.mkdir(parents=True, exist_ok=True)

    replace_symlink(profile / "fab-agon-emulator", executable)
    replace_symlink(profile / "firmware", firmware)
    replace_symlink(sdcard / "bin", shared_sdcard / "bin")
    replace_symlink(sdcard / "mos", shared_sdcard / "mos")
    replace_symlink(sdcard / "firmware.bin", shared_sdcard / "firmware.bin")
    replace_symlink(sdcard / "MOS.bin", shared_sdcard / "MOS.bin")
    replace_symlink(sdcard / "mapmaker", MAPMAKER_ROOT)

    autoexec = (
        b"SET KEYBOARD 1\r\n"
        b"cd mapmaker\r\n"
        b"bbcbasic.bin\r\n"
        b"RUN . MAPMAKER.BBC\r\n"
    )
    (sdcard / "autoexec.txt").write_bytes(autoexec)

    print(f"Emulator profile: {profile}")
    print(f"MapMaker root:    {MAPMAKER_ROOT}")
    print(f"Autoexec:         {sdcard / 'autoexec.txt'}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Set up the project-local MapMaker emulator."
    )
    parser.add_argument(
        "--emulator-source",
        type=Path,
        default=DEFAULT_EMULATOR_SOURCE,
        help=f"Fab Agon emulator checkout (default: {DEFAULT_EMULATOR_SOURCE})",
    )
    parser.add_argument(
        "--profile",
        type=Path,
        default=DEFAULT_PROFILE,
        help=f"local emulator profile (default: {DEFAULT_PROFILE})",
    )
    args = parser.parse_args()
    setup_emulator(args.emulator_source, args.profile)


if __name__ == "__main__":
    main()
