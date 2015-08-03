#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import locale

SHOWN_DATES = 3
FIRST_DATE = datetime.datetime(2014, 1, 29, 19)
DELTA = datetime.timedelta(weeks=2)
DATES_TO_SKIP = (datetime.datetime(2014, 12, 31, 19), )

WANTED_LOCALE = 'de_DE.UTF-8'
try:
    locale.setlocale(locale.LC_ALL, WANTED_LOCALE)
except locale.Error:
    print("Einstellen der deutschen Sprachsettings gescheitert."
          "Bitte sicherstellen, dass die locale '{0}' vorhanden ist."
          .format(WANTED_LOCALE))


def main():
    def format_date(date, hide_agenda_link=False):
        if hide_agenda_link:
            line_template = '<li><span style="color: #999999;">Mittwoch, {date.day}. {month} {date.year} um {date.hour}:{date.minute:02} Uhr</span></li>'
        else:
            line_template = '<li id="current"><span>Mittwoch, {date.day}. {month} {date.year} um {date.hour}:{date.minute:02} Uhr (<a href="https://pads.darmstadt.ccc.de/p/pystada-{date.year}-{date.month:02}-{date.day:02}">Agenda</a>)</span></li>'

        return line_template.format(date=date, month=date.strftime('%B'))


    starting_date, issue = get_next_date()
    print("Nächster PyStaDa: #{1} am {0}".format(starting_date, issue))

    list_template = '''\
<ul>
{elements}
</ul>\
'''.format(elements='\n'.join([format_date(starting_date + (i * DELTA),
                                           hide_agenda_link=i)
                               for i in range(SHOWN_DATES)]))

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
    today = datetime.datetime.now()
    issue = 1
    starting_date = FIRST_DATE
    latest_date = today + DELTA

    while starting_date <= latest_date:
        if starting_date not in DATES_TO_SKIP:
            yield (starting_date, issue)
            issue += 1

        starting_date += DELTA


if __name__ == '__main__':
    main()
