#!/usr/bin/env python3
"""Generate a line plot image from an input JSON file."""

import argparse
import json
import itertools
import urllib.parse
import urllib.request

from pathlib import Path


def get_lap_params(racers: dict) -> dict:
    """Return the appropriate parameters for a line plot."""

    racer_names = []
    racer_laps = []

    for racer_name, racer in racers.items():
        racer_names.append(racer_name)
        racer_laps.append(",".join(str(laptime) for laptime in [0, *racer["laps"]]))

    return {
        "chdl": "|".join(racer_names),
        "cht": "lc",  # Line plot with Y values
        "chd": "a:" + "|".join(racer_laps),
        "chtt": "Total Time by Lap",  # Title of the chart
        "chm": "d,000000,0,-1,5.0", # Marker
    }

def get_split_params(racers: dict) -> dict:
    """Return the appropriate parameters for a bar plot."""
    racer_names = []
    racer_splits = []

    for racer_name, racer in racers.items():
        racer_names.append(racer_name)

        split_times = []
        for prior_lap, next_lap in itertools.pairwise(itertools.chain([0], racer["laps"])):
            split_times.append(f"{next_lap-prior_lap:0.2f}")

        racer_splits.append(",".join(split_times))

    return {
        "chdl": "|".join(racer_names),
        "cht": "bvg",
        "chd": "a:" + "|".join(racer_splits),
        "chtt": "Lap Split Times", 
    }


def generate_line_plot(datafile: Path, outputfile: Path, width: int, height: int, plot_type: str):
    """Generates a PNG line plot using the Image Charts API and saves it to a file."""
    # Extract x and y data
    with datafile.open(mode="rb") as infile:
        data = json.load(infile)

    # Construct the Image Charts API URL
    base_url = "https://image-charts.com/chart"
    params = {
        "chs": f"{width}x{height}",  # Chart size (width x height)
        "chxt": "x,y",  # Show axis
        "chg": "1,1",   # Grid lines
    }

    if plot_type == "lap":
        params.update(get_lap_params(data))
    elif plot_type == "split":
        params.update(get_split_params(data))
    else:
        raise ValueError(f"Unknown plot type '{plot_type}'!")

    # Encode the parameters into the URL
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    # Make the HTTP request to fetch the PNG image
    with urllib.request.urlopen(url) as response:
        outputfile.write_bytes(response.read())

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", type=Path)
    parser.add_argument("outputfile", type=Path)
    parser.add_argument("--width", type=int, default=800)
    parser.add_argument("--height", type=int, default=800)

    parser.add_argument(
        "--type",
        required=True,
        choices=("lap", "split"),
    )

    args = parser.parse_args()

    # Generate the plot
    generate_line_plot(
        args.datafile,
        args.outputfile,
        args.width,
        args.height,
        args.type,
    )
