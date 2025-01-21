#!/usr/bin/env python3
"""
Make an animated GIF from one or more frames.

(Like mosaic.py, this is a cheap imitation of imagemagick.)
"""

import argparse
from pathlib import Path

from PIL import Image


def create_animated_gif(
    input_paths: list[Path], output_path: Path, duration: int = 500, loop: int = 0
):
    """Create an animated GIF from two or more image frames."""
    if len(input_paths) < 2:
        raise ValueError("Please supply at least two images.")

    imgs = [Image.open(path) for path in input_paths]

    if len({img.size for img in imgs}) > 1:
        raise ValueError("Input images must have equal sizes")

    # Save the frames as an animated GIF
    imgs[0].save(
        output_path,
        save_all=True,
        append_images=imgs[1:],
        duration=duration,
        loop=loop,
        format="GIF",
    )
    print(f"Animated GIF saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create an animated gif from multiple images."
    )
    parser.add_argument("input", type=Path, nargs="+", help="Input image(s)")
    parser.add_argument("--output", type=Path, required=True, help="Output filename")
    parser.add_argument(
        "--duration", default=500, metavar="ms", help="Delay (in ms) between frames"
    )
    parser.add_argument(
        "--repeat",
        default=0,
        metavar="count",
        help="Animation repeat count (0 for unlimited)",
    )

    args = parser.parse_args()

    create_animated_gif(
        args.input, args.output, duration=args.duration, loop=args.repeat
    )
