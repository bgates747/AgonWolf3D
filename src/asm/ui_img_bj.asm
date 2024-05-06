; Bitmap indices:
BUF_UI_BJ_PISTOL_00: equ 0x2100
BUF_UI_BJ_PISTOL_01: equ 0x2101
BUF_UI_BJ_PISTOL_02: equ 0x2102
BUF_UI_BJ_PISTOL_03: equ 0x2103
BUF_UI_BJ_PISTOL_04: equ 0x2104

; Import .rgba2 bitmap files and load them into VDP buffers
load_ui_images_bj:

	ld hl,F_UI_bj_pistol_00
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_PISTOL_00
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_pistol_01
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_PISTOL_01
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_pistol_02
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_PISTOL_02
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_pistol_03
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_PISTOL_03
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_pistol_04
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_PISTOL_04
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ret

F_UI_bj_pistol_00: db "ui/bj/bj_pistol_00.rgba2",0
F_UI_bj_pistol_01: db "ui/bj/bj_pistol_01.rgba2",0
F_UI_bj_pistol_02: db "ui/bj/bj_pistol_02.rgba2",0
F_UI_bj_pistol_03: db "ui/bj/bj_pistol_03.rgba2",0
F_UI_bj_pistol_04: db "ui/bj/bj_pistol_04.rgba2",0
