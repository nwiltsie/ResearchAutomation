# Automatically Drafting Emails

The scripts in this directory are examples of how to programmatically draft emails. They do so in two ways:

* As of January 2025, opening a link like [this](https://mail.google.com/mail/u/0/?to=recipient@example.com&cc=one@example.com,two@example.com&bcc=bcc@example.com&su=Email+Subject&body=Hello+There&tf=cm) will navigate to a new Gmail compose window with the To, CC, BCC, Subject, and Body pre-filled from the URL parameters ([source](https://til.simonwillison.net/google/gmail-compose-url)).
* On macOS, Outlook is registered as the default handler for `.emltpl` files, which have an identical format to [`.eml` files](https://www.loc.gov/preservation/digital/formats/fdd/fdd000388.shtml). Constructing and opening a temporary `.emltpl` file triggers Outlook to display the message as a draft.

## Compose a single email

```console
usage: single_email.py [-h] [--subject SUBJECT] --to TO [TO ...]
                       [--cc CC [CC ...]] [--bcc BCC [BCC ...]] [--body BODY]
                       (--outlook | --gmail)

options:
  -h, --help           show this help message and exit
  --subject SUBJECT    Subject line
  --to TO [TO ...]
  --cc CC [CC ...]
  --bcc BCC [BCC ...]
  --body BODY          Email body
  --outlook            Open email draft in Outlook (macOS only)
  --gmail              Open email draft in Gmail compose window
```

## Compose multiple emails from a CSV

```console
usage: batch_email.py [-h] (--outlook | --gmail) datafile

positional arguments:
  datafile    CSV with `firstname`, `lastname`, and `score` columns

options:
  -h, --help  show this help message and exit
  --outlook   Open email draft in Outlook (macOS only)
  --gmail     Open email draft in Gmail compose window
```
