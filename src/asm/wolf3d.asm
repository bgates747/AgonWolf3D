    .assume adl=1   
    .org 0x040000    

    jp start       

    .align 64      
    .db "MOS"       
    .db 00h         
    .db 01h

	include "src/asm/images.asm"
	include "src/asm/fonts_bmp.asm"
	include "src/asm/maps.asm"
	include "src/asm/render.asm"
	include "src/asm/polys.asm"
	include "src/asm/font_itc_honda.asm"
	include "src/asm/font_retro_computer.asm"
	include "src/asm/ui.asm"
	include "src/asm/ui_img.asm"
	include "src/asm/ui_img_bj.asm"
	include "src/asm/sprites.asm"
    include "src/asm/mos_api.asm"
	include "src/asm/vdu.asm"
	include "src/asm/vdu_sound.asm"
    include "src/asm/functions.asm"
	include "src/asm/player.asm"
	include "src/asm/maths.asm"
	include "src/asm/img_load.asm"
	include "src/asm/sfx.asm"
	include "src/asm/timer.asm"


start:              
    push af
    push bc
    push de
    push ix
    push iy

	call init ; Initialization code
    call main ; Call the main function

exit:

    pop iy 
    pop ix
    pop de
    pop bc
    pop af
    ld hl,0

    ret 

hello_world: defb "Welcome to Agon Wolf3D",0
loading_ui: defb "Loading UI",0

init:
; initialize global timestamps
    MOSCALL mos_sysvars
    ld hl,(ix+sysvar_time)
    ld (timestamp_now),hl

; set the cursor off
	call cursor_off

; initialize PRT interrupt and calibrate timer
	ld hl,calibrating_timer
	call printString
	call prt_irq_init
	call prt_calibrate
	push de ; save number of PRT interrupts during test interval
	call printString
	call prt_set
	pop hl ; get number of PRT interrupts during test interval
	call printDec
	call printNewLine

; print loading ui message
	ld hl,loading_ui
	call printString

; load fonts
	call load_font_itc_honda
	call load_font_retro_computer

; load UI images
	call load_ui_images
	call load_ui_images_bj

; set up the display
    ld a,8+128 ; 320x240x64 double-buffered
    call vdu_set_screen_mode
    xor a
    call vdu_set_scaling

; set text background color
	ld a,4 + 128
	call vdu_colour_text

; set gfx bg color
	xor a ; plotting mode 0
	ld c,4 ; dark blue
	call vdu_gcol_bg
	call vdu_clg

; set the cursor off again since we changed screen modes
	call cursor_off

; VDU 28, left, bottom, right, top: Set text viewport **
; MIND THE LITTLE-ENDIANESS
; inputs: c=left,b=bottom,e=right,d=top
	ld c,0 ; left
	ld d,20 ; top
	ld e,39 ; right
	ld b,29; bottom
	call vdu_set_txt_viewport

; initialize image load routine
	call img_load_init

; load panels
	ld bc,cube_num_panels
	ld hl,cube_buffer_id_lut
	ld (cur_buffer_id_lut),hl
	ld hl,cube_load_panels_table
	ld (cur_load_jump_table),hl
	call img_load_main

; load sprites
	ld bc,sprite_num_panels
	ld hl,sprite_buffer_id_lut
	ld (cur_buffer_id_lut),hl
	ld hl,sprite_load_panels_table
	ld (cur_load_jump_table),hl
	call img_load_main

; load distance walls
	ld bc,dws_num_panels
	ld hl,dws_buffer_id_lut
	ld (cur_buffer_id_lut),hl
	ld hl,dws_load_panels_table
	ld (cur_load_jump_table),hl
	call img_load_main

; if running on hardware we don't load sounds and leave vdu_play_sfx disabled
	ld a,(is_emulator)
	and a
	ret z ; initialation done

; enable all the sound chanels
	call vdu_enable_channels

; load sound effects
	ld bc,SFX_num_buffers
	ld hl,SFX_buffer_id_lut
	ld (cur_buffer_id_lut),hl
	ld hl,SFX_load_routines_table
	ld (cur_load_jump_table),hl
	call sfx_load_main

; self modify vdu_play_sfx to enable sound
	xor a
	ld (vdu_play_sfx_disable),a

; initialization done
	ret

; DEBUG: set up a simple countdown timer
debug_timer: db 0x01

main_loop_tmr: ds 6
framerate: equ 30

main:
; set map variables and load initial map file
	call map_init
; initialize player position
	call plyr_init

main_loop:
; ; DEBUG: set up loop timer
;     call prt_loop_reset
; ; END DEBUG
; ; DEBUG: start loop timer
;     call prt_loop_start
; ; END DEBUG

; update timestamp
    call timestamp_tick

; move enemies
	call sprites_see_plyr ; 220-285  prt ticks

; get player input and update sprite position
	; 0-1 prt ticks
	call plyr_input ; ix points to cell defs/status, a is target cell current obj_id

; render the updated scene
	call render_scene ; 6-12 prt ticks
; full loop 12-16 prt ticks

; ; DEBUG: stop loop timer
;     call prt_loop_stop
; ; END DEBUG

; DEBUG: PRINT TIMER STUFF
    ld c,1 ; x
    ld b,8 ; y 
	call prt_loop_print
; END DEBUG

; flip the screen
	call vdu_flip

; DEBUG: set up loop timer
    call prt_loop_reset
; END DEBUG
; DEBUG: start loop timer
    call prt_loop_start
; END DEBUG
; wait for main loop timer to expire before contiuining
; 40-50 prt ticks at 60fps
; 100-120 prt ticks at 30fps
; 160-180 prt ticks at 20fps
; 210-230 prt ticks at 15fps
; 290-310 prt ticks at 12fps
; 340-360 prt ticks at 10fps
; 590-610 prt ticks at 6fps
; 710-730 prt ticks at 5fps
; 890-910 prt ticks at 4fps
; 1200-1230 prt ticks at 3fps
; 1820-1840 prt ticks at 2fps
; 3670-3690 prt ticks at 1fps

@wait:
	ld iy,main_loop_tmr
	call tmr_get
	jp z,@continue
	jp m,@continue
	jp @wait
@continue:
; DEBUG: stop loop timer
    call prt_loop_stop
; END DEBUG

; reset main loop timer
	ld iy,main_loop_tmr
	ld hl,120/framerate
	call tmr_set

; check for escape key and quit if pressed
	MOSCALL mos_getkbmap
; 113 Escape
    bit 0,(ix+14)
	jr nz,main_end
@Escape:
	jr main_loop

main_end:
	; call do_outro
; restore screen to something normalish
	xor a
	call vdu_set_screen_mode
	call cursor_on
	ret


; files.asm must go here so that filedata doesn't stomp on program data
	include "src/asm/files.asm"