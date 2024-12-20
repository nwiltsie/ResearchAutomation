#!/usr/bin/env python3
"""Extract a single racer's data and format it as JSON."""

import argparse
import json

from pathlib import Path


def clean_data(infile: Path, outfile: Path):
    """Interpolate any missing lap times for this racer."""
    with infile.open() as infileobj:
        racers = json.load(infileobj)

    # This is cheating - I know that the first and last lap times will always
    # be defined and that there are never two empty laps in a row
    for racer in racers.values():
        total_laps = len(racer["laps"])
        for index, laptime in enumerate(racer["laps"]):
            if index in (0, total_laps-1) or laptime is not None:
                continue

            prior_lap = racer["laps"][index-1]
            next_lap = racer["laps"][index+1]

            racer["laps"][index] = prior_lap + (next_lap-prior_lap) / 2

    with outfile.open(mode="w", encoding="utf-8") as outfileobj:
        json.dump(racers, outfileobj, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=Path)
    parser.add_argument("outfile", type=Path)
    args = parser.parse_args()

    clean_data(args.infile, args.outfile)
