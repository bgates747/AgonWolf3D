; Bitmap indices:
BUF_UI_BJ_120_120: equ 0x2000
BUF_UI_LOWER_PANEL: equ 0x2001
BUF_UI_SPLASH: equ 0x2002

; Import .rgba2 bitmap files and load them into VDP buffers
load_ui_images:

	ld hl,F_UI_bj_120_120
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_120_120
	ld bc,120
	ld de,120
	ld ix,14400
	call vdu_load_img

	ld hl,F_UI_lower_panel
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_LOWER_PANEL
	ld bc,320
	ld de,80
	ld ix,25600
	call vdu_load_img

	ld hl,F_UI_splash
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_SPLASH
	ld bc,320
	ld de,160
	ld ix,51200
	call vdu_load_img

	ret

F_UI_bj_120_120: db "ui/bj_120_120.rgba2",0
F_UI_lower_panel: db "ui/lower_panel.rgba2",0
F_UI_splash: db "ui/splash.rgba2",0
