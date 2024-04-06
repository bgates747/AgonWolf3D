; the ez80 instruction set includes the mlt instructions, which does unsigned multiplication
; on two 8-bit registers belonging to the same 16-bit register pair, and writes the answer
; back to the same 16-bit register pair. e.g., mlt hl gives hl=h*l. now suppose we have two
; 24-bit registers, ubc and ude that we want to multiply. propose a long-multiplication
; algorithm leveraging the mlt instruction, bearing in mind that we don't have direct access
; to the upper bytes of the 24-bit register triplets on the ez80, so i suggest the first step
; is to write them to scratch. use hl to do the mlt. bc and de can be used as pointers to the
; ube and ude scratch registers as we move through the multiplication. finally, accumulate the
; 48 bit result in an output scratch location, using ix and if necessary iy as pointers to
; the output scratch

; Multiply two 24-bit registers using long-multiplication algorithm

; Input:
;   ubc - Upper 24 bits of the first 24-bit register
;   ude - Upper 24 bits of the second 24-bit register
; Output:
;   hl - Lower 16 bits of the 48-bit result

; Scratch Registers:
;   bc - Pointer to the ubc scratch register
;   de - Pointer to the ude scratch register
;   ix - Pointer to the output scratch register

mlt24:
    push af
    push hl
    push bc
    push de
    push ix

    ; Initialize scratch registers
    ld bc, ubc
    ld de, ude
    ld ix, output_scratch

    ; Clear the output scratch register
    ld hl, 0
    ld (ix), hl
    inc ix
    ld (ix), hl

    ; Multiply the lower 8 bits
    ld a, c
    ld h, d
    mlt hl
    ld (ix), hl
    inc ix

    ; Multiply the middle 8 bits
    ld a, b
    ld h, e
    mlt hl
    ld (ix), hl
    inc ix

    ; Multiply the upper 8 bits
    ld a, b
    ld h, d
    mlt hl
    ld (ix), hl

    pop ix
    pop de
    pop bc
    pop hl
    pop af
    ret
