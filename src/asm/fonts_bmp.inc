; plots a bitmap character to the screen
; inputs: a; ascii character to plot
;      bc,de = x,y screen coordinates in pixels
;      ix pointed at the font definition lut
; returns: bc as the next x coordinate to plot
;          pretty pixels which hopefully resemble readable text
; destroys: lotsa stuff
font_bmp_plot:
; back up bc,de
    push bc
    push de
; get the buffer id of the character
    sub 32 ; lookup table starts at ascii 32
    ld b,6 ; six bytes per lookup record
    ld c,a
    mlt bc
    add ix,bc ; now ix points to the character definition
    ld hl,(ix+3) ; hl has the buffer id
    call vdu_buff_select
; plot the character
    pop de
    ld a,(ix+2) ; a has the y-offset of the character
    add a,e ; add the y-coordinate
    ld e,a
    ld a,0 ; can't xor it because we need carry
    adc a,d
    ld d,a ; plot_y now correct for the character
    pop bc ; plot_x
    push bc ; we want it back after the plot
    call vdu_plot_bmp
; now set bc to the next x coordinate
    pop bc
    ld a,(ix+0) ; a has the width of the character
    add a,2 ; add a little padding between characters
    add a,c ; bump the original x-coordinate
    ld c,a
    ld a,0 ; can't xor it because we need carry
    adc a,b
    ld b,a ; plot_x now correct for the next character
    ret

; plots a zero-terminated string of bitmap characters to the screen
; inputs: hl; pointer to the string
;       bc,de = x,y screen coordinates in pixels
;       ix pointed at the font definition lut
; returns: bc as the next x coordinate to plot
;          de as the next y coordinate to plot
;          pretty pixels which hopefully resemble readable text
font_bmp_print:
@next_char:
; fetch the next character in the string
    ld a,(hl) ; a has the ascii value of the character
    cp 0 ; is it zero?
    ret z ; if so, we're done
    inc hl ; point to the next character
    push hl ; save the pointer
    push de ; save our y-coordinate
    push ix ; save the font lut pointer
    call font_bmp_plot ; plot the character
    pop ix ; restore the font lut pointer
    pop de ; restore our y-coordinate
    pop hl ; restore the pointer
    jp @next_char ; loop