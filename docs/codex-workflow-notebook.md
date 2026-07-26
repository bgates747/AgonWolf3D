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
`True` assignments. Do not redesign that convention without the Author's
agreement. For map-only changes, stages 06, 07, 91c, and 99 are the effective
dependency path.

The current release-planning document is:

```text
docs/v0.3.0-alpha-goals.md
```

It is a draft. Update it as scope is agreed; do not silently promote candidate
items into release requirements.

Always invoke Python through `.venv/bin/python`. The environment uses the
editable canonical agon-utils checkout at
`/home/smith/Agon/mystuff/agon-utils`.

When a Python script provides progress output, invoke it unbuffered (for
example, `.venv/bin/python -u script.py`) or in a PTY. Progress messages must
be visible while the job is running so Codex can monitor the work, report
useful status, and notice a stalled or failed stage promptly; do not allow
redirected stdout buffering to hide them until process exit. Before running a
potentially large job, inspect how frequently it prints. If it could emit
thousands of per-file, per-record, or per-cell messages, first change or
configure its reporting to provide bounded milestones, periodic summaries,
warnings, and errors instead. Preserve useful progress visibility without
spending conversation tokens on mechanically repetitive output.

## Checklist conventions

Give every actionable checkbox or TODO an explicit, stable number, including
Codex recommendations and temporary implementation checklists. This lets the
Author refer to an item by number alone.

- Number items consecutively within the canonical checklist.
- Never reuse or silently renumber an item after it has been presented; append
  newly discovered work with new numbers.
- Supporting explanation may remain unnumbered, but any independently
  actionable subtask must receive its own checkbox and number.
- When work proceeds off the cuff, retroactively add the completed actions in
  the order performed and mark them complete. Keep planned work after them
  rather than rewriting history.

Keep implementation status in the goals/checklist and development log.
Reference manuals describe the settled design contract or expected behavior
without embedding task numbers, open/complete status, or transitional
“once implemented” language. This avoids synchronized status edits across
multiple documents whenever a task is completed.

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

The master build's `map_src_dir` is the sole map-selection setting. Stage 06
discovers every direct `FF_R.map` child, requires dense zero-based floors and
dense zero-based rooms within each floor, and supplies that ordered set to the
remaining map stages. Do not reintroduce a manually synchronized
`floor_nums` list.

The living map-design, build, format, and runtime reference is:

```text
docs/map-design-manual/README.md
```

Read the relevant practical chapter before map work and the technical
appendices before changing map build or assembly behavior. Update the manual
when a map feature's implemented behavior or authoring contract changes.

In this project, a **map room** means one complete map definition that can be
held in one MapMaker instance. MapMaker authors a 15×15 tile area because its
original display layout lacked room for 16×16. The build/runtime
representation pads that authored area to the engine's natural 16×16 grid,
where the runtime cell ID holds 4-bit X and Y coordinates. Do not treat the
authored 15×15 size as an accidental off-by-one error.

Room-to-room movement crosses between separate map definitions. Verifying and
correcting those transitions is the first Author-defined v0.3.0alpha task. A
true 16×16 MapMaker redesign is explicitly a possible long-term goal, not part
of the v0.3 release.

The shared MapMaker emulator is also managed by the canonical environment:

```bash
cd /home/smith/Agon/mystuff/agon-dev-env
python3 scripts/setup_emulator.py mapmaker
scripts/run_emulator.sh mapmaker
```

MapMaker's working BBC BASIC autoexec sequence is documented centrally in
`codex/emulator.md`.
