from typing import Union

from pydantic import BaseModel, field_validator, validator, root_validator
from datetime import date, datetime


class Network(BaseModel):
    # id: int
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


# network = Network(client_id=1, location_name="new york", date_taken="02/02/1950")


