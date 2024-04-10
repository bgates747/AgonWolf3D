; render a 3D panel
; inputs: uhl is the poly_id, hl is the buffer_id
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
    ld bc,0 ; make sure bcu is zero
    ld b,a
    ld c,6
    mlt bc
; add the offset to the lookup table
    add ix,bc
; get the panel coordinates
    ld iy,(ix) ; plot_x
    push iy
    pop bc
    ld iy,(ix+3) ; plot_y
    ; ld de,240-160 ; temp debug to make room for dumpRegistersHex
    ; add iy,de
    push iy
    pop de
; plot that mofo and go home
    call vdu_plot_bmp
    ret
@hlu: ds 3

; render a full 3d scene
; inputs: ix pointed to cell lookup, (orietation) set
; outputs: pretty pictures
; destroys: a, hl, bc, de, ix
render_scene:
; get cell info from lookup table
    ld hl,(ix+map_render) ; hl = pointer to base of render routines
    ld bc,0 ; make sure bcu is zero
    ld b,3 ; 3 bytes per address label
    ld a,(orientation)
    ld c,a
    mlt bc ; bc = offset from base address
    add hl,bc ; hl points to routine address
    ld hl,(hl) ; don't do this on a z80
    push hl
    call vdu_cls
    pop hl
    ld a,(orientation)
    ld iy,(cur_x)
    jp (hl) ; 'call' the routine
; we always jp back here from the render routine
render_scene_return: 
    ret