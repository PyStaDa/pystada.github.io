#! /usr/bin/env python

import requests

from create_site import get_dates

empty_pad_template = """Willkommen im Etherpad!

Dieses Pad synchronisiert beim Tippen, daher werden alle Personen die gerade dieses Pad
anschauen das selbe sehen. Dies erlaubt gemeinsam, gleichzeitig an einem Text zu arbeiten.

"""

def main():
    with requests.Session() as session:
        session.verify = 'cacert-root.crt'

        for date, meeting_number in get_dates():
            url = "https://pads.darmstadt.ccc.de/p/pystada-{:%Y-%m-%d}/export/txt".format(date)

            response = session.get(url)

            if response.status_code != 200:
                print("Everything failed (code: {}) for {}".format(response.status_code, url))
                continue

            if response.text == empty_pad_template:
                print("Pad in {} is unused".format(url))
                continue

            with open("archive/pystada-{}-{:%Y-%m-%d}.txt".format(meeting_number, date), "w") as out:
                out.write(response.text)


if __name__ == '__main__':
    main()
