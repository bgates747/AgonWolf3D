# Current image-loading startup trace

Date traced: 2026-07-24

> Integration update, 2026-07-24: the loose-file cube/panel pass documented
> below has now been replaced by a panels-only `tgt/images.agnb` load. Fonts,
> UI, sprites, distance walls, and sound effects retain the paths documented
> here. `agnb_load_images` calls `img_load_agnb_progress` after each panel has
> been streamed, consolidated, and created as a bitmap, preserving the splash,
> per-panel debug plot, moving BJ, progress text, stopwatch, and display flip.
> The historical loose panel trace remains below as the implementation
> baseline and explains the structure being replaced.

This document records the current, working image-loading path from program entry through application startup. It is a reference for replacing the loose-file panel, sprite, and distance-wall loads with AGNB container loads while preserving the existing splash/progress/debug behavior.

The active application entry point is `src/asm/wolf3d.asm`. Both `build/scripts/build_00_all_the_things.py` and `build/scripts/build_99_asm_assemble.py` assemble that file. The obsolete `src/asm/wolf3d1.asm` is not part of the working build.

## Top-level execution order

The binary is assembled for ADL mode at `0x040000` and begins with `jp start` (`src/asm/wolf3d.asm`).

1. `start` (`src/asm/wolf3d.asm`)
   - Saves `AF`, `BC`, `DE`, `IX`, and `IY`.
   - Calls `init`.
   - Calls `main`.
   - Restores the saved registers and returns to MOS with `HL=0`.

2. `init` (`src/asm/wolf3d.asm`)
   - Performs all startup display, font, UI, world-image, and sound loading described below.
   - Does not return until the user presses a key at the completed loading screen.

3. `main` (`src/asm/wolf3d.asm`)
   - Calls `new_game`, then enters `main_loop`.
   - No primary image files are loaded here. Rendering consumes the VDP buffers populated by `init`.

## `init` call trace, in execution order

### Display and timing setup

1. `vdu_clear_all_buffers` (`src/asm/vdu.asm`)
   - Sends buffer command 2 with buffer ID `0xFFFF`, clearing every VDP buffer.

2. `vdu_set_screen_mode` (`src/asm/vdu.asm`)
   - Called with `A=8+128`: mode 8, 320x240x64, double buffered.

3. `vdu_set_scaling` (`src/asm/vdu.asm`)
   - Called with `A=0`, disabling logical-screen scaling.

4. `stopwatch_set` (`src/asm/timer.asm`)
   - Calls `mos_sysvars` through the `MOSCALL` macro (`src/asm/mos_api.asm`).
   - Reads `(IX+sysvar_time)`.
   - Stores the 24-bit clock in `stopwatch_started` (`src/asm/timer.asm`).
   - Leaves `IX` pointing at the MOS system-variable table.

5. Inline timestamp initialization (`src/asm/wolf3d.asm`)
   - Copies `(IX+sysvar_time)` to `timestamp_now` (`src/asm/timer.asm`).
   - `sysvar_time EQU 00h` is defined in `src/asm/mos_api.asm`.

6. `vdu_enable_channels` (`src/asm/vdu_sound.asm`)
   - Enables the additional VDP audio channels.

7. `cursor_off` (`src/asm/vdu.asm`)

8. `printString` (`src/asm/functions.asm`)
   - Prints `loading_ui`, defined in `src/asm/wolf3d.asm`.

### Proportional bitmap-font loads

9. `load_font_itc_honda` (`src/asm/font_itc_honda.asm`)

10. `load_font_retro_computer` (`src/asm/font_retro_computer.asm`)

Both are generated, straight-line sequences. For every available glyph they:

1. Put a zero-terminated loose `.rgba2` filename in `HL`.
2. Put `filedata` in `DE`.
3. Put `65536` in `BC`.
4. Put `mos_load` in `A` and invoke `RST.LIL 08h`.
5. Put the glyph's VDP buffer ID in `HL`, width in `BC`, height in `DE`, and byte count in `IX`.
6. Call `vdu_load_img` (`src/asm/img_load.asm`).

The Honda buffers occupy the generated character-derived range `0x1120` through `0x117A`; Retro Computer occupies `0x1020` through `0x105A`. Missing glyphs reuse a fallback entry in each font's lookup table and do not cause another file load.

Each font lookup record and its `EQU` buffer IDs live in its generated source file. A lookup record contains two 24-bit fields: packed `[y_offset, height, width]`, followed by the glyph buffer ID. `font_bmp_plot` and `font_bmp_print` (`src/asm/fonts_bmp.asm`) use these records to select and plot one VDP bitmap per glyph, which is what permits proportional widths and vertical offsets.

### UI and splash assets

11. `load_ui_images` (`src/asm/ui_img.asm`)
   - Loads 11 loose `.rgba2` files by the same MOS-load → `filedata` → `vdu_load_img` sequence.
   - Uses VDP buffers `0x2000` through `0x200A`.
   - Important progress-screen assets:
     - `BUF_UI_BJ_120_120 EQU 0x2004`
     - `BUF_UI_SPLASH EQU 0x200A`
   - Prints `.` through `RST.LIL 10h` after each image.

12. `load_ui_images_bj` (`src/asm/ui_img_bj.asm`)
   - Loads 20 64x64 BJ weapon-animation images by the same sequence.
   - Uses VDP buffers `0x2100` through `0x2113`.
   - Prints `.` after each image.

The splash and moving 120x120 BJ image must therefore be loaded successfully before the panel/sprite/distance-wall progress loop begins.

### Loading-screen configuration

13. `vdu_colour_text` (`src/asm/vdu.asm`), with `A=132`, sets text background colour 4.

14. `vdu_colour_text` (`src/asm/vdu.asm`), with `A=47`, sets the text foreground.

15. `vdu_gcol_bg` (`src/asm/vdu.asm`), with `A=0`, `C=4`, sets the graphics background.

16. `vdu_clg` (`src/asm/vdu.asm`) clears graphics.

17. `cursor_off` (`src/asm/vdu.asm`) hides the cursor again.

18. `vdu_set_txt_viewport` (`src/asm/vdu.asm`)
   - Called with left 0, top 20, right 39, bottom 29.

19. `img_load_init` (`src/asm/img_load.asm`)
   - Initializes the BJ progress animation once:
     - horizontal position 10, bounds 10–200, velocity +1;
     - vertical position and bounds 45, velocity 0.
   - These values persist across all three world-image families.

### Panels, sprites, and distance walls

The following three blocks repeat the same setup and call:

20. Panels/cubes (`src/asm/wolf3d.asm`)
   - `BC=cube_num_panels` (308).
   - `cur_buffer_id_lut=cube_buffer_id_lut`.
   - `cur_load_jump_table=cube_load_panels_table`.
   - Calls `img_load_main`.
   - Generated buffer range: `0x0100`–`0x0233`.

21. Sprites (`src/asm/wolf3d.asm`)
   - `BC=sprite_num_panels` (100).
   - Uses `sprite_buffer_id_lut` and `sprite_load_panels_table`.
   - Calls `img_load_main`.
   - Generated buffer range: `0x0234`–`0x0297`.

22. Distance walls (`src/asm/wolf3d.asm`)
   - `BC=dws_num_panels` (9).
   - Uses `dws_buffer_id_lut` and `dws_load_panels_table`.
   - Calls `img_load_main`.
   - Generated buffer range: `0x0298`–`0x02A0`.

The buffer constants, counts, and lookup tables, plus the remaining sprite and
distance-wall loose loaders, are generated in `src/asm/images.asm` by
`build/scripts/build_91_asm_images.py`. Cube/panel payloads are generated into
`tgt/images.agnb` by `build/scripts/build_05a_make_panels_agnb.py`.

### `img_load_main` per-image trace

`img_load_main` (`src/asm/img_load.asm`) resets `cur_file_idx` to zero at the start of each family. For each item it then performs:

1. Save the family loop counter `BC`.
2. Call `load_next_panel` (`src/asm/img_load.asm`).
3. Call `tmp_draw_all_the_things` (`src/asm/img_load.asm`).
   - Selects `BUF_UI_SPLASH`.
   - Calls `vdu_plot_bmp` at `(0,0)`.
4. Select `cur_buffer_id` with `vdu_buff_select` (`src/asm/vdu.asm`).
5. Call `vdu_plot_bmp` (`src/asm/vdu.asm`) at `(0,0)`.
   - This plots the newly loaded texture as a visual debugging aid.
6. Call `move_bj` (`src/asm/img_load.asm`).
   - Selects `BUF_UI_BJ_120_120`.
   - Advances and bounces its x coordinate.
   - Plots it at the current `(x,y)`.
7. Call `font_bmp_print` (`src/asm/fonts_bmp.asm`) with:
   - font table `font_itc_honda` (`src/asm/font_itc_honda.asm`);
   - string `hello_world` (`src/asm/wolf3d.asm`);
   - pixel position `(32,2)`.
8. Call `vdu_cls` (`src/asm/vdu.asm`) to clear the text area.
9. Print `cur_filename`, then a newline, through `printString` and `printNewLine` (`src/asm/functions.asm`).
10. Print `loading_time`, call `stopwatch_get` (`src/asm/timer.asm`), then `printDec` (`src/asm/functions.asm`).
11. Call `vdu_flip` (`src/asm/vdu.asm`).
12. Restore and decrement the family counter, then repeat until zero.

The splash is redrawn every iteration, followed by the debug texture and moving BJ. The filename and elapsed-time text are updated every iteration. Any AGNB replacement must preserve this per-item opportunity if the existing visual progress behavior is to remain unchanged.

### `load_next_panel` dispatch

`load_next_panel` (`src/asm/img_load.asm`) does two separate 24-bit table lookups:

1. Multiplies `cur_file_idx` by three, adds `cur_load_jump_table`, and reads a 24-bit routine address.
2. Writes that address into the operand of its local `call 0`, then executes it. This is self-modifying code.
3. Repeats the index calculation against `cur_buffer_id_lut`, reads the 24-bit buffer ID, and stores it in `cur_buffer_id`.
4. Increments `cur_file_idx`.

The current jump-table routine is one hard-coded generated routine per loose image. The table-driven family structure, count, buffer-ID lookup, per-item display loop, and index state can remain useful even when those individual routines are replaced.

### One generated world-image load routine

Every routine in `src/asm/images.asm` currently has this effective shape:

```asm
    ld hl,F_filename
    ld (cur_filename),hl
    ld de,filedata
    ld bc,65536
    ld a,mos_load
    RST.LIL 08h
    ld hl,BUF_image
    ld bc,width
    ld de,height
    ld ix,width*height
    call vdu_load_img
    ret
```

Thus each routine owns the filename, buffer ID, dimensions, and uncompressed byte count. It also publishes the filename pointer for the progress display.

### `vdu_load_img` and the shared payload scratch area

`vdu_load_img` (`src/asm/img_load.asm`):

1. Saves width and height.
2. Calls `vdu_load_buffer_from_file` (`src/asm/files.asm`).
3. Restores height and width.
4. Sets `A=1` for RGBA2222.
5. Tail-jumps to `vdu_bmp_create` (`src/asm/vdu.asm`).

Despite its name, `vdu_load_buffer_from_file` does not read a filesystem file. The generated caller has already loaded the file into `filedata`. This routine builds and sends one VDP byte stream that:

1. Clears the destination buffer.
2. Selects that buffer as the current bitmap.
3. Uploads `IX` bytes beginning at `filedata`.

The VDP upload length in this template is 16-bit, so one call cannot upload more than 65,535 bytes. `vdu_bmp_create` then defines the selected buffer as a bitmap using the supplied dimensions and RGBA2222 format.

`src/asm/files.asm` is deliberately the final include in `src/asm/wolf3d.asm`. Its `filedata` label is immediately after the VDU command template and has no allocated storage; MOS loads overwrite otherwise unused memory following the assembled program. Moving code or data after this include would allow image loads to overwrite it.

### End of startup loading

23. `sfx_load_main` (`src/asm/sfx.asm`) loads sound buffers after the images. It reuses `cur_buffer_id_lut` and `cur_load_jump_table`, but is outside the first image-container scope.

24. `init` enables playback, identifies emulator versus hardware from the stopwatch duration, prints the final elapsed time, flips the display, and waits for a keypress (`src/asm/wolf3d.asm`).

25. `main` calls `new_game`, then enters the application loop (`src/asm/wolf3d.asm`).

## Image-loader state and scratch-memory inventory

Unless an absolute address is stated, these are labels assembled into the application image rather than fixed external addresses.

| Symbol or storage | Size/use | Defined in |
|---|---|---|
| `cur_file_idx` | 24-bit current item index; reset for every family | `src/asm/img_load.asm` |
| `cur_filename` | 24-bit pointer used by loading-screen text | `src/asm/img_load.asm` |
| `cur_buffer_id` | 24-bit ID of the most recently loaded image | `src/asm/img_load.asm` |
| `cur_buffer_id_lut` | 24-bit pointer to current family ID table | `src/asm/img_load.asm` |
| `cur_load_jump_table` | 24-bit pointer to current family routine table | `src/asm/img_load.asm` |
| `bj_xvel`, `bj_x_cur`, `bj_x_min`, `bj_x_max` | Four 24-bit horizontal animation values | `src/asm/img_load.asm` |
| `bj_yvel`, `bj_y_cur`, `bj_y_min`, `bj_y_max` | Four 24-bit vertical animation values | `src/asm/img_load.asm` |
| `filedata` | Unallocated tail scratch address for the current loose file payload | `src/asm/files.asm` |
| `stopwatch_started` | Three-byte startup stopwatch value | `src/asm/timer.asm` |
| `timestamp_now`, `timestamp_old`, `timestamp_chg` | Three 24-bit global clock values | `src/asm/timer.asm` |
| `_printDecBuffer` | Nine-byte decimal-print scratch buffer | `src/asm/functions.asm` |
| `is_emulator` | One-byte startup result | `src/asm/wolf3d.asm` |
| `sysvar_time EQU 00h` | Offset of the MOS clock in the system-variable table | `src/asm/mos_api.asm` |

The relevant VDU helpers also use self-modifying command templates local to their routines:

- `vdu_load_buffer_from_file` patches three buffer IDs and one 16-bit size (`src/asm/files.asm`).
- `vdu_buff_select`, `vdu_bmp_create`, and `vdu_plot_bmp` patch arguments into static VDU byte strings (`src/asm/vdu.asm`).
- `load_next_panel` patches the operand of a local `call 0` (`src/asm/img_load.asm`).

Other fixed scratch regions used later by the running application, but not by startup image loading, include:

- `cell_status EQU 0xB7E000` and `cell_views EQU 0xB7E400` (`src/asm/maps.asm`);
- `sprite_table_base EQU 0xB7FC00` (`src/asm/sprites.asm`).

These regions still matter when choosing any fixed RAM location for AGNB metadata, manifests, read buffers, or loader workspace.

## Current buffer-ID conventions

| Asset family | IDs | Source of `EQU`s |
|---|---:|---|
| Panels/cubes | `0x0100`–`0x0233` | `src/asm/images.asm` |
| Sprites | `0x0234`–`0x0297` | `src/asm/images.asm` |
| Distance walls | `0x0298`–`0x02A0` | `src/asm/images.asm` |
| Retro Computer glyphs | character-derived IDs in `0x1020`–`0x105A` | `src/asm/font_retro_computer.asm` |
| ITC Honda glyphs | character-derived IDs in `0x1120`–`0x117A` | `src/asm/font_itc_honda.asm` |
| Core UI | `0x2000`–`0x200A` | `src/asm/ui_img.asm` |
| BJ weapon UI | `0x2100`–`0x2113` | `src/asm/ui_img_bj.asm` |

The world-image IDs are one contiguous generated sequence beginning at 256. The family boundaries are a consequence of current manifest counts, so regenerating changed manifests can move later-family IDs unless the generator is changed to stabilize them.

## AGNB integration implications exposed by this trace

1. Replacing only `vdu_load_img` is insufficient: the loose-file MOS load occurs earlier, inside every generated per-image routine.
2. The useful reusable structure is the family count, ID LUT, ordered per-item loop, current-item globals, and progress/debug drawing.
3. An AGNB-aware path must provide, per item, at least destination buffer ID, dimensions/format or equivalent creation metadata, payload location/length, and a displayable name or substitute if filename progress text is retained.
4. The current scratch contract is a single payload at `filedata`. AGNB introduces a container plus directory/metadata access pattern, so its RAM ownership must not collide with the executable tail or the fixed map/sprite regions.
5. The progress animation currently advances once per image, not once per source file. A container loader should expose an item-by-item step or callback if this cadence is to remain.
6. The debug texture plot depends on `cur_buffer_id` being updated after each item has become a valid VDP bitmap.
7. The splash and BJ progress assets are UI loose files loaded before the world containers. They may remain loose during the first implementation.
8. Font and UI containerization are follow-up work. Fonts require one VDP buffer per proportional glyph under the present renderer, so a future font container must retain per-glyph buffer IDs and metrics.
