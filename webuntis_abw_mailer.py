import webbrowser
import csv
import configparser
import datetime
import urllib.parse

# Langname	Vorname	ID	Klasse	Beginndatum	Beginnzeit	Enddatum	Endzeit	Unterbrechungen	Abwesenheitsgrund	Text/Grund	Entschuldigungsnummer	Status	Entschuldigungstext	gemeldet von Schüler*in
URL_TEMPLATE = "mailto:{to}?subject={subject}&body={body}"

config = configparser.ConfigParser()
config.read('config.ini')


def read_absences(filename:str):
    csv.register_dialect('untis', delimiter='\t')
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='untis')
        for row in reader:
            yield row

def send_mail(to, subject, body):
    webbrowser.open(
        URL_TEMPLATE.format(
            to=to, 
            subject=urllib.parse.quote(subject), 
            body=urllib.parse.quote(body))
    )

def main():
    for row in read_absences(config['DEFAULT']['CSV_FILE']):
        klasse = row['Klasse']
        if 'Ausbilder.'+klasse not in config:
            continue

        b_dat, b_zeit = row['Beginndatum'], row['Beginnzeit']
        e_dat, e_zeit = row['Enddatum'], row['Endzeit']

        if b_dat  == e_dat:
            b = datetime.time.fromisoformat(b_zeit)
            e = datetime.time.fromisoformat(e_zeit)
            today = datetime.date.today()
            delta = datetime.datetime.combine(today, e) - \
                    datetime.datetime.combine(today, b)
            minutes_late = delta.total_seconds() / 60
            if minutes_late < int(config['DEFAULT']['TOLERIERTE_VERSPAETUNG_MINUTEN']):
                continue

        name = row['Langname']        
        body = config['Template']['BODY'].format(
            langname=name,
            beginndatum=b_dat, beginnzeit=b_zeit,
            enddatum=e_dat, endzeit=e_zeit
        )
        if name not in config['Ausbilder.'+klasse]:
            print(f'Keine Ausbildermail für {name} ({klasse})')
            continue
        ausbildermail = config['Ausbilder.'+klasse][name]
        subject = config['Template']['SUBJECT'].format(langname=name)
        print('Sende Verspätung für', name, 'an', ausbildermail)
        send_mail(ausbildermail, subject, body)

        input("Enter for next mail")

if __name__ == '__main__':
    main()
