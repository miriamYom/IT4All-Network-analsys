from pydantic import BaseModel
from datetime import date


class Network(BaseModel):
    id: int
    client_id: int
    location_name: str = "ירושלים"
    date_taken: str



