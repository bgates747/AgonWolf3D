; Bitmap indices:
BUF_4384: equ 0x1120 ; 32  
; Missing character 33 !
; Missing character 34 "
; Missing character 35 #
; Missing character 36 $
; Missing character 37 %
; Missing character 38 &
; Missing character 39 '
; Missing character 40 (
; Missing character 41 )
; Missing character 42 *
; Missing character 43 +
; Missing character 44 ,
; Missing character 45 -
BUF_4398: equ 0x112E ; 46 .
; Missing character 47 /
BUF_4400: equ 0x1130 ; 48 0
BUF_4401: equ 0x1131 ; 49 1
BUF_4402: equ 0x1132 ; 50 2
BUF_4403: equ 0x1133 ; 51 3
BUF_4404: equ 0x1134 ; 52 4
BUF_4405: equ 0x1135 ; 53 5
BUF_4406: equ 0x1136 ; 54 6
BUF_4407: equ 0x1137 ; 55 7
BUF_4408: equ 0x1138 ; 56 8
BUF_4409: equ 0x1139 ; 57 9
; Missing character 58 :
; Missing character 59 ;
; Missing character 60 <
; Missing character 61 =
; Missing character 62 >
; Missing character 63 ?
; Missing character 64 @
BUF_4417: equ 0x1141 ; 65 A
BUF_4418: equ 0x1142 ; 66 B
BUF_4419: equ 0x1143 ; 67 C
BUF_4420: equ 0x1144 ; 68 D
BUF_4421: equ 0x1145 ; 69 E
BUF_4422: equ 0x1146 ; 70 F
BUF_4423: equ 0x1147 ; 71 G
BUF_4424: equ 0x1148 ; 72 H
BUF_4425: equ 0x1149 ; 73 I
BUF_4426: equ 0x114A ; 74 J
BUF_4427: equ 0x114B ; 75 K
BUF_4428: equ 0x114C ; 76 L
BUF_4429: equ 0x114D ; 77 M
BUF_4430: equ 0x114E ; 78 N
BUF_4431: equ 0x114F ; 79 O
BUF_4432: equ 0x1150 ; 80 P
BUF_4433: equ 0x1151 ; 81 Q
BUF_4434: equ 0x1152 ; 82 R
BUF_4435: equ 0x1153 ; 83 S
BUF_4436: equ 0x1154 ; 84 T
BUF_4437: equ 0x1155 ; 85 U
BUF_4438: equ 0x1156 ; 86 V
BUF_4439: equ 0x1157 ; 87 W
BUF_4440: equ 0x1158 ; 88 X
BUF_4441: equ 0x1159 ; 89 Y
BUF_4442: equ 0x115A ; 90 Z
; Missing character 91 [
; Missing character 92 \
; Missing character 93 ]
; Missing character 94 ^
; Missing character 95 _
; Missing character 96 `
BUF_4449: equ 0x1161 ; 97 a
BUF_4450: equ 0x1162 ; 98 b
BUF_4451: equ 0x1163 ; 99 c
BUF_4452: equ 0x1164 ; 100 d
BUF_4453: equ 0x1165 ; 101 e
BUF_4454: equ 0x1166 ; 102 f
BUF_4455: equ 0x1167 ; 103 g
BUF_4456: equ 0x1168 ; 104 h
BUF_4457: equ 0x1169 ; 105 i
BUF_4458: equ 0x116A ; 106 j
BUF_4459: equ 0x116B ; 107 k
BUF_4460: equ 0x116C ; 108 l
BUF_4461: equ 0x116D ; 109 m
BUF_4462: equ 0x116E ; 110 n
BUF_4463: equ 0x116F ; 111 o
BUF_4464: equ 0x1170 ; 112 p
BUF_4465: equ 0x1171 ; 113 q
BUF_4466: equ 0x1172 ; 114 r
BUF_4467: equ 0x1173 ; 115 s
BUF_4468: equ 0x1174 ; 116 t
BUF_4469: equ 0x1175 ; 117 u
BUF_4470: equ 0x1176 ; 118 v
BUF_4471: equ 0x1177 ; 119 w
BUF_4472: equ 0x1178 ; 120 x
BUF_4473: equ 0x1179 ; 121 y
BUF_4474: equ 0x117A ; 122 z
; [y_offset, dim_y, dim_x], buffer_id label: ; mind the little-endian order when fetching these!!!
font_itc_honda:
	dl 0x000106,BUF_4384
	dl 0x000106,BUF_4384 ; Missing character 33
	dl 0x000106,BUF_4384 ; Missing character 34
	dl 0x000106,BUF_4384 ; Missing character 35
	dl 0x000106,BUF_4384 ; Missing character 36
	dl 0x000106,BUF_4384 ; Missing character 37
	dl 0x000106,BUF_4384 ; Missing character 38
	dl 0x000106,BUF_4384 ; Missing character 39
	dl 0x000106,BUF_4384 ; Missing character 40
	dl 0x000106,BUF_4384 ; Missing character 41
	dl 0x000106,BUF_4384 ; Missing character 42
	dl 0x000106,BUF_4384 ; Missing character 43
	dl 0x000106,BUF_4384 ; Missing character 44
	dl 0x000106,BUF_4384 ; Missing character 45
	dl 0x0E0505,BUF_4398
	dl 0x000106,BUF_4384 ; Missing character 47
	dl 0x00120A,BUF_4400
	dl 0x001204,BUF_4401
	dl 0x001209,BUF_4402
	dl 0x00120A,BUF_4403
	dl 0x00120C,BUF_4404
	dl 0x00120A,BUF_4405
	dl 0x00120A,BUF_4406
	dl 0x001208,BUF_4407
	dl 0x00120A,BUF_4408
	dl 0x00120A,BUF_4409
	dl 0x000106,BUF_4384 ; Missing character 58
	dl 0x000106,BUF_4384 ; Missing character 59
	dl 0x000106,BUF_4384 ; Missing character 60
	dl 0x000106,BUF_4384 ; Missing character 61
	dl 0x000106,BUF_4384 ; Missing character 62
	dl 0x000106,BUF_4384 ; Missing character 63
	dl 0x000106,BUF_4384 ; Missing character 64
	dl 0x01120A,BUF_4417
	dl 0x00120A,BUF_4418
	dl 0x001308,BUF_4419
	dl 0x00120A,BUF_4420
	dl 0x001208,BUF_4421
	dl 0x001208,BUF_4422
	dl 0x00120A,BUF_4423
	dl 0x00120A,BUF_4424
	dl 0x001203,BUF_4425
	dl 0x001206,BUF_4426
	dl 0x00120A,BUF_4427
	dl 0x011208,BUF_4428
	dl 0x00120E,BUF_4429
	dl 0x00120A,BUF_4430
	dl 0x00120A,BUF_4431
	dl 0x00120A,BUF_4432
	dl 0x00150A,BUF_4433
	dl 0x00120A,BUF_4434
	dl 0x001309,BUF_4435
	dl 0x00120A,BUF_4436
	dl 0x00120A,BUF_4437
	dl 0x00120A,BUF_4438
	dl 0x001210,BUF_4439
	dl 0x00120A,BUF_4440
	dl 0x01120A,BUF_4441
	dl 0x011209,BUF_4442
	dl 0x000106,BUF_4384 ; Missing character 91
	dl 0x000106,BUF_4384 ; Missing character 92
	dl 0x000106,BUF_4384 ; Missing character 93
	dl 0x000106,BUF_4384 ; Missing character 94
	dl 0x000106,BUF_4384 ; Missing character 95
	dl 0x000106,BUF_4384 ; Missing character 96
	dl 0x060C08,BUF_4449
	dl 0x011209,BUF_4450
	dl 0x060C07,BUF_4451
	dl 0x001209,BUF_4452
	dl 0x060C08,BUF_4453
	dl 0x001209,BUF_4454
	dl 0x061209,BUF_4455
	dl 0x011209,BUF_4456
	dl 0x001204,BUF_4457
	dl 0x001808,BUF_4458
	dl 0x011209,BUF_4459
	dl 0x001203,BUF_4460
	dl 0x060D0E,BUF_4461
	dl 0x060C09,BUF_4462
	dl 0x060C09,BUF_4463
	dl 0x061209,BUF_4464
	dl 0x061209,BUF_4465
	dl 0x060D06,BUF_4466
	dl 0x060D08,BUF_4467
	dl 0x030F07,BUF_4468
	dl 0x060C09,BUF_4469
	dl 0x060C09,BUF_4470
	dl 0x060C0E,BUF_4471
	dl 0x060C09,BUF_4472
	dl 0x061109,BUF_4473
	dl 0x060C09,BUF_4474

; Import .rgba2 bitmap files and load them into VDP buffers
load_font_itc_honda:

	ld hl,Fhonda032
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4384
	ld bc,6
	ld de,1
	ld ix,6
	call vdu_load_img
; Missing character 33
; Missing character 34
; Missing character 35
; Missing character 36
; Missing character 37
; Missing character 38
; Missing character 39
; Missing character 40
; Missing character 41
; Missing character 42
; Missing character 43
; Missing character 44
; Missing character 45

	ld hl,Fhonda046
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4398
	ld bc,5
	ld de,5
	ld ix,25
	call vdu_load_img
; Missing character 47

	ld hl,Fhonda048
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4400
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda049
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4401
	ld bc,4
	ld de,18
	ld ix,72
	call vdu_load_img

	ld hl,Fhonda050
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4402
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_img

	ld hl,Fhonda051
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4403
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda052
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4404
	ld bc,12
	ld de,18
	ld ix,216
	call vdu_load_img

	ld hl,Fhonda053
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4405
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda054
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4406
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda055
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4407
	ld bc,8
	ld de,18
	ld ix,144
	call vdu_load_img

	ld hl,Fhonda056
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4408
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda057
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4409
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img
; Missing character 58
; Missing character 59
; Missing character 60
; Missing character 61
; Missing character 62
; Missing character 63
; Missing character 64

	ld hl,Fhonda065
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4417
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda066
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4418
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda067
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4419
	ld bc,8
	ld de,19
	ld ix,152
	call vdu_load_img

	ld hl,Fhonda068
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4420
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda069
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4421
	ld bc,8
	ld de,18
	ld ix,144
	call vdu_load_img

	ld hl,Fhonda070
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4422
	ld bc,8
	ld de,18
	ld ix,144
	call vdu_load_img

	ld hl,Fhonda071
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4423
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda072
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4424
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda073
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4425
	ld bc,3
	ld de,18
	ld ix,54
	call vdu_load_img

	ld hl,Fhonda074
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4426
	ld bc,6
	ld de,18
	ld ix,108
	call vdu_load_img

	ld hl,Fhonda075
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4427
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda076
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4428
	ld bc,8
	ld de,18
	ld ix,144
	call vdu_load_img

	ld hl,Fhonda077
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4429
	ld bc,14
	ld de,18
	ld ix,252
	call vdu_load_img

	ld hl,Fhonda078
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4430
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda079
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4431
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda080
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4432
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda081
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4433
	ld bc,10
	ld de,21
	ld ix,210
	call vdu_load_img

	ld hl,Fhonda082
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4434
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda083
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4435
	ld bc,9
	ld de,19
	ld ix,171
	call vdu_load_img

	ld hl,Fhonda084
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4436
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda085
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4437
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda086
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4438
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda087
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4439
	ld bc,16
	ld de,18
	ld ix,288
	call vdu_load_img

	ld hl,Fhonda088
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4440
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda089
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4441
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_img

	ld hl,Fhonda090
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4442
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_img
; Missing character 91
; Missing character 92
; Missing character 93
; Missing character 94
; Missing character 95
; Missing character 96

	ld hl,Fhonda097
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4449
	ld bc,8
	ld de,12
	ld ix,96
	call vdu_load_img

	ld hl,Fhonda098
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4450
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_img

	ld hl,Fhonda099
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4451
	ld bc,7
	ld de,12
	ld ix,84
	call vdu_load_img

	ld hl,Fhonda100
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4452
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_img

	ld hl,Fhonda101
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4453
	ld bc,8
	ld de,12
	ld ix,96
	call vdu_load_img

	ld hl,Fhonda102
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4454
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_img

	ld hl,Fhonda103
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4455
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_img

	ld hl,Fhonda104
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4456
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_img

	ld hl,Fhonda105
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4457
	ld bc,4
	ld de,18
	ld ix,72
	call vdu_load_img

	ld hl,Fhonda106
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4458
	ld bc,8
	ld de,24
	ld ix,192
	call vdu_load_img

	ld hl,Fhonda107
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4459
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_img

	ld hl,Fhonda108
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4460
	ld bc,3
	ld de,18
	ld ix,54
	call vdu_load_img

	ld hl,Fhonda109
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4461
	ld bc,14
	ld de,13
	ld ix,182
	call vdu_load_img

	ld hl,Fhonda110
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4462
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_img

	ld hl,Fhonda111
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4463
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_img

	ld hl,Fhonda112
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4464
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_img

	ld hl,Fhonda113
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4465
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_img

	ld hl,Fhonda114
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4466
	ld bc,6
	ld de,13
	ld ix,78
	call vdu_load_img

	ld hl,Fhonda115
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4467
	ld bc,8
	ld de,13
	ld ix,104
	call vdu_load_img

	ld hl,Fhonda116
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4468
	ld bc,7
	ld de,15
	ld ix,105
	call vdu_load_img

	ld hl,Fhonda117
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4469
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_img

	ld hl,Fhonda118
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4470
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_img

	ld hl,Fhonda119
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4471
	ld bc,14
	ld de,12
	ld ix,168
	call vdu_load_img

	ld hl,Fhonda120
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4472
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_img

	ld hl,Fhonda121
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4473
	ld bc,9
	ld de,17
	ld ix,153
	call vdu_load_img

	ld hl,Fhonda122
	ld de,filedata
	ld bc,65536
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4474
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_img

	ret

Fhonda032: db "fonts/honda/032.rgba2",0
Fhonda046: db "fonts/honda/046.rgba2",0
Fhonda048: db "fonts/honda/048.rgba2",0
Fhonda049: db "fonts/honda/049.rgba2",0
Fhonda050: db "fonts/honda/050.rgba2",0
Fhonda051: db "fonts/honda/051.rgba2",0
Fhonda052: db "fonts/honda/052.rgba2",0
Fhonda053: db "fonts/honda/053.rgba2",0
Fhonda054: db "fonts/honda/054.rgba2",0
Fhonda055: db "fonts/honda/055.rgba2",0
Fhonda056: db "fonts/honda/056.rgba2",0
Fhonda057: db "fonts/honda/057.rgba2",0
Fhonda065: db "fonts/honda/065.rgba2",0
Fhonda066: db "fonts/honda/066.rgba2",0
Fhonda067: db "fonts/honda/067.rgba2",0
Fhonda068: db "fonts/honda/068.rgba2",0
Fhonda069: db "fonts/honda/069.rgba2",0
Fhonda070: db "fonts/honda/070.rgba2",0
Fhonda071: db "fonts/honda/071.rgba2",0
Fhonda072: db "fonts/honda/072.rgba2",0
Fhonda073: db "fonts/honda/073.rgba2",0
Fhonda074: db "fonts/honda/074.rgba2",0
Fhonda075: db "fonts/honda/075.rgba2",0
Fhonda076: db "fonts/honda/076.rgba2",0
Fhonda077: db "fonts/honda/077.rgba2",0
Fhonda078: db "fonts/honda/078.rgba2",0
Fhonda079: db "fonts/honda/079.rgba2",0
Fhonda080: db "fonts/honda/080.rgba2",0
Fhonda081: db "fonts/honda/081.rgba2",0
Fhonda082: db "fonts/honda/082.rgba2",0
Fhonda083: db "fonts/honda/083.rgba2",0
Fhonda084: db "fonts/honda/084.rgba2",0
Fhonda085: db "fonts/honda/085.rgba2",0
Fhonda086: db "fonts/honda/086.rgba2",0
Fhonda087: db "fonts/honda/087.rgba2",0
Fhonda088: db "fonts/honda/088.rgba2",0
Fhonda089: db "fonts/honda/089.rgba2",0
Fhonda090: db "fonts/honda/090.rgba2",0
Fhonda097: db "fonts/honda/097.rgba2",0
Fhonda098: db "fonts/honda/098.rgba2",0
Fhonda099: db "fonts/honda/099.rgba2",0
Fhonda100: db "fonts/honda/100.rgba2",0
Fhonda101: db "fonts/honda/101.rgba2",0
Fhonda102: db "fonts/honda/102.rgba2",0
Fhonda103: db "fonts/honda/103.rgba2",0
Fhonda104: db "fonts/honda/104.rgba2",0
Fhonda105: db "fonts/honda/105.rgba2",0
Fhonda106: db "fonts/honda/106.rgba2",0
Fhonda107: db "fonts/honda/107.rgba2",0
Fhonda108: db "fonts/honda/108.rgba2",0
Fhonda109: db "fonts/honda/109.rgba2",0
Fhonda110: db "fonts/honda/110.rgba2",0
Fhonda111: db "fonts/honda/111.rgba2",0
Fhonda112: db "fonts/honda/112.rgba2",0
Fhonda113: db "fonts/honda/113.rgba2",0
Fhonda114: db "fonts/honda/114.rgba2",0
Fhonda115: db "fonts/honda/115.rgba2",0
Fhonda116: db "fonts/honda/116.rgba2",0
Fhonda117: db "fonts/honda/117.rgba2",0
Fhonda118: db "fonts/honda/118.rgba2",0
Fhonda119: db "fonts/honda/119.rgba2",0
Fhonda120: db "fonts/honda/120.rgba2",0
Fhonda121: db "fonts/honda/121.rgba2",0
Fhonda122: db "fonts/honda/122.rgba2",0
