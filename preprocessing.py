import hl7
from datetime import datetime
import numpy as np


def preprocess(system_dict, database_dict):
    """Prepares the input to the logistic regression model.
    Args:
        system_dict: A dictionary (from PAS or LIMS system) with the following keys:
        - 'type': The type of message (PAS or LIMS). (type: str)
        - 'mrn': The patient's medical record number. (type: int)
        - 'dob': The patient's date of birth (PAS only). (type: datetime)
        - 'sex': The patient's sex (PAS only). (type: str)
        - 'time': The time of the test (LIMS only). (type: datetime)
        - 'result': The test result (LIMS only). (type: float)

        database_dict: A dictionary from SQLite with the following keys:
        - 'mrn': The patient's medical record number. (type: int)
        - 'dob': The patient's date of birth (PAS only). (type: datetime)
        - 'sex': The patient's sex (PAS only). (type: str)
        - 'min_measurement': The patient's minimum measurement based on their health record (type: float)
        - 'mean_measurement': The patient's mean measurement based on their health record (type: float)
        - 'num_of_tests": number of tests taken so far (int)

    Returns:
        A numpy array with the features for the logistic regression model.
        The returned array will be of the form: [age, sex, min_measurement, mean_measurement, new_measurement]
        where:
        - 'age': The patient's age (type: float)
        - 'sex': The patient's sex (type: int)
        - 'min_measurement': The patient's minimum measurement based on their health record (type: float)
        - 'mean_measurement': The patient's mean measurement based on their health record (type: float)
        - 'new_measurement': The patient's latest measurement (type: float)
    """

    
    if system_dict.get('type')== 'LIMS': #Identify if PAS or LIMS 

        #Assuming datetime objects in both PAS and SQLite, '%Y%m%d%H%M%S' format in LIMS (testtime), '%Y%m%d' in SQLite (dob)
        age= int((system_dict.get('time') - database_dict.get('dob')).days/365) 
        

        #Retrieve sex from SQLite and preprocess it 
        sex= database_dict.get('sex')
        assert (sex == 'M' or sex == 'F'), "patient's gender is not male or female"
        sex = (1 if sex == 'M' else 0)  #what if 'M' or 'F' instead of 'm'/'f'???


        #Check existence of historical data in SQLite, if values are set to 'None' then replace them with the last measurement from LIMS
        ##min_measurement, mean_measurement = database_dict.get('min_measurement'), database_dict.get('mean_measurement')
        ##all_none= all(value is None for value in [min_measurement, mean_measurement])

        # all_none= all(value is None for value in historical_data)
        # min_measurement = database_dict.get('min_measurement')
        # mean_measurement = database_dict.get('mean_measurement')
        latest_result= system_dict.get('result')
        prev_result= database_dict.get('last_measurement') #the current last measurement which will turn into previous_measurement


        if prev_result==None:
            prev_result= latest_result 
 

        ##if all_none:
            ##for key in ['min_measurement', 'mean_measurement']:
                ##database_dict[key]= new_measurement
            ##database_dict['num_of_tests'] = 1 #access the last key of the dictionary and set its value to 1
        ##else:
            #Retrieve latest (new) measurement
            ##num_of_tests = database_dict.get('num_of_tests')  # Provide default value to avoid NoneType

            #Update mean and min values and number of tests taken (in database)
            ##mean_measurement = (num_of_tests * mean_measurement + new_measurement) / (num_of_tests + 1)
            ##database_dict.update({'mean_measurement': mean_measurement})
            ##min_measurement = min(database_dict.get('min_measurement'), new_measurement) #retrieves the min_measurement from database, using "new_measurement" as the default value if min_measurement doesn't exist in the dict
            ##database_dict.update({'min_measurement': min_measurement})
            ##database_dict.update({'num_of_tests': num_of_tests+1 })
  
        return {
            "age": age,
            "sex": sex, 
            ##"min": database_dict.get('min_measurement'),
            ##"mean": database_dict.get('mean_measurement'),
            "latest_result": latest_result,
            "prev_result": prev_result
            } #feed this to the model by first converting it to a numpy array

    elif system_dict.get('type')== 'PAS':

        #age= int((datetime.now()-system_dict.get('dob')).days/365)
        #Retrieve up-to-date sex from the PAS dict directly
        #sex= system_dict.get('sex')

        print("Waiting for LIMS message first ...")
        return None
    
    else:
        raise ValueError("Invalid data, dictionary from 'PAS' or 'LIMS' system is expected")
    








#BELOW IS JUST FOR TESTING
# obr7="202302041530"
# obr7db="19960913"
# obr7db=datetime.strptime(obr7db, '%Y%m%d') #maybe string?
# obr7 = datetime.strptime(obr7, '%Y%m%d%H%M')
# trial_lims= {'type': 'LIMS', 'mrn': 132, 'time': obr7, 'result': 123}
# trial_pas= {'type': 'PAS', 'mrn': 151, 'dob': obr7db, 'sex': 'M'}
# trial_database_dict= {'mrn': 132, 'dob': obr7db, 'sex': 'f', 'min_measurement': None, 'mean_measurement': None, 'num_of_tests': None}
# trial_run= new_preprocessing(trial_lims, trial_database_dict)
# print(trial_run)







