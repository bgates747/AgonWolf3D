; inputs: bc is the number of sounds to load, cur_buffer_id_lut and cur_load_jump_table set to the address of the first entry in the respective lookup tables
sfx_load_main:
    ld hl,0
    ld (cur_file_idx),hl
sfx_load_main_loop:
; back up loop counter
    push bc
; load the next sound
    call load_next_sound
; draw all the things
    call tmp_draw_all_the_things
; move bj
	call move_bj
; print welcome message
	ld ix,font_itc_honda
	ld hl,hello_world
	ld bc,32
	ld de,2
	call font_bmp_print
; print current filename
	call vdu_cls
	ld hl,(cur_filename)
	call printString
	call printNewline
; flip screen 
    call vdu_flip 
; decrement loop counter
    pop bc
	dec bc
; ; DEBUG: DUMP REGISTERS
; 	push bc
; 	call dumpRegistersHex
; 	call vdu_flip
; 	pop bc
; ; END DEBUG
    ld a,c
    or a
    jp nz,sfx_load_main_loop
    ld a,b
    or a
    jp nz,sfx_load_main_loop
    ret

load_next_sound:
; look up the load routine for the current file index
	ld hl,(cur_file_idx) 
	add hl,hl ; multiply current index by 2 ...
	ld de,(cur_file_idx)
	add hl,de ; ... now by 3
	ld de,(cur_load_jump_table) ; tack it on to the base address of the jump table
	add hl,de 
	ld hl,(hl) ; hl is pointing to load routine address
	ld (@jump_addr+1),hl ; self-modifying code ...
@jump_addr:
	call 0 ; call the sound load routine
; look up the buffer id for the current file
	ld hl,(cur_file_idx) 
	add hl,hl ; multiply current index by 2 ...
	ld de,(cur_file_idx)
	add hl,de ; ... now by 3
	ld de,(cur_buffer_id_lut) ; tack it on to the base address of the lookup table
	add hl,de 
	ld hl,(hl)
	ld (cur_buffer_id),hl
; bump the current file index
	ld hl,(cur_file_idx)
	inc hl
	ld (cur_file_idx),hl
	ret

; load a sound file to a buffer
; inputs: hl = bufferId ; ix = file size
vdu_load_sfx:
; back up input parameters
    push hl ; bufferId
; load the sound
	call vdu_load_buffer_from_file
; now make the buffer a sound sample
    pop hl ; bufferId
	xor a ; zero is the magic number for 8-bit signed PCM 16KHz
    push hl ; bufferId
	call vdu_buffer_to_sound 
; play the loaded sound
    ld c,0 ; channel
    ld b,127 ; full volume
    ld de,1000 ; 1 second duration
    pop hl ; bufferId
    call vdu_play_sample
    ld a,%10000000 ; 1 second delay
    call multiPurposeDelay
    ret
