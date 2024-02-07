#!/usr/bin/env python3
from preprocessing import new_preprocessing
from parse import *
import argparse
import socket
import threading
import http.server
from datetime import datetime
import requests
import sqlite3
import time
import pickle
import numpy as np

VERSION = "0.0.0"

MLLP_BUFFER_SIZE = 1024
MLLP_START_OF_BLOCK = 0x0b
MLLP_END_OF_BLOCK = 0x1c
MLLP_CARRIAGE_RETURN = 0x0d

class Client():
    def __init__(self) -> None:
        self.messages = []

    def connect_to_server(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            trained_model = pickle.load(open('model/trained_model.sav', 'rb'))
            s.connect((host, port)) # connect with host
            conn = sqlite3.connect('./patients.db', uri=True)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            while True:
                data = s.recv(MLLP_BUFFER_SIZE) # reads server message
                if len(data) == 0:
                    raise Exception("server has no incoming messages")
                # TODO: check data validity here for if statement?

                parsed_dict = parse_hl7_message(data)
                # avoid discharge messages that return None
                if parsed_dict != None:
                    if parsed_dict["type"] == 'PAS':
                        self.save_query_db(conn, c, parsed_dict)
                    elif parsed_dict["type"] == 'LIMS':
                        t0 = time.time()
                        dict = self.retrieve_query_db(conn, c, parsed_dict["mrn"])
                        features = new_preprocessing(parsed_dict, dict)
                        features = np.array(list(features.values())).reshape(1,-1)
                        prediction = trained_model.predict(features)
                        if prediction == 'y':
                            page_request(host, port, parsed_dict["mrn"])
                        self.update_query_db(conn, c, parsed_dict)
                        t1 = time.time()
                        print("latency = ", t1-t0)
                msg = self.create_message("AA")
                s.sendall(msg) # send message to server
                print(f"Received {data!r}")
            conn.close()

    def create_message(self, msg_type):
        """
        Returns bytearray of the message to send depending on msg_type
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
            c.execute("SELECT MIN(value) AS min_measurement,"
                      " AVG(value) AS mean_measurement, COUNT(value) AS num_of_tests"
                      " FROM measurements WHERE _mrn=:_mrn", {'_mrn': _mrn})
            patient_history = dict(c.fetchall()[0])
            if patient_data['dob'] != None:
                patient_data['dob'] = datetime.strptime(patient_data['dob'],
                                                        '%Y-%m-%d %H:%M:%S')
            db_dict = {
                'mrn': patient_data['_mrn'],
                'dob': patient_data['dob'],
                'sex': patient_data['sex'],
                'min_measurement': patient_history['min_measurement'],
                'mean_measurement': patient_history['mean_measurement'],
                'num_of_tests': patient_history['num_of_tests']
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
    url = f"http://{host}:{port}/page"
    requests.post(url, data=mrn)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mllp", default=8440, type=int, help="Port for server")
    parser.add_argument("--pager", default=8441, type=int, help="Post on which to listen for pager requests via HTTP")
    flags = parser.parse_args()
    client = Client()
    client.connect_to_server("0.0.0.0", flags.mllp)
    # page_request("0.0.0.0", flags.pager)

    return

if __name__ == "__main__":
    # to kill port: lsof -i :PORT_NUM then kill PID
    main()