sfx_last_channel: db 0x00 ; 8-bit value between 0 and 31

; ; play a sound effect on the next available channel at full volume for its full duration
; ; inputs: hl = bufferId
; sfx_play:
; 	ld iy,sfx_last_channel
; 	ld a,(iy+0)
; 	ld (@bufferId),hl
; @find_next_channel:
; 	inc a ; bump to next channel
; 	and 31 ; modulo 32 channel
; 	cp (iy+0) ; if this is zero we've wrapped around and not found a free channel
; 	ret z ; so we return to caller without doing anything
; 	push af ; back up channel
; 	call vdu_channel_status ; a comes back with channel status bitmask
; 	and %00000010 ; bit 1 is the "is playing" flag
; 	jr z,@play_sfx ; if not playing, we can use this channel
; 	pop af ; restore channel
; 	jr @find_next_channel ; try the next channel
; @play_sfx:
; 	pop af ; restore channel
; 	ld (iy+0),a ; store channel
; 	ld hl,(@bufferId)
; 	ld c,a ; channel
; 	ld b,127 ; full volume
; 	ld de,1000 ; 1 second duration (should have no effect)
; 	jp vdu_play_sample 
; @bufferId:
; 	dw 0x0000 ; 16-bit value

; play a sound effect on the next available channel at full volume for its full duration
; inputs: hl = bufferId
sfx_play:
	ld iy,sfx_last_channel
	ld a,(iy+0)
	inc a ; bump to next channel
	and 31 ; modulo 32 channel
	ld (iy+0),a ; store channel
	ld c,a ; channel
	ld b,127 ; full volume
	ld de,1000 ; 1 second duration (should have no effect)
	jp vdu_play_sample 

sfx_play_got_treasure:
	ld hl,BUF_GOT_TREASURE
	jp sfx_play 

sfx_play_achtung:
	ld hl,BUF_ACHTUNG
	jp sfx_play 

sfx_play_schusstaffel:
	ld hl,BUF_SCHUSSTAFFEL
	jp sfx_play

sfx_play_dog_woof:
	ld hl,BUF_DOG_WOOF
	jp sfx_play 

sfx_play_dog_yelp:
	ld hl,BUF_DOG_YELP
	jp sfx_play 

sfx_play_mein_leben:
	ld hl,BUF_MEIN_LEBEN
	jp sfx_play 

sfx_play_wilhelm:
	ld hl,BUF_WILHELM
	jp sfx_play

sfx_play_shot_pistol:
	ld hl,BUF_SHOT_PISTOL
	jp sfx_play

sfx_play_shot_machine_gun_single:
	ld hl,BUF_SHOT_MACHINE_GUN_SINGLE
	jp sfx_play

sfx_play_shot_machine_gun_burst:
	ld hl,BUF_SHOT_MACHINE_GUN_BURST
	jp sfx_play

sfx_play_shot_gatling_single:
	ld hl,BUF_SHOT_GATLING_SINGLE
	jp sfx_play

sfx_play_shot_gatling_burst:
	ld hl,BUF_SHOT_GATLING_BURST
	jp sfx_play

sfx_play_explode:
	ld hl,BUF_EXPLODE
	jp sfx_play

sfx_play_ayee_high:
	ld hl,BUF_AYEE_HIGH
	jp sfx_play

sfx_play_ugh:
	ld hl,BUF_UGH
	jp sfx_play

sfx_play_ahh:
	ld hl,BUF_AHH
	jp sfx_play



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
; ; delay for a bit so sound can play
;     ld a,%10000000 ; 1 second delay
;     call multiPurposeDelay
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
    ; push hl ; bufferId
	call vdu_buffer_to_sound 
; ; play the loaded sound
;     ld c,0 ; channel
;     ld b,127 ; full volume
;     ld de,1000 ; 1 second duration
;     pop hl ; bufferId
;     call vdu_play_sample
    ret
