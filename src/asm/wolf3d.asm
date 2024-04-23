; macro files generally want to go here, before any of the other includes
; which call the macro, otherwise the assembler won't have the macro
; available to run when it is called, and will fail with something 
; along the lines of 'invalid label' at such and such a line
    ; include "agon_api/asm/macros.asm"

;MOS INITIALIATION MUST GO HERE BEFORE ANY OTHER CODE
    .assume adl=1   
    .org 0x040000    

    jp start       

    .align 64      
    .db "MOS"       
    .db 00h         
    .db 01h       

start:              
    push af
    push bc
    push de
    push ix
    push iy

; ###############################################
; ez80asmLinker.py loader code goes here if used.
; ###############################################

; ###############################################
	call init ; Initialization code
    call main ; Call the main function
; ###############################################

exit:

    pop iy                              ; Pop all registers back from the stack
    pop ix
    pop de
    pop bc
    pop af
    ld hl,0                             ; Load the MOS API return code (0) for no errors.

    ret                                 ; Return MOS