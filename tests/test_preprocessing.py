"""Testing the preprocessing module."""

#import sys
#import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#import unittest
#from new_preprocessing import new_preprocessing

#class TestPreprocessing(unittest.TestCase):
    #"""Testing the preprocessing module."""

    # TODO add tests
    # def test_preprocessing(self):
    #     """Test the new_preprocessing function."""
    #     from datetime import datetime
    #     trial_lims = {'type': 'LIMS', 'mrn': 132, 'time': datetime(2023, 2, 4, 15, 30), 'result': 123}
    #     trial_database_dict = 

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from preprocessing import new_preprocessing
from datetime import datetime

class TestPreprocessing(unittest.TestCase):
    """Testing the preprocessing module."""

    def test_preprocessing(self):
        """Test the new_preprocessing function."""
        

         
        # Define a sample input
        trial_input = {
            'type': 'LIMS',
            'mrn': 132,
            'time': datetime.now(),
            'result': 123
        }
        
        database_dict={'mrn': 132,
                'dob': datetime(1996, 9, 13, 15, 30),
                'sex': 'F',
                'min_measurement': None,
                'mean_measurement': None,
                'num_of_tests': None

        }

        # Call the preprocessing function
        actual_output = new_preprocessing(trial_input, database_dict)
        age_from_actual_output = actual_output.get('age', None)


        # Expected output after preprocessing, assuming what changes are made by the function
        expected_output = { "age": int((datetime.now()-database_dict.get('dob')).days/365),
            "sex": 1, 
            "min": 123,
            "mean": 123,
            "new measurement": 123}
          

        # Assert that the actual output matches the expected output
        self.assertEqual(actual_output, expected_output)


    def test_preprocessing_storage(self):
        """Test the new_preprocessing function."""
         
        # Define a sample input
        trial_input = {
            'type': 'LIMS',
            'mrn': 132,
            'time': datetime.now(),
            'result': 120
        }
        
        database_dict = {
            'mrn': 132,
            'dob': datetime(1996, 9, 13, 15, 30),
            'sex': 'F',
            'min_measurement': 150,  # Example previous value
            'mean_measurement': 140,  # Example previous average
            'num_of_tests': 1  # Example number of previous tests
        }

        # Call the preprocessing function
        actual_output = new_preprocessing(trial_input, database_dict)

        # Extract the updated values from the actual output
        updated_min = actual_output.get('min', None)
        updated_mean = actual_output.get('mean', None)
        updated_test_number= database_dict.update({'num_of_tests': database_dict.get('num_of_tests')+1})
        
        expected_min = 120
        expected_mean = 130
        expected_test_number= 2

        # Assert that the actual minimum and mean match the expected values
        self.assertEqual(updated_min, expected_min, "The minimum value did not match the expected value.")
        self.assertEqual(updated_mean, expected_mean, "The mean value did not match the expected value.")


if __name__ == '__main__':
    unittest.main()