; ###### SPRITE TABLE FIELD INDICES ######
sprite_id:              equ 00 ; 1 byte  - unique spriteId, zero-based
sprite_obj:             equ 01 ; 1 byte  - type of sprite as defined in polys.asm, 255 is dead
sprite_health:          equ 02 ; 1 byte  - health points, signed binary, zero or negative is dead
sprite_behavior_index:  equ 03 ; 1 byte  - index of sprite's behavior subroutine in enemies.asm
sprite_x:               equ 04 ; 1 byte  - map x position
sprite_y:               equ 05 ; 1 byte  - map y position
sprite_orientation:     equ 06 ; 1 byte  - orientation
sprite_animation:       equ 07 ; 1 byte  - current animation index, zero-based
sprite_animation_timer: equ 08 ; 1 byte  - when hits zero, draw next animation frame
sprite_move_timer:      equ 09 ; 1 byte  - when zero, go to next move program, or step
sprite_move_step:       equ 10 ; 1 byte  - stage in a move program sequence, varies
sprite_points:          equ 11 ; 1 byte  - points awarded for killing this sprite type, BCD
sprite_health_damage:   equ 12 ; 1 byte  - health points deducted per successful attack on player, signed binary (positive gains health)
sprite_unassigned:      equ 13 ; 3 bytes - unassigned can be used for custom properties
sprite_record_size: equ 16 ; 16 bytes per sprite record


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
;           ix pointing to new sprite vars, carry set
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

; set the active sprite record to no sprite and remove it from the map cell it was in
; inputs: iy pointed to sprite record
sprite_kill:
    ret

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
; inputs: iy = sprite_table_pointer to correct sprite record, sprite_obj set for that record
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
sp_shoot:  equ 2
sp_see:    equ 3
sp_kill:   equ 4

; calls the sprite behavior routine for the sprite pointed to by iy
; inputs: iy points to sprite record, sprite_obj set for that record, 
;         a = type index of routine to call
do_sprite_behavior:
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
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

BARREL:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db -20 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

TABLE:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

OVERHEAD_LIGHT:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

RADIOACTIVE_BARREL:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db -50;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

HEALTH_PACK:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 020 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    ld a,(iy+sprite_health_damage)
    call player_mod_health
    ld a,sp_kill
    call do_sprite_behavior
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

GOLD_CHALISE:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 100 ;sprite_points
    db 000 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

GOLD_CROSS:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 050 ;sprite_points
    db 000 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

PLATE_OF_FOOD:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 010 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    ld a,(iy+sprite_health_damage)
    call player_mod_health
    ld a,sp_kill
    call do_sprite_behavior
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

KEYCARD:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

GOLD_CHEST:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 250 ;sprite_points
    db 000 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

MACHINE_GUN:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

GATLING_GUN:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

DOG_FOOD:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 005 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    ld a,(iy+sprite_health_damage)
    call player_mod_health
    ld a,sp_kill
    call do_sprite_behavior
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

GOLD_KEY:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 000 ;sprite_points
    db 000 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

DOG:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 010 ;sprite_points
    db -10 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

GERMAN_TROOPER:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 020 ;sprite_points
    db -20 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return

SS_GUARD:
; behavior routine address lookup
    dl @init
    dl @use
    dl @shoot
    dl @see
    dl @kill
@init:
    ld hl,@data ; address for LDIR to copy from
    jp sprite_behavior_return
@data:
    db 100 ;sprite_health
    db 000 ;sprite_behavior_index
    db 000 ;sprite_x
    db 000 ;sprite_y
    db 000 ;sprite_orientation
    db 000 ;sprite_animation
    db 000 ;sprite_animation_timer
    db 000 ;sprite_move_timer
    db 000 ;sprite_move_step
    db 030 ;sprite_points
    db -30 ;sprite_health_damage
    db 000 ;sprite_unassigned_0
    db 000 ;sprite_unassigned_1
    db 000 ;sprite_unassigned_2
@use:
    jp sprite_behavior_return
@shoot:
    jp sprite_behavior_return
@see:
    jp sprite_behavior_return
@kill:
    call sprite_kill
    jp sprite_behavior_return