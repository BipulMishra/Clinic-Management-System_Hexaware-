class PatientNotFoundException(Exception):
    def __init__(self):
        super().__init__("Patient not found. Please check patient ID or name.")