; ###### macros go here ######
	macro SET_MODE mode
	ld a, 22					; set mode...
	rst.lil $10
	ld a, mode					; to mode
	rst.lil $10
	endmacro

    include "../agon_api/asm/mos_api.inc"

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