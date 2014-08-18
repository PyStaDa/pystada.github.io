#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

SHOWN_DATES = 3


def main():
    def format_date(date, hide_agenda_link=False):
        if hide_agenda_link:
            line_template = '<li><span style="color: #999999;">Mittwoch, {date.day} {month} {date.year} um 19:30 Uhr <!--(<a href="https://pads.ccc.de/pystada-{date.year}-{date.month:02}-{date.day:02}">Agenda</a>)--></span></li>'
        else:
            line_template = '<li><span>Mittwoch, {date.day} {month} {date.year} um 19:30 Uhr (<a href="https://pads.ccc.de/pystada-{date.year}-{date.month:02}-{date.day:02}">Agenda</a>)</span></li>'

        return line_template.format(date=date, month=date.strftime('%B'))

    today = datetime.datetime.now()
    starting_date = datetime.datetime(2014, 8, 13, 19, 30)
    delta = datetime.timedelta(weeks=2)

    while starting_date < today:
        starting_date += delta

    print("Nächster PyStaDa: {0}".format(starting_date))

    list_template = '''\
<ul>
{elements}
</ul>\
'''.format(elements='\n'.join([format_date(starting_date + (i * delta), hide_agenda_link=i) for i in range(SHOWN_DATES)]))

    with open('index.html.template') as template_file:
        site_template = ''.join(template_file.readlines())

    with open('index.html', 'w') as outputfile:
        outputfile.write(site_template.format(dates=list_template))


if __name__ == '__main__':
    main()
