#!/usr/bin/env python3
"""Open a draft email for review in Outlook or Gmail."""

import subprocess
import sys
import tempfile
import textwrap
import time
import urllib.parse
import webbrowser

from email.message import EmailMessage
from pathlib import Path


def open_outlook(msg: EmailMessage):
    """
    Open an Outlook compose window with the email.

    Only works on macOS.
    """
    if sys.platform != "darwin":
        raise RuntimeError("--outlook is only available on macOS")

    with tempfile.TemporaryDirectory() as tempdir:
        template_file = Path(tempdir, "email.emltpl")

        # This is some hackery - Outlook by default strips newlines from
        # plaintext messages. Work around that by adding three spaces to the
        # front of every line.
        if "text/plain;" in msg.get("content-type", ""):
            msg.set_content(textwrap.indent(msg.get_content(), "  ", lambda line: True))

        template_file.write_text(str(msg), encoding="utf-8")
        print(template_file.read_text(encoding="utf-8"))

        subprocess.run(["/usr/bin/open", template_file], check=True)

        # There's a race condition here - we don't want to remove the directory
        # until Outlook has opened the file. This isn't particularly robust.
        time.sleep(1)


def open_gmail_url(msg: EmailMessage):
    """Open a Gmail compose page pre-filled with the email."""
    base_url = "https://mail.google.com/mail/"
    params = {"view": "cm", "fs": "1"}

    header_map = {"to": "to", "cc": "cc", "bcc": "bcc", "subject": "su"}

    for header, param in header_map.items():
        if value := msg.get(header):
            params[param] = value

    try:
        if value := msg.get_content():
            params["body"] = value
    except AttributeError:
        pass

    webbrowser.open(f"{base_url}?{urllib.parse.urlencode(params)}")
