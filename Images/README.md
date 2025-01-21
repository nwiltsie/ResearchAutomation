# Image Comparisons

## Setup

In this directory, create a virtual environment and install the required packages:

```console
$ python3 -m venv imagevenv
$ . imagevenv/bin/activate
(imagevenv) $ pip install -r requirements.txt
```

## Generate Plots

Run the `./make_plot.py` script multiple times to generate multiple plots. Do they appear consistent?

```console
usage: make_plot.py [-h] outfile

Generate a consistent, unchanging scatter plot.

positional arguments:
  outfile     Output filename for the plot

options:
  -h, --help  show this help message and exit
```

## Difference Spotting (Human)

Pass two or more plots to the `./animate.py` script, then open the resulting `.gif` file in a web browser. Do you see any differences?

```console
usage: animate.py [-h] --output OUTPUT [--duration ms] [--repeat count] input [input ...]

Create an animated gif from multiple images.

positional arguments:
  input            Input image(s)

options:
  -h, --help       show this help message and exit
  --output OUTPUT  Output filename
  --duration ms    Delay (in ms) between frames
  --repeat count   Animation repeat count (0 for unlimited)
```

## Difference Spotting (Computer)

Pass two plots to the `./compare.py` script and examine the comparison image. Check the exit code of the script with `echo $?`.

```console
usage: compare.py [-h] --output OUTPUT input1 input2

Compare two PNG images and generate an output PNG.

positional arguments:
  input1           Path to the first input PNG
  input2           Path to the second input PNG

options:
  -h, --help       show this help message and exit
  --output OUTPUT  Path to save the output PNG
```
