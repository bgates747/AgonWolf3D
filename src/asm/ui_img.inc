; Bitmap indices:
BUF_UI_BJ_120_120: equ 0x2000
BUF_UI_BOX_ART: equ 0x2001
BUF_UI_LAVENDER: equ 0x2002
BUF_UI_LOWER_PANEL: equ 0x2003
BUF_UI_NURP_BG_CR: equ 0x2004
BUF_UI_NURP_LOG: equ 0x2005
BUF_UI_SPLASH: equ 0x2006

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
	call init_img_load
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_box_art
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BOX_ART
	ld bc,256
	ld de,240
	ld ix,61440
	call init_img_load
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_lavender
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_LAVENDER
	ld bc,320
	ld de,204
	ld ix,65280
	call init_img_load
	LD A, '.'
	RST.LIL 10h

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
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_nurp_bg_cr
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_NURP_BG_CR
	ld bc,320
	ld de,160
	ld ix,51200
	call init_img_load
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_nurp_log
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_NURP_LOG
	ld bc,305
	ld de,180
	ld ix,54900
	call init_img_load
	LD A, '.'
	RST.LIL 10h

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
	LD A, '.'
	RST.LIL 10h

	ret

F_UI_bj_120_120: db "ui/bj_120_120.rgba2",0
F_UI_box_art: db "ui/box_art.rgba2",0
F_UI_lavender: db "ui/lavender.rgba2",0
F_UI_lower_panel: db "ui/lower_panel.rgba2",0
F_UI_nurp_bg_cr: db "ui/nurp_bg_cr.rgba2",0
F_UI_nurp_log: db "ui/nurp_log.rgba2",0
F_UI_splash: db "ui/splash.rgba2",0
