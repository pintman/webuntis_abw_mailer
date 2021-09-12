import webbrowser
import csv
import config
import datetime

# Langname	Vorname	ID	Klasse	Beginndatum	Beginnzeit	Enddatum	Endzeit	Unterbrechungen	Abwesenheitsgrund	Text/Grund	Entschuldigungsnummer	Status	Entschuldigungstext	gemeldet von Schüler*in
URL_TEMPLATE = "mailto:{to}?subject={subject}&body={body}"

def read_absences(filename:str):
    csv.register_dialect('untis', delimiter='\t')
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='untis')
        for row in reader:
            yield row

def send_mail(to, subject, body):
    webbrowser.open(
        URL_TEMPLATE.format(to=to, subject=subject, body=body)
    )

def main():
    for row in read_absences(config.CSV_FILE):
        klasse = row['Klasse']
        if klasse not in config.AUSBILDER:
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
            if minutes_late < config.TOLERIERTE_VERSPAETUNG_MINUTEN:
                continue

        name = row['Langname']        
        body = config.BODY_TEMPLATE.format(
            langname=name,
            beginndatum=b_dat, beginnzeit=b_zeit,
            enddatum=e_dat, endzeit=e_zeit
        )
        if name not in config.AUSBILDER[klasse]:
            print(f'Keine Ausbildermail für {name} ({klasse})')
            continue
        ausbildermail = config.AUSBILDER[klasse][name]
        subject = config.SUBJECT_TEMPLATE.format(langname=name)
        print('Sende Verspätung für', name, 'an', ausbildermail)
        send_mail(ausbildermail, subject, body)

        input("Enter for next mail")

if __name__ == '__main__':
    main()
