#!/usr/bin/env python3

import argparse
import csv
import numpy as np
from preprocess_data import data_preprocessing
import pickle


def main():

    # Step 1: load the test csv which will be used to make predictions and open a csv file to store the output
    print("Loading the test csv...")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/test.csv")
    parser.add_argument("--output", default="data/aki.csv")
    flags = parser.parse_args()
    r = csv.reader(open(flags.input))
    w = csv.writer(open(flags.output, "w"))
    w.writerow(("aki",))

    # Step 2: Perform data preprocessing in the test csv
    print("Performing data preprocessing..")
    test_data = data_preprocessing(r, csv_type='test')

    # Step 3: Load the pre-trained model
    print("Loading the pre-trained model...")
    trained_model = pickle.load(open('model/trained_model.sav', 'rb'))

    # Step 4: Make predictions using the trained model
    print("Making predictions...")
    predictions = trained_model.predict(test_data)
    predictions = np.where(predictions == 0, "n", "y")

    # Step 5: Store the predictions in a csv file
    print("Storing the predicitons on aki.csv...")
    for pred in predictions:
        w.writerow(pred)
    print("Done.")


if __name__ == "__main__":
    main()