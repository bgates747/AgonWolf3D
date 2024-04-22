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
	; include "files.inc" ; file handling and memory allocation for loading files from disk

hello_world: defb "Welcome to Agon Wolf3D",0
loading_panels: defb "Loading panels",0
loading_sprites: defb "Loading sprites",0
loading_dws: defb "Loading distance walls",0
loading_ui: defb "Loading UI",0

init:
; print loading ui message
	ld hl,loading_ui
	call printString

; load fonts
	call load_font_itc_honda
	call load_font_retro_computer

; load UI images
	call load_ui_images

; set up the display
    ld a,8
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

; display the splash screen
	ld hl,BUF_UI_SPLASH
	call vdu_buff_select
	ld bc,0
	ld de,0
	call vdu_plot_bmp

; print loading message
	ld ix,font_itc_honda
	ld hl,hello_world
	ld bc,32
	ld de,2
	call font_bmp_print

; load panels
	ld hl,loading_panels
	call printString
	call load_panels

; load sprites
	call printNewline
	ld hl,loading_sprites
	call printString
	call load_sprites

; load distance walls
	call printNewline
	ld hl,loading_dws
	call printString
	call load_dws
	
; clear the screen
	call vdu_cls
	call vdu_clg

; initialization done
	ret

vdu_load_img:
; load the image
	call vdu_load_buffer_from_file
; print a progess breadcrumb
	LD A, '.'
	RST.LIL 10h
	ret

; WARNING: it may be tempting to move this routine to src/agon_api/vdp_buff.asm
; where it feels more in place, but for now it needs to live here because it depends on its location relative to the filedata: label just below, 
; and also since the agon_api includes live in the onboard 8kb SRAM, 
; there's no room for the up to 4 MB of bitmap data that is possible to load onto the VDP
; Credit to @HeathenUK for the original code that this is based on
; I had tried for literally days to make this work
; https://discord.com/channels/1158535358624039014/1158536809916149831/1208492884861653145
; load an rgba2222 bitmap to a 16-bit bufferId
; inputs: bc = width, de = height, hl = bufferId, ix = size
vdu_load_buffer_from_file:
		; load bitmap ids
		ld (@id0),hl
		ld (@id1),hl
		ld (@id2),hl
	; clean up bytes that got stomped on by the ID loads
		ld a,2
		ld (@id0+2),a
		ld a,23
		ld (@id1+2),a
		xor a
		ld (@id2+2),a
	; read size from ix
		push bc ; we need these later
		push de
		ld a,ixl
		ld (@size),a
		ld a,ixh
		ld (@size+1),a
	; get all the ducks in a row for the vdu call
		ld bc,filedata-@start
		add ix,bc
		ld b,ixh
		ld c,ixl
		ld hl,@start
	; push the button
		rst.lil $18
	; now make it a bitmap
		pop de
		pop bc
		ld a,1 ; the magic number for rgba2222
		jp vdu_bmp_create ; will return to caller from there
	; Clear buffer
@start: db 23,0,0xA0
@id0:	dw 0x0000 ; bufferId
		db 2
	; select buffer VDU 23, 27, &20, bufferId;
		db 23,27,0x20 
@id1:	dw 0x0000 ; bufferId
	; Upload data :: VDU 23, 0 &A0, bufferId; 0, length; <buffer-data>
		db 23,0,0xA0
@id2:	dw 0x0000 ; bufferId
		db 0 
		; CAUTION: the size argument is a 16-bit value, so the max number of bytes we can load in one chunk is 64KiB!! This corresponds to an rgba2 image size of 320x204.
@size:	dw 0x0000 ;width * height ; length of data in bytes
filedata: ; no need to allocate space for the bitmap data as we org the map data at 0x070000 just after this
