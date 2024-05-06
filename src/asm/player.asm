; ######## GAME STATE VARIABLES #######
; THESE MUST BE IN THIS ORDER FOR new_game TO WORK PROPERLY
player_score: db 0x00,#00,#00 ; bcd
; player current health,binary
; when < 0 player splodes
; restores to player_max_health when new ship spawns
player_health: db 50 ; binary TODO: temp set at 50% for testing, set to 100 for actual game
; max player health,binary
; can increase with power-ups (todo)
player_max_health: db 100 ; binary
; when reaches zero,game ends
; can increase based on TODO
player_lives: db 0x03 ; binary

; ######### Player Variables ##########
; player position on the map and orientation
cur_floor: db 0x00 ; 0-255, corresponds to floor_num in build scripts
cur_room: db 0x00 ; 0-9, corresponds to room_id in build scripts
cur_cell: db 0x00 ; 0-255, corresponds to cell_id in build scripts
from_floor: db 0x00 ; 0-255, corresponds to floor_num in build scripts
from_room: db 0x00 ; 0-9, corresponds to room_id in build scripts
orientation: db 0x00 ; 0-3 north,east,south,west
cur_x: db 0x00
cur_y: db 0x00
       db 0x00 ; padding so we can read/write 24-bit registers
xvel:  db 0x00
yvel:  db 0x00
       db 0x00 ; padding
dy:    db 0x00
dx:    db 0x00
       db 0x00 ; padding

player_shot_x:      db 0x00
player_shot_y:      db 0x00
                    db 0x00 ; padding
player_shot_xvel:   db 0x00
player_shot_yvel:   db 0x00
                    db 0x00 ; padding
player_shot_status: db 0xFF ; -1 = no shot, otherwise shot direction of travel
player_shot_time:   dl 0x000000 ; time shot was fired from RTC

; ######### PLAYER CONSTANTS ##########
speed_player: equ 0x01 ; 1 map grid unit per movement tick
move_timer_reset: equ 8 ; 4 ticks per secoond at 32 frames per second

; ######### PLAYER SPRITE PARAMETERS ##########
; uses the same offsets from its table base as the main sprite table:
player_start_variables: ; label marking beginning of table
player_id:               db table_max_records
player_type:             db     0x00 ; 1 bytes currently not used
player_base_bufferId:    dl 0x000000 ; 3 bytes bitmap bufferId
player_move_program:     dl 0x000000 ; 3 bytes not currently used
player_collisions:       db     0x00 ; 1 bytes bit 0 set=alive, otherwise dead, bit 1 set=just died
player_dim_x:            db     0x00 ; 1 bytes sprite width in pixels
player_dim_y:            db     0x00 ; 1 bytes sprite height in pixels
player_x:                dl 0x000000 ; 3 bytes 16.8 fractional x position in pixels
player_y:                dl 0x000000 ; 3 bytes 16.8 fractional y position in pixels
player_xvel:             dl 0x000000 ; 3 bytes x-component velocity, 16.8 fixed, pixels
player_yvel:             dl 0x000000 ; 3 bytes y-component velocity, 16.8 fixed, pixels
playervel:              dl 0x000000 ; 3 bytes velocity px/frame (16.8 fixed)
player_heading:          dl 0x000000 ; 3 bytes sprite movement direction deg256 16.8 fixed
player_orientation:      dl 0x000000 ; 3 bytes not currently used
player_animation:        db     0x00 ; 1 bytes not currently used
player_animation_timer:  db     0x00 ; 1 bytes not currently used
player_move_timer:       db     0x00 ; 1 bytes not currently used
player_move_step:        db     0x00 ; 1 bytes not currently used
player_points:           db     0x00 ; 1 bytes not currently used
player_health_damage:    db     0x00 ; 1 bytes not currently used
player_end_variables: ; for when we want to traverse this table in reverse

; set initial player position
; inputs: none,everything is hardcoded
; outputs: player set to the first valid position on the map
; destroys: a
player_init:
    call get_start_pos ; a = cell_id, d = map_y, e = map_x
    ld (cur_cell),a
    ld (cur_x),de ; implicitly populates cur_y
    xor a ; north is default orientation
    ld (orientation),a
    ld a,move_timer_reset
    ld (player_move_timer),a
    ret

; modifies the players health by a set amount
; inputs: a is the signed amount to modify health
player_mod_health:
    ld hl,player_health
    add a,(hl)
    ld (hl),a
    ret

player_shoot:
    ; play the sound effect
    call sfx_play_shot_pistol
    ; check whether the player hit anything
    ld a,(orientation) ; direction shot is moving
    ld (player_shot_status),a ; save shot direction -- indicates live shot in flight
    ld e,a
    ld d,1 ; shot "velocity" in map units
    call get_dx_dy ; d,e = dy,dx
    ld (player_shot_xvel),de ; implicity populates yvel
    ld hl,(cur_x) ; h,l = player y,x
    ld (player_shot_x),hl ; initial shot position

    ; call stepRegistersHex

@move_bullet:
    ld de,(player_shot_xvel) ; d,e = shot yvel,xvel
    ld hl,(player_shot_x) ; h,l = player shot y,x

    push hl ; DEBUG
    pop bc ; DEBUG

    ; bump bullet position one map unit in direction of travel
    ld a,l ; player shot x
    add a,e ; add xvel
    ld l,a ; save new x
    ld a,h ; player shot y
    add a,d ; add yvel
    ld h,a ; save new y

    ; call stepRegistersHex
    
    ld (player_shot_x),hl ; and save that position
    ex de,hl ; d,e = bullet y,x
    call get_cell_from_coords ; ix = pointer to cell_status lut; a = obj_id, bc = cell_id
; check whether target cell contains a sprite
    ld a,(ix+map_sprite_id)
    cp 255 ; value if not sprite
    jr z,@not_sprite
; is a sprite so run its "use" behavior routine
    call sprite_set_pointer
    ld a,sp_shoot
    call do_sprite_behavior ; a = sprite behavior return code
    cp 255 ; value if shot hit a shootable sprite
    ret z ; if we hit a sprite, we're done
; fall through because we still need to check out what's going on in the target cell
@not_sprite:
    ld de,(player_shot_xvel) ; restore yvel,xvel to d,e
; read map type/status mask from target cell
    ld a,(ix+map_type_status)
    and %00000011 ; mask off everytying but the render type mask bits
; branch on the values in the bitmask
    cp render_type_floor
    jr z,@move_bullet ; keep going if map cell is a floor
    ld a,255
    ld (player_shot_status),a ; set shot status to -1 to indicate shot is done
    ret ; combat ended

; process player keyboard input
; Inputs: player_x/y set at desired position
; Returns: player position updated
; Destroys: probably everything except maybe iy
player_input:
; first check player_move_timer for zero
    ld a,(player_move_timer)
    and a ; if zero we can move so get keyboard move input
    jr z,@get_kb
    dec a ; otherwise decrement timer and return
    ld (player_move_timer),a
    ret
@get_kb:
; reset player component velocities to zero as the default
    ld hl,0
    ld (xvel),hl ; implicitly sets yvel
; we will set a to zero on a keypress, default of -1 will mean no keypress
    ld a,-1
; check for keypresses and branch accordingly
; for how this works,see: https://github.com/breakintoprogram/agon-docs/wiki/MOS-API-%E2%80%90-Virtual-Keyboard
    MOSCALL	mos_getkbmap ;ix = pointer to MOS virtual keys table
; we test all four arrow keys and add/subract velocities accordingly
; this handles the case where two opposing movement keys
; are down simultaneously (velocities will net to zero)
; and allows diagonal movement when a vertical and horizontal key are down
; it also allows movement and action keys to be detected simultaneously
; so we can walk and chew gum at the same time
;
; BEGIN CHECKING FOR KEY PRESSES
;
; 34 W player moves forward
    bit 1,(ix+4)
    jr z,@W
    ld a,speed_player ; this is *camera* relative, not map relative, so y-axis is NOT inverted!
    ld (yvel),a
    xor a
@W: 
; =====================
; 82 S player moves backward
    bit 1,(ix+10)
    jr z,@S
    ld d,-speed_player ; this is *camera* relative, not map relative, so y-axis is NOT inverted!
    ld a,(yvel)
    add a,d
    ld (yvel),a
    xor a
@S:
; =====================
; 66 A plyer moves left
    bit 1,(ix+8)
    jr z,@A
    ld a,-speed_player ; no funky axis conversion here
    ld (xvel),a
    xor a
@A:
; =====================
; 51 D player moves right
    bit 2,(ix+6)
    jr z,@D
    ld d,speed_player ; no funky axis conversion here
    ld a,(xvel)
    add a,d
    ld (xvel),a
    xor a
@D:
; =====================
; 26 Left player rotates anti-clockwise
    bit 1,(ix+3)
    jr z,@Left
    ld a,(orientation)
    dec a
    and 0x03 ; modulo 4
    ld (orientation),a
    xor a
@Left:
; =====================
; 122 Right player rotates clockwise
    bit 1,(ix+15)
    jr z,@Right
    ld a,(orientation)
    inc a
    and 0x03 ; modulo 4
    ld (orientation),a
    xor a
@Right:
; =====================
; 99 Space FIRE ZEE MISSILES!!!111
; TODO: implement 
    bit 2,(ix+12)
    jr z,@Space
    call player_shoot
    xor a ; we may not want to reset move timer on a shot
@Space:
; =====================
; check whether player pressed a key
    and a ; this will be -1 if player didn't press a key
    ret nz ; non zero so no key pressed
; move player according to velocities set by keypresses
; TODO: this finagling could go to a conveninece function
    ld de,(xvel) ; d = yvel, e = xvel
    ld a,(orientation)
    call trans_dx_dy ; d = dy, e = dx
    ld (dx),de
    ld a,(cur_x)
    add a,e
    ld e,a
    ld a,(cur_y)
    add a,d
    ld d,a
    ld (xvel),de ; save yvel,xvel from d,e
    call get_cell_from_coords ; ix points to cell defs/status, a is target cell current obj_id, bc is cell_id
; check whether target cell contains a sprite
    ld a,(ix+map_sprite_id)
    cp 255 ; value if not sprite
    jr z,@not_sprite
; is a sprite so run its "use" behavior routine
    call sprite_set_pointer
    ld a,sp_use
    call do_sprite_behavior
; fall through because we still need to check out what's going on in the target cell
@not_sprite:
    ld de,(xvel) ; restore yvel,xvel to d,e
; read map type/status mask from target cell
    ld a,(ix+map_type_status)
    ld b,a ; b = target cell type/status
; branch on the values in the bitmask
    ld a,cell_is_door
    and b
    jr nz,@door
    ld a,cell_is_wall
    and b
    ret nz ; can't move thru walls
    jr @move_it ; if it wasn't a wall or door, move as normal
@door:
    ld de,(dx) ; d = dy, e = dx
    call get_dir_from_dy_dx ; a is direction of attempted movement
    push af
    ld d,2 ; 1 past the door in the movement direction
    ld e,a
    call get_dx_dy
    ld (dx),de
    pop af
    ld e,a
    ld d,2
    ld bc,(cur_x)
    call get_neighbor ; ix points to cell defs/status, a is target cell current obj_id
    ld a,(ix+map_type_status)
    ld b,a ; b = target cell type/status
    ld a,cell_is_wall
    and b
    ret nz ; can't move thru walls
    ; fall through to @move_it
@move_it:
; we are cleared for movement so update player position
    ld de,0 ; make sure deu is zero
    ld bc,(dx) ; b = dy, c = dx
    ld a,(cur_x)
    add a,c
    ld e,a
    ld (cur_x),a
    ld a,(cur_y)
    add a,b
    ld d,a
    ld (cur_y),a
@reset_move_timer:
    ld a,move_timer_reset
    ld (player_move_timer),a
    ret