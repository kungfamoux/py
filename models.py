from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Patient(BaseModel):
    id: int
    name: str
    age: int
    sex: str
    weight: float
    height: float
    phone: str


class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    is_available: bool = True


class Appointment(BaseModel):
    id: int
    patient: int  # Use patient id
    doctor: int  # Use doctor id
    date: datetime
