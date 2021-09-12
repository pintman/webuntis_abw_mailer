import webbrowser
import csv
import configparser
import datetime
import urllib.parse

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

def time_delta_minutes(t1, t2):
    b = datetime.time.fromisoformat(t1)
    e = datetime.time.fromisoformat(t2)
    today = datetime.date.today()
    delta = datetime.datetime.combine(today, e) - \
            datetime.datetime.combine(today, b)
    return delta.total_seconds() / 60

def main():
    for row in read_absences(config['DEFAULT']['CSV_FILE']):
        klasse = row['Klasse']
        ausbilder_key = 'Ausbilder.' + klasse
        if ausbilder_key not in config:
            continue

        b_dat, b_zeit = row['Beginndatum'], row['Beginnzeit']
        e_dat, e_zeit = row['Enddatum'], row['Endzeit']

        name = row['Langname']        
        if b_dat  == e_dat:
            minutes_late = time_delta_minutes(b_zeit, e_zeit)
            tolerable_late_minutes = int(config['DEFAULT']['TOLERIERTE_VERSPAETUNG_MINUTEN'])
            if minutes_late <= tolerable_late_minutes:
                print(f'Tolerierte Abwesenheit: {name} ({klasse}) {b_dat}: {b_zeit} - {e_zeit}')
                continue

        body = config['Template']['BODY'].format(
            langname=name,
            beginndatum=b_dat, beginnzeit=b_zeit,
            enddatum=e_dat, endzeit=e_zeit
        )
        if name not in config[ausbilder_key]:
            print(f'Keine Ausbildermail für {name} ({klasse})')
            continue
        ausbildermail = config[ausbilder_key][name]
        subject = config['Template']['SUBJECT'].format(langname=name)
        print('Sende Verspätung für', name, 'an', ausbildermail)
        send_mail(ausbildermail, subject, body)

        input("Enter for next mail")

if __name__ == '__main__':
    main()
