"""Testing the preprocessing module."""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from preprocessing import preprocess
from datetime import datetime

class TestPreprocessing(unittest.TestCase):
    """Testing the preprocessing module."""

    def test_preprocess_pas(self):
        """Test the preprocess function on a PAS message."""
        # PAS message
        system_dict = {'type': 'PAS', 'mrn': 478237423, 'dob': datetime(1984, 2, 3), 'sex': 'F'}
        database_dict = {'mrn': 478237423, 'dob': datetime(1984, 2, 3), 'sex': 'F', 'last_measurement': 103.4}
        self.assertIsNone(preprocess(system_dict, database_dict))

    def test_preprocess_lims(self):
        """Test the preprocess function on a LIMS message."""
        # LIMS message
        system_dict = {'type': 'LIMS', 'mrn': 478237423, 'time': datetime(2024, 1, 20, 22, 43, 00), 'result': 103.4}
        database_dict = {'mrn': 478237423, 'dob': datetime(1984, 2, 3), 'sex': 'F', 'last_measurement': 99.6}
        expected_age = int((system_dict.get('time') - database_dict.get('dob')).days/365) 
        expected_output = {'age': expected_age, 'sex': 0, 'prev_result': 99.6, 'latest_result': 103.4}
        self.assertEqual(preprocess(system_dict, database_dict), expected_output)

    def test_preprocess_lims_one_result(self):
        """Test the preprocess function on a LIMS message with only one result (no result in db)."""
        # LIMS message
        system_dict = {'type': 'LIMS', 'mrn': 478237423, 'time': datetime(2024, 1, 20, 22, 43, 00), 'result': 103.4}
        database_dict = {'mrn': 478237423, 'dob': datetime(1984, 2, 3), 'sex': 'M', 'last_measurement': None}
        expected_age = int((system_dict.get('time') - database_dict.get('dob')).days/365) 
        expected_output = {'age': expected_age, 'sex': 1, 'prev_result': 103.4, 'latest_result': 103.4}
        self.assertEqual(preprocess(system_dict, database_dict), expected_output)

    def test_preprocess_invalid(self):
        """Test the preprocess function on an invalid message."""
        # Invalid message
        # Should not occur
        system_dict = {'type': 'invalid', 'mrn': 478237423, 'time': datetime(2024, 1, 20, 22, 43, 00), 'result': 103.4}
        database_dict = {'mrn': 478237423, 'dob': datetime(1984, 2, 3), 'sex': 'F', 'last_measurement': 99.6}
        self.assertRaises(ValueError, preprocess, system_dict, database_dict)


if __name__ == '__main__':
    unittest.main()
