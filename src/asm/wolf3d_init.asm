; after this we can put includes in any order we wish, even in between
; code blocks if there is any program-dependent or asethetic reason to do so
	; include "panels.asm" ; replaced by images.asm
	include "images.asm"
	include "fonts_bmp.asm"
	include "maps.asm"
	include "render.asm"
	include "polys.asm"
	include "font_itc_honda.asm"
	include "font_retro_computer.asm"
	include "ui.asm"
	include "ui_img.asm"
	; include "files.asm" ; file handling and memory allocation for loading files from disk

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

; img_load.asm must go here so that filedata doesn't stomp on program data
	include "img_load.asm"