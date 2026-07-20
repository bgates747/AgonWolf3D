# Environment Setup — 2026-07-20

## Objective

Re-establish a working AgonWolf3D development environment on Linux using the
current Python toolchain, assembler, emulator, MOS firmware, and VDP firmware.
The practical success criterion was an end-to-end build followed by successful
execution in both the emulator and on real Agon hardware.

## Python Environment

A project-local virtual environment was created at:

```text
AgonWolf3D/.venv
```

It uses Python 3.14.6. The Python scripts under `build/scripts` and
`dev/scripts` were scanned for their imports, and the following third-party
packages were installed:

- `numpy`
- `pandas`
- `pillow`
- `opencv-python`
- `matplotlib`
- `pygame-ce`

The workspace was configured to use the `.venv` interpreter.

The `bpy` and `bmesh` modules were not installed with `pip`; they are supplied
by Blender's own Python runtime and must be used by invoking Blender.

## eZ80 Assembler

`ez80asm` was built from source on Linux from:

```text
~/Agon/agon-ez80asm
```

The Linux build was produced with:

```bash
make linux
```

The resulting executable was copied to:

```text
~/.local/bin/ez80asm
```

This puts the assembler on `PATH` for the build scripts. The final assembly
stage of `build/scripts/build_00_all_the_things.py` completed successfully with
this assembler.

## Fab Agon Emulator

`fab-agon-emulator` was prepared from:

```text
~/Agon/fab-agon-emulator
```

Setup included:

- Following the Linux build instructions in `docs/compiling.md`.
- Initializing the repository's firmware and VDP submodules.
- Building the emulator and its VDP shared objects.
- Resolving the required SDL, audio, and video build/runtime dependencies.
- Installing a launcher at `~/.local/bin/fab-agon-emulator` so the emulator is
  available on `PATH`.

The emulator can now be launched from a shell with:

```bash
fab-agon-emulator
```

## Emulator Filesystem Integration

The emulator's host-backed SD-card directory is:

```text
~/Agon/fab-agon-emulator/sdcard
```

It contains this development convenience link:

```text
~/Agon/fab-agon-emulator/sdcard/mystuff -> ~/Agon/mystuff
```

This makes the project available to MOS inside the emulator at:

```text
mystuff/AgonWolf3D
```

The project deliberately does not link the complete emulator SD-card directory
back into the repository because that would create a recursive symlink path.
Instead, the project exposes only the emulator startup file:

```text
AgonWolf3D/.emulator/autoexec.txt
    -> ~/Agon/fab-agon-emulator/sdcard/autoexec.txt
```

`.emulator/` is ignored by Git. The workspace settings explicitly keep it
visible in the VS Code Explorer.

The emulator `autoexec.txt` uses CRLF line endings, as expected by the target
environment. VS Code is configured to detect and preserve its existing line
endings.

At the end of this session, its startup commands were:

```text
SET KEYBOARD 1
cd mystuff/AgonWolf3D/tgt
load wolf3d.bin
```

## End-to-End Validation

The complete build pipeline still works with the new environment. In
particular:

- Asset and code-generation stages run with Python 3.14.6 and the installed
  packages.
- The assembly stage produces the target artifacts under `tgt/`.
- The generated game runs successfully in `fab-agon-emulator`.
- The generated game also starts and runs on real Agon hardware after a clean
  SD-card deployment.
- No compatibility problem was observed with the current Python version,
  `ez80asm`, emulator, MOS firmware, or VDP firmware.

## Follow-up Observation

On real hardware, transferring/loading the game assets into the VDP is
noticeably slower than it was previously. A future session should compare the
game's current MOS file-access method with the newer or preferred MOS API. This
performance issue does not prevent the game from starting.

## Repository Files Changed

- `.gitignore` — explicitly ignored the project-local `.emulator/` directory.
- `build/data/build.db` — regenerated the build database during the full build.
- `build/panels/png/48_007.png` — regenerated panel image output.
- `build/scripts/build_00_all_the_things.py` — left only the final assembly stage enabled.
- `build/scripts/deploy_01_to_sd.py` — added clean deployment of `tgt/` to the hardware SD card.
- `conversation-summary.md` — recorded the initial project and environment handoff.
- `dev/session-notes/2026-07-20-environment-setup.md` — documented this environment setup session.
- `project-overview.md` — added a concise overview of the Agon platform architecture.
- `src/asm/wolf3d.lst` — regenerated the assembler listing with the current assembler.
- `tgt/panels/48_007.rgba2` — regenerated the target-format panel asset.

## Local Files Changed but Not Versioned

- `.emulator/autoexec.txt` — linked the project to the emulator SD-card startup file.
- `.vscode/settings.json` — kept `.emulator/` visible and preserved detected line endings.
- `.venv/` — created the project-local Python environment and installed dependencies.
- `~/Agon/fab-agon-emulator/sdcard/autoexec.txt` — set emulator startup commands with CRLF endings.
- `~/Agon/fab-agon-emulator/sdcard/mystuff` — linked the emulator SD card to `~/Agon/mystuff`.
- `~/.local/bin/ez80asm` — installed the locally built assembler on `PATH`.
- `~/.local/bin/fab-agon-emulator` — installed the emulator launcher on `PATH`.
