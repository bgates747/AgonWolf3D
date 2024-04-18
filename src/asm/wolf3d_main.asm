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

; check for escape key and quit if pressed
	MOSCALL mos_getkbmap
; 113 Escape
    bit 0,(ix+14)
    jr z,@Escape
	jr main_end
@Escape:

; throttle the framerate
	ld a,60/8; 4 fps at 60Hz
@wait:
	ld (@timer),a
	call WAIT_VBLANK
	ld a,(@timer)
	dec a
	jr nz,@wait
; do it again, Sam
    jr main_loop
@timer: ds 1

main_end:

; do the outro advert for purple nurples
; set to double-buffered mode
    ld a,8 + 128
    call vdu_set_screen_mode
    call cursor_off
@loop_animation:
; print a thanks for playing message
	ld ix,font_itc_honda
	ld hl,thanks_for_playing
	ld bc,20 ; x
	ld de,2 ; y
	call font_bmp_print
; print coming soon message
	ld ix,font_retro_computer
	ld hl,coming_soon
	ld bc,14 ; x
	ld de,24+160 ; y
	call font_bmp_print
; replot the background
    ld hl,BUF_UI_NURP_BG_CR
    call vdu_buff_select
    ld bc,0
    ld de,0
    call vdu_plot_bmp
; then plot the logo
    ld hl,BUF_UI_NURP_LOG
    call vdu_buff_select
    ld bc,(@logo_x)
    inc bc
    inc bc
    ld (@logo_x),bc
    ld de,(@logo_y)
    call vdu_plot_bmp
; flip the screen buffer
    call vdu_flip
; wait a tick
    call WAIT_VBLANK
; update loop counter
    ld a,(@loop_counter)
    dec a
    ld (@loop_counter),a
    jr z,@done
    jp @loop_animation
@loop_counter: db 168
@logo_x: dl -315
@logo_y: dl 24
@done:

; return things to normal state
    ld a,8
    call vdu_set_screen_mode

; one final render of the outro advert
; print a thanks for playing message
	ld ix,font_itc_honda
	ld hl,thanks_for_playing
	ld bc,20 ; x
	ld de,2 ; y
	call font_bmp_print
; print coming soon message
	ld ix,font_retro_computer
	ld hl,coming_soon
	ld bc,14 ; x
	ld de,24+160 ; y
	call font_bmp_print
; replot the background
    ld hl,BUF_UI_NURP_BG_CR
    call vdu_buff_select
    ld bc,0
    ld de,0
    call vdu_plot_bmp
; then plot the logo
    ld hl,BUF_UI_NURP_LOG
    call vdu_buff_select
    ld bc,(@logo_x)
    inc bc
    inc bc
    ld (@logo_x),bc
    ld de,(@logo_y)
    call vdu_plot_bmp
	
; move the cursor to the bottom of the screen
	ld c,0
	ld b,29 ; bottom of screen in mode 8
	call vdu_move_cursor
    call cursor_on

; and out
	ret

thanks_for_playing: defb "We hope you enjoyed Wolf3D",0
be_sure_not_to_miss: defb "BE SURE NOT TO MISS",0
attack_of: defb "ATTACK OF THE",0
coming_soon: defb "COMING SOON TO AN AGON NEAR YOU!",0