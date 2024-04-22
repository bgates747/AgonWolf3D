; ###### SPRITE TABLE FIELD INDICES ######
table_bytes_per_record: equ 38 ; 38 bytes per sprite record
sprite_id:              equ 00 ; 1 bytes unique spriteId, zero-based
sprite_type:            equ 01 ; 1 bytes type of sprite as defined in enemies.inc
sprite_base_bufferId:   equ 02 ; 3 bytes bitmap bufferId
sprite_move_program:    equ 05 ; 3 bytes address of sprite's behavior subroutine
sprite_collisions:      equ 08 ; 1 bytes low/high nibble: collision details
sprite_dim_x:           equ 09 ; 1 bytes sprite width in pixels
sprite_dim_y:           equ 10 ; 1 bytes sprite height in pixels
sprite_x:               equ 11 ; 3 bytes 16.8 fractional x position in pixels
sprite_y:               equ 14 ; 3 bytes 16.8 fractional y position in pixels
sprite_xvel:            equ 17 ; 3 bytes x-component velocity, 16.8 fixed, pixels
sprite_yvel:            equ 20 ; 3 bytes y-component velocity, 16.8 fixed, pixels
sprite_vel:             equ 23 ; 3 bytes velocity px/frame (16.8 fixed)
sprite_heading:         equ 26 ; 3 bytes sprite movement direction deg256 16.8 fixed
sprite_orientation:     equ 29 ; 3 bytes orientation bits
sprite_animation:       equ 32 ; 1 bytes current animation index, zero-based
sprite_animation_timer: equ 33 ; 1 bytes when hits zero, draw next animation
sprite_move_timer:      equ 34 ; 1 bytes when zero, go to next move program, or step
sprite_move_step:       equ 35 ; 1 bytes stage in a move program sequence, varies
sprite_points:          equ 36 ; 1 bytes points awarded for killing this sprite type, BCD
sprite_shield_damage:   equ 37 ; 1 bytes shield points deducted for collision, binary

; ###### SPRITE TABLE VARIABLES ######
; On-chip 8KB high-speed SRAM from 0xB7.E000 to 0xB7.FFFF.
; sprite table high address
table_base: equ 0xB7E000  
; maximum number of sprites
table_max_records: equ 4 ; it can handle more but this is pushing it
table_total_bytes: equ table_max_records*table_bytes_per_record

; #### THIS IS THE SPACE ALLOCATED TO THE SPRITE TABLE ####
sprite_start_variables: ds table_total_bytes, 0 ; fill with zeroes
sprite_end_variables: ; in case we want to traverse the table in reverse

; pointer to top address of current record, initialized to table_base
table_pointer: dl table_base
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
    ld ix,table_base
    ld de,table_bytes_per_record
    ld b,table_max_records
@loop:
    ld a,(ix+sprite_type)
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
    ld ix,table_base
    add ix,de
    xor a
    ld (ix+sprite_type),a
    ld ix,table_active_sprites
    dec (ix)
    ret