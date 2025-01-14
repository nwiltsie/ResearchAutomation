#!/usr/bin/env python3
"""Demonstrate the effect of various encodings."""


def bytes_to_hex(data: bytes) -> str:
    """Return a hex string like '0x32 0x4f' from the data."""
    return " ".join(f"0x{byte:02x}" for byte in data)


def draw_box(data: bytes, encoding: str):
    """Draw the characters associated bytes in boxes."""
    box_t_down = "┬"
    box_t_up = "┴"
    box_vert = "│"
    box_horiz = "─"
    box_corners = ("┌", "┐", "└", "┘")

    indent = "   "

    top_str = indent + box_corners[0]
    total_char_str = indent + box_vert
    total_hex_str = indent + box_vert
    bottom_str = indent + box_corners[2]

    # Decode with surrogateescape so that we can back out what bytes went into
    # each character
    for char in data.decode(encoding, errors="surrogateescape"):
        # Re-encode the character into the original bytes
        encoded_char = char.encode(encoding, errors="surrogateescape")

        hex_str = bytes_to_hex(encoded_char)
        # Pad out the width to account for the separators
        hex_str = " " + hex_str.replace(" ", "   ") + " "

        # Decode the bytes again, replacing the character on errors
        total_char_str += (
            f"`{encoded_char.decode(encoding, errors='replace')}`".center(
                len(hex_str), " "
            )
            + box_vert
        )
        total_hex_str += hex_str + box_vert

        # This is a total cheat for the specific example I am providing. It's
        # _very_ difficult to determine the printing width of an arbitrary
        # unicode character, so I'm just cheating.
        if char == "😊":
            total_char_str = total_char_str[:-2] + box_vert

        top_str += box_horiz * len(hex_str) + box_t_down
        bottom_str += box_horiz * len(hex_str) + box_t_up

    # Fix up the trailing corners
    top_str = top_str[:-1] + box_corners[1]
    bottom_str = bottom_str[:-1] + box_corners[3]

    print(top_str)
    print(total_char_str)
    print(total_hex_str)
    print(bottom_str)
    print()


def print_encodings(data, encodings):
    """Main entrypoint."""

    width = max(len(x) for x in encodings)

    for encoding in encodings:
        print(
            f"{encoding:<{width}s}:",
            data.decode(encoding, errors="replace"),
        )

        draw_box(data, encoding)


if __name__ == "__main__":
    print_encodings(b"\x45\x6c\x20\x4e\x69\xc3\xb1\x6f", ("UTF-8", "windows-1252"))

    print_encodings(b"\x45\x6c\x20\x4e\x69\xf1\x6f", ("windows-1252", "UTF-8"))

    print_encodings(
        b"\x49\x20\xe2\x99\xa5\x20\x50\x79\x74\x68\x6f\x6e", ("UTF-8", "windows-1252")
    )

    print_encodings(
        b"\x43\x61\x66\xc3\xa9\x20\xf0\x9f\x98\x8a", ("UTF-8", "ISO-8859-1")
    )
