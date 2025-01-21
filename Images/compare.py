#!/usr/bin/env python3
"""Compare two images."""

import sys
from pathlib import Path

from PIL import Image


def process_images(input_path1: Path, input_path2: Path, output_path: Path) -> bool:
    """Compare two images, generating a difference image and returning True if they match."""
    try:
        # Load the images
        img1 = Image.open(input_path1)
        img2 = Image.open(input_path2)

        # Check if the images are the same size
        if img1.size != img2.size:
            print("Error: The input images must be the same size.")
            sys.exit(1)

        # Create a new image for the output
        output_img = Image.new("RGB", img1.size)

        # Process each pixel
        pixels1 = img1.load()
        pixels2 = img2.load()
        output_pixels = output_img.load()

        identical = True

        for y in range(img1.size[1]):
            for x in range(img1.size[0]):
                pixel1 = pixels1[x, y]
                pixel2 = pixels2[x, y]

                # If the pixels match, use a faint version of the inputs
                if pixel1 == pixel2:
                    faint_pixel = tuple(
                        int((value + 255 + 255) / 3) for value in pixel1[:3]
                    )
                    output_pixels[x, y] = faint_pixel
                else:
                    # If the pixels do not match, set the pixel to red
                    output_pixels[x, y] = (255, 0, 0)
                    identical = False

        # Save the output image
        output_img.save(output_path)
        return identical

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Compare two PNG images and generate an output PNG."
    )
    parser.add_argument("input1", type=Path, help="Path to the first input PNG")
    parser.add_argument("input2", type=Path, help="Path to the second input PNG")
    parser.add_argument(
        "--output", type=Path, required=True, help="Path to save the output PNG"
    )

    args = parser.parse_args()
    sys.exit(0 if process_images(args.input1, args.input2, args.output) else 1)
