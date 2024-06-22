; macros, macro include files, globals and constants can go here
; but anything which will generate bytes must go below MOS initialization
    ; include "src/asm/agon_api/asm/macros.asm"

; MOS INITIALIATION MUST GO HERE BEFORE ANY OTHER CODE
    .assume adl=1   
    .org 0x040000    

    jp start       

    .align 64      
    .db "MOS"       
    .db 00h         
    .db 01h
; END OF MOS INITIALIZATION

; include files can go here
	include "src/asm/images.asm"
	include "src/asm/fonts_bmp.asm"
	include "src/asm/maps.asm"
	include "src/asm/render.asm"
	include "src/asm/polys.asm"
	include "src/asm/font_itc_honda.asm"
	include "src/asm/font_retro_computer.asm"
	include "src/asm/ui.asm"
	include "src/asm/ui_img.asm"
	include "src/asm/sprites.asm"
    include "src/asm/mos_api.asm"
	include "src/asm/vdu.asm"
    include "src/asm/functions.asm"
	include "src/asm/player.asm"
    include "src/asm/map00_0.asm"

start:              
    push af
    push bc
    push de
    push ix
    push iy

; ###############################################
; ez80asmLinker.py loader code goes here if used.
; ###############################################

; ###############################################
	call init ; Initialization code
    call main ; Call the main function
; ###############################################

exit:

    pop iy                              ; Pop all registers back from the stack
    pop ix
    pop de
    pop bc
    pop af
    ld hl,0                             ; Load the MOS API return code (0) for no errors.

    ret                                 ; Return MOS

hello_world: defb "Welcome to Agon Wolf3D",0
loading_panels: defb "Loading panels",0
loading_sprites: defb "Loading sprites",0
loading_dws: defb "Loading distance walls",0
loading_ui: defb "Loading UI",0

init:
; set the cursor off
	call cursor_off

; print loading ui message
	ld hl,loading_ui
	call printString

; load fonts
	call load_font_itc_honda
	call load_font_retro_computer

; load UI images
	call load_ui_images

; set up the display
    ld a,8 + 128
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
	
; clear the screen
	call vdu_cls
	call vdu_clg
	call vdu_flip

; initialization done
	ret

main:
; initialize player position
	call player_init
	
; render initial scene
	ld de,(cur_x) ; implicitly loads cur_y
	call get_cell_from_coords
	xor a ; north orientation
	ld (orientation),a
	call render_scene
	call vdu_flip

main_loop:
; move enemies
	; call move_enemies

; get player input and update sprite position
	call player_input ; ix points to cell defs/status, a is target cell current obj_id

; render the updated scene
	call render_scene
; flip the screen
	call vdu_flip
; wait for the next VBLANK
	call vdu_vblank

; check for escape key and quit if pressed
	MOSCALL mos_getkbmap
; 113 Escape
    bit 0,(ix+14)
    jr z,@Escape
	jr main_end
@Escape:

; do it again, Sam
    jr main_loop

main_end:
	; call do_outro
; restore screen to something normalish
	xor a
	call vdu_set_screen_mode
	call cursor_on
	ret


; img_load.asm must go here so that filedata doesn't stomp on program data
	include "src/asm/img_load.asm"