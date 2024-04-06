
; https://agonconsole8.github.io/agon-docs/VDP---Bitmaps-API.html
; Macro for loading bitmaps to VDP buffers
	macro LOADBMP n,width,height,file
	db 23,27,0  ; VDU 23, 27, 0 select bitmap
	db n      ; specify target bitmap number (8-bits)
	db 23,27,1  ; load bitmap data
    dw width    ; in pixels
    dw height   ; in pixels
	incbin file ; path to file containing binary bitmap data
	endmacro

; https://discord.com/channels/1158535358624039014/1158536809916149831/1208492884861653145
	; load an rgba2222 bitmap to a 16-bit bufferId
	macro LOADBMPBUFFER2 bufferId,width,height,file

    ; Clear buffer
    db 23,0,0xA0
    dw bufferId
    db 2
    
    db 23,27,0x20 ; select buffer VDU 23, 27, &20, bufferId;
    dw bufferId

    ; Upload data :: VDU 23, 0 &A0, bufferId; 0, length; <buffer-data>
    db 23,0,0xA0
    dw bufferId
    db 0 
	dw width * height ; length of data in bytes
    incbin file ; bitmap data
    
    ;Create bitmap from selected buffer :: VDU 23, 27, &21, w; h; format
    db 23,27,0x21
    dw width ; in pixels
    dw height ; in pixels
    db 1 ; bitmap format: 1 = RGBA2222 (1-bytes per pixel)
    endmacro

	; load an rgba8888 bitmap to a 16-bit bufferId
	macro LOADBMPBUFFER8 bufferId,width,height,file

    ; Clear buffer
    db 23,0,0xA0
    dw bufferId
    db 2
    
    db 23,27,0x20 ; select buffer VDU 23, 27, &20, bufferId;
    dw bufferId

    ; Upload data :: VDU 23, 0 &A0, bufferId; 0, length; <buffer-data>
    db 23,0,0xA0
    dw bufferId
    db 0 
	dw width * height * 4 ; length of data in bytes
    incbin file ; bitmap data
    
    ;Create bitmap from selected buffer :: VDU 23, 27, &21, w; h; format
    db 23,27,0x21
    dw width ; in pixels
    dw height ; in pixels
    db 0 ; bitmap format: 0 = RGBA8888 (4-bytes per pixel)
    endmacro