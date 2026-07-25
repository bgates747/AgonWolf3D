; ############ GAME VARIABLES ############
; This file separates durable game state from runtime-only game workspace.
;
; Mutable map cells and sprite records are stored elsewhere. They occupy the
; active 8 KiB room image at cell_status and the visited-room backing images
; addressed by room_dat_lut. A complete save file must store those room images
; separately from the scalar record below.

; ############ DURABLE SAVE RECORD ############
; The bytes from game_save_vars_start through game_save_vars_end contain the
; confirmed scalar state needed to resume a game. Keep this block contiguous
; so a versioned save-file implementation can write and validate it directly.
game_save_vars_start:

; score and player condition
plyr_score: dl 0x000000
plyr_health: dl 0x000000
plyr_max_health: dl 100
plyr_lives: dl 3

; floor, room, map position, and orientation
cur_floor: db 0x00 ; 0-255, corresponds to floor_num in build scripts
cur_room: db 0x00 ; 0-9, corresponds to room_id in build scripts
cur_cell: db 0x00 ; 0-255, corresponds to cell_id in build scripts
from_floor: db 0x00 ; 0-255, corresponds to floor_num in build scripts
from_room: db 0x00 ; 0-9, corresponds to room_id in build scripts
orientation: db 0x00 ; 0-3 north,east,south,west
cur_x: db 0x00
cur_y: db 0x00
       db 0x00 ; padding so we can read/write 24-bit registers

; reciprocal-room-door state
room_transition_active: db 0
room_transition_entry_delta: dl 0 ; low to high: map-relative dx,dy,0

; active player projectile
plyr_shot_x: db 0x00
plyr_shot_y: db 0x00
             db 0x00 ; padding
plyr_shot_xvel: db 0x00
plyr_shot_yvel: db 0x00
                db 0x00 ; padding
plyr_shot_status: db 0xFF ; -1 = no shot, otherwise direction of travel
plyr_shot_damage: db 0x00

; weapons and ammunition
plyr_wpns: db 0x00
plyr_wpn_active: db 0x00
plyr_wpn_knife: equ %00000001
plyr_wpn_pistol: equ %00000010
plyr_wpn_mg: equ %00000100
plyr_wpn_gg: equ %00001000
plyr_wpn_anim_fr: dl 0x000000
plyr_ammo: dl 0x000000

; room visitation identifies which room_dat_lut backing images are valid
room_flags: blkb 10,0
room_flag_visited: equ %00000001

; authoritative bookkeeping for the active room's sprite table
sprite_table_pointer: dl sprite_table_base
table_active_sprites: db 0x00
sprite_next_id: db 0

; current health portrait; derivable from plyr_health but effectively free to
; preserve as part of the contiguous save image
bj_health_image: dl BUF_UI_BJ_100

; random-generator state preserves the future random sequence after loading
r_seed: db 0x50
seed1: dl 0
seed2: dl 0

game_save_vars_end:
game_save_vars_size: equ game_save_vars_end-game_save_vars_start


; ############ RUNTIME-ONLY GAME WORKSPACE ############
; These variables are game-related, but should be reset, reconstructed, or
; rebased after loading rather than copied verbatim from a save file.
game_runtime_vars_start:

; current input and movement calculation
xvel: db 0x00
yvel: db 0x00
      db 0x00 ; padding
dy: db 0x00
dx: db 0x00
    db 0x00 ; padding
avel: db 0x00 ; angular velocity in orientation ticks per movement tick

; absolute timestamp for the active projectile; restore code must rebase it
plyr_shot_time: dl 0x000000

; parameters derived from plyr_wpn_active
plyr_wpn_damage: db 0x00
plyr_wpn_ui_sm: dl 0x000000
plyr_wpn_ui_lg: dl 0x000000
plyr_wpn_fire_rate: dl 0x000000

; absolute timer deadlines; restore code must reset or rebase them
plyr_wpn_select_tmr: ds 6
plyr_wpn_fire_tmr: ds 6

; formatted-number scratch
plyr_ammo_str: ds 8
               db 0

; movement timing
speed_plyr: equ 1
plyr_move_timer: ds 6
plyr_move_rate: equ 120/4

; player sprite workspace; most fields are not currently used
; uses the same offsets from its table base as the main sprite table
plyr_start_variables:
plyr_id: db table_max_records
plyr_type: db 0x00
plyr_base_bufferId: dl 0x000000
plyr_move_program: dl 0x000000
plyr_collisions: db 0x00
plyr_dim_x: db 0x00
plyr_dim_y: db 0x00
plyr_x: dl 0x000000
plyr_y: dl 0x000000
plyr_xvel: dl 0x000000
plyr_yvel: dl 0x000000
playervel: dl 0x000000
plyr_heading: dl 0x000000
plyr_orientation: dl 0x000000
plyr_animation: db 0x00
plyr_anim_tmr: db 0x00
plyr_move_step: db 0x00
plyr_points: db 0x00
plyr_health_damage: db 0x00
plyr_end_variables:

game_runtime_vars_end:
game_runtime_vars_size: equ game_runtime_vars_end-game_runtime_vars_start


; ############ DEBUG-ONLY GAME WORKSPACE ############
; Nothing between game_debug_vars_start and game_debug_vars_end is part of the
; save-file contract. Any value placed here may disappear, reset, or become
; misleading after a reload, at the Author's sanity's peril.
game_debug_vars_start:

debug_timer: db 0x01
last_damage: dl 0x00

game_debug_vars_end:
game_debug_vars_size: equ game_debug_vars_end-game_debug_vars_start


; ############ SAVE-STATE FOLLOW-UPS ############
; These candidates remain in their owning modules until their authority and
; restoration requirements are understood:
;
; - main-loop, global timestamp, and sprite timers need an explicit reset or
;   rebase policy because absolute deadlines are not portable across sessions.
; - key possession and floor-completion/progression state were not found as
;   authoritative global variables and may not yet be implemented.
; - active and visited room images need their own save-file records; the
;   durable scalar block records which cached room images are meaningful.
