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
	include "sprites.asm"
; API includes
    include "../agon_api/asm/mos_api.asm"
    include "../agon_api/asm/functions.asm"
    include "../agon_api/asm/vdu.asm"
    ; include "../agon_api/asm/vdu_buff.asm"
    include "../agon_api/asm/vdu_plot.asm"
	include "../agon_api/asm/vdu_sprites.asm"
	include "../agon_api/asm/vdp.asm"
	include "../agon_api/asm/div_168_signed.asm"
	; include "../agon_api/asm/maths24.asm"
	include "../agon_api/asm/maths.asm"
; App-specific includes
	include "player.asm"
	; include "tiles.asm"
	; include "enemies.asm"
	; include "laser.asm"
	; include "outro.asm"

; ; #### BEGIN GAME VARIABLES ####

main:
; ; DEBUG: EXIT APP TO ENSURE IT DOES SO CLEANLY AFTER THE IMAGE LOADS
; 	jp main_end

; initialize player position
	call player_init
	
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
	call vdu_vblank

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
