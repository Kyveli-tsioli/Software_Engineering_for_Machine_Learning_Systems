import hl7
from datetime import datetime

def parse_hl7_message(hl7_message: str) -> dict:
    """Parse an HL7 message into a Python dictionary.
    Args:
        hl7_message: A string containing an HL7 message.
    Returns:
        A dictionary containing the parsed HL7 message.
        The dictionary will contain the following keys:
        - 'type': The type of message (PAS or LIMS). (type: str)
        - 'mrn': The patient's medical record number. (type: int)
        - 'dob': The patient's date of birth (PAS only). (type: datetime)
        - 'sex': The patient's sex (PAS only). (type: str)
        - 'time': The time of the test (LIMS only). (type: datetime)
        - 'result': The test result (LIMS only). (type: float)
        None if the message is not ADT^A01 or ORU^R01.
    """
    # Identify if PAS or LIMS
    message = hl7.parse(hl7_message)
    # Message type (PAS or LIMS)
    msh9 = str(message.segments('MSH')[0][9][0])
    # Patient MRN
    pid3 = int(str(message.segments('PID')[0][3]))

    if msh9 == "ADT^A01":
        # PAS admission
        # Patient DOB
        pid7 = str(message.segments('PID')[0][7])
        pid7 = datetime.strptime(pid7, '%Y%m%d')
        # Patient sex
        pid8 = str(message.segments('PID')[0][8])
        return {'type': 'PAS', 'mrn': pid3, 'dob': pid7, 'sex': pid8}

    elif msh9 == "ORU^R01":
        # LIMS result
        # Check if creatinine
        obx3 = str(message.segments('OBX')[0][3])
        if obx3 == "CREATININE":
            # Time of test
            obr7 = str(message.segments('OBR')[0][7])
            obr7 = datetime.strptime(obr7, '%Y%m%d%H%M%S')
            # Creatinine result
            obx5 = float(message.segments('OBX')[0][5][0])
            return {'type': 'LIMS', 'mrn': pid3, 'time': obr7, 'result': obx5}
        else:
            # Not creatinine, ignore
            return None
        
    else:
        # Not ADT^01 or ORU^01, ignore
        return None

if __name__ == "__main__":
    # Below just for testing
    # ADT^A01 message
    message = "MSH|^~\&|SIMULATION|SOUTH RIVERSIDE|||202401201630||ADT^A01|||2.5\r"
    message += "PID|1||478237423||ELIZABETH HOLMES||19840203|F\r"
    message += "NK1|1|SUNNY BALWANI|PARTNER\r"
    
    # # ORU^R01 message
    # message = "MSH|^~\&|SIMULATION|SOUTH RIVERSIDE|||202401201800||ORU^R01|||2.5\r"
    # message += "PID|1||478237423\r"
    # message += "OBR|1||||||202401202243\r"
    # message += "OBX|1|SN|CREATININE||103.4\r"

    # # ADT^A03 message (should return None)
    # message = "MSH|^~\&|SIMULATION|SOUTH RIVERSIDE|||202401221000||ADT^A03|||2.5\r"
    # message += "PID|1||478237423\r"

    parsed_message = parse_hl7_message(message)
    for key, value in parsed_message.items():
        print(f"{key}: {value} of type {type(value)}")