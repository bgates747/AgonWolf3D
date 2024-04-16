; Bitmap indices:
BUF_4128: equ 0x1020 ; 32  
BUF_4129: equ 0x1021 ; 33 !
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
BUF_4144: equ 0x1030 ; 48 0
BUF_4145: equ 0x1031 ; 49 1
BUF_4146: equ 0x1032 ; 50 2
BUF_4147: equ 0x1033 ; 51 3
BUF_4148: equ 0x1034 ; 52 4
BUF_4149: equ 0x1035 ; 53 5
BUF_4150: equ 0x1036 ; 54 6
BUF_4151: equ 0x1037 ; 55 7
BUF_4152: equ 0x1038 ; 56 8
BUF_4153: equ 0x1039 ; 57 9
; Missing character 58 :
; Missing character 59 ;
; Missing character 60 <
; Missing character 61 =
; Missing character 62 >
BUF_4159: equ 0x103F ; 63 ?
; Missing character 64 @
BUF_4161: equ 0x1041 ; 65 A
BUF_4162: equ 0x1042 ; 66 B
BUF_4163: equ 0x1043 ; 67 C
BUF_4164: equ 0x1044 ; 68 D
BUF_4165: equ 0x1045 ; 69 E
BUF_4166: equ 0x1046 ; 70 F
BUF_4167: equ 0x1047 ; 71 G
BUF_4168: equ 0x1048 ; 72 H
BUF_4169: equ 0x1049 ; 73 I
BUF_4170: equ 0x104A ; 74 J
BUF_4171: equ 0x104B ; 75 K
BUF_4172: equ 0x104C ; 76 L
BUF_4173: equ 0x104D ; 77 M
BUF_4174: equ 0x104E ; 78 N
BUF_4175: equ 0x104F ; 79 O
BUF_4176: equ 0x1050 ; 80 P
BUF_4177: equ 0x1051 ; 81 Q
BUF_4178: equ 0x1052 ; 82 R
BUF_4179: equ 0x1053 ; 83 S
BUF_4180: equ 0x1054 ; 84 T
BUF_4181: equ 0x1055 ; 85 U
BUF_4182: equ 0x1056 ; 86 V
BUF_4183: equ 0x1057 ; 87 W
BUF_4184: equ 0x1058 ; 88 X
BUF_4185: equ 0x1059 ; 89 Y
BUF_4186: equ 0x105A ; 90 Z
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
	dl 0x000106,BUF_4128
	dl 0x000E03,BUF_4129
	dl 0x000106,BUF_4128 ; Missing character 34
	dl 0x000106,BUF_4128 ; Missing character 35
	dl 0x000106,BUF_4128 ; Missing character 36
	dl 0x000106,BUF_4128 ; Missing character 37
	dl 0x000106,BUF_4128 ; Missing character 38
	dl 0x000106,BUF_4128 ; Missing character 39
	dl 0x000106,BUF_4128 ; Missing character 40
	dl 0x000106,BUF_4128 ; Missing character 41
	dl 0x000106,BUF_4128 ; Missing character 42
	dl 0x000106,BUF_4128 ; Missing character 43
	dl 0x000106,BUF_4128 ; Missing character 44
	dl 0x000106,BUF_4128 ; Missing character 45
	dl 0x000106,BUF_4128 ; Missing character 46
	dl 0x000106,BUF_4128 ; Missing character 47
	dl 0x000E08,BUF_4144
	dl 0x000E08,BUF_4145
	dl 0x000E08,BUF_4146
	dl 0x000E08,BUF_4147
	dl 0x000E08,BUF_4148
	dl 0x000E08,BUF_4149
	dl 0x000E08,BUF_4150
	dl 0x000E08,BUF_4151
	dl 0x000E08,BUF_4152
	dl 0x000E08,BUF_4153
	dl 0x000106,BUF_4128 ; Missing character 58
	dl 0x000106,BUF_4128 ; Missing character 59
	dl 0x000106,BUF_4128 ; Missing character 60
	dl 0x000106,BUF_4128 ; Missing character 61
	dl 0x000106,BUF_4128 ; Missing character 62
	dl 0x000E08,BUF_4159
	dl 0x000106,BUF_4128 ; Missing character 64
	dl 0x000E07,BUF_4161
	dl 0x000E08,BUF_4162
	dl 0x000E07,BUF_4163
	dl 0x000E08,BUF_4164
	dl 0x000E08,BUF_4165
	dl 0x000E07,BUF_4166
	dl 0x000E08,BUF_4167
	dl 0x000E07,BUF_4168
	dl 0x000E07,BUF_4169
	dl 0x000E08,BUF_4170
	dl 0x000E07,BUF_4171
	dl 0x000E08,BUF_4172
	dl 0x000E09,BUF_4173
	dl 0x000E07,BUF_4174
	dl 0x000E08,BUF_4175
	dl 0x000E07,BUF_4176
	dl 0x000F08,BUF_4177
	dl 0x000E08,BUF_4178
	dl 0x000E08,BUF_4179
	dl 0x000E07,BUF_4180
	dl 0x000E08,BUF_4181
	dl 0x000E07,BUF_4182
	dl 0x000E0B,BUF_4183
	dl 0x000E07,BUF_4184
	dl 0x000E08,BUF_4185
	dl 0x000E07,BUF_4186
	dl 0x000106,BUF_4128 ; Missing character 91
	dl 0x000106,BUF_4128 ; Missing character 92
	dl 0x000106,BUF_4128 ; Missing character 93
	dl 0x000106,BUF_4128 ; Missing character 94
	dl 0x000106,BUF_4128 ; Missing character 95
	dl 0x000106,BUF_4128 ; Missing character 96
	dl 0x000106,BUF_4128 ; Missing character 97
	dl 0x000106,BUF_4128 ; Missing character 98
	dl 0x000106,BUF_4128 ; Missing character 99
	dl 0x000106,BUF_4128 ; Missing character 100
	dl 0x000106,BUF_4128 ; Missing character 101
	dl 0x000106,BUF_4128 ; Missing character 102
	dl 0x000106,BUF_4128 ; Missing character 103
	dl 0x000106,BUF_4128 ; Missing character 104
	dl 0x000106,BUF_4128 ; Missing character 105
	dl 0x000106,BUF_4128 ; Missing character 106
	dl 0x000106,BUF_4128 ; Missing character 107
	dl 0x000106,BUF_4128 ; Missing character 108
	dl 0x000106,BUF_4128 ; Missing character 109
	dl 0x000106,BUF_4128 ; Missing character 110
	dl 0x000106,BUF_4128 ; Missing character 111
	dl 0x000106,BUF_4128 ; Missing character 112
	dl 0x000106,BUF_4128 ; Missing character 113
	dl 0x000106,BUF_4128 ; Missing character 114
	dl 0x000106,BUF_4128 ; Missing character 115
	dl 0x000106,BUF_4128 ; Missing character 116
	dl 0x000106,BUF_4128 ; Missing character 117
	dl 0x000106,BUF_4128 ; Missing character 118
	dl 0x000106,BUF_4128 ; Missing character 119
	dl 0x000106,BUF_4128 ; Missing character 120
	dl 0x000106,BUF_4128 ; Missing character 121
	dl 0x000106,BUF_4128 ; Missing character 122

; Import .rgba bitmap files and load them into VDP buffers
load_font_retro_computer:

	ld hl,F032
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4128
	ld bc,6
	ld de,1
	ld ix,6
	call vdu_load_bmp2_from_file

	ld hl,F033
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4129
	ld bc,3
	ld de,14
	ld ix,42
	call vdu_load_bmp2_from_file
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

	ld hl,F048
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4144
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F049
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4145
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F050
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4146
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F051
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4147
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F052
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4148
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F053
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4149
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F054
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4150
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F055
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4151
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F056
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4152
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F057
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4153
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file
; Missing character 58
; Missing character 59
; Missing character 60
; Missing character 61
; Missing character 62

	ld hl,F063
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4159
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file
; Missing character 64

	ld hl,F065
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4161
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F066
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4162
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F067
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4163
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F068
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4164
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F069
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4165
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F070
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4166
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F071
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4167
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F072
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4168
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F073
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4169
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F074
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4170
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F075
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4171
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F076
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4172
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F077
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4173
	ld bc,9
	ld de,14
	ld ix,126
	call vdu_load_bmp2_from_file

	ld hl,F078
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4174
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F079
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4175
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F080
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4176
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F081
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4177
	ld bc,8
	ld de,15
	ld ix,120
	call vdu_load_bmp2_from_file

	ld hl,F082
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4178
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F083
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4179
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F084
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4180
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F085
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4181
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F086
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4182
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F087
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4183
	ld bc,11
	ld de,14
	ld ix,154
	call vdu_load_bmp2_from_file

	ld hl,F088
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4184
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file

	ld hl,F089
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4185
	ld bc,8
	ld de,14
	ld ix,112
	call vdu_load_bmp2_from_file

	ld hl,F090
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4186
	ld bc,7
	ld de,14
	ld ix,98
	call vdu_load_bmp2_from_file
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

F032: db "fonts/rc/032.rgba2",0
F033: db "fonts/rc/033.rgba2",0
F048: db "fonts/rc/048.rgba2",0
F049: db "fonts/rc/049.rgba2",0
F050: db "fonts/rc/050.rgba2",0
F051: db "fonts/rc/051.rgba2",0
F052: db "fonts/rc/052.rgba2",0
F053: db "fonts/rc/053.rgba2",0
F054: db "fonts/rc/054.rgba2",0
F055: db "fonts/rc/055.rgba2",0
F056: db "fonts/rc/056.rgba2",0
F057: db "fonts/rc/057.rgba2",0
F063: db "fonts/rc/063.rgba2",0
F065: db "fonts/rc/065.rgba2",0
F066: db "fonts/rc/066.rgba2",0
F067: db "fonts/rc/067.rgba2",0
F068: db "fonts/rc/068.rgba2",0
F069: db "fonts/rc/069.rgba2",0
F070: db "fonts/rc/070.rgba2",0
F071: db "fonts/rc/071.rgba2",0
F072: db "fonts/rc/072.rgba2",0
F073: db "fonts/rc/073.rgba2",0
F074: db "fonts/rc/074.rgba2",0
F075: db "fonts/rc/075.rgba2",0
F076: db "fonts/rc/076.rgba2",0
F077: db "fonts/rc/077.rgba2",0
F078: db "fonts/rc/078.rgba2",0
F079: db "fonts/rc/079.rgba2",0
F080: db "fonts/rc/080.rgba2",0
F081: db "fonts/rc/081.rgba2",0
F082: db "fonts/rc/082.rgba2",0
F083: db "fonts/rc/083.rgba2",0
F084: db "fonts/rc/084.rgba2",0
F085: db "fonts/rc/085.rgba2",0
F086: db "fonts/rc/086.rgba2",0
F087: db "fonts/rc/087.rgba2",0
F088: db "fonts/rc/088.rgba2",0
F089: db "fonts/rc/089.rgba2",0
F090: db "fonts/rc/090.rgba2",0
