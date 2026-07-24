"""Replace the Agon hardware SD-card deployment with the local tgt tree."""

import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_TGT = (PROJECT_ROOT / "tgt").resolve()
SD_MOUNT = Path("/media/smith/AGON")
DEPLOY_ROOT = SD_MOUNT / "mystuff/AgonWolf3D"
EXPECTED_DEPLOY_ROOT = Path("/media/smith/AGON/mystuff/AgonWolf3D")


def deploy_to_sd():
    if not SD_MOUNT.is_mount():
        raise SystemExit(f"Agon SD card is not mounted at {SD_MOUNT}")
    if not SOURCE_TGT.is_dir():
        raise SystemExit(f"Build target directory is missing: {SOURCE_TGT}")

    deploy_root = DEPLOY_ROOT.resolve()
    if deploy_root != EXPECTED_DEPLOY_ROOT:
        raise SystemExit(f"Refusing unexpected deployment path: {deploy_root}")
    if deploy_root.is_symlink():
        raise SystemExit(f"Refusing symlinked deployment path: {deploy_root}")

    deploy_root.mkdir(parents=True, exist_ok=True)
    destination = deploy_root / "tgt"
    if destination.is_symlink():
        raise SystemExit(f"Refusing symlinked deployment target: {destination}")
    if destination.exists():
        if not destination.is_dir():
            raise SystemExit(
                f"Refusing non-directory deployment target: {destination}"
            )
        shutil.rmtree(destination)

    shutil.copytree(SOURCE_TGT, destination)
    print(f"Deployed {SOURCE_TGT} to {destination}")


if __name__ == "__main__":
    deploy_to_sd()
