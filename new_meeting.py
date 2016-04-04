#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import locale
from itertools import chain

try:
    import requests
except ImportError:
    requests = None

SHOWN_DATES = 3
REAL_FIRST_DATE = datetime.datetime(2014, 1, 29, 19)
FIRST_DATE = datetime.datetime(2016, 2, 10, 19)
DELTA = datetime.timedelta(weeks=4)
DATES_TO_SKIP = (datetime.datetime(2014, 12, 31, 19),
                 datetime.datetime(2015, 12, 30, 19),)

WANTED_LOCALE = 'de_DE.UTF-8'

EMPTY_PAD_TEMPLATE = """Willkommen im Etherpad!

Dieses Pad synchronisiert beim Tippen, daher werden alle Personen die gerade dieses Pad
anschauen das selbe sehen. Dies erlaubt gemeinsam, gleichzeitig an einem Text zu arbeiten.

"""

try:
    locale.setlocale(locale.LC_ALL, WANTED_LOCALE)
except locale.Error:
    print("Einstellen der deutschen Sprachsettings gescheitert."
          "Bitte sicherstellen, dass die locale '{0}' vorhanden ist."
          .format(WANTED_LOCALE))


RECOMMENDED_MAILING_LISTS = [
    ("Chaos Darmstadt", "darmstadt@lists.metarheinmain.de", "https://lists.metarheinmain.de/mailman/listinfo/darmstadt"),
    ("Python-DE", "python-de@python.org", "http://mail.python.org/mailman/listinfo/python-de"),
]

def update_site():
    def format_date(date, hide_agenda_link=False):
        if hide_agenda_link:
            line_template = '<li><span style="color: #999999;">Mittwoch, {date.day}. {month} {date.year} um {date.hour}:{date.minute:02} Uhr</span></li>'
        else:
            line_template = '<li id="current"><span>Mittwoch, {date.day}. {month} {date.year} um {date.hour}:{date.minute:02} Uhr (<a href="https://pads.darmstadt.ccc.de/p/pystada-{date.year}-{date.month:02}-{date.day:02}">Agenda</a>)</span></li>'

        return line_template.format(date=date, month=date.strftime('%B'))

    starting_date, issue = get_next_date()

    elements = []
    i = 0
    while len(elements) < SHOWN_DATES:
        new_date = starting_date + (i * DELTA)
        if new_date not in DATES_TO_SKIP:
            elements.append(new_date)
        i += 1

    list_template = '''\
<ul>
{elements}
</ul>\
'''.format(elements='\n'.join([format_date(date, hide_agenda_link=i)
                               for i, date in enumerate(elements)]))

    with open('index.html.template') as template_file:
        site_template = ''.join(template_file.readlines())

    with open('index.html', 'w') as outputfile:
        outputfile.write(site_template.format(dates=list_template))


def get_next_date():
    today = datetime.datetime.now()

    for date, meeting_number in get_dates():
        if date < today:
            continue

        return (date, meeting_number)


def get_dates():
    for date, issue in chain(get_first_dates(), get_new_dates()):
        yield date, issue


def get_first_dates():
    """
    Get the dates of the meeting still with the two-week cycle.
    """
    issue = 1
    starting_date = REAL_FIRST_DATE
    last_meeting_date = datetime.datetime(2016, 1, 14, 19, 0)
    two_weeks = datetime.timedelta(weeks=2)

    while starting_date <= last_meeting_date:
        if starting_date not in DATES_TO_SKIP:
            yield (starting_date, issue)
            issue += 1

        starting_date += two_weeks


def get_new_dates():
    "The dates sinces Christian and Sven took over running PyStaDa."
    today = datetime.datetime.now()
    issue = 51
    starting_date = FIRST_DATE
    latest_date = today + DELTA

    while starting_date <= latest_date:
        if starting_date not in DATES_TO_SKIP:
            yield (starting_date, issue)
            issue += 1

        starting_date += DELTA


def create_mail():
    starting_date, issue = get_next_date()
    print("Ankündigungen sollten wenn möglich nicht nur auf der PyStaDa-ML, sondern auch auf anderen relavanten MLs erscheinen, da wir ja auch potenzielle neue Mitglieder ansprechen wollen.")
    print("Auf folgenden Mailinglisten sind die Ankündigungen gut aufgehoben:")
    for (name, mail_address, website) in RECOMMENDED_MAILING_LISTS:
        print("{name}: {address} ({website})".format(name=name, address=mail_address, website=website))

    print("\n\nMail-Inhalt folgt...")
    print("-" * 10)

    with open('mail.template') as template_file:
        mail_template = ''.join(template_file.readlines())

    print(mail_template.format(date=starting_date, month=starting_date.strftime('%B')))


def show_pad_template():
    date, issue = get_next_date()

    print('\n' * 2)
    print('''PyStaDa Treffen #{issue} am {date.day}.{date.month}.{date.year}
=================================

Visit: http://pystada.github.io or join #PyStaDa on Hackint or follow @PyStaDa on Twitter

Agenda
------

* Füll mich!
'''.format(issue=issue, date=date, month=date.strftime('%B')))
    print('\n' * 2)


def archive_pads():
    if requests is None:
        print("Bitte 'requests' installieren um die Pads zu archivieren.")
        return

    with requests.Session() as session:

        for date, issue in get_dates():
            url = "https://pads.darmstadt.ccc.de/p/pystada-{:%Y-%m-%d}/export/txt".format(date)

            response = session.get(url)

            if response.status_code != 200:
                print("Everything failed (code: {}) for {}".format(response.status_code, url))
                continue

            if response.text == EMPTY_PAD_TEMPLATE:
                print("Pad in {} is unused".format(url))
                continue

            with open("archive/pystada-{}-{:%Y-%m-%d}.txt".format(issue, date), "w") as out:
                out.write(response.text)


if __name__ == '__main__':
    starting_date, issue = get_next_date()
    print("Nächster PyStaDa: #{1} am {0}".format(starting_date, issue))

    update_site()
    archive_pads()
    show_pad_template()
    create_mail()

