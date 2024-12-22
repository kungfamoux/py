from fastapi import FastAPI, HTTPException
from typing import List
from models import Patient, Doctor, Appointment

app = FastAPI()

patients_db = {}
doctors_db = {}
appointments_db = {}

@app.post("/patients/", response_model=Patient)
def create_patient(patient: Patient):
    patients_db[patient.id] = patient
    return patient

@app.get("/patients/", response_model=List[Patient])
def get_patients():
    return list(patients_db.values())

@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient: Patient):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    patients_db[patient_id] = patient
    return patient

@app.delete("/patients/{patient_id}", status_code=204)
def delete_patient(patient_id: int):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    del patients_db[patient_id]

@app.post("/doctors/", response_model=Doctor)
def create_doctor(doctor: Doctor):
    doctors_db[doctor.id] = doctor
    return doctor

@app.get("/doctors/", response_model=List[Doctor])
def get_doctors():
    return list(doctors_db.values())

@app.put("/doctors/{doctor_id}", response_model=Doctor)
def update_doctor(doctor_id: int, doctor: Doctor):
    if doctor_id not in doctors_db:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctors_db[doctor_id] = doctor
    return doctor

@app.delete("/doctors/{doctor_id}", status_code=204)
def delete_doctor(doctor_id: int):
    if doctor_id not in doctors_db:
        raise HTTPException(status_code=404, detail="Doctor not found")
    del doctors_db[doctor_id]

@app.post("/appointments/", response_model=Appointment)
def create_appointment(appointment: Appointment):
    available_doctor = None
    for doctor in doctors_db.values():
        if doctor.is_available:
            available_doctor = doctor
            break

    if not available_doctor:
        raise HTTPException(status_code=400, detail="No doctors available")

    appointment.doctor = available_doctor.id
    appointments_db[appointment.id] = appointment
    available_doctor.is_available = False  # Mark doctor as unavailable
    return appointment

@app.post("/appointments/{appointment_id}/complete", status_code=204)
def complete_appointment(appointment_id: int):
    if appointment_id not in appointments_db:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment = appointments_db[appointment_id]
    doctor = doctors_db[appointment.doctor]
    doctor.is_available = True
    del appointments_db[appointment_id]

@app.delete("/appointments/{appointment_id}", status_code=204)
def cancel_appointment(appointment_id: int):
    if appointment_id not in appointments_db:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment = appointments_db[appointment_id]
    doctor = doctors_db[appointment.doctor]
    doctor.is_available = True  # Make doctor available again
    del appointments_db[appointment_id]

@app.put("/doctors/{doctor_id}/availability")
def set_availability(doctor_id: int, is_available: bool):
    if doctor_id not in doctors_db:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctors_db[doctor_id].is_available = is_available
