# copy this file to config.py and fill out

CSV_FILE = "AbsenceList.csv"

AUSBILDER = {
    'ITF19a': {
        'Schmitz': 'meier@example.org',
        'Meiler': 'mueller@example.org',
    }
}

SUBJECT_TEMPLATE = "Versäumter Untericht {langname}"

BODY_TEMPLATE = """{langname} hat gefehlt am {beginndatum} {beginnzeit} bis {enddatum} {endzeit}
"""

TOLERIERTE_VERSPAETUNG_MINUTEN = 30
