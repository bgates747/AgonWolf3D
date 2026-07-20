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

## VS Code Assembly Language Support

Zaets and Alex Parker's EZ80 Assembly extension were evaluated, including a
temporary and non-durable attempt to combine features from both. They were
subsequently uninstalled in favor of Maziac's ASM Code Lens 2.6.13, which had
been used successfully with this project in the past.

The workspace assigns both `.asm` and `.inc` files to ASM Code Lens' native
`asm-collection` language ID:

```json
"files.associations": {
    "*.asm": "asm-collection",
    "*.inc": "asm-collection"
}
```

ASM Code Lens scopes labels as `variable.parameter.label.asm`. The active VS
Code theme rendered that scope orange, so the workspace adds a TextMate color
override of `#DCDCAA` (light yellow) to restore the familiar label appearance.
Mnemonic scopes are similarly overridden to `#569CD6` (medium blue), while
register coloring remains controlled by the active theme.

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

## Local Agon Documentation Checkout

The official `AgonPlatform/agon-docs` repository was cloned for local access
while developing against current MOS and VDP behavior:

```text
~/Agon/agon-docs
```

The checkout was on branch `main` at commit `f9806bd` when cloned. A
machine-local symlink exposes it from the project root:

```text
AgonWolf3D/agon-docs -> ~/Agon/agon-docs
```

The root-level `agon-docs` link is ignored by Git. This keeps the external
repository out of AgonWolf3D version control while making its documentation
directly available in the project workspace.

The existing AgonVideo project was temporarily exposed through a machine-local
project-root symlink for reference during file-handling work:

```text
AgonWolf3D/AgonVideo -> ~/Projects/AgonVideo
```

The link was removed later in the session to reduce project-root clutter. The
external repository at `~/Projects/AgonVideo` was not changed.

The `bgates747/nurples` game repository was cloned as another implementation
reference. It was on branch `main` at commit `2032953` when cloned:

```text
~/Agon/nurples
AgonWolf3D/nurples -> ~/Agon/nurples
```

The project-root link was removed later in the session to reduce clutter. The
external checkout at `~/Agon/nurples` remains independently versioned and was
not changed.

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

- `.gitignore` — ignored the local `.emulator/` directory and `agon-docs` link.
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
- `agon-docs` — linked the project root to the external Agon documentation checkout.
- `~/Agon/fab-agon-emulator/sdcard/autoexec.txt` — set emulator startup commands with CRLF endings.
- `~/Agon/fab-agon-emulator/sdcard/mystuff` — linked the emulator SD card to `~/Agon/mystuff`.
- `~/Agon/agon-docs/` — cloned the official Agon platform documentation repository.
- `~/Agon/nurples/` — cloned the Nurples game repository for implementation reference.
- `~/.local/bin/ez80asm` — installed the locally built assembler on `PATH`.
- `~/.local/bin/fab-agon-emulator` — installed the emulator launcher on `PATH`.
