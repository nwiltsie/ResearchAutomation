#!/usr/bin/env python3
"""DoIt dodo file."""

import subprocess
from functools import lru_cache
from pathlib import Path

import doit
from doit.action import CmdAction
from doit.tools import result_dep

SCRIPT_DIR = (Path(__file__).parent.parent / "scripts").resolve()
CSV_FILE = (Path(__file__).parent.parent / "data/2021-02-18-data.csv").resolve()

TEMP_DIR = (Path(__file__).parent / "temp").resolve()
OUTPUT_DIR = (Path(__file__).parent / "output").resolve()


DOIT_CONFIG = {
    "verbosity": 2,
    "default_tasks": ["plot*"],
}


@lru_cache(maxsize=1)
def get_racer_names() -> list[str]:
    """Return a list of all of the racer names."""
    parse_script = SCRIPT_DIR / "print_racer_names.py"
    return (
        subprocess.check_output([parse_script, CSV_FILE]).decode("utf-8").splitlines()
    )


def datahash(infile: Path):
    """Return a dictionary with the hash of the input file's contents."""
    # This is a bit of a cheat to help the "merged_racers" task - doit
    # struggles with dependencies for 'getargs'. Add in this task with a
    # result that depends on the _contents_ of the clean file.
    return {"hash": hash(infile.read_bytes())}


def task_mkdir():
    """Create a directory"""
    for path in (TEMP_DIR, OUTPUT_DIR):
        yield {
            "name": path.name,
            "targets": [path],
            "actions": [(path.mkdir, [], {"exist_ok": True})],
            "uptodate": [path.exists],
            "clean": True,
        }


def task_single_racers():
    """Extract and clean data for a single racer."""
    # Yield this to override the docstring for the extract tasks
    yield {
        "basename": "extract",
        "name": None,
        "doc": "Extract and clean data for a single racer",
    }

    # Yield these to override the docstrings for the plot tasks
    yield {
        "basename": "plot-lap",
        "name": None,
        "doc": "Plot single-racer lap times",
    }
    yield {
        "basename": "plot-split",
        "name": None,
        "doc": "Plot single-racer split times",
    }

    extract_script = SCRIPT_DIR / "extract_racer_data.py"
    clean_script = SCRIPT_DIR / "clean_racer_data.py"

    def extract(racer_name: str, outfile: Path):
        subprocess.check_output([
            extract_script,
            CSV_FILE,
            "--name",
            racer_name,
            outfile,
        ])
        return {"raw_data": str(outfile)}

    def qc(infile: Path, outfile: Path):
        subprocess.check_output([clean_script, infile, outfile])
        return {"clean_data": str(outfile)}

    for racer_name in get_racer_names():
        racer_data = TEMP_DIR / f"raw-{racer_name}.json"
        clean_racer_data = TEMP_DIR / f"clean-{racer_name}.json"

        yield {
            "basename": "extract",
            "name": racer_name,
            "task_dep": ["mkdir:temp"],
            "file_dep": [extract_script, clean_script, CSV_FILE],
            "targets": [racer_data, clean_racer_data],
            "actions": [
                (extract, (racer_name, racer_data)),
                (qc, (racer_data, clean_racer_data)),
            ],
            "clean": True,
        }

        yield {
            "basename": "_hashcheck",
            "name": racer_name,
            "file_dep": [clean_racer_data],
            "actions": [
                (datahash, (clean_racer_data,)),
            ],
        }

        yield from make_plots(clean_racer_data, racer_name)


def task_merged_racers():
    """Yield tasks to handle the re-merged racers."""
    merge_script = SCRIPT_DIR / "merge_racer_data.py"
    combined_data = TEMP_DIR / "merged.json"

    def merge_data(racer_values):
        subprocess.check_output([merge_script, combined_data, *racer_values.values()])

    yield {
        "basename": "merge",
        "actions": [merge_data],
        "targets": [combined_data],
        "task_dep": ["mkdir:temp"],
        "getargs": {"racer_values": ("extract", "clean_data")},
        "uptodate": [result_dep("_hashcheck")],
        "clean": True,
        "doc": "Re-merge the cleaned data",
    }

    # Need to adjust tweak the name
    for task in make_plots(combined_data, "remerged"):
        task["basename"] += "-merged"
        task.pop("name")
        yield task


def make_plots(datafile: Path, name: str):
    """Yield tasks to make the plots."""
    plot_script = SCRIPT_DIR / "plot_data.py"
    lap_plot = OUTPUT_DIR / f"lap-{name}.png"
    split_plot = OUTPUT_DIR / f"split-{name}.png"

    yield {
        "basename": "plot-lap",
        "name": name,
        "actions": [
            CmdAction([plot_script, datafile, lap_plot, "--type", "lap"], shell=False),
        ],
        "file_dep": [plot_script, datafile],
        "task_dep": ["mkdir:output"],
        "targets": [lap_plot],
        "clean": True,
        "doc": "Plot total lap time",
    }

    yield {
        "basename": "plot-split",
        "name": name,
        "actions": [
            CmdAction(
                [plot_script, datafile, split_plot, "--type", "split"], shell=False
            ),
        ],
        "file_dep": [plot_script, datafile],
        "task_dep": ["mkdir:output"],
        "targets": [split_plot],
        "clean": True,
        "doc": "Plot split lap time",
    }


if __name__ == "__main__":
    doit.run(globals())
