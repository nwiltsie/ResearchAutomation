# Experiments with Blinkytape

## Local Usage

```console
usage: blinky.py [-h] [--blinkyport port] (--color name | --cylon)

options:
  -h, --help         show this help message and exit
  --blinkyport port  Path to the blinkytape serial port (e.g. /dev/tty.usbmodemXXXX)
  --color name       Color name to display
  --cylon            Display a cylon pattern
```

## Server

```console
usage: blinky_server.py [-h] [--address ADDRESS] [--port PORT] [--workers WORKERS] [--blinkyport port] [--ngrok]

options:
  -h, --help         show this help message and exit
  --address ADDRESS  Local server bind address (default 0.0.0.0)
  --port PORT        Local server port (default 8000)
  --workers WORKERS  Gunicorn worker threads (default 4)
  --blinkyport port  Path to the blinkytape serial port (e.g. /dev/tty.usbmodemXXXX)
  --ngrok            Bind a public URL with ngrok
```
