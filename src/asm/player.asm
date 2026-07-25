; set initial player position
; inputs: none,everything is hardcoded
; outputs: player set to the first valid position on the map
; destroys: a
plyr_init:
    call get_floor_start ; a = cell_id, d = map_y, e = map_x
    ld (cur_cell),a
    ld (cur_x),de ; implicitly populates cur_y
    xor a ; north is default orientation
    ld (orientation),a
    ld hl,plyr_move_rate
    ld iy,plyr_move_timer
    call timestamp_tmr_set
    ld a,3
    ld (plyr_lives),a
    ld a,100
    ld (plyr_health),a
    ld a,8
    ld (plyr_ammo),a
    ld a,plyr_wpn_knife 
    or plyr_wpn_pistol
    ld (plyr_wpns),a
    ld a,plyr_wpn_knife
    ld (plyr_wpn_active),a
    call plyr_set_weapon_parameters
    ld iy,plyr_wpn_select_tmr
    ld hl,0
    call timestamp_tmr_set
    ret

; restart player after dying
; inputs: none,everything is hardcoded
; outputs: player set to the first valid position on the map
; destroys: a
plyr_restart:
    ld a,(cur_room)
    and a
    jr z,@no_load
; not in room zero so save state of current room
    ld hl,room_flags
	ld de,0 ; make sure deu and d are zero
	ld e,a
	add hl,de ; hl = address of room flags entry
	ld a,room_flag_visited
	or (hl)
	ld (hl),a
; update from_room
	ld a,(cur_room)
	ld (from_room),a
; save old room state to room dat memory location
	ld hl,room_dat_lut
	ld d,a
	ld e,3 ; three bytes per lookup record
	mlt de ; de = offset to room dat entry
	add hl,de ; hl = address of room dat entry
	ld de,(hl) ; destination address for room data
	ld hl,cell_status ; source address for room data
	ld bc,8*1024 ; size of room data
	ldir
; fetch room zero state from room dat memory location
	ld hl,(room_00_dat) ; source address for room data
	ld de,cell_status ; destination address for room data
	ld bc,8*1024 ; size of room data
	ldir
@no_load:
    xor a
    ld (cur_room),a
    ld (orientation),a ; north is default orientation
    ld hl,plyr_move_rate
    ld iy,plyr_move_timer

    ld a,(plyr_lives)
    dec a
    ld (plyr_lives),a
    ld a,100
    ld (plyr_health),a
    ld a,8
    call plyr_add_ammo

    call get_floor_start ; a = cell_id, d = map_y, e = map_x
    ld (cur_cell),a
    ld (cur_x),de ; implicitly populates cur_y

    ret

plyr_next_weapon:
; check if select weapons timer has expired
    ld iy,plyr_wpn_select_tmr
    call timestamp_tmr_get ; hl is time left in 120ths of a second, sign flag or zero flag set if expired
    ret p ; time left on timer so no weapon select
; reset weapon select timer
    ld hl,120/6 ; 1/6 second
    call timestamp_tmr_set
; select next weapon
    ld hl,plyr_wpns ; hl points to plyr_wpns flags
    ld bc,(hl) ; bc contains bitmask of player's weapons inventory
@loop:
    ld a,(plyr_wpn_active)
    rlca ; rotate left
    ld (plyr_wpn_active),a
    and (hl) ; check inventory mask
    jr z,@loop
    jp plyr_set_weapon_parameters
    
plyr_previous_weapon:
; check if select weapons timer has expired
    ld iy,plyr_wpn_select_tmr
    call timestamp_tmr_get ; hl is time left in 120ths of a second, sign flag or zero flag set if expired
    ret p ; time left on timer so no weapon select
; reset weapon select timer
    ld hl,120/6 ; 1/6 second
    call timestamp_tmr_set
; select next weapon
    ld hl,plyr_wpns ; hl points to plyr_wpns flags
    ld bc,(hl) ; bc contains bitmask of player's weapons inventory
@loop:
    ld a,(plyr_wpn_active)
    rrca ; rotate right
    ld (plyr_wpn_active),a
    and (hl) ; check inventory mask
    jr z,@loop
    ; fall through to plyr_set_weapon_parameters

plyr_set_weapon_parameters:
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
    ld (plyr_wpn_ui_lg),hl
    ld hl,BUF_UI_LOWER_PANEL_KNIFE
    ld (plyr_wpn_ui_sm),hl
    ld a,20 ; dps = 60
    ld (plyr_wpn_damage),a
    ld hl,120/2 ; 3 times/second
    ld (plyr_wpn_fire_rate),hl
    ld iy,plyr_wpn_fire_tmr
    call timestamp_tmr_set
    ret
@pistol:
    ld hl,BUF_UI_BJ_PISTOL_00
    ld (plyr_wpn_ui_lg),hl
    ld hl,BUF_UI_LOWER_PANEL_PISTOL
    ld (plyr_wpn_ui_sm),hl
; 1 shots/burst, 3 bursts/sec, 30 dmg/burst, 90 dmg/sec, 30 dmg/shot
    ld a,30 ; damage/burst
    ld (plyr_wpn_damage),a
    ld hl,120/3 ; 3 bursts/second
    ld (plyr_wpn_fire_rate),hl
    ld iy,plyr_wpn_fire_tmr
    call timestamp_tmr_set
    ret
@machine_gun:
    ld hl,BUF_UI_BJ_MACHINE_GUN_00
    ld (plyr_wpn_ui_lg),hl
    ld hl,BUF_UI_LOWER_PANEL_MACHINE_GUN
    ld (plyr_wpn_ui_sm),hl
; 4 shots/burst, 3 bursts/sec, 80 dmg/burst, 240 dmg/sec, 20 dmg/shot
    ld a,80 ; damage/burst
    ld (plyr_wpn_damage),a
    ld hl,120/3 ; 3 bursts/second
    ld (plyr_wpn_fire_rate),hl
    ld iy,plyr_wpn_fire_tmr
    call timestamp_tmr_set
    ret
@gatling_gun:
    ld hl,BUF_UI_BJ_GATLING_00
    ld (plyr_wpn_ui_lg),hl
    ld hl,BUF_UI_LOWER_PANEL_GATLING
    ld (plyr_wpn_ui_sm),hl
; 8 shots/burst, 3 bursts/sec, 120 dmg/burst, 360 dmg/sec, 15 dmg/shot
    ld a,120 ; damage/burst
    ld (plyr_wpn_damage),a
    ld hl,120/3 ; 3 bursts/second
    ld (plyr_wpn_fire_rate),hl
    ld iy,plyr_wpn_fire_tmr
    call timestamp_tmr_set
    ret

; adds to player's health by a set amount
; inputs: a is the signed amount to modify health
; outputs: a will contain amount of health remaining
;          carry will be set if health maxes out to 255
plyr_add_health:
    ld hl,plyr_health
    add a,(hl)
    jp nc,@update ; if we roll over to zero when adding
    ld a,255 ; ... set health remaining to max
@update:
    ld (hl),a
    jp plyr_health_image

; subtracts from player's health by a set amount
; inputs: a is the signed amount to modify health
; outputs: zero flag set, carry reset if player health rolls through/becomes zero
;        a contains remaining health
plyr_sub_health:
    and a
    ret z
; DEBUG
    neg
    ld (last_damage),a
    neg
; END DEBUG
    ld hl,plyr_health
    add a,(hl)
    jp z,@zero
    jp c,@update
@zero:
    ld hl,BUF_UI_BJ_100
    ld (bj_health_image),hl
    jp plyr_restart ; will go the right place from there
@update:
    ld (hl),a
; fall through to plyr_health_image

plyr_health_image:
    cp 25
    jr c,@less_than_25
    cp 50
    jr c,@less_than_50
    cp 75
    jr c,@less_than_75
    ld hl,BUF_UI_BJ_100
    jr @update
@less_than_25:
    ld hl,BUF_UI_BJ_025
    jr @update
@less_than_50:
    ld hl,BUF_UI_BJ_050
    jr @update
@less_than_75:
    ld hl,BUF_UI_BJ_075
@update:
    ld (bj_health_image),hl
    ret

; modifies the players score by a set amount
; inputs: a is the signed amount to modify score
plyr_mod_score:
    ld de,0 ; make sure deu is zero
    ld e,a
    ld hl,(plyr_score)
    add hl,de
    ld (plyr_score),hl
    ret

; adds to player's ammo by a set amount
; inputs: a is the signed amount to modify ammo
; outputs: a will contain amount of ammo remaining
;          carry will be set if ammo maxes out to 255
plyr_add_ammo:
    ld hl,plyr_ammo
    add a,(hl)
    jp nc,@update ; if we roll over to zero when adding
    ld a,255 ; ... set ammo remaining to max
@update:
    ld (hl),a
    ret

; subtracts from player's ammo by a set amount
; inputs: a is the signed amount to modify ammo
; outputs: carry reset if player was out of ammo before firing
;          a will also contain amount of ammo remaining after shot
plyr_sub_ammo:
    ld hl,plyr_ammo
    add a,(hl)
    jp c,@update
    ld a,%00000001 ; knife
    ld (plyr_wpn_active),a
    call plyr_set_weapon_parameters
    xor a ; clear carry, set ammo to zero
    ld hl,plyr_ammo
@update:
    ld (hl),a
    ret

plyr_shoot_knife:
    call sfx_play_knife
    ; check whether the player hit anything
    ld a,(orientation) ; direction knife is moving
    ld e,a
    ld d,1 ; shot "velocity" in map units
    call get_dx_dy ; d,e = dy,dx
    ld (plyr_shot_xvel),de ; implicity populates yvel
    ld hl,(cur_x) ; h,l = player y,x
    ld (plyr_shot_x),hl ; initial shot position
    ld de,(plyr_shot_xvel) ; d,e = shot yvel,xvel
    ld hl,(plyr_shot_x) ; h,l = player shot y,x
    ; bump bullet position one map unit in direction of travel
    ld a,l ; player shot x
    add a,e ; add xvel
    ld l,a ; save new x
    ld a,h ; player shot y
    add a,d ; add yvel
    ld h,a ; save new y
    ld (plyr_shot_x),hl ; and save that position
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

plyr_shoot_pistol:
    ld a,-1
    call plyr_sub_ammo
    jp c,@shoot
    call sfx_play_gun_empty
    ret
@shoot:
    call sfx_play_shot_pistol
    jp plyr_move_bullet

plyr_shoot_machine_gun:
    ld a,-4
    call plyr_sub_ammo
    jp c,@shoot
    call sfx_play_gun_empty
    ret
@shoot:
    call sfx_play_shot_machine_gun_burst
    jp plyr_move_bullet

plyr_shoot_gatling_gun:  
    ld a,-8
    call plyr_sub_ammo
    jp c,@shoot
    call sfx_play_gun_empty
    ret
@shoot:
    call sfx_play_shot_gatling_burst
    jp plyr_move_bullet

plyr_move_bullet:
    ; check whether the player hit anything
    ld a,(orientation) ; direction shot is moving
    ld (plyr_shot_status),a ; save shot direction -- indicates live shot in flight
    ld e,a
    ld d,1 ; shot "velocity" in map units
    call get_dx_dy ; d,e = dy,dx
    ld (plyr_shot_xvel),de ; implicity populates yvel
    ld hl,(cur_x) ; h,l = player y,x
    ld (plyr_shot_x),hl ; initial shot position
    ld b,view_distance ; loop counter so player can't shoot past view distance
@loop:
    push bc ; save loop counter
    ld de,(plyr_shot_xvel) ; d,e = shot yvel,xvel
    ld hl,(plyr_shot_x) ; h,l = player shot y,x
    ; bump bullet position one map unit in direction of travel
    ld a,l ; player shot x
    add a,e ; add xvel
    ld l,a ; save new x
    ld a,h ; player shot y
    add a,d ; add yvel
    ld h,a ; save new y
    ld (plyr_shot_x),hl ; and save that position
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
    ld a,(plyr_shot_status)
    cp 255 ; value if shot hit a shootable sprite
    jr z,@stop_bullet ; if we hit a shootable sprite, we're done
    jr @move_bullet ; otherwise keep moving bullet
@not_sprite:
    ld de,(plyr_shot_xvel) ; restore yvel,xvel to d,e
; read map type/status mask from target cell
    ld a,(ix+map_type_status)
    and %00000011 ; mask off everything but the render type mask bits
; branch on the values in the bitmask
    cp render_type_floor
    jr z,@move_bullet ; keep going if map cell is a floor
@stop_bullet:
    pop bc ; dummy pop to balance stack
    ld a,255
    ld (plyr_shot_status),a ; set shot status to -1 to indicate shot is done
    ret ; combat ended
@move_bullet:
    pop bc ; restore loop counter
    djnz @loop ; keep moving bullet if we have more distance to cover
    ld a,255
    ld (plyr_shot_status),a ; set shot status to -1 to indicate shot is done
    ret ; combat ended

plyr_shoot:
; check if fire weapons timer has expired
    ld iy,plyr_wpn_fire_tmr
    call timestamp_tmr_get ; hl is time left in 120ths of a second, sign flag or zero flag set if expired
    jp z,@time_up ; timer zero so fire weapon
    jp m,@time_up ; timer negative so fire weapon
    ret ; timer not expired so don't fire weapon
@time_up:
; reset fire weapon timer
    ld iy,plyr_wpn_fire_tmr ; DEBUG - we should not need this?
    ld hl,(plyr_wpn_fire_rate)
    call timestamp_tmr_set
; check animation frame for zero
    ld hl,plyr_wpn_anim_fr
    ld a,(hl)
    and a
    jr nz,@shoot ; if not zero, we're already in the middle of an animation
    inc (hl) ; is zero so bump to first animation frame
@shoot:
; roll for damage modifier
    call rand_8 ; a is a bitmask we apply to the weapon's dmg/burst
    ld hl,plyr_wpn_damage
    and a,(hl) ; a contains modified damage value
    neg ; so we can add the negative
    ld (plyr_shot_damage),a ; pass shot damage to sprite hurt routine
; determine active weapon and shoot it
    ld a,(plyr_wpn_active) 
    cp plyr_wpn_pistol
    jp z,plyr_shoot_pistol
    cp plyr_wpn_mg
    jp z,plyr_shoot_machine_gun
    cp plyr_wpn_gg
    jp z,plyr_shoot_gatling_gun
    cp plyr_wpn_knife
    jp z,plyr_shoot_knife
    ret

; process player keyboard input
; Inputs: plyr_x/y set at desired position
; Returns: player position updated
; Destroys: probably everything
plyr_input:
; check weapon anmation frame for zero
    ld a,(plyr_wpn_anim_fr)
    and 3 ; modulo 4
    ld (plyr_wpn_anim_fr),a
    jr z,@get_input
; ; animation frame is not zero so check animation timer
;     ld iy,plyr_wpn_anim_tmr
;     call timestamp_tmr_get ; hl is time left in 120ths of a second, sign flag or zero flag set if expired
;     jp z,@animate ; timer zero so animate
;     jp m,@animate ; timer negative so animate
;     jp @get_input ; time left on timer so no animation
; bump animation frame
@animate:
    ld hl,plyr_wpn_anim_fr
    inc (hl) ; next frame
; ; reset animation timer
;     ld iy,plyr_wpn_anim_tmr ; DEBUG - we should not need this?
;     ld hl,(plyr_wpn_anim_tmr_rst)
;     call timestamp_tmr_set

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
    call plyr_next_weapon
    pop ix
@Up:

; 42 Down
    bit 1,(ix+5)
    jr z,@Down
    push ix ; it gets clobbered by the weapon select routine
    call plyr_previous_weapon
    pop ix
@Down:

; =====================
; 99 Space FIRE ZEE MISSILES!!!111
    bit 2,(ix+12)
    jr z,@Space
    push ix ; it gets clobbered by the weapon firing
    call plyr_shoot
    pop ix ; restore ix
@Space:

; CHECK MOVEMENT KEYS
; non-zero means no movement key was pressed
    ld a,-1

; 34 W player moves forward
    bit 1,(ix+4)
    jr z,@W
    ld a,speed_plyr ; this is *camera* relative, not map relative, so y-axis is NOT inverted!
    ld (yvel),a
    xor a
@W: 

; 82 S player moves backward
    bit 1,(ix+10)
    jr z,@S
    ld d,-speed_plyr ; this is *camera* relative, not map relative, so y-axis is NOT inverted!
    ld a,(yvel)
    add a,d
    ld (yvel),a
    xor a
@S:

; 66 A plyer moves left
    bit 1,(ix+8)
    jr z,@A
    ld a,-speed_plyr ; no funky axis conversion here
    ld (xvel),a
    xor a
@A:

; 51 D player moves right
    bit 2,(ix+6)
    jr z,@D
    ld d,speed_plyr ; no funky axis conversion here
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
    ld iy,plyr_move_timer
    call timestamp_tmr_get ; hl is time left in 120ths of a second, sign flag or zero flag set if expired
    ret p ; time left on timer so no movement
; reset_move_timer
    ld hl,plyr_move_rate
    ld iy,plyr_move_timer; DEBUG - we should not need this?
    call timestamp_tmr_set
; move player according to velocities set by keypresses
    ld de,(xvel) ; d = yvel, e = xvel
    ld a,(avel)
    ld hl,orientation
    add a,(hl)
    and 0x03 ; modulo 4
    ld (hl),a
    call trans_dx_dy ; d = dy, e = dx
    ld (dx),de
; if the player is standing on a room-transition cell, handle rotation or
; reversal before treating an adjacent cell as the ordinary movement target
    call room_transition_depart
    ret c ; transition-door state consumed this movement tick
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
    ld a,cell_is_wall
    and b
    ret nz ; can't move thru walls
    ld a,cell_is_to_room
    and b
    jp nz,change_room
    ; fall through to @move_it
@move_it:
; we are cleared for movement so update player position
    xor a
    ld (room_transition_active),a
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
