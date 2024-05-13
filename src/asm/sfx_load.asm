; This file is created by build_98_asm_sfx.py, do not edit it!

SFX_num_buffers: equ 16
; SFX buffer ids:
BUF_ACHTUNG: equ 0x3000
BUF_AHH: equ 0x3001
BUF_AUGH: equ 0x3002
BUF_AYEE: equ 0x3003
BUF_AYEE_HIGH: equ 0x3004
BUF_DOG_WOOF: equ 0x3005
BUF_DOG_YELP: equ 0x3006
BUF_EXPLODE: equ 0x3007
BUF_GOT_TREASURE: equ 0x3008
BUF_MEIN_LEBEN: equ 0x3009
BUF_SCHUSSTAFFEL: equ 0x300A
BUF_SHOT_GATLING_BURST: equ 0x300B
BUF_SHOT_MACHINE_GUN_BURST: equ 0x300C
BUF_SHOT_PISTOL: equ 0x300D
BUF_UGH: equ 0x300E
BUF_WILHELM: equ 0x300F

; SFX buffer id reverse lookup:
SFX_buffer_id_lut:
	dl BUF_ACHTUNG
	dl BUF_AHH
	dl BUF_AUGH
	dl BUF_AYEE
	dl BUF_AYEE_HIGH
	dl BUF_DOG_WOOF
	dl BUF_DOG_YELP
	dl BUF_EXPLODE
	dl BUF_GOT_TREASURE
	dl BUF_MEIN_LEBEN
	dl BUF_SCHUSSTAFFEL
	dl BUF_SHOT_GATLING_BURST
	dl BUF_SHOT_MACHINE_GUN_BURST
	dl BUF_SHOT_PISTOL
	dl BUF_UGH
	dl BUF_WILHELM

; SFX duration lookup:
SFX_duration_lut:
	dw 839 ; ACHTUNG
	dw 396 ; AHH
	dw 858 ; AUGH
	dw 540 ; AYEE
	dw 1119 ; AYEE_HIGH
	dw 774 ; DOG_WOOF
	dw 441 ; DOG_YELP
	dw 1247 ; EXPLODE
	dw 1574 ; GOT_TREASURE
	dw 876 ; MEIN_LEBEN
	dw 656 ; SCHUSSTAFFEL
	dw 333 ; SHOT_GATLING_BURST
	dw 360 ; SHOT_MACHINE_GUN_BURST
	dw 522 ; SHOT_PISTOL
	dw 363 ; UGH
	dw 1386 ; WILHELM

; SFX load routines jump table:
SFX_load_routines_table:
	dl load_sfx_ACHTUNG
	dl load_sfx_AHH
	dl load_sfx_AUGH
	dl load_sfx_AYEE
	dl load_sfx_AYEE_HIGH
	dl load_sfx_DOG_WOOF
	dl load_sfx_DOG_YELP
	dl load_sfx_EXPLODE
	dl load_sfx_GOT_TREASURE
	dl load_sfx_MEIN_LEBEN
	dl load_sfx_SCHUSSTAFFEL
	dl load_sfx_SHOT_GATLING_BURST
	dl load_sfx_SHOT_MACHINE_GUN_BURST
	dl load_sfx_SHOT_PISTOL
	dl load_sfx_UGH
	dl load_sfx_WILHELM

; Import sfx .raw files and load them into VDP buffers

load_sfx_ACHTUNG:
	ld hl,FACHTUNG
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_ACHTUNG
	ld ix,13430
	call vdu_load_sfx
	ret

load_sfx_AHH:
	ld hl,FAHH
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_AHH
	ld ix,6340
	call vdu_load_sfx
	ret

load_sfx_AUGH:
	ld hl,FAUGH
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_AUGH
	ld ix,13740
	call vdu_load_sfx
	ret

load_sfx_AYEE:
	ld hl,FAYEE
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_AYEE
	ld ix,8649
	call vdu_load_sfx
	ret

load_sfx_AYEE_HIGH:
	ld hl,FAYEE_HIGH
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_AYEE_HIGH
	ld ix,17904
	call vdu_load_sfx
	ret

load_sfx_DOG_WOOF:
	ld hl,FDOG_WOOF
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_DOG_WOOF
	ld ix,12393
	call vdu_load_sfx
	ret

load_sfx_DOG_YELP:
	ld hl,FDOG_YELP
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_DOG_YELP
	ld ix,7071
	call vdu_load_sfx
	ret

load_sfx_EXPLODE:
	ld hl,FEXPLODE
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_EXPLODE
	ld ix,19957
	call vdu_load_sfx
	ret

load_sfx_GOT_TREASURE:
	ld hl,FGOT_TREASURE
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_GOT_TREASURE
	ld ix,25198
	call vdu_load_sfx
	ret

load_sfx_MEIN_LEBEN:
	ld hl,FMEIN_LEBEN
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_MEIN_LEBEN
	ld ix,14025
	call vdu_load_sfx
	ret

load_sfx_SCHUSSTAFFEL:
	ld hl,FSCHUSSTAFFEL
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SCHUSSTAFFEL
	ld ix,10504
	call vdu_load_sfx
	ret

load_sfx_SHOT_GATLING_BURST:
	ld hl,FSHOT_GATLING_BURST
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SHOT_GATLING_BURST
	ld ix,5328
	call vdu_load_sfx
	ret

load_sfx_SHOT_MACHINE_GUN_BURST:
	ld hl,FSHOT_MACHINE_GUN_BURST
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SHOT_MACHINE_GUN_BURST
	ld ix,5760
	call vdu_load_sfx
	ret

load_sfx_SHOT_PISTOL:
	ld hl,FSHOT_PISTOL
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SHOT_PISTOL
	ld ix,8364
	call vdu_load_sfx
	ret

load_sfx_UGH:
	ld hl,FUGH
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UGH
	ld ix,5823
	call vdu_load_sfx
	ret

load_sfx_WILHELM:
	ld hl,FWILHELM
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_WILHELM
	ld ix,22183
	call vdu_load_sfx
	ret

; File name lookups:
FACHTUNG: db "sfx/ACHTUNG.raw",0
FAHH: db "sfx/AHH.raw",0
FAUGH: db "sfx/AUGH.raw",0
FAYEE: db "sfx/AYEE.raw",0
FAYEE_HIGH: db "sfx/AYEE_HIGH.raw",0
FDOG_WOOF: db "sfx/DOG_WOOF.raw",0
FDOG_YELP: db "sfx/DOG_YELP.raw",0
FEXPLODE: db "sfx/EXPLODE.raw",0
FGOT_TREASURE: db "sfx/GOT_TREASURE.raw",0
FMEIN_LEBEN: db "sfx/MEIN_LEBEN.raw",0
FSCHUSSTAFFEL: db "sfx/SCHUSSTAFFEL.raw",0
FSHOT_GATLING_BURST: db "sfx/SHOT_GATLING_BURST.raw",0
FSHOT_MACHINE_GUN_BURST: db "sfx/SHOT_MACHINE_GUN_BURST.raw",0
FSHOT_PISTOL: db "sfx/SHOT_PISTOL.raw",0
FUGH: db "sfx/UGH.raw",0
FWILHELM: db "sfx/WILHELM.raw",0
