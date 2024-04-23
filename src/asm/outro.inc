do_outro:
; clear both screen buffers
	xor a ; plotting mode 0
	ld c,4 ; dark blue
	call vdu_gcol_bg
	call vdu_clg
	call vdu_flip
	call vdu_clg
	call vdu_flip

; do the thanks for playing loop
outro1:
; clear the screen
	call vdu_clg
; plot the box art background image
	ld hl,BUF_UI_BOX_ART
	call vdu_buff_select
	ld bc,32
	ld de,0
	call vdu_plot_bmp
; print the text message
	ld ix,font_itc_honda
	ld hl,thanks_for_playing
	ld bc,20 ; x
	ld de,(@text_y) ; y
	dec de
	ld (@text_y),de
	call font_bmp_print
	ld a,(@loop_counter)
	dec a
	ld (@loop_counter),a
	jr z,outro1_end
	call vdu_flip
	call vdu_vblank
	call vdu_vblank
	jp outro1
@text_y: dl 240
@loop_counter: db 240


outro1_end:
	ld a,128
	push af
@wait_loop:
	call vdu_vblank
	pop af
	dec a
	jr z,@wait_done
	push af
	jp @wait_loop
@wait_done:

; clear the screen
	call vdu_clg
; plot the box art background image
	ld hl,BUF_UI_BOX_ART
	call vdu_buff_select
	ld bc,32
	ld de,0
	call vdu_plot_bmp
	call vdu_flip
; clear the screen
	call vdu_clg
; plot the box art background image .. again
	ld hl,BUF_UI_BOX_ART
	call vdu_buff_select
	ld bc,32
	ld de,0
	call vdu_plot_bmp

outro2:
; replot the background
    ld hl,BUF_UI_NURP_BG_CR
    call vdu_buff_select
    ld bc,(@logo_x)
    ld de,(@logo_y)
	dec de
    dec de
    dec de
	ld (@logo_y),de
    call vdu_plot_bmp
; print be sure not to miss
	ld ix,font_retro_computer
	ld hl,be_sure_not_to_miss
	ld bc,2 ; x
	ld de,2 ; y
	call font_bmp_print
; flip the screen buffer
    call vdu_flip
; wait a tick
    call vdu_vblank
; update loop counter
    ld a,(@loop_counter)
    dec a
    ld (@loop_counter),a
    jr z,@done
    jp outro2
@loop_counter: db 80
@logo_x: dl 0
@logo_y: dl 240
@done:

; set gfx bg color
	xor a ; plotting mode 0
	ld c,0 ; black
	call vdu_gcol_bg
; clear both video buffers
    call vdu_clg
    call vdu_flip
    call vdu_clg

; do the outro advert for purple nurples
outro3:
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
    inc bc
    inc bc
    ld (@logo_x),bc
    ld de,(@logo_y)
    call vdu_plot_bmp
; print coming soon message
	ld ix,font_retro_computer
	ld hl,coming_soon
	ld bc,14 ; x
	ld de,240-30; y
	call font_bmp_print
; flip the screen buffer
    call vdu_flip
; wait a tick
    call vdu_vblank
; update loop counter
    ld a,(@loop_counter)
    dec a
    ld (@loop_counter),a
    jr z,@done
    jp outro3
@loop_counter: db 80
@logo_x: dl -315
@logo_y: dl 24
@done:

; return things to normal state
    ld a,8
    call vdu_set_screen_mode

; one final render of the outro advert
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
; prit attack of the
	ld ix,font_retro_computer
	ld hl,attack_of
	ld bc,180 ; x
	ld de,8; y
	call font_bmp_print
; print coming soon message
	ld ix,font_retro_computer
	ld hl,coming_soon
	ld bc,14 ; x
	ld de,240-30; y
	call font_bmp_print
	
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