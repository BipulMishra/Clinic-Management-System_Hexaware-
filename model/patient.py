class Patient:
    def __init__(self,patient_id,name,age,gender,symptoms,contact):
        self.patient_id=patient_id
        self.name=name
        self.age=age
        self.gender=gender
        self.symptoms=symptoms
        self.contact=contact

    def __str__(self):
        return (f'Patient ID:{self.patient_id}\n'
                f'Name:{self.name}\n'
                f'Age:{self.age}\n'
                f'Gender:{self.gender}\n'
                f'Symptoms:{self.symptoms}\n'
                f'Contact:{self.contact}\n')      