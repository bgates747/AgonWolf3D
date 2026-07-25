# AgonWolf3D Project Handoff

Read `/home/smith/Agon/mystuff/agon-dev-env/codex/AGENTS.md` first. This file
contains only AgonWolf3D-specific guidance.

## Project and current baseline

AgonWolf3D is an eZ80 assembly game with a Python asset-generation and
code-generation pipeline. `main` is the release branch. Release
`v0.2.0.alpha` is the first version in which all bitmap and sound assets load
from a small set of AGNB containers.

The master build driver is:

```text
build/scripts/build_00_all_the_things.py
```

Its second flag block is intentionally edited by commenting out unwanted
`True` assignments. Do not redesign that convention without the user's
agreement. For map-only changes, stages 06, 07, 91c, and 99 are the effective
dependency path.

Always invoke Python through `.venv/bin/python`. The environment uses the
editable canonical agon-utils checkout at
`/home/smith/Agon/mystuff/agon-utils`.

## Session-start reading

Read only what the task requires:

1. The latest file under `dev/session-notes`.
2. `docs/ez80_hacks.md` before assembly implementation.
3. `docs/current-image-loading-startup-trace.md` for startup/load changes.
4. `docs/wolf3d-image-build-and-agnb-integration-precis.md` for asset builds.
5. AGNB specifications and API précis for container work.

## Build and deployment

Full or selectively enabled build:

```bash
.venv/bin/python build/scripts/build_00_all_the_things.py
```

Assembly only:

```bash
ez80asm -l src/asm/wolf3d.asm tgt/wolf3d.bin
```

Hardware deployment:

```bash
.venv/bin/python build/scripts/deploy_01_to_sd.py
```

Emulator profiles are managed outside this repository:

```bash
cd /home/smith/Agon/mystuff/agon-dev-env
python3 scripts/setup_emulator.py wolf3d
scripts/run_emulator.sh wolf3d
```

## Application-specific conventions

- `wolf3d.asm` is the active application entry point.
- Keep reusable AGNB code application-neutral. Wolf3D progress animation,
  breadcrumbs, error presentation, and filenames belong outside the API.
- Use `printInline` for messages emitted from one distinct call site. Keep
  named strings when several callers share them.
- Generated `.lst` files and build-only RGBA2 payloads are not tracked.
- Preserve all current work and inspect the build database and generated
  targets carefully before committing.

## MapMaker

The active MapMaker tree is `src/mapmaker`. `dev/mapmaker` is deprecated and
retained only until its contents are audited.

The shared MapMaker emulator is also managed by the canonical environment:

```bash
cd /home/smith/Agon/mystuff/agon-dev-env
python3 scripts/setup_emulator.py mapmaker
scripts/run_emulator.sh mapmaker
```

MapMaker's working BBC BASIC autoexec sequence is documented centrally in
`codex/emulator.md`.
