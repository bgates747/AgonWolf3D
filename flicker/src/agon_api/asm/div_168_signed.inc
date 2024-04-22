; 24-bit integer and 16.8 fixed point division routines
; by Brandon R. Gates (BeeGee747)
; have undergone cursory testing and seem to be generating
; correct results (assuming no overflows) but seem very inefficient,
; so they have been published for review and improvement
; see: https://discord.com/channels/1158535358624039014/1158536711148675072/1212136741608099910
;
; ---------------------------------------------------------
; GLOBAL SCRATCH VARIABLES
; ---------------------------------------------------------
uaf: ds 4 ; 32-bit scratch
uhl: ds 4 ; the extra byte at the end
ubc: ds 4 ; is padding for overflow
ude: ds 4 ; when shifting up registers
uix: ds 4
uiy: ds 4
usp: ds 4
upc: ds 4

; ---------------------------------------------------------
; BEGIN DIVISION ROUTINES
; ---------------------------------------------------------
;
; perform signed division of 16.8 fixed place values
; with an signed 16.8 fixed place result
; inputs: ub.c is dividend,ud.e is divisor
; outputs: uh.l is quotient
; destroys: a,bc
; note: uses carry flag to test for sign of operands and result
;       which can be confusing and should perhaps be changed
; note2: helper functions abs_hlu and neg_hlu have been modified
;       to return accurate flags according to the origional signs 
;       (or zero) of this function's inputs
sdiv168:
; make everything positive and save signs
    push bc         ; get bc to hl
    pop hl          ; for the next call
    call abs_hlu    ; sets sign flag if hlu was negative, zero if zero
    jp z,@is_zero   ; if bc is zero, answer is zero and we're done
    push af         ; save sign of bc
    push hl         ; now put abs(hl)
    pop bc          ; back into bc = abs(bc)
    ex de,hl        ; now we do de same way
    call abs_hlu
    jp z,@div_by_zero  ; if de was zero, answer is undefined and we're done
    ex de,hl        ; hl back to de = abs(de)
; determine sign of result
    jp p,@de_pos    ; sign positive,de is positive
    pop af          ; get back sign of bc
    jp m,@result_pos  ; bc and de negative, result is positive
    jr @result_neg
@de_pos:
    pop af          ; get back sign of bc
    jp p,@result_pos   ; bc and de are both positive so result is positive
                    ; fall through to result_neg
@result_neg:
    xor a           ; zero a and clear carry 
    dec a           ; set sign flag to negative
    jr @do_div      
@result_pos:
    xor a           ; zero a and clear carry 
    inc a           ; set sign flag to negative
                    ; fall through to do_div
@do_div:
    push af         ; save sign of result
    call udiv168
    pop af          ; get back sign of result
    ret p           ; result is positive so nothing to do
    call neg_hlu    ; result is negative so negate it
    ret
@is_zero:           ; result is zero
    xor a           ; sets zero flag, which we want, 
                    ; sets pv flag which we might not (zero is parity even)
                    ; resets all others which is okay
    ret
@div_by_zero:       ; result is undefined, which isn't defined in binary
                    ; so we'll just return zero until i can think of something better
    pop af          ; dummy pop
    xor a           ; sets zero flag, which is ok, 
                    ; sets pv flag which could be interpreted as overflow, which is good
                    ; resets all others which is okay
    ret

; ; perform unsigned division of 16.8 fixed place values
; ; with an unsigned 16.8 fixed place result
; ; inputs: ub.c is dividend,ud.e is divisor
; ; outputs: uh.l is quotient
; ; destroys: a,bc
; udiv168:
; ; get the 16-bit integer part of the quotient
;     ; call div_24
;     call udiv24
;     ; call dumpRegistersHex
; ; load quotient to upper three bytes of output
;     ld (div168_out+1),bc
; ; TODO: THIS MAY BE BUGGED
; ; check remainder for zero, and if it is 
; ; we can skip calculating the fractional part
;     add hl,de
;     or a
;     sbc hl,de 
;     jr nz,@div256
;     xor a
;     jr @write_frac
; ; END TODO
; @div256:
; ; divide divisor by 256
;     push hl ; save remainder
; ; TODO: it feels like this could be more efficient
;     ld (ude),de
;     ld a,d
;     ld (ude),a
;     ld a,(ude+2)
;     ld (ude+1),a
;     xor a
;     ld (ude+2),a
;     ld hl,(ude) ; (just for now, we want it in de eventually)
; ; TODO: THIS MAY BE BUGGED
; ; now we check the shifted divisor for zero, and if it is
; ; we again set the fractional part to zero
;     add hl,de
;     or a
;     sbc hl,de 
;     ex de,hl ; now de is where it's supposed to be
;     pop hl ; get remainder back
; ; TODO: THIS MAY BE BUGGED
;     jr nz,@div_frac
;     xor a
;     jr @write_frac
; ; END TODO
; ; now divide the remainder by the shifted divisor
; @div_frac:
;     push hl ; my kingdom for ld bc,hl
;     pop bc  ; or even ex bc,hl
;     ; call div_24
;     call udiv24
; ; load low byte of quotient to low byte of output
;     ld a,c
; @write_frac:
;     ld (div168_out),a
; ; load hl with return value
;     ld hl,(div168_out)
; ; load a with any overflow
;     ld a,(div168_out+3)
;     ret ; uh.l is the 16.8 result
; div168_out: ds 4 ; the extra byte is for overflow

; perform unsigned division of fixed place values
; with an unsigned 16.8 fixed place result
; inputs: b.c is 8.8 dividend, ud.e is 16.8 divisor
; outputs: uh.l is the 16.8 quotient ub.c is the 16.8 remainder
; destroys: a,bc
udiv168:
; shift dividend left 8 bits
    ld (ubc+1),bc
    xor a
    ld (ubc),a
    ld bc,(ubc)
    call udiv24
; flip-flop outptuts to satisfy downstream consumers
; TODO: this is a hack and should be fixed
; (so says copilot ... but it's not wrong)
    push hl 
    push bc
    pop hl 
    pop bc 
    ret

; this is an adaptation of Div16 extended to 24 bits
; from https://map.grauw.nl/articles/mult_div_shifts.php
; it works by shifting each byte of the dividend left into carry 8 times
; and adding the dividend into hl if the carry is set
; thus hl accumulates a remainder depending on the result of each iteration
; ---------------------------------------------------------
; Divide 24-bit unsigned values 
;   with 24-bit unsigned result
;   and 24-bit remainder
; In: Divide ubc by ude
; Out: ubc = result, uhl = remainder
; Destroys: a,hl,bc
div_24:
    ld hl,0     ; Clear accumulator for remainder
; put dividend in scratch so we can get at all its bytes
    ld (ubc),bc ; scratch ubc also accumulates the quotient
    ld a,(ubc+2); grab the upper byte of the dividend
    ld b,8      ; loop counter for 8 bits in a byte
@loop0:
    rla         ; shift the next bit of dividend into the carry flag
    adc hl,hl   ; shift the remainder left one bit and add carry if any
    sbc hl,de   ; subtract divisor from remainder
    jr nc,@noadd0   ; if no carry,remainder is <= divisor
                ; meaning remainder is divisible by divisor
    add hl,de   ; otherwise add divisor back to remainder
                ; reversing the previous subtraction
@noadd0:
    djnz @loop0 ; repeat for all 8 bits
    rla         ; now we shift a left one more time
    cpl         ; then flip its bits for some reason
    ld (ubc+2),a; magically this is the upper byte of the quotient
    ld a,(ubc+1); now we pick up the middle byte of the dividend
    ld b,8      ; set up the next loop and do it all again ...
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
    ld (ubc+1),a ; writing the middle byte of quotient
    ld a,(ubc)
    ld b,8
@loop2:          ; compute low byte of quotient
    rla
    adc hl,hl
    sbc hl,de
    jr nc,@noadd2
    add hl,de
@noadd2:
    djnz @loop2
    rla
    cpl
    ld (ubc),a  ; ... write low byte of quotient
    ld bc,(ubc) ; load quotient into bc for return
    ret         ; hl already contains remainder so we're done

; ---------------------------------------------------------
; BEGIN HELPER ROUTINES
; ---------------------------------------------------------
;
; absolute value of hlu
; returns: abs(hlu), flags set according to the incoming sign of hlu:
;         s1,z0,pv0,n1,c0 if hlu was negative
;         s0,z1,pv0,n1,c0 if hlu was zero
;         s0,z0,pv0,n1,c0 if hlu was positive
; destroys: a
abs_hlu:
    add hl,de
    or a
    sbc hl,de 
    jp m,@is_neg
    ret         ; hlu is positive or zero so we're done
@is_neg:
    push af     ; otherwise, save current flags for return
    call neg_hlu ; negate hlu
    pop af      ; get back flags
    ret

; flip the sign of hlu
; inputs: hlu
; returns: 0-hlu, flags set appropriately for the result:
;         s1,z0,pv0,n1,c1 if result is negative
;         s0,z1,pv0,n1,c0 if result is zero
;         s0,z0,pv0,n1,c1 if result is positive
; destroys a
neg_hlu:
    push de     ; save de
    ex de,hl    ; put hl into de
    ld hl,0     ; clear hl
    xor a       ; clear carry
    sbc hl,de   ; 0-hlu = -hlu
    pop de      ; get de back
    ret         ; easy peasy

; -----------------------------------------------------------------------
; https://github.com/sijnstra/agon-projects/blob/main/calc24/arith24.asm
;------------------------------------------------------------------------
;  arith24.asm 
;  24-bit ez80 arithmetic routines
;  Copyright (c) Shawn Sijnstra 2024
;  MIT license
;
;  This library was created as a tool to help make ez80
;  24-bit native assembly routines for simple mathematical problems
;  more widely available.
;  
;------------------------------------------------------------------------

;------------------------------------------------------------------------
; umul24:	HLU = BCU*DEU (unsigned)
; Preserves AF, BCU, DEU
; Uses a fast multiply routine.
;------------------------------------------------------------------------
; modified to take BCU as multiplier instead of HLU
umul24:
	; push	DE 
	; push	BC
	; push	AF	
	; push	HL
	; pop		BC
    ld	 	a,24 ; No. of bits to process 
    ld	 	hl,0 ; Result
umul24_lp:
	add	hl,hl
	ex	de,hl
	add	hl,hl
	ex	de,hl
	jr	nc,umul24_nc
	add	hl,bc
umul24_nc: 
	dec	a
	jr	nz,umul24_lp
    dec bc ; debug
	; pop	af
	; pop	bc
	; pop	de
	ret


;------------------------------------------------------------------------
; udiv24
; Unsigned 24-bit division
; Divides BCU by DEU. Gives result in BCU, remainder in HLU.
; 
; Uses AF BC DE HL
; Uses Restoring Division algorithm
;------------------------------------------------------------------------
; modified to take BCU as dividend instead of HLU
; and give BCU as quotient instead of DEU
; -----------------------------------------------------------------------
udiv24:
	; push	hl
	; pop		bc	;move dividend to BCU
	ld		hl,0	;result
	and		a
	sbc		hl,de	;test for div by 0
	ret		z		;it's zero, carry flag is clear
	add		hl,de	;HL is 0 again
	ld		a,24	;number of loops through.
udiv1:
	push	bc	;complicated way of doing this because of lack of access to top bits
	ex		(sp),hl
	scf
	adc	hl,hl
	ex	(sp),hl
	pop	bc		;we now have bc = (bc * 2) + 1

	adc	hl,hl
	and	a		;is this the bug
	sbc	hl,de
	jr	nc,udiv2
	add	hl,de
;	dec	c
	dec	bc
udiv2:
	dec	a
	jr	nz,udiv1
	scf		;flag used for div0 error
	; push	bc
	; pop		de	;remainder
	ret



;------------------------------------------------------------------------
; neg24
; Returns: HLU = 0-HLU
; preserves all other registers
;------------------------------------------------------------------------
neg24:
	push	de
	ex		de,hl
	ld		hl,0
	or		a
	sbc		hl,de
	pop		de
	ret

;------------------------------------------------------------------------
; or_hlu_deu: 24 bit bitwise OR
; Returns: hlu = hlu OR deu
; preserves all other registers
;------------------------------------------------------------------------
or_hlu_deu:
	ld	(bitbuf1),hl
	ld	(bitbuf2),de
	push	de	;preserve DEU
	push	bc	;preserve BCU
	ld		b,3
	ld	hl,bitbuf1
	ld	de,bitbuf1
orloop_24:
	ld	a,(de)
	or	(hl)
	ld	(de),a
	inc	de
	inc	hl
	djnz	orloop_24
	ld	hl,(bitbuf2)
	pop		bc	;restore BC
	pop		de	;restore DE

;------------------------------------------------------------------------
; and_hlu_deu: 24 bit bitwise AND
; Returns: hlu = hlu AND deu
; preserves all other registers
;------------------------------------------------------------------------
and_hlu_deu:
	ld	(bitbuf1),hl
	ld	(bitbuf2),de
	push	de	;preserve DEU
	push	bc	;preserve BCU
	ld		b,3
	ld	hl,bitbuf1
	ld	de,bitbuf1
andloop_24:
	ld	a,(de)
	and	(hl)
	ld	(de),a
	inc	de
	inc	hl
	djnz	andloop_24
	ld	hl,(bitbuf2)
	pop		bc	;restore BC
	pop		de	;restore DE

;------------------------------------------------------------------------
; xor_hlu_deu: 24 bit bitwise XOR
; Returns: hlu = hlu XOR deu
; preserves all other registers
;------------------------------------------------------------------------
xor_hlu_deu:
	ld	(bitbuf1),hl
	ld	(bitbuf2),de
	push	de	;preserve DEU
	push	bc	;preserve BCU
	ld		b,3
	ld	hl,bitbuf1
	ld	de,bitbuf1
xorloop_24:
	ld	a,(de)
	xor	(hl)
	ld	(de),a
	inc	de
	inc	hl
	djnz	xorloop_24
	ld	hl,(bitbuf2)
	pop		bc	;restore BC
	pop		de	;restore DE

;------------------------------------------------------------------------
; shl_hlu: 24 bit shift left hlu by deu positions
; Returns: hlu = hlu << deu
;		   de = 0
; NOTE: only considers deu up to 16 bits. 
; preserves all other registers
;------------------------------------------------------------------------
shl_hlu:
	ld		a,d		;up to 16 bit.
	or		e
	ret		z		;we're done
	add		hl,hl	;shift HLU left
	dec		de
	jr		shl_hlu

;------------------------------------------------------------------------
; shr_hlu: 24 bit shift right hlu by deu positions
; Returns: hlu = hlu >> deu
;		   de = 0
; NOTE: only considers deu up to 16 bits. 
; preserves all other registers
;------------------------------------------------------------------------
shr_hlu:
	ld		(bitbuf1),hl
	ld		hl,bitbuf1+2
shr_loop:
	ld		a,d		;up to 16 bit.
	or		e
	jr		z,shr_done		;we're done
;carry is clear from or instruction
	rr		(hl)
	dec		hl
	rr		(hl)
	dec		hl
	rr		(hl)
	inc		hl
	inc		hl
	dec		de
	jr		shr_loop
shr_done:
	ld		hl,(bitbuf1)	;collect result
	ret

;------------------------------------------------------------------------
; divide hlu by 2, inspired by above
;------------------------------------------------------------------------
hlu_div2:
	ld		(bitbuf1),hl
	ld		hl,bitbuf1+2
	rr		(hl)
	dec		hl
	rr		(hl)
	dec		hl
	rr		(hl)
	inc		hl
	inc		hl
    ld hl,(bitbuf1)
    ret

; this is my little hack to divide by 16
hlu_div16:
    xor a
    add hl,hl
    rla
    add hl,hl
    rla
    add hl,hl
    rla
    add hl,hl
    rla
    ld (@scratch),hl
    ld (@scratch+3),a
    ld hl,(@scratch+1) 
    ret
@scratch: ds 4

;------------------------------------------------------------------------
; Scratch area for calculations
;------------------------------------------------------------------------
bitbuf1:	dw24	0	;bit manipulation buffer 1
bitbuf2:	dw24	0	;bit manipulation buffer 2


; -----------------------------------------------------------------------
; EEMES TUTORIALS
; -----------------------------------------------------------------------
; https://tutorials.eeems.ca/Z80ASM/part4.htm
; DEHL=BC*DE
Mul16:                           
    ld hl,0
    ld a,16
Mul16Loop:
    add hl,hl
    rl e
    rl d
    jp nc,NoMul16
    add hl,bc
    jp nc,NoMul16
    inc de
NoMul16:
    dec a
    jp nz,Mul16Loop
    ret

; DEUHLU=BCU*DEU
umul2448:                           
    ld hl,0
    ld a,24
umul2448Loop:
    add hl,hl
    ex de,hl
    adc hl,hl
    ex de,hl
    jp nc,Noumul2448
    add hl,bc
    jp nc,Noumul2448
    inc de
Noumul2448:
    dec a
    jp nz,umul2448Loop
    ret

umul168:
    call umul2448

    ; call dumpUDEUHLHex

; UDEU.HL is the 32.16 fixed result
; we want UH.L to be the 16.8 fixed result
; so we divide by 256 by shiftng down a byte
; easiest way is to write deu and hlu to scratch
    ld (umul168out+3),de
    ld (umul168out),hl
; then load hlu from scratch shfited forward a byte
    ld hl,(umul168out+1)
    ld a,(umul168out+5) ; send a back with any overflow
    ret
umul168out: ds 6

; perform signed multiplication of 16.8 fixed place values
; with an signed 16.8 fixed place result
; inputs: ub.c and ud.e are the operands
; outputs: uh.l is the product
; destroys: a,bc
; TODO: make flags appropriate to the sign of the result
smul168:
; make everything positive and save signs
    push bc         ; get bc to hl
    pop hl          ; for the next call
    call abs_hlu    ; sets sign flag if ubc was negative, zero if zero

    ; call dumpFlags ; passes

    jp z,@is_zero   ; if bc is zero, answer is zero and we're done
    push af         ; save sign of bc
    push hl         ; now put abs(hl)
    pop bc          ; back into bc = abs(bc)
    ex de,hl        ; now we do de same way
    call abs_hlu    ; sets sign flag if ude was negative, zero if zero

    ; call dumpFlags ; passes

    jp z,@is_zero  ; if de was zero, answer is zero and we're done
    ex de,hl        ; hl back to de = abs(de)
; determine sign of result
    jp p,@de_pos    ; sign positive,de is positive

    ; call dumpFlags ; correctly doesnt make it here

    pop af          ; get back sign of bc

    ; call dumpFlags ; correctly doesn't make it here

    jp m,@result_pos  ; bc and de negative, result is positive

    ; call dumpFlags  ; corectly doesn't make it here

    jr @result_neg
@de_pos:
    pop af          ; get back sign of bc

    ; call dumpFlags  ; passes

    jp p,@result_pos   ; bc and de are both positive so result is positive

    ; call dumpFlags ; correctly makes it here

                    ; fall through to result_neg
@result_neg:
    xor a           ; zero a and clear carry 
    dec a           ; set sign flag to negative

    ; call dumpFlags ; passes

    jr @do_mul      
@result_pos:
    xor a           ; zero a and clear carry 
    inc a           ; set sign flag to positive
                    ; fall through to do_mul

    ; call dumpFlags ; correctly doesn't make it here

@do_mul:
    push af         ; save sign of result
    call umul168
    pop af          ; get back sign of result

    ; call dumpFlags ; passes

    ret p           ; result is positive so nothing to do

    ; call dumpRegistersHex ; passes

    call neg_hlu    ; result is negative so negate it

    ; call dumpRegistersHex ; passes
    ret
@is_zero:           ; result is zero
    xor a           ; sets zero flag, which we want, 
                    ; sets pv flag which we might not (zero is parity even)
                    ; resets all others which is okay
    ret