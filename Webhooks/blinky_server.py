#!/usr/bin/env python3
"""Webserver to display a POSTed color on the blinkytape."""

import argparse
import os
import subprocess
import time
from contextlib import contextmanager, ExitStack
from pathlib import Path

import requests

from gunicorn.app.base import BaseApplication
from flask import Flask, request, jsonify, current_app

from blinky import send_color, send_cylon, guess_blinkyport, named_color


@contextmanager
def scoped_ngrok_url(server_port: int):
    """Run ngrok in the background as a context manager."""
    pid = os.getpid()
    process = None

    try:
        process = subprocess.Popen(
            [
                "ngrok",
                "http",
                str(server_port),
                "--url",
                "pro-oarfish-patient.ngrok-free.app",
                "--name",
                "blinky",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        public_url = ""

        # Get the public URL (waiting up to 5 seconds)
        for _ in range(5):
            try:
                tunnels = {
                    item["name"]: item["public_url"]
                    for item in requests.get(
                        "http://localhost:4040/api/tunnels"
                    ).json()["tunnels"]
                }
                if public_url := tunnels.get("blinky"):
                    break

            except requests.exceptions.ConnectionError:
                time.sleep(1)

        if not public_url:
            raise RuntimeError("Could not get public URL from ngrok!")

        yield public_url

    finally:
        # Only tear down the process from the original process
        if process and pid == os.getpid():
            print(f"Terminating ngrok process with PID: {process.pid}")
            process.terminate()
            process.wait()
            print("ngrok terminated.")


@contextmanager
def cleared_blinkytape(blinky_port: Path):
    """Reset the blinkytape on enter and exit."""
    black = named_color("black")

    try:
        # Initialize the tape with a cylon display
        send_cylon(blinky_port)

        yield
    finally:
        send_color(blinky_port, black)


def create_app(blinky_port: Path):
    """Create the flask application."""
    app = Flask(__name__)

    # Store the serial port address in the Flask app config
    app.config["BLINKY_PORT"] = blinky_port

    @app.route("/", methods=["POST"])
    def color():
        try:
            # Parse the JSON body
            data = request.get_json()
            if not data or "color" not in data:
                raise ValueError("Missing 'color' field in request body.")

            color_name = data["color"].strip()
            if not color_name:
                raise ValueError("The 'color' field must not be empty.")

            # Convert the color name to RGB
            rgb_triplet = named_color(color_name)

            response = {
                "color": color_name,
                "rgb": {
                    "red": rgb_triplet.red,
                    "green": rgb_triplet.green,
                    "blue": rgb_triplet.blue,
                },
            }

            # Access the `port` value from the app config
            if port := current_app.config.get("BLINKY_PORT", None):
                send_color(port, rgb_triplet)

            return jsonify(response), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception:
            return jsonify({"error": "An unexpected error occurred."}), 500

    @app.route("/github", methods=["POST"])
    def github():
        try:
            # Parse the JSON body
            data = request.get_json()

            if not data:
                raise ValueError("No body")

            if data["action"] == "ping":
                # GitHub sends PING events to verify that a webhook is working.
                return jsonify({"result": True}, 200)

            # Extract the complete body of the issue comment
            color_name = data["comment"]["body"].strip()
            if not color_name:
                raise ValueError("The 'color' field must not be empty.")

            # Convert the color name to RGB
            rgb_triplet = named_color(color_name)

            response = {
                "color": color_name,
                "rgb": {
                    "red": rgb_triplet.red,
                    "green": rgb_triplet.green,
                    "blue": rgb_triplet.blue,
                },
            }

            if port := current_app.config.get("BLINKY_PORT", None):
                send_color(port, rgb_triplet)

            return jsonify(response), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception:
            return jsonify({"error": "An unexpected error occurred."}), 500

    @app.route("/color/<colorname>", methods=["GET"])
    def get_color(colorname):
        """Handle GET requests for a color name."""
        try:
            if not colorname:
                raise ValueError("Color name must not be empty.")

            # Strip and convert the color name to RGB
            color_name = colorname.strip()
            rgb_triplet = named_color(color_name)

            response = {
                "color": color_name,
                "rgb": {
                    "red": rgb_triplet.red,
                    "green": rgb_triplet.green,
                    "blue": rgb_triplet.blue,
                },
            }

            # Access the `port` value from the app config
            if port := current_app.config.get("BLINKY_PORT", None):
                send_color(port, rgb_triplet)

            return jsonify(response), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception:
            return jsonify({"error": "An unexpected error occurred."}), 500

    return app


class BlinkyApp(BaseApplication):
    """
    A simple Gunicorn app to allow running from within python.

    This is only appropriate for development - gunicorn generally be managed externally.
    """

    def __init__(self, app, user_config):
        self.app = app
        self.user_config = user_config
        super().__init__()

    def load_config(self):
        """Load the Gunicorn configuration from the input options."""
        for key, value in self.user_config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """Load the application for the server."""
        return self.app


# Main function to launch Gunicorn
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--address",
        default="0.0.0.0",
        help="Local server bind address (default 0.0.0.0)",
    )
    parser.add_argument("--port", default=8000, help="Local server port (default 8000)")
    parser.add_argument(
        "--workers", default=4, help="Gunicorn worker threads (default 4)"
    )

    parser.add_argument(
        "--blinkyport",
        metavar="port",
        type=Path,
        help="Path to the blinkytape serial port (e.g. /dev/tty.usbmodemXXXX)",
    )
    parser.add_argument(
        "--ngrok", action="store_true", help="Bind a public URL with ngrok"
    )

    args = parser.parse_args()

    if not args.blinkyport:
        args.blinkyport = guess_blinkyport()

    with ExitStack() as stack:
        stack.enter_context(cleared_blinkytape(args.blinkyport))

        if args.ngrok:
            ngrok_url = stack.enter_context(scoped_ngrok_url(args.port))
            print(f"Public server available at {ngrok_url}")

        BlinkyApp(
            app=create_app(blinky_port=args.blinkyport),
            user_config={
                "bind": f"{args.address}:{args.port}",
                "workers": args.workers,
            },
        ).run()
