; https://github.com/envenomator/Agon/blob/master/ez80asm%20examples%20(annotated)/mos_api.inc
;
; Title:	AGON MOS - API for user projects
; Author:	Dean Belfield
;			Adapted for agon-ez80asm by Jeroen Venema
;			Added MOS error codes for return in HL
; Created:	03/08/2022
; Last Updated:	10/08/2023
;
; Modinfo:
; 05/08/2022:	Added mos_feof
; 09/08/2022:	Added system variables: cursorX, cursorY
; 18/08/2022:	Added system variables: scrchar, scrpixel, audioChannel, audioSuccess, vpd_pflags
; 05/09/2022:	Added mos_ren, vdp_pflag_mode
; 24/09/2022:	Added mos_getError, mos_mkdir
; 13/10/2022:	Added mos_oscli
; 23/02/2023:	Added more sysvars, fixed typo in sysvar_audioSuccess, offsets for sysvar_scrCols, sysvar_scrRows
; 04/03/2023:	Added sysvar_scrpixelIndex
; 08/03/2023:	Renamed sysvar_keycode to sysvar_keyascii, added sysvar_vkeycode
; 15/03/2023:	Added mos_copy, mos_getrtc, mos_setrtc, rtc, vdp_pflag_rtc
; 21/03/2023:	Added mos_setintvector, sysvars for keyboard status, vdu codes for vdp
; 22/03/2023:	The VDP commands are now indexed from 0x80
; 29/03/2023:	Added mos_uopen, mos_uclose, mos_ugetc, mos_uputc
; 13/04/2023:	Added FatFS file structures (FFOBJID, FIL, DIR, FILINFO)
; 15/04/2023:	Added mos_getfil, mos_fread, mos_fwrite and mos_flseek
; 19/05/2023:	Added sysvar_scrMode
; 05/06/2023:	Added sysvar_rtcEnable
; 03/08/2023:	Added mos_setkbvector
; 10/08/2023:	Added mos_getkbmap

; VDP control (VDU 23, 0, n)
;
vdp_gp:				EQU 80h
vdp_keycode:		EQU 81h
vdp_cursor:			EQU	82h
vdp_scrchar:		EQU	83h
vdp_scrpixel:		EQU	84h
vdp_audio:			EQU	85h
vdp_mode:			EQU	86h
vdp_rtc:			EQU	87h
vdp_keystate:		EQU	88h
vdp_logicalcoords:	EQU	C0h
vdp_terminalmode:	EQU	FFh

;
; Macro for calling the API
; Parameters:
; - function: One of the function numbers listed below
;
	MACRO	MOSCALL	function
			LD	A, function
			RST.LIL	08h
	ENDMACRO 	

;
; Same as above but keeps IY safe on FFS calls. This was added after some FFS
; functions unexpectedly destroyed IY in the emulator; that behavior may since
; have been fixed. TODO: test current emulator and hardware MOS builds, then
; remove this wrapper if unnecessary: PUSH/POP IY adds avoidable cycles and
; index-register stack operations are costlier than their GP-register forms.
; (Can be used for regular MOS calls as well.)
;
	MACRO	FFSCALL	function
			PUSH IY
			LD	A, function
			RST.LIL	08h
			POP IY
	ENDMACRO 	

; MOS high level functions
;
; Get keycode
; Returns:
;  A: ASCII code of key pressed, or 0 if no key pressed
mos_getkey:			EQU	00h

; Load an area of memory from a file.
; HLU: Address of filename (zero terminated)
; DEU: Address at which to load
; BCU: Maximum allowed size (bytes)
; Returns:
; - A: File error, or 0 if OK
; - F: Carry reset indicates no room for file.
mos_load:			EQU	01h

; Save a file to the SD card from RAM
; HLU: Address of filename (zero terminated)
; DEU: Address to save from
; BCU: Number of bytes to save
; Returns:
; - A: File error, or 0 if OK
; - F: Carry reset indicates no room for file
mos_save:			EQU	02h

; Change directory
; HLU: Address of path (zero terminated)
; Returns:
; - A: File error, or 0 if OK
mos_cd:				EQU	03h

; Directory listing
; HLU: Address of path (zero terminated)
; Returns:
; - A: File error, or 0 if OK
mos_dir:			EQU	04h

; Delete a file from the SD card
; HLU: Address of filename (zero terminated)
; Returns:
; - A: File error, or 0 if OK
mos_del:			EQU	05h

; Rename a file on the SD card
; HLU: Address of filename1 (zero terminated)
; DEU: Address of filename2 (zero terminated)
; Returns:
; - A: File error, or 0 if OK
mos_ren:			EQU	06h

; Make a folder on the SD card
; HLU: Address of filename (zero terminated)
; Returns:
; - A: File error, or 0 if OK
mos_mkdir:			EQU	07h

; Get a pointer to a system variable
; Returns:
; IXU: Pointer to system variables (see mos_api.asm for more details)
mos_sysvars:		EQU	08h

; Invoke the line editor
; HLU: Address of the buffer
; BCU: Buffer length
;   E: 0 to not clear buffer, 1 to clear
; Returns:
;   A: Key that was used to exit the input loop (CR=13, ESC=27)
mos_editline:		EQU	09h

; Open a file
; HLU: Filename
;   C: Mode
; Returns:
;   A: Filehandle, or 0 if couldn't open
mos_fopen:			EQU	0Ah

; Close a file
;   C: Filehandle
; Returns
;   A: Number of files still open
mos_fclose:			EQU	0Bh

; Get a character from a file
;   C: Filehandle
; Returns:
;   A: Character read
;   F: C set if last character in file, otherwise NC
mos_fgetc:			EQU	0Ch

; Write a character to a file
;   C: Filehandle
;   B: Character to write
mos_fputc:			EQU	0Dh

; Check whether we're at the end of the file
;   C: Filehandle
; Returns:
;   A: 1 if at end of file, otherwise 0
mos_feof:			EQU	0Eh

; Copy an error message
;   E: The error code
; HLU: Address of buffer to copy message into
; BCU: Size of buffer
mos_getError:		EQU	0Fh

; Execute a MOS command
; HLU: Pointer the the MOS command string
; DEU: Pointer to additional command structure
; BCU: Number of additional commands
; Returns:
;   A: MOS error code
mos_oscli:			EQU	10h

; Copy a file on the SD card
; HLU: Address of filename1 (zero terminated)
; DEU: Address of filename2 (zero terminated)
; Returns:
; - A: File error, or 0 if OK
mos_copy:			EQU	11h

; Fetch a RTC string
; HLU: Pointer to a buffer to copy the string to
; Returns:
;   A: Length of time
mos_getrtc:			EQU	12h

; Set the RTC
; HLU: Pointer to a buffer with the time data in
mos_setrtc:			EQU	13h

; Set an interrupt vector
; HLU: Pointer to the interrupt vector (24-bit pointer)
;   E: Vector # to set
; Returns:
; HLU: Pointer to the previous vector
mos_setintvector:	EQU	14h

; Open UART1
; IXU: Pointer to UART struct
;	+0: Baud rate (24-bit, little endian)
;	+3: Data bits
;	+4: Stop bits
;	+5: Parity bits
;	+6: Flow control (0: None, 1: Hardware)
;	+7: Enabled interrupts
; Returns:
;   A: Error code (0 = no error)
mos_uopen:			EQU	15h

; Close UART1
mos_uclose:			EQU	16h

; Get a character from UART1
; Returns:
;   A: Character read
;   F: C if successful
;   F: NC if the UART is not open
mos_ugetc:			EQU	17h

; Write a character to UART1
;   C: Character to write
; Returns:
;   F: C if successful
;   F: NC if the UART is not open
mos_uputc:			EQU	18h

; Convert a file handle to a FIL structure pointer
;   C: Filehandle
; Returns:
; HLU: Pointer to a FIL struct
mos_getfil:			EQU	19h

; Read a block of data from a file
;   C: Filehandle
; HLU: Pointer to where to write the data to
; DEU: Number of bytes to read
; Returns:
; DEU: Number of bytes read
mos_fread:			EQU	1Ah

; Write a block of data to a file
;  C: Filehandle
; HLU: Pointer to where the data is
; DEU: Number of bytes to write
; Returns:
; DEU: Number of bytes read
mos_fwrite:			EQU	1Bh

; Move the read/write pointer in a file
;   C: Filehandle
; HLU: Least significant 3 bytes of the offset from the start of the file (DWORD)
;   E: Most significant byte of the offset
; Returns:
;   A: FRESULT
mos_flseek:			EQU	1Ch

; Move the read/write pointer in a file relative to the current position
;   C: Filehandle
; DEU: Signed 24-bit offset
; Returns:
;   A: FRESULT
mos_api_flseek_rel:
	push bc ; back up file handle in c
	push de ; save offset
	MOSCALL mos_getfil
	push hl
	pop iy ; iy points to FIL struct
	ld hl,(iy+fil_fptr) ; get lowest 3 bytes of current position
	xor a ; clear carry
	pop de ; restore offset
	adc hl,de ; adc the offset because we need sign flag
	jp p,@not_neg
	ld hl,0 ; seek to beginning of file
@not_neg:
	pop bc ; restore file handle to c
	ld e,0 ; highest byte of offset
	MOSCALL mos_flseek
	ret

; Set a VDP keyboard packet receiver callback
;   C: If non-zero then set the top byte of HLU(callback address)  to MB (for ADL=0 callers)
; HLU: Pointer to callback
mos_setkbvector:	EQU	1Dh

; Get the address of the keyboard map
; Returns:
; IXU: Base address of the keymap
mos_getkbmap:		EQU	1Eh

; MOS program exit codes
;
EXIT_OK:				EQU  0;	"OK",
EXIT_ERROR_SD_ACCESS:	EQU	 1;	"Error accessing SD card",
EXIT_ERROR_ASSERTION:	EQU  2;	"Assertion failed",
EXIT_SD_CARDFAILURE:	EQU  3;	"SD card failure",
EXIT_FILENOTFOUND:		EQU  4;	"Could not find file",
EXIT_PATHNOTFOUND:		EQU  5;	"Could not find path",
EXIT_INVALIDPATHNAME:	EQU  6;	"Invalid path name",
EXIT_ACCESSDENIED_FULL:	EQU  7;	"Access denied or directory full",
EXIT_ACCESSDENIED:		EQU  8;	"Access denied",
EXIT_INVALIDOBJECT:		EQU  9;	"Invalid file/directory object",
EXIT_SD_WRITEPROTECTED:	EQU 10;	"SD card is write protected",
EXIT_INVALIDDRIVENUMBER:EQU 11;	"Logical drive number is invalid",
EXIT_NOVOLUMEWORKAREA:	EQU 12;	"Volume has no work area",
EXIT_NOVALIDFATVOLUME:	EQU 13;	"No valid FAT volume",
EXIT_ERRORMKFS:			EQU 14;	"Error occurred during mkfs",
EXIT_VOLUMETIMEOUT:		EQU 15;	"Volume timeout",
EXIT_VOLUMELOCKED:		EQU 16;	"Volume locked",
EXIT_LFNALLOCATION:		EQU 17;	"LFN working buffer could not be allocated",
EXIT_MAXOPENFILES:		EQU 18;	"Too many open files",
EXIT_INVALIDPARAMETER:	EQU 19;	"Invalid parameter",
EXIT_INVALIDCOMMAND:	EQU 20;	"Invalid command",
EXIT_INVALIDEXECUTABLE:	EQU 21;	"Invalid executable",

; FatFS file access functions
;
; Open a file
; HLU: Pointer to a blank FIL struct
; DEU: Pointer to the filename (0 terminated)
;   C: File mode
; Returns:
;   A: FRESULT
ffs_fopen:			EQU	80h

; Close a file
; HLU: Pointer to a blank FIL struct
; Returns:
;   A: FRESULT
ffs_fclose:			EQU	81h

; Read data from a file
; HLU: Pointer to a FIL struct
; DEU: Pointer to where to write the file out
; BCU: Number of bytes to read
; Returns:
;   A: FRESULT
; BCU: Number of bytes read
ffs_fread:			EQU	82h

; Write data to a file
; HLU: Pointer to a FIL struct
; DEU: Pointer to the data to write out
; BCU: Number of bytes to write
; Returns:
;   A: FRESULT
; BCU: Number of bytes written
ffs_fwrite:			EQU	83h

; Move the read/write pointer in a file
; HLU: Pointer to a FIL struct
; DEU: Least significant 3 bytes of the offset from the start of the file (DWORD)
;   C: Most significant byte of the offset
; Returns:
;   A: FRESULT
ffs_flseek:			EQU	84h

; not implemented
ffs_ftruncate:		EQU	85h

; not implemented
ffs_fsync:			EQU	86h

; not implemented
ffs_fforward:		EQU	87h

; not implemented
ffs_fexpand:		EQU	88h

; not implemented
ffs_fgets:			EQU	89h

; not implemented
ffs_fputc:			EQU	8Ah

; not implemented
ffs_fputs:			EQU	8Bh

; not implemented
ffs_fprintf:		EQU	8Ch

; not implemented
ffs_ftell:			EQU	8Dh

; Check for EOF
; HLU: Pointer to a FILINFO struct
; Returns:
;   A: 1 if end of file, otherwise 0
ffs_feof:			EQU	8Eh

; not implemented
ffs_fsize:			EQU	8Fh

; not implemented
ffs_ferror:			EQU	90h

; FatFS directory access functions
;
; Open a directory
; HLU: Pointer to a blank DIR struct
; DEU: Pointer to the directory path
; Returns:
; A: FRESULT
ffs_dopen:			EQU	91h

; Close a directory
; HLU: Pointer to an open DIR struct
; Returns:
; A: FRESULT
ffs_dclose:			EQU	92h

; Read the next FILINFO from an open DIR
; HLU: Pointer to an open DIR struct
; DEU: Pointer to an empty FILINFO struct
; Returns:
; A: FRESULT
ffs_dread:			EQU	93h

; not implemented
ffs_dfindfirst:		EQU	94h

; not implemented
ffs_dfindnext:		EQU	95h

; FatFS file and directory management functions
;
; Check file exists
; HLU: Pointer to a FILINFO struct
; DEU: Pointer to the filename (0 terminated)
; Returns:
;   A: FRESULT
ffs_stat:			EQU	96h

; not implemented
ffs_unlink:			EQU	97h

; not implemented
ffs_rename:			EQU	98h

; not implemented
ffs_chmod:			EQU	99h

; not implemented
ffs_utime:			EQU	9Ah

; not implemented
ffs_mkdir:			EQU	9Bh

; not implemented
ffs_chdir:			EQU	9Ch

; not implemented
ffs_chdrive:		EQU	9Dh

; Copy the current directory (string) into buffer (hl)
; HLU: Pointer to a buffer
; BCU: Maximum length of buffer
; Returns:
; A: FRESULT
ffs_getcwd:			EQU	9Eh

; FatFS volume management and system configuration functions
;
; not implemented
ffs_mount:			EQU	9Fh

; not implemented
ffs_mkfs:			EQU	A0h

; not implemented
ffs_fdisk:			EQU	A1h

; not implemented
ffs_getfree:		EQU	A2h

; not implemented
ffs_getlabel:		EQU	A3h

; not implemented
ffs_setlabel:		EQU	A4h

; not implemented
ffs_setcp:			EQU	A5h
	
; File access modes
;
fa_read:			EQU	01h
fa_write:			EQU	02h
fa_open_existing:	EQU	00h
fa_create_new:		EQU	04h
fa_create_always:	EQU	08h
fa_open_always:		EQU	10h
fa_open_append:		EQU	30h
	
; System variable indexes for api_sysvars
; Index into _sysvars in globals.asm
;
sysvar_time:			EQU	00h	; 4: Clock timer in centiseconds (incremented by 2 every VBLANK)
sysvar_vpd_pflags:		EQU	04h	; 1: Flags to indicate completion of VDP commands
sysvar_keyascii:		EQU	05h	; 1: ASCII keycode, or 0 if no key is pressed
sysvar_keymods:			EQU	06h	; 1: Keycode modifiers
sysvar_cursorX:			EQU	07h	; 1: Cursor X position
sysvar_cursorY:			EQU	08h	; 1: Cursor Y position
sysvar_scrchar:			EQU	09h	; 1: Character read from screen
sysvar_scrpixel:		EQU	0Ah	; 3: Pixel data read from screen (R,B,G)
sysvar_audioChannel:	EQU	0Dh	; 1: Audio channel 
sysvar_audioSuccess:	EQU	0Eh	; 1: Audio channel note queued (0 = no, 1 = yes)
sysvar_scrWidth:		EQU	0Fh	; 2: Screen width in pixels
sysvar_scrHeight:		EQU	11h	; 2: Screen height in pixels
sysvar_scrCols:			EQU	13h	; 1: Screen columns in characters
sysvar_scrRows:			EQU	14h	; 1: Screen rows in characters
sysvar_scrColours:		EQU	15h	; 1: Number of colours displayed
sysvar_scrpixelIndex:	EQU	16h	; 1: Index of pixel data read from screen
sysvar_vkeycode:		EQU	17h	; 1: Virtual key code from FabGL
sysvar_vkeydown:		EQU	18h	; 1: Virtual key state from FabGL (0=up, 1=down)
sysvar_vkeycount:		EQU	19h	; 1: Incremented every time a key packet is received
sysvar_rtc:				EQU	1Ah	; 6: Real time clock data
sysvar_spare:			EQU	20h	; 2: Spare, previously used by rtc
sysvar_keydelay:		EQU	22h	; 2: Keyboard repeat delay
sysvar_keyrate:			EQU	24h	; 2: Keyboard repeat reat
sysvar_keyled:			EQU	26h	; 1: Keyboard LED status
sysvar_scrMode:			EQU	27h	; 1: Screen mode
sysvar_rtcEnable:		EQU	28h	; 1: RTC enable flag (0: disabled, 1: use ESP32 RTC)
	
; Flags for the VPD protocol
;
vdp_pflag_cursor:		EQU	00000001b
vdp_pflag_scrchar:		EQU	00000010b
vdp_pflag_point:		EQU	00000100b
vdp_pflag_audio:		EQU	00001000b
vdp_pflag_mode:			EQU	00010000b
vdp_pflag_rtc:			EQU	00100000b

;
; FatFS structures
; These mirror the structures contained in src_fatfs/ff.h in the MOS project
;
; Object ID and allocation information (FFOBJID)
;
; Indexes into FFOBJID structure
ffobjid_fs:			EQU	0	; 3: Pointer to the hosting volume of this object
ffobjid_id:			EQU	3	; 2: Hosting volume mount ID
ffobjid_attr:		EQU	5	; 1: Object attribute
ffobjid_stat:		EQU	6	; 1: Object chain status (b1-0: =0:not contiguous, =2:contiguous, =3:fragmented in this session, b2:sub-directory stretched)
ffobjid_sclust:		EQU	7	; 4: Object data start cluster (0:no cluster or root directory)
ffobjid_objsize:	EQU	11	; 4: Object size (valid when sclust != 0)
;
; File object structure (FIL)
;
; Indexes into FIL structure
fil_obj:		EQU 0	; 15: Object identifier
fil_flag:		EQU	15 	;  1: File status flags
fil_err:		EQU	16	;  1: Abort flag (error code)
fil_fptr:		EQU	17	;  4: File read/write pointer (Zeroed on file open)
fil_clust:		EQU	21	;  4: Current cluster of fpter (invalid when fptr is 0)
fil_sect:		EQU	25	;  4: Sector number appearing in buf[] (0:invalid)
fil_dir_sect:	EQU	29	;  4: Sector number containing the directory entry
fil_dir_ptr:	EQU	33	;  3: Pointer to the directory entry in the win[]
;
; Directory object structure (DIR)
; Indexes into DIR structure
dir_obj:		EQU  0	; 15: Object identifier
dir_dptr:		EQU	15	;  4: Current read/write offset
dir_clust:		EQU	19	;  4: Current cluster
dir_sect:		EQU	23	;  4: Current sector (0:Read operation has terminated)
dir_dir:		EQU	27	;  3: Pointer to the directory item in the win[]
dir_fn:			EQU	30	; 12: SFN (in/out) {body[8],ext[3],status[1]}
dir_blk_ofs:	EQU	42	;  4: Offset of current entry block being processed (0xFFFFFFFF:Invalid)
;
; File information structure (FILINFO)
;
; Indexes into FILINFO structure
filinfo_fsize:		EQU 0	;   4: File size
filinfo_fdate:		EQU	4	;   2: Modified date
filinfo_ftime:		EQU	6	;   2: Modified time
filinfo_fattrib:	EQU	8	;   1: File attribute
filinfo_altname:	EQU	9	;  13: Alternative file name
filinfo_fname:		EQU	22	; 256: Primary file name
