; Bitmap indices:
BUF_UI_BJ_120_120: equ 0x2000

; Import .rgba2 bitmap files and load them into VDP buffers
load_ui_images:

	ld hl,F_UI_bj_120_120
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_120_120
	ld bc,120
	ld de,120
	ld ix,14400
	call vdu_load_img

	ret

F_UI_bj_120_120: db "ui/bj_120_120.rgba2",0
