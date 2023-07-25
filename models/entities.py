from pydantic import BaseModel
from datetime import date


class Network(BaseModel):
    client_id: int
    location_name: str = "ירושלים"
    date_taken: date


network = Network(client_id=2,date_taken=15/25/2022)
print(network)
