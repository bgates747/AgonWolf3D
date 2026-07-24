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

FONT_ITC_HONDA_IMAGE_COUNT: equ 64
; Glyph pixels are packaged in font.agnb.
