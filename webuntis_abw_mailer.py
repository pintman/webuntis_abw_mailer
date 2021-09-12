import webbrowser
import csv
import config

CSV_FILE = "AbsenceList.csv"
# Langname	Vorname	ID	Klasse	Beginndatum	Beginnzeit	Enddatum	Endzeit	Unterbrechungen	Abwesenheitsgrund	Text/Grund	Entschuldigungsnummer	Status	Entschuldigungstext	gemeldet von Schüler*in
URL_TEMPLATE = "mailto:{to}?subject={subject}&body={body}"

def read_absences(filename:str):
    csv.register_dialect('untis', delimiter='\t')
    with open(CSV_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='untis')
        for row in reader:
            yield row
               

def send_mail(to, subject, body):
    print('sending mail to',to)
    webbrowser.open(
        URL_TEMPLATE.format(to=to, subject=subject, body=body)
    )

for row in read_absences(CSV_FILE):
    klasse = row['Klasse']
    if klasse not in config.AUSBILDER:
        continue

    name = row['Langname']
    ausbildermail = config.AUSBILDER[klasse][name]
    subject = config.SUBJECT_TEMPLATE.format(langname=name)
    body = config.BODY_TEMPLATE.format(
        langname=name,
        beginndatum=row['Beginndatum'], beginnzeit=row['Beginnzeit'],
        enddatum=row['Enddatum'], endzeit=row['Endzeit']
    )
    send_mail(ausbildermail, subject, body)
    input("Enter for next mail")
