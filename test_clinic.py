import os
import pytest # type: ignore
from repository.appointment_management import AppointmentManagement
from exception.patient_not_found_exception import PatientNotFoundException

# Folder existence tests
def test_model_folder_exists():
    assert os.path.isdir("model"), "model folder does not exist"

def test_repository_folder_exists():
    assert os.path.isdir("repository"), "repository folder does not exist"

def test_util_folder_exists():
    assert os.path.isdir("util"), "util folder does not exist"

def test_exception_folder_exists():
    assert os.path.isdir("exception"), "exception folder does not exist"

# File existence tests
def test_patient_file_exists():
    assert os.path.isfile("model/patient.py"), "patient.py file missing"

def test_appointment_management_file_exists():
    assert os.path.isfile("repository/appointment_management.py"), "appointment_management.py file missing"

def test_db_util_file_exists():
    assert os.path.isfile("util/db_util.py"), "db_util.py file missing"

def test_patient_not_found_exception_file_exists():
    assert os.path.isfile("exception/patient_not_found_exception.py"), "patient_not_found_exception.py file missing"

# Functional tests
@pytest.fixture(scope="module")
def appointment_repo():
    repo = AppointmentManagement()
    yield repo
    repo.close_connection()

def test_add_patient(appointment_repo):
    assert appointment_repo.add_patient("John Doe", 35, "Male", "Fever and cough", "john@example.com") is True

def test_search_patient(appointment_repo):
    appointment_repo.add_patient("Jane Smith", 28, "Female", "Migraine", "jane@example.com")
    results = appointment_repo.search_patient("Jane")
    assert len(results) > 0, "Patient search failed"

def test_update_patient_contact(appointment_repo):
    appointment_repo.add_patient("Alice Brown", 42, "Female", "Fatigue", "alice@old.com")
    patients = appointment_repo.search_patient("Alice")
    if patients:
        patient_id = patients[0].patient_id
        assert appointment_repo.update_patient_contact(patient_id, "alice@new.com") is True
    else:
        pytest.fail("Patient not found for update test")

def test_delete_patient(appointment_repo):
    appointment_repo.add_patient("Bob Clark", 30, "Male", "Back pain", "bob@example.com")
    patients = appointment_repo.search_patient("Bob")
    assert len(patients) > 0, "Patient was not added properly"
    patient_id = patients[0].patient_id
    assert appointment_repo.delete_patient(patient_id) is True, "Patient deletion failed"
    try:
        remaining = appointment_repo.search_patient("Bob")
        assert not any(p.patient_id == patient_id for p in remaining), "Patient still exists after deletion"
    except PatientNotFoundException:
        pass  