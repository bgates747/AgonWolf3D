keycode_ptr:	dl	0
frame_ptr:		dl	0
vk_code:		dl	0
key_up:			dl	0

keycode:		db	0
vk:				db	0

c_up:			db	0
c_dn:			db	0
c_lf:			db	0
c_rt:			db	0

VK_U: 			equ 150
VK_D: 			equ 152
VK_L: 			equ 154
VK_R: 			equ 156

; ############# MY MODIFICATIONS / ADDITIONS #############
; flip the screen buffer so we can see what we just drew
; if working in a non-buffered screen mode (i.e. < 129)
; this won't do anything and can be excluded
vdu_flip_screen_buffer:
	ld hl,@cmd         
	ld bc,@end-@cmd    
	rst.lil $18         
	ret
@cmd:
; https://github.com/breakintoprogram/agon-docs/wiki/VDP
; VDU 23,0,&C3: Flip the screen buffer (double-buffered modes only)
	db 23,0,$C3
@end:

; https://github.com/breakintoprogram/agon-docs/wiki/VDP
; VDU 23, 7: Scrolling
;     VDU 23, 7, extent, direction, speed: Scroll the screen
; inputs: a, extent; l, direction; h; speed
vdu_scroll_down:
	ld (@extent),a
	ld (@dir),hl ; implicitly populates @speed
	ld hl,@cmd
	ld bc,@end-@cmd
	rst.lil $18     ;; Sending command to VDP
	ret
@cmd:       db 23,7
@extent:    db 0x00 ; 0 current text window, 1 entire screen, 2 curr gfx viewport
@dir:       db 0x00 ; 0 right, 1 left, 2 down, 3 up
@speed:     db 0x00 ; pixels
@end:		db 0x00 ; padding


; ####### ROKKY ORIGINAL STUFF BELOW, WITH SOME COMMENTARY BY ME

vdu_init:
; TODO: this is technically MOS stuff,and should live in mos_api.inc
; Get pointers to the MOS sysvars we'll be using,and stash
; their addresses as scratch variables in program space
	MOSCALL mos_sysvars 
	lea hl,ix+5
	ld (keycode_ptr),hl
	lea hl,ix+$17
	ld  (vk_code),hl
	lea hl,ix+$18
	ld (key_up),hl
	ld (frame_ptr),ix
; ; set up a string of VDP commands and send them
; 	ld hl,vdu_init_cmd
; 	ld bc,vdu_init_end-vdu_init_cmd
; 	rst.lil $18
	ret
; vdu_init_cmd: db 22 ; set screen mode
; vdu_init_mode: db 0 ; presently self-modified in _main at startup
; 	db 23,1,0 ; Hide cursor
; 	db 23,0,$88 ; set keyboard mode?
; 	dw 250,33 ; no idea
; 	db 255 ; stumped here as well
; 	; VDU 23, 0, &C0, n: Turn logical screen scaling on and off *
; 	db 23,0,0xC0,0 ; 0 IS OFF
; vdu_init_end:

vk_down:
	ld hl,(vk_code)
	ld a,(hl)

	ld hl,c_up
	cp VK_U
	jr z,@write

	inc hl
	cp VK_D
	jr z,@write
	
	inc hl
	cp VK_L
	jr z,@write

	inc hl
	cp VK_R
	jr z,@write
	ret
@write:
	ld a,1
	ld (hl),a
	ret

vk_up:
	ld hl,(vk_code)
	ld a,(hl)

	ld hl,c_up
	cp VK_U
	jr z,@write

	inc hl
	cp VK_D
	jr z,@write
	
	inc hl
	cp VK_L
	jr z,@write

	inc hl
	cp VK_R
	jr z,@write
	ret
@write:
	xor a
	ld (hl),a
	ret


get_key:
	xor a
	ld (keycode),a

	ld hl,(key_up)
	ld a,(hl)
	and a
	jr z,vk_up	

	call vk_down

	ld hl,(keycode_ptr)
	ld a,(hl)
	ld (keycode),a
	ret

vsync:
	ld hl,(frame_ptr)
	ld a,(hl)
@wait:	push af
	push hl
	call get_key
	pop hl
	pop af
	cp (hl)
	jr z,@wait
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

vdu_close:
	ld hl,@cmd
	ld bc,@end-@cmd
	rst.lil $18
	ret
@cmd:
	db 22,0
	db 17,7,17,$80
	db 23,1,1
	db 12
@end:


WAIT_VBLANK:		PUSH 	IX			; Wait for VBLANK interrupt
			MOSCALL	mos_sysvars		; Fetch pointer to system variables
			LD	A, (IX + sysvar_time + 0)
@wait:			CP 	A, (IX + sysvar_time + 0)
			JR	Z, @wait
			POP	IX
			RET