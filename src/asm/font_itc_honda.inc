; Bitmap indices:
BUF_4128: equ 0x1020 ; 32  
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
BUF_4142: equ 0x102E ; 46 .
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
; Missing character 63 ?
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
BUF_4193: equ 0x1061 ; 97 a
BUF_4194: equ 0x1062 ; 98 b
BUF_4195: equ 0x1063 ; 99 c
BUF_4196: equ 0x1064 ; 100 d
BUF_4197: equ 0x1065 ; 101 e
BUF_4198: equ 0x1066 ; 102 f
BUF_4199: equ 0x1067 ; 103 g
BUF_4200: equ 0x1068 ; 104 h
BUF_4201: equ 0x1069 ; 105 i
BUF_4202: equ 0x106A ; 106 j
BUF_4203: equ 0x106B ; 107 k
BUF_4204: equ 0x106C ; 108 l
BUF_4205: equ 0x106D ; 109 m
BUF_4206: equ 0x106E ; 110 n
BUF_4207: equ 0x106F ; 111 o
BUF_4208: equ 0x1070 ; 112 p
BUF_4209: equ 0x1071 ; 113 q
BUF_4210: equ 0x1072 ; 114 r
BUF_4211: equ 0x1073 ; 115 s
BUF_4212: equ 0x1074 ; 116 t
BUF_4213: equ 0x1075 ; 117 u
BUF_4214: equ 0x1076 ; 118 v
BUF_4215: equ 0x1077 ; 119 w
BUF_4216: equ 0x1078 ; 120 x
BUF_4217: equ 0x1079 ; 121 y
BUF_4218: equ 0x107A ; 122 z
; [plot_y, dim_y, dim_x], buffer_id label: ; mind the little-endian order when fetching these!!!
font_itc_honda:
	dl 0x000106,BUF_4128
	dl 0x000106,BUF_4128 ; Missing character 33
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
	dl 0x0E0505,BUF_4142
	dl 0x000106,BUF_4128 ; Missing character 47
	dl 0x00120A,BUF_4144
	dl 0x001204,BUF_4145
	dl 0x001209,BUF_4146
	dl 0x00120A,BUF_4147
	dl 0x00120C,BUF_4148
	dl 0x00120A,BUF_4149
	dl 0x00120A,BUF_4150
	dl 0x001208,BUF_4151
	dl 0x00120A,BUF_4152
	dl 0x00120A,BUF_4153
	dl 0x000106,BUF_4128 ; Missing character 58
	dl 0x000106,BUF_4128 ; Missing character 59
	dl 0x000106,BUF_4128 ; Missing character 60
	dl 0x000106,BUF_4128 ; Missing character 61
	dl 0x000106,BUF_4128 ; Missing character 62
	dl 0x000106,BUF_4128 ; Missing character 63
	dl 0x000106,BUF_4128 ; Missing character 64
	dl 0x01120A,BUF_4161
	dl 0x00120A,BUF_4162
	dl 0x001308,BUF_4163
	dl 0x00120A,BUF_4164
	dl 0x001208,BUF_4165
	dl 0x001208,BUF_4166
	dl 0x00120A,BUF_4167
	dl 0x00120A,BUF_4168
	dl 0x001203,BUF_4169
	dl 0x001206,BUF_4170
	dl 0x00120A,BUF_4171
	dl 0x011208,BUF_4172
	dl 0x00120E,BUF_4173
	dl 0x00120A,BUF_4174
	dl 0x00120A,BUF_4175
	dl 0x00120A,BUF_4176
	dl 0x00150A,BUF_4177
	dl 0x00120A,BUF_4178
	dl 0x001309,BUF_4179
	dl 0x00120A,BUF_4180
	dl 0x00120A,BUF_4181
	dl 0x00120A,BUF_4182
	dl 0x001210,BUF_4183
	dl 0x00120A,BUF_4184
	dl 0x01120A,BUF_4185
	dl 0x011209,BUF_4186
	dl 0x000106,BUF_4128 ; Missing character 91
	dl 0x000106,BUF_4128 ; Missing character 92
	dl 0x000106,BUF_4128 ; Missing character 93
	dl 0x000106,BUF_4128 ; Missing character 94
	dl 0x000106,BUF_4128 ; Missing character 95
	dl 0x000106,BUF_4128 ; Missing character 96
	dl 0x060C08,BUF_4193
	dl 0x011209,BUF_4194
	dl 0x060C07,BUF_4195
	dl 0x001209,BUF_4196
	dl 0x060C08,BUF_4197
	dl 0x001209,BUF_4198
	dl 0x061209,BUF_4199
	dl 0x011209,BUF_4200
	dl 0x001204,BUF_4201
	dl 0x001808,BUF_4202
	dl 0x011209,BUF_4203
	dl 0x001203,BUF_4204
	dl 0x060D0E,BUF_4205
	dl 0x060C09,BUF_4206
	dl 0x060C09,BUF_4207
	dl 0x061209,BUF_4208
	dl 0x061209,BUF_4209
	dl 0x060D06,BUF_4210
	dl 0x060D08,BUF_4211
	dl 0x030F07,BUF_4212
	dl 0x060C09,BUF_4213
	dl 0x060C09,BUF_4214
	dl 0x060C0E,BUF_4215
	dl 0x060C09,BUF_4216
	dl 0x061109,BUF_4217
	dl 0x060C09,BUF_4218

; Import .rgba bitmap files and load them into VDP buffers
load_font_itc_honda:

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

	ld hl,F046
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4142
	ld bc,5
	ld de,5
	ld ix,25
	call vdu_load_bmp2_from_file
; Missing character 47

	ld hl,F048
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4144
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F049
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4145
	ld bc,4
	ld de,18
	ld ix,72
	call vdu_load_bmp2_from_file

	ld hl,F050
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4146
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_bmp2_from_file

	ld hl,F051
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4147
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F052
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4148
	ld bc,12
	ld de,18
	ld ix,216
	call vdu_load_bmp2_from_file

	ld hl,F053
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4149
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F054
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4150
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F055
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4151
	ld bc,8
	ld de,18
	ld ix,144
	call vdu_load_bmp2_from_file

	ld hl,F056
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4152
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F057
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4153
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file
; Missing character 58
; Missing character 59
; Missing character 60
; Missing character 61
; Missing character 62
; Missing character 63
; Missing character 64

	ld hl,F065
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4161
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F066
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4162
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F067
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4163
	ld bc,8
	ld de,19
	ld ix,152
	call vdu_load_bmp2_from_file

	ld hl,F068
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4164
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F069
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4165
	ld bc,8
	ld de,18
	ld ix,144
	call vdu_load_bmp2_from_file

	ld hl,F070
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4166
	ld bc,8
	ld de,18
	ld ix,144
	call vdu_load_bmp2_from_file

	ld hl,F071
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4167
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F072
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4168
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F073
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4169
	ld bc,3
	ld de,18
	ld ix,54
	call vdu_load_bmp2_from_file

	ld hl,F074
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4170
	ld bc,6
	ld de,18
	ld ix,108
	call vdu_load_bmp2_from_file

	ld hl,F075
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4171
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F076
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4172
	ld bc,8
	ld de,18
	ld ix,144
	call vdu_load_bmp2_from_file

	ld hl,F077
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4173
	ld bc,14
	ld de,18
	ld ix,252
	call vdu_load_bmp2_from_file

	ld hl,F078
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4174
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F079
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4175
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F080
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4176
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F081
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4177
	ld bc,10
	ld de,21
	ld ix,210
	call vdu_load_bmp2_from_file

	ld hl,F082
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4178
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F083
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4179
	ld bc,9
	ld de,19
	ld ix,171
	call vdu_load_bmp2_from_file

	ld hl,F084
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4180
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F085
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4181
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F086
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4182
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F087
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4183
	ld bc,16
	ld de,18
	ld ix,288
	call vdu_load_bmp2_from_file

	ld hl,F088
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4184
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F089
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4185
	ld bc,10
	ld de,18
	ld ix,180
	call vdu_load_bmp2_from_file

	ld hl,F090
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4186
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_bmp2_from_file
; Missing character 91
; Missing character 92
; Missing character 93
; Missing character 94
; Missing character 95
; Missing character 96

	ld hl,F097
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4193
	ld bc,8
	ld de,12
	ld ix,96
	call vdu_load_bmp2_from_file

	ld hl,F098
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4194
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_bmp2_from_file

	ld hl,F099
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4195
	ld bc,7
	ld de,12
	ld ix,84
	call vdu_load_bmp2_from_file

	ld hl,F100
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4196
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_bmp2_from_file

	ld hl,F101
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4197
	ld bc,8
	ld de,12
	ld ix,96
	call vdu_load_bmp2_from_file

	ld hl,F102
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4198
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_bmp2_from_file

	ld hl,F103
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4199
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_bmp2_from_file

	ld hl,F104
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4200
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_bmp2_from_file

	ld hl,F105
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4201
	ld bc,4
	ld de,18
	ld ix,72
	call vdu_load_bmp2_from_file

	ld hl,F106
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4202
	ld bc,8
	ld de,24
	ld ix,192
	call vdu_load_bmp2_from_file

	ld hl,F107
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4203
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_bmp2_from_file

	ld hl,F108
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4204
	ld bc,3
	ld de,18
	ld ix,54
	call vdu_load_bmp2_from_file

	ld hl,F109
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4205
	ld bc,14
	ld de,13
	ld ix,182
	call vdu_load_bmp2_from_file

	ld hl,F110
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4206
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_bmp2_from_file

	ld hl,F111
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4207
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_bmp2_from_file

	ld hl,F112
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4208
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_bmp2_from_file

	ld hl,F113
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4209
	ld bc,9
	ld de,18
	ld ix,162
	call vdu_load_bmp2_from_file

	ld hl,F114
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4210
	ld bc,6
	ld de,13
	ld ix,78
	call vdu_load_bmp2_from_file

	ld hl,F115
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4211
	ld bc,8
	ld de,13
	ld ix,104
	call vdu_load_bmp2_from_file

	ld hl,F116
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4212
	ld bc,7
	ld de,15
	ld ix,105
	call vdu_load_bmp2_from_file

	ld hl,F117
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4213
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_bmp2_from_file

	ld hl,F118
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4214
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_bmp2_from_file

	ld hl,F119
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4215
	ld bc,14
	ld de,12
	ld ix,168
	call vdu_load_bmp2_from_file

	ld hl,F120
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4216
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_bmp2_from_file

	ld hl,F121
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4217
	ld bc,9
	ld de,17
	ld ix,153
	call vdu_load_bmp2_from_file

	ld hl,F122
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_4218
	ld bc,9
	ld de,12
	ld ix,108
	call vdu_load_bmp2_from_file

	ret

F032: db "fonts/honda/032.rgba2",0
F046: db "fonts/honda/046.rgba2",0
F048: db "fonts/honda/048.rgba2",0
F049: db "fonts/honda/049.rgba2",0
F050: db "fonts/honda/050.rgba2",0
F051: db "fonts/honda/051.rgba2",0
F052: db "fonts/honda/052.rgba2",0
F053: db "fonts/honda/053.rgba2",0
F054: db "fonts/honda/054.rgba2",0
F055: db "fonts/honda/055.rgba2",0
F056: db "fonts/honda/056.rgba2",0
F057: db "fonts/honda/057.rgba2",0
F065: db "fonts/honda/065.rgba2",0
F066: db "fonts/honda/066.rgba2",0
F067: db "fonts/honda/067.rgba2",0
F068: db "fonts/honda/068.rgba2",0
F069: db "fonts/honda/069.rgba2",0
F070: db "fonts/honda/070.rgba2",0
F071: db "fonts/honda/071.rgba2",0
F072: db "fonts/honda/072.rgba2",0
F073: db "fonts/honda/073.rgba2",0
F074: db "fonts/honda/074.rgba2",0
F075: db "fonts/honda/075.rgba2",0
F076: db "fonts/honda/076.rgba2",0
F077: db "fonts/honda/077.rgba2",0
F078: db "fonts/honda/078.rgba2",0
F079: db "fonts/honda/079.rgba2",0
F080: db "fonts/honda/080.rgba2",0
F081: db "fonts/honda/081.rgba2",0
F082: db "fonts/honda/082.rgba2",0
F083: db "fonts/honda/083.rgba2",0
F084: db "fonts/honda/084.rgba2",0
F085: db "fonts/honda/085.rgba2",0
F086: db "fonts/honda/086.rgba2",0
F087: db "fonts/honda/087.rgba2",0
F088: db "fonts/honda/088.rgba2",0
F089: db "fonts/honda/089.rgba2",0
F090: db "fonts/honda/090.rgba2",0
F097: db "fonts/honda/097.rgba2",0
F098: db "fonts/honda/098.rgba2",0
F099: db "fonts/honda/099.rgba2",0
F100: db "fonts/honda/100.rgba2",0
F101: db "fonts/honda/101.rgba2",0
F102: db "fonts/honda/102.rgba2",0
F103: db "fonts/honda/103.rgba2",0
F104: db "fonts/honda/104.rgba2",0
F105: db "fonts/honda/105.rgba2",0
F106: db "fonts/honda/106.rgba2",0
F107: db "fonts/honda/107.rgba2",0
F108: db "fonts/honda/108.rgba2",0
F109: db "fonts/honda/109.rgba2",0
F110: db "fonts/honda/110.rgba2",0
F111: db "fonts/honda/111.rgba2",0
F112: db "fonts/honda/112.rgba2",0
F113: db "fonts/honda/113.rgba2",0
F114: db "fonts/honda/114.rgba2",0
F115: db "fonts/honda/115.rgba2",0
F116: db "fonts/honda/116.rgba2",0
F117: db "fonts/honda/117.rgba2",0
F118: db "fonts/honda/118.rgba2",0
F119: db "fonts/honda/119.rgba2",0
F120: db "fonts/honda/120.rgba2",0
F121: db "fonts/honda/121.rgba2",0
F122: db "fonts/honda/122.rgba2",0
