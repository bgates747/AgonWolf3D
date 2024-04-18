; ###### macros go here ######
	macro CLS
	ld a, 12
	rst.lil $10
	endmacro

	macro SET_COLOUR value
	ld a, 17					; set text colour
	rst.lil $10
	ld a, value					; colour to use
	rst.lil $10
	endmacro

	macro SET_BG_COLOUR value
	ld a, 17					; set text colour
	rst.lil $10
	ld a, value					; colour to use
	add a, 128
	rst.lil $10
	endmacro

	macro TAB_TO x,y
	ld a, 31					; move to...
	rst.lil $10
	ld a, x						; X position
	rst.lil $10
	ld a, y						; Y position
	rst.lil $10
	endmacro

	macro SET_MODE mode
	ld a, 22					; set mode...
	rst.lil $10
	ld a, mode					; to mode
	rst.lil $10
	endmacro

	macro MOSCALL arg1
	ld a, arg1
	rst.lil $08
	endmacro

; ###### global constants can go here ######

; ###### NO CODE OR MEMORY ALLOCATIONS ABOVE THIS LINE ######
    .assume adl=1   
    .org 0x040000    

    jp start       

    .align 64      
    .db "MOS"       
    .db 00h         
    .db 01h  

; ###### includes can go here ######     

; ###### BEGINNING OF CODE ######
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

; ###############################################
; actual program code section
; ###############################################

main:
; prepare the screen

    SET_MODE 8 + 128 ; 320x240x64 double-buffered   

    xor a
    call vdu_set_scaling ; turn off screen scaling         

main_loop:
; clear the screen
    call vdu_cls                      ; causes flickering on emulator
    ; call vdu_clg                      ; causes flickering on emulator

; Sending a VDU byte stream
    ld hl, VDUdata                      ; address of string to use
    ld bc, endVDUdata - VDUdata         ; length of string
    rst.lil $18                         ; Call the MOS API to send data to VDP 

    call vdu_flip                       ; flip the screen so we can see what was drawn
    ; call vdu_cls                      ; causes flickering on emulator
    ; call vdu_clg                      ; causes flickering on emulator

; exit if ESC key pressed
    ld a, $08                           ; code to send to MOS
    rst.lil $08                         ; get IX pointer to System Variables
    ld a, (ix + $05)                    ; get ASCII code of key pressed
    cp 27                               ; check if 27 (ascii code for ESC)   
    jp z, EXIT_HERE                     ; if pressed, jump to exit

; ESC not pressed so loop
    jr main_loop

; ------------------
; This is where we exit the program

EXIT_HERE:
    SET_MODE 0 ; 640x480x16 single-buffered
    call vdu_cls
    ret                                 ; Return to MOS

; ------------------
; This is the data we send to VDP

VDUdata:
    ; FOR A SINGLE PIXEL PLOT

    .db 18, 0, bright_red               ; set graphics colour: mode (0), colour

    .db 25, 69                          ; PLOT: mode (69 is a point in current colour),
    .dw 200,80                          ; X; Y;

    ; FOR A LINE

    .db 18, 0, bright_magenta           ; set graphics colour: mode (0), colour

    .db 25, 69                          ; PLOT: mode (69 is a point in current colour),
    .dw 300, 60                         ; X; Y;

    .db 25, 13                          ; PLOT: mode (13 is a line),
    .dw 250,130                         ; X; Y;

    ; FOR A RECTANGLE

    .db 18, 0, green                    ; set graphics colour: mode (0), colour

    .db 25, 69                          ; PLOT: mode (69 is a point in current colour),
    .dw 10,120                          ; X; Y;

    .db 25, 101                         ; PLOT: mode (101 is a filled rectangle),
    .dw 100,180                         ; X; Y;


   ; FOR A CIRCLE   

    .db 18, 0, bright_yellow            ; set graphics colour: mode (0), colour

    .db 25, 68                          ; PLOT: mode (69 is a MOVE TO but don't plot point),
    .dw 180,140                         ; X; Y;

    .db 25, 149                         ; PLOT: mode (149 is an outlined circle),
    .dw 200,160                         ; X; Y;

    ; FOR A FILLED TRIANGLE

    .db 18, 0, blue                     ; set graphics colour: mode (0), colour

    .db 25, 69                          ; PLOT: mode (69 is a point in current colour),
    .dw 10,10                           ; X; Y;

    .db 25, 69                          ; PLOT: mode (69 is a point in current colour),
    .dw 50, 100                         ; X; Y;

    .db 25, 85                          ; PLOT: mode (85 is a filled triangle),
    .dw 200,20                          ; X; Y;
endVDUdata:

; ------------------
; colour data

bright_red:     equ     9
green:          equ     2
bright_yellow:  equ     11
bright_magenta: equ     13
blue:           equ     4
white:          equ     7
black:          equ     0
bright_white:   equ     15


vdu_flip:       
	ld hl,@cmd         
	ld bc,@end-@cmd    
	rst.lil $18         
	ret
@cmd: db 23,0,0xC3
@end:

; VDU 23, 0, &C0, n: Turn logical screen scaling on and off *
; inputs: a is scaling mode, 1=on, 0=off
; note: default setting on boot is scaling ON
vdu_set_scaling:
	ld (@arg),a        
	ld hl,@cmd         
	ld bc,@end-@cmd    
	rst.lil $18         
	ret
@cmd: db 23,0,0xC0
@arg: db 0  ; scaling on/off
@end:

; VDU 12: Clear text area (CLS)
vdu_cls:
    ld a,12
	rst.lil $10  
	ret

; VDU 16: Clear graphics area (CLG)
vdu_clg:
    ld a,16
	rst.lil $10  
	ret
