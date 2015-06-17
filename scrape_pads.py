#! /usr/bin/env python

import requests

from create_site import get_dates


def main():
    for date, meeting_number in get_dates():
        url = "https://pads.ccc.de/ep/pad/export/pystada-{:%Y-%m-%d}/latest?format=txt".format(date)

        response = requests.get(url, verify=False)

        if response.status_code != 200:
            print("Everything failed (code: {}) for {}".format(response.status_code, url))
            continue

        with open("archive/pystada-{}-{:%Y-%m-%d}.txt".format(meeting_number, date), "w") as out:
            out.write(response.text)


if __name__ == '__main__':
    main()
