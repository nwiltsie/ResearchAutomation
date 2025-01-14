#!/usr/bin/env python3
"""Batch-prepare emails with student scores."""

import argparse
import csv
import textwrap
from operator import itemgetter
from statistics import mean
from typing import Iterator

from email.message import EmailMessage
from email.headerregistry import Address
from pathlib import Path

from emaillib import open_gmail_url, open_outlook


def prepare_emails(datafile: Path) -> Iterator[EmailMessage]:
    """Prepare the batch of emails."""
    # I generated this CSV with Excel, which inserted a byte-order mark (BOM)
    # into the file. If we didn't use the utf-8-sig encoding the fieldnames
    # would be read as '\ufefffirstname' instead of 'firstname'.
    data = []

    with datafile.open(encoding="utf-8-sig", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["score"] = float(row["score"])
            data.append(row)

    average_score = mean(datum["score"] for datum in data)

    data.sort(key=itemgetter("score"), reverse=True)

    for rank, datum in enumerate(data, start=1):
        message = EmailMessage()
        message["Subject"] = "Test Scores"

        firstname = datum["firstname"]
        lastname = datum["lastname"]
        score = datum["score"]

        # Set an plain text body as the default.
        message.set_content(
            textwrap.dedent(f"""\
            Dear {firstname} {lastname},

            On the most recent test you scored {score}. The average was {average_score}.

            That puts you at rank {rank}/{len(data)} in the class.

            Sincerely,
            Professor
            """),
            subtype="plain",
        )

        # Also add an HTML body type for Outlook (it _really_ wants to strip
        # newlines from plain text emails)
        message.add_alternative(
            textwrap.dedent(f"""\
            <!DOCTYPE html>
            <html>
            <body>
            <p>Dear {firstname} {lastname},</p>

            <p>On the most recent test you scored <b>{score}</b>. The average was <b>{average_score}</b>.</p>

            <p>That puts you at rank <b>{rank}/{len(data)}</b> in the class.</p>

            <p>Sincerely,<br>
            Professor</p>
            </body>
            </html>
            """),
            subtype="html",
        )

        message["To"] = Address(addr_spec=f"{firstname}.{lastname}@example.com")
        print(message)

        yield message


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "datafile",
        type=Path,
        help="CSV with `firstname`, `lastname`, and `score` columns",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--outlook",
        action="store_true",
        help="Open email draft in Outlook (macOS only)",
    )
    group.add_argument(
        "--gmail", action="store_true", help="Open email draft in Gmail compose window"
    )

    args = parser.parse_args()

    for msg in prepare_emails(args.datafile):
        if args.gmail:
            open_gmail_url(msg)
        elif args.outlook:
            open_outlook(msg)
