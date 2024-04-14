; ############# MAP CONSTANTS #############
; ; temporary hardcoded until we implement 
; ; dynamically from tiles defs
; null_cell: equ 19 ; 0x13
; blank_cell: equ 29 ; 0x1D
; door_cell: equ 57 ; 0x39
; elevator_cell: equ 59 ; 0x3B

; map type/status flags
cell_is_door:     EQU %10000000  ; Bit 7: door flag
cell_is_wall:     EQU %01000000  ; Bit 6: wall flag
cell_is_trigger:  EQU %00100000  ; Bit 5: trigger flag
cell_is_blocking: EQU %00010000  ; Bit 4: blocking flag

; HOW THE MAP TABLE IS LAID OUT
; (obj_id render_obj type/status mask), render routine address
; cell_000: dl 0x110000,rend_000; 0x00 : 00,00 : 0x00,0x00 
;
; map table field offset constants
; (mind the little-endianess)
map_type_status: equ 0
map_render_obj: equ 1
map_obj_id: equ 2
map_render: equ 3
map_record_size: equ 6

; gets cell info from a directional displacement from a given map location
; inputs: ; d = distance ; e = direction, b,c = y,x
; returns: ix = pointer to cell lookup address; a = obj_id; hl = address of cell base render routine
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
; returns: ix = pointer to cell lookup address; a = obj_id
get_cell_from_coords:
	ld b,d ; y
	ld c,16 ; number of cells in a column
	mlt bc ; bc = cell_id of y,0
	ld hl,0 ; make sure uhl is zero
	ld l,e ; x
	add hl,bc ; hl = cell_id of x,y
	push hl ; now account for 6 bytes per record
	add hl,hl ; hl * 2
	pop bc
	add hl,bc ; hl * 3
	add hl,hl ; hl * 6
	ex de,hl
	ld ix,cells ; base address of lookup table
	add ix,de ; ix = address of cell record
	ld a,(ix+map_obj_id) ; a = obj_id
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