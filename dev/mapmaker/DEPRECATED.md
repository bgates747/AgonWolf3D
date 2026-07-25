# DEPRECATED — DO NOT USE FOR CURRENT MAP WORK

This directory contains an older layout in which each numbered level folder
has its own copy of MapMaker. It has been superseded by:

```text
src/mapmaker
```

The current directory keeps one MapMaker application beside its numbered tile
packs and map files. Its emulator environment is initialized by:

```bash
.venv/bin/python src/mapmaker/setup_emulator.py
```

Do not edit maps here or use these copies of `mapmaker.bas` and
`MAPMAKER.BBC`. This deprecated tree is being retained temporarily until its
contents have been audited for anything still worth preserving.
