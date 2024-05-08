; Bitmap indices:
BUF_UI_BJ_GATLING_00: equ 0x2100
BUF_UI_BJ_GATLING_01: equ 0x2101
BUF_UI_BJ_GATLING_02: equ 0x2102
BUF_UI_BJ_GATLING_03: equ 0x2103
BUF_UI_BJ_GATLING_04: equ 0x2104
BUF_UI_BJ_KNIFE_00: equ 0x2105
BUF_UI_BJ_KNIFE_01: equ 0x2106
BUF_UI_BJ_KNIFE_02: equ 0x2107
BUF_UI_BJ_KNIFE_03: equ 0x2108
BUF_UI_BJ_KNIFE_04: equ 0x2109
BUF_UI_BJ_MACHINE_GUN_00: equ 0x210A
BUF_UI_BJ_MACHINE_GUN_01: equ 0x210B
BUF_UI_BJ_MACHINE_GUN_02: equ 0x210C
BUF_UI_BJ_MACHINE_GUN_03: equ 0x210D
BUF_UI_BJ_MACHINE_GUN_04: equ 0x210E
BUF_UI_BJ_PISTOL_00: equ 0x210F
BUF_UI_BJ_PISTOL_01: equ 0x2110
BUF_UI_BJ_PISTOL_02: equ 0x2111
BUF_UI_BJ_PISTOL_03: equ 0x2112
BUF_UI_BJ_PISTOL_04: equ 0x2113

; Import .rgba2 bitmap files and load them into VDP buffers
load_ui_images_bj:

	ld hl,F_UI_bj_gatling_00
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_GATLING_00
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_gatling_01
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_GATLING_01
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_gatling_02
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_GATLING_02
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_gatling_03
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_GATLING_03
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_gatling_04
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_GATLING_04
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_knife_00
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_KNIFE_00
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_knife_01
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_KNIFE_01
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_knife_02
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_KNIFE_02
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_knife_03
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_KNIFE_03
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_knife_04
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_KNIFE_04
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_machine_gun_00
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_MACHINE_GUN_00
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_machine_gun_01
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_MACHINE_GUN_01
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_machine_gun_02
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_MACHINE_GUN_02
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_machine_gun_03
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_MACHINE_GUN_03
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

	ld hl,F_UI_bj_machine_gun_04
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_BJ_MACHINE_GUN_04
	ld bc,64
	ld de,64
	ld ix,4096
	call vdu_load_img

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

F_UI_bj_gatling_00: db "ui/bj/bj_gatling_00.rgba2",0
F_UI_bj_gatling_01: db "ui/bj/bj_gatling_01.rgba2",0
F_UI_bj_gatling_02: db "ui/bj/bj_gatling_02.rgba2",0
F_UI_bj_gatling_03: db "ui/bj/bj_gatling_03.rgba2",0
F_UI_bj_gatling_04: db "ui/bj/bj_gatling_04.rgba2",0
F_UI_bj_knife_00: db "ui/bj/bj_knife_00.rgba2",0
F_UI_bj_knife_01: db "ui/bj/bj_knife_01.rgba2",0
F_UI_bj_knife_02: db "ui/bj/bj_knife_02.rgba2",0
F_UI_bj_knife_03: db "ui/bj/bj_knife_03.rgba2",0
F_UI_bj_knife_04: db "ui/bj/bj_knife_04.rgba2",0
F_UI_bj_machine_gun_00: db "ui/bj/bj_machine_gun_00.rgba2",0
F_UI_bj_machine_gun_01: db "ui/bj/bj_machine_gun_01.rgba2",0
F_UI_bj_machine_gun_02: db "ui/bj/bj_machine_gun_02.rgba2",0
F_UI_bj_machine_gun_03: db "ui/bj/bj_machine_gun_03.rgba2",0
F_UI_bj_machine_gun_04: db "ui/bj/bj_machine_gun_04.rgba2",0
F_UI_bj_pistol_00: db "ui/bj/bj_pistol_00.rgba2",0
F_UI_bj_pistol_01: db "ui/bj/bj_pistol_01.rgba2",0
F_UI_bj_pistol_02: db "ui/bj/bj_pistol_02.rgba2",0
F_UI_bj_pistol_03: db "ui/bj/bj_pistol_03.rgba2",0
F_UI_bj_pistol_04: db "ui/bj/bj_pistol_04.rgba2",0
