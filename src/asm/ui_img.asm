; Bitmap indices:
BUF_UI_BJ_025: equ 0x2000
BUF_UI_BJ_050: equ 0x2001
BUF_UI_BJ_075: equ 0x2002
BUF_UI_BJ_100: equ 0x2003
BUF_UI_BJ_120_120: equ 0x2004
BUF_UI_LOWER_PANEL: equ 0x2005
BUF_UI_LOWER_PANEL_GATLING: equ 0x2006
BUF_UI_LOWER_PANEL_KNIFE: equ 0x2007
BUF_UI_LOWER_PANEL_MACHINE_GUN: equ 0x2008
BUF_UI_LOWER_PANEL_PISTOL: equ 0x2009
BUF_UI_SPLASH: equ 0x200A

; Import .rgba2 bitmap files and load them into VDP buffers
load_ui_images:

	ld hl,F_UI_bj_025
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_025
	ld bc,32
	ld de,32
	ld ix,1024
	call vdu_load_img
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_bj_050
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_050
	ld bc,32
	ld de,32
	ld ix,1024
	call vdu_load_img
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_bj_075
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_075
	ld bc,32
	ld de,32
	ld ix,1024
	call vdu_load_img
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_bj_100
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_100
	ld bc,32
	ld de,32
	ld ix,1024
	call vdu_load_img
	LD A, '.'
	RST.LIL 10h

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
	LD A, '.'
	RST.LIL 10h

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
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_lower_panel_gatling
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_LOWER_PANEL_GATLING
	ld bc,40
	ld de,20
	ld ix,800
	call vdu_load_img
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_lower_panel_knife
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_LOWER_PANEL_KNIFE
	ld bc,40
	ld de,20
	ld ix,800
	call vdu_load_img
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_lower_panel_machine_gun
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_LOWER_PANEL_MACHINE_GUN
	ld bc,40
	ld de,20
	ld ix,800
	call vdu_load_img
	LD A, '.'
	RST.LIL 10h

	ld hl,F_UI_lower_panel_pistol
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_LOWER_PANEL_PISTOL
	ld bc,40
	ld de,20
	ld ix,800
	call vdu_load_img
	LD A, '.'
	RST.LIL 10h

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
	LD A, '.'
	RST.LIL 10h

	ret

F_UI_bj_025: db "ui/bj_025.rgba2",0
F_UI_bj_050: db "ui/bj_050.rgba2",0
F_UI_bj_075: db "ui/bj_075.rgba2",0
F_UI_bj_100: db "ui/bj_100.rgba2",0
F_UI_bj_120_120: db "ui/bj_120_120.rgba2",0
F_UI_lower_panel: db "ui/lower_panel.rgba2",0
F_UI_lower_panel_gatling: db "ui/lower_panel_gatling.rgba2",0
F_UI_lower_panel_knife: db "ui/lower_panel_knife.rgba2",0
F_UI_lower_panel_machine_gun: db "ui/lower_panel_machine_gun.rgba2",0
F_UI_lower_panel_pistol: db "ui/lower_panel_pistol.rgba2",0
F_UI_splash: db "ui/splash.rgba2",0
