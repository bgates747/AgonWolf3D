; render background as a prelude to rendering panels and sprites
; hl is the buffer id, bc and de are plot_x and plot_y
render_background:
; back up everything
    push bc
    push de
    push hl
; plot background
    xor a ; color mode
    ld c,c_blue ; color
    call vdu_gcol_fg
    ld bc,0 ; x0
    ld de,0 ; y0
    ld ix,320
    ld iy,80
    call vdu_plot_rf
    xor a ; color mode
    ld c,c_red_dk ; color
    call vdu_gcol_fg
    ld bc,0 ; x0
    ld de,80 ; y0
    ld ix,320
    ld iy,160
    call vdu_plot_rf
; plot the background
    pop hl ; get back the buffer id
    call vdu_buff_select
    pop de ; get back plot_y
    pop bc ; get back plot_x
    call vdu_plot_bmp
    ret

; render a 3D panel
; inputs: uhl is to_poly_id, hl is the buffer_id
render_panel:
; write hl to scratch
    ld (@hlu),hl
; make the bitmap buffer active
    call vdu_buff_select
; get the coordinates of the panel
    ld ix,polys_lookup ; pointer to polys lookup table
; put hlu in a
    ld a,(@hlu+2)
; multiply a by 6 to get the offset
    ld b,a
    ld c,6
    mlt bc
; add the offset to the lookup table
    add ix,bc
; get the panel coordinates
    ld hl,(ix) ; plot_x
    push hl
    pop bc
    ld hl,(ix+3) ; plot_y
    ex de,hl
; plot that mofo and go home
    call vdu_plot_bmp
    ret
@hlu: ds 3

; render a 3D sprite
; inputs: a is the poly_id of the cell to render, ix pointed to cell lookup
render_sprite:
    ld bc,0 ; make sure bcu is zero
    ld c,a ; bc is poly_id
; find the current map_render_obj of the target cell
    ld a,(ix+map_render_obj)
; if zero, nothing to draw
    and a
    jr nz,@not_zero
    ret 
@not_zero:
; look up sprite_obj from render_obj
    ld iy,render_obj_to_sprite_obj
    ld e,a ; render_obj
    ld d,3 ; three byte per record in lut
    mlt de
    add iy,de ; iy points to label
    ld iy,(iy) ; iy has base address of sprite polys
; look up south_poly from poly_id
    ld hl,polys_south_lookup
    add hl,bc ; hl points to south poly id
    ld a,(hl) ; a is south poly id
    ld e,a
    ld d,9 ; nine byte per record in lut
    mlt de
    add iy,de ; iy points to sprite poly defs
; select buffer
    ld hl,(iy+6)
    call vdu_buff_select
; plot sprite 
    ld bc,(iy+0) ; plot_x
    ld de,(iy+3) ; plot_y
    call vdu_plot_bmp
    ret

; render a full 3d scene
; inputs: ix pointed to cell lookup, (orietation) set
; outputs: pretty pictures
; destroys: a, hl, bc, de, ix
render_scene:
; get cell info from lookup table
    ld hl,(ix+map_render) ; hl = pointer to base of render routiness
    ld b,3 ; 3 bytes per address label
    ld a,(orientation)
    ld c,a
    mlt bc ; bc = offset from base address
    add hl,bc ; hl points to routine address
    ld hl,(hl) ; don't do this on a z80
    push hl
    ; call vdu_cls ; no longer necessary now that we have a background
    pop hl
    ld a,(orientation)
    ld iy,(cur_x)
    jp (hl) ; 'call' the routine
; we always jp back here from the render routine
render_scene_return: 
    ret