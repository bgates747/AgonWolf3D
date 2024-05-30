; This file is created by build_98_asm_sfx.py, do not edit it!

SFX_num_buffers: equ 22
; SFX buffer ids:
BUF_ACHTUNG: equ 0xFB00
BUF_AHH: equ 0xFB01
BUF_AUGH: equ 0xFB02
BUF_AYEE: equ 0xFB03
BUF_AYEE_HIGH: equ 0xFB04
BUF_DOG_WOOF_DOUBLE: equ 0xFB05
BUF_DOG_WOOF_SINGLE: equ 0xFB06
BUF_DOG_YELP: equ 0xFB07
BUF_EXPLODE: equ 0xFB08
BUF_GOT_TREASURE: equ 0xFB09
BUF_GUN_EMPTY: equ 0xFB0A
BUF_GUN_RELOAD: equ 0xFB0B
BUF_KNIFE: equ 0xFB0C
BUF_MEIN_LEBEN: equ 0xFB0D
BUF_OOF: equ 0xFB0E
BUF_SCHUSSTAFFEL: equ 0xFB0F
BUF_SCREAM: equ 0xFB10
BUF_SHOT_GATLING_BURST: equ 0xFB11
BUF_SHOT_MACHINE_GUN_BURST: equ 0xFB12
BUF_SHOT_PISTOL: equ 0xFB13
BUF_UGH: equ 0xFB14
BUF_WILHELM: equ 0xFB15

; SFX buffer id reverse lookup:
SFX_buffer_id_lut:
	dl BUF_ACHTUNG
	dl BUF_AHH
	dl BUF_AUGH
	dl BUF_AYEE
	dl BUF_AYEE_HIGH
	dl BUF_DOG_WOOF_DOUBLE
	dl BUF_DOG_WOOF_SINGLE
	dl BUF_DOG_YELP
	dl BUF_EXPLODE
	dl BUF_GOT_TREASURE
	dl BUF_GUN_EMPTY
	dl BUF_GUN_RELOAD
	dl BUF_KNIFE
	dl BUF_MEIN_LEBEN
	dl BUF_OOF
	dl BUF_SCHUSSTAFFEL
	dl BUF_SCREAM
	dl BUF_SHOT_GATLING_BURST
	dl BUF_SHOT_MACHINE_GUN_BURST
	dl BUF_SHOT_PISTOL
	dl BUF_UGH
	dl BUF_WILHELM

; SFX duration lookup:
SFX_duration_lut:
	dw 856 ; ACHTUNG
	dw 401 ; AHH
	dw 764 ; AUGH
	dw 486 ; AYEE
	dw 1088 ; AYEE_HIGH
	dw 611 ; DOG_WOOF_DOUBLE
	dw 533 ; DOG_WOOF_SINGLE
	dw 432 ; DOG_YELP
	dw 1299 ; EXPLODE
	dw 1447 ; GOT_TREASURE
	dw 292 ; GUN_EMPTY
	dw 442 ; GUN_RELOAD
	dw 242 ; KNIFE
	dw 814 ; MEIN_LEBEN
	dw 974 ; OOF
	dw 584 ; SCHUSSTAFFEL
	dw 736 ; SCREAM
	dw 1462 ; SHOT_GATLING_BURST
	dw 1017 ; SHOT_MACHINE_GUN_BURST
	dw 1148 ; SHOT_PISTOL
	dw 375 ; UGH
	dw 1277 ; WILHELM

; SFX load routines jump table:
SFX_load_routines_table:
	dl load_sfx_ACHTUNG
	dl load_sfx_AHH
	dl load_sfx_AUGH
	dl load_sfx_AYEE
	dl load_sfx_AYEE_HIGH
	dl load_sfx_DOG_WOOF_DOUBLE
	dl load_sfx_DOG_WOOF_SINGLE
	dl load_sfx_DOG_YELP
	dl load_sfx_EXPLODE
	dl load_sfx_GOT_TREASURE
	dl load_sfx_GUN_EMPTY
	dl load_sfx_GUN_RELOAD
	dl load_sfx_KNIFE
	dl load_sfx_MEIN_LEBEN
	dl load_sfx_OOF
	dl load_sfx_SCHUSSTAFFEL
	dl load_sfx_SCREAM
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
	ld ix,14394
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
	ld ix,6755
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
	ld ix,12857
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
	ld ix,8192
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
	ld ix,18295
	call vdu_load_sfx
	WAVEFORM_SAMPLE 5, BUF_AYEE_HIGH

load_sfx_DOG_WOOF_DOUBLE:
	ld hl,FDOG_WOOF_DOUBLE
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_DOG_WOOF_DOUBLE
	ld ix,10276
	call vdu_load_sfx
	WAVEFORM_SAMPLE 6, BUF_DOG_WOOF_DOUBLE

load_sfx_DOG_WOOF_SINGLE:
	ld hl,FDOG_WOOF_SINGLE
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_DOG_WOOF_SINGLE
	ld ix,8976
	call vdu_load_sfx
	WAVEFORM_SAMPLE 7, BUF_DOG_WOOF_SINGLE

load_sfx_DOG_YELP:
	ld hl,FDOG_YELP
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_DOG_YELP
	ld ix,7264
	call vdu_load_sfx
	WAVEFORM_SAMPLE 8, BUF_DOG_YELP

load_sfx_EXPLODE:
	ld hl,FEXPLODE
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_EXPLODE
	ld ix,21832
	call vdu_load_sfx
	WAVEFORM_SAMPLE 9, BUF_EXPLODE

load_sfx_GOT_TREASURE:
	ld hl,FGOT_TREASURE
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_GOT_TREASURE
	ld ix,24327
	call vdu_load_sfx
	WAVEFORM_SAMPLE 10, BUF_GOT_TREASURE

load_sfx_GUN_EMPTY:
	ld hl,FGUN_EMPTY
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_GUN_EMPTY
	ld ix,4927
	call vdu_load_sfx
	WAVEFORM_SAMPLE 11, BUF_GUN_EMPTY

load_sfx_GUN_RELOAD:
	ld hl,FGUN_RELOAD
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_GUN_RELOAD
	ld ix,7439
	call vdu_load_sfx
	WAVEFORM_SAMPLE 12, BUF_GUN_RELOAD

load_sfx_KNIFE:
	ld hl,FKNIFE
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_KNIFE
	ld ix,4083
	call vdu_load_sfx
	WAVEFORM_SAMPLE 13, BUF_KNIFE

load_sfx_MEIN_LEBEN:
	ld hl,FMEIN_LEBEN
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_MEIN_LEBEN
	ld ix,13697
	call vdu_load_sfx
	WAVEFORM_SAMPLE 14, BUF_MEIN_LEBEN

load_sfx_OOF:
	ld hl,FOOF
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_OOF
	ld ix,16384
	call vdu_load_sfx
	WAVEFORM_SAMPLE 15, BUF_OOF

load_sfx_SCHUSSTAFFEL:
	ld hl,FSCHUSSTAFFEL
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SCHUSSTAFFEL
	ld ix,9827
	call vdu_load_sfx
	WAVEFORM_SAMPLE 16, BUF_SCHUSSTAFFEL

load_sfx_SCREAM:
	ld hl,FSCREAM
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SCREAM
	ld ix,12382
	call vdu_load_sfx
	WAVEFORM_SAMPLE 17, BUF_SCREAM

load_sfx_SHOT_GATLING_BURST:
	ld hl,FSHOT_GATLING_BURST
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SHOT_GATLING_BURST
	ld ix,24576
	call vdu_load_sfx
	WAVEFORM_SAMPLE 18, BUF_SHOT_GATLING_BURST

load_sfx_SHOT_MACHINE_GUN_BURST:
	ld hl,FSHOT_MACHINE_GUN_BURST
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SHOT_MACHINE_GUN_BURST
	ld ix,17092
	call vdu_load_sfx
	WAVEFORM_SAMPLE 19, BUF_SHOT_MACHINE_GUN_BURST

load_sfx_SHOT_PISTOL:
	ld hl,FSHOT_PISTOL
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_SHOT_PISTOL
	ld ix,19297
	call vdu_load_sfx
	WAVEFORM_SAMPLE 20, BUF_SHOT_PISTOL

load_sfx_UGH:
	ld hl,FUGH
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UGH
	ld ix,6313
	call vdu_load_sfx
	WAVEFORM_SAMPLE 21, BUF_UGH

load_sfx_WILHELM:
	ld hl,FWILHELM
	ld (cur_filename),hl
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_WILHELM
	ld ix,21463
	call vdu_load_sfx
	WAVEFORM_SAMPLE 22, BUF_WILHELM

; File name lookups:
FACHTUNG: db "sfx/ACHTUNG.raw",0
FAHH: db "sfx/AHH.raw",0
FAUGH: db "sfx/AUGH.raw",0
FAYEE: db "sfx/AYEE.raw",0
FAYEE_HIGH: db "sfx/AYEE_HIGH.raw",0
FDOG_WOOF_DOUBLE: db "sfx/DOG_WOOF_DOUBLE.raw",0
FDOG_WOOF_SINGLE: db "sfx/DOG_WOOF_SINGLE.raw",0
FDOG_YELP: db "sfx/DOG_YELP.raw",0
FEXPLODE: db "sfx/EXPLODE.raw",0
FGOT_TREASURE: db "sfx/GOT_TREASURE.raw",0
FGUN_EMPTY: db "sfx/GUN_EMPTY.raw",0
FGUN_RELOAD: db "sfx/GUN_RELOAD.raw",0
FKNIFE: db "sfx/KNIFE.raw",0
FMEIN_LEBEN: db "sfx/MEIN_LEBEN.raw",0
FOOF: db "sfx/OOF.raw",0
FSCHUSSTAFFEL: db "sfx/SCHUSSTAFFEL.raw",0
FSCREAM: db "sfx/SCREAM.raw",0
FSHOT_GATLING_BURST: db "sfx/SHOT_GATLING_BURST.raw",0
FSHOT_MACHINE_GUN_BURST: db "sfx/SHOT_MACHINE_GUN_BURST.raw",0
FSHOT_PISTOL: db "sfx/SHOT_PISTOL.raw",0
FUGH: db "sfx/UGH.raw",0
FWILHELM: db "sfx/WILHELM.raw",0

; Play sfx routines

sfx_play_achtung:
	PLAY_SAMPLE BUF_ACHTUNG, 127, 856

sfx_play_ahh:
	PLAY_SAMPLE BUF_AHH, 127, 401

sfx_play_augh:
	PLAY_SAMPLE BUF_AUGH, 127, 764

sfx_play_ayee:
	PLAY_SAMPLE BUF_AYEE, 127, 486

sfx_play_ayee_high:
	PLAY_SAMPLE BUF_AYEE_HIGH, 127, 1088

sfx_play_dog_woof_double:
	PLAY_SAMPLE BUF_DOG_WOOF_DOUBLE, 127, 611

sfx_play_dog_woof_single:
	PLAY_SAMPLE BUF_DOG_WOOF_SINGLE, 127, 533

sfx_play_dog_yelp:
	PLAY_SAMPLE BUF_DOG_YELP, 127, 432

sfx_play_explode:
	PLAY_SAMPLE BUF_EXPLODE, 127, 1299

sfx_play_got_treasure:
	PLAY_SAMPLE BUF_GOT_TREASURE, 127, 1447

sfx_play_gun_empty:
	PLAY_SAMPLE BUF_GUN_EMPTY, 127, 292

sfx_play_gun_reload:
	PLAY_SAMPLE BUF_GUN_RELOAD, 127, 442

sfx_play_knife:
	PLAY_SAMPLE BUF_KNIFE, 127, 242

sfx_play_mein_leben:
	PLAY_SAMPLE BUF_MEIN_LEBEN, 127, 814

sfx_play_oof:
	PLAY_SAMPLE BUF_OOF, 127, 974

sfx_play_schusstaffel:
	PLAY_SAMPLE BUF_SCHUSSTAFFEL, 127, 584

sfx_play_scream:
	PLAY_SAMPLE BUF_SCREAM, 127, 736

sfx_play_shot_gatling_burst:
	PLAY_SAMPLE BUF_SHOT_GATLING_BURST, 127, 1462

sfx_play_shot_machine_gun_burst:
	PLAY_SAMPLE BUF_SHOT_MACHINE_GUN_BURST, 127, 1017

sfx_play_shot_pistol:
	PLAY_SAMPLE BUF_SHOT_PISTOL, 127, 1148

sfx_play_ugh:
	PLAY_SAMPLE BUF_UGH, 127, 375

sfx_play_wilhelm:
	PLAY_SAMPLE BUF_WILHELM, 127, 1277
