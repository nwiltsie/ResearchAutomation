#!/usr/bin/env python3
"""Extract a single racer's data and format it as JSON."""

import argparse
import csv
import json

from pathlib import Path


def extract_data(datafile: Path, outfile: Path, name: str):
    """Print the racer identifiers."""
    with datafile.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for racer in reader:
            if racer["name"] == name:
                break
        else:
            raise ValueError(f"Racer {name} not found!")

    racer["age"] = int(racer["age"])
    racer["laps"] = []
    for lap in range(1, 31):
        lap_time = racer.pop(f"lap_{lap}")
        try:
            racer["laps"].append(float(lap_time))
        except ValueError:
            racer["laps"].append(None)

    racers = {racer["name"]: racer}

    with outfile.open(mode="w", encoding="utf-8") as outfileobj:
        json.dump(racers, outfileobj, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", type=Path)
    parser.add_argument("outfile", type=Path)
    parser.add_argument("--name", required=True, type=str)
    args = parser.parse_args()

    extract_data(args.datafile, args.outfile, args.name)
