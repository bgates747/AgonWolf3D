; This file is created by build_98_asm_sfx.py, do not edit it!

SFX_num_buffers: equ 29
; SFX buffer ids:
BUF_ACHTUNG: equ 0x3000
BUF_ACHTUNG2: equ 0x3001
BUF_AHH: equ 0x3002
BUF_AUF_WEIDERSHEN: equ 0x3003
BUF_AUGH: equ 0x3004
BUF_AYEE: equ 0x3005
BUF_AYEE_HIGH: equ 0x3006
BUF_BANG2: equ 0x3007
BUF_DOG_WOOF: equ 0x3008
BUF_DOG_YELP: equ 0x3009
BUF_DOOR_SHUT: equ 0x300A
BUF_ENEMY_GATLING: equ 0x300B
BUF_EVA: equ 0x300C
BUF_EXPLODE: equ 0x300D
BUF_GIB: equ 0x300E
BUF_GOT_TREASURE: equ 0x300F
BUF_GUARD_SHOT_PISTOL: equ 0x3010
BUF_GUTEN_TAG: equ 0x3011
BUF_LOCKED_DOOR: equ 0x3012
BUF_MEIN_LEBEN: equ 0x3013
BUF_MUTTI: equ 0x3014
BUF_SCHUSSTAFFEL: equ 0x3015
BUF_SHOT_MACHINE_GUN: equ 0x3016
BUF_SHOT_MACHINE_GUN_SINGLE: equ 0x3017
BUF_SHOT_PISTOL: equ 0x3018
BUF_SPION: equ 0x3019
BUF_UGH: equ 0x301A
BUF_WILHELM: equ 0x301B
BUF_WOOF: equ 0x301C

; SFX buffer id reverse lookup:
SFX_buffer_id_lut:
	dl BUF_ACHTUNG
	dl BUF_ACHTUNG2
	dl BUF_AHH
	dl BUF_AUF_WEIDERSHEN
	dl BUF_AUGH
	dl BUF_AYEE
	dl BUF_AYEE_HIGH
	dl BUF_BANG2
	dl BUF_DOG_WOOF
	dl BUF_DOG_YELP
	dl BUF_DOOR_SHUT
	dl BUF_ENEMY_GATLING
	dl BUF_EVA
	dl BUF_EXPLODE
	dl BUF_GIB
	dl BUF_GOT_TREASURE
	dl BUF_GUARD_SHOT_PISTOL
	dl BUF_GUTEN_TAG
	dl BUF_LOCKED_DOOR
	dl BUF_MEIN_LEBEN
	dl BUF_MUTTI
	dl BUF_SCHUSSTAFFEL
	dl BUF_SHOT_MACHINE_GUN
	dl BUF_SHOT_MACHINE_GUN_SINGLE
	dl BUF_SHOT_PISTOL
	dl BUF_SPION
	dl BUF_UGH
	dl BUF_WILHELM
	dl BUF_WOOF

; SFX duration lookup:
SFX_duration_lut:
	dw 839 ; ACHTUNG
	dw 822 ; ACHTUNG2
	dw 396 ; AHH
	dw 1168 ; AUF_WEIDERSHEN
	dw 858 ; AUGH
	dw 540 ; AYEE
	dw 1119 ; AYEE_HIGH
	dw 646 ; BANG2
	dw 774 ; DOG_WOOF
	dw 441 ; DOG_YELP
	dw 491 ; DOOR_SHUT
	dw 1500 ; ENEMY_GATLING
	dw 869 ; EVA
	dw 1247 ; EXPLODE
	dw 1361 ; GIB
	dw 1574 ; GOT_TREASURE
	dw 1223 ; GUARD_SHOT_PISTOL
	dw 928 ; GUTEN_TAG
	dw 522 ; LOCKED_DOOR
	dw 876 ; MEIN_LEBEN
	dw 897 ; MUTTI
	dw 656 ; SCHUSSTAFFEL
	dw 843 ; SHOT_MACHINE_GUN
	dw 547 ; SHOT_MACHINE_GUN_SINGLE
	dw 522 ; SHOT_PISTOL
	dw 774 ; SPION
	dw 363 ; UGH
	dw 1386 ; WILHELM
	dw 590 ; WOOF

; SFX load routines jump table:
SFX_load_routines_table:
	dl load_sfx_ACHTUNG
	dl load_sfx_ACHTUNG2
	dl load_sfx_AHH
	dl load_sfx_AUF_WEIDERSHEN
	dl load_sfx_AUGH
	dl load_sfx_AYEE
	dl load_sfx_AYEE_HIGH
	dl load_sfx_BANG2
	dl load_sfx_DOG_WOOF
	dl load_sfx_DOG_YELP
	dl load_sfx_DOOR_SHUT
	dl load_sfx_ENEMY_GATLING
	dl load_sfx_EVA
	dl load_sfx_EXPLODE
	dl load_sfx_GIB
	dl load_sfx_GOT_TREASURE
	dl load_sfx_GUARD_SHOT_PISTOL
	dl load_sfx_GUTEN_TAG
	dl load_sfx_LOCKED_DOOR
	dl load_sfx_MEIN_LEBEN
	dl load_sfx_MUTTI
	dl load_sfx_SCHUSSTAFFEL
	dl load_sfx_SHOT_MACHINE_GUN
	dl load_sfx_SHOT_MACHINE_GUN_SINGLE
	dl load_sfx_SHOT_PISTOL
	dl load_sfx_SPION
	dl load_sfx_UGH
	dl load_sfx_WILHELM
	dl load_sfx_WOOF

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

load_sfx_ACHTUNG2:
	ld hl,FACHTUNG2
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_ACHTUNG2
	ld ix,13152
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

load_sfx_AUF_WEIDERSHEN:
	ld hl,FAUF_WEIDERSHEN
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_AUF_WEIDERSHEN
	ld ix,18689
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

load_sfx_BANG2:
	ld hl,FBANG2
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_BANG2
	ld ix,10348
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

load_sfx_DOOR_SHUT:
	ld hl,FDOOR_SHUT
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_DOOR_SHUT
	ld ix,7857
	call vdu_load_sfx
	ret

load_sfx_ENEMY_GATLING:
	ld hl,FENEMY_GATLING
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_ENEMY_GATLING
	ld ix,24003
	call vdu_load_sfx
	ret

load_sfx_EVA:
	ld hl,FEVA
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_EVA
	ld ix,13911
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

load_sfx_GIB:
	ld hl,FGIB
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_GIB
	ld ix,21782
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

load_sfx_GUARD_SHOT_PISTOL:
	ld hl,FGUARD_SHOT_PISTOL
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_GUARD_SHOT_PISTOL
	ld ix,19577
	call vdu_load_sfx
	ret

load_sfx_GUTEN_TAG:
	ld hl,FGUTEN_TAG
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_GUTEN_TAG
	ld ix,14861
	call vdu_load_sfx
	ret

load_sfx_LOCKED_DOOR:
	ld hl,FLOCKED_DOOR
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_LOCKED_DOOR
	ld ix,8364
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

load_sfx_MUTTI:
	ld hl,FMUTTI
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_MUTTI
	ld ix,14355
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

load_sfx_SHOT_MACHINE_GUN:
	ld hl,FSHOT_MACHINE_GUN
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SHOT_MACHINE_GUN
	ld ix,13499
	call vdu_load_sfx
	ret

load_sfx_SHOT_MACHINE_GUN_SINGLE:
	ld hl,FSHOT_MACHINE_GUN_SINGLE
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SHOT_MACHINE_GUN_SINGLE
	ld ix,8753
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

load_sfx_SPION:
	ld hl,FSPION
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SPION
	ld ix,12392
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

load_sfx_WOOF:
	ld hl,FWOOF
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_WOOF
	ld ix,9453
	call vdu_load_sfx
	ret

; File name lookups:
FACHTUNG: db "sfx/ACHTUNG.raw",0
FACHTUNG2: db "sfx/ACHTUNG2.raw",0
FAHH: db "sfx/AHH.raw",0
FAUF_WEIDERSHEN: db "sfx/AUF_WEIDERSHEN.raw",0
FAUGH: db "sfx/AUGH.raw",0
FAYEE: db "sfx/AYEE.raw",0
FAYEE_HIGH: db "sfx/AYEE_HIGH.raw",0
FBANG2: db "sfx/BANG2.raw",0
FDOG_WOOF: db "sfx/DOG_WOOF.raw",0
FDOG_YELP: db "sfx/DOG_YELP.raw",0
FDOOR_SHUT: db "sfx/DOOR_SHUT.raw",0
FENEMY_GATLING: db "sfx/ENEMY_GATLING.raw",0
FEVA: db "sfx/EVA.raw",0
FEXPLODE: db "sfx/EXPLODE.raw",0
FGIB: db "sfx/GIB.raw",0
FGOT_TREASURE: db "sfx/GOT_TREASURE.raw",0
FGUARD_SHOT_PISTOL: db "sfx/GUARD_SHOT_PISTOL.raw",0
FGUTEN_TAG: db "sfx/GUTEN_TAG.raw",0
FLOCKED_DOOR: db "sfx/LOCKED_DOOR.raw",0
FMEIN_LEBEN: db "sfx/MEIN_LEBEN.raw",0
FMUTTI: db "sfx/MUTTI.raw",0
FSCHUSSTAFFEL: db "sfx/SCHUSSTAFFEL.raw",0
FSHOT_MACHINE_GUN: db "sfx/SHOT_MACHINE_GUN.raw",0
FSHOT_MACHINE_GUN_SINGLE: db "sfx/SHOT_MACHINE_GUN_SINGLE.raw",0
FSHOT_PISTOL: db "sfx/SHOT_PISTOL.raw",0
FSPION: db "sfx/SPION.raw",0
FUGH: db "sfx/UGH.raw",0
FWILHELM: db "sfx/WILHELM.raw",0
FWOOF: db "sfx/WOOF.raw",0
