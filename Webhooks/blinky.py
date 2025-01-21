#!/usr/bin/env python3
"""Library to interface with blinkytape."""

import argparse
import struct
import time
from pathlib import Path

import serial
import webcolors


def send_color(blinky_port: Path, color: webcolors.IntegerRGB):
    """Set all of the blinkytape LEDs to the input color."""
    with serial.Serial(str(blinky_port), 115200, write_timeout=1) as blinky:
        # The blinkytape has 60 LEDs. It is programmed by sending three bytes
        # of RGB color (capped at 254 / 0xFE) for each LED, then a single 255 /
        # 0xFF byte.
        blinky.write(
            60
            * struct.pack(
                "3B", min(color.red, 254), min(color.green, 254), min(color.blue, 254)
            )
        )
        blinky.flush()
        blinky.write(struct.pack("B", 255))
        blinky.flush()

        # This is irritating - as far as I can tell there is no way to
        # determine when the output buffer has been fully drained (flush()
        # passes it off to another layer). Exiting too fast will close the
        # connection. Waiting here seems to work, but I don't like it.
        time.sleep(0.01)


def send_cylon(blinky_port: Path):
    """Set the blinkytape to show a cylon animation."""
    # Establish a three byte wide pattern
    data = struct.pack("9B171x", 128, 0, 0, 254, 0, 0, 128, 0, 0)

    with serial.Serial(str(blinky_port), 115200, write_timeout=1) as blinky:
        for _ in range(58):
            blinky.write(data)
            blinky.write(struct.pack("B", 255))
            blinky.flush()
            time.sleep(0.01)

            # Shift the pattern down by one pixel (three bytes)
            data = data[-3:] + data[:-3]

        for _ in range(58):
            # Shift the pattern up by one pixel (three bytes)
            data = data[3:] + data[:3]

            blinky.write(data)
            blinky.write(struct.pack("B", 255))
            blinky.flush()
            time.sleep(0.01)

        # Clear all of the LEDs
        blinky.write(struct.pack("180x1B", 255))
        blinky.flush()
        time.sleep(0.01)


def guess_blinkyport() -> Path:
    """Guess at the default serial port for the blinkytape."""
    # Guess at the correct port
    all_ports = Path("/dev").glob("tty.usbmodem*")
    if not all_ports:
        raise RuntimeError("Could not determine serial port to use for blinkytape")

    return sorted(all_ports)[0]


def named_color(value) -> webcolors.IntegerRGB:
    """Custom argparse type to convert a color name to an RGB tuple."""
    try:
        return webcolors.name_to_rgb(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid color name '{value}': {e}") from e


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--blinkyport",
        metavar="port",
        type=Path,
        help="Path to the blinkytape serial port (e.g. /dev/tty.usbmodemXXXX)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--color", metavar="name", type=named_color, help="Color name to display"
    )
    group.add_argument("--cylon", action="store_true", help="Display a cylon pattern")

    args = parser.parse_args()

    if not args.blinkyport:
        args.blinkyport = guess_blinkyport()

    if args.cylon:
        send_cylon(args.blinkyport)
    else:
        send_color(args.blinkyport, args.color)
        time.sleep(0.05)
