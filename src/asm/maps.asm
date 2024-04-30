; ############# MAP CONSTANTS #############
; map tables addresses
cell_status: 		equ 0xB7E000 ; base of on-chip high speed SRAM
cell_views: 		equ 0xB7E400 ; cell_status + 256*4

; map status/type flags
cell_is_door:     	equ %10000000  ; Bit 7: door flag
cell_is_wall:     	equ %01000000  ; Bit 6: wall flag
cell_is_trigger:  	equ %00100000  ; Bit 5: trigger flag
cell_is_blocking: 	equ %00010000  ; Bit 4: blocking flag
cell_is_start:		equ %00001000  ; Bit 3: start flag
cell_is_to_room:    equ %00000100  ; Bit 2: to room flag
; bits 1 and 0 are the render_type mask
render_type_cube:   equ %00000000  ; 0
render_type_floor:  equ %00000001  ; 1
render_type_null:   equ %00000010  ; 2
render_type_sprite: equ %00000011  ; 3

; HOW THE MAP TABLE IS LAID OUT
; map table field offset constants
; (mind the little-endianess)
map_type_status: 	equ 0
map_img_idx: 		equ 1
map_obj_id: 		equ 2
map_sprite_id: 		equ 3
map_record_size: 	equ 4 ; bytes per cell_status record

; gets cell info from a directional displacement from a given map location
; inputs: ; d = distance ; e = direction, b,c = y,x
; returns: ix = pointer to cell_status lut; a = obj_id; hl = address of cell base render routine
; calls: get_dx_dy, get_cell_from_coords
get_neighbor:
; modulo 4 on orientation
    ld a,e
    and 0x03
    ld e,a
	call get_dx_dy ; d,e = dy,dx
; add add b,c to the deltas in d,e
	ld a,c
	add a,e
	ld e,a
	ld a,b
	add a,d
	ld d,a
; fall through to get_cell_from_coords

; gets cell info from a given x,y map coordinate
; inputs: ; d,e = map_y,map_x
; returns: ix = pointer to cell_status lut; a = obj_id, bc = cell_id
get_cell_from_coords:
; modulo 16 on input coords
	ld a,e
	and 0x0F
	ld e,a
	ld a,d
	and 0x0F
	ld d,a
; get cell_id from x,y
	ld b,d ; y
	ld c,16 ; number of cells in a column
	mlt bc ; bc = cell_id of y,0
	ld hl,0 ; make sure uhl is zero
	ld l,e ; x
	add hl,bc ; hl = cell_id of x,y
	push hl ; so we can return cell_id
	ld c,l ; c = cell_id
; get address of cell record in cell_status table
	ld b,map_record_size ; b = bytes per record
	mlt bc ; bc = offset to cell record
	ld ix,cell_status ; base address of lookup table
	add ix,bc ; ix = address of cell record
	ld a,(ix+map_obj_id) ; a = obj_id
	pop bc ; bc = cell_id
	ret

; gets dx,dy from orientation and distance
; d = distance ; e = orientation
; returns: d,e = dy,dx
get_dx_dy:
; modulo 4 on orientation
	ld a,e
	and 0x03
	cp 0
	jr z,@north
	cp 1
	jr z,@east
	cp 2
	jr z,@south
	cp 3
	jr z,@west
; if none of those, return zeroes
	ld de,0
	ret
@north:
; x = 0, y = -d
	ld e,0
	ld a,d
	neg
	ld d,a
	ret
@east:
; x = d, y = 0
	ld e,d
	ld d,0
	ret
@south:	
; x = 0, y = d
	ld e,0
	ret
@west:
; x = -d, y = 0
	ld a,d
	neg
	ld e,a
	ld d,0
	ret

; gets the direction from a dy,dx pair
; basically atan2(dy,dx) but for only the 4 cardinal directions
; inputs: ; d = dy ; e = dx
; returns: a = orientation
get_dir_from_dy_dx:
	xor a
	sub e
	jr z,@not_x
	ld a,1
	ret m
	ld a,3
	ret
@not_x:
	xor a
	sub d
	ret z
	ld a,2
	ret m
	xor a
	ret


; translate camera relative x,y deltas to map x,y deltas
; inputs: ; d = dy ; e = dx ; a = camera orientation
; returns:	d = map_dy ; e = map_dx
trans_dx_dy:
; modulo 4 on orientation
	and 0x03
	jr z,@north
	cp 1 ; east
	jr z,@east
	cp 2 ; south
	jr z,@south
	cp 3 ; west
	jr z,@west
; if none of those, return zeroes
	ld de,0
	ret
@north: ; invert y axis, x unnchanged
	ld a,d
	neg
	ld d,a
	ret
@east: ; +x = +y, +y = +x
	ld a,d
	ld d,e
	ld e,a
	ret
@south: ; invert x axis, y unchanged
	ld a,e
	neg
	ld e,a
	ret
@west: ; +x = -y, +y = -x
	ld a,d ; y
	neg ; -y
	ld d,e ; x
	ld e,a ; -y
	ld a,d ; x
	neg ; -x
	ld d,a ; -x
	ret

; initialize map variables and load map file
; inputs: none
map_init:
	xor a
	ld (cur_floor),a
	ld (cur_room),a
; load room file
	call map_load
; set player initial position
	ret

; load map file
; inputs: cur_floor, cur_room set
map_load:
	ld hl,floors ; address of floors lut
	ld a,(cur_floor)
	ld e,a
	ld d,3 ; three bytes per lookup record
	mlt de ; de = offset to floor lut entry
	add hl,de ; hl = address of floor lut entry
	ld hl,(hl) ; hl = base address of rooms for given floor
	ld a,(cur_room)
	ld e,a
	ld d,3 ; three bytes per lookup record
	mlt de ; de = offset to room lut entry
	add hl,de ; hl = address of room lut entry
	ld hl,(hl) ; hl = address of room file name
	ld (cur_filename),hl ; DEBUG
	ld de,cell_status ; address to load map data
	ld bc,8*1024 ; size of map data in bytes
	ld a,mos_load
	RST.LIL 08h
; DEBUG: print filename
	ld hl,(cur_filename)
	call printString
; load sprite data
	call map_init_sprites
	ret

; initialize sprite data for the current room into sprite table
; inputs: map data loaded
map_init_sprites:
; initialize pointers
	ld ix,cell_status
	ld iy,sprite_table_base
@loop:
	ld (sprite_table_pointer),iy ; probably don't strictly need this but why not
	ld a,(ix+map_sprite_id)
	cp 255 ; check for no sprite
	jr z,@next_cell
	ld (iy+sprite_id),a
	ld a,(ix+map_img_idx)
	ld (iy+sprite_obj),a
	call sprite_init_data
	lea iy,iy+sprite_record_size ; advance pointer to next sprite record
@next_cell:
	lea ix,ix+map_record_size ; advance pointer to next cell
; check if we've reached the end of the map data
	ld de,cell_views ; this address is the end of cell_status table + 1
	push ix ; why no sbc ix,rr, zilog?
	pop hl
	xor a ; clear carry
	sbc hl,de
	jr nz,@loop
	ld iy,sprite_table_base ; reset pointer
	ld (sprite_table_pointer),iy
	ret

; get the x,y map coordinates from a cell_id
; inputs: a = cell_id
; returns: a = cell_id, d = map_y, e = map_x
cell_id_to_coords:
	push af	; Save the cell id
; Calculate the y coordinate by dividing the index by 16
	ld d,a      ; Move index into d
	sra d        ; Shift right once (d = d / 2)
	sra d        ; Shift right again (d = d / 4)
	sra d        ; Shift right again (d = d / 8)
	sra d        ; Shift right again (d = d / 16)
; Calculate the x coordinate by taking the index modulo 16
	and 15       ; e = e & 15 (retain the lower 4 bits of the cell id, which is modulo 16)
	ld e,a      ; e is now the x coordinate
	pop af	; a is cell id
	ret

; get starting position based on the start flag
; inputs: none
; returns: a = cell_id, d = map_y, e = map_x
get_start_pos:
	ld de,0 ; initialize to 0,0 as a default
	ld ix,cell_status ; ix points to the start of the map data
	xor a ; start at cell 0
@loop:
	push af ; save cell_id
	ld a,(ix+map_type_status) ; a is the cell status bitmmask
	and cell_is_start ; testing whether the cell start bit is lit
	jr z,@not_start ; go to the next cell if not
	pop	af ; a is cell_id
	call cell_id_to_coords ; d = map_y, e = map_x
	ret
@not_start:
	pop	af ; a is cell_id
	inc a ; bump cell id
	ret z ; if zero we've wrapped around so we return 0,0 in de and 0 in a as cell_id
	lea ix,ix+map_record_size ; otherwise bump pointer to next map record
	jr @loop

; #### AUTO-GENERATED MAP DATA BELOW THIS LINE DO NOT EDIT ####

floors:
	dl floor_00

; map room filename labels
room_files:
floor_00:
	dl room_00_0
	dl room_00_1

; map data filenames
room_00_0: db "maps/map_00_0.bin",0
room_00_1: db "maps/map_00_1.bin",0