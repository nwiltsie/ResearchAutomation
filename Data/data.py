#!/usr/bin/env python3
"""Demonstrate that raw data can be interpreted in many different ways."""

import struct
import tempfile
import time
import webbrowser

from pathlib import Path
from string import Template


HTML_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RGBA Color Visualizer</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        div {
            width: 200px;
            height: 200px;
            border: 1px solid #000;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
    </style>
</head>
<body>
    <div style="background: $rgb_color">$rgb_color</div>
    <div style="background: $rgba_color">$rgba_color</div>
</body>
</html>
""")


def decode():
    """Decode the data."""
    data = b"\x44\x6f\x67\x3f"

    red, green, blue, alpha = struct.unpack("4b", data)

    print("Hex:    ", " ".join(f"0x{byte:02x}" for byte in data))
    print("ASCII:  ", struct.unpack("4s", data)[0].decode("ascii"))
    print("Integer:", struct.unpack("i", data)[0])
    print("Float:  ", struct.unpack("f", data)[0])
    print("RGBA:   ", red, green, blue, alpha)

    rgb_color = f"rgb({red},{green},{blue})"
    rgba_color = f"rgba({red},{green},{blue},{alpha / 0xFF:0.2f})"

    with tempfile.TemporaryDirectory() as tempdir:
        html_file = Path(tempdir, "color.html")

        html_file.write_text(
            HTML_TEMPLATE.substitute(rgb_color=rgb_color, rgba_color=rgba_color),
            encoding="utf-8",
        )

        # There's a race condition between the browser opening this file and
        # the file being deleted. Gloss over it by waiting for 1 second (this
        # is not a robust fix)
        webbrowser.open(f"file://{html_file}")
        time.sleep(1)


if __name__ == "__main__":
    decode()
