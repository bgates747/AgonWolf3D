; after this we can put includes in any order we wish, even in between
; code blocks if there is any program-dependent or asethetic reason to do so
	include "panels.inc"
	include "fonts.inc"
	include "maps.inc"
	include "render.inc"
	include "polys.inc"
	; include "files.inc" ; file handling and memory allocation for loading files from disk

hello_world: defb "Welcome to Agon Wolf3D!\n\r",0
loading_images: defb "Loading images...",0

init:
; ; set fonts
; 	ld hl,font_nurples
; 	ld b,144 ; loop counter for 96 chars
; 	ld a,32 ; first char to define (space)
; @loop:
; 	push bc
; 	push hl
; 	push af
; 	call vdu_define_character
; 	pop af
; 	inc a
; 	pop hl
; 	ld de,8
; 	add hl,de
; 	pop bc
; 	djnz @loop

; set up the display
    ld a,8
    call vdu_set_screen_mode
    xor a
    call vdu_set_scaling

; grab a bunch of sysvars and stuff
	call vdu_init

; set the cursor off
	call cursor_off

; print loading message
	ld hl,hello_world
	call printString
	ld hl,loading_images
	call printString

; load the bitmaps
	call load_panels

; clear the screen
	call vdu_cls
	call vdu_clg

; call main
	call main
	call cursor_on
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
vdu_load_bmp2_from_file:
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
@size:	dw 0x0000 ;width * height ; length of data in bytes

filedata: ; no need to allocate space for the bitmap data as we org the map data at 0x070000 just after this
