#!/usr/bin/env python3
"""
Tile two images horizontally in a mosaic.

(This is much worse than using imagemagick).
"""

import argparse
from pathlib import Path

from PIL import Image


def create_horizontal_mosaic(input_paths: list[Path], output_path: Path):
    """Create a horizontal mosaic of two or more images."""
    if len(input_paths) < 2:
        raise ValueError("Please supply at least two images.")

    imgs = [Image.open(path) for path in input_paths]

    if len({img.size for img in imgs}) > 1:
        raise ValueError("Input images must have equal sizes")

    # Calculate the total width and height for the new image
    total_width = imgs[0].size[0] * len(imgs)
    total_height = imgs[0].size[1]

    # Create a new blank image with the combined width and max height
    mosaic = Image.new("RGB", (total_width, total_height))

    # Paste the two images side by side
    for index, img in enumerate(imgs):
        mosaic.paste(img, (index * img.size[0], 0))

    # Save the resulting mosaic image
    mosaic.save(output_path)
    print(f"Mosaic saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()

    create_horizontal_mosaic(args.input, args.output)
