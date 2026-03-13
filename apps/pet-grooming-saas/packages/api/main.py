"""
Pet Grooming API — demo CRUD for appointments.

In-memory store for demo purposes. No DB credentials in code;
connect a real database via env vars in production.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Pet Grooming API", version="0.1.0")


def _uuid() -> str:
    return uuid4().hex[:12]


def _now() -> str:
    return datetime.now().isoformat()


class AppointmentCreate(BaseModel):
    pet_name: str
    owner_name: str
    service: str = "bath_and_trim"
    scheduled_at: str


class Appointment(BaseModel):
    id: str = Field(default_factory=_uuid)
    pet_name: str
    owner_name: str
    service: str
    scheduled_at: str
    created_at: str = Field(default_factory=_now)
    status: str = "scheduled"


_STORE: dict[str, Appointment] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/appointments", status_code=201)
def create_appointment(body: AppointmentCreate) -> Appointment:
    appt = Appointment(**body.model_dump())
    _STORE[appt.id] = appt
    return appt


@app.get("/api/v1/appointments")
def list_appointments() -> list[Appointment]:
    return list(_STORE.values())


@app.get("/api/v1/appointments/{appt_id}")
def get_appointment(appt_id: str) -> Appointment:
    appt = _STORE.get(appt_id)
    if appt is None:
        raise HTTPException(404, detail="appointment not found")
    return appt


@app.patch("/api/v1/appointments/{appt_id}")
def update_appointment(appt_id: str, body: dict) -> Appointment:
    appt = _STORE.get(appt_id)
    if appt is None:
        raise HTTPException(404, detail="appointment not found")
    for key, val in body.items():
        if hasattr(appt, key):
            setattr(appt, key, val)
    return appt


@app.delete(
    "/api/v1/appointments/{appt_id}",
    status_code=204,
)
def delete_appointment(appt_id: str):
    if appt_id not in _STORE:
        raise HTTPException(404, detail="appointment not found")
    del _STORE[appt_id]
