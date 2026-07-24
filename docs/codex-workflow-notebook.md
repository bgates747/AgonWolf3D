# Codex Workflow Notebook

This is a concise, living handoff document for starting new Codex
conversations. Review it at the beginning of a session and update it when a
durable workflow convention becomes clear. Do not turn it into a detailed
session log or duplicate project specifications here.

## Working relationship

- Work collaboratively and conversationally. Make reasonable, reversible
  assumptions when they keep the task moving, and call out assumptions that
  could materially affect the result.
- Prefer completing a requested implementation and checking it over merely
  describing the steps.
- Preserve the user's existing and uncommitted work. Inspect repository status
  before edits, commits, or cleanup, and do not fold unrelated changes into a
  commit without agreement.
- Give concise progress updates during longer work. Lead the final report with
  the outcome, important decisions, verification performed, and any remaining
  issue.
- The user may manually move, rename, edit, build, or test files between
  prompts. Reinspect current state rather than assuming it is unchanged.
- Treat explanation, review, design discussion, and agreement in principle as
  read-only. Never modify code or project files until the user explicitly asks
  for the change. A statement describing how code should work is not by itself
  authorization to implement it; wait for a direct instruction to edit.
- Present design work in small, sequential, implementation-sized decisions.
  Do not assume the user has absorbed a complete design document before coding;
  introduce the next relevant constraint when it becomes actionable and work
  through it collaboratively.
- The user may intentionally discover or decide behavior while coding and let
  the code serve as the working specification. Treat that behavior as
  provisional until it is tested and agreed, then distill the durable contract
  into the authoritative specification instead of requiring an up-front,
  exhaustive design pass.

## Documentation roles

The local checkout of the official Agon platform documentation is rooted at:

```text
/home/smith/Agon/agon-docs/docs
```

Use this as the first source for MOS, VDP, API, and platform behavior when
working on Agon projects. Project-specific technical precis documents should
record the exact files consulted and the conclusions relevant to that project.

- **Specification:** the authoritative, normative description of a format or
  interface. Keep it compact and current.
- **Technical precis:** verified platform facts, API behavior, constraints, and
  mappings to relevant source code that will inform implementation.
- **Development log:** chronological session work, experiments, decisions, and
  brief rationale. It may be more detailed while work is exploratory.
- **Environment setup log:** durable machine, editor, toolchain, repository,
  symlink, and deployment setup—not application design work.
- **This notebook:** reusable workflow conventions only.

Avoid repeating the same explanation in several documents. A log should note
that a durable decision was made and point to the authoritative specification
instead of copying the entire decision.

## Python environment

- Before running Python in an open project, look for a project-local `.venv`
  and invoke its interpreter explicitly, even when the user's interactive
  terminal appears to have activated it. Tool shells may not inherit
  `VIRTUAL_ENV` or the same `PATH`.
- If no project `.venv` is found, ask the user before trying a system Python.
  Do not silently fall back to `/usr/bin/python`, `python3`, or another global
  interpreter.
- This is especially important when the project contains or imports the custom
  `agonutils` extension, because its compiled Python ABI and its Python-package
  dependencies must come from the matching virtual environment.
- For the `agon-utils` repository, verify the environment at the beginning of
  each new session with:

  ```text
  .venv/bin/python tests/test_agonutils.py
  ```

  Treat an import, ABI, dependency, or round-trip failure as an environment
  problem to resolve before running project scripts.
- An Agon application that imports `agonutils` must install the local
  `agon-utils` checkout into the application's own `.venv`; verifying only the
  utility repository's separate environment is insufficient. With compatible
  dependencies already installed, run this from the application root:

  ```text
  .venv/bin/python -m pip install --no-build-isolation --no-deps -e /home/smith/Agon/mystuff/agon-utils
  ```

  Then verify the consumer environment explicitly:

  ```text
  cd /home/smith/Agon/mystuff/agon-utils
  /path/to/application/.venv/bin/python tests/test_agonutils.py
  /path/to/application/.venv/bin/python -m pip check
  /path/to/application/.venv/bin/python -c "import agonutils; print(agonutils.__file__)"
  ```

  The reported extension path should resolve into the local `agon-utils`
  checkout, and the Python ABI must match the consumer environment.

## Assembly style

- When asked to consider or modify an eZ80 assembly-language project, read
  `docs/ez80_hacks.md` before proposing implementation idioms. It records
  project-tested, non-obvious eZ80 behavior, including undocumented
  instruction details that may be smaller or faster than conventional code.
- Use `ASCIZ` for null-terminated string literals instead of spelling out a
  separate zero byte. For example, the current preferred form is:

  ```asm
  agnb_filename: asciz "images.agnb"
  ```

  Treat this as the Modern Way in new assembly code unless an existing binary
  layout requires the terminator to be expressed separately.

## AGNB implementation reuse

- The hardware-proven AGNB image-container writer is implemented in
  `/home/smith/Agon/mystuff/agon-utils/examples/agnb/container/scripts/do_assembly.py`.
  Its `ImageRecord`, `make_chunk`, `make_buffer_record`, and `build_container`
  code implements the version 0.1 `RIFF AGNB` layout, alignment, explicit
  buffer IDs, and RGBA2222 validation. Reuse or adapt this implementation when
  adding AGNB generation to another project instead of independently
  reimplementing the binary format.
- The independent parser and structural validator is
  `/home/smith/Agon/mystuff/agon-utils/examples/agnb/container/scripts/view_agnb.py`.
  Its `parse_container` path can be reused without launching the GUI.

## Keeping context economical

- As requirements stabilize, distill exploratory prose into short,
  authoritative statements.
- Periodically prune obsolete discussion, resolved questions, duplicated
  explanations, and implementation speculation that is no longer useful.
- Use Git history as the normal archive for deleted or superseded prose. Do not
  maintain an `old`, `archive`, or `ignore this` directory merely to retain
  earlier wording; it creates search noise and can be mistaken for current
  guidance.
- Retain a short rejected-alternative note only when its rationale is likely to
  prevent repeating an expensive investigation.
- Preserve substantial experiments, benchmarks, or postmortems when they
  remain useful evidence, clearly labeling their status.
- Mark unfinished material `DRAFT`. Make authoritative documents and unresolved
  questions easy to identify.

## Starting a new conversation

At the start of a fresh session:

1. Read this notebook.
2. Find and select the open project's `.venv`. For `agon-utils`, run
   `.venv/bin/python tests/test_agonutils.py` and confirm that the custom
   extension works before using other Python scripts. If `.venv` is absent,
   ask the user before using system Python.
3. Read the current project specification or task document relevant to the
   requested work.
4. Read only the pertinent technical precis and latest development-log entry.
5. Inspect repository status and the relevant source files before changing
   anything.
6. Treat current documents and code as authoritative; consult Git history only
   when the reason for a current decision matters.

Do not reconstruct the entire project from old chat transcripts when the
current documents answer the question.

## Maintaining this notebook

- Add a convention only when it is likely to help across multiple sessions or
  projects.
- Phrase conventions as current guidance, not as a narrative of how they were
  discovered.
- Prune or revise this file as the workflow improves; Git retains its earlier
  versions.
- Other Codex sessions may propose additions after working with the user, but
  they should avoid adding project-specific technical details.
