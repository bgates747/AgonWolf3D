# Conversation Summary

## Project

AgonWolf3D is a 3D shoot 'em up for the Agon Light, built in homage to Wolfenstein 3D. The codebase is split into asset generation, map/build tooling, and the runtime assembly sources that target the eZ80/VDP platform.

The main build pipeline is driven by `build/scripts/build_00_all_the_things.py`, which stages the asset and code generation steps behind toggles. The later assembly step produces the final target artifacts, including the `tgt/` outputs and generated assembly include files under `src/asm/`.

## Environment Setup

### Python `.venv`

- Created a project-local virtual environment at `.venv` with Python 3.14.6.
- Reconfigured the workspace to use that interpreter.
- Scanned the Python scripts in `build/scripts` and `dev/scripts` for imports.
- Installed the needed packages into the venv:
  - `numpy`
  - `pandas`
  - `pillow`
  - `opencv-python`
  - `matplotlib`
  - `pygame-ce`
- Noted that `bpy` and `bmesh` come from Blender's Python runtime rather than normal pip installs.

### `ez80asm`

- Built ez80asm from source on Linux in `~/Agon/agon-ez80asm` with `make linux`.
- Copied the resulting binary to `~/.local/bin/ez80asm` so it is on `PATH`.
- Verified that the build pipeline's final assembly step works once `ez80asm` is available.

### `fab-agon-emulator`

- Followed the emulator's Linux compile guide in `docs/compiling.md`.
- Ran `git submodule update --init` so the firmware and VDP pieces were available.
- Built the emulator and its VDP shared objects.
- Set up the runtime so the emulator can be launched directly from the shell with `fab-agon-emulator`.
- Created a global launcher in `~/.local/bin` so the command is available on `PATH`.

The main takeaway from the emulator work was that the local SDL/audio/video dependencies had to be built and wired correctly before the emulator would start cleanly.