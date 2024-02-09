#!/usr/bin/env python3
# Relevant custom modules
from preprocessing import preprocess
from parse import *

# Standard libraries
import socket
from datetime import datetime
import time
import urllib.request
import os

# Machine learning libraries
import sqlite3
import pickle
import numpy as np


MLLP_BUFFER_SIZE = 1024
MLLP_START_OF_BLOCK = 0x0b
MLLP_END_OF_BLOCK = 0x1c
MLLP_CARRIAGE_RETURN = 0x0d

class Client():
    def __init__(self) -> None:
        self.messages = []

    def connect_to_server(self, host, port, pager_host, pager_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # load pre-trained model for inference
            trained_model = pickle.load(open('/model/trained_model.sav', 'rb'))
            s.connect((host, port))
            # connect with database containing historical data
            conn = sqlite3.connect('./patients.db', uri=True)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            while True:
                data = s.recv(MLLP_BUFFER_SIZE)
                if len(data) == 0:
                    print("No incoming messages.")
                    break
                parsed_dict = parse_hl7_message(data)
                # Disregard discharge messages that return None
                if parsed_dict != None:
                    if parsed_dict["type"] == 'PAS':
                        # Save information to database
                        self.save_query_db(conn, c, parsed_dict)
                    elif parsed_dict["type"] == 'LIMS':
                        t0 = time.time()
                        # Retrieve patient information from database using "mrn"
                        dict = self.retrieve_query_db(conn, c, parsed_dict["mrn"])
                        features = preprocess(parsed_dict, dict)
                        features = np.array(list(features.values())).reshape(1,-1)
                        prediction = 'n' if trained_model.predict(features)==0 else 'y'
                        if prediction == 'y':
                            # Send page request if inferred AKI
                            page_request(pager_host, pager_port, bytes(str(parsed_dict["mrn"]), "ascii"))
                        # Update test result to database
                        self.update_query_db(conn, c, parsed_dict)
                        t1 = time.time()
                        # print("latency = ", t1-t0)
                # Send message acknowledgement to server
                msg = self.create_message("AA")
                s.sendall(msg)
            conn.close()

    def create_message(self, msg_type):
        """
        Returns bytearray of the message to send depending on msg_type.
        """
        msg = bytes(chr(MLLP_START_OF_BLOCK), "ascii")
        curr_time = datetime.now().strftime("%Y%m%d%H%M%S")
        msg += bytes("MSH|^~\&|||||" + curr_time + "||ACK|||2.5", "ascii")
        msg += bytes(chr(MLLP_CARRIAGE_RETURN), "ascii")
        msg += bytes("MSA|" + msg_type, "ascii")
        msg += bytes(chr(MLLP_END_OF_BLOCK) + chr(MLLP_CARRIAGE_RETURN), "ascii")
        return msg

    def save_query_db(self, conn, c, parsed_dict):

        with conn:
            sql_statement = """
            INSERT INTO patients (_mrn, dob, sex)
            VALUES (?, ?, ?)
            ON CONFLICT(_mrn) DO UPDATE SET
                dob = excluded.dob,
                sex = excluded.sex;
            """
            data = (parsed_dict['mrn'], parsed_dict['dob'], parsed_dict['sex'])
            c.execute(sql_statement, data)

    def retrieve_query_db(self, conn, c, _mrn):
        with conn:
            c.execute("SELECT * FROM patients WHERE _mrn=:_mrn",
                      {'_mrn': _mrn})
            patient_data = dict(c.fetchall()[0])
            # c.execute("SELECT MIN(value) AS min_measurement,"
            #           " AVG(value) AS mean_measurement, COUNT(value) AS num_of_tests"
            #           " FROM measurements WHERE _mrn=:_mrn", {'_mrn': _mrn})
            c.execute("SELECT value AS latest_measurement"
                      " FROM measurements WHERE _mrn=:_mrn"
                      " ORDER BY date DESC"
                      " LIMIT 1"
                      , {'_mrn': _mrn})
            patient_history = dict(c.fetchall()[0])
            if patient_data['dob'] != None:
                patient_data['dob'] = datetime.strptime(patient_data['dob'],
                                                        '%Y-%m-%d %H:%M:%S')
            # db_dict = {
            #     'mrn': patient_data['_mrn'],
            #     'dob': patient_data['dob'],
            #     'sex': patient_data['sex'],
            #     'min_measurement': patient_history['min_measurement'],
            #     'mean_measurement': patient_history['mean_measurement'],
            #     'num_of_tests': patient_history['num_of_tests']
            # }
            db_dict = {
                'mrn': patient_data['_mrn'],
                'dob': patient_data['dob'],
                'sex': patient_data['sex'],
                'latest_measurement': patient_history['latest_measurement']
            }
        return db_dict

    def update_query_db(self, conn, c, parsed_dict):

        with conn:
            sql_statement = """
            INSERT INTO measurements (_mrn, date, value)
            VALUES (?, ?, ?)
            ON CONFLICT(_mrn, date, value) DO NOTHING;
            """
            data = (parsed_dict['mrn'],
                    parsed_dict['time'],
                    parsed_dict['result'])
            c.execute(sql_statement, data)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def page_request(host, port, mrn):
    """
    Sends a request with mrn to pager at host:port.
    """
    url = f"http://{host}:{port}/page"
    urllib.request.urlopen(url, data=mrn)


def split_host_port(string):
    """
    Splits string 'host:port' into host and port values.
    """
    if not string.rsplit(':', 1)[-1].isdigit():
        return string, None
    string = string.rsplit(':', 1)

    host = string[0]  # 1st index is always host
    port = int(string[1])

    return host, port


def main():
    mllp_host, mllp_port = split_host_port(os.environ['MLLP_ADDRESS'])
    pager_host, pager_port = split_host_port(os.environ['PAGER_ADDRESS'])
    client = Client()
    client.connect_to_server(mllp_host, mllp_port, pager_host, pager_port)

if __name__ == "__main__":
    main()

