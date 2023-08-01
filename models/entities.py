from typing import Union
import re

from pydantic import BaseModel
from datetime import date
from typing import Union

from pydantic import BaseModel, field_validator, validator, root_validator
from datetime import date, datetime


class Network(BaseModel):
    id: Union[int, None] = None
    client_id: int
    location_name: str = "ירושלים"
    date_taken: Union[date, str]

    @field_validator('date_taken')
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        else:
            try:
                return datetime.strptime(value, '%d/%m/%Y').date()
            except ValueError as e:
                raise ValueError("Invalid date format. Date should be in the format 'dd/mm/yyyy'.")


class Device(BaseModel):
    NetworkID: int
    IP: str
    Mac: str
    Name: Union[str, None] = "Device"
    Vendor: str = "vendor"
    Info: Union[str, None] = None


class Connection(BaseModel):
    SourceMac: str
    DestMac: str
    ProtocolName: str
    Length: int
    Time: str

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return False
        return (self.SourceMac, self.DestMac) == (other.SourceMac, other.DestMac)

    def __hash__(self):
        return hash((self.SourceMac, self.DestMac))


class User(BaseModel):
    ID: int = None
    FirstName: Union[str, None]
    LastName: Union[str, None] = None
    Email: str
    RoleName: Union[str, None] = "technician"

    @field_validator('Email')
    def validate_email(cls, value):
        if not cls.is_valid_email(value):
            raise ValueError("Invalid email address")
        return value

    @classmethod
    def is_valid_email(cls, email):
        # Regular expression for email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))


class UserInDB(User):
    HashedPassword: str


class UserLogin(User):
    RoleName: Union[str, None]
    Password: Union[str, None]


class Client(User):
    Address: Union[str, None]
    Phone: Union[str, None]
