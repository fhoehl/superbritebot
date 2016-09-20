#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Get your tickets!"""

import argparse
import re
import json
from collections import defaultdict
from datetime import datetime

from lxml import html
import requests


ORDER_START_URL = "https://www.eventbrite.co.uk/orderstart"


def get_ticket(event_page_url, user_info):
    """Return register url."""

    session = requests.Session()

    event_page = session.get(event_page_url)

    # Looking for embedded json data
    res = re.search(r"collection[\s:]+(\[{.*\])", event_page.text)
    collection = json.loads(res.group(1))

    # Choose one of the available tickets
    ticket = defaultdict(str)

    for item in collection:
        item_start = item["start_sales_with_tz"]
        item_start_time = datetime.strptime(item_start["utc"], "%Y-%m-%dT%H:%M:%SZ")
        delta_time = datetime.now() - item_start_time

        if delta_time.total_seconds() >= 0:
            ticket = item

    # Finding interesting form inputs
    tree = html.fromstring(event_page.content)
    eid = tree.xpath('//input[@name="eid"]/@value')
    source_id = tree.xpath('//input[@name="source_id"]/@value')

    # Pre requesting a ticket
    payload = dict(eid=eid,
                   has_javascript=1,
                   source_id=source_id,
                   payment_type="free",
                   legacy_event_page=1,)

    quant = ticket.get("ticket_form_element_name", "")
    payload[quant] = 1

    prerequest_response = session.post(ORDER_START_URL, params=payload)

    # Requesting a ticket
    register_payload = dict(submitted=1,
                            payment_type="free",
                            first_name=user_info["first_name"],
                            last_name=user_info["last_name"],
                            email_address=user_info["email"],
                            confirm_email_address=user_info["email"],)

    ticket_response = session.post(prerequest_response.url, params=register_payload)

    if ticket_response.status_code == 200:
        print("I think you got a ticket! 😎")
    else:
        print("Something went wrong 🤔")


def main():
    """Main"""

    parser = argparse.ArgumentParser(description="Get your tickets!")
    parser.add_argument("event_page_url", help="Event page url")
    parser.add_argument("first_name", help="Your first name")
    parser.add_argument("last_name", help="Your last name")
    parser.add_argument("email", help="Your email")
    args = parser.parse_args()

    user_info = defaultdict(str)
    user_info["first_name"] = args.first_name
    user_info["last_name"] = args.last_name
    user_info["email"] = args.email

    get_ticket(args.event_page_url, user_info)


if __name__ == "__main__":
    main()
