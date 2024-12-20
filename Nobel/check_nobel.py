#!/usr/bin/env python3
"""Check if someone has won a Nobel Prize."""

import argparse
import datetime
import json
import sys
import urllib.parse
from urllib.request import Request, urlopen


def print_prize(prize: dict):
    """Print information about a Nobel Prize."""
    print(prize["categoryFullName"]["en"])
    print(prize["dateAwarded"])

    for winner in sorted(prize["laureates"], key=lambda x: int(x["sortOrder"])):
        print(f"    {winner['knownName']['en']} {winner['motivation']['en']}")


def check_nobel_prize_winners(surname: str, years_back: int):
    """Check if the surname appears as a Nobel Prize winner."""
    this_year = datetime.date.today().year

    query_params = {
        "sort": "desc",
        "nobelPrizeYear": this_year,
        "yearTo": this_year - max(years_back, 0),
    }

    full_url = urllib.parse.urlunparse((
        "http",
        "api.nobelprize.org",
        "/2.0/nobelPrizes",
        "",
        urllib.parse.urlencode(query_params),
        "",
    ))

    headers = {"User-Agent": "Crawler"}

    with urlopen(Request(full_url, headers=headers)) as response:
        if response.status == 200:
            data = json.load(response)
        else:
            raise RuntimeError(
                f"Failed to fetch data. HTTP status code: {response.status}"
            )

    won_any = False

    search_name = surname.casefold()

    for prize in data["nobelPrizes"]:
        for winner in prize["laureates"]:
            # Add all of their names
            for key in ["fullName", "knownName"]:
                if key in winner and search_name in winner[key].get("en").casefold():
                    won_any = True
                    print_prize(prize)
                    break

    if not won_any:
        print(f"{surname.title()} hasn't won a Nobel Prize :(")

    return won_any


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check if someone has one a Nobel Prize."
    )
    parser.add_argument("surname", type=str, help="surname to check against database")
    parser.add_argument(
        "--years", type=int, default=3, help="number of recent award rounds to check"
    )

    args = parser.parse_args()

    sys.exit(0 if check_nobel_prize_winners(args.surname, args.years) else 1)
