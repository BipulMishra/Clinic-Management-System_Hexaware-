# main.py 

from repository.appointment_management import AppointmentManagement
from exception.patient_not_found_exception import PatientNotFoundException

def main():
    app_mgmt = AppointmentManagement()

    while True:
        print("\nClinic Appointment Management\n")
        print("1. Add patient")
        print("2. Update contact")
        print("3. Delete patient")
        print("4. View all patients")
        print("5. Search patients")
        print("6. Filter by age")
        print("7. Exit\n")

        choice = input("Enter choice: ")

        try:
            if choice == '1':
                name = input("\nName: ")
                age = int(input("Age: "))
                gender = input("Gender: ")
                symptoms = input("Symptoms: ")
                contact = input("Contact: ")
                if app_mgmt.add_patient(name, age, gender, symptoms, contact):
                    print("\nPatient added successfully")

            elif choice == '2':
                patient_id = int(input("\nEnter Patient ID: "))
                new_contact = input("Enter new contact: ")
                if app_mgmt.update_patient_contact(patient_id, new_contact):
                    print("\nContact updated.")

            elif choice =='3':
                patient_id = int(input("\nEnter Patient ID to delete: "))
                if app_mgmt.delete_patient(patient_id):
                    print("\nPatient deleted.")

            elif choice == '4':
                print()
                patients = app_mgmt.get_all_patients()
                if not patients:
                    print("No patients found.")
                else:
                    for patient in patients:
                        print(patient)

            elif choice == '5':
                search_term = input("\nEnter name or symptom to search: ")
                print()
                patients = app_mgmt.search_patient(search_term)
                for patient in patients:
                    print(patient)

            elif choice == '6':
                threshold = int(input("\nEnter age threshold: "))
                print()
                patients = app_mgmt.filter_by_age(threshold)
                if not patients:
                    print(f"No patients found older than {threshold}.")
                else:
                    for patient in patients:
                        print(patient)

            elif choice == '7':
                print("\nExiting...\n")
                app_mgmt.close_connection()
                break

            else:
                print("\nInvalid choice. Please select between 1-7.")

        except PatientNotFoundException as pnf:
            print(f"\n{pnf}")

        except ValueError:
            print("\nInvalid input. Please enter correct data types.")

        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()


# main.py OVER 
# ------------------------------------------------------
# db_util.py


import pyodbc # type: ignore

class DBConnection:
    def __init__(self):
        self.conn=pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost,1433;'
            'DATABASE=appdb ;'
            'UID=sa;'
            'PWD=examlyMssql@123;'
        )
        self.cursor=self.conn.cursor()
        self.initialize_schema()

    def initialize_schema(self):
        create_table_query='''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Patients' AND xtype='U')
        CREATE TABLE Patients(
            patient_id INT IDENTITY(1,1) PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            gender VARCHAR(10),
            symptoms VARCHAR(255),
            contact VARCHAR(100)
        )
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def get_cursor(self):
        return self.cursor
    
    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

# db_util.py OVER
# ------------------------------------------------------
# appointment_management.py
from model.patient import Patient
from exception.patient_not_found_exception import PatientNotFoundException
from util.db_util import DBConnection

class AppointmentManagement:
    def __init__(self):
        self.db=DBConnection()
        self.cursor=self.db.get_cursor()

    def add_patient(self,name,age,gender,symptoms,contact):
        try:
            query = "INSERT INTO Patients (name,age,gender,symptoms,contact) Values (?,?,?,?,?)"
            self.cursor.execute(query,(name,age,gender,symptoms,contact))
            self.db.commit()
            return True 
        except Exception as e:
            print("Error while adding patients:",e)
            return False
            
    def update_patient_contact(self,patient_id,contact):
        self.cursor.execute("UPDATE Patients SET contact=? WHERE patient_id = ?",(contact,patient_id))
        if self.cursor.rowcount == 0:
            raise PatientNotFoundException()
        self.db.commit()
        return True
    
    def delete_patient(self,patient_id):
        self.cursor.execute("DELETE FROM Patients where patient_id=?",(patient_id,))
        if self.cursor.rowcount == 0:
            raise PatientNotFoundException()
        self.db.commit()
        return True 
    
    def get_all_patients(self):
        self.cursor.execute("SELECT * FROM Patients")
        patients =  self.cursor.fetchall()
        return [Patient(*row) for row in patients]

    def search_patient(self,search_term):
        query="SELECT * FROM Patients WHERE name LIKE ? OR symptoms LIKE ?"
        search_value=f"%{search_term}%"
        self.cursor.execute(query,(search_value,search_value))
        rows=self.cursor.fetchall()
        if not rows:
            raise PatientNotFoundException()
        return [Patient(*row) for row in rows]
    
    def filter_by_age(self, threshold):
        query = "SELECT * FROM Patients WHERE age > ?"
        self.cursor.execute(query, (threshold,))
        rows = self.cursor.fetchall()
        return [Patient(*row) for row in rows]
    
    def close_connection(self):
        self.db.close()       

# appointment_management.py OVER
# ------------------------------------------------------

# patient.py
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
    
# patient.py OVER
# ------------------------------------------------------
# patient_not_found_exception.py
class PatientNotFoundException(Exception):
    def __init__(self):
        super().__init__("Patient not found. Please check patient ID or name.")

# patient_not_found_exception.py OVER
