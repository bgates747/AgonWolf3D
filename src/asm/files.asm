; WARNING: this routine must be the last one loaded in the main program so that filedata doesn't stomp on any program code
; inputs: hl = bufferId, ix = file size
vdu_load_buffer_from_file:
	; load buffer ids
		ld (@id0),hl
		ld (@id1),hl
		ld (@id2),hl
	; clean up bytes that got stomped on by the ID loads
		ld a,2
		ld (@id0+2),a
		ld a,23
		ld (@id1+2),a
		xor a
		ld (@id2+2),a
	; read size from ix
		ld a,ixl
		ld (@size),a
		ld a,ixh
		ld (@size+1),a
	; get all the ducks in a row for the vdu call
		ld bc,filedata-@start
		add ix,bc
		ld b,ixh
		ld c,ixl
		ld hl,@start
	; push the button
		rst.lil $18
	; back to caller
		ret
; vdp command string:
@start: db 23,0,0xA0 ; Clear buffer
@id0:	dw 0x0000 ; bufferId
		db 2
	; select buffer VDU 23, 27, &20, bufferId;
		db 23,27,0x20 
@id1:	dw 0x0000 ; bufferId
	; Upload data :: VDU 23, 0 &A0, bufferId; 0, length; <buffer-data>
		db 23,0,0xA0
@id2:	dw 0x0000 ; bufferId
		db 0 
		; CAUTION: the size argument is a 16-bit value, so the max number of bytes we can load in one chunk is 64KiB!! This corresponds to an rgba2 image size of 320x204.
@size:	dw 0x0000 ; length of data in bytes
filedata: ; no need to allocate space here if this is the final include of the application
	; ds 65536 ; placeholder for file data	DEBUG