#!/usr/bin/env python3
"""Given a datafile, print each racer identifier on a separate line."""

import argparse
import csv

from pathlib import Path


def print_identifiers(datafile: Path):
    """Print the racer identifiers."""
    with datafile.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row["name"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", type=Path)
    args = parser.parse_args()

    print_identifiers(args.datafile)
