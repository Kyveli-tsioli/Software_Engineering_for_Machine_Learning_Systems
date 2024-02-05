from datetime import datetime
import numpy as np


def data_preprocessing(x, csv_type):
    """Perform preprocessing on training and test csv files.

    Parameters
    ----------
    x : {reader object} of csv with one row per patient and dynamic number of columns
    csv_type: {str} "train" for a csv containing labels, or "test" otherwise

    Returns
    -------
    preprocessed_data: numpy array of shape [n_patients, n_features]
                       The 5 features used for each patient are:
                       a) age,
                       b) gender,
                       c) minimum creatinine measurement,
                       d) median creatinine measurement,
                       e) most recent creatinine measurement
    labels: {numpy array} of shape [n_patients] if input_type='train'
            or None if input_type='test'
    """

    next(x) # skip headers
    all_data = list()
    if csv_type == 'train':
        training_labels = list()
    elif csv_type == 'test':
        pass
    else:
        raise ValueError("Invalid argument, 'train' or 'test' type expected")

    for patient_data in x:

        # Read the age of the patient and raise an error if it is not an integer or is missing.
        age = patient_data[0]
        assert age.isdigit(), "patient's age is not an integer"
        patient_data.pop(0)

        # Read the gender of the patient and raise an error if it is not male or female
        # Convert male to '0' and female to '1'
        gender = patient_data[0]
        assert (gender == 'm' or gender == 'f'), "patient's gender is not male or female"
        gender = (0 if gender == 'm' else 1)
        patient_data.pop(0)

        # Read the aki of the patient and raise an error if it is not yes or no
        # Convert no to '0' and yes to '1'
        if csv_type == 'train':
            aki = patient_data[0]
            assert (aki == 'n' or aki == 'y'), "patient's aki is not yes or no"
            aki = (0 if aki == 'n' else 1)
            patient_data.pop(0)

        # Isolate creatinine min measurement, median measurement, and last measurement
        min_measurement, median_measurement, last_measurement_result = measurements_preprocessing(patient_data)

        # Append the preprocessed information of the patient to a list
        all_data.append([int(age), gender, min_measurement, median_measurement, last_measurement_result])
        if csv_type == 'train':
            training_labels.append(aki)

    # convert the lists to numpy arrays for easier manipulation
    all_data = np.array(all_data)
    if csv_type == 'train':
        training_labels = np.array(training_labels)

    if csv_type == 'train':
        return all_data, training_labels
    else:
        return all_data


def measurements_preprocessing(x):

    creatinine_results = list()
    for measurement_idx in range(0, len(x), 2):
        try:
            date = datetime.strptime(x[measurement_idx], '%Y-%m-%d %H:%M:%S')
            result = float(x[measurement_idx+1])
            creatinine_results.append(result)
        except ValueError:
            continue

    creatinine_results = np.array(creatinine_results)

    last_measurement_result = creatinine_results[-1]
    median_measurement = np.median(creatinine_results)
    min_measurement = creatinine_results.min()

    # return min measurement, median measurement, and last measurement
    return min_measurement, median_measurement, last_measurement_result
