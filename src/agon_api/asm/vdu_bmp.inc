; =========================================================================
; Bitmaps
; -------------------------------------------------------------------------
; VDU 23, 27, 0, n: Select bitmap n
; VDU 23, 27, &20, bufferId;: Select bitmap using a 16-bit buffer ID *
; VDU 23, 27, 1, w; h; b1, b2 ... bn: Load colour bitmap data into current bitmap

; VDU 23, 27, 1, n, 0, 0;: Capture screen data into bitmap n *
; VDU 23, 27, &21, bitmapId; 0; : same, but to 16-bit buffer ID *
; Any PLOT, or VDU 25, style command will push the graphics cursor position - 
; typically "move" style plot commands are used to define the rectangle.
; To be clear, this command should be performed after two "move" style PLOT commands.
; inputs: hl; target bufferId
; all the following are in 16.8 fixed point format
;   ub.c; top-left x coordinate
;   ud.e; top-left y coordinate
;   ui.x; width
;   ui.y; height
vdu_buff_screen_capture168:
        ld (@y0-1),de
        ld (@x0-1),bc
        ld a,0x44 ; plot_pt+mv_abs
        ld (@x0-1),a

        ld (@x1),ix
        ld (@y1),iy
        ld a,23
        ld (@y1+2),a

        ld (@bufId),hl
        xor a
        ld (@bufId+2),a

        ld hl,@begin
        ld bc,@end-@begin
        rst.lil $18
        ret
@begin:
; absolute move gfx cursor to top-left screen coordinate
; VDU 25, mode, x; y;: PLOT command
        db 25,0x44 ; plot_pt+mv_abs
@x0: 	dw 64
@y0: 	dw 64
; relative move gfx cursor to bottom-right screen coordinate
; VDU 25, mode, x; y;: PLOT command
        db 25,0x40 ; plot_pt+mv_rel
@x1: 	dw 15
@y1: 	dw 15
; now the main event
; VDU 23, 27, &21, bitmapId; 0;
        db 23,27,0x21
@bufId: dw 0x2000,0x0000
@end: ; no padding required

vdu_buff_screen_capture_full:
        ld hl,@begin
        ld bc,@end-@begin
        rst.lil $18
        ret
@begin:
; absolute move gfx cursor to top-left screen coordinate
; VDU 25, mode, x; y;: PLOT command
        db 25,0x44 ; plot_pt+mv_abs
@x0: 	dw 0
@y0: 	dw 0
; relative move gfx cursor to bottom-right screen coordinate
; VDU 25, mode, x; y;: PLOT command
        db 25,0x40 ; plot_pt+mv_rel
@x1: 	dw 319
@y1: 	dw 239
; now the main event
; VDU 23, 27, &21, bitmapId; 0;
        db 23,27,0x21
@bufId: dw 0x2000,0x0000
@end: ; no padding required

vdu_buff_screen_paste_full:
        ld hl,@begin
        ld bc,@end-@begin
        rst.lil $18
        ret
; VDU 23, 27, &20, bufferId; : Select bitmap (using a buffer ID)
@begin:    db 23,27,0x20
@bufferId: dw 0x2000
; VDU 25, mode, x; y;: PLOT command
           db 25,0xED ; plot_bmp+dr_abs_fg
           dw 0x0000,0x0000
@end: ; no padding required

vdu_buff_screen_capture_tiles:
        ld hl,@begin
        ld bc,@end-@begin
        rst.lil $18
        ret
@begin:
; absolute move gfx cursor to top-left screen coordinate
; VDU 25, mode, x; y;: PLOT command
        db 25,0x44 ; plot_pt+mv_abs
@x0: 	dw 0
@y0: 	dw 0
; relative move gfx cursor to bottom-right screen coordinate
; VDU 25, mode, x; y;: PLOT command
        db 25,0x40 ; plot_pt+mv_rel
@x1: 	dw 319-64
@y1: 	dw 239
; now the main event
; VDU 23, 27, &21, bitmapId; 0;
        db 23,27,0x21
@bufId: dw 0x2000,0x0000
@end: ; no padding required

vdu_buff_screen_paste_tiles:
        ld hl,@begin
        ld bc,@end-@begin
        rst.lil $18
        ret
; VDU 23, 27, &20, bufferId; : Select bitmap (using a buffer ID)
@begin:    db 23,27,0x20
@bufferId: dw 0x2000
; VDU 25, mode, x; y;: PLOT command
           db 25,0xED ; plot_bmp+dr_abs_fg
           dw 0x0000,0x0001
@end: ; no padding required

; VDU 23, 27, 2, w; h; col1; col2;: Create a solid colour rectangular bitmap
; VDU 23, 27, 3, x; y;: Draw current bitmap on screen at pixel position x, y
; VDU 23, 27, &21, w; h; format: Create bitmap from selected buffer *
; Value	Meaning
; 0	RGBA8888 (4-bytes per pixel)
; 1	RGBA2222 (1-bytes per pixel)
; 2	Mono/Mask (1-bit per pixel)
; 3	Reserved for internal use by VDP ("native" format)VDP. 
;     They have some significant limitations, and are not intended for general use.

; =========================================================================
; Sprites
; -------------------------------------------------------------------------
; VDU 23, 27, 4, n: Select sprite n
; VDU 23, 27, 5: Clear frames in current sprite
; VDU 23, 27, 6, n: Add bitmap n as a frame to current sprite (where bitmap's buffer ID is 64000+n)
; VDU 23, 27, &26, n;: Add bitmap n as a frame to current sprite using a 16-bit buffer ID
; VDU 23, 27, 7, n: Activate n sprites
; VDU 23, 27, 8: Select next frame of current sprite
; VDU 23, 27, 9: Select previous frame of current sprite
; VDU 23, 27, 10, n: Select the nth frame of current sprite
; VDU 23, 27, 11: Show current sprite
; VDU 23, 27, 12: Hide current sprite
; VDU 23, 27, 13, x; y;: Move current sprite to pixel position x, y
; VDU 23, 27, 14, x; y;: Move current sprite by x, y pixels
; VDU 23, 27, 15: Update the sprites in the GPU
; VDU 23, 27, 16: Reset bitmaps and sprites and clear all data
; VDU 23, 27, 17: Reset sprites (only) and clear all data
; VDU 23, 27, 18, n: Set the current sprite GCOL paint mode to n **

; =========================================================================
; Mouse cursor
; -------------------------------------------------------------------------
; VDU 23, 27, &40, hotX, hotY: Setup a mouse cursor with a hot spot at hotX, hotY