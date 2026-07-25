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
	dw 487 ; AYEE
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
	dw 975 ; OOF
	dw 584 ; SCHUSSTAFFEL
	dw 736 ; SCREAM
	dw 1463 ; SHOT_GATLING_BURST
	dw 1017 ; SHOT_MACHINE_GUN_BURST
	dw 1148 ; SHOT_PISTOL
	dw 375 ; UGH
	dw 1277 ; WILHELM

; PCM payloads are packaged in sfx.agnb.

; Play sfx routines

sfx_play_achtung:
	ld hl,BUF_ACHTUNG
	ld bc,856
	jp vdu_play_sfx

sfx_play_ahh:
	ld hl,BUF_AHH
	ld bc,401
	jp vdu_play_sfx

sfx_play_augh:
	ld hl,BUF_AUGH
	ld bc,764
	jp vdu_play_sfx

sfx_play_ayee:
	ld hl,BUF_AYEE
	ld bc,487
	jp vdu_play_sfx

sfx_play_ayee_high:
	ld hl,BUF_AYEE_HIGH
	ld bc,1088
	jp vdu_play_sfx

sfx_play_dog_woof_double:
	ld hl,BUF_DOG_WOOF_DOUBLE
	ld bc,611
	jp vdu_play_sfx

sfx_play_dog_woof_single:
	ld hl,BUF_DOG_WOOF_SINGLE
	ld bc,533
	jp vdu_play_sfx

sfx_play_dog_yelp:
	ld hl,BUF_DOG_YELP
	ld bc,432
	jp vdu_play_sfx

sfx_play_explode:
	ld hl,BUF_EXPLODE
	ld bc,1299
	jp vdu_play_sfx

sfx_play_got_treasure:
	ld hl,BUF_GOT_TREASURE
	ld bc,1447
	jp vdu_play_sfx

sfx_play_gun_empty:
	ld hl,BUF_GUN_EMPTY
	ld bc,292
	jp vdu_play_sfx

sfx_play_gun_reload:
	ld hl,BUF_GUN_RELOAD
	ld bc,442
	jp vdu_play_sfx

sfx_play_knife:
	ld hl,BUF_KNIFE
	ld bc,242
	jp vdu_play_sfx

sfx_play_mein_leben:
	ld hl,BUF_MEIN_LEBEN
	ld bc,814
	jp vdu_play_sfx

sfx_play_oof:
	ld hl,BUF_OOF
	ld bc,975
	jp vdu_play_sfx

sfx_play_schusstaffel:
	ld hl,BUF_SCHUSSTAFFEL
	ld bc,584
	jp vdu_play_sfx

sfx_play_scream:
	ld hl,BUF_SCREAM
	ld bc,736
	jp vdu_play_sfx

sfx_play_shot_gatling_burst:
	ld hl,BUF_SHOT_GATLING_BURST
	ld bc,1463
	jp vdu_play_sfx

sfx_play_shot_machine_gun_burst:
	ld hl,BUF_SHOT_MACHINE_GUN_BURST
	ld bc,1017
	jp vdu_play_sfx

sfx_play_shot_pistol:
	ld hl,BUF_SHOT_PISTOL
	ld bc,1148
	jp vdu_play_sfx

sfx_play_ugh:
	ld hl,BUF_UGH
	ld bc,375
	jp vdu_play_sfx

sfx_play_wilhelm:
	ld hl,BUF_WILHELM
	ld bc,1277
	jp vdu_play_sfx
