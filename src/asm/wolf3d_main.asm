; On-chip 8KB high-speed SRAM
; This on-chip memory is mapped by Quark MOS firmware to upper-byte B7, 
; effectively mapping it from 0xB7.E000 to 0xB7.FFFF. It is currently 
; unused by Quark firmware, allowing full access to the user, provided 
; the program employs 24-bit ADL address mode. If required, this memory 
; can be remapped by the user program to a different upper-byte address; 
; it will be mapped to B7 again by Quark MOS at each boot-up.
    org 0xB7E000
; now these includes and any code below it will be loaded into the fast SRAM
; SPRITE TABLE NEEDS TO BE HERE SO THAT IT ALIGNS WITH table_base
	include "sprites.inc"
; API includes
    include "../agon_api/asm/mos_api.inc"
    include "../agon_api/asm/functions.inc"
    include "../agon_api/asm/vdu.inc"
    ; include "../agon_api/asm/vdu_buff.inc"
    include "../agon_api/asm/vdu_plot.inc"
	include "../agon_api/asm/vdu_sprites.inc"
	include "../agon_api/asm/vdp.inc"
	include "../agon_api/asm/div_168_signed.inc"
	; include "../agon_api/asm/maths24.inc"
	include "../agon_api/asm/maths.inc"
; App-specific includes
	include "player.inc"
	; include "tiles.inc"
	; include "enemies.inc"
	; include "laser.inc"

; ; #### BEGIN GAME VARIABLES ####

main:
; initialize player position
	call player_init

; set screen to double-buffered mode
	ld a,8 + 128
	call vdu_set_screen_mode

; render initial scene
	ld de,(cur_x) ; implicitly loads cur_y
	call get_cell_from_coords
	xor a ; north orientation
	call render_scene
	call vdu_flip_screen

main_loop:
; wait for the next vsync
	call vsync

; get player input and update sprite position
	call player_input

; move enemies
	; call move_enemies

; update the screen if the player or enemies have moved
	ld a,(player_move_timer) ; if player has moved, this timer
	cp move_timer_reset ; will be at its reset value
	jr nz, @no_render
	ld de,(cur_x) ; implicitly loads cur_y
	call get_cell_from_coords
	ld a,(orientation)
	call render_scene
	call vdu_flip_screen

@no_render:
; poll keyboard
    ld a, $08                           ; code to send to MOS
    rst.lil $08                         ; get IX pointer to System Variables
    
    ld a, (ix + $05)                    ; get ASCII code of key pressed
    cp 27                               ; check if 27 (ascii code for ESC)   
    jp z, main_end                     ; if pressed, jump to exit

    jp main_loop

main_end:
	ret