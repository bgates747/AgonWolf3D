; ###### SPRITE TABLE FIELD INDICES ######
sprite_id:              equ 00 ; 1 byte  - unique spriteId, zero-based
sprite_obj:             equ 01 ; 1 byte  - type of sprite as defined in polys.asm, 255 is dead
sprite_health:          equ 02 ; 1 byte  - health points, signed binary, zero or negative is dead
sprite_triggers_mask:   equ 03 ; 1 byte  - bitmask for tracking which sprite behaviors have been triggered
sprite_x:               equ 04 ; 1 byte  - map x position
sprite_y:               equ 05 ; 1 byte  - map y position
sprite_orientation:     equ 06 ; 1 byte  - orientation
sprite_animation:       equ 07 ; 1 byte  - current animation index, zero-based
sprite_animation_timer: equ 08 ; 1 byte  - when hits zero, draw next animation frame
sprite_move_timer:      equ 09 ; 1 byte  - when zero, go to next move program, or step
sprite_move_step:       equ 10 ; 1 byte  - stage in a move program sequence, varies
sprite_points:          equ 11 ; 1 byte  - points awarded for killing this sprite type, BCD
sprite_health_modifier:   equ 12 ; 1 byte  - health points deducted per successful attack on player, signed binary (positive gains health)
sprite_unassigned:      equ 13 ; 3 bytes - unassigned can be used for custom properties
sprite_record_size: equ 16 ; 16 bytes per sprite record

; sprite_triggers_mask defs
sprite_trigger_see:     equ %00000001 ; player has been seen
sprite_trigger_use:     equ %00000010 ; player has used the sprite
sprite_trigger_hurt:    equ %00000100 ; player has hurt the sprite
sprite_trigger_kill:    equ %00001000 ; player has killed the sprite
sprite_trigger_move:    equ %00010000 ; sprite has moved
sprite_trigger_shoot:   equ %00100000 ; sprite has shot

; ###### SPRITE TABLE VARIABLES ######
; maximum number of sprites
table_max_records:      equ 64 ; at 16 bytes per record = 1024 bytes + 7 KiB for the map is an even 8 KiB
table_total_bytes:      equ table_max_records*sprite_record_size

; #### THIS DEFINES THE SPACE ALLOCATED TO THE SPRITE TABLE IN EACH MAP FILE ####
sprite_table_base:       equ 0xB7FC00
sprite_table_limit:      equ sprite_table_base + table_total_bytes + 1 ; in case we ever need to know where it ends

; pointer to top address of current record, initialized to sprite_table_base
sprite_table_pointer: dl sprite_table_base
; how many active sprites
table_active_sprites: db 0x00
; flag indicating collision with screen edge
; uses orientation codes to specify which edge(s)
sprite_screen_edge: db #00 
; next sprite id to use
sprite_next_id: db 0

; ######### COLLISION SPRITE PARAMETERS ##########
; integer coordinates are all that are needed for collision calculations
collision_x: db 0x00 
collision_y: db 0x00
collision_dim_x: db 0x00
collision_dim_y: db 0x00

; scratch variables
x: db 0x00 ; 8-bit signed integer
y: db 0x00 ; 8-bit signed integer
x0: dl 0x000000 ; 16.8 signed fixed place
y0: dl 0x000000 ; 16.8 signed fixed place
incx1: dl 0x000000 ; 16.8 signed fixed place
incy1: dl 0x000000 ; 16.8 signed fixed place
incx2: dl 0x000000 ; 16.8 signed fixed place
incy2: dl 0x000000 ; 16.8 signed fixed place

; sprite_heading: dl 0x000000 ; signed fixed 16.8 
radius: dl 0x000000 ; signed fixed 16.8 (but should always be positive)
sin_sprite_heading: dl 0x000000 ; signed fixed 16.8
cos_sprite_heading: dl 0x000000 ; signed fixed 16.8

; gets the next available sprite id
; inputs; none
; returns: if new sprite available, a = sprite id, 
;      ix pointing to new sprite vars, carry set
;      otherwise, a = 0, carry flag reset, ix pointing to highest sprite vars
; destroys: a,b,hl,ix
; affects: bumps table_active_sprites by one
table_get_next_id:
    ld ix,sprite_table_base
    ld de,sprite_record_size
    ld b,table_max_records
@loop:
    ld a,(ix+sprite_obj)
    and a
    jr z,@found
    add ix,de
    djnz @loop
@notfound:
    xor a ; a = 0 and reset carry flag indicating that we didn't find a free sprite
    ret
@found:
; bump number of active sprites
    ld hl,table_active_sprites
    inc (hl)
; return sprite id
    ld a,table_max_records
    sub b
    ld (sprite_next_id),a
    scf ; sets carry flag indicating we found a free sprite
    ret ; done

; deactivate the sprite with the given id
; inputs: a = sprite id
; outputs: nothing
; destroys: a,ix,de
; affects: decrements table_active_sprites by one
table_deactivate_sprite:
    push af ; save sprite id bc we need it later
    call vdu_sprite_select
    call vdu_sprite_hide
    pop af ; restore sprite id
    ld de,0 ; clear deu
    ld d,a
    ld e,sprite_record_size
    mlt de
    ld ix,sprite_table_base
    add ix,de
    xor a
    ld (ix+sprite_obj),a
    ld ix,table_active_sprites
    dec (ix)
    ret

; sets iy and sprite_table_pointer to the sprite record with the given id
; inputs: a = sprite id
; outputs: iy = sprite_table_pointer to the sprite record with the given id
; destroys: bc
sprite_set_pointer:
    ld b,a
    ld c,sprite_record_size
    mlt bc
    ld iy,sprite_table_base
    add iy,bc
    ld (sprite_table_pointer),iy
    ret

; set the active sprite record to no sprite and remove it from the map cell it was in
; inputs: iy pointed at sprite record to clear
sprite_kill:
; set sprite table record to no sprite
    ld hl,0xFFFFFF ; a string of -1s
    ld (iy),hl ; populates sprite_id, sprite_obj and sprite_heatlth with -1, all indicating that it is quite dead

; set map cell to no sprite and normal floor
    ld hl,0x1DFF01 ; normal floor TODO: we should set these values dyanmically based on the defs in tiles.txt at some point
    ld (ix),hl
    ld a,0xFF ; no sprite
    ld (ix+map_sprite_id),a ; now sprite is truly dead
    ret

sprite_new_x: db 0x00
sprite_new_y: db 0x00
              db 0x00 ; padding

; checks if the sprite can move to the new position
; inputs: iy pointed at sprite record, d,e = new y,x position
sprite_check_move:
    ld (sprite_new_x),de ; save new y,x position
    call get_cell_from_coords ; ix points to cell defs/status, a is target cell current obj_id, bc is cell_id
; check whether target cell contains a sprite
    ld a,(ix+map_sprite_id)
    cp 255 ; value if not sprite
    ret nz ; already occupied by another sprite so we can't move there
; read map type/status mask from target cell
    ld a,(ix+map_type_status)
    and render_type_floor
    ret z ; target cell is not a floor so we can't move there
; we are cleared for movement so fall through to sprite_move

; moves the sprite to the given map position
; inputs: iy pointed at sprite record, sprite_new_x/y populated
sprite_move:
; update old sprite position to no sprite
    ld de,(iy+sprite_x) ; d,e = sprite current y,x position
    call get_cell_from_coords ; ix points to cell defs/status, a is target cell current obj_id, bc is cell_id
; set map cell to no sprite and normal floor
    ld hl,0x1DFF01 ; normal floor TODO: we should set these values dyanmically based on the defs in tiles.txt at some point
    ld (ix),hl
    ld a,0xFF ; no sprite
    ld (ix+map_sprite_id),a
; update sprite record with new position
    ld de,(sprite_new_x) ; d,e = sprite new y,x position
    ld (iy+sprite_x),de
; update new map cell with sprite id
    call get_cell_from_coords ; ix points to cell defs/status, a is target cell current obj_id, bc is cell_id
    ld a,(iy+sprite_id)
    ld (ix+map_sprite_id),a
    ret

; move a sprite in a random direction
; inputs: iy pointed at sprite record
sprite_move_random:
; point iy at sprite record
    ld iy,(sprite_table_pointer)
; DEBUG:
    ; ld bc,(iy+sprite_x)
    ; push bc
; pick a random direction
    call rand_8
    and 3 ; direction between 0 and 3
; get dy,dx for moving once cell in the chosen direction
    ld e,a
    ld d,1 ; distance
    call get_dx_dy ; d,e = dy,dx
; calculate new position
    ld a,(iy+sprite_x)
    add a,e
    and 15 ; modulo 16
    ld e,a
    ld a,(iy+sprite_y)
    add a,d
    and 15 ; modulo 16
    ld d,a

    ; pop bc
    ; call stepRegistersHex
    jp sprite_check_move

; #### SPRITE BEHAVIOR SUBROUTINES ####
sprite_behavior_lookup:
    dl LAMP
    dl BARREL
    dl TABLE
    dl OVERHEAD_LIGHT
    dl RADIOACTIVE_BARREL
    dl HEALTH_PACK
    dl GOLD_CHALISE
    dl GOLD_CROSS
    dl PLATE_OF_FOOD
    dl KEYCARD
    dl GOLD_CHEST
    dl MACHINE_GUN
    dl GATLING_GUN
    dl DOG_FOOD
    dl GOLD_KEY
    dl DOG
    dl GERMAN_TROOPER
    dl SS_GUARD

; initializes sprite data for a particular sprite type and id
; inputs: iy pointed at sprite record, sprite_obj set for same 
sprite_init_data:
    ld a,sp_init ; index for sprite init routine
    call do_sprite_behavior ; hl points at address to copy from
    lea de,iy+sprite_health ; de points at the address for LDIR to copy to
    ld bc,sprite_record_size-2 ; copy all but the first two bytes
    ldir ; hl came back with the copy from address, so we're ready to copy the data
    ret ; done

; #### SPRITE BEHAVIOR ROUTINES ####
; sprite behavior indices
sp_init:   equ 0
sp_use:    equ 1
sp_hurt:  equ 2
sp_kill:   equ 3
sp_see:    equ 4
sp_move:  equ 5
sp_shoot:  equ 6

; calls the sprite behavior routine for the sprite pointed to by iy
; inputs: iy pointed at sprite record, sprite_obj set for same 
;         a = type index of routine to call
do_sprite_behavior:
    ld (sprite_table_pointer),iy ; save pointer to sprite record
    ld b,(iy+sprite_obj)
    ld c,3 ; three bytes per lookup record
    mlt bc ; bc is offset from the base of the lookup table
    ld hl,sprite_behavior_lookup
    add hl,bc
    ld hl,(hl) ; hl points to the base address of the sprite behavior routines
    ld b,a ; b holds the routine index
    ld c,3 ; three bytes per lookup record
    mlt bc ; bc is offset from the base of the lookup table
    add hl,bc ; hl points to the label of the routine to call
    ld hl,(hl) ; hl points to the routine to call
    jp (hl) ; call the behavior routine
sprite_behavior_return: ; we always return here from a sprite behavior call
    ret

LAMP:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

BARREL:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 018 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db -50 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@hurt:
    ld a,255 ; kill player's shot
    ld (player_shot_status),a
    ld a,(player_shot_damage) ; damage done by player's shot set by player_shoot
    add a,(iy+sprite_health)
    ld (iy+sprite_health),a
    jp p,sprite_behavior_return ; if health is positive, return
    ; otherwise fall through to kill sprite
@kill:
    push iy 
    call sfx_play_explode
    pop iy 
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

TABLE:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

OVERHEAD_LIGHT:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

RADIOACTIVE_BARREL:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 024 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db -75 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@hurt:
    ld a,255 ; kill player's shot
    ld (player_shot_status),a
    ld a,(player_shot_damage) ; damage done by player's shot set by player_shoot
    add a,(iy+sprite_health)
    ld (iy+sprite_health),a
    jp p,sprite_behavior_return ; if health is positive, return
    ; otherwise fall through to kill sprite
@kill:
    push iy 
    call sfx_play_explode
    pop iy
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

HEALTH_PACK:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 020 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    ld a,(iy+sprite_health_modifier)
    call player_mod_health
    jr @kill
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

GOLD_CHALISE:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 100 ;sprite_points
    db 000 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    push iy 
    call sfx_play_got_treasure
    pop iy 
    ld a,(iy+sprite_points)
    call player_mod_score
    jr @kill
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

GOLD_CROSS:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 050 ;sprite_points
    db 000 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    push iy 
    call sfx_play_got_treasure
    pop iy 
    ld a,(iy+sprite_points)
    call player_mod_score
    jr @kill
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

PLATE_OF_FOOD:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 010 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    ld a,(iy+sprite_health_modifier)
    call player_mod_health
    jr @kill
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

KEYCARD:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

GOLD_CHEST:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 250 ;sprite_points
    db 000 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    push iy 
    call sfx_play_got_treasure
    pop iy 
    ld a,(iy+sprite_points)
    call player_mod_score
    jr @kill
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

MACHINE_GUN:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

GATLING_GUN:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

DOG_FOOD:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 005 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    ld a,(iy+sprite_health_modifier)
    call player_mod_health
    jr @kill
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

GOLD_KEY:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@hurt:
    xor a
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@move:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

DOG:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 050 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 010 ;sprite_points
    db -10 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    push iy 
    call sfx_play_dog_woof
    pop iy 
    jp sprite_behavior_return
@hurt:
    call rand_8
    and %00000001
    jr nz,@nosound
    push iy 
    call sfx_play_dog_yelp
    pop iy 
@nosound:
    ld a,255 ; kill player's shot
    ld (player_shot_status),a
    ld a,(player_shot_damage) ; damage done by player's shot set by player_shoot
    add a,(iy+sprite_health)
    ld (iy+sprite_health),a
    jp p,sprite_behavior_return ; if health is positive, return
    ; otherwise fall through to kill sprite
@kill:
    push iy 
    call sfx_play_dog_yelp
    pop iy 
    call sprite_kill
    jp sprite_behavior_return
@see:
    ; fall through to @move
@move:
    dec (iy+sprite_move_timer)
    jr z,@do_move
    jp sprite_behavior_return
@do_move:
    call rand_8
    and %00111111 ; between 0 and 63
    ; or %00100000  ; at least 32
    or %00010000  ; at least 16
    ld (iy+sprite_move_timer),a
    call sprite_move_random
    call sfx_play_dog_woof
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

GERMAN_TROOPER:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 075 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 020 ;sprite_points
    db -20 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    push iy 
    call sfx_play_achtung
    pop iy 
    jp sprite_behavior_return
@hurt:
    call rand_8
    and %00000001
    jr nz,@nosound
    push iy 
    call sfx_play_random_hurt
    pop iy 
@nosound:
    ld a,255 ; kill player's shot
    ld (player_shot_status),a
    ld a,(player_shot_damage) ; damage done by player's shot set by player_shoot
    add a,(iy+sprite_health)
    ld (iy+sprite_health),a
    jp p,sprite_behavior_return ; if health is positive, return
    ; otherwise fall through to kill sprite
@kill:
    push iy 
    call sfx_play_wilhelm
    pop iy 
    call sprite_kill
    jp sprite_behavior_return
@see:
    ld a,(iy+sprite_triggers_mask)
    and sprite_trigger_see
    jp nz,@move
    ld a,sprite_trigger_see
    or a,(iy+sprite_triggers_mask)
    ld (iy+sprite_triggers_mask),a
    push iy 
    call sfx_play_achtung
    pop iy 
    jp sprite_behavior_return
@move:
    dec (iy+sprite_move_timer)
    jr z,@do_move
    jp sprite_behavior_return
@do_move:
    call rand_8
    and %00111111 ; between 0 and 63
    ; or %00100000  ; at least 32
    or %00010000  ; at least 16
    ld (iy+sprite_move_timer),a
    call sprite_move_random
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

SS_GUARD:
; behavior routine address lookup
    dl @init
    dl @use
    dl @hurt
    dl @kill
    dl @see
    dl @move
    dl @shoot
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_triggers_mask
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 001 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 030 ;sprite_points
    db -30 ;sprite_health_modifier
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    push iy 
    call sfx_play_schusstaffel
    pop iy 
    jp sprite_behavior_return
@hurt:
    call rand_8
    and %00000001
    jr nz,@nosound
    push iy 
    call sfx_play_random_hurt
    pop iy 
@nosound:
    ld a,255 ; kill player's shot
    ld (player_shot_status),a
    ld a,(player_shot_damage) ; damage done by player's shot set by player_shoot
    add a,(iy+sprite_health)
    ld (iy+sprite_health),a
    jp p,sprite_behavior_return ; if health is positive, return
    ; otherwise fall through to kill sprite
@kill:
    push iy 
    call sfx_play_mein_leben
    pop iy 
    call sprite_kill
    jp sprite_behavior_return
@see:
    ld a,(iy+sprite_triggers_mask)
    and sprite_trigger_see
    jp nz,@move
    ld a,sprite_trigger_see
    or a,(iy+sprite_triggers_mask)
    ld (iy+sprite_triggers_mask),a
    push iy 
    call sfx_play_schusstaffel
    pop iy 
    jp sprite_behavior_return
@move:
    dec (iy+sprite_move_timer)
    jr z,@do_move
    jp sprite_behavior_return
@do_move:
    call rand_8
    and %00111111 ; between 0 and 63
    ; or %00100000  ; at least 32
    or %00010000  ; at least 16
    ld (iy+sprite_move_timer),a
    call sprite_move_random
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return

see_orientation: db 0x00
; cycle through all cells visible to the player from the current position
; and all orientations, and trigger the @see behavior for any sprites in those cells
; inputs: cur_x, cur_y,
; outputs: player-aware enemies
; destroys: everything
sprites_see_player:
; intialize orientation
    xor a
    ld (see_orientation),a
@loop_orientation:
; get current map position and camera orientation
    ld de,(cur_x) ; d,e = cur_y,x
    call get_cell_from_coords ; ix=cell_status lut; a=obj_id, bc = cell_id
; get cell_views address for this cell and orientation
    ld a,(see_orientation)
    ld e,a
    ld d,6 ; 6 bytes per orientation
    mlt de ; de = orientation offset 
    ex de,hl ; hl = orientation offset
    ld b,24 ; 24 bytes per cell in cell_views lut
    mlt bc ; bc = offset from base address of cell_views lut
    add hl,bc ; hl = total offset from cell_views base address
    ex de,hl ; becaue we can't add iy to hl
    ld iy,cell_views ; base address of cell_views lut
    add iy,de ; iy = cell_views address
    ld (cur_cell_views),iy
; cycle through the cell views masks and trigger the @see behavior for any sprites in those cells
    ld bc,0x284600 ; bcu = jr z,nnn opcode, c = bit operand, b = displacement operand
    xor a ; poly_id
    ld (to_poly_id),a
@loop: 
    ld (@bit_iy+2),bc
    ld iy,(cur_cell_views)
@bit_iy:
    bit 0,(iy+0) ; the bit tested and offset will be self-modified through the loop
    jr z,@next_poly ; the first byte of this instruction is 0x28, and will be re-written as such each loop
; get_polys_deltas inputs: a is the orientation, c is the poly_id
    ld a,(to_poly_id)
    ld c,a ; poly_id
    ld a,(see_orientation)
    call get_polys_deltas ; d,e = y,x deltas
    ld a,(cur_x)
    add a,e
    ld e,a
    ld a,(cur_y)
    add a,d
    ld d,a
    call get_cell_from_coords
    ld a,(ix+map_sprite_id)
    cp 0xFF ; no sprite
    jr z,@next_poly
    call sprite_set_pointer
    ld a,sp_see
    call do_sprite_behavior
@next_poly:
    ld bc,(@bit_iy+2)
    ld a,(to_poly_id)
    inc a ; a is next poly_id
    ld (to_poly_id),a
    cp num_polys
    jr z,@next_orientation
    ld a,8
    add a,b
    ld b,a ; bit tested codes to 0x46 + b/8
    cp 0x86 ; = 0x7E + 8 where 0x7E is the highest bit possible (7)
    jr nz,@loop
    ld b,0x46
    inc c ; iy address offset 
    jr @loop
@next_orientation:
    ld a,(see_orientation)
    inc a
    ld (see_orientation),a
    jp nz,@loop_orientation
    ret