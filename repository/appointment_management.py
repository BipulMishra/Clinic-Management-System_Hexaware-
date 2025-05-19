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