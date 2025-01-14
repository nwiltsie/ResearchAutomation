#!/usr/bin/env python3
"""Open a draft email for review in Outlook or Gmail."""

import argparse

from email.message import EmailMessage
from email.headerregistry import Address

from emaillib import open_gmail_url, open_outlook


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", help="Subject line")
    parser.add_argument("--to", nargs="+", required=True)
    parser.add_argument("--cc", nargs="+")
    parser.add_argument("--bcc", nargs="+")
    parser.add_argument("--body", help="Email body")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--outlook", action="store_true", help="Open email draft in Outlook"
    )
    group.add_argument(
        "--gmail", action="store_true", help="Open email draft in Gmail compose window"
    )

    args = parser.parse_args()
    message = EmailMessage()

    if args.subject:
        message["Subject"] = args.subject

    if args.body:
        message.set_content(args.body)

    if args.to:
        message["To"] = [Address(addr_spec=item) for item in args.to]

    if args.cc:
        message["CC"] = [Address(addr_spec=item) for item in args.cc]

    if args.bcc:
        message["BCC"] = [Address(addr_spec=item) for item in args.bcc]

    if args.gmail:
        open_gmail_url(message)
    elif args.outlook:
        open_outlook(message)
