"""Testing the parse module."""

import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from datetime import datetime
from parse import parse_hl7_message

class TestParse(unittest.TestCase):
    """Testing the parse module."""

    def test_parse_admission(self):
        """Test the parse_hl7_message function on an ADT^A01 message."""
        # ADT^A01 message
        message = "MSH|^~\&|SIMULATION|SOUTH RIVERSIDE|||202401201630||ADT^A01|||2.5\r"
        message += "PID|1||478237423||ELIZABETH HOLMES||19840203|F\r"
        message += "NK1|1|SUNNY BALWANI|PARTNER\r"
        self.assertEqual(parse_hl7_message(message), {'type': 'PAS', 'mrn': 478237423, 'dob': datetime(1984, 2, 3), 'sex': 'F'})
    
    def test_parse_lims(self):
        """Test the parse_hl7_message function on an ORU^R01 message."""
        # ORU^R01 message
        message = "MSH|^~\&|SIMULATION|SOUTH RIVERSIDE|||202401201800||ORU^R01|||2.5\r"
        message += "PID|1||478237423\r"
        message += "OBR|1||||||20240120224300\r"
        message += "OBX|1|SN|CREATININE||103.4\r"
        self.assertEqual(parse_hl7_message(message), {'type': 'LIMS', 'mrn': 478237423, 'time': datetime(2024, 1, 20, 22, 43, 00), 'result': 103.4})

    def test_parse_lims_not_creatinine(self):
        """Test the parse_hl7_message function on an ORU^R01 message with a test that is not creatinine."""
        # ORU^R01 message (not creatinine)
        message = "MSH|^~\&|SIMULATION|SOUTH RIVERSIDE|||202401201800||ORU^R01|||2.5\r"
        message += "PID|1||478237423\r"
        message += "OBR|1||||||20240120224300\r"
        message += "OBX|1|SN|BLOOD||103.4\r"
        self.assertIsNone(parse_hl7_message(message))

    def test_parse_ignore(self):
        """Test the parse_hl7_message function on an ADT^A03 message."""
        # ADT^A03 message (should return None)
        message = "MSH|^~\&|SIMULATION|SOUTH RIVERSIDE|||202401221000||ADT^A03|||2.5\r"
        message += "PID|1||478237423\r"
        self.assertIsNone(parse_hl7_message(message))

if __name__ == "__main__":
    unittest.main()