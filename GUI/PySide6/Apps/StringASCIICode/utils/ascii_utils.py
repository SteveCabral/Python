import unicodedata

# Maps control-character code points to short display tokens.
_CONTROL_TOKENS: dict[int, str] = {
    0:  '<NUL>',
    1:  '<SOH>',
    2:  '<STX>',
    3:  '<ETX>',
    4:  '<EOT>',
    5:  '<ENQ>',
    6:  '<ACK>',
    7:  '<BEL>',
    8:  '<BS>',
    9:  '<TAB>',
    10: '<LF>',
    11: '<VT>',
    12: '<FF>',
    13: '<CR>',
    14: '<SO>',
    15: '<SI>',
    16: '<DLE>',
    17: '<DC1>',
    18: '<DC2>',
    19: '<DC3>',
    20: '<DC4>',
    21: '<NAK>',
    22: '<SYN>',
    23: '<ETB>',
    24: '<CAN>',
    25: '<EM>',
    26: '<SUB>',
    27: '<ESC>',
    28: '<FS>',
    29: '<GS>',
    30: '<RS>',
    31: '<US>',
    32: '<SP>',
    127: '<DEL>',
}


def get_char_display(ch: str) -> str:
    """Return a displayable token for a character.

    Control characters and plain space are shown as <TOKEN>.
    All other printable characters are returned as-is.
    """
    return _CONTROL_TOKENS.get(ord(ch), ch)


def get_description(ch: str) -> str:
    """Return the Unicode name for a character, with a safe fallback."""
    try:
        return unicodedata.name(ch)
    except ValueError:
        code = ord(ch)
        if code < 32:
            return f'CONTROL CHARACTER {code}'
        return f'CHARACTER U+{code:04X}'


def char_to_hex(ch: str) -> str:
    """Return the hex code point in 0xNN format (minimum 2 digits)."""
    return f'0x{ord(ch):02X}'
