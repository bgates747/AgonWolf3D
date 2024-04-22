; ###############################################
; Agon Console 8 - Code Page 437 Borders Example
; Compiles on the native ez80asm assembler
; Filename: borders_437.asm
; Author: Brandon R. Gates (BeeGee747) 03-03-2024
; Github: https://github.com/bgates747/agon-testing/blob/main/font-borders-437.asm
; License: <https://unlicense.org>
; ###############################################
; STANDARD MOS HEADER
; ###############################################
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

; set up the display
    ld a,8
    call vdu_set_screen_mode

; print a hello message
	ld hl,hello_world
	call printString

	call main ; Call the main function

    pop iy  ; Pop all registers back from the stack
    pop ix
    pop de
    pop bc
    pop af
    ld hl,0  ; Load the MOS API return code (0) for no errors.
    ret      ; Return to MOS

hello_world: db "Hello, Code Page 437!\r\n",0

; ###############################################
; MAIN PROGRAM
; ###############################################
main:
    call set_borders_437
    ; call test_borders_437
    call print_borders_437_samples
    ret

; prints a 40x22 array with some sample boxes
print_borders_437_samples:
    ld hl,font_borders_437_samples
    ld b,18 ; 18 rows to print
@loop:
    push bc
    push hl
    call printString
    ; call printNewline ; not needed for 40 col screen modes, e.g. mode 8
    pop hl
    ld de,41 ; 40 chars per row + 1 for the zero terminator
    add hl,de
    pop bc
    djnz @loop
    ret

; cycle through all 48 border chars
; and print them sequentially to the screen
test_borders_437:
    call set_borders_437
    ld b,48 ; 48 chars
    ld a,128 ; first char
@loop:
    push bc
    push af
    rst.lil 10h ; print the ascii char in a at text cursor
    pop af
    inc a
    pop bc
    djnz @loop
    ret

; sets Agon user defined font characters 128-175
; to the IBM coed page 437 border glyphs
set_borders_437:
	ld hl,font_borders_437
	ld b,48 ; loop counter for 48 chars
	ld a,128 ; first char to define (─)
@loop:
	push bc
	push hl
	push af
	call vdu_define_character
	pop af
	inc a
	pop hl
	ld de,8
	add hl,de
	pop bc
	djnz @loop
    ret

; VDU 4: Write text at text cursor
;     This causes text to be written at the current text cursor position. 
;     This is the default mode for text display.
;     Text is written using the current text foreground and background colours.
; inputs: a is the character to write to the screen
; prerequisites: the text cursor at the intended position on screen
; outputs: prints the character and moves text cursor right one position
; destroys: a, hl, bc
vdu_char_to_text_cursor:
	ld (@arg),a        
	ld hl,@cmd         
	ld bc,@end-@cmd    
	rst.lil $18         
	ret
@cmd: db 4
@arg: db 0 
@end:

; VDU 22, n: Select screen mode (MODE n)
; Inputs: a, screen mode (8-bit unsigned integer), in the following list:
; https://agonconsole8.github.io/agon-docs/VDP---Screen-Modes.html
vdu_set_screen_mode:
	ld (@arg),a        
	ld hl,@cmd         
	ld bc,@end-@cmd    
	rst.lil $18         
	ret
@cmd: db 22 ; set screen mode
@arg: db 0  ; screen mode parameter
@end:

; VDU 23, n: Re-program display character / System Commands
; inputs: a, ascii code; hl, pointer to bitmask data
vdu_define_character:
	ld (@ascii),a
	ld de,@data
	ld b,8 ; loop counter for 8 bytes of data
@loop:
	ld a,(hl)
	ld (de),a
	inc hl
	inc de
	djnz @loop
	ld hl,@cmd
	ld bc,@end-@cmd
	rst.lil $18
	ret
@cmd:   db 23 
@ascii: db 0 
@data:  ds 8
@end: 

; Print a zero-terminated string
; HL: Pointer to string
printString:
	PUSH	BC
	LD		BC,0
	LD 	 	A,0
	RST.LIL 18h
	POP		BC
	RET

; IBM Code Page 437 border glyphs
; Each byte is a bitmask for one row of an 8x8 character
; NOTE: the assigned codes are 128-175 (0x80-0xAF)
; which differ from the original IBM code page 437 codes
; which are 9472-9619 (0x2500-0x2593)
; this is done because the Agon API only allows for
; 256 total character definitions
font_borders_437:
    db 0x00,0x00,0x00,0xFF,0x00,0x00,0x00,0x00  ; ─ 0x80 128
    db 0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10  ; │ 0x81 129
    db 0x00,0x00,0x00,0x1F,0x10,0x10,0x10,0x10  ; ┌ 0x82 130
    db 0x00,0x00,0x00,0xF0,0x10,0x10,0x10,0x10  ; ┐ 0x83 131
    db 0x10,0x10,0x10,0x1F,0x00,0x00,0x00,0x00  ; └ 0x84 132
    db 0x10,0x10,0x10,0xF0,0x00,0x00,0x00,0x00  ; ┘ 0x85 133
    db 0x10,0x10,0x10,0x1F,0x10,0x10,0x10,0x10  ; ├ 0x86 134
    db 0x10,0x10,0x10,0xF0,0x10,0x10,0x10,0x10  ; ┤ 0x87 135
    db 0x00,0x00,0x00,0xFF,0x10,0x10,0x10,0x10  ; ┬ 0x88 136
    db 0x10,0x10,0x10,0xFF,0x00,0x00,0x00,0x00  ; ┴ 0x89 137
    db 0x10,0x10,0x10,0xFF,0x10,0x10,0x10,0x10  ; ┼ 0x8A 138
    db 0x00,0x00,0xFF,0x00,0xFF,0x00,0x00,0x00  ; ═ 0x8B 139
    db 0x28,0x28,0x28,0x28,0x28,0x28,0x28,0x28  ; ║ 0x8C 140
    db 0x00,0x00,0x1F,0x10,0x1F,0x10,0x10,0x10  ; ╒ 0x8D 141
    db 0x00,0x00,0x00,0x3F,0x28,0x28,0x28,0x28  ; ╓ 0x8E 142
    db 0x00,0x00,0x3F,0x20,0x2F,0x28,0x28,0x28  ; ╔ 0x8F 143
    db 0x00,0x00,0xF0,0x10,0xF0,0x10,0x10,0x10  ; ╕ 0x90 144
    db 0x00,0x00,0x00,0xF8,0x28,0x28,0x28,0x28  ; ╖ 0x91 145
    db 0x00,0x00,0xF8,0x08,0xE8,0x28,0x28,0x28  ; ╗ 0x92 146
    db 0x10,0x10,0x1F,0x10,0x1F,0x00,0x00,0x00  ; ╘ 0x93 147
    db 0x28,0x28,0x28,0x3F,0x00,0x00,0x00,0x00  ; ╙ 0x94 148
    db 0x28,0x28,0x2F,0x20,0x3F,0x00,0x00,0x00  ; ╚ 0x95 149
    db 0x10,0x10,0xF0,0x10,0xF0,0x00,0x00,0x00  ; ╛ 0x96 150
    db 0x28,0x28,0x28,0xF8,0x00,0x00,0x00,0x00  ; ╜ 0x97 151
    db 0x28,0x28,0xE8,0x08,0xF8,0x00,0x00,0x00  ; ╝ 0x98 152
    db 0x10,0x10,0x1F,0x10,0x1F,0x10,0x10,0x10  ; ╞ 0x99 153
    db 0x28,0x28,0x28,0x2F,0x28,0x28,0x28,0x28  ; ╟ 0x9A 154
    db 0x28,0x28,0x2F,0x20,0x2F,0x28,0x28,0x28  ; ╠ 0x9B 155
    db 0x10,0x10,0xF0,0x10,0xF0,0x10,0x10,0x10  ; ╡ 0x9C 156
    db 0x28,0x28,0x28,0xE8,0x28,0x28,0x28,0x28  ; ╢ 0x9D 157
    db 0x28,0x28,0xE8,0x08,0xE8,0x28,0x28,0x28  ; ╣ 0x9E 158
    db 0x00,0x00,0xFF,0x00,0xFF,0x10,0x10,0x10  ; ╤ 0x9F 159
    db 0x00,0x00,0x00,0xFF,0x28,0x28,0x28,0x28  ; ╥ 0xA0 160
    db 0x00,0x00,0xFF,0x00,0xEF,0x28,0x28,0x28  ; ╦ 0xA1 161
    db 0x10,0x10,0xFF,0x00,0xFF,0x00,0x00,0x00  ; ╧ 0xA2 162
    db 0x28,0x28,0x28,0xFF,0x00,0x00,0x00,0x00  ; ╨ 0xA3 163
    db 0x28,0x28,0xEF,0x00,0xFF,0x00,0x00,0x00  ; ╩ 0xA4 164
    db 0x10,0x10,0xFF,0x10,0xFF,0x10,0x10,0x10  ; ╪ 0xA5 165
    db 0x28,0x28,0x28,0xFF,0x28,0x28,0x28,0x28  ; ╫ 0xA6 166
    db 0x28,0x28,0xEF,0x00,0xEF,0x28,0x28,0x28  ; ╬ 0xA7 167
    db 0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00  ; ▀ 0xA8 168
    db 0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF  ; ▄ 0xA9 169
    db 0xE3,0xE3,0xE3,0xE3,0xE3,0xE3,0xE3,0xE3  ; █ 0xAA 170
    db 0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0  ; ▌ 0xAB 171
    db 0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03  ; ▐ 0xAC 172
    db 0x55,0x00,0x55,0x00,0x55,0x00,0x55,0x00  ; ░ 0xAD 173
    db 0x55,0xAA,0x55,0xAA,0x55,0xAA,0x55,0xAA  ; ▒ 0xAE 174
    db 0x55,0xFF,0x55,0xFF,0x55,0xFF,0x55,0xFF  ; ▓ 0xAF 175

; A 40x18 array of example boxes drawn with the IBM code page 437 border glyphs
; Strings are zero-terminated for use with the printString function
font_borders_437_samples:
    db 32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0
    db 32,130,128,128,136,128,128,131,32,32,32,130,128,136,128,131,32,32,143,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,146,0
    db 32,129,32,32,129,32,32,129,173,32,32,134,128,138,128,135,32,32,140,32,32,32,32,32,84,73,84,76,69,32,66,65,82,32,32,32,32,32,32,140,0
    db 32,129,32,32,129,32,32,129,173,32,32,129,32,129,32,129,32,32,155,139,159,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,158,0
    db 32,134,128,128,138,128,128,135,173,32,32,132,128,137,128,133,32,32,140,32,129,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,175,140,0
    db 32,129,32,32,129,32,32,129,173,32,32,32,32,32,32,32,32,32,140,32,129,83,111,109,101,32,116,101,120,116,32,104,101,114,101,33,32,32,173,140,0
    db 32,129,32,32,129,32,32,129,173,32,32,32,32,32,32,32,32,32,154,128,138,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,157,0
    db 32,132,128,128,137,128,128,133,173,32,32,32,32,32,32,32,32,32,140,32,129,173,175,173,173,173,173,173,173,173,173,173,173,173,173,173,173,173,173,140,0
    db 32,32,173,173,173,173,173,173,173,32,32,32,32,32,32,32,32,32,149,139,162,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,152,0
    db 32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0
    db 32,143,139,139,161,139,139,146,32,32,32,32,32,130,141,142,143,136,159,160,161,131,144,145,146,128,139,129,140,32,32,32,32,32,32,32,32,32,32,32,0
    db 32,140,32,32,140,32,32,140,174,32,32,32,32,134,153,154,155,138,165,166,167,135,156,157,158,168,169,171,172,32,32,32,32,32,32,32,32,32,32,32,0
    db 32,140,32,32,140,32,32,140,174,32,32,32,32,132,147,148,149,137,162,163,164,133,150,151,152,173,174,175,170,32,32,32,32,32,32,32,32,32,32,32,0
    db 32,155,139,139,167,139,139,158,174,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0
    db 32,140,32,32,140,32,32,140,174,32,32,32,32,130,136,128,131,32,141,159,139,144,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0
    db 32,140,32,32,140,32,32,140,174,32,32,32,32,134,138,128,135,32,153,165,139,156,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0
    db 32,149,139,139,164,139,139,152,174,32,32,32,32,129,129,32,129,32,129,129,32,129,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0
    db 32,32,174,174,174,174,174,174,174,32,32,32,32,132,137,128,133,32,147,162,139,150,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0
