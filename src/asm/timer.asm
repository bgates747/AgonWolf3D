; Table 32. Timer Control Registers
; this constant is the base address of the timer control registers
; each timer takes three bytes:
;   0: control register
;   1: low byte of timer reset value
;   2: high byte of timer reset value
; note that the value is only 8-bits, so we use in0/out0 i/o calls,
; which correctly force the high and upper bytes of the address bus to zero
TMR_CTL:     equ 80h

; Timer Control Register Bit Definitions
PRT_IRQ_0:    equ %00000000 ; The timer does not reach its end-of-count value. 
                            ; This bit is reset to 0 every time the TMRx_CTL register is read.
PRT_IRQ_1:    equ %10000000 ; The timer reaches its end-of-count value. If IRQ_EN is set to 1, 
                            ; an interrupt signal is sent to the CPU. This bit remains 1 until 
                            ; the TMRx_CTL register is read.

IRQ_EN_0:     equ %00000000 ; Timer interrupt requests are disabled.
IRQ_EN_1:     equ %01000000 ; Timer interrupt requests are enabled.

PRT_MODE_0:   equ %00000000 ; The timer operates in SINGLE PASS mode. PRT_EN (bit 0) is reset to
                            ;  0, and counting stops when the end-of-count value is reached.
PRT_MODE_1:   equ %00010000 ; The timer operates in CONTINUOUS mode. The timer reload value is
                            ; written to the counter when the end-of-count value is reached.

; CLK_DIV is a 2-bit mask that sets the timer input source clock divider
CLK_DIV_256:  equ %00001100 ; 
CLK_DIV_64:   equ %00001000 ; 
CLK_DIV_16:   equ %00000100 ;
CLK_DIV_4:    equ %00000000 ;

RST_EN_0:     equ %00000000 ; The reload and restart function is disabled. 
RST_EN_1:     equ %00000010 ; The reload and restart function is enabled. 
                            ; When a 1 is written to this bit, the values in the reload registers
                            ;  are loaded into the downcounter when the timer restarts. The 
                            ; programmer must ensure that this bit is set to 1 each time 
                            ; SINGLE-PASS mode is used.

; disable/enable the programmable reload timer
PRT_EN_0:     equ %00000000 ;
PRT_EN_1:     equ %00000001 ;

; Table 37. Timer Input Source Select Register
; Each of the 4 timers are allocated two bits of the 8-bit register
; in little-endian order, with TMR0 using bits 0 and 1, TMR1 using bits 2 and 3, etc.
;   00: System clock / CLK_DIV
;   01: RTC / CLK_DIV
;   NOTE: these are the values given in the manual, but it may be a typo
;   10: GPIO port B pin 1.
;   11: GPIO port B pin 1.
TMR_ISS:   equ 92h ; register address

; Table 51. Real-Time Clock Control Register
RTC_CTRL: equ EDh ; register address

; alarm interrupt disable/enable
RTC_ALARM_0:    equ %00000000
RTC_ALARM_1:    equ %10000000

; interrupt on alarm disable/enable
RTC_INT_ENT_0:  equ %00000000
RTC_INT_ENT_1:  equ %01000000

RTC_BCD_EN_0:   equ %00000000   ; RTC count and alarm registers are binary
RTC_BCD_EN_1:   equ %00100000   ; RTC count and alarm registers are BCD

RTC_CLK_SEL_0:  equ %00000000   ; RTC clock source is crystal oscillator output (32768 Hz). 
                                ; On-chip 32768 Hz oscillator is enabled.
RTC_CLK_SEL_1:  equ %00010000   ; RTC clock source is power line frequency input as set by FREQ_SEL.
                                ; On-chip 32768 Hz oscillator is disabled.

RTC_FREQ_SEL_0: equ %00000000   ; 60 Hz power line frequency.
RTC_FREQ_SEL_1: equ %00001000   ; 50 Hz power line frequency.

RTC_SLP_WAKE_0: equ %00000000   ; RTC does not generate a sleep-mode recovery reset.
RTC_SLP_WAKE_1: equ %00000010   ; RTC generates a sleep-mode recovery reset.

RTC_UNLOCK_0:   equ %00000000   ; RTC count registers are locked to prevent Write access.
                                ; RTC counter is enabled.
RTC_UNLOCK_1:   equ %00000001   ; RTC count registers are unlocked to allow Write access. 
                                ; RTC counter is disabled.

; returns 0 if running on hardware, 1 if running on emulator
prt_calibrate:
; set a MOS timer
    ld hl,120*1 ; 1 second
    ld iy,timer_test
    call timer_set
; set a PRT timer
    ld hl,1000
    ld (prt_reload),hl
    call prt_set
@loop:
; check time remaining on MOS timer
    call timer_get
    jp z,@done ; time expired, so quit
    jp m,@done ; time past expiration (negative), so quit
    jr @loop
@done:
    ld bc,0x1200 ; default value for running on hardware
    ld (prt_reload),bc
    ld de,(prt_irq_counter)
    ld hl,3942 ; halfway between 4608 for real hardware and 3276 for emulator
    xor a; clear carry, zero is default value for running on hardware
    sbc hl,de
    ld hl,on_hardware ; default message for running on hardware
    ret m ; negative result means we're on hardware
    inc a ; we're on emulator
    ld bc,0x0CCC
    ld (prt_reload),bc
    ld hl,on_emulator
    ret

calibrating_timer: defb "Calibrating timer\r\n",0
on_emulator: defb "Running on emulator\r\n",0
on_hardware: defb "Running on hardware\r\n",0

; 3276d = 1,000 milliseconds on emulator
; 1200h = 1,000 milliseconds on hardware
prt_reload: dl 0x000000
prt_reload_str: ds 8

; set PRT timer
prt_set:
; set PRT reload value
    ld hl, (prt_reload)
    out0 ($84), l
	out0 ($85), h
; enable PRT, with interrupt and CONTINUOUS mode, clock divider 4
    ld a,PRT_IRQ_0 | IRQ_EN_1 | PRT_MODE_1 | CLK_DIV_4 | RST_EN_1 | PRT_EN_1 ; 0x53
	out0 ($83), a
    ret

; ===============================================
; PRT Timer Interrupt Handling
; https://github.com/tomm/agon-cpu-emulator/blob/main/sdcard/regression_suite/timerirq.asm
; -----------------------------------------------
prt_irq_init:
    ; set up interrupt vector table 2
	ld hl, 0
	ld a,($10c)
	ld l, a
	ld a,($10d)
	ld h, a

	; skip over CALL ($c3)
	inc hl
	; load address of jump into vector table 2 (in ram)
	ld hl,(hl)

	; write CALL prt_irq_handler to vector table 2
	ld a, $c3
	ld (hl), a
	inc hl
	ld de, prt_irq_handler
	ld (hl), de

    ret

prt_irq_handler:
	di
	push af
    push hl
	in0 a,($83)
	ld (prt_got_irq),a
	ld hl,(prt_irq_counter)
	inc hl
	ld (prt_irq_counter),hl
    pop hl
	pop af
	ei
	reti.l

prt_got_irq:
	.db 0
prt_irq_counter:
	.dl 0
prt_irq_counter_str: ds 8

; ===============================================
; Timer functions
; -----------------------------------------------
; set a countdown timer
; inputs: hl = time to set in 1/120ths of a second; iy = pointer to 3-byte buffer holding start time, iy+3 = pointer to 3-byte buffer holding timer set value
; returns: hl = current time 
timer_set:
    ld (iy+3),hl            ; set time remaining
    MOSCALL mos_sysvars     ; ix points to syvars table
    ld hl,(ix+sysvar_time)  ; get current time
    ld (iy+0),hl            ; set start time
    ret

; gets time remaining on a countdown timer
; inputs: iy = pointer to 3-byte buffer holding start time, iy+3 = pointer to 3-byte buffer holding timer set value
; returns: hl pos = time remaining in 1/120ths of a second, hl neg = time past expiration
;          sign flags: pos = time not expired, zero or neg = time expired
timer_get:
    MOSCALL mos_sysvars     ; ix points to syvars table
    ld de,(ix+sysvar_time)  ; get current time
    ld hl,(iy+0)            ; get start time
    xor a                   ; clear carry
    sbc hl,de               ; hl = time elapsed (will always be zero or negative)
    ld de,(iy+3)            ; get timer set value
    xor a                   ; clear carry
    adc hl,de               ; hl = time remaining 
                            ; (we do adc because add hl,rr doesn't set sign or zero flags)
    ret

timer_test: ds 6 ; example of a buffer to hold timer data


; ------------------
; delay routine
; Author: Richard Turrnidge
; https://github.com/richardturnnidge/lessons/blob/main/slowdown.asm
; routine waits a fixed time, then returns
; arrive with A =  the delay byte. One bit to be set only.
; eg. ld A, 00000100b

multiPurposeDelay:
    push af                      
    push bc
    push ix                 
    ld b, a 
    ld a,$08
    RST.LIL	08h                 ; get IX pointer to sysvars               

waitLoop:

    ld a, (ix + 0)              ; ix+0h is lowest byte of clock timer

                                ;   we check if bit set is same as last time we checked.
                                ;   bit 0 - don't use
                                ;   bit 1 - changes 64 times per second
                                ;   bit 2 - changes 32 times per second
                                ;   bit 3 - changes 16 times per second

                                ;   bit 4 - changes 8 times per second
                                ;   bit 5 - changes 4 times per second
                                ;   bit 6 - changes 2 times per second
                                ;   bit 7 - changes 1 times per second
    and b 
    ld c,a 
    ld a, (oldTimeStamp)
    cp c                        ; is A same as last value?
    jr z, waitLoop              ; loop here if it is
    ld a, c 
    ld (oldTimeStamp), a        ; set new value

    pop ix
    pop bc
    pop af
    ret

oldTimeStamp:   .db 00h