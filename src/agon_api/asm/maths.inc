; #### BEGIN lib_bcd STUFF

; these are sample scratch memory defintions
; for add/sub_bcd routines
; they can be used as-is or renamed
add_bcd_arg1: db #00,#00,#00,#00
add_bcd_arg2: db #00,#00,#00,#00

; set bcd values in a scratch memory address from registers bcde
; input: hl; scratch address,bcde; 8-place bcd number
; destroys ; hl
set_bcd:
    ld (hl),e
    inc hl
    ld (hl),d
    inc hl
    ld (hl),c
    inc hl
    ld (hl),b
    ret

; load bcd values from a scratch memory address to bcde
; input: hl; scratch address
; output: bcde; 8-place bcd number
; destroys: hl
get_bcd:
    ld e,(hl)
    inc hl
    ld d,(hl)
    inc hl
    ld c,(hl)
    inc hl
    ld b,(hl)
    ret

; BCD addition
; inputs: (hl) and (de) point to BCD numbers of equal length (divisible by 2)
;       a is the number of bytes holding each number (number of places/2)
; outputs: (hl) + (de) --> (hl)
; destroys: a,b,de,hl
add_bcd:
    ld b,a ; loop counter
    xor a ; reset a,clear carry flag
adcec: 
    ld a,(de) ; addend to acc
    adc a,(hl) ; add (hl) to acc
    daa ; adjust result to bcd
    ld (hl),a ; store result
    inc hl ; advance memory pointers
    inc de
    djnz adcec ; loop until b == 0
    ret ; fall through 

; ###### STUFF FROM lib_math_88 ######
; http://www.z80.info/pseudo-random.txt
rand_8:
    push bc
    ld a,(r_seed)
    ld c,a 

    rrca ; multiply by 32
    rrca
    rrca
    xor 0x1f

    add a,c
    sbc a,255 ; carry

    ld (r_seed),a
    pop bc
    ret
r_seed: defb $50


; ; MOVED TO maths24.inc
; ; a convenience function to convert cartesian
; ; to polar coordinates
; ; inputs: bc and de as y0,x0 and y1,x1,8-bit integers
; ; returns: b.c as angle in degrees 256 8.8 fixed
; ;          de as the radius in pixels,***16-bit integer***
; ; destroys: everything except indexes
; cartesian_to_polar:
; ; get the distance
;     call distance16game
;     push de ; save the result
; ; time to get our angle,which is a simple atan2 operation
;     ld bc,(distance16game_dx2) ; distance16game populated these
;     ld de,(distance16game_dy2) ; ....
;     call atan2_88
;     ld b,h ; h.l is our angle,
;     ld c,l ; and it needs to go back as b.c
;     pop de ; and de needs to go back as the radius
;     ret ; easy peasy


; ; MOVED TO maths24.inc
; ; 8.8 fixed inputs / outputs
; ; takes: b.c as angle in degrees 256
; ;        d.e as radius
; ; returns b.c as dx,d.e as dy 
; ;        displacements from origin (0,0)
; ; destroys: everything except indexes
; polar_to_cartesian:
;     push bc
;     push de
;     call cos_bc
;     pop de
;     pop bc
;     call neg_hl ; invert it
;     push hl ; store it
;     push bc
;     push de
;     call sin_bc
;     pop de
;     pop bc 
; ; compute dx = sin(bc) * de
;     ld b,h
;     ld c,l
;     push de
;     call BC_Mul_DE_88
;     ld b,h
;     ld c,l
;     pop de ; radius
;     pop hl ; -cos(bc)
;     push bc ; save dx
; ; compute dy = -cos(bc) * de
;     ld b,h
;     ld c,l
;     call BC_Mul_DE_88
;     ex de,hl ; return dy
;     pop bc ; restore dx
; ; and out
;     ret

; ; MOVED TO maths24.inc
; ; atan2(bcu,deu)
; ; inputs: ub.c as y, ud.e as x
; ;   whether inputs are integers or fractional doesn't matter
; ;   as long as the sign bit of the upper byte is correct
; ; returns h.l as 8.8 fixed result in degrees 256
; ;   note: hlu will always return as zero
; ; angles are COMPASS HEADINGS based on
; ; screen coordinate conventions,where the y axis is flipped
; ; #E0 315      0       45 #20
; ;        -x,-y | +x,-y
; ; #C0 270------+------ 90 #40
; ;        -x,+y | +x,+y
; ; #A0 225   180 #80   135 #60
; atan2_88:
; ; get signs and make everything positive
; ; get abs(x) and store its original sign
;     push bc
;     pop hl
;     call abs_hlu ; if x was negative this also sets the sign flag
;     push af ; store sign of x
;     pop bc ; bc = abs(x)
; ; get abs(y) and store its original sign
;     ex de,hl ; hl = y
;     call abs_hlu ; if y was negative this also sets the sign flag
;     push af ; store sign of y
;     ex de,hl ; de = abs(y)
; ; if bc < de,then we do bc/de,otherwise de/bc
;     and a ; clear the carry flag
;     push de
;     pop hl
;     sbc hl,bc
;     push af ; save bc < de
;     jp p,@1 ; bc < de, so we skip ahead
;     ; otherwise we swap bc and de
;     push bc
;     pop hl
;     ex de,hl
;     push hl
;     pop bc
; @1:
; ; now we're ready to snag our preliminary result
;     call atan_88_game ; hl comes back with prelim result
; ; now we adjust hl based on bc < de
;     pop af
;     jp p,@2 ; bc < de,so we skip ahead
;     ex de,hl
;     ld hl,0x004000 ; 90 degrees
;     and a ; clear the carry flag
;     sbc hl,de ; subtract result from 90 degrees
; @2:
; ; now the fun part of adjusting the result
; ; based on which quadrant (x,y) is in
; ; #E0 315      0       45 #20
; ;        -x,-y | +x,-y
; ; #C0 270------+------ 90 #40
; ;        -x,+y | +x,+y
; ; #A0 225   180 #80   135 #60
;     pop af ; sign of y
;     jp z,@y_zero
;     jp p,@y_pos
;     ; y neg,check x
;     pop af ; sign of x
;     jp z,@y_neg_x_zero
;     jp p,@y_neg_x_pos
;     ; y neg,x neg
;     ; angle is 270-360
;     ; negating the intermediate does the trick
;     call neg_hl
;     ret
; @y_neg_x_zero:
;     ; y neg,x zero
;     ; angle is 0
;     ld hl,0
;     ret
; @y_neg_x_pos:
;     ; y neg,x pos
;     ; angle is 0 to 90
;     ; so we're good
;     ret
; @y_pos:
;     pop af ; sign of x
;     jp z,@y_pos_x_zero
;     jp p,@y_pos_x_pos

;     ; y pos,x neg
;     ; angle is 180-270
;     ; so we add 180 to intermediate
;     ld de,0x008000
;     add hl,de
;     ret
; @y_pos_x_zero:
;     ; y pos,x zero
;     ; angle is 180
;     ld hl,0x008000
;     ret
; @y_pos_x_pos:
;     ; y pos,x pos
;     ; angle is 90-180
;     ; neg the intermediate and add 180 degrees
;     call neg_hl
;     ld de,0x008000
;     add hl,de
;     ret
; @y_zero:
;     pop af ; sign of x
;     jp m,@y_zero_x_neg
;     ; y zero,x pos
;     ; angle is 90,nothing to do
;     ret
; @y_zero_x_neg:
;     ; y zero ,x neg
;     ; angle is 270
;     ld hl,0x00C000
;     ret

; ; SUPERCEDED BY atan2_168 IN maths24.inc
; ; deviates from the standard function in lib_math_88
; ; by dropping the interpolation step for performance
; ; atan(b.c,d.e) --> h.l where b.c / d.e = tan(theta)
; ; in the normal world this would be de/bc (y/x)
; ; but we use compass headings in these parts 
; ; well shit,and we flip the sign of y as well
; ; because that's how screen coordinates work
; ; ONLY WORKS FOR POSITIVE VALUES OF BC AND DE
; ; I.E. FROM 0 TO 45 DEGREES
; ; outputs: h.l as 8.8 representation of degrees256
; ; destroys: everything except ix,iy
; atan_88_game:
; ; because we use compass headings instead of radians:
; ; we compute b.c/d.e = x/y
; ; which is 1/tan(theta) in the normal world
;     call div_88
; ; if bc = de then we have hl = 1 or tan(1),which is: #20.00 (45 degrees decimal)
;     ld a,h ; just need the high byte 
;     sub 1
;     jr z,atan_88_game_45
; ; build an index for the atan_lut
;     ; there are 32 entries in the lookup table
;     ; representing 0 <= tan(theta) < 1
;     ; plus one entry for tan = 1 for the interpolator
;     ; series begins at 0,add 1/32 for next in series
;     ; at two bytes per entry,h.l / 4 gives us our index
;     ld a,l ; all we need is the fractional part
;     ; while we're here,if hl = 0 then we have tan(0),which is zero
;     and a
;     jr z,atan_88_game_00
;     ; otherwise we forge ahead
;     rrca ; divide a
;     rrca ; by 4
;     ; mask off the high bits that rotated in
;     and %00111110 ; and the low bit to ensure a is even
;     ld hl,atan_lut ; address of first entry
;     add a,l ; now we bump hl by the index 
;     ld l,a
;     ld a,h
;     adc a,0
;     ld h,a
;     ; now hl has the index
;     ld e,(hl) ; low byte comes first
;     inc hl ; now to the high byte
;     ld d,(hl)
;     ex de,hl
;     ret

; ; for the case tan(1)
; atan_88_game_45:
;     ld hl,#2000 ; 45 degrees decimal
;     ret

; ; for the case tan(0)
; atan_88_game_00:
;     ld hl,0
;     ret

; ; SUPERCEDED BY atan2_lut_168 IN maths24.inc
; atan_lut: 
;     defw #0000,#0146,#028B,#03CF,#0511,#0651,#078D,#08C6
;     defw #09FB,#0B2C,#0C57,#0D7D,#0E9E,#0FB9,#10CE,#11DC
;     defw #12E4,#13E6,#14E0,#15D5,#16C2,#17AA,#188A,#1964
;     defw #1A38,#1B05,#1BCD,#1C8E,#1D4A,#1DFF,#1EB0,#1F5A
;     ; defw #2000

; ; SUPERCEDED BY cos168 IN maths24.inc
; ; fixed 8.8 routine
; ; cos(b.c) --> h.l
; ; destroys: everything but indexes
; cos_bc:
; ; for cos we simply increment the angle by 90 degrees
; ; or 40h in degrees256
; ; which makes it a sin problem
;     ld a,#40
;     add a,b
;     ld b,a
;     call sin_bc
;     ret

; ; SUPERCEDED BY sin_lut_168 IN maths24.inc
; ; these values represent the fixed 8.8 fractional portion of the sine function
; ; for degrees256 0 to 61 decimal (0 to 85.78 degrees360 decimal). anything larger
; ; than that and the answer is 1.00,which would take two bytes to represent in 8.8
; sin_lut:
;     defb #00,#06,#0D,#13,#19,#1F,#26,#2C,#32,#38,#3E,#44,#4A,#50,#56,#5C
;     defb #62,#68,#6D,#73,#79,#7E,#84,#89,#8E,#93,#98,#9D,#A2,#A7,#AC,#B1
;     defb #B5,#B9,#BE,#C2,#C6,#CA,#CE,#D1,#D5,#D8,#DC,#DF,#E2,#E5,#E7,#EA
;     defb #ED,#EF,#F1,#F3,#F5,#F7,#F8,#FA,#FB,#FC,#FD,#FE,#FF,#FF ; no need to store the rest

; ; SUPERCEDED BY sin168 IN maths24.inc
; ; fixed 8.8 routine
; ; sin(b.c) --> h.l
; ; destroys: everything but indexes
; sin_bc:
; ; apply quadrant-based rules to angle b
;     ld a,b
;     cp 192
;     jr nc,sin_bc_192
;     cp 128
;     jr nc,sin_bc_128
;     cp 64
;     jr nc,sin_bc_64
; ; fall through

; ; 0 <= b <= 63
; ; no manipulations required
;     call trig_bc_game
;     ret

; ; 64 <= b <= 127
; ; we compute sin(128-b.c)
; sin_bc_64:
;     ; ; the easy to understand way
;     ; ld h,128 ; 7 2
;     ; ld l,0 ; 7 2
;     ; and a ; clear the carry flag ; 4 1
;     ; sbc hl,bc ; 15 2
;     ; ld c,l ; 4 1
;     ; ld b,h ; 4 1
;     ;         ; 41 9

;     ; the using our thinking cap more efficient way
;     ld a,c ; 4 1
;     neg ; 8 1
;     ld c,a ; 4 1
;     ld a,128 ; 7 2
;     sbc a,b ; 4 1
;     ld b,a ; 4 1
;             ; 31 7
;     call trig_bc_game
;     ret

; ; 128 <= b <= 191
; ; we compute -sin(b.c-128)
; sin_bc_128:
;     sub 128 ; a already has b
;     ld b,a
;     call trig_bc_game
;     call neg_hl
;     ret

; ; 192 <= b <= 255
; ; we compute -sin(-b.c)
; sin_bc_192:
; ; neg b.c
;     xor a ; 4 1
;     sub c ; 4 1
;     ld c,a ; 4 1
;     sbc a,a ; 4 1
;     sub b ; 4 1
;     ld b,a ; 4 1
;     ;       24 5
;     call trig_bc_game
;     call neg_hl
;     ret

; ; SUPERCEDED BY cos168 IN maths24.inc
; ; deviates from the standard trig_bc in lib_math_88
; ; by dropping the interpolation routine and thus only
; ; returning the values for whole angles
; trig_bc_game:
; ; right off the bat,if b > 61,the answer is 1 and we can go home
;     ld hl,256
;     ld a,61
;     cp b
;     ret c
; ; set de to the address of the value we want from sin_lut
;     ld de,sin_lut ; base address of the table
;     ld a,b
;     add a,e
;     ld e,a
;     ld a,0 ; can't xor it because we need carry flag
;     adc a,d
;     ld d,a
;     ld a,(de) ; now grab the lookup value
;     ld l,a ; store the fractional part
;     ld h,0 ; this is the integer part,which will always be 0 if we got this far
;     ret

; absolute value of hl
; destroys: a,hl
; S1 if result is negative,S0 if positive or zero
abs_hl:
    xor a ; zero a and clear flags
    bit 7,h ; test the sign bit
    ret z ; if positive,we're done
    ; otherwise fall through and negate hl

; flip the sign of hl
; destroys a,hl
; S1 if result is negative,S0 if positive or zero
neg_hl:
    xor a
    sub l
    ld l,a
    sbc a,a
    sub h
    ld h,a
    ret

; fixed 8.8 routine
; multiplies B.C by D.E,stores the result in H.L 
; http://z80-heaven.wikidot.com/advanced-math
BC_Mul_DE_88:
; from 242 byes unrolled,to 88 bytes rolled,
; to 76 bytes converting all to b.c * d.e = h.l
; First,find out if the output is positive or negative
    ld a,b
    xor d
    push af   ;sign bit is the result sign bit

; Now make sure the inputs are positive
    xor d     ;A now has the value of H,since I XORed it with D twice (cancelling)
    jp p,BC_Mul_DE_88_1   ;if Positive,don't negate
    xor a
    sub c
    ld c,a
    sbc a,a
    sub b
    ld b,a
BC_Mul_DE_88_1:
    bit 7,d
    jr z,BC_Mul_DE_88_2
    xor a
    sub e
    ld e,a
    sbc a,a
    sub d
    ld d,a
BC_Mul_DE_88_2:
    call mul16
;Need to round,so get the top bit of L
    sla l ; if bit7 was set,this sets carry flag,which is all we want

;Get the middle two bytes,EH,and put them in HL
    ld l,h ; this overwrites the shifted l
    ld h,e ; copying continues as advertised

    ld a,d ; we save d to check for overflow later
    ld de,0 ;
    adc hl,de

;check for overflow!
;We should check for overflow. If A>0,we will set HL to 0x7FFF
    adc a,e ; this is d + e with carry
    jr c,$+4  ; and if that carries out,jump to overflow
    jr z,BC_Mul_DE_88_3
    ld hl,$7FFF
BC_Mul_DE_88_3:

; Now we need to restore the sign
    pop af
    ret p    ;don't need to do anything,result is already positive
    xor a
    sub l
    ld l,a
    sbc a,a
    sub h
    ld h,a
    ret

; This routine performs the operation DEHL=BC*DE
; If multiplicands were two 8.8 fixed numbers
; result will be a 16.16 fixed number
mul16_signed:
; First,find out if the output is positive or negative
    ld a,b
    xor d
    push af   ;sign bit is the result sign bit

; Now make sure the inputs are positive
    xor d     ;A now has the value of H,since I XORed it with D twice (cancelling)
    jp p,mul16_signed_1   ;if Positive,don't negate
    xor a
    sub c
    ld c,a
    sbc a,a
    sub b
    ld b,a
mul16_signed_1:
    bit 7,d
    jr z,mul16_signed_2
    xor a
    sub e
    ld e,a
    sbc a,a
    sub d
    ld d,a
mul16_signed_2:
    call mul16
; Now we need to restore the sign
    pop af
    ret p    ;don't need to do anything,result is already positive
    call neg_DEHL ; otherwise flip that sign
    ret


; flip the sign of dehl
; destroys a,hl,de
neg_DEHL:
; hl first
    xor a
    sub l
    ld l,a
    sbc a,a
    sub h
    ld h,a
; now de
    ld a,-1
    xor e
    ld e,a
    ld a,-1
    xor d
    ld d,a
    ret

; https://tutorials.eeems.ca/Z80ASM/part4.htm#mul16
; This routine performs the operation DEHL=BC*DE
; If multiplicands were two 8.8 fixed numbers
; result will be a 16.16 fixed number
; WARNING: for correct handling of sign use mul16_signed
; which calls this routine and properly signs the result
mul16:                    
    ld hl,0
    ld a,16
mul16Loop:
    add hl,hl
    rl e
    rl d
    jp nc,Nomul16
    add hl,bc
    jp nc,Nomul16
    inc de ; This instruction (with the jump) is like an "ADC DE,0"
Nomul16:
    dec a
    jp nz,mul16Loop
    ret

; makes hl the same sign as the carry flags
; destroys: a,hl
hl_set_sign_cy:
    jr nc,hl_set_sign_cy_pos
    ld a,h
    rla
    ret c
    call neg_hl
    ret
hl_set_sign_cy_pos:
    ld a,h
    rla
    ret nc
    call neg_hl
    ret

; makes hl the same sign as a
; destroys a,hl
hl_set_sign_a:
    call get_sign_a
    ret z ; a is zero so we leave things lie
    jp m,hl_set_sign_a_neg ; a is negative
    ; otherwise a is positive,now we check the sign of h
    ld a,h
    call get_sign_a
    ret p ; so is hl so nothing more to do
    call neg_hl ; otherwise we neg hl
    ret ; and out
hl_set_sign_a_neg:
    ; check the sign of h
    ld a,h
    call get_sign_a
    ret m ; hl is also negative so nothing to do
    call neg_hl ; otherwise we neg hl
    ret ; and out

; tests the sign of hl
; returns: a in [-1,0,1]
;   sign and zero flags as expected
;   hl is untouched
; GPT-4 wrote most of this. the or l was inspired. it did bit 7,a instead of h
; and it left the zero flag set after ld a,1,which i fixed by anding it
get_sign_hl:
    ld a,h             ; Load the high byte of HL into A
    or l                ; OR with the low byte to check if HL is zero
    ret z               ; Return if HL is zero

    ld a,-1             ; Send A back as -1 if the sign flag is set
    bit 7,h            ; Test the sign bit (7th bit) of the high byte
    ret nz              ; If set,HL is negative,return with the sign flag set

    ld a,1             ; Otherwise,HL is positive
    and a               ; Reset the zero flag
    ret                 ; Return with A set to 1


; https://map.grauw.nl/articles/mult_div_shifts.php
; Divide 16-bit values (with 16-bit result)
; In: Divide BC by divider DE
; Out: BC = result,HL = rest
; unsigned 16-bit division with 16-bit result and 16-bit remainder
div_16:
    ld hl,0
    ld a,b
    ld b,8
@loop1:
    rla
    adc hl,hl
    sbc hl,de
    jr nc,@noadd1
    add hl,de
@noadd1:
    djnz @loop1
    rla
    cpl
    ld b,a
    ld a,c
    ld c,b
    ld b,8
@loop2:
    rla
    adc hl,hl
    sbc hl,de
    jr nc,@noadd2
    add hl,de
@noadd2:
    djnz @loop2
    rla
    cpl
    ld b,c
    ld c,a
    ret

;Inputs:
;     DE,BC are 8.8 Fixed Point numbers
;Outputs:
;     HL is the 8.8 Fixed Point result (rounded to the least significant bit)
div_88:
; https://github.com/Zeda/Z80-Optimized-Routines/blob/master/math/division/divfixed_88.z80
; -------------------
; mod by me: 
; -1st: in ADL mode we need to make sure bcu and deu are zero
    ld hl,0
    ld h,b
    ld l,c
    push hl
    pop bc
    ld hl,0
    ld h,d
    ld l,e
    push hl
    pop de
; Zeroth,is de zero?
    ld a,0
    cp e
    jr nz,div_88_start
    cp d
    jr nz,div_88_start
    ld hl,0
    ret
; end mod by me
; -------------------
div_88_start:
; First,find out if the output is positive or negative
    ld a,b
    xor d
    push af   ;sign bit is the result sign bit

; Now make sure the inputs are positive
    xor d     ;A now has the value of B,since I XORed it with D twice (cancelling)
    jp p,div_88_1   ;if Positive,don't negate

    xor a
    sub c
    ld c,a
    sbc a,a
    sub b
    ld b,a

div_88_1:
;now make DE negative to optimize the remainder comparison
    ld a,d
    or d
    jp m,div_88_2

    xor a
    sub e
    ld e,a
    sbc a,a
    sub d
    ld d,a

div_88_2:
;if DE is 0,we can call it an overflow
;A is the current value of D
  or e
  jr z,div_88_overflow

;The accumulator gets set to B if no overflow.
;We can use H=0 to save a few cc in the meantime
    ld h,0

;if B+DE>=0,then we'll have overflow
    ld a,b
    add a,e
    ld a,d
    adc a,h
    jr c,div_88_overflow

;Now we can load the accumulator/remainder with B
;H is already 0
    ld l,b
    ld a,c
    call div_88_sub

    ld c,a
    ld a,b      ;A is now 0
    call div_88_sub

; if 2HL+DE<=0,increment result to round.
    add hl,hl
    add hl,de
    ld h,c
    ld l,a
    jr nc,div_88_3
    inc hl

;Now check if H is overflowed
div_88_3:
    bit 7,h
    jr nz,div_88_overflow

    pop af
    ret p
    xor a
    sub l
    ld l,a
    sbc a,a
    sub h
    ld h,a
    ret

div_88_overflow:
    ld hl,$7FFF
    pop af
    ret p
    inc hl
    inc l
    ret

div_88_sub:
    ld b,8
div_88_4:
    rla
    adc hl,hl
    add hl,de
    jr c,div_88_sub_1
    sbc hl,de
div_88_sub_1:
    djnz div_88_4
    adc a,a
    ret

; tests the sign of a
; returns: a in [-1,0,1]
;   sign and zero flags as expected
; (my own little hack and i'm quite proud of it)
get_sign_a:
    and a
    ret z
    or %01111111
    ret m
    ld a,1
    ret

; scratch memory populated by distance16game
; which is useful for cartestian_to_polar
; they are the signed 16-bit integer values
; of dx and dy divided by 2 to prevent overflow
; when squaring them
distance16game_dx2: defw 0
distance16game_dy2: defw 0

; compute the euclidian distance between two cartesian coordinates
; using the formula d = sqrt(dx^2+dy^2)
; the sum of the squares will overflow 16 bits if distance > 255
; so we divide each delta by 2 before squaring them
; then multiply the result of the square root of the summed squares by 2
; inputs: bc and de as dx,dy respectively
; outputs: hl as the 16-bit integer distance
;   distance16game_dx2 and distance16game_dy2 are dx and dy divided by 2
;   which can be plugged into atan2_88 to get a bearing to target
; destroys: everything except indexes
; NOTE: THIS IS MODIFIED FROM THE lib_math_88 routine
; TO REDUCE REDUNDANT CALCULATIONS OF DELTAS
distance16game:
; compute dx/2
    sra b
    rr c
    ld (distance16game_dx2),bc
; compute dy/2 same way
    sra d
    rr e
    ld (distance16game_dy2),de
; now we square dy/2 with mul16
    ld b,d
    ld c,e ; and bc the multiplicand
    call mul16 ; result will be limited to 16 bits
    ld de,(distance16game_dx2) ; de = dx/2
    ld (distance16game_dy2),hl ; save (dy/2)^2
; and now we square dx/2 with mul16
    ld b,d
    ld c,e
    call mul16 ; again de is redundant
    ld de,(distance16game_dy2) ; snag back (dy/2)^2
    add hl,de ; sum the squares
    ex de,hl
    call sqrtDE ; take the square root
    add hl,hl ; multiply it by 2
    ret ; we gon


;returns HL as the sqrt,DE as the remainder
sqrtDE:
; https://github.com/Zeda/Z80-Optimized-Routines/blob/master/math/squareroot/sqrtDE_slower.z80
    ld b,$80
    xor a
    ld h,a
    ld l,a
sqrt_loop:
    srl b
    rra
    ld c,a
    add hl,bc
    ex de,hl
    sbc hl,de
    jr nc,sqrt_loop_1
    add hl,de
    ex de,hl
    or a
    sbc hl,bc
    defb #DA   ;start of jp c,** which is 10cc to skip the next two bytes.
sqrt_loop_1:
    ex de,hl
    add hl,bc
    srl h
    rr l
    srl b
    rra
    jr nc,sqrt_loop
    ret


;Inputs: H.L
;Output: D.E contains the squareroot
; destroys: everything but indexes
;Adapted from Axe
; https://github.com/Zeda/Z80-Optimized-Routines/blob/master/math/squareroot/sqrtfixed_88.z80
sqrt_HL_to_DE:
; original routine is sqrt a.c --> d.e
; so we burn 8 t-states in the name of syntactic sugar
    ld a,h
    ld c,l
; back to original routine
	ld	b,12
	ld	de,0
	ld	h,d
	ld	l,e
sqrt_HL_to_DE_loop:
	sub	$40
	sbc	hl,de
	jr	nc,sqrt_HL_to_DE_skip
	add	a,$40
	adc	hl,de
sqrt_HL_to_DE_skip:
	ccf
	rl	e
	rl	d
	sla	c
	rla
	adc	hl,hl
	sla	c
	rla
	adc 	hl,hl
	djnz	sqrt_HL_to_DE_loop
	ret