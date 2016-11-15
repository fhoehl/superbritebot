# Helps you get your :ticket: on Eventbrite

superbritebot is a very simple bot that lets you automate your ticket
registration on Eventbrite.

It’s a baby bot :baby: so it has lots of limitations for now. New features might
come later :baby_bottle:

Limitations are:

* only works with free ticket events
* only works with events with simple forms (email, last name and first name)

```bash
usage: superbritebot.py [-h] event_page_url first_name last_name email time

Get your tickets!

positional arguments:
  event_page_url  Event page url
  first_name      Your first name
  last_name       Your last name
  email           Your email
  time            When does the script should submit an order. Accepts 24-hour
                  notation (16:00)

optional arguments:
  -h, --help      show this help message and exit
```

## How to use it?

```bash
cd superbritebot
pip3 install -r requirements.txt
python3 superbritebot.py $EVENT_URL $FIRST_NAME $LASTNAME $EMAIL 16:00
```
