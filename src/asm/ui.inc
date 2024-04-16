BUF_UI_001: equ 0x2000 ; lower panel

load_ui_images:
; lower panel
	ld hl,F_UI_001
	ld de,filedata
	ld bc,102400
	ld a,mos_load
	RST.LIL 08h
	ld hl,BUF_UI_001
	ld bc,320
	ld de,79
	ld ix,25280
	call vdu_load_bmp2_from_file

    ret

F_UI_001: db "ui/lower_panel.rgba2",0

