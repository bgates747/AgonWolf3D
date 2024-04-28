; ###### SPRITE TABLE FIELD INDICES ######
sprite_id:              equ 00 ; 1 byte  - unique spriteId, zero-based
sprite_obj:             equ 01 ; 1 byte  - type of sprite as defined in polys.asm, 255 is dead
sprite_health:          equ 02 ; 1 byte  - health points, signed binary, negative is dead
sprite_behavior_index:  equ 03 ; 1 byte  - index of sprite's behavior subroutine in enemies.asm
sprite_x:               equ 04 ; 1 byte  - map x position
sprite_y:               equ 05 ; 1 byte  - map y position
sprite_orientation:     equ 06 ; 1 byte  - orientation
sprite_animation:       equ 07 ; 1 byte  - current animation index, zero-based
sprite_animation_timer: equ 08 ; 1 byte  - when hits zero, draw next animation frame
sprite_move_timer:      equ 09 ; 1 byte  - when zero, go to next move program, or step
sprite_move_step:       equ 10 ; 1 byte  - stage in a move program sequence, varies
sprite_points:          equ 11 ; 1 byte  - points awarded for killing this sprite type, BCD
sprite_health_damage:   equ 12 ; 1 byte  - health points deducted per successful attack on player, signed binary (negative gains health)
sprite_unassigned:      equ 13 ; 3 bytes - unassigned can be used for custom properties
table_bytes_per_record: equ 16 ; 16 bytes per sprite record


; ###### SPRITE TABLE VARIABLES ######
; maximum number of sprites
table_max_records:      equ 64 ; at 16 bytes per record = 1024 bytes + 7 KiB for the map is an even 8 KiB
table_total_bytes:      equ table_max_records*table_bytes_per_record

; #### THIS DEFINES THE SPACE ALLOCATED TO THE SPRITE TABLE IN EACH MAP FILE ####
spite_table_base:       equ 0x081C00
spite_table_limit:      equ sprite_table_base + table_total_bytes ; in case we ever need to know where it ends

; pointer to top address of current record, initialized to spite_table_base
table_pointer: dl spite_table_base
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
    ld ix,spite_table_base
    ld de,table_bytes_per_record
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
    ld e,table_bytes_per_record
    mlt de
    ld ix,spite_table_base
    add ix,de
    xor a
    ld (ix+sprite_obj),a
    ld ix,table_active_sprites
    dec (ix)
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

LAMP:
    ret

BARREL:
    ret

TABLE:
    ret

OVERHEAD_LIGHT:
    ret

RADIOACTIVE_BARREL:
    ret

HEALTH_PACK:
    ret

GOLD_CHALISE:
    ret

GOLD_CROSS:
    ret

PLATE_OF_FOOD:
    ret

KEYCARD:
    ret

GOLD_CHEST:
    ret

MACHINE_GUN:
    ret

GATLING_GUN:
    ret

DOG_FOOD:
    ret

GOLD_KEY:
    ret

DOG:
    ret

GERMAN_TROOPER:
    ret

SS_GUARD:
    ret

; #### SPRITE INITIALIZATION SUBROUTINES ####
sprite_init_lookup:
    dl INIT_LAMP
    dl INIT_BARREL
    dl INIT_TABLE
    dl INIT_OVERHEAD_LIGHT
    dl INIT_RADIOACTIVE_BARREL
    dl INIT_HEALTH_PACK
    dl INIT_GOLD_CHALISE
    dl INIT_GOLD_CROSS
    dl INIT_PLATE_OF_FOOD
    dl INIT_KEYCARD
    dl INIT_GOLD_CHEST
    dl INIT_MACHINE_GUN
    dl INIT_GATLING_GUN
    dl INIT_DOG_FOOD
    dl INIT_GOLD_KEY
    dl INIT_DOG
    dl INIT_GERMAN_TROOPER
    dl INIT_SS_GUARD

INIT_LAMP:
    ret

INIT_BARREL:
    ret

INIT_TABLE:
    ret

INIT_OVERHEAD_LIGHT:
    ret

INIT_RADIOACTIVE_BARREL:
    ret

INIT_HEALTH_PACK:
    ret

INIT_GOLD_CHALISE:
    ret

INIT_GOLD_CROSS:
    ret

INIT_PLATE_OF_FOOD:
    ret

INIT_KEYCARD:
    ret

INIT_GOLD_CHEST:
    ret

INIT_MACHINE_GUN:
    ret

INIT_GATLING_GUN:
    ret

INIT_DOG_FOOD:
    ret

INIT_GOLD_KEY:
    ret

INIT_DOG:
    ret

INIT_GERMAN_TROOPER:
    ret

INIT_SS_GUARD:
    ret