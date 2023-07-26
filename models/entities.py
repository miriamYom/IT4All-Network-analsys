from typing import Union

from pydantic import BaseModel
from datetime import date


class Network(BaseModel):
    id: Union[int, None] = None
    client_id: int
    location_name: str = "ירושלים"
    date_taken: str


class Device(BaseModel):
    id: Union[int, None] = None
    network_id: int
    ip: str
    Mac: str
    Name:Union[str, None] = "Device"
    Vendor:str
    Info:Union[str, None]=None


