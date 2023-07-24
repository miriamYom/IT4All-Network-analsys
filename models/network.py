from fastapi import UploadFile
from pydantic import BaseModel


class Network(BaseModel):
    client_id: str
    date_taken: str
    location_name: str
