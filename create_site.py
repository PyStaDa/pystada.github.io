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
            line_template = '<li><span style="color: #999999;">Mittwoch, {date.day}. {month} {date.year} um {date.hour}:{date.minute:02} Uhr <!--(<a href="https://pads.ccc.de/pystada-{date.year}-{date.month:02}-{date.day:02}">Agenda</a>)--></span></li>'
        else:
            line_template = '<li id="current"><span>Mittwoch, {date.day}. {month} {date.year} um {date.hour}:{date.minute:02} Uhr (<a href="https://pads.ccc.de/pystada-{date.year}-{date.month:02}-{date.day:02}">Agenda</a>)</span></li>'

        return line_template.format(date=date, month=date.strftime('%B'))


    starting_date, meetings = get_next_date()
    print("Nächster PyStaDa: #{1} am {0}".format(starting_date, meetings))

    list_template = '''\
<ul>
{elements}
</ul>\
'''.format(elements='\n'.join([format_date(starting_date + (i * DELTA), hide_agenda_link=i) for i in range(SHOWN_DATES)]))

    with open('index.html.template') as template_file:
        site_template = ''.join(template_file.readlines())

    with open('index.html', 'w') as outputfile:
        outputfile.write(site_template.format(dates=list_template))


def get_next_date():
    today = datetime.datetime.now()
    meetings = 1
    starting_date = FIRST_DATE

    while starting_date < today or starting_date in DATES_TO_SKIP:
        if starting_date not in DATES_TO_SKIP:
            meetings += 1

        starting_date += DELTA

    return (starting_date, meetings)


if __name__ == '__main__':
    main()

