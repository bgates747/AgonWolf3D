cur_file_idx: dl 0
cur_filename: dl 0
cur_buffer_id: dl 0

img_load_init:
; ; prepare the screen

;     SET_MODE 8 ;+ 128 ; 320x240x64 double-buffered   

;     xor a
;     call vdu_set_scaling ; turn off screen scaling  

; ; VDU 28, left, bottom, right, top: Set text viewport **
; ; MIND THE LITTLE-ENDIANESS
; ; inputs: c=left,b=bottom,e=right,d=top
; 	ld c,0 ; left
; 	ld d,20 ; top
; 	ld e,39 ; right
; 	ld b,29; bottom
; 	call vdu_set_txt_viewport

; ; set the cursor off
; 	call cursor_off

; ; load the bitmaps
; 	call load_ui_images

; initialize bj's position parameters
	ld hl,0
	ld (bj_y_vel),hl

    ld hl,45
	ld (bj_y_cur),hl
	ld (bj_y_min),hl
    ld (bj_y_max),hl

	ld hl,1
	ld (bj_x_vel),hl

	ld hl,10
	ld (bj_x_cur),hl
	ld (bj_x_min),hl

	ld hl,320-120
	ld (bj_x_max),hl
	
; load the panels
    ld hl,0 ; make sure this is zero in case program was restarted
    ld (cur_file_idx),hl
    ld bc,num_panels
img_load_init_loop:
; back up loop counter
    push bc
; load the next panel
    call load_next_panel
; draw all the things
    call tmp_draw_all_the_things
; draw the most recently loaded panel
	ld hl,(cur_buffer_id)
	call vdu_buff_select
	ld bc,0
	ld de,0
	call vdu_plot_bmp
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
; flip screen and wait for next vblank
    call vdu_flip 
	; call WAIT_VBLANK 
; decrement loop counter
    pop bc
    ld a,c
    or a
    jp nz,img_load_init_loop
    ld a,b
    or a
    jp nz,img_load_init_loop
    ret

load_next_panel:
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
; bump the current file index
	ld hl,(cur_file_idx)
	inc hl
	ld (cur_file_idx),hl
	ret

move_bj:
; activate bj bitmap
	ld hl, BUF_UI_BJ_120_120
	call vdu_buff_select
; update position based on velocity parameters
	ld hl, (bj_x_cur)
	ld de, (bj_x_vel)
	add hl, de
	ld (bj_x_cur), hl
	ex de,hl ; store x_cur in de
; check if we're < x_min
	ld hl,(bj_x_min)
	xor a ; clear carry
	sbc hl,de ; x_min - x_cur
	jp p, move_bj_x_min
; check if we're > x_max
	ld hl,(bj_x_max)
	xor a ; clear carry
	sbc hl,de ; x_max - x_cur
	jp m, move_bj_x_max
; if not at either boundary, fall through to draw bj's
draw_bj:
	ld bc,(bj_x_cur)
	ld de,(bj_y_cur)
	call vdu_plot_bmp
	ret
move_bj_x_min:
	ld hl,1
	ld (bj_x_vel),hl
	ld hl,(bj_x_min)
	ld (bj_x_cur),hl
	jr draw_bj
move_bj_x_max:
	ld hl,-1
	ld (bj_x_vel),hl
	ld hl,(bj_x_max)
	ld (bj_x_cur),hl
	jr draw_bj
bj_x_vel: dl 0
bj_x_cur: dl 0
bj_x_min: dl 0
bj_x_max: dl 0

bj_y_vel: dl 0
bj_y_cur: dl 0
bj_y_min: dl 0
bj_y_max: dl 0

tmp_draw_all_the_things:
    ld hl,BUF_UI_SPLASH
    call vdu_buff_select
    ld bc,0
    ld de,0
    call vdu_plot_bmp
	ret

vdu_load_img:
; load the image
	call vdu_load_buffer_from_file
; ; print a progess breadcrumb
; 	LD A, '.'
; 	RST.LIL 10h
	ret

; WARNING: this routine must be the last one loaded in the main program so that filedata doesn't stomp on any program code
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
filedata: ; no need to allocate space here if this is the final include of the application