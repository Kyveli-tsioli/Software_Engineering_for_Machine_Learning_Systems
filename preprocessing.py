"""Preprocesses the input to the model."""

from datetime import datetime

def preprocess(system_dict, database_dict):
    """Prepares the input to the model.
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
        - 'latest_measurement': The patient's latest measurement in the database (type: float)

    Returns:
        If LIMS message, a dictionary with the following keys:
        - 'age': The patient's age (type: float)
        - 'sex': The patient's sex (type: int)
        - 'prev_result': The patient's previous measurement based on their health record (type: float)
        - 'latest_result': The patient's latest measurement based on their health record (type: float)
        Else, None.
    """
    if system_dict.get('type')== 'LIMS': # Identify if PAS or LIMS 

        # Assuming datetime objects in both PAS and SQLite, '%Y%m%d%H%M%S' format in LIMS (testtime), '%Y%m%d' in SQLite (dob)
        age = int((system_dict.get('time') - database_dict.get('dob')).days/365) 
        

        # Retrieve sex from SQLite and preprocess it 
        sex = database_dict.get('sex')
        assert (sex == 'M' or sex == 'F'), "patient's sex is not male or female"
        sex = (1 if sex == 'M' else 0)  #what if 'M' or 'F' instead of 'm'/'f'???

        # Get the latest result from system dict and previous from db
        latest_result = system_dict.get('result')
        prev_result = database_dict.get('last_measurement') # the current last measurement which will turn into prev_result

        # If the previous result is None, then the latest result will be the previous result
        if prev_result == None:
            prev_result = latest_result 
 
        # Return the preprocessed data
        return {
            "age": age,
            "sex": sex, 
            "latest_result": latest_result,
            "prev_result": prev_result
            }

    elif system_dict.get('type')== 'PAS':
        # No preprocessing needed for PAS message
        print("Waiting for LIMS message first ...")
        return None
    
    else:
        raise ValueError("Invalid data, dictionary from 'PAS' or 'LIMS' system is expected")
    