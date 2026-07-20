#!/usr/bin/env python3
"""Deploy the generated target directory to the Agon Light SD card."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = PROJECT_ROOT / "tgt"
SD_CARD_ROOT = Path("/media/smith/AGON")
DESTINATION_DIR = SD_CARD_ROOT / "mystuff" / "AgonWolf3D" / "tgt"


def copy_with_progress(source: str, destination: str) -> str:
    relative_source = Path(source).relative_to(PROJECT_ROOT)
    print(f"\r\033[Kcopying {relative_source}", end="", flush=True)
    return shutil.copy2(source, destination)


def deploy(*, dry_run: bool = False) -> None:
    if not SOURCE_DIR.is_dir():
        raise SystemExit(f"Build target directory does not exist: {SOURCE_DIR}")

    if not os.path.ismount(SD_CARD_ROOT):
        raise SystemExit(
            f"AGON SD card is not mounted at {SD_CARD_ROOT}. "
            "Insert or mount the card before deploying."
        )

    if os.statvfs(SD_CARD_ROOT).f_flag & os.ST_RDONLY:
        raise SystemExit(
            f"AGON SD card is mounted read-only at {SD_CARD_ROOT}. "
            "Repair or remount the card read-write before deploying."
        )

    source_files = [path for path in SOURCE_DIR.rglob("*") if path.is_file()]
    print(f"Source:      {SOURCE_DIR}")
    print(f"Destination: {DESTINATION_DIR}")
    print(f"Files:       {len(source_files)}")
    print("Mode:        clean replacement")

    if dry_run:
        print("Dry run: destination not deleted and no files copied.")
        return

    if DESTINATION_DIR.is_symlink():
        raise SystemExit(f"Refusing to replace symlink: {DESTINATION_DIR}")

    if DESTINATION_DIR.exists():
        if not DESTINATION_DIR.is_dir():
            raise SystemExit(f"Destination exists but is not a directory: {DESTINATION_DIR}")
        print(f"Deleting:    {DESTINATION_DIR}")
        shutil.rmtree(DESTINATION_DIR)

    print(f"Copying:     {SOURCE_DIR} -> {DESTINATION_DIR}")
    shutil.copytree(SOURCE_DIR, DESTINATION_DIR, copy_function=copy_with_progress)
    print("\r\033[KDeployment complete.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Copy the project's tgt directory to the Agon Light SD card."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show the resolved paths and file count without copying",
    )
    args = parser.parse_args()
    deploy(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
