; This file is created by build_98_asm_sfx.py, do not edit it!

SFX_num_buffers: equ 16
; SFX buffer ids:
BUF_ACHTUNG: equ 0xFB00
BUF_AHH: equ 0xFB01
BUF_AUGH: equ 0xFB02
BUF_AYEE: equ 0xFB03
BUF_AYEE_HIGH: equ 0xFB04
BUF_DOG_WOOF: equ 0xFB05
BUF_DOG_YELP: equ 0xFB06
BUF_EXPLODE: equ 0xFB07
BUF_GOT_TREASURE: equ 0xFB08
BUF_MEIN_LEBEN: equ 0xFB09
BUF_SCHUSSTAFFEL: equ 0xFB0A
BUF_SHOT_GATLING_BURST: equ 0xFB0B
BUF_SHOT_MACHINE_GUN_BURST: equ 0xFB0C
BUF_SHOT_PISTOL: equ 0xFB0D
BUF_UGH: equ 0xFB0E
BUF_WILHELM: equ 0xFB0F

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
	dw 818 ; ACHTUNG
	dw 386 ; AHH
	dw 837 ; AUGH
	dw 526 ; AYEE
	dw 1091 ; AYEE_HIGH
	dw 755 ; DOG_WOOF
	dw 430 ; DOG_YELP
	dw 1216 ; EXPLODE
	dw 1535 ; GOT_TREASURE
	dw 854 ; MEIN_LEBEN
	dw 640 ; SCHUSSTAFFEL
	dw 324 ; SHOT_GATLING_BURST
	dw 351 ; SHOT_MACHINE_GUN_BURST
	dw 509 ; SHOT_PISTOL
	dw 354 ; UGH
	dw 1352 ; WILHELM

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
	WAVEFORM_SAMPLE 1, BUF_ACHTUNG

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
	WAVEFORM_SAMPLE 2, BUF_AHH

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
	WAVEFORM_SAMPLE 3, BUF_AUGH

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
	WAVEFORM_SAMPLE 4, BUF_AYEE

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
	WAVEFORM_SAMPLE 5, BUF_AYEE_HIGH

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
	WAVEFORM_SAMPLE 6, BUF_DOG_WOOF

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
	WAVEFORM_SAMPLE 7, BUF_DOG_YELP

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
	WAVEFORM_SAMPLE 8, BUF_EXPLODE

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
	WAVEFORM_SAMPLE 9, BUF_GOT_TREASURE

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
	WAVEFORM_SAMPLE 10, BUF_MEIN_LEBEN

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
	WAVEFORM_SAMPLE 11, BUF_SCHUSSTAFFEL

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
	WAVEFORM_SAMPLE 12, BUF_SHOT_GATLING_BURST

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
	WAVEFORM_SAMPLE 13, BUF_SHOT_MACHINE_GUN_BURST

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
	WAVEFORM_SAMPLE 14, BUF_SHOT_PISTOL

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
	WAVEFORM_SAMPLE 15, BUF_UGH

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
	WAVEFORM_SAMPLE 16, BUF_WILHELM

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

; Play sfx routines

sfx_play_achtung:
	PLAY_SAMPLE 1, 127, 818

sfx_play_ahh:
	PLAY_SAMPLE 2, 127, 386

sfx_play_augh:
	PLAY_SAMPLE 3, 127, 837

sfx_play_ayee:
	PLAY_SAMPLE 4, 127, 526

sfx_play_ayee_high:
	PLAY_SAMPLE 5, 127, 1091

sfx_play_dog_woof:
	PLAY_SAMPLE 6, 127, 755

sfx_play_dog_yelp:
	PLAY_SAMPLE 7, 127, 430

sfx_play_explode:
	PLAY_SAMPLE 8, 127, 1216

sfx_play_got_treasure:
	PLAY_SAMPLE 9, 127, 1535

sfx_play_mein_leben:
	PLAY_SAMPLE 10, 127, 854

sfx_play_schusstaffel:
	PLAY_SAMPLE 11, 127, 640

sfx_play_shot_gatling_burst:
	PLAY_SAMPLE 12, 127, 324

sfx_play_shot_machine_gun_burst:
	PLAY_SAMPLE 13, 127, 351

sfx_play_shot_pistol:
	PLAY_SAMPLE 14, 127, 509

sfx_play_ugh:
	PLAY_SAMPLE 15, 127, 354

sfx_play_wilhelm:
	PLAY_SAMPLE 16, 127, 1352
