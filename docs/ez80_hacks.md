# eZ80 Assembly Hacks

This living note records useful eZ80 idioms whose behavior is non-obvious,
especially when it depends on ADL mode or an undocumented instruction detail.
Verify such behavior on the project's assembler, emulator, and hardware before
treating it as portable beyond the Agon toolchain.

## Clear HLU While Preserving HL

In ADL mode, `HL` is the low 16-bit portion of the 24-bit `UHL` register and
`HLU` names its upper byte. The following idiom preserves the low word while
clearing the upper byte:

```asm
    dec hl
    inc.s hl ; undocumented: preserves HL and clears HLU
```

The short-mode `.s` increment clears HLU as an undocumented side effect. The
preceding 24-bit decrement compensates for the increment in the low word,
including when that word wraps through zero.

This is useful for zero-extending a two-byte value loaded with an ADL
three-byte memory load:

```asm
    ld hl,(agnb_metadata+agnb_meta_bufferId)
    dec hl
    inc.s hl ; bufferId remains in HL; the unwanted following byte is removed
```

Compared with clearing UHL and loading the two component bytes separately, the
idiom is faster and smaller. In the AGNB loader, applying it to two dimension
loads and three bufferId loads reduced the assembled application by 34 bytes.

Do not use this sequence when the entire 24-bit register must become zero. It
preserves the existing low 16 bits by design.

The same trick works for every 24-bit register pair, including the index
registers:

```asm
    dec bc
    inc.s bc ; clears BCU while preserving BC

    dec de
    inc.s de ; clears DEU while preserving DE

    dec ix
    inc.s ix ; clears IXU while preserving IX

    dec iy
    inc.s iy ; clears IYU while preserving IY
```

Use the corresponding pair for whichever 16-bit value must be zero-extended.
The index-register forms are valid but retain the eZ80's usual extra cycle cost
for IX/IY operations.

This convention was already used and documented in AgonVideo's `macros.inc`
and repeatedly exercised in AgonMaths' soft-float conversion routines.

## Parenthesize or Reorder Constant Expressions for `ez80asm`

Do not assume normal multiplication-before-addition precedence in `ez80asm`
constant expressions. The assembler evaluates this expression left to right:

```asm
    ld de,agnb_list_type_size+3*agnb_chunk_header_size
```

With values 4 and 8, it emits `(4+3)*8 = 56`, not `4+(3*8) = 28`.
The assembler does not accept parentheses in this operand, so put the
multiplication first:

```asm
    ld de,3*agnb_chunk_header_size+agnb_list_type_size
```

Confirm critical calculated constants in the generated `.lst` file. For this
example the immediate bytes must encode `0x00001C`, not `0x000038`.

This bug appeared in the AGNB reader's minimum `LIST BUFR` payload check.
Normal image records were larger than the erroneous 56-byte threshold, hiding
the defect. A valid 1-by-1 RGBA2222 placeholder has a 44-byte LIST payload and
therefore failed with `agnb_error_chunk` (`07`) until the expression was
reordered.

## Simulate Indirect Calls Through `HL`, `IX`, or `IY`

The eZ80 provides `jp (hl)` but no corresponding indirect `call (hl)`.
`CALL_HL` in `macros.inc` constructs the missing call by pushing the address
immediately after the macro expansion, then jumping through `HL`:

```asm
; inputs: HL = subroutine address
; destroys: BC, plus whatever the subroutine destroys
    MACRO CALL_HL
    ld bc,$+6
    push bc
    jp (hl)
    ENDMACRO
```

In ADL mode the pushed `BC` is the complete 24-bit return address. The macro
expands to six bytes, so `$+6` identifies the first instruction after
`jp (hl)`. When the indirect subroutine executes `ret`, it pops that synthetic
address and resumes after the macro exactly as if the processor supported
`call (hl)`.

This is particularly useful for function-pointer tables, callbacks, and state
machines in which the caller must perform more work after the indirect
subroutine returns. Account for the unconditional destruction of `BC`, and
ensure the called routine obeys the normal stack contract.

`CALL_IX` and `CALL_IY` use the same technique, substituting `jp (ix)` or
`jp (iy)` while retaining the six-byte expansion and synthetic return address.
A separate useful callback pattern is:

```asm
    call callback_trampoline
    ; continuation

callback_trampoline:
    ld hl,(callback_address)
    jp (hl)
```

Here the real `call` has already stacked the continuation address, so the
trampoline can tail-jump through `HL`; the callback's `ret` returns directly
to the continuation. This avoids the macro's `BC` clobber when a dedicated
trampoline is a natural part of the API.
