# Generating Word and PowerPoint Documents

## Setup

In this directory, create a virtual environment and install the required packages:

```console
$ python3 -m venv officevenv
$ . officevenv/bin/activate
(officevenv) $ pip install -r requirements.txt
```

## Generate Slides

```console
# Basic usage
$ ./make_powerpoint.py data.csv --template template.pptx --outname slides
Saved presentation as slides.pptx
```

## Generate Document

```console
$ ./make_document.py data.csv --outname mydoc
Saved document as mydoc.docx
