; Bitmap indices:
BUF_UI_LOWER_PANEL: equ 0x2000
BUF_UI_SPLASH: equ 0x2001

; Import .rgba2 bitmap files and load them into VDP buffers
load_ui_images:

	ld hl,F_UI_lower_panel
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_LOWER_PANEL
	ld bc,320
	ld de,79
	ld ix,25280
	call init_img_load

	ld hl,F_UI_splash
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_SPLASH
	ld bc,320
	ld de,160
	ld ix,51200
	call init_img_load

	ret

F_UI_lower_panel: db "ui/lower_panel.rgba2",0
F_UI_splash: db "ui/splash.rgba2",0
