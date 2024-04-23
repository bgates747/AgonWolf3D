; 1 Shift
    bit 0,(ix+0)
    jr z,@Shift
@Shift:
; 2 Ctrl
    bit 1,(ix+0)
    jr z,@Ctrl
@Ctrl:
; 3 Alt
    bit 2,(ix+0)
    jr z,@Alt
@Alt:
; 4 LeftShift
    bit 3,(ix+0)
    jr z,@LeftShift
@LeftShift:
; 5 LeftCtrl
    bit 4,(ix+0)
    jr z,@LeftCtrl
@LeftCtrl:
; 6 LeftAlt
    bit 5,(ix+0)
    jr z,@LeftAlt
@LeftAlt:
; 7 RightShift
    bit 6,(ix+0)
    jr z,@RightShift
@RightShift:
; 8 RightCtrl
    bit 7,(ix+0)
    jr z,@RightCtrl
@RightCtrl:
; 9 RightAlt
    bit 0,(ix+1)
    jr z,@RightAlt
@RightAlt:
; 10 MouseSelect
    bit 1,(ix+1)
    jr z,@MouseSelect
@MouseSelect:
; 11 MouseMenu
    bit 2,(ix+1)
    jr z,@MouseMenu
@MouseMenu:
; 12 MouseAdjust
    bit 3,(ix+1)
    jr z,@MouseAdjust
@MouseAdjust:
; 17 Q
    bit 0,(ix+2)
    jr z,@Q
@Q:
; 18 Num3
    bit 1,(ix+2)
    jr z,@Num3
@Num3:
; 19 Num4
    bit 2,(ix+2)
    jr z,@Num4
@Num4:
; 20 Num5
    bit 3,(ix+2)
    jr z,@Num5
@Num5:
; 21 F4
    bit 4,(ix+2)
    jr z,@F4
@F4:
; 22 Num8
    bit 5,(ix+2)
    jr z,@Num8
@Num8:
; 23 F7
    bit 6,(ix+2)
    jr z,@F7
@F7:
; 24 Minus
    bit 7,(ix+2)
    jr z,@Minus
@Minus:
; 25 Hat
    bit 0,(ix+3)
    jr z,@Hat
@Hat:
; 26 Left
    bit 1,(ix+3)
    jr z,@Left
@Left:
; 27 Kpd6
    bit 2,(ix+3)
    jr z,@Kpd6
@Kpd6:
; 28 Kpd7
    bit 3,(ix+3)
    jr z,@Kpd7
@Kpd7:
; 29 F11
    bit 4,(ix+3)
    jr z,@F11
@F11:
; 30 F12
    bit 5,(ix+3)
    jr z,@F12
@F12:
; 31 F10
    bit 6,(ix+3)
    jr z,@F10
@F10:
; 32 ScrollLock
    bit 7,(ix+3)
    jr z,@ScrollLock
@ScrollLock:
; 33 F0
    bit 0,(ix+4)
    jr z,@F0
@F0:
; 34 W
    bit 1,(ix+4)
    jr z,@W
@W:
; 35 E
    bit 2,(ix+4)
    jr z,@E
@E:
; 36 T
    bit 3,(ix+4)
    jr z,@T
@T:
; 37 Num7
    bit 4,(ix+4)
    jr z,@Num7
@Num7:
; 38 I
    bit 5,(ix+4)
    jr z,@I
@I:
; 39 Num9
    bit 6,(ix+4)
    jr z,@Num9
@Num9:
; 40 Num0
    bit 7,(ix+4)
    jr z,@Num0
@Num0:
; 41 Underscore
    bit 0,(ix+5)
    jr z,@Underscore
@Underscore:
; 42 Down
    bit 1,(ix+5)
    jr z,@Down
@Down:
; 43 Kpd8
    bit 2,(ix+5)
    jr z,@Kpd8
@Kpd8:
; 44 Kpd9
    bit 3,(ix+5)
    jr z,@Kpd9
@Kpd9:
; 45 Break
    bit 4,(ix+5)
    jr z,@Break
@Break:
; 46 Tilde
    bit 5,(ix+5)
    jr z,@Tilde
@Tilde:
; 48 Backspace
    bit 7,(ix+5)
    jr z,@Backspace
@Backspace:
; 49 Num1
    bit 0,(ix+6)
    jr z,@Num1
@Num1:
; 50 Num2
    bit 1,(ix+6)
    jr z,@Num2
@Num2:
; 51 D
    bit 2,(ix+6)
    jr z,@D
@D:
; 52 R
    bit 3,(ix+6)
    jr z,@R
@R:
; 53 Num6
    bit 4,(ix+6)
    jr z,@Num6
@Num6:
; 54 U
    bit 5,(ix+6)
    jr z,@U
@U:
; 55 O
    bit 6,(ix+6)
    jr z,@O
@O:
; 56 P
    bit 7,(ix+6)
    jr z,@P
@P:
; 57 LeftBracket
    bit 0,(ix+7)
    jr z,@LeftBracket
@LeftBracket:
; 58 Up
    bit 1,(ix+7)
    jr z,@Up
@Up:
; 59 KpdPlus
    bit 2,(ix+7)
    jr z,@KpdPlus
@KpdPlus:
; 60 KpdMinus
    bit 3,(ix+7)
    jr z,@KpdMinus
@KpdMinus:
; 61 KpdEnter
    bit 4,(ix+7)
    jr z,@KpdEnter
@KpdEnter:
; 62 Insert
    bit 5,(ix+7)
    jr z,@Insert
@Insert:
; 63 Home
    bit 6,(ix+7)
    jr z,@Home
@Home:
; 64 PgUp
    bit 7,(ix+7)
    jr z,@PgUp
@PgUp:
; 65 Caps
    bit 0,(ix+8)
    jr z,@Caps
@Caps:
; 66 A
    bit 1,(ix+8)
    jr z,@A
@A:
; 67 X
    bit 2,(ix+8)
    jr z,@X
@X:
; 68 F
    bit 3,(ix+8)
    jr z,@F
@F:
; 69 Y
    bit 4,(ix+8)
    jr z,@Y
@Y:
; 70 J
    bit 5,(ix+8)
    jr z,@J
@J:
; 71 K
    bit 6,(ix+8)
    jr z,@K
@K:
; 72 At
    bit 7,(ix+8)
    jr z,@At
@At:
; 73 Colon
    bit 0,(ix+9)
    jr z,@Colon
@Colon:
; 74 Return
    bit 1,(ix+9)
    jr z,@Return
@Return:
; 75 KpdFwdSlash
    bit 2,(ix+9)
    jr z,@KpdFwdSlash
@KpdFwdSlash:
; 76 KpdDel
    bit 3,(ix+9)
    jr z,@KpdDel
@KpdDel:
; 77 KpdDot
    bit 4,(ix+9)
    jr z,@KpdDot
@KpdDot:
; 78 NumLock
    bit 5,(ix+9)
    jr z,@NumLock
@NumLock:
; 79 PgDn
    bit 6,(ix+9)
    jr z,@PgDn
@PgDn:
; 81 ShiftLock
    bit 0,(ix+10)
    jr z,@ShiftLock
@ShiftLock:
; 82 S
    bit 1,(ix+10)
    jr z,@S
@S:
; 83 C
    bit 2,(ix+10)
    jr z,@C
@C:
; 84 G
    bit 3,(ix+10)
    jr z,@G
@G:
; 85 H
    bit 4,(ix+10)
    jr z,@H
@H:
; 86 N
    bit 5,(ix+10)
    jr z,@N
@N:
; 87 L
    bit 6,(ix+10)
    jr z,@L
@L:
; 88 Semicolon
    bit 7,(ix+10)
    jr z,@Semicolon
@Semicolon:
; 89 RightBracket
    bit 0,(ix+11)
    jr z,@RightBracket
@RightBracket:
; 90 Delete
    bit 1,(ix+11)
    jr z,@Delete
@Delete:
; 92 KpdStar
    bit 3,(ix+11)
    jr z,@KpdStar
@KpdStar:
; 93 KpdComma
    bit 4,(ix+11)
    jr z,@KpdComma
@KpdComma:
; 94 KpdPlus
    bit 5,(ix+11)
    jr z,@KpdPlus
@KpdPlus:
; 96 Underscore1
    bit 7,(ix+11)
    jr z,@Underscore1
@Underscore1:
; 97 Tab
    bit 0,(ix+12)
    jr z,@Tab
@Tab:
; 98 Z
    bit 1,(ix+12)
    jr z,@Z
@Z:
; 99 Space
    bit 2,(ix+12)
    jr z,@Space
@Space:
; 100 V
    bit 3,(ix+12)
    jr z,@V
@V:
; 101 B
    bit 4,(ix+12)
    jr z,@B
@B:
; 102 M
    bit 5,(ix+12)
    jr z,@M
@M:
; 103 Comma
    bit 6,(ix+12)
    jr z,@Comma
@Comma:
; 104 Dot
    bit 7,(ix+12)
    jr z,@Dot
@Dot:
; 105 ForwardSlash
    bit 0,(ix+13)
    jr z,@ForwardSlash
@ForwardSlash:
; 106 CopyEnd
    bit 1,(ix+13)
    jr z,@CopyEnd
@CopyEnd:
; 107 Kpd0
    bit 2,(ix+13)
    jr z,@Kpd0
@Kpd0:
; 108 Kpd1
    bit 3,(ix+13)
    jr z,@Kpd1
@Kpd1:
; 109 Kpd3
    bit 4,(ix+13)
    jr z,@Kpd3
@Kpd3:
; 113 Escape
    bit 0,(ix+14)
    jr z,@Escape
@Escape:
; 114 F1
    bit 1,(ix+14)
    jr z,@F1
@F1:
; 115 F2
    bit 2,(ix+14)
    jr z,@F2
@F2:
; 116 F3
    bit 3,(ix+14)
    jr z,@F3
@F3:
; 117 F5
    bit 4,(ix+14)
    jr z,@F5
@F5:
; 118 F6
    bit 5,(ix+14)
    jr z,@F6
@F6:
; 119 F8
    bit 6,(ix+14)
    jr z,@F8
@F8:
; 120 F9
    bit 7,(ix+14)
    jr z,@F9
@F9:
; 122 Right
    bit 1,(ix+15)
    jr z,@Right
@Right:
; 123 Kpd4
    bit 2,(ix+15)
    jr z,@Kpd4
@Kpd4:
; 124 Kpd5
    bit 3,(ix+15)
    jr z,@Kpd5
@Kpd5:
; 125 Kpd2
    bit 4,(ix+15)
    jr z,@Kpd2
@Kpd2:
; 126 WinLeft
    bit 5,(ix+15)
    jr z,@WinLeft
@WinLeft:
; 127 WinRight
    bit 6,(ix+15)
    jr z,@WinRight
@WinRight:
; 128 WinMenu
    bit 7,(ix+15)
    jr z,@WinMenu
@WinMenu: