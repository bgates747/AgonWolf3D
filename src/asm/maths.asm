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
    xor a ; reset a, clear carry flag
adcec: 
    ld a,(de) ; addend to acc
    adc a,(hl) ; add (hl) to acc
    daa ; adjust result to bcd
    ld (hl),a ; store result
    inc hl ; advance memory pointers
    inc de
    djnz adcec ; loop until b == 0
    ret 

; BCD subtraction
; inputs: (hl) and (de) point to BCD numbers of equal length (divisible by 2)
;       a is the number of bytes holding each number (number of places/2)
; outputs: (hl) - (de) --> (hl)
; destroys: a,b,de,hl
sub_bcd:
    ld b,a ; loop counter
    xor a ; reset a,clear carry flag
subdec: 
    ld a,(de) ; subtrahend to acc
    sbc a,(hl) ; subtract (hl) from acc
    daa ; adjust result to bcd
    ld (hl),a ; store result
    inc hl ; advance memory pointers
    inc de
    djnz subdec ; loop until b == 0
    ret 