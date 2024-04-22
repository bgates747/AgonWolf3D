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
	; include "outro.inc"

; ; #### BEGIN GAME VARIABLES ####

main:
; initialize player position
	call player_init

; set screen to double-buffered mode
	ld a,8 + 128
	call vdu_set_screen_mode

; turn off cursor ... again
	call cursor_off

; render initial scene
	ld de,(cur_x) ; implicitly loads cur_y
	call get_cell_from_coords
	xor a ; north orientation
	ld (orientation),a
	call render_scene
	call vdu_flip

main_loop:
; move enemies
	; call move_enemies

; get player input and update sprite position
	call player_input ; ix points to cell defs/status, a is target cell current obj_id

; render the updated scene
	call render_scene
; flip the screen
	call vdu_flip
; wait for the next VBLANK
	call WAIT_VBLANK

; check for escape key and quit if pressed
	MOSCALL mos_getkbmap
; 113 Escape
    bit 0,(ix+14)
    jr z,@Escape
	jr main_end
@Escape:

; do it again, Sam
    jr main_loop

main_end:
	; call do_outro
; restore screen to something normalish
	xor a
	call vdu_set_screen_mode
	call cursor_on
	ret
