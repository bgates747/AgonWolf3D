; #### RENDERING SCRATCH VARIABLES ####
; first three bytes of cell_status record in little-endian order
to_cell_status: 
to_map_type_status: ds 1
to_img_idx: ds 1
to_obj_id: ds 1
; fourth byte of cell_status record
to_sprite_id: ds 1

to_poly_id: ds 1
to_buffer_id: ds 3

cur_cell_views: ds 3

view_distance: equ 5 ; furthest player can see or be seen in map units

; render background as a prelude to rendering panels and sprites
; hl is the buffer id, bc and de are plot_x and plot_y
render_background:
; back up everything
    push bc
    push de
    push hl
; plot background
    xor a ; color mode
    ld c,c_grey_dk ; color
    call vdu_gcol_fg
    ld bc,0 ; x0
    ld de,0 ; y0
    ld ix,319
    ld iy,80
    call vdu_plot_rf
    xor a ; color mode
    ld c,c_grey ; color
    call vdu_gcol_fg
    ld bc,0 ; x0
    ld de,80 ; y0
    ld ix,319
    ld iy,159
    call vdu_plot_rf
; plot the background
    pop hl ; get back the buffer id
    call vdu_buff_select
    pop de ; get back plot_y
    pop bc ; get back plot_x
    call vdu_plot_bmp
    ret

; render a 3D panel
; inputs: to_poly_id set, to_buffer_id set
render_panel:
; make the bitmap buffer active
    ld hl,(to_buffer_id)
    call vdu_buff_select
; get the coordinates of the panel
    ld ix,polys_lookup_plot ; pointer to polys lookup table
; get the panel's poly_id
    ld a,(to_poly_id)
; multiply a by 6 to get the offset
    ld b,a
    ld c,6
    mlt bc
; add the offset to the lookup table
    add ix,bc
; get the panel coordinates
    ld bc,(ix) ; plot_x
    ld de,(ix+3) ; plot_y
; plot that mofo and go home
    call vdu_plot_bmp
    ret

; render a 3D sprite
; inputs: a is sprite_id, to_poly_id set, to_cell_status fields set
; (ix should also be pointed to cell_status record but we don't depend on it for the time being)
render_sprite:
; look up sprite_obj in sprite table
    ld iy,sprite_table_base
    ld b,a ; sprite id
    ld c,sprite_record_size
    mlt bc
    add iy,bc ; iy points to sprite record
    ld (sprite_table_pointer),iy
; get sprite imgs lookup
    ld a,(iy+sprite_obj) ; a is sprite_obj
    ld iy,sprite_imgs_lookup ; base address of sprite_imgs lookup table
    ld b,a
    ld c,3 ; 3 bytes per record
    mlt bc
    add iy,bc ; iy points to the sprite's sprite_imgs_lookup record
    ld iy,(iy) ; iy is the base address of the sprite's image defs lookup
; convert to_poly_id to sprite_poly
    ld hl,sprite_polys_lookup
    ld a,(to_poly_id)
    ld bc,0  ; make sure bcu and b are zero
    ld c,a
    add hl,bc ; hl points to the sprite's poly id
; get the sprites image defs for the particular poly id
    ld a,(hl)
    ld b,a
    ld c,9  ; 9 bytes per record
    mlt bc
    add iy,bc ; iy is the offset to the sprite's image def
; select buffer
    ld hl,(iy+6)
    call vdu_buff_select
; plot sprite 
    ld bc,(iy+0) ; plot_x
    ld de,(iy+3) ; plot_y
    call vdu_plot_bmp
    ret

; render the object in a given cell and poly_id
; inputs: to_poly_id set, d,e are the cell coords
render_cell:
; get the cell to render's cell_status data and store it in scratch
    call get_cell_from_coords ; ix=cell_status lut; a=obj_id, bc = cell_id
    ld hl,(ix) ; l = to_map_type_status, h = to_img_idx, hlu = to_obj_id
    ld (to_cell_status),hl
; get sprite_id from cell_status lut
    ld a,(ix+map_sprite_id)
    cp 255 ; value if no sprite present
    jp nz,render_sprite
; get cell's render_type
    ld a,l ; map_type_status
    and 2 ; mask off everything but lowest two bits
    jr z,@cube ; render_type_cube is 0
    jr @nodraw ; placeholder for future implementation TODO
@cube:
    ; get map_img_idx from cell_status lut
    ld a,(to_img_idx)
    cp 255 ; value for cell with nothing to draw
    jr z,@nodraw
; prepare render_panel ; inputs: to_poly_id set, to_buffer_id set
    ld hl,cube_img_idx_lookup
    ld b,a
    ld c,3 ; three bytes per record
    mlt bc
    add hl,bc ; hl points to the cube's base buffer id
    ld hl,(hl) ; hl is the base buffer id
    ex de,hl ; stash the base buffer id in de for later
    ld hl,cube_poly_idx_lookup
    ld a,(to_poly_id)
    ld bc,0 ; make sure bcu is zero
    ld c,a
    add hl,bc ; hl is the buffer id index address
    ld a,(hl) ; a is the buffer id index value
    ld hl,0 ; make sure hlu is zero
    ld l,a ; hl is the buffer id index value
    add hl,de ; hl is the buffer id
    ld (to_buffer_id),hl
    jp render_panel
@nodraw:
    ret

; render a full 3d scene
; inputs: cur_x, cur_y, orientation set
; outputs: pretty pictures
; destroys: everything
render_scene:
; clear the screen
    call render_background
; get current map position and camera orientation
    ld de,(cur_x) ; d,e = cur_y,x
    call get_cell_from_coords ; ix=cell_status lut; a=obj_id, bc = cell_id
; get cell_views address for this cell and orientation
    ld a,(orientation)
    ld e,a
    ld d,6 ; 6 bytes per orientation
    mlt de ; de = orientation offset 
    ex de,hl ; hl = orientation offset
    ld b,24 ; 24 bytes per cell in cell_views lut
    mlt bc ; bc = offset from base address of cell_views lut
    add hl,bc ; hl = total offset from cell_views base address
    ex de,hl ; becaue we can't add iy to hl
    ld iy,cell_views ; base address of cell_views lut
    add iy,de ; iy = cell_views address
    ld (cur_cell_views),iy
; cycle through the cell views masks and render the appropriate objects
    ld bc,0x284600 ; bcu = jr z,nnn opcode, c = bit operand, b = displacement operand
    xor a ; poly_id
    ld (to_poly_id),a
@loop: 
    ld (@bit_iy+2),bc
    ld iy,(cur_cell_views)
@bit_iy:
    bit 0,(iy+0) ; the bit tested and offset will be self-modified through the loop
    jr z,@next_poly ; the first byte of this instruction is 0x28, and will be re-written as such each loop
; get_polys_deltas inputs: a is the orientation, c is the poly_id
    ld a,(to_poly_id)
    ld c,a ; poly_id
    ld a,(orientation)
    call get_polys_deltas ; d,e = y,x deltas
    ld a,(cur_x)
    add a,e
    ld e,a
    ld a,(cur_y)
    add a,d
    ld d,a
    ld a,(to_poly_id)
    call render_cell ; d,e = to_render y,x coords, we don't need to worry about the modulo 16
@next_poly:
    ld bc,(@bit_iy+2)
    ld a,(to_poly_id)
    inc a ; a is next poly_id
    ld (to_poly_id),a
    cp num_polys
    jr z,@end
    ld a,8
    add a,b
    ld b,a ; bit tested codes to 0x46 + b/8
    cp 0x86 ; = 0x7E + 8 where 0x7E is the highest bit possible (7)
    jr nz,@loop
    ld b,0x46
    inc c ; iy address offset 
    jr @loop
@end:
; draw the graphic portions of the ui
	ld hl,BUF_UI_LOWER_PANEL
    call vdu_buff_select
	ld bc,0 ; x
	ld de,160 ; y
	call vdu_plot_bmp

    ld hl,(player_weapon_ui_buffer_id_large)
    ld de,(player_weapon_animation_frame)
    add hl,de
    call vdu_buff_select
    ld bc,128 ; x
    ld de,96 ; y
    call vdu_plot_bmp

    ld hl,(player_weapon_ui_buffer_id_small)
    call vdu_buff_select
    ld bc,266 ; x
    ld de,178 ; y
    call vdu_plot_bmp

; draw the text portions of the ui
    ld c,8 ; x
    ld b,3 ; y 
    call vdu_move_cursor
    ld hl,(player_score)
    ld de,player_score_str
    call Num2String
    ld hl,player_score_str
    call printString

    ld c,22 ; x
    ld b,3 ; y 
    call vdu_move_cursor
    ld hl,(player_health)
    ld de,player_health_str
    call Num2String
    ld hl,player_health_str
    call printString

    ld c,28 ; x
    ld b,3 ; y 
    call vdu_move_cursor
    ld hl,(player_ammo)
    ld de,player_ammo_str
    call Num2String
    ld hl,player_ammo_str
    call printString

; all done
    ret

; get the map coordinates deltas for a given orientation and poly_id
; inputs: a is the orientation, c is the poly_id
; returns: d,e are the y,x deltas, deu will be the next byte in the lookup table and should be ignored
get_polys_deltas:
; get the base address of the orientation-specific deltas lookup table
    cp 0
    jr z,@orientation_0
    cp 1
    jr z,@orientation_1
    cp 2
    jr z,@orientation_2
    cp 3
    jr z,@orientation_3
; return zeros if not found
    ld de,0
    ret
@orientation_0: ; north
    ld hl,polys_map_deltas_0
    jr @get_deltas
@orientation_1: ; east
    ld hl,polys_map_deltas_1
    jr @get_deltas
@orientation_2: ; south
    ld hl,polys_map_deltas_2
    jr @get_deltas
@orientation_3: ; west
    ld hl,polys_map_deltas_3
@get_deltas:
    ld b,2 ; 2 bytes per record
    mlt bc ; poly_id * 2
    add hl,bc ; hl points to the deltas
    ld de,(hl) ;d,e = dy,dx
    ret
