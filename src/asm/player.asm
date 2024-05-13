; ######## GAME STATE VARIABLES #######
; we use 24-bit values for all of these for easy use with Num2String function
player_score: dl 0x000000 ; binary
; player current health,binary
; when < 0 player splodes
; restores to player_max_health when new ship spawns
player_health: dl 0x000000 ; binary TODO: temp set at 50% for testing, set to 100 for actual game
; max player health,binary
; can increase with power-ups (todo)
player_max_health: dl 100 ; binary
; when reaches zero,game ends
; can increase based on TODO
player_lives: dl 3 ; binary

player_health_str:  ds 8 ; Num2String buffer
                    db 0 ; string terminator

player_score_str:   ds 8 ; Num2String buffer
                    db 0 ; string terminator

player_lives_str:   ds 8 ; Num2String buffer
                    db 0 ; string terminator

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
avel:  db 0x00 ; player angular velocity in orientation ticks per move tick

player_shot_x:      db 0x00
player_shot_y:      db 0x00
                    db 0x00 ; padding
player_shot_xvel:   db 0x00
player_shot_yvel:   db 0x00
                    db 0x00 ; padding
player_shot_status: db 0xFF ; -1 = no shot, otherwise shot direction of travel
player_shot_time:   dl 0x000000 ; time shot was fired from RTC
player_shot_damage: db 0x00 ; damage dealt by latest shot

player_weapons:     db 0x00 ; weapons in player's possession according to following bitmasks
player_weapon_active: db 0x00 ; currently active weapon according to following bitmasks
player_weapon_knife: equ %00000001
player_weapon_pistol: equ %00000010
player_weapon_machine_gun: equ %00000100
player_weapon_gatling_gun: equ %00001000
player_weapon_damage: db 0x00 ; damage dealt by current weapon
player_weapon_ui_buffer_id_small: dl 0x000000 ; bufferId for weapon UI
player_weapon_ui_buffer_id_large: dl 0x000000 ; bufferId for weapon UI
player_weapon_select_timer: ds 6 ; time until player can selet a new weapon in 1/120ths of a second
player_weapon_fire_timer: ds 6 ; time until player can fire again in 1/120ths of a second
player_weapon_fire_rate: dl 0x000000 ; 1/rate of fire in 1/120ths of a second

player_weapon_animation_timer: ds 6 ; time until next weapon animation frame in 1/120ths of a second
player_weapon_animation_frame: dl 0x000000 ; current weapon animation frame
player_weapon_animation_timer_reset: equ 10 


player_ammo: dl 0x000000 ; ammo for all projectile weapons
player_ammo_str: ds 8 ; Num2String buffer
                 db 0 ; string terminator

; ######### PLAYER CONSTANTS ##########
speed_player: equ 0x01 ; 1 map grid unit per movement tick
player_move_timer: ds 6 ; time until player can move again in 1/120ths of a second
player_move_rate: equ 120/4 ; 4 times per second

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
playervel:               dl 0x000000 ; 3 bytes velocity px/frame (16.8 fixed)
player_heading:          dl 0x000000 ; 3 bytes sprite movement direction deg256 16.8 fixed
player_orientation:      dl 0x000000 ; 3 bytes not currently used
player_animation:        db     0x00 ; 1 bytes not currently used
player_animation_timer:  db     0x00 ; 1 bytes not currently used
; player_move_timer:       db     0x00 ; 1 bytes not currently used
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
    ld hl,player_move_rate
    ld iy,player_move_timer
    call timer_set
    ld a,80 ; 80% health
    ld (player_health),a
    ; ld a,%00000001 ; knife only
    ld a,%00001111 ; all weapons DEBUG
    ld (player_weapons),a
    ld a,player_weapon_knife
    ld (player_weapon_active),a
    call player_set_weapon_parameters
    ld iy,player_weapon_select_timer
    ld hl,0 ; zero timer means player can immediately select a different weapon
    ld a,200 ; DEBUG - this is too much ammo to start with
    ld (player_ammo),a
    call timer_set
    ret


player_next_weapon:
; check if select weapons timer has expired
    ld iy,player_weapon_select_timer
    call timer_get ; hl is time left in 120ths of a second, sign flag or zero flag set if expired
    ret p ; time left on timer so no weapon select
; reset weapon select timer
    ld hl,120/8 ; 1/6 second
    call timer_set
; select next weapon
    ld hl,player_weapons ; hl points to player_weapons flags
    ld bc,(hl) ; bc contains bitmask of player's weapons inventory
@loop:
    ld a,(player_weapon_active)
    rlca ; rotate left
    ld (player_weapon_active),a
    and (hl) ; check inventory mask
    jr z,@loop
    jp player_set_weapon_parameters
    
player_previous_weapon:
; check if select weapons timer has expired
    ld iy,player_weapon_select_timer
    call timer_get ; hl is time left in 120ths of a second, sign flag or zero flag set if expired
    ret p ; time left on timer so no weapon select
; reset weapon select timer
    ld hl,120/8 ; 1/8 second
    call timer_set
; select next weapon
    ld hl,player_weapons ; hl points to player_weapons flags
    ld bc,(hl) ; bc contains bitmask of player's weapons inventory
@loop:
    ld a,(player_weapon_active)
    rrca ; rotate right
    ld (player_weapon_active),a
    and (hl) ; check inventory mask
    jr z,@loop
    ; fall through to player_set_weapon_parameters

player_set_weapon_parameters:
    cp %00000001 ; knife
    jp z,@knife
    cp %00000010 ; pistol
    jp z,@pistol
    cp %00000100 ; machine gun
    jp z,@machine_gun
    cp %00001000 ; gatling gun
    jp z,@gatling_gun
    ret ; if none of the above do nothing
@knife:
    ld hl,BUF_UI_BJ_KNIFE_00
    ld (player_weapon_ui_buffer_id_large),hl
    ld hl,BUF_UI_LOWER_PANEL_KNIFE
    ld (player_weapon_ui_buffer_id_small),hl
    ld a,15 ; dps = 60
    ld (player_weapon_damage),a
    ld hl,120/4 ; 4 times/second
    ld (player_weapon_fire_rate),hl
    ld iy,player_weapon_fire_timer
    call timer_set
    ret
@pistol:
    ld hl,BUF_UI_BJ_PISTOL_00
    ld (player_weapon_ui_buffer_id_large),hl
    ld hl,BUF_UI_LOWER_PANEL_PISTOL
    ld (player_weapon_ui_buffer_id_small),hl
; 1 shots/burst, 3 bursts/sec, 30 dmg/burst, 90 dmg/sec, 30 dmg/shot
    ld a,30 ; damage/burst
    ld (player_weapon_damage),a
    ld hl,120/3 ; 3 bursts/second
    ld (player_weapon_fire_rate),hl
    ld iy,player_weapon_fire_timer
    call timer_set
    ret
@machine_gun:
    ld hl,BUF_UI_BJ_MACHINE_GUN_00
    ld (player_weapon_ui_buffer_id_large),hl
    ld hl,BUF_UI_LOWER_PANEL_MACHINE_GUN
    ld (player_weapon_ui_buffer_id_small),hl
; 4 shots/burst, 3 bursts/sec, 80 dmg/burst, 240 dmg/sec, 20 dmg/shot
    ld a,80 ; damage/burst
    ld (player_weapon_damage),a
    ld hl,40 ; 3 bursts/second
    ld (player_weapon_fire_rate),hl
    ld iy,player_weapon_fire_timer
    call timer_set
    ret
@gatling_gun:
    ld hl,BUF_UI_BJ_GATLING_00
    ld (player_weapon_ui_buffer_id_large),hl
    ld hl,BUF_UI_LOWER_PANEL_GATLING
    ld (player_weapon_ui_buffer_id_small),hl
; 8 shots/burst, 3 bursts/sec, 120 dmg/burst, 360 dmg/sec, 15 dmg/shot
    ld a,120 ; damage/burst
    ld (player_weapon_damage),a
    ld hl,40 ; 3 bursts/second
    ld (player_weapon_fire_rate),hl
    ld iy,player_weapon_fire_timer
    call timer_set
    ret

; modifies the players health by a set amount
; inputs: a is the signed amount to modify health
player_mod_health:
    ld hl,player_health
    add a,(hl)
    ld (hl),a
    ret

; modifies the players score by a set amount
; inputs: a is the signed amount to modify score
player_mod_score:
    ld hl,player_score
    add a,(hl)
    ld (hl),a
    ret

; modifies the players ammo by a set amount
; inputs: a is the signed amount to modify score
player_mod_ammo:
    ld hl,player_ammo
    add a,(hl)
    ld (hl),a
    ret

player_shoot_knife:
    ; check whether the player hit anything
    ld a,(orientation) ; direction knife is moving
    ld e,a
    ld d,1 ; shot "velocity" in map units
    call get_dx_dy ; d,e = dy,dx
    ld (player_shot_xvel),de ; implicity populates yvel
    ld hl,(cur_x) ; h,l = player y,x
    ld (player_shot_x),hl ; initial shot position
    ld de,(player_shot_xvel) ; d,e = shot yvel,xvel
    ld hl,(player_shot_x) ; h,l = player shot y,x
    ; bump bullet position one map unit in direction of travel
    ld a,l ; player shot x
    add a,e ; add xvel
    ld l,a ; save new x
    ld a,h ; player shot y
    add a,d ; add yvel
    ld h,a ; save new y
    ld (player_shot_x),hl ; and save that position
    ex de,hl ; d,e = bullet y,x
    call get_cell_from_coords ; ix = pointer to cell_status lut; a = obj_id, bc = cell_id
; check whether target cell contains a sprite
    ld a,(ix+map_sprite_id)
    cp 255 ; value if not sprite
    ret z ; if we hit a non-sprite, we're done
; is a sprite so run its "hurt" behavior routine
    call sprite_set_pointer
    ld a,sp_hurt
    call do_sprite_behavior ; a = sprite behavior return code
    ret

player_shoot_pistol:
    ld a,-1
    call player_mod_ammo
    call sfx_play_shot_pistol
    jp player_move_bullet

player_shoot_machine_gun:
    ld a,-4
    call player_mod_ammo
    call sfx_play_shot_machine_gun_burst
    jp player_move_bullet

player_shoot_gatling_gun:  
    ld a,-8
    call player_mod_ammo
    call sfx_play_shot_gatling_burst
    jp player_move_bullet

player_move_bullet:
    ; check whether the player hit anything
    ld a,(orientation) ; direction shot is moving
    ld (player_shot_status),a ; save shot direction -- indicates live shot in flight
    ld e,a
    ld d,1 ; shot "velocity" in map units
    call get_dx_dy ; d,e = dy,dx
    ld (player_shot_xvel),de ; implicity populates yvel
    ld hl,(cur_x) ; h,l = player y,x
    ld (player_shot_x),hl ; initial shot position
    ld b,view_distance ; loop counter so player can't shoot past view distance
@loop:
    push bc ; save loop counter
    ld de,(player_shot_xvel) ; d,e = shot yvel,xvel
    ld hl,(player_shot_x) ; h,l = player shot y,x
    ; bump bullet position one map unit in direction of travel
    ld a,l ; player shot x
    add a,e ; add xvel
    ld l,a ; save new x
    ld a,h ; player shot y
    add a,d ; add yvel
    ld h,a ; save new y
    ld (player_shot_x),hl ; and save that position
    ex de,hl ; d,e = bullet y,x
    call get_cell_from_coords ; ix = pointer to cell_status lut; a = obj_id, bc = cell_id
; check whether target cell contains a sprite
    ld a,(ix+map_sprite_id)
    cp 255 ; value if not sprite
    jr z,@not_sprite
; is a sprite so run its "hurt" behavior routine
    call sprite_set_pointer
    ld a,sp_hurt
    call do_sprite_behavior ; a = sprite behavior return code
    ld a,(player_shot_status)
    cp 255 ; value if shot hit a shootable sprite
    jr z,@stop_bullet ; if we hit a shootable sprite, we're done
    jr @move_bullet ; otherwise keep moving bullet
@not_sprite:
    ld de,(player_shot_xvel) ; restore yvel,xvel to d,e
; read map type/status mask from target cell
    ld a,(ix+map_type_status)
    and %00000011 ; mask off everything but the render type mask bits
; branch on the values in the bitmask
    cp render_type_floor
    jr z,@move_bullet ; keep going if map cell is a floor
@stop_bullet:
    pop bc ; dummy pop to balance stack
    ld a,255
    ld (player_shot_status),a ; set shot status to -1 to indicate shot is done
    ret ; combat ended
@move_bullet:
    pop bc ; restore loop counter
    djnz @loop ; keep moving bullet if we have more distance to cover
    ld a,255
    ld (player_shot_status),a ; set shot status to -1 to indicate shot is done
    ret ; combat ended

player_shoot:
; check if fire weapons timer has expired
    ld iy,player_weapon_fire_timer
    call timer_get ; hl is time left in 120ths of a second, sign flag or zero flag set if expired
    ret p ; timer not expired so don't fire weapon
; reset fire weapon timer
    ld iy,player_weapon_fire_timer ; DEBUG - we should not need this?
    ld hl,(player_weapon_fire_rate)
    call timer_set
; check animation frame for zero
    ld hl,player_weapon_animation_frame
    ld a,(hl)
    and a
    jr nz,@shoot ; if not zero, we're already in the middle of an animation
    inc (hl) ; is zero so bump to first animation frame
; set animation timer
    ld hl,player_weapon_animation_timer_reset
    ld iy,player_weapon_animation_timer
    call timer_set
@shoot:
; roll for damage modifier
    call rand_8 ; a is a bitmask we apply to the weapon's dmg/burst
    ld hl,player_weapon_damage
    and a,(hl) ; a contains modified damage value
    neg ; so we can add the negative
    ld (player_shot_damage),a ; pass shot damage to sprite hurt routine
; determine active weapon and shoot it
    ld a,(player_weapon_active) 
    cp player_weapon_pistol
    jp z,player_shoot_pistol
    cp player_weapon_machine_gun
    jp z,player_shoot_machine_gun
    cp player_weapon_gatling_gun
    jp z,player_shoot_gatling_gun
    cp player_weapon_knife
    jp z,player_shoot_knife
    ret

; process player keyboard input
; Inputs: player_x/y set at desired position
; Returns: player position updated
; Destroys: probably everything
player_input:
; check weapon anmation frame for zero
    ld a,(player_weapon_animation_frame)
    and 3 ; modulo 4
    ld (player_weapon_animation_frame),a
    jr z,@get_input
; animation frame is not zero so check animation timer
    ld iy,player_weapon_animation_timer
    call timer_get ; hl is time left in 120ths of a second, sign flag or zero flag set if expired
    jp p,@get_input ; time left on timer so no animation
; bump animation frame
    ld hl,player_weapon_animation_frame
    inc (hl) ; next frame
; reset animation timer
    ld iy,player_weapon_animation_timer ; DEBUG - we should not need this?
    ld hl,player_weapon_animation_timer_reset
    call timer_set

@get_input:
; reset player component velocities to zero as the default
    ld hl,0
    ld (xvel),hl ; implicitly sets yvel
    xor a ;
    ld (avel),a ; set player angular velocity to zero as default

; check for keypresses and branch accordingly
    MOSCALL	mos_getkbmap ;ix = pointer to MOS virtual keys table

; CHECK WEAPON CONTROL KEYS
; 58 Up player selects next weapon
    bit 1,(ix+7)
    jr z,@Up
    push ix ; it gets clobbered by the weapon select routine
    call player_next_weapon
    pop ix
@Up:

; 42 Down
    bit 1,(ix+5)
    jr z,@Down
    push ix ; it gets clobbered by the weapon select routine
    call player_previous_weapon
    pop ix
@Down:

; =====================
; 99 Space FIRE ZEE MISSILES!!!111
    bit 2,(ix+12)
    jr z,@Space
    push ix ; it gets clobbered by the weapon firing
    call player_shoot
    pop ix ; restore ix
@Space:

; CHECK MOVEMENT KEYS
; non-zero means no movement key was pressed
    ld a,-1

; 34 W player moves forward
    bit 1,(ix+4)
    jr z,@W
    ld a,speed_player ; this is *camera* relative, not map relative, so y-axis is NOT inverted!
    ld (yvel),a
    xor a
@W: 

; 82 S player moves backward
    bit 1,(ix+10)
    jr z,@S
    ld d,-speed_player ; this is *camera* relative, not map relative, so y-axis is NOT inverted!
    ld a,(yvel)
    add a,d
    ld (yvel),a
    xor a
@S:

; 66 A plyer moves left
    bit 1,(ix+8)
    jr z,@A
    ld a,-speed_player ; no funky axis conversion here
    ld (xvel),a
    xor a
@A:

; 51 D player moves right
    bit 2,(ix+6)
    jr z,@D
    ld d,speed_player ; no funky axis conversion here
    ld a,(xvel)
    add a,d
    ld (xvel),a
    xor a
@D:

; 26 Left player rotates anti-clockwise
    bit 1,(ix+3)
    jr z,@Left
    ld hl,avel
    dec (hl)
    xor a
@Left:

; 122 Right player rotates clockwise
    bit 1,(ix+15)
    jr z,@Right
    ld hl,avel
    inc (hl)
    xor a
@Right:

; KEYPRESS DETECTION DONE
    and a ; this will zero if player pressed a movement key
    ret nz ; non zero so no key pressed
; check move timer 
    ld iy,player_move_timer
    call timer_get ; hl is time left in 120ths of a second, sign flag or zero flag set if expired
    ret p ; time left on timer so no movement
; reset_move_timer
    ld hl,player_move_rate
    ld iy,player_move_timer; DEBUG - we should not need this?
    call timer_set
; move player according to velocities set by keypresses
    ld de,(xvel) ; d = yvel, e = xvel
    ld a,(avel)
    ld hl,orientation
    add a,(hl)
    and 0x03 ; modulo 4
    ld (hl),a
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
    ret