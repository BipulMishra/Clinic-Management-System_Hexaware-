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


 
