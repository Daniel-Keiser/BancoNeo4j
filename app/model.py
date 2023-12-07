# model.py
from datetime import datetime
from typing import Optional
from typing import Union


from pydantic import BaseModel, Field, validator
from pydantic.v1.datetime_parse import parse_datetime


class UserList(BaseModel):
    id: str
    username: str
    password: str
    username: str
    first_name: str
    last_name: str
    gender: str
    create_at: str
    status: str

class UserEntry(BaseModel):
    username: str = Field(..., example="potinejj")
    username: str = Field(..., example="PotineCool")
    password: str = Field(..., example="potinejj")
    first_name: str = Field(..., example="Potine")
    last_name: str = Field(..., example="Sambo")
    gender: str = Field(..., example="M")

class UserUpdate(BaseModel):
    id: str = Field(..., example="Enter your id")
    username:  str = Field(..., example="PotineCool")
    first_name: str = Field(..., example="Potine")
    last_name: str = Field(..., example="Sambo")
    gender: str = Field(..., example="M")
    status: str = Field(..., example="1")


class UserDelete(BaseModel):
    id: str = Field(..., example="Enter your id")

# SQLAlchemy model for creating a specialty
class SpecialtyCreate(BaseModel):
    name: str

class StatusCreate(BaseModel):
    name: str

# SQLAlchemy model for retrieving a specialty
class Specialty(BaseModel):
    id: int
    name: str


class Status(BaseModel):
    id: str
    name: str


# Crie um endpoint para a criação de médicos
class PatientCreate(BaseModel):
    user_id: str
    medical_history: str
    contact_emergency: str
    address: str
    phone_number: str
    age: int

class Patient(PatientCreate):
    id: Optional[int]

    class Config:
        orm_mode = True


class DoctorCreate(BaseModel):
    user_id: str
    specialization_id: str


class MedicalAppointmentCreate(BaseModel):
    patient_id: Optional[str]
    doctor_id: Optional[str]
    specialty_id: Optional[str]
    appointment_datetime: Optional[str]  # Agora, estamos recebendo a data como string
    status_id: Optional[str]
    observations: Optional[str]
    duration: Optional[str]


class MedicalAppointmentWithDetails(BaseModel):
    appointment_id: str
    status_id: str
    status_name: str
    specialty_id: str
    specialty_name: str
    doctor_id: str
    patient_id: str
    appointment_datetime: str
    observations: str
    duration: str

class DoctorWithDetails(BaseModel):
    doctor_id: Optional[str]
    user_id: Optional[str]
    specialization_id: Optional[str]
    specialization_name: Optional[str]
    username: Optional[str]


class PatientWithUserDetails(BaseModel):
    patient_id: Optional[str]
    user_id: Optional[str]
    medical_history: Optional[str]
    contact_emergency: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    age: Optional[int]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class PatientUpdate(BaseModel):
    medical_history: Optional[str] = None
    contact_emergency: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    age: Optional[int] = None


class User(BaseModel):
    id: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    
class Patient(BaseModel):
    id: str
    user_id: str
    medical_history: Optional[str] = None
    contact_emergency: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    age: Optional[int] = None

class PatientWithUserDetails(BaseModel):
    patient_id: str
    user_id: str
    medical_history: Optional[str] = None
    contact_emergency: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    age: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    specialty_id: str
    appointment_datetime: str
    status_id: str
    observations: str
    duration: str