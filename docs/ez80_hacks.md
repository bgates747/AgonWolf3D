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
