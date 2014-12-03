#! /usr/bin/env python
# -*- coding: utf-8 -*-

from create_site import get_next_date


RECOMMENDED_MAILING_LISTS = [
    ("Chaos Darmstadt", "darmstadt@lists.metarheinmain.de", "https://lists.metarheinmain.de/mailman/listinfo/darmstadt"),
    ("Python-DE", "python-de@python.org", "http://mail.python.org/mailman/listinfo/python-de"),

]

def main():
    starting_date, meetings = get_next_date()
    print("Nächster PyStaDa: #{1} am {0}".format(starting_date, meetings))
    print("Ankündigungen sollten wenn möglich nicht nur auf der PyStaDa-ML, sondern auch auf anderen relavanten MLs erscheinen, da wir ja auch potenzielle neue Mitglieder ansprechen wollen.")
    print("Auf folgenden Mailinglisten sind die Ankündigungen gut aufgehoben:")
    for (name, mail_address, website) in RECOMMENDED_MAILING_LISTS:
        print("{name}: {address} ({website})".format(name=name, address=mail_address, website=website))
    
    print("\n\nMail-Inhalt folgt...")
    print("-" * 10)

    with open('mail.template') as template_file:
        mail_template = ''.join(template_file.readlines())

    
    print(mail_template.format(date=starting_date, month=starting_date.strftime('%B')))


if __name__ == '__main__':
    main()

