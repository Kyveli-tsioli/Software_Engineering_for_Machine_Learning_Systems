import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect('./patients.db', uri=True)

c = conn.cursor()

c.execute("""DROP TABLE patients""")
c.execute("""DROP TABLE measurements""")
c.execute("""CREATE TABLE patients (
            _mrn integer,
            dob text,
            sex text,
            PRIMARY KEY (_mrn)
            )""")
c.execute("""CREATE TABLE measurements (
            _mrn integer,
            date text,
            value real,
            PRIMARY KEY (_mrn, date, value)
            )""")

with open('./data/history.csv', 'r') as file:
    r = csv.reader(file)
    next(r) # skip headers

    for patient_data in r:

        # Read the age of the patient and raise an error if it is not an integer or is missing.
        mrn = patient_data[0]
        assert mrn.isdigit(), "patient's age is not an integer"
        patient_data.pop(0)

        with conn:
            c.execute("INSERT INTO patients VALUES (:_mrn, :dob, :sex)",
                      {'_mrn': mrn, 'dob': None, 'sex': None})

        for measurement_idx in range(0, len(patient_data), 2):
            try:
                date = datetime.strptime(patient_data[measurement_idx], '%Y-%m-%d %H:%M:%S')
                value = float(patient_data[measurement_idx+1])
                with conn:
                    c.execute("INSERT INTO measurements VALUES (:_mrn, :date, :value)",
                              {'_mrn': mrn, 'date': date, 'value': value})
            except ValueError:
                continue

conn.close()