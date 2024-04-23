; Bitmap indices:
BUF_4384: equ 0x1120 ; 32  
BUF_4385: equ 0x1121 ; 33 !
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
; Missing character 46 .
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
BUF_4415: equ 0x113F ; 63 ?
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
; Missing character 97 a
; Missing character 98 b
; Missing character 99 c
; Missing character 100 d
; Missing character 101 e
; Missing character 102 f
; Missing character 103 g
; Missing character 104 h
; Missing character 105 i
; Missing character 106 j
; Missing character 107 k
; Missing character 108 l
; Missing character 109 m
; Missing character 110 n
; Missing character 111 o
; Missing character 112 p
; Missing character 113 q
; Missing character 114 r
; Missing character 115 s
; Missing character 116 t
; Missing character 117 u
; Missing character 118 v
; Missing character 119 w
; Missing character 120 x
; Missing character 121 y
; Missing character 122 z
; [y_offset, dim_y, dim_x], buffer_id label: ; mind the little-endian order when fetching these!!!
font_retro_computer:
	dl 0x000106,BUF_4384
	dl 0x000E03,BUF_4385
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
	dl 0x000106,BUF_4384 ; Missing character 46
	dl 0x000106,BUF_4384 ; Missing character 47
	dl 0x000E08,BUF_4400
	dl 0x000E08,BUF_4401
	dl 0x000E08,BUF_4402
	dl 0x000E08,BUF_4403
	dl 0x000E08,BUF_4404
	dl 0x000E08,BUF_4405
	dl 0x000E08,BUF_4406
	dl 0x000E08,BUF_4407
	dl 0x000E08,BUF_4408
	dl 0x000E08,BUF_4409
	dl 0x000106,BUF_4384 ; Missing character 58
	dl 0x000106,BUF_4384 ; Missing character 59
	dl 0x000106,BUF_4384 ; Missing character 60
	dl 0x000106,BUF_4384 ; Missing character 61
	dl 0x000106,BUF_4384 ; Missing character 62
	dl 0x000E08,BUF_4415
	dl 0x000106,BUF_4384 ; Missing character 64
	dl 0x000E07,BUF_4417
	dl 0x000E08,BUF_4418
	dl 0x000E07,BUF_4419
	dl 0x000E08,BUF_4420
	dl 0x000E08,BUF_4421
	dl 0x000E07,BUF_4422
	dl 0x000E08,BUF_4423
	dl 0x000E07,BUF_4424
	dl 0x000E07,BUF_4425
	dl 0x000E08,BUF_4426
	dl 0x000E07,BUF_4427
	dl 0x000E08,BUF_4428
	dl 0x000E09,BUF_4429
	dl 0x000E07,BUF_4430
	dl 0x000E08,BUF_4431
	dl 0x000E07,BUF_4432
	dl 0x000F08,BUF_4433
	dl 0x000E08,BUF_4434
	dl 0x000E08,BUF_4435
	dl 0x000E07,BUF_4436
	dl 0x000E08,BUF_4437
	dl 0x000E07,BUF_4438
	dl 0x000E0B,BUF_4439
	dl 0x000E07,BUF_4440
	dl 0x000E08,BUF_4441
	dl 0x000E07,BUF_4442
	dl 0x000106,BUF_4384 ; Missing character 91
	dl 0x000106,BUF_4384 ; Missing character 92
	dl 0x000106,BUF_4384 ; Missing character 93
	dl 0x000106,BUF_4384 ; Missing character 94
	dl 0x000106,BUF_4384 ; Missing character 95
	dl 0x000106,BUF_4384 ; Missing character 96
	dl 0x000106,BUF_4384 ; Missing character 97
	dl 0x000106,BUF_4384 ; Missing character 98
	dl 0x000106,BUF_4384 ; Missing character 99
	dl 0x000106,BUF_4384 ; Missing character 100
	dl 0x000106,BUF_4384 ; Missing character 101
	dl 0x000106,BUF_4384 ; Missing character 102
	dl 0x000106,BUF_4384 ; Missing character 103
	dl 0x000106,BUF_4384 ; Missing character 104
	dl 0x000106,BUF_4384 ; Missing character 105
	dl 0x000106,BUF_4384 ; Missing character 106
	dl 0x000106,BUF_4384 ; Missing character 107
	dl 0x000106,BUF_4384 ; Missing character 108
	dl 0x000106,BUF_4384 ; Missing character 109
	dl 0x000106,BUF_4384 ; Missing character 110
	dl 0x000106,BUF_4384 ; Missing character 111
	dl 0x000106,BUF_4384 ; Missing character 112
	dl 0x000106,BUF_4384 ; Missing character 113
	dl 0x000106,BUF_4384 ; Missing character 114
	dl 0x000106,BUF_4384 ; Missing character 115
	dl 0x000106,BUF_4384 ; Missing character 116
	dl 0x000106,BUF_4384 ; Missing character 117
	dl 0x000106,BUF_4384 ; Missing character 118
	dl 0x000106,BUF_4384 ; Missing character 119
	dl 0x000106,BUF_4384 ; Missing character 120
	dl 0x000106,BUF_4384 ; Missing character 121
	dl 0x000106,BUF_4384 ; Missing character 122

; Import .rgba2 bitmap files and load them into VDP buffers
load_font_retro_computer:

	ld hl,Frc032
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4384
	ld bc,6
	ld de,1
	ld ix,6
	call vdu_load_img

	ld hl,Frc033
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4385
	ld bc,3
	ld de,14
	ld ix,42
	call vdu_load_img
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
; Missing character 46
; Missing character 47

	ld hl,Frc048
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4400
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc049
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4401
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc050
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4402
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc051
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4403
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc052
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4404
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc053
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4405
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc054
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4406
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc055
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4407
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc056
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4408
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc057
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4409
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img
; Missing character 58
; Missing character 59
; Missing character 60
; Missing character 61
; Missing character 62

	ld hl,Frc063
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4415
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img
; Missing character 64

	ld hl,Frc065
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4417
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc066
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4418
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc067
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4419
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc068
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4420
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc069
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4421
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc070
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4422
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc071
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4423
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc072
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4424
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc073
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4425
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc074
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4426
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc075
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4427
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc076
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4428
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc077
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4429
	ld bc,9
	ld de,14
	ld ix,126
	call vdu_load_img

	ld hl,Frc078
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4430
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc079
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4431
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc080
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4432
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc081
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4433
	ld bc,8
	ld de,15
	ld ix,120
	call vdu_load_img

	ld hl,Frc082
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4434
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc083
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4435
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc084
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4436
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc085
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4437
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc086
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4438
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc087
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4439
	ld bc,11
	ld de,14
	ld ix,154
	call vdu_load_img

	ld hl,Frc088
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4440
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img

	ld hl,Frc089
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4441
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_img

	ld hl,Frc090
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4442
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_img
; Missing character 91
; Missing character 92
; Missing character 93
; Missing character 94
; Missing character 95
; Missing character 96
; Missing character 97
; Missing character 98
; Missing character 99
; Missing character 100
; Missing character 101
; Missing character 102
; Missing character 103
; Missing character 104
; Missing character 105
; Missing character 106
; Missing character 107
; Missing character 108
; Missing character 109
; Missing character 110
; Missing character 111
; Missing character 112
; Missing character 113
; Missing character 114
; Missing character 115
; Missing character 116
; Missing character 117
; Missing character 118
; Missing character 119
; Missing character 120
; Missing character 121
; Missing character 122

	ret

Frc032: db "fonts/rc/032.rgba2",0
Frc033: db "fonts/rc/033.rgba2",0
Frc048: db "fonts/rc/048.rgba2",0
Frc049: db "fonts/rc/049.rgba2",0
Frc050: db "fonts/rc/050.rgba2",0
Frc051: db "fonts/rc/051.rgba2",0
Frc052: db "fonts/rc/052.rgba2",0
Frc053: db "fonts/rc/053.rgba2",0
Frc054: db "fonts/rc/054.rgba2",0
Frc055: db "fonts/rc/055.rgba2",0
Frc056: db "fonts/rc/056.rgba2",0
Frc057: db "fonts/rc/057.rgba2",0
Frc063: db "fonts/rc/063.rgba2",0
Frc065: db "fonts/rc/065.rgba2",0
Frc066: db "fonts/rc/066.rgba2",0
Frc067: db "fonts/rc/067.rgba2",0
Frc068: db "fonts/rc/068.rgba2",0
Frc069: db "fonts/rc/069.rgba2",0
Frc070: db "fonts/rc/070.rgba2",0
Frc071: db "fonts/rc/071.rgba2",0
Frc072: db "fonts/rc/072.rgba2",0
Frc073: db "fonts/rc/073.rgba2",0
Frc074: db "fonts/rc/074.rgba2",0
Frc075: db "fonts/rc/075.rgba2",0
Frc076: db "fonts/rc/076.rgba2",0
Frc077: db "fonts/rc/077.rgba2",0
Frc078: db "fonts/rc/078.rgba2",0
Frc079: db "fonts/rc/079.rgba2",0
Frc080: db "fonts/rc/080.rgba2",0
Frc081: db "fonts/rc/081.rgba2",0
Frc082: db "fonts/rc/082.rgba2",0
Frc083: db "fonts/rc/083.rgba2",0
Frc084: db "fonts/rc/084.rgba2",0
Frc085: db "fonts/rc/085.rgba2",0
Frc086: db "fonts/rc/086.rgba2",0
Frc087: db "fonts/rc/087.rgba2",0
Frc088: db "fonts/rc/088.rgba2",0
Frc089: db "fonts/rc/089.rgba2",0
Frc090: db "fonts/rc/090.rgba2",0
