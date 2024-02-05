import argparse
import csv

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from preprocess_data import data_preprocessing
from sklearn.metrics import fbeta_score
import pickle


def train_model():

    # read the training csv
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/training.csv")
    flags = parser.parse_args()
    r = csv.reader(open(flags.input))

    # preprocess the training data
    training_data, training_labels = data_preprocessing(r, csv_type='train')

    # split the data into a training and test set with 80%-20% ratio
    X_train, X_test, y_train, y_test = train_test_split(training_data, training_labels,
                                                        test_size = 0.2, random_state = 42)

    # fit the model and make predicitons
    logisticRegr = LogisticRegression()
    logisticRegr.fit(X_train, y_train)
    predictions = logisticRegr.predict(X_test)
    print("The F3 score of the model is: " + str(fbeta_score(y_test, predictions, beta=3)))

    # store the model weights into a pickle file
    filename = 'model/trained_model.sav'
    pickle.dump(logisticRegr, open(filename, 'wb'))


train_model()
