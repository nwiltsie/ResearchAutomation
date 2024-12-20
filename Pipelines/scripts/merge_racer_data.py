#!/usr/bin/env python3
"""Extract a single racer's data and format it as JSON."""

import argparse
import json

from pathlib import Path


def merge_data(datafiles: list[Path], outfile: Path):
    """Print the racer identifiers."""
    racers = {}

    for datafile in datafiles:
        with datafile.open() as infile:
            racers.update(json.load(infile))


    with outfile.open(mode="w", encoding="utf-8") as outfileobj:
        json.dump(racers, outfileobj, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("outfile", type=Path)
    parser.add_argument("datafiles", type=Path, nargs="+")
    args = parser.parse_args()
    merge_data(args.datafiles, args.outfile)
