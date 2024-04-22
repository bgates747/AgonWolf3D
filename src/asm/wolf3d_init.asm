; after this we can put includes in any order we wish, even in between
; code blocks if there is any program-dependent or asethetic reason to do so
	include "panels.inc"
	include "fonts_bmp.inc"
	include "maps.inc"
	include "render.inc"
	include "polys.inc"
	include "font_itc_honda.inc"
	include "font_retro_computer.inc"
	include "ui.inc"
	include "ui_img.inc"

hello_world: defb "Welcome to Agon Wolf3D",0
loading_panels: defb "Loading panels",0
loading_sprites: defb "Loading sprites",0
loading_dws: defb "Loading distance walls",0
loading_ui: defb "Loading UI",0

init:
	; call img_load_init
	; ret

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

; set the cursor off
	call cursor_off

; ; display the splash screen
; 	ld hl,BUF_UI_SPLASH
; 	call vdu_buff_select
; 	ld bc,0
; 	ld de,0
; 	call vdu_plot_bmp

; ; print loading message
; 	ld ix,font_itc_honda
; 	ld hl,hello_world
; 	ld bc,32
; 	ld de,2
; 	call font_bmp_print

; ; load panels
; 	ld hl,loading_panels
; 	call printString
; 	call load_panels

; ; load sprites
; 	call printNewline
; 	ld hl,loading_sprites
; 	call printString
; 	call load_sprites

; ; load distance walls
; 	call printNewline
; 	ld hl,loading_dws
; 	call printString
; 	call load_dws

; load panels and sprites
	call img_load_init
	
; clear the screen
	call vdu_cls
	call vdu_clg

; initialization done
	ret

; #### this include must go here so that filedata doesn't stomp on program data ####
	include "img_load.asm"