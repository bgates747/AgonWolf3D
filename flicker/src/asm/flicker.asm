; ###### macros go here ######
	macro MOSCALL arg1
	ld a, arg1
	rst.lil $08
	endmacro

	macro SET_MODE mode
	ld a, 22					; set mode...
	rst.lil $10
	ld a, mode					; to mode
	rst.lil $10
	endmacro

; ###### global constants can go here ######
mos_load:			EQU	01h
mos_sysvars:		EQU	08h
sysvar_time:		EQU	00h
mos_getkbmap:		EQU	1Eh

plot_bmp: equ 0xE8
dr_abs_fg: equ 5

; ###### NO CODE OR MEMORY ALLOCATIONS ABOVE THIS LINE ######
    .assume adl=1   
    .org 0x040000    

    jp start       

    .align 64      
    .db "MOS"       
    .db 00h         
    .db 01h  

; ###### includes can go here ######  
	include "src/asm/panels.inc"
	; include "src/asm/font_itc_honda.inc"
	; include "src/asm/font_retro_computer.inc"
	include "src/asm/ui_img.inc"

; ###### BEGINNING OF CODE ######
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

; ###############################################
; actual program code section
; ###############################################

main:
; prepare the screen

    SET_MODE 8 + 128 ; 320x240x64 double-buffered   

    xor a
    call vdu_set_scaling ; turn off screen scaling  

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

; load the bitmaps
	call load_ui_images
    call load_panels_init

; initialize the moving position parameters
	ld hl,0
	ld (box_y_vel),hl
	ld (box_y_cur),hl
	ld (box_y_min),hl

	ld hl,1
	ld (box_x_vel),hl
	ld hl,-120
	ld (box_x_cur),hl
	ld (box_x_min),hl

	ld hl,320
	ld (box_x_max),hl
	ld hl,240
	ld (box_y_max),hl

; initialize load timer 
	ld a,load_timer_reset
	ld (load_timer),a

main_loop:
; draw all the things
    call tmp_draw_all_the_things
; move moving
	call move_moving
; draw the most recently loaded panel
	ld hl,(cur_buffer_id)
	call vdu_buff_select
	ld bc,0
	ld de,0
	call vdu_plot_bmp
; print current filename
	call vdu_cls
	ld hl,(cur_filename)
	call printString
; flip screen and wait for next vblank
    call vdu_flip 
	call WAIT_VBLANK ;

; check for keypress
	MOSCALL	mos_getkbmap
; 113 Escape
    bit 0,(ix+14)
    jr z,@Escape
	jp 	EXIT_HERE
@Escape:
; load next bitmap if load time is zero and user presses space
	ld a,(load_timer)
	or a
	jr z,@is_space_pressed
	dec a
	ld (load_timer),a
	jr @Space
@is_space_pressed:
; 99 Space
    bit 2,(ix+12)
    jr z,@Space
	call load_next_panel
	ld a,load_timer_reset
	ld (load_timer),a
@Space:

; ESC not pressed so loop
    jr main_loop

EXIT_HERE:
    SET_MODE 0 ; 640x480x16 single-buffered
    call vdu_cls
    ret   

cur_file_idx: dl 0
cur_filename: dl 0
cur_buffer_id: dl 0
load_timer: db 0
load_timer_reset: equ 2

load_panels_init:
	ld b,25 ; initial load of 25 panels
	ld hl,load_panels_table ; base address of load panels jump table
@loop:
	push bc
	push hl
	ld hl,(hl)
	ld (@jump_addr+1),hl ; self-modifying code
@jump_addr:
	call 0 ; call the panel load routine
	pop hl
; bump pointer to next panel
	inc hl
	inc hl
	inc hl
	pop bc
	djnz @loop
	ld hl,25
	ld (cur_file_idx),hl
	ret

load_next_panel:
; bump the current file index
	ld hl,(cur_file_idx)
	inc hl
	ld (cur_file_idx),hl
; look up the load routine for the current file index
	ld hl,(cur_file_idx) 
	add hl,hl ; multiply current index by 2 ...
	ld de,(cur_file_idx)
	add hl,de ; ... now by 3
	ld de,load_panels_table ; tack it on to the base address of the jump table
	add hl,de 
	ld hl,(hl) ; hl is pointing to load routine address
	ld (@jump_addr+1),hl ; self-modifying code ...
@jump_addr:
	call 0 ; call the panel load routine
; look up the buffer id for the current file
	ld hl,(cur_file_idx) 
	add hl,hl ; multiply current index by 2 ...
	ld de,(cur_file_idx)
	add hl,de ; ... now by 3
	ld de,buffer_id_lut ; tack it on to the base address of the lookup table
	add hl,de 
	ld hl,(hl)
	ld (cur_buffer_id),hl
	ret

move_moving:
; activate moving bitmap
	ld hl, BUF_UI_BJ_120_120
	call vdu_buff_select
; update position based on velocity parameters
	ld hl, (box_x_cur)
	ld de, (box_x_vel)
	add hl, de
	ld (box_x_cur), hl
	ex de,hl ; store x_cur in de
; check if we're < x_min
	ld hl,(box_x_min)
	xor a ; clear carry
	sbc hl,de ; x_min - x_cur
	jp p, move_moving_x_min
; check if we're > x_max
	ld hl,(box_x_max)
	xor a ; clear carry
	sbc hl,de ; x_max - x_cur
	jp m, move_moving_x_max
; if not at either boundary, fall through to draw the moving
draw_moving:
	ld bc,(box_x_cur)
	ld de,(box_y_cur)
	call vdu_plot_bmp
	ret
move_moving_x_min:
	ld hl,1
	ld (box_x_vel),hl
	ld hl,(box_x_min)
	ld (box_x_cur),hl
	jr draw_moving
move_moving_x_max:
	ld hl,-1
	ld (box_x_vel),hl
	ld hl,(box_x_max)
	ld (box_x_cur),hl
	jr draw_moving
box_x_vel: dl 0
box_x_cur: dl 0
box_x_min: dl 0
box_x_max: dl 0

box_y_vel: dl 0
box_y_cur: dl 0
box_y_min: dl 0
box_y_max: dl 0

WAIT_VBLANK:		PUSH 	IX			; Wait for VBLANK interrupt
			MOSCALL	mos_sysvars		; Fetch pointer to system variables
			LD	A, (IX + sysvar_time + 0)
@wait:			CP 	A, (IX + sysvar_time + 0)
			JR	Z, @wait
			POP	IX
			RET

vdu_flip:       
	ld hl,@cmd         
	ld bc,@end-@cmd    
	rst.lil $18         
	ret
@cmd: db 23,0,0xC3
@end:

; VDU 23, 0, &C0, n: Turn logical screen scaling on and off *
; inputs: a is scaling mode, 1=on, 0=off
; note: default setting on boot is scaling ON
vdu_set_scaling:
	ld (@arg),a        
	ld hl,@cmd         
	ld bc,@end-@cmd    
	rst.lil $18         
	ret
@cmd: db 23,0,0xC0
@arg: db 0  ; scaling on/off
@end:

; VDU 12: Clear text area (CLS)
vdu_cls:
    ld a,12
	rst.lil $10  
	ret

; VDU 16: Clear graphics area (CLG)
vdu_clg:
    ld a,16
	rst.lil $10  
	ret

cursor_on:
	ld hl,@cmd
	ld bc,@end-@cmd
	rst.lil $18
	ret
@cmd:
	db 23,1,1
@end:

cursor_off:	
	ld hl,@cmd
	ld bc,@end-@cmd
	rst.lil $18
	ret
@cmd:
	db 23,1,0
@end:

; VDU 30: Home cursor
vdu_home_cursor:
    ld a,30
	rst.lil $10  
	ret

; VDU 28, left, bottom, right, top: Set text viewport **
; MIND THE LITTLE-ENDIANESS
; inputs: c=left,b=bottom,e=right,d=top
; outputs; nothing
; destroys: a might make it out alive
vdu_set_txt_viewport:
    ld (@lb),bc
	ld (@rt),de
	ld hl,@cmd
	ld bc,@end-@cmd
	rst.lil $18
	ret
@cmd:   db 28 ; set text viewport command
@lb: 	dw 0x0000 ; set by bc
@rt: 	dw 0x0000 ; set by de
@end:   db 0x00	  ; padding

; VDU 23, 27, &21, w; h; format: Create bitmap from selected buffer
; inputs: a=format; bc=width; de=height
; prerequisites: buffer selected by vdu_bmp_select or vdu_buff_select
; formats: https://agonconsole8.github.io/agon-docs/VDP---Bitmaps-API.html
; 0 	RGBA8888 (4-bytes per pixel)
; 1 	RGBA2222 (1-bytes per pixel)
; 2 	Mono/Mask (1-bit per pixel)
; 3 	Reserved for internal use by VDP (“native” format)
vdu_bmp_create:
    ld (@width),bc
    ld (@height),de
    ld (@fmt),a
	ld hl,@cmd
	ld bc,@end-@cmd
	rst.lil $18
	ret
@cmd:       db 23,27,0x21
@width:     dw 0x0000
@height:    dw 0x0000
@fmt:       db 0x00
@end:

; VDU 23, 27, &20, bufferId; : Select bitmap (using a buffer ID)
; inputs: hl=bufferId
vdu_buff_select:
	ld (@bufferId),hl
	ld hl,@cmd
	ld bc,@end-@cmd
	rst.lil $18
	ret
@cmd: db 23,27,0x20
@bufferId: dw 0x0000
@end: db 0x00 ; padding

; https://agonconsole8.github.io/agon-docs/VDP---PLOT-Commands.html
; &E8-&EF 	232-239 	Bitmap plot §
; VDU 25, mode, x; y;: PLOT command
; inputs: bc=x0, de=y0
; prerequisites: vdu_buff_select
vdu_plot_bmp:
    ld (@x0),bc
    ld (@y0),de
	ld hl,@cmd
	ld bc,@end-@cmd
	rst.lil $18
	ret
@cmd:   db 25
@mode:  db plot_bmp+dr_abs_fg ; 0xED
@x0: 	dw 0x0000
@y0: 	dw 0x0000
@end:   db 0x00 ; padding

tmp_draw_all_the_things:
	 ld hl,BUF_10_004
	 call vdu_buff_select
	 ld bc,0
	 ld de,62
	 call vdu_plot_bmp

	 ld hl,BUF_10_004
	 call vdu_buff_select
	 ld bc,35
	 ld de,62
	 call vdu_plot_bmp

	 ld hl,BUF_10_004
	 call vdu_buff_select
	 ld bc,71
	 ld de,62
	 call vdu_plot_bmp

	 ld hl,BUF_10_004
	 call vdu_buff_select
	 ld bc,106
	 ld de,62
	 call vdu_plot_bmp

	 ld hl,BUF_10_004
	 call vdu_buff_select
	 ld bc,142
	 ld de,62
	 call vdu_plot_bmp

	 ld hl,BUF_10_004
	 call vdu_buff_select
	 ld bc,177
	 ld de,62
	 call vdu_plot_bmp

	 ld hl,BUF_10_004
	 call vdu_buff_select
	 ld bc,213
	 ld de,62
	 call vdu_plot_bmp

	 ld hl,BUF_10_004
	 call vdu_buff_select
	 ld bc,248
	 ld de,62
	 call vdu_plot_bmp

	 ld hl,BUF_10_004
	 call vdu_buff_select
	 ld bc,284
	 ld de,62
	 call vdu_plot_bmp

	 ld hl,BUF_10_009
	 call vdu_buff_select
	 ld bc,0
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_010
	 call vdu_buff_select
	 ld bc,46
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_011
	 call vdu_buff_select
	 ld bc,91
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_012
	 call vdu_buff_select
	 ld bc,137
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_013
	 call vdu_buff_select
	 ld bc,177
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_014
	 call vdu_buff_select
	 ld bc,213
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_015
	 call vdu_buff_select
	 ld bc,248
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_016
	 call vdu_buff_select
	 ld bc,284
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_020
	 call vdu_buff_select
	 ld bc,0
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_020
	 call vdu_buff_select
	 ld bc,46
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_020
	 call vdu_buff_select
	 ld bc,91
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_020
	 call vdu_buff_select
	 ld bc,137
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_020
	 call vdu_buff_select
	 ld bc,182
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_020
	 call vdu_buff_select
	 ld bc,228
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_020
	 call vdu_buff_select
	 ld bc,273
	 ld de,57
	 call vdu_plot_bmp

	 ld hl,BUF_10_024
	 call vdu_buff_select
	 ld bc,0
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_025
	 call vdu_buff_select
	 ld bc,63
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_026
	 call vdu_buff_select
	 ld bc,128
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_027
	 call vdu_buff_select
	 ld bc,182
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_028
	 call vdu_buff_select
	 ld bc,228
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_029
	 call vdu_buff_select
	 ld bc,273
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_032
	 call vdu_buff_select
	 ld bc,0
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_032
	 call vdu_buff_select
	 ld bc,63
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_032
	 call vdu_buff_select
	 ld bc,128
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_032
	 call vdu_buff_select
	 ld bc,192
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_032
	 call vdu_buff_select
	 ld bc,256
	 ld de,48
	 call vdu_plot_bmp

	 ld hl,BUF_10_035
	 call vdu_buff_select
	 ld bc,0
	 ld de,26
	 call vdu_plot_bmp

	 ld hl,BUF_10_036
	 call vdu_buff_select
	 ld bc,106
	 ld de,26
	 call vdu_plot_bmp

	 ld hl,BUF_10_037
	 call vdu_buff_select
	 ld bc,192
	 ld de,26
	 call vdu_plot_bmp

	 ld hl,BUF_10_038
	 call vdu_buff_select
	 ld bc,256
	 ld de,26
	 call vdu_plot_bmp

	 ld hl,BUF_10_040
	 call vdu_buff_select
	 ld bc,0
	 ld de,26
	 call vdu_plot_bmp

	 ld hl,BUF_10_040
	 call vdu_buff_select
	 ld bc,106
	 ld de,26
	 call vdu_plot_bmp

	 ld hl,BUF_10_040
	 call vdu_buff_select
	 ld bc,213
	 ld de,26
	 call vdu_plot_bmp

	 ld hl,BUF_10_042
	 call vdu_buff_select
	 ld bc,0
	 ld de,0
	 call vdu_plot_bmp

	 ld hl,BUF_10_043
	 call vdu_buff_select
	 ld bc,213
	 ld de,0
	 call vdu_plot_bmp

	 ld hl,BUF_10_044
	 call vdu_buff_select
	 ld bc,0
	 ld de,0
	 call vdu_plot_bmp

	 ret

; Print a zero-terminated string
; HL: Pointer to string
printString:
	PUSH	BC
	LD		BC,0
	LD 	 	A,0
	RST.LIL 18h
	POP		BC
	RET

vdu_load_img:
	; load the image
	call vdu_load_buffer_from_file
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
		; ds 65536 ; 64KiB

