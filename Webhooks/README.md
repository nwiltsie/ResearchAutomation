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

While running, the server (base URL <https://pro-oarfish-patient.ngrok-free.app>) makes three endpoints available, each of which will set the BlinkyTape's color:

| Method | Endpoint | Body |
| --- | --- | --- |
| `GET` | `/color/<colorname>` | -- |
| `POST` | `/` | JSON, e.g. `{"color": "red"}`. |
| `POST` | `/github` | GitHub `issue_comment` [payload](https://docs.github.com/en/webhooks/webhook-events-and-payloads#issue_comment). The comment text must consist only of a color name. |

```console
$ curl https://pro-oarfish-patient.ngrok-free.app/color/red
{"color":"red","rgb":{"blue":0,"green":0,"red":255}}

$ curl -X POST https://pro-oarfish-patient.ngrok-free.app -H "Content-Type: application/json" -d '{"color": "green"}'
{"color":"green","rgb":{"blue":0,"green":128,"red":0}}
```
