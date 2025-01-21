#!/usr/bin/env python3
"""Create a scatter plot."""

import argparse
import time

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def make_plot(output_filename: Path):
    """Make a scatter plot and save it as the given filename."""
    # Generate data
    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    noise = np.random.normal(0, 1, size=100)
    y = 2 * x + noise

    # Intentional subtle error: modify x values slightly
    np.random.seed(int(time.time()))
    # x[10:-10] += np.random.normal(0, 0.1, size=80)  # Error: Adds small noise to x
    # Pick a random point and adjust it vertically
    y[np.random.randint(low=10, high=90)] += np.random.normal(0, 0.1)

    # Create scatter plot
    plt.figure(figsize=(8, 6), dpi=300)
    plt.scatter(x, y, label="Data Points", color="blue", alpha=0.7)
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.legend()
    plt.grid(True)

    # Save and display the plot
    plt.tight_layout()
    plt.savefig(output_filename, bbox_inches="tight")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a consistent, unchanging scatter plot."
    )
    parser.add_argument("outfile", type=Path, help="Output filename for the plot")

    args = parser.parse_args()
    make_plot(args.outfile)
